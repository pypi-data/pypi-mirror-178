'''
========================================
Declassed Tor Circuits Manager version 2
========================================

Maintain the specified number of circuits and attach streams to them in a round-robin manner.

How to use:

.. code:: python

    from dtcm2 import TorCircuitsManager

    async with TorCircuitsManager('127.0.0.1', 9051, 'my-secret-password',
                                  hops=2, num_circuits=500) as tcm:
        await tcm.run()

Mind exceptions and re-run this block when shit happens. Up to you.

This module uses torcontrol.
See also Stem-based version 1: https://declassed.art/repository/dtcm

:copyright: Copyright 2022 AXY axy@declassed.art
:license: LGPLv3, see LICENSE for details.
'''

__version__ = '2.0.2'

import asyncio
import random
import time
import traceback

from torcontrol import TorController, OperationFailed, parsers

class TorCircuitsManager(TorController):

    def __init__(self, host, port, password, hops=2, num_circuits=100, stable_only=False, fast_only=False):
        # settings
        self.password = password
        self.hops = hops
        self.num_circuits = num_circuits
        self.stable_only = stable_only
        self.fast_only = fast_only

        # circuits to assign to streams in round robin manner
        self._circuit_ids = []
        self._circuit_index = 0

        # managed circuits
        self._circuit_paths = dict()  # all paths, either for circuits in-use or just being created
        self._circuits_awaiting_creation = set()  # circuits being created

        # relay info
        self._exit_fingerprints = None
        self._middle_fingerprints = None
        self._guard_fingerprints = None
        self._fingerprints_last_updated = None

        super().__init__(host, port)

    async def run(self):
        '''
        Run circuits manager.
        '''
        # start monitor task
        monitor_task = asyncio.create_task(self._monitor())

        try:
            # setup Tor
            await self.authenticate(self.password)
            await self._update_fingerprints()

            # we need CIRC and STREAM events
            await self.set_events('CIRC', 'STREAM')

            await self._collect_existing_cirsuits()

            # leave stream management to us
            await self.set_conf('__LeaveStreamsUnattached', '1')
            try:
                # maintain the requested number of circuits.
                create_this_many_circuits_in_parallel = max(3, self.num_circuits // 10)
                while True:
                    await asyncio.sleep(1)
                    if monitor_task.done():
                        break

                    circuits_needed = self.num_circuits - len(self._circuit_paths)
                    if circuits_needed <= 0:
                        # enough circuits created, nothing to do
                        continue

                    circuits_todo = min(circuits_needed, create_this_many_circuits_in_parallel)
                    if circuits_todo <= 0:
                        # enough circuits in progress, nothing to do
                        continue

                    for i in range(circuits_todo):
                        # create new path
                        path = self._create_path()
                        if path is None:
                            # not enough relays, re-try later
                            break
                        # start creating circuit
                        self.log_info(f'Creating new circuit {path}')
                        try:
                            circuit_id = await self.extend_circuit('0', path)
                        except OperationFailed as e:
                            self.log_error(e)
                            continue
                        self._circuit_paths[circuit_id] = path
                        self._circuits_awaiting_creation.add(circuit_id)

                    if time.monotonic() - self._fingerprints_last_updated > 3600:
                        self._update_fingerprints()

            finally:
                try:
                    await self.set_conf('__LeaveStreamsUnattached', '0')
                except Exception:
                    self.log_error(traceback.format_exc())

        finally:
            # cancel monitor tasks and wait for completion, this also propagates exceptions, if any
            monitor_task.cancel()
            await monitor_task

    async def _monitor(self):
        '''
        Internal background task.
        Check control connection.
        '''
        while True:
            await asyncio.sleep(5)
            await self.send_command('GETINFO version')

    async def _update_fingerprints(self):
        '''
        Update fingerprints of relays.
        '''
        new_guards = []
        new_middles = []
        new_exits = set()
        async for desc in self.get_network_statuses():
            if self.stable_only and 'Stable' not in desc['flags']:
                continue
            if self.fast_only and 'Fast' not in desc['flags']:
                continue
            # at first, collect exit nodes
            if 'Exit' in desc['flags']:
                new_exits.add(desc['fingerprint'])
                continue
            # there are a lot of guard nodes, and on the one hand the following approach has to be changed to choose less guards
            # but on the other hand that's not bad for short circuits that don't need anonymity
            if 'Guard' in desc['flags'] and desc['fingerprint'] not in new_exits:
                new_guards.append(desc['fingerprint'])
            else:
                new_middles.append(desc['fingerprint'])
        self.log_info(f'{len(new_guards)} guard, {len(new_middles)} middle, {len(new_exits)} exit relays')
        self._guard_fingerprints = new_guards
        self._middle_fingerprints = new_middles
        self._exit_fingerprints = list(new_exits)
        self._fingerprints_last_updated = time.monotonic()

    async def _collect_existing_cirsuits(self):
        '''
        Get existing circuits and collect those that have requested number of hops.
        '''
        async for circ in self.get_circuits():
            if circ['status'] != 'BUILT':
                continue
            if circ['purpose'] != 'GENERAL':
                continue
            if len(circ['path']) == self.hops:
                self._circuit_ids.append(circ['id'])
                self._circuit_paths[circ['id']] = circ['path']
                self.log_info(f'Using existing circuit {circ["id"]}')

    async def handle_event(self, event):
        '''
        Asynchronous event handler.
        '''
        event_type = parsers.extract_event_type(event)
        if event_type == 'CIRC':
            circuit = parsers.parse_circuit_event(event)
            self._handle_circuit(circuit)
        elif event_type == 'STREAM':
            stream = parsers.parse_stream_event(event)
            await self._handle_stream(stream)
        else:
            super().handle_event(event)

    def _handle_circuit(self, circuit):
        if circuit['status'] == 'BUILT':
            num_hops = len(circuit['path'])
            if num_hops != self.hops:
                self.log_info(f'Rejecting created {num_hops}-hops circuit {circuit["id"]}')
                self._forget_circuit(circuit['id'])
            else:
                self.log_info(f'Using created {num_hops}-hops circuit {circuit["id"]}')
                self._circuit_created(circuit['id'])
        elif circuit['status'] in ['CLOSED', 'FAILED']:
            if circuit['status'] == 'CLOSED':
                self.log_info(f'Closed circuit {circuit["id"]}')
            elif circuit['status'] == 'FAILED':
                self.log_info(f'Failed circuit {circuit["id"]}')
            self._forget_circuit(circuit["id"])

    async def _handle_stream(self, stream):
        if stream['status'] == 'NEW':
            # Don't stuck in here for too long, three attempts only.
            # Tor spec says: Tor will close unattached streams by itself,
            # roughly two minutes after they are born.
            for attempt in range(3):
                circuit_id = self._get_circuit_for_stream()
                if circuit_id is None:
                    # oops, no circuits!
                    self.log_error(f'No circuits to attach stream {stream["id"]} to')
                    await asyncio.sleep(1)
                    continue
                try:
                    await self.attach_stream(stream['id'], circuit_id)
                    self.log_info(f'Attached stream {stream["id"]} to circuit {circuit_id}')
                    return
                except OperationFailed as e:
                    if e.code == '551':
                        # 551 Can't attach stream for some reason. Try again.
                        self.log_error(e)
                        continue
                    elif e.code == '552':
                        # 552 Unknown circuit or stream.
                        self.log_error(e)
                        if e.message.startswith('Unknown circuit'):
                            # unknown circuit, try again
                            continue
                        else:
                            # unknown stream?
                            break
                    elif e.code == '555':
                        # 555 Connection is not managed by controller.
                        self.log_error(e)
                        break
                    else:
                        raise
            self.log_error(f'Failed attaching stream {stream["id"]} to circuit {circuit_id}')

    def _get_circuit_for_stream(self):
        # get a circuit for new stream
        if len(self._circuit_ids) == 0:
            return None
        if self._circuit_index >= len(self._circuit_ids):
            self._circuit_index = 0
        circuit_id = self._circuit_ids[self._circuit_index]
        self._circuit_index = (self._circuit_index + 1) % len(self._circuit_ids)
        return circuit_id

    def _circuit_created(self, circuit_id):
        # move circuit from the set of circuits awaiting creation to the list of available circuits
        self._circuit_ids.append(circuit_id)
        if circuit_id in self._circuits_awaiting_creation:
            self._circuits_awaiting_creation.remove(circuit_id)

    def _forget_circuit(self, circuit_id):
        # remove circuit from all internal structures
        try:
            self._circuit_ids.remove(circuit_id)
        except ValueError:
            pass
        if circuit_id in self._circuits_awaiting_creation:
            self._circuits_awaiting_creation.remove(circuit_id)
        if circuit_id in self._circuit_paths:
            del self._circuit_paths[circuit_id]

    def _create_path(self):
        # create path for new circuit
        fingerprints_in_use = set()
        for fingerprints in self._circuit_paths.values():
            fingerprints_in_use.update(fingerprints)
        path = []
        if self.hops > 1:
            guards = list(set(self._guard_fingerprints) - fingerprints_in_use)
            if len(guards) == 0:
                self.log_info(f'All available {len(self._guard_fingerprints)} guard relays are in use')
                return None
            guard = random.choice(guards)
            path.append(guard)

        while len(path) < self.hops - 1:
            middles = list(set(self._middle_fingerprints) - fingerprints_in_use - set(path))
            if len(middles) == 0:
                self.log_info(f'All available {len(self._middle_fingerprints)} middle relays are in use')
                return None
            middle = random.choice(middles)
            path.append(middle)

        exits = list(set(self._exit_fingerprints) - fingerprints_in_use - set(path))
        if len(exits) == 0:
            self.log_info(f'All available {len(self._exit_fingerprints)} exit relays are in use')
            return None
        exit = random.choice(exits)
        path.append(exit)
        return path

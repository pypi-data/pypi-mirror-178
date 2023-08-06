'''
Minimalistic Tor Controller

This module contains TorCommands mixin that implements controller commands.

:copyright: Copyright 2022 AXY axy@declassed.art
:license: LGPLv3, see LICENSE for details.
'''

from . import parsers


class OperationFailed(Exception):

    def __init__(self, reply, description):
        code = '???'
        message = '???'
        if len(reply):
            code = reply[0][:3]
            message = reply[0][4:]
        self.code = code
        self.message = message
        self.description = description

    def __str__(self):
        return f'{self.description} {self.code}: {self.message}'

class TorCommands:
    '''
    A mixin that implements controller commands.
    '''

    async def authenticate(self, password):
        '''
        Authenticate client.
        XXX implement all authentication methods.
        '''
        # XXX check password authentication is supported
        # await c.send_command('PROTOCOLINFO 1'))

        password = password.replace('"', '\\"')
        reply = await self.send_command(f'AUTHENTICATE "{password}"')
        if reply != ['250 OK']:
            raise OperationFailed(reply, 'Authentication failed')

    async def get_network_statuses(self):
        '''
        Yiels relay descriptors.
        '''
        reply = await self.send_command('GETINFO ns/all')
        if reply == ['250-ns/all=', '250 OK']:
            return
        if reply[0] != '250+ns/all=':
            raise OperationFailed(reply, f'Unexpected reply: {reply[0]}')

        desc = None
        for line in reply[1:]:
            if line == '.':
                break

            parts = line.split()

            # get and run parser method
            parse = getattr(parsers, f'_parse_{parts[0]}_line')
            data_dict = parse(parts[1:])

            if parts[0] == 'r':
                # a descriptor starts with r line, yield previous one if any
                if desc is not None:
                    yield desc
                desc = data_dict
            else:
                # update current descriptor with the data, concat lists and merge dicts and sets
                for k, v in data_dict.items():
                    if k in desc:
                        if isinstance(desc[k], list) and isinstance(v, list):
                            desc[k].extend(v)
                        elif isinstance(desc[k], dict) and isinstance(v, dict):
                            desc[k].update(v)
                        elif isinstance(desc[k], set) and isinstance(v, set):
                            desc[k].update(v)
                        else:
                            raise Exception(f'Duplicate data in descriptor: {k}={desc[k]}; {k}={v}')
                    else:
                        desc[k] = v

        # yield the last descriptor
        if desc is not None:
            yield desc

    async def get_circuits(self):
        '''
        Yield currently available circuits.
        '''
        reply = await self.send_command('GETINFO circuit-status')
        if reply == ['250-circuit-status=', '250 OK']:
            return
        if reply[0] != '250+circuit-status=':
            raise OperationFailed(reply, f'Unexpected reply: {reply[0]}')

        for line in reply[1:]:
            if line == '.':
                break
            yield parsers.parse_circuit_status(line)

    async def extend_circuit(self, circuit_id, path=None, purpose=None):
        '''
        Extend or create circuit.
        Return id of circuit to be extended or created.
        The caller should process CIRC events to get further status.
        '''
        args = [circuit_id]
        if path:
            args.append(','.join(path))
        if purpose:
            args.append(purpose)
        reply = await self.send_command(f'EXTENDCIRCUIT {" ".join(args)}')
        if reply[0].startswith('250 EXTENDED'):
            return reply[0].rsplit(' ', 1)[-1]
        else:
            raise OperationFailed(reply, f'Unexpected reply: {reply}')

    async def set_events(self, *event_codes):
        '''
        event_codes may start with EXTENDED according to torspec
        '''
        if event_codes:
            command = f'SETEVENTS {" ".join(event_codes)}'
        else:
            command = 'SETEVENTS'
        reply = await self.send_command(command)
        if reply != ['250 OK']:
            raise OperationFailed(reply, 'Cannot set events')

    async def set_conf(self, key, value):
        '''
        Change the value of Tor configuration variable.
        '''
        reply = await self.send_command(f'SETCONF {key}="{value}"')
        if reply != ['250 OK']:
            raise OperationFailed(reply, f'Cannot set {key}={value}')

    async def attach_stream(self, stream_id, circuit_id):
        reply = await self.send_command(f'ATTACHSTREAM {stream_id} {circuit_id}')
        if reply != ['250 OK']:
            raise OperationFailed(reply, f'Cannot attach stream {stream_id} to circuit {circuit_id}')

'''
Minimalistic Tor Controller

This module contains TorConnection which provides two basic methods:
* send_command
* handle_event, you need to override it in your subclass

:copyright: Copyright 2022 AXY axy@declassed.art
:license: LGPLv3, see LICENSE for details.
'''

import asyncio
import sys
import traceback

class TorConnection:
    '''
    The basic connection to Tor control port.
    Provides send_command method.
    The basic handle_event method simply logs asynchronous replies.
    '''

    def __init__(self, host, port):
        self.host = host
        self.port = port

        # serialize commands to the controller
        self._command_lock = asyncio.Lock()

        # log errors to:
        self.error_logfile = None

    async def __aenter__(self):
        '''
        Enter the runtime context: prepare the instance to work with Tor.
        '''
        # create queues for replies
        self._sync_reply_queue = asyncio.Queue()
        self._async_reply_queue = asyncio.Queue()

        # connect to Tor control port
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)

        # start background tasks
        self._events_handler_task = asyncio.create_task(self._events_handler())
        self._receiver_task = asyncio.create_task(self._receiver())

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        '''
        Exit the runtime context: stop working with Tor.
        '''
        # Close connection. This forces self._reader.read functions to return empty data,
        # so receiver task can gracefully stop.
        self._writer.close()
        await self._writer.wait_closed()

        # wait for background tasks to complete
        await self._events_handler_task
        await self._receiver_task

    async def _events_handler(self):
        '''
        Internal background task.
        Get events from async reply queue and call handle_event method.
        '''
        try:
            while True:
                try:
                    event = await self._async_reply_queue.get()
                    if event is None:
                        return
                    else:
                        try:
                            await self.handle_event(event)
                        except Exception as e:
                            self.log_error(e)
                except asyncio.CancelledError:
                    # suppress this for proper cleanup in __aexit__
                    pass
        except Exception:
            self.log_error(traceback.format_exc())

    async def _receiver(self):
        '''
        Internal background task.
        Receive replies from Tor.
        '''
        try:
            reply = []  # collect reply lines here before pushing to a queue
            multiline_value = False

            while True:
                try:
                    # get line
                    line = await self._reader.readline()
                    if line == b'':
                        # connection closed, put markers to stop background tasks
                        self._sync_reply_queue.put_nowait(None)
                        self._async_reply_queue.put_nowait(None)
                        return

                    # process line, add to reply
                    line = line.rstrip(b'\n').rstrip(b'\r').decode('ascii')
                    self.log_debug('>>>', line)
                    reply.append(line)
                    if multiline_value:
                        if line == '.':
                            multiline_value = False
                        continue
                    if line[3] != ' ':
                        # intermediate line
                        if line[3] == '+' and line.endswith('='):
                            multiline_value = True
                        continue

                    # got end reply line, put reply to the appropriate queue
                    if line.startswith('6'):
                        queue = self._async_reply_queue
                    else:
                        queue = self._sync_reply_queue
                    queue.put_nowait(reply)
                    reply = []
                except asyncio.CancelledError:
                    # suppress this for proper cleanup in __aexit__
                    pass
        except ConnectionResetError:
            # connection closed, put markers to stop background tasks
            self._sync_reply_queue.put_nowait(None)
            self._async_reply_queue.put_nowait(None)
        except Exception:
            self.log_error(traceback.format_exc())

    async def send_command(self, command):
        '''
        Send command and return reply.
        '''
        async with self._command_lock:
            # Make sure _sync_reply_queue contains no data.
            # However, it may contain None if connection is closed.
            if not self._sync_reply_queue.empty():
                reply = self._sync_reply_queue.get_nowait()
                if reply is None:
                    # Connection was closed by peer, sending the command does not make sense.
                    # Keep None in the queue to cancel any future calls.
                    self._sync_reply_queue.put_nowait(None)
                    raise ConnectionResetError()
                else:
                    raise Exception(f'Unexpected reply: {reply}')

            # send command
            self.log_debug('###', command)
            self._writer.write(command.encode('ascii') + b'\r\n')
            await self._writer.drain()

            # await reply
            reply = await self._sync_reply_queue.get()
            if reply is None:
                # Keep None in the queue to cancel any future calls.
                self._sync_reply_queue.put_nowait(None)
                raise ConnectionResetError()
            else:
                return reply

    async def handle_event(self, event):
        '''
        Override and customize this method in a subclass, if necessary.
        '''
        self.log_error('Unhandled event:\n', '\n'.join(event))

    def log_debug(self, *msg):
        '''
        Override and customize this method in a subclass, if necessary.
        '''
        #print(*msg)
        pass

    def log_info(self, *msg):
        '''
        Override and customize this method in a subclass, if necessary.
        '''
        print(*msg)

    def log_error(self, *msg):
        '''
        Override and customize this method in a subclass, if necessary.
        '''
        print(*msg, file=sys.stderr)
        if self.error_logfile:
            print(*msg, file=self.error_logfile)
            self.error_logfile.flush()

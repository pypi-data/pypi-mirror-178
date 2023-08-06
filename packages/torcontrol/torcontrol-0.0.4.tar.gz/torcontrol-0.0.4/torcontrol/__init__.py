'''
===========================
Minimalistic Tor Controller
===========================

A minimalistic asyncio-based Tor controller.

How to use:

.. code:: python

    from torcontrol import TorController

    async with TorController('127.0.0.1', 9051) as tc:
        await tc.authenticate('my-secret-password')
        async for circuit in tc.get_circuits():
            print(circuit)

This controller neither does nor will implement auto reconnect.
It's the user's responsibility to catch any exceptions
and re-run the entire "async with TorContrller..." code block.

All response parsing is very minimalistic. E.g. date/time strings are not parsed.

Currently this project is at alpha stage because only small
subset of commands is implemented for this particular project:
https://declassed.art/repository/dtcm2

:copyright: Copyright 2022 AXY axy@declassed.art
:license: LGPLv3, see LICENSE for details.
'''

__version__ = '0.0.4'

from .connection import TorConnection
from .commands import TorCommands, OperationFailed
from . import parsers

class TorController(TorConnection, TorCommands):
    pass

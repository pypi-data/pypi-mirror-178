'''
Asoke: a simple class-based dispatcher and a quickstart wrapper.

For now, this initial version is intended to build API only.

:copyright: Copyright 2022 AXY axy@declassed.art
:license: BSD, see LICENSE for details.
'''

__version__ = '0.0.2'

from .app import quickstart
from .dispatcher import build_request_handlers, expose, dispatch
from .errors import APIError

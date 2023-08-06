'''
Exceptions and exception handling.

:copyright: Copyright 2022 AXY axy@declassed.art
:license: BSD, see LICENSE for details.
'''

class APIError(Exception):

    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description

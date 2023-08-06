'''
Class-based dispatcher for ASGI.

:copyright: Copyright 2022 AXY axy@declassed.art
:license: BSD, see LICENSE for details.
'''

import logging
import traceback
import types

from starlette.requests import Request
from starlette.responses import JSONResponse

from .errors import APIError

def expose(*args, **expose_params):
    '''
    The decorator is intended for use with class methods to
    mark them as 'exposed' with `expose_params`.

    Exposed methods are collected by `build_request_handlers`.
    '''

    def prepare_expose_params():
        '''
        Sanitize some known `expose_params`.
        '''
        # set default methods to POST
        params = expose_params.copy()
        if 'methods' in params:
            methods = params['methods']
            if isinstance(methods, str):
                methods = [m.upper() for m in methods.split()]
        else:
            methods = ['POST']
        params['methods'] = set(methods)
        return params

    def decorator(func):

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.exposed = dict(**prepare_expose_params())
        return wrapper

    if len(args) and isinstance(args[0], types.FunctionType):
        return decorator(args[0])
    else:
        return decorator

def build_request_handlers(root, base_uri):
    '''
    Build request handlers from `root` object.
    The result is a dict where keys are URIs and values are request handlers.
    '''
    def collect_exposed_methods(obj, path, handlers):
        for name in dir(obj):
            if not name.startswith('__'):
                value = getattr(obj, name)
                if callable(value) and hasattr(value, 'exposed'):
                    method_name = value.exposed.get('name', name)
                    handlers[f'{path}/{method_name}'] = value
                elif hasattr(obj, '__dict__'):
                    collect_exposed_methods(value, f'{path}/{name}', handlers)

    handlers = dict()
    collect_exposed_methods(root, base_uri.rstrip('/'), handlers)
    return handlers

async def dispatch(scope, handlers, receive, send):
    '''
    Dispatch ASGI request.

    XXX currently for API only, need to rethink error handling
    '''
    request = Request(scope, receive)

    # get request handler
    path = request['path']
    if path not in handlers:
        response = JSONResponse(dict(status='error', description='Bad endpoint'), status_code=404)
        await response(scope, receive, send)
        return

    handler = handlers[path]

    # allow specific methods only
    if request.method not in handler.exposed['methods']:
        response = JSONResponse(dict(status='error', description='Method not allowed'), status_code=405)
        await response(scope, receive, send)
        return

    # call request handler
    try:
        response = await handler(request)
    except APIError as e:
        response = JSONResponse(dict(status='error', description=e.description), status_code=e.status_code)
    except Exception:
        response = JSONResponse(dict(status='error', description='Server error'), status_code=500)
        logging.error(traceback.format_exc())
    await response(scope, receive, send)

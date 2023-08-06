'''
Application module.

:copyright: Copyright 2022 AXY axy@declassed.art
:license: BSD, see LICENSE for details.
'''

import asyncio

import hypercorn
import hypercorn.asyncio
import uvloop

from .dispatcher import build_request_handlers, dispatch


def quickstart(root, config={}, base_uri='/', on_startup=None, on_shutdown=None):
    '''
    Create and run web application.
    '''
    handlers = build_request_handlers(root, base_uri)
    hconf = hypercorn.config.Config.from_mapping(config)

    async def main():

        async def app(scope, receive, send):
            '''
            ASGI application based on Starlette Request and responses.
            '''
            if scope['type'] == 'lifespan':
                while True:
                    message = await receive()
                    if message['type'] == 'lifespan.startup':
                        if on_startup:
                            await on_startup()
                        await send({'type': 'lifespan.startup.complete'})
                    elif message['type'] == 'lifespan.shutdown':
                        if on_shutdown:
                            await on_shutdown()
                        await send({'type': 'lifespan.shutdown.complete'})
                        return

            await dispatch(scope, handlers, receive, send)

        await hypercorn.asyncio.serve(app, hconf)

    uvloop.install()
    asyncio.run(main())

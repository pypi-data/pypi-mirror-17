"""
Asphalt framework mixin for Kyokai.
"""
import logging

import asyncio
from functools import partial
from typing import Union

from asphalt.core import Component, resolve_reference, Context
from typeguard import check_argument_types

from kyoukai.app import Kyoukai
from kyoukai.protocol import KyoukaiProtocol
from kyoukai.context import HTTPRequestContext

logger = logging.getLogger("Kyoukai")


class KyoukaiComponent(Component):
    def __init__(self, app: Union[str, Kyoukai], ip: str = '0.0.0.0', port: int = 4444, **cfg):
        assert check_argument_types()
        if not isinstance(app, Kyoukai):
            self.app = resolve_reference(app)
        else:
            self.app = app
        self.ip = ip
        self.port = port
        self._extra_cfg = cfg

        # Reconfigure the app with the extra config.
        self.app.reconfigure(**self._extra_cfg)

        self.server = None

    def get_protocol(self, ctx: Context):
        return KyoukaiProtocol(self.app, ctx)

    async def start(self, ctx: Context):
        """
        Starts a Kyokai server.
        """
        # Call on_startup.
        await self.app.call_on_startup()
        # Put the config on the HTTPRequestContext.
        HTTPRequestContext.cfg = self.app.config

        # Start serving on the specified ports.
        protocol = partial(self.get_protocol, ctx)
        self.server = await asyncio.get_event_loop().create_server(protocol, self.ip, self.port)
        logger.info("Kyoukai serving on {}:{}.".format(self.ip, self.port))

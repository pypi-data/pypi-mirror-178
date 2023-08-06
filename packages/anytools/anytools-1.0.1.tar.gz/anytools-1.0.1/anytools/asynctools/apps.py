import asyncio
import signal

from anytools.asynctools.common import (
    add_dummy_signal_handler,
    add_shutdown_signal_handler,
)


class BaseAsyncApplication:
    async def async_init(self, signals=[signal.SIGINT]):
        self._signals = signals
        add_dummy_signal_handler(self._signals, reason="init")
        await self._async_init()
        add_shutdown_signal_handler(self._signals)

    async def async_run(self):
        await self._async_run()

    async def async_close(self):
        add_dummy_signal_handler(self._signals, reason="close")
        await self._async_close()

    async def _async_init(self):
        raise NotImplemented

    async def _async_run(self):
        raise NotImplemented

    async def _async_close(self):
        raise NotImplemented

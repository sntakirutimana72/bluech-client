import asyncio as io

class DummyServer:
    handle: io.base_events.Server | None = None
    host = 'localhost'
    port = 8000

    async def initiate(self, callback=None):
        if callback is None:
            callback = io.coroutine(lambda r, w: ...)
        handle = await io.start_server(callback, host=self.host, port=self.port)
        self.handle = handle

    async def terminate(self):
        if handle := self.handle:
            handle.close()
            await handle.wait_closed()
        self.handle = None


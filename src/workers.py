import asyncio as io
import threading as rd
import typing as tip

from kivy.clock import mainthread
from kivy.event import EventDispatcher

class Base(EventDispatcher):
    loop: io.AbstractEventLoop
    reader: io.StreamReader | None
    writer: io.StreamWriter | None

    OUTS_Q = io.Queue()
    OUTS_LCK = io.Lock()
    INS_Q = io.Queue()
    INS_LCK = io.Lock()

    @mainthread
    def delegate(self, action, **kwargs):
        self.dispatch(action, **kwargs)

class SessionUnit(Base):
    user: dict[str, tip.Any] | None
    is_authenticated = False
    session_lock = io.Lock()

    async def signin(self):
        ...

    async def signout(self):
        ...

    async def set_session(self, user):
        async with self.session_lock:
            self.user = user
            self.is_authenticated = bool(user)

class ConfiguratorUnit(SessionUnit):
    def configure(self):
        self.loop = io.get_event_loop_policy().new_event_loop()
        io.set_event_loop(self.loop)
        self.loop.create_task(self.pulse())
        self.loop.run_forever()

    @staticmethod
    async def pulse():
        while True:
            await io.sleep(5)

class QueuePosterUnit(ConfiguratorUnit):
    def post_payload(self, **kwargs):
        loop = self.loop
        while loop is None:
            loop = self.loop
        loop.call_soon_threadsafe(self.threadsafe_poster, kwargs)

    def threadsafe_poster(self, payload: dict[str, tip.Any]):
        self.loop.create_task(self.poster(**payload))

    async def poster(self, **kwargs):
        await self.OUTS_Q.put(kwargs)

class ProcessorUnit(QueuePosterUnit):
    async def establish_connection(self):
        is_connected = None
        while is_connected is None:
            try:
                reader, writer = await io.open_connection()
            except:
                await io.sleep(10)
                continue
            is_connected = True
            self.reader = reader
            self.writer = writer
            io.create_task(self.signin())

class Worker(ConfiguratorUnit):
    __events__ = (
        'on_connected',
        'on_disconnected',
        'on_response',
        'on_status'
    )

    def on_connected(self, **kwargs):
        ...

    def on_disconnected(self, **kwargs):
        ...

    def on_response(self, **kwargs):
        ...

    def on_status(self, **kwargs):
        ...

    def __init__(self):
        super().__init__()
        self.engine = rd.Thread(target=self.configure, daemon=True)

    def ignite(self):
        self.engine.start()

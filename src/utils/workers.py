import asyncio as io
import threading as rd
import typing as tip

from kivy.clock import mainthread
from kivy.event import EventDispatcher

from .logger import Logger

class Base(EventDispatcher):
    loop: io.AbstractEventLoop
    is_connected = None
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

    async def establish_connection(self):
        try:
            Logger.info('Attempting to establish connection with server')
            self.delegate('on_status', status='connecting')
            await io.sleep(1.75)
            reader, writer = await io.open_connection(host='localhost', port=8090)
        except:
            Logger.error()
            await io.sleep(1.75)
            self.delegate('on_status', status='offline')
        else:
            Logger.info('Connection with server established [success]')
            self.reader = reader
            self.writer = writer
            self.is_connected = True
            self.delegate('on_status', status='online')

    async def pulse(self):
        while True:
            if self.is_connected is None:
                await self.establish_connection()
            await io.sleep(20)

class QueuePosterUnit(ConfiguratorUnit):
    def post_job(self, **job):
        loop = self.loop
        while loop is None:
            loop = self.loop
        loop.call_soon_threadsafe(self.post_job_safely, job)

    def post_job_safely(self, payload: dict[str, tip.Any]):
        self.loop.create_task(self.post_in_queue(**payload))

    async def post_in_queue(self, **kwargs):
        await self.OUTS_Q.put(kwargs)

class ProcessorUnit(QueuePosterUnit):
    ...

class Worker(ProcessorUnit):
    __events__ = (
        'on_signed_in',
        'on_signed_out',
        'on_response',
        'on_status',
    )

    def on_signed_in(self, **kwargs):
        ...

    def on_signed_out(self, **kwargs):
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

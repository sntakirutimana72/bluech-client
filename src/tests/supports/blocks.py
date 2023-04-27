import contextlib as xlib

from .utils import get_event_loop, get_callback
from .mocks.servers import DummyServer

@xlib.contextmanager
def async_block():
    event = get_event_loop()
    yield event
    event.close()

@xlib.contextmanager
def async_exc(fn, *args, **kwargs):
    with async_block() as e:
        future = get_callback(fn, *args, **kwargs)
        result = e.run_until_complete(future)
        yield result

@xlib.contextmanager
def async_serve(server: DummyServer):
    with async_block() as e:
        e.run_until_complete(server.initiate())
        yield e.run_until_complete
        e.run_until_complete(server.terminate())

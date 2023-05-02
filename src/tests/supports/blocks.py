import contextlib as xlib

from .utils import get_event_loop, get_callback

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

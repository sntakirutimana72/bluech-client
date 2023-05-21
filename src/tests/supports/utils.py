import platform
import asyncio as io

def get_callback(fn, *args, **kwargs):
    if not (args or kwargs):
        return fn()
    elif args and kwargs:
        return fn(*args, **kwargs)
    elif args:
        return fn(*args)
    else:
        return fn(**kwargs)

def get_event_loop():
    if platform.system() == 'Windows':
        # As pytest with asyncio throws occasional RuntimeError('Event loop is closed') on Windows oses,
        # I'm setting windows loop event policy to avoid this issue.
        # It happens when working with sockets and streams
        io.set_event_loop_policy(io.WindowsSelectorEventLoopPolicy())
    return io.get_event_loop_policy().new_event_loop()

def get_cls(instance):
    return instance.__class__

def get_cls_name(cls: type):
    return cls.__name__

def get_instance_cls_name(instance: object):
    cls = get_cls(instance)
    return get_cls_name(cls)

class Mocks:
    class Users:
        @staticmethod
        def regular():
            return {
                'email': 'regular@email.test',
                'nickname': 'regular',
                'pass_w': '@12345!',
                'id': 7089
            }

    class Responses:
        @staticmethod
        def signedIn(user=None):
            if user is None:
                user = Mocks.Users.regular()
                del user['pass_w']
            return {'proto': 'connected', 'user': user}

        @staticmethod
        def error500(status=400):
            return {'proto': 'invalid_request', 'message': f'{status}: Invalid Request'}

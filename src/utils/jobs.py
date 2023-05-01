from ..settings import ENDPOINT_PROTOCOLS

class AnyJobs(object):
    @staticmethod
    def any_job(proto: str, **kwargs):
        default_job = {
            'proto': ENDPOINT_PROTOCOLS[proto],
            'content_size': 0,
            'content_type': '',
            'request': kwargs
        }
        return default_job

class AuthJobs(AnyJobs):
    @classmethod
    def signin(cls, credentials: dict[str]):
        signin_req = {'body': {'user': credentials}}
        signin_job = cls.any_job('signin', **signin_req)
        return signin_job

    @classmethod
    def signout(cls):
        signout_job = cls.any_job('signout')
        return signout_job

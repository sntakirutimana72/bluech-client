import importlib.util as utils
import traceback as trace

from ..settings import BASE_DIR, DYNAMIC_IMPORTS

# noinspection PyBroadException
def require(name, lookup_packages=None):
    """
    imports any module relatively to the :param ~ lookup_packages, which is used as a focal point to find
    the module whose name is :param ~ module_name. It raises and importError if nothing is found.

    :param name ~ it's a name used to find a module, and it must be of `<class str>` type.
    :param lookup_packages
    :return:
    """
    try:
        if lookup_packages is None:
            lookup_packages = []
        spec = utils.spec_from_file_location(
            name=DYNAMIC_IMPORTS[name],
            location=BASE_DIR.joinpath(*lookup_packages, f'{name}.py')
        )
        module = utils.module_from_spec(spec)
        spec.loader.exec_module(module)
    except:
        trace.print_exc()
        raise ImportError
    return module

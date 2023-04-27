import time
import re
import asyncio as aio
import inspect

from kivy.uix.widget import Widget as Wid

from .utils import get_cls_name, get_cls

class ElementsSelector(object):
    @staticmethod
    def is_timed(timeout, now):
        if timeout is None:
            return True
        return timeout > time.time() - now

    @classmethod
    def select_element(cls, tree: Wid, matcher_cb):
        if matcher_cb(tree):
            return tree
        for node in tree.children[:]:
            if matcher_cb(node):
                return node
            elif target := cls.select_element(node, matcher_cb):
                return target

    @classmethod
    async def find_any(cls, tree: Wid, matcher_cb, timeout=None):
        now = time.time()
        while cls.is_timed(timeout, now):
            if result := cls.select_element(tree, matcher_cb):
                return result
            await aio.sleep(1/6)

    @classmethod
    async def find_by_text(cls, tree: Wid, pattern: str, timeout=None):
        def callback(node: Wid):
            if hasattr(node, 'text'):
                regex = re.compile(pattern, re.IGNORECASE)
                return regex.search(node.text)

        result = await cls.find_any(tree, callback, timeout)

        return result

    @classmethod
    async def find_by_role(cls, tree: Wid, role: str, timeout=None):
        def get_lineage(instance: object):
            mro_cls = inspect.getmro(get_cls(instance))
            yield from mro_cls

        def callback(node: Wid):
            regex = re.compile(rf'^{role}$', re.IGNORECASE)
            for a_cls in get_lineage(node):
                if regex.search(get_cls_name(a_cls)):
                    return True

        result = await cls.find_any(tree, callback, timeout)

        return result

from .supports.unittest import GUnittest
from .supports.blocks import async_exc

class AppTestCase(GUnittest):
    def test_successfully_rendered(self):
        self.build()
        with async_exc(self.find_by_role, self.root, 'PagesManager') as element:
            self.assertEqual(self.manager, element)

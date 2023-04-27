from .supports.utils import get_instance_cls_name
from .supports.blocks import async_exc
from .supports.unittest import GUnittest

class IndexTestCases(GUnittest):
    def test_display_label(self):
        self.build()
        with async_exc(self.find_by_text, self.current_page, r'bluech.+client') as element:
            self.assertIsNotNone(element)

    def test_has_stat_element(self):
        self.build()
        with async_exc(self.find_by_role, self.current_page, 'StatWidget') as element:
            self.assertEqual(get_instance_cls_name(element), 'StatWidget')

    def test_stat_element_when_offline(self):
        self.build()
        with async_exc(self.find_by_role, self.current_page, 'StatWidget') as element:
            self.assertEqual(element.ring_image, 'offline')
            index_page = self.current_page
            index_page.on_status(status='connecting')
            self.assertEqual(element.ring_image, 'connecting')
            index_page.on_status(status='offline')
            self.assertEqual(element.ring_image, 'offline')

    def test_stat_element_when_online(self):
        self.build()
        with async_exc(self.find_by_role, self.current_page, 'StatWidget') as element:
            index_page = self.current_page
            index_page.on_status(status='connecting')
            index_page.on_status(status='online')
            self.assertEqual(element.ring_image, 'online')
            self.assertNotEqual(self.current_page, index_page)

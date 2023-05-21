from .supports.utils import Mocks
from .supports.unittest import GUnittest
from .supports.blocks import async_exc

class WelcomeTestCases(GUnittest):
    def test_successfully_rendered(self):
        resp = Mocks.Responses.signedIn()
        self.buildLogon()
        self.signInUser(**resp)

        welcome = self.current_page
        with async_exc(self.find_by_text, welcome, resp['user']['nickname']) as element:
            self.assertIsNotNone(element)

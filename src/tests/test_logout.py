from .supports.utils import Mocks
from .supports.unittest import GUnittest

class LogoutSpecs(GUnittest):
    def logging_out(self, status: int, synced=True):
        self.buildLogon()
        self.signInUser(**Mocks.Responses.signedIn())

        welcome = self.current_page
        self.root.signing_out()
        self.assertNotEqual(welcome, self.current_page)
        self.app.synced = synced
        self.root.on_signed_out(status=status)

        return welcome

    def test_failed_to_logout(self):
        old_pg = self.logging_out(500)
        self.assertEqual(old_pg, self.current_page)

    def test_successfully_logged_out_synced(self):
        old_pg = self.logging_out(200)
        self.assertNotEqual(old_pg, self.current_page)
        self.assertEqual(self.current_page.name, 'logon')

    def test_successfully_logged_out_unsynced(self):
        old_pg = self.logging_out(200, False)
        self.assertNotEqual(old_pg, self.current_page)
        self.assertEqual(self.current_page.name, 'index')

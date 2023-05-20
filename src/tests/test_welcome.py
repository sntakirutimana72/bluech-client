from .supports.unittest import GUnittest
from .supports.blocks import async_exc

class WelcomeTestCases(GUnittest):
    def build(self):
        super().build()
        index_page = self.current_page
        index_page.on_status(status='online')
        form = getattr(self.current_page, 'form')
        self.assertIsNotNone(form)
        self.form = form

    def go_to_welcome(self):
        self.build()
        self.prompt_user(username='stevie', pass_w='@123')

        self.assertFalse(self.form.submit_btn.disabled)
        self.click(self.form.submit_btn)
        self.assertTrue(self.form.submit_btn.disabled)

        self.resp = resp = {
            'proto': 'connected',
            'user': {
                'email': 'user@email',
                'nickname': 'sntakirutimana72',
                'id': 7089
            }
        }
        logon_pg = self.current_page
        logon_pg.on_signed_in(**resp)

    def prompt_user(self, **kwargs):
        self.form.username.value = kwargs['username']
        self.form.password.value = kwargs['pass_w']

    def test_page_rendered(self):
        self.go_to_welcome()
        wlc_pg = self.current_page
        with async_exc(self.find_by_text, wlc_pg, self.resp['user']['nickname']) as element:
            self.assertIsNotNone(element)

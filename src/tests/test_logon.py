from .supports.unittest import GUnittest
from .supports.blocks import async_exc
from ..templates.forms import LogonForm

class LogonTestCases(GUnittest):
    def build(self):
        super().build()
        index_page = self.current_page
        index_page.on_status(status='online')
        form = getattr(self.current_page, 'form')
        self.assertIsInstance(form, LogonForm)
        self.form = form

    def enter_credentials(self, **kwargs):
        self.form.username.value = kwargs['username']
        self.form.password.value = kwargs['pass_w']

class FormContainsElements(LogonTestCases):
    def test_form_contains_username_field(self):
        self.build()
        username_field = self.form.username
        self.assertIsNotNone(username_field)
        self.assertTrue(hasattr(username_field, 'value'))

    def test_form_contains_password_field(self):
        self.build()
        password_field = self.form.password
        self.assertIsNotNone(password_field)
        self.assertTrue(hasattr(password_field, 'value'))

    def test_form_contains_submit_button(self):
        self.build()
        submit_btn = self.form.submit_btn
        self.assertIsNotNone(submit_btn)
        self.assertIn(submit_btn.text, 'Signin')

class SubmissionDisability(LogonTestCases):
    def test_disability_by_default(self):
        self.build()
        self.assertFalse(self.form.username.disabled)
        self.assertFalse(self.form.password.disabled)
        self.assertTrue(self.form.submit_btn.disabled)

    def test_disability_when_both_username_and_password_change(self):
        self.build()
        self.enter_credentials(username='steve@email', pass_w='pass@123')
        self.assertFalse(self.form.submit_btn.disabled)

        self.enter_credentials(username='', pass_w='pass@123')
        self.assertTrue(self.form.submit_btn.disabled)
        self.enter_credentials(username='steve@email', pass_w='')
        self.assertTrue(self.form.submit_btn.disabled)

    def test_disability_on_submission(self):
        self.build()
        self.enter_credentials(username='steve@email', pass_w='pass@123')
        self.click(self.form.submit_btn)

        self.assertTrue(self.form.submit_btn.disabled)
        self.assertTrue(self.form.username.disabled)
        self.assertTrue(self.form.password.disabled)

class PostSubmissionBehaviors(LogonTestCases):
    def pre_signin(self):
        self.build()
        self.enter_credentials(username='stevie', pass_w='@123')

        self.assertFalse(self.form.submit_btn.disabled)
        self.click(self.form.submit_btn)
        self.assertTrue(self.form.submit_btn.disabled)

    def test_failure_response(self):
        self.pre_signin()
        response = {'proto': 'invalid_request', 'message': '400: Invalid Request'}
        self.current_page.on_signed_in(**response)
        self.assertFalse(self.form.submit_btn.disabled)
        self.assertEqual(self.form.errors, response['message'])
        self.assertEqual(len(self.form.ids.errors_container.children), 1)

    def test_success_response(self):
        self.pre_signin()
        response = {
            'proto': 'connected',
            'user': {
                'email': 'user@email',
                'nickname': 'user@nickname',
                'id': 7089
            }
        }
        logon_page = self.current_page
        logon_page.on_signed_in(**response)
        self.assertTrue(self.form.submit_btn.disabled)
        self.assertNotEqual(self.current_page, logon_page)
        self.assertFalse(self.current_page.app.user['is_anonymous'])

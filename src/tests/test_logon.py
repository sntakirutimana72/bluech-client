from .supports.utils import Mocks
from .supports.unittest import GUnittest

class FormContainsElements(GUnittest):
    def test_form_contains_username_field(self):
        self.buildLogon()
        username_field = self.form.username
        self.assertIsNotNone(username_field)
        self.assertTrue(hasattr(username_field, 'value'))

    def test_form_contains_password_field(self):
        self.buildLogon()
        password_field = self.form.password
        self.assertIsNotNone(password_field)
        self.assertTrue(hasattr(password_field, 'value'))

    def test_form_contains_submit_button(self):
        self.buildLogon()
        submit_btn = self.form.submit_btn
        self.assertIsNotNone(submit_btn)
        self.assertIn(submit_btn.text, 'Signin')

class SubmissionDisability(GUnittest):
    def test_disability_by_default(self):
        self.buildLogon()
        self.assertFalse(self.form.username.disabled)
        self.assertFalse(self.form.password.disabled)
        self.assertTrue(self.form.submit_btn.disabled)

    def test_disability_when_both_username_and_password_change(self):
        self.buildLogon()
        self.prompt_user(username='steve@email', pass_w='pass@123')
        self.assertFalse(self.form.submit_btn.disabled)

        self.prompt_user(username='', pass_w='pass@123')
        self.assertTrue(self.form.submit_btn.disabled)
        self.prompt_user(username='steve@email', pass_w='')
        self.assertTrue(self.form.submit_btn.disabled)

    def test_disability_on_submission(self):
        self.buildLogon()
        self.prompt_user(username='steve@email', pass_w='pass@123')
        self.click(self.form.submit_btn)

        self.assertTrue(self.form.submit_btn.disabled)
        self.assertTrue(self.form.username.disabled)
        self.assertTrue(self.form.password.disabled)

class PostSubmissionBehaviors(GUnittest):
    def smartSignin(self, response):
        self.buildLogon()
        logon = self.current_page
        self.signInUser(**response)
        return logon

    def test_failure_response(self):
        response = Mocks.Responses.error500()
        self.smartSignin(response)
        self.assertFalse(self.form.submit_btn.disabled)
        self.assertEqual(self.form.errors, response['message'])
        self.assertEqual(len(self.form.ids.errors_container.children), 1)

    def test_success_response(self):
        logon = self.smartSignin(Mocks.Responses.signedIn())
        self.assertTrue(self.form.submit_btn.disabled)
        self.assertNotEqual(self.current_page, logon)
        self.assertFalse(self.current_page.app.user['is_anonymous'])

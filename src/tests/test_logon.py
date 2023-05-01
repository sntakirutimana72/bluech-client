from .supports.unittest import GUnittest
from .supports.blocks import async_exc

class LogonTestCases(GUnittest):
    def build(self):
        super().build()
        index_page = self.current_page
        index_page.on_status(status='online')
        with async_exc(self.find_by_role, self.current_page, 'LogonForm') as form:
            self.assertIsNotNone(form)
            self.form = form

class FormContainsElements(LogonTestCases):
    def test_form_contains_username_field(self):
        self.build()
        with async_exc(self.find_by_attrib, self.form, 'name', r'^username$') as element:
            self.assertIsNotNone(element)
            self.assertTrue(hasattr(element, 'value'))

    def test_form_contains_password_field(self):
        self.build()
        with async_exc(self.find_by_attrib, self.form, 'name', r'^password$') as element:
            self.assertIsNotNone(element)
            self.assertTrue(hasattr(element, 'value'))

    def test_form_contains_submit_button(self):
        self.build()
        with async_exc(self.find_by_role, self.form, 'PrimaryButton') as element:
            self.assertIsNotNone(element)
            self.assertIn(element.text, 'Signin')

class SubmissionDisability(LogonTestCases):
    def enter_credentials(self, **kwargs):
        self.form.username.value = kwargs['username']
        self.form.password.value = kwargs['pass_w']

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
        self.form.submit_btn.dispatch('on_press')
        self.assertTrue(self.form.submit_btn.disabled)
        self.assertTrue(self.form.username.disabled)
        self.assertTrue(self.form.password.disabled)

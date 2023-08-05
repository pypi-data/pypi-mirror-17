"""PytSite Auth Password Driver.
"""
from pytsite import auth as _auth, form as _form, router as _router, widget as _widget, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _SignInForm(_form.Form):
    """Password Login Form.
    """
    def _setup_widgets(self):
        """Hook.
        """
        for k, v in _router.request().inp.items():
            self.add_widget(_widget.input.Hidden(uid=self.uid + '-' + k, name=k, value=v, form_area='hidden'))

        self.add_widget(_widget.input.Email(
            uid='login',
            label=_lang.t('pytsite.auth@email'),
            weight=10,
            required=True,
            value=_router.request().inp.get('login', ''),
        ))

        self.add_widget(_widget.input.Password(
            uid='password',
            label=_lang.t('pytsite.auth@password'),
            weight=20,
            required=True,
        ))

        self.get_widget('action-submit').value = _lang.t('pytsite.auth@login')


class Password(_auth.driver.Authentication):
    """ULogin Driver.
    """
    def get_name(self) -> str:
        """Get name of the driver.
        """
        return 'password'

    def get_sign_up_form(self, form_uid: str, **kwargs) -> _form.Form:
        # TODO
        pass

    def get_sign_in_form(self, form_uid: str, **kwargs) -> _form.Form:
        """Get the login form.
        """
        return _SignInForm(uid=form_uid, **kwargs)

    def sign_up(self, data: dict):
        # TODO
        pass

    def sign_in(self, data: dict) -> _auth.model.AbstractUser:
        """Authenticate user.
        """
        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            raise _auth.error.AuthenticationError('Login or password is not specified.')

        # Check if the user exists
        user = _auth.get_user(login)
        if not user:
            raise _auth.error.AuthenticationError(_lang.t('pytsite.auth@authentication_error'))

        # Check password
        if not _auth.verify_password(password, user.password):
            raise _auth.error.AuthenticationError(_lang.t('pytsite.auth@authentication_error'))

        return user

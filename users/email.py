from djoser import email

# these classes are inheriting from djoser's email class and then changing the template to our custom our


class ActivationEmail(email.ActivationEmail):
    template_name = 'users/activation.html'


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'users/confirmation.html'


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'users/password_reset.html'


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = 'users/password_changed_confirmation.html'
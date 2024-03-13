from django.core.exceptions import (
    ValidationError,
)


class UppercaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError("The password must contain at least one uppercase letter.", code='password_no_upper')

    def get_help_text(self):
        return (
            "Your password must contain at least one uppercase letter."
        )
    
class SymbolValidator:
    def validate(self, password, user=None):
        if not any(char in "!@#$%^&*()-_=+[]{};:'\"\\|,.<>/?`~" for char in password):
            raise ValidationError("The password must contain at least one symbol.", code='password_no_symbol')

    def get_help_text(self):
        return (
            "Your password must contain at least one symbol."
        )
    
class LowercaseValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                "The password must contain at least one lowercase letter.",
                code='password_no_lower',
            )

    def get_help_text(self):
        return (
            "Your password must contain at least one lowercase letter."
        )
    

class NumericValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                "The password must contain at least one Number.", code='password_no_numeric',
            )

    def get_help_text(self):
        return (
            "Your password must contain at least one Number."
        )

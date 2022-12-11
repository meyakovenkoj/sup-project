import string

from common import consts


class BaseValidator:

    def check_validation(self, input_data):
        self._validate(input_data)

    def _validate(self, input_data):
        raise NotImplementedError(f"_validate method of {self.__class__.__name__} must be implemented!")


class PasswordValidator(BaseValidator):
    def _validate(self, input_data):
        return (
                isinstance(input_data, str) and
                len(input_data) >= consts.MIN_PASSWORD_LEN and
                any(char.isdigit() for char in input_data) and
                any(char.islower() for char in input_data) and
                any(char.isupper() for char in input_data) and
                any(char in string.punctuation for char in input_data) and
                all(char in consts.PASSWORD_SIMBOLS for char in input_data)
        )


class UsernameValidator(BaseValidator):
    def _validate(self, input_data):
        return (
                isinstance(input_data, str) and
                all(char in consts.USERNAME_SIMBOLS for char in input_data)
        )


class NameValidator(BaseValidator):
    def _validate(self, input_data):
        return (
                isinstance(input_data, str) and
                (all(char.isalpha() or char == '-' or char == ' ' for char in input_data))
        )

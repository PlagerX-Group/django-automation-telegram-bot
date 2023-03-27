import enum
import typing as t

from extendeduser.models import ExtendedUserModel


@enum.unique
class ValidatorWarningsEnum(enum.Enum):
    CORRECT: str = None
    GITLAB_USERNAME_NOT_SET: str = "Имя пользователя в Gitlab не установлено!"


@enum.unique
class ValidatorErrorsEnum(enum.Enum):
    CORRECT: str = None


TypeValidatorEnum = t.Union[ValidatorWarningsEnum, ValidatorErrorsEnum]


class Validator:

    @staticmethod
    def validate_user_gitlab(user_id: int, /) -> TypeValidatorEnum:
        user = ExtendedUserModel.objects.get(telegram_user_id=user_id)
        if isinstance(user.gitlab_username, str) and user.gitlab_username != '':
            return ValidatorWarningsEnum.CORRECT
        return ValidatorWarningsEnum.GITLAB_USERNAME_NOT_SET

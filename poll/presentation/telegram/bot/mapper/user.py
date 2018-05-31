from bot.api.domain import ApiObject

from poll.presentation.model.user import UserViewModel


class UserViewModelMapper:
    @staticmethod
    def map_user(user: UserViewModel) -> ApiObject:
        return ApiObject(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language
        )

    @staticmethod
    def unmap_user(user: ApiObject) -> UserViewModel:
        return UserViewModel(
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            user.language_code
        )

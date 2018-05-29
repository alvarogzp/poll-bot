from bot.api.domain import ApiObject

from poll.presentation.model.user import UserViewModel


class UserViewModelMapper:
    @staticmethod
    def unmap_user(user: ApiObject) -> UserViewModel:
        return UserViewModel(
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            user.language_code
        )

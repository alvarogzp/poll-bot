from bot.api.domain import ApiObject

from poll.presentation.model.publication.publication import PublicationViewModel


class PublicationViewModelMapper:
    @staticmethod
    def unmap_publication(api_object: ApiObject) -> PublicationViewModel:
        return PublicationViewModel(
            api_object.inline_message_id
        )

from poll.domain.model.poll.publication import PollPublication
from poll.presentation.model.publication.publication import PublicationViewModel


class PollPublicationMapper:
    @staticmethod
    def map_publication(publication: PollPublication) -> PublicationViewModel:
        return PublicationViewModel(
            publication.id
        )

    @staticmethod
    def unmap_publication(publication: PublicationViewModel) -> PollPublication:
        return PollPublication(
            publication.id
        )

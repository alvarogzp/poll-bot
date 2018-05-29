from typing import Sequence

from poll.domain.model.poll.publication import PollPublication


class PollPublications:
    def __init__(self, publications: Sequence[PollPublication]):
        self.publications = publications

    def __iter__(self):
        return self.publications.__iter__()

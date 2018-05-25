from poll.domain.interactors.poll.get import GetPollInteractor
from poll.domain.interactors.poll.vote import VotePollInteractor
from poll.domain.model.poll.full.poll import FullOptionPoll
from poll.domain.model.poll.vote import OptionPollVote
from poll.presentation.model.mapper.full.poll import FullPollMapper
from poll.presentation.model.mapper.option import PollOptionNumberMapper
from poll.presentation.model.mapper.publication import PollPublicationMapper
from poll.presentation.model.mapper.user import UserMapper
from poll.presentation.model.poll.option import PollOptionIdViewModel
from poll.presentation.model.publication.action import PublicationActionViewModel
from poll.presentation.view.vote import VotePollView


class VotePollPresenter:
    def __init__(self, view: VotePollView, interactor_vote: VotePollInteractor, interactor_get: GetPollInteractor,
                 mapper_user: UserMapper, mapper_poll_publication: PollPublicationMapper,
                 mapper_poll_option_number: PollOptionNumberMapper, mapper_full_poll: FullPollMapper):
        self.view = view
        self.interactor_vote = interactor_vote
        self.interactor_get = interactor_get
        self.mapper_user = mapper_user
        self.mapper_poll_publication = mapper_poll_publication
        self.mapper_poll_option_number = mapper_poll_option_number
        self.mapper_full_poll = mapper_full_poll

    def vote(self, action: PublicationActionViewModel, option_id: PollOptionIdViewModel):
        user = self.mapper_user.unmap_user(action.user)
        publication = self.mapper_poll_publication.unmap_publication(action.publication)
        option = self.mapper_poll_option_number.unmap_poll_option_number(option_id)

        vote = OptionPollVote(user, publication, option)
        result = self.interactor_vote.vote(vote)

        full_poll = self.interactor_get.by_publication(publication)
        assert isinstance(full_poll, FullOptionPoll)

        option_info = full_poll.options.get_info(option)
        self.view.voted(action, option_info, result)

        full_poll_view_model = self.mapper_full_poll.map_full_poll(full_poll)

        # first update the publication where the user voted, so that the user sees his/her vote as soon as possible
        self.view.update_poll(action.publication, full_poll_view_model)

        # then update all other publications in reverse order of creation (ie. most recent first)
        for poll_publication in reversed(full_poll.publications):
            # skip the publication in which the user voted, as it has been already updated
            if poll_publication != publication:
                poll_publication = self.mapper_poll_publication.map_publication(poll_publication)
                self.view.update_poll(poll_publication, full_poll_view_model)

from poll.domain.model.base import Comparable


class PollPublication(Comparable):
    def __init__(self, publication_id: str):
        """
        :param publication_id: IMPORTANT!
          This id must come from a trusted source (that a user is not able to tamper)
          or be a cryptographically secure hash (hard to guess and predict).
          They must also be unique among all polls, as they are used to retrieve the poll from them.
          Finally, the presentation layer is responsible for generating them.

          This token grants any user the ability to vote in the associated poll. With it, you can also
          get full poll data (so that the bot can refresh poll votes). It cannot be used to
          manage the poll.

          As a hint, telegram's inline_message_id is considered safe to be used as publication_id,
          as it comes from a trusted source (the API), it is a value users cannot alter, and should
          uniquely identify a single message created via the bot (ie. a poll publication).
        """
        super().__init__(publication_id, PollPublication)
        self.id = publication_id

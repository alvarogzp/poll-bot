class NotFoundError(RuntimeError):
    def __init__(self, name: str, value=None):
        super().__init__(
            "{name}{value} was not found".format(
                name=name,
                value=" '{value}'".format(value=value) if value is not None else ""
            )
        )
        self.name = name
        self.value = value

class Response:

    def __init__(
        self,
        status: int,
        text: str | None = None
    ):
        self.status = status
        self.text = text

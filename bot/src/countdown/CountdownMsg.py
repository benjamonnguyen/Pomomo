from discord import Message


class CountdownMsg:

    def __init__(self, title: str, message: Message):
        self.title = title
        self.message = message

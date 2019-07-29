
class Offset:

    def __init__(self, offset: int):
        self.offset = offset

    def __str__(self) -> str:
        return f'({self.offset})' if self.offset != 0 else ''
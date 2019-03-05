class BaseBotException(Exception):
    pass


class IncorrectInputException(BaseBotException):
    pass


class WrongUrlException(BaseBotException):
    pass


class PostWithoutImagesException(BaseBotException):
    pass

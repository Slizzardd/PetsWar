class FarmTimeNotPassed(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InsufficientBalance(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class FarmDataNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotEnoughBalance(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class TgUsernameNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DuelAlreadyExists(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class BalanceNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotRegistered(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class QuestCooldownError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

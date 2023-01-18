class SwitchBotAppError(Exception):
    def __init__(self, *args: object) -> None:
        self.message = args[0]
        super().__init__(*args)


class UnauthorizedError(SwitchBotAppError):
    pass


class CommandNotSupportedError(SwitchBotAppError):
    pass


class ConfigurationMissingError(SwitchBotAppError):
    pass

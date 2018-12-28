class EmailAlreadyExists(Exception):
    pass


class UsernameAlreadyExists(Exception):
    pass


class NotFound(Exception):
    pass


class NotMine(Exception):
    pass


class UserNotExists(Exception):
    pass


class RepositoryError(Exception):
    pass


class InvalidRouter(Exception):
    pass


class UploadFileError(Exception):
    pass


class InvalidEnvironment(Exception):
    pass


class NoImplementationError(Exception):
    pass


class ConfigClassNotFound(Exception):
    pass


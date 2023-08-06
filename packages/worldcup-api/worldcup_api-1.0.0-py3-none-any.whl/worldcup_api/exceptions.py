class NotRegistered(Exception):
    def __init__(self, message="Need to register first"):
        self.message = message
        super().__init__(self.message)


class AlreadyRegistered(Exception):
    def __init__(self, message="Already registered"):
        self.message = message
        super().__init__(self.message)


class NotLoggedIn(Exception):
    def __init__(self, message="Need to login first"):
        self.message = message
        super().__init__(self.message)


class TokenInvalid(Exception):
    def __init__(self, message="Token is invalid"):
        self.message = message
        super().__init__(self.message)

class UserAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email '{email}' already exists.")

class InvalidCredentialsError(Exception):
    pass

class UserNotFoundError(Exception):
    def __init__(self, user_id: int = None, email: str = None):
        self.user_id = user_id
        self.email = email
        if user_id:
            super().__init__(f"User with ID {user_id} not found.")
        elif email:
            super().__init__(f"User with email '{email}' not found.")
        else:
            super().__init__("User not found.")

class PostNotFoundError(Exception):
    def __init__(self, message: str = "Post not found or you don't have permission to access it"):
        self.message = message
        super().__init__(self.message)
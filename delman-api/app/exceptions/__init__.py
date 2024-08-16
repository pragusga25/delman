class UsernameAlreadyExistsError(Exception):
    """Raised when attempting to create an entity with a username that already exists."""
    def __init__(self, entity_name: str, username: str):
        self.username = username
        self.message = f"An {entity_name} with username '{username}' already exists."
        super().__init__(self.message)

class DuplicateResourceError(Exception):
    """Raised when attempting to create duplicated resource."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ResourceNotFoundError(Exception):
    """Raised when attempting to get non-existent resource."""
    def __init__(self, message: str, err_code: str):
        self.message = message
        self.err_code = err_code
        super().__init__(self.message)

class ValidationError(Exception):
    """Raised when attempting to create an entity with invalid data."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

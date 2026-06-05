
class DatabaseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class QueryError(DatabaseError):
    def __init__(self, message: str):
        super().__init__(message)

class DatabaseConnectionError(DatabaseError):
    def __init__(self, message: str):
        super().__init__(message)
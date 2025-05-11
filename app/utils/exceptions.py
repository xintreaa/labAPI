from fastapi import status


class LibraryException(Exception):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)

class BookNotAvailableException(LibraryException):
    """Exception raised when a book is not available for borrowing"""
    pass


class UserBorrowLimitException(LibraryException):
    """Exception raised when a user has reached their borrow limit"""
    pass


class EntityNotFoundException(LibraryException):
    """Exception raised when an entity is not found"""
    pass


class DuplicateEntityException(LibraryException):
    """Exception raised when attempting to create a duplicate entity"""
    pass
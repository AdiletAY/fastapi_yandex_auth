class DatabaseOperationError(Exception):
    """Custom exception for database operation errors.

    Raised when an error occurred
    during the database operation.

    Attributes:
        message (str): Explanation of the error.

    """


class DuplicateEntryError(Exception):
    """Exception raised for violations of unique constraints in the database.

    This exception is triggered when an attempt is made to insert or update
    an entry in the database that would violate a unique constraint, such as
    a duplicate key or unique field.

    Attributes:
        message (str): Explanation of the error.
    """

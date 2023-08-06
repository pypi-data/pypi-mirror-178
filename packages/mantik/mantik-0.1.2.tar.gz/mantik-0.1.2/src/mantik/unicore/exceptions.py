class UnicoreError(Exception):
    """Generic class for all unicore errors."""


class AuthenticationFailedException(UnicoreError):
    """User authentication has failed.

    Unfortunately the response by the server does not give any detailed
    information why the authentication fails.

    """


class UnsupportedFileTypeException(UnicoreError):
    """Unsupported File Extension for Backend Config"""


class ConfigurationError(UnicoreError):
    """Error in the backend configuration."""

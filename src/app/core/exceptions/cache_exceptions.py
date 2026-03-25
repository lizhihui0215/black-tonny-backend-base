class CacheIdentificationInferenceError(RuntimeError):
    """Raised when a cache key cannot be inferred from request arguments."""


class InvalidRequestError(RuntimeError):
    """Raised when a cache helper is used in an unsupported request mode."""


class MissingClientError(RuntimeError):
    """Raised when cache access is attempted without a configured backend client."""

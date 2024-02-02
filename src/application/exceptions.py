class ValidationError(Exception):
    """An error while validating data."""


class CannotOpenVideoFileError(Exception):
    """An error when video file can't be opened."""


class CannotReadVideoFileError(Exception):
    """An error when video file can't be read."""

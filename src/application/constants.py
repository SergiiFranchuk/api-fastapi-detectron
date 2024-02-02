from enum import Enum


class FileContentType(str, Enum):
    VIDEO = "video/"
    IMAGE = "image/"
    APPLICATION = "application/"
    TEXT = "text/"

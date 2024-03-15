from enum import Enum


class FileType(Enum):
    CSV = "csv"
    TEXT = "txt"
    JSON = "json"
    EXCEL = "excel"
    CONSOLE = "console"


class VariableType(Enum):
    FORMULA = "Formula"
    DATA = "Data"

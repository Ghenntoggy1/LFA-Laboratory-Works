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
    DATASET = "dataset"


class ExportToType(Enum):
    EXPORT_TO_IMAGE = "ExportToImage"
    EXPORT_TO_FILE = "ExportToFile"


from enum import Enum


class FileType(Enum):
    CSV = "csv"
    TEXT = "txt"
    JSON = "json"
    EXCEL = "excel"
    CONSOLE = "console"


class ImageType(Enum):
    JPG = "jpg"
    PNG = "png"


class PlotType(Enum):
    GRAPH = "graph"
    BAR = "bar"
    PIE = "pie"
    PLOT = "plot"
    HIST = "hist"


class VariableType(Enum):
    FORMULA = "Formula"
    DATA = "Data"
    DATASET = "dataset"
    NAME = "name"


class ExportToType(Enum):
    EXPORT_TO_IMAGE = "ExportToImage"
    EXPORT_TO_FILE = "ExportToFile"


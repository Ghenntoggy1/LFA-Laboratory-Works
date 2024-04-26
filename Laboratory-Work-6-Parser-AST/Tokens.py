from enum import Enum


class OperatorType(Enum):
    MULTIPLY = "*"
    DIVISION = "/"
    ADDITION = "+"
    SUBTRACTION = "-"
    POWER = "**"


class ComparatorType(Enum):
    EQUALS = "=="
    NOT_EQUALS = "!="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LESS_THAN_OR_EQUALS = "<="
    GREATER_THAN_OR_EQUALS = ">="


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


class VisualizationType(Enum):
    VISUALIZE_DATA = "VisualData"
    VISUALIZE_FORMULA = "VisualFormula"

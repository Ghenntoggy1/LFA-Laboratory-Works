class LanguageError(RuntimeError):
    def __init__(self, component, message):
        component.mark()
        self.line = component.line
        self.message = message

    def __str__(self):
        return f"{self.line.get_marks()}\n{type(self).__name__} : {self.message}"

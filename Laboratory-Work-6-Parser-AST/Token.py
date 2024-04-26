class Token:
    def __init__(self, kind, line):
        self.kind = kind
        self.line = line
        self.locale, self.string = line.new_locale()

        # If retrieved string is empty, then set it as "EOF", otherwise - stays the same retrieved string
        self.string = self.string or "EOF"

    def __repr__(self):
        return f"{self.kind}: '{self.string}'"

    def mark(self):
        self.line.mark(self)

    def ast_repr(self, _):
        return f"{self.kind} ── {self.string}"

    def has(self, *strings):
        return self.string in strings

    def of(self, *kinds):
        return self.kind in kinds

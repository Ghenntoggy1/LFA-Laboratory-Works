class SourceLine:
    def __init__(self, line):
        self.line = line  # Actual line from the User Input
        self.locale = [0, 0]  # Track START and END of a Token
        self.marked = [len(line), -1]

    # Checks if line was processed entirely
    def finished(self):
        return self.locale[1] >= len(self.line)

    # Refers to next character that code will work on
    def next(self):
        return "EOF" if self.finished() else self.line[self.locale[1]]

    # Adjusts the states and takes one symbol at a time
    def take(self):
        symbol = self.next()
        self.locale[1] += 0 if self.finished() else 1

        return symbol

    # Ignores current Locale for example spaces
    def ignore(self):
        self.locale[0] = self.locale[1]

    # Takes MultiCharacter Symbol
    def taken(self):
        return self.line[self.locale[0]:self.locale[1]]

    def new_locale(self):
        locale, taken = self.locale.copy(), self.taken()
        self.locale[0] = self.locale[1]
        return locale, taken

    # Set the Marks
    def mark(self, token):
        self.marked[0] = min(token.locale[0], self.marked[0])
        self.marked[1] = max(token.locale[1], self.marked[1])

    # Creates Error Marks
    def get_marks(self):
        marks = "  "

        for i in range(len(self.line) + 1):
            between = self.marked[0] <= i < self.marked[1]
            marks += "^" if between or self.marked[0] == i else " "

        return marks

import re

class Directive:
    def __init__(self, pattern: re, action, preProcessor: bool = True, conditionals: bool = False) -> None:
        self.pattern       =  re.compile(pattern)
        self._action       =  action
        self.preprocessor  =  preProcessor
        self.isconditional =  conditionals

    def invoke(self, line) -> bool:
        match = self.pattern.match(line)
        if match:
            self._action(match.groups())
            return True
        return False

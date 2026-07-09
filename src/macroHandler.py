from scripts.utils import *
from er.DSL import PRP0161

class Macro:
    def __init__(self) -> None:
        self.macros: Manager
        self.line: list

    def replace_macro(self, match):
        macro_name = match.group(1)
        expanded = self.macros.get(macro_name)
        if not expanded or expanded[0]:
            return macro_name
        EXPECT(expanded != None, PRP0161[0].replace('%s', macro_name), hint=PRP0161[1], code=macro_name, type=ERROR)
        return expanded[1]
    
    def replace_w_arg_macro(self, match):
        macro_name = match.group(1)
        EXPECT(self.isdefined(macro_name), PRP0161[0].replace('%s', macro_name), hint=PRP0161[1], code=self.line, type=ERROR)
        args = match.group(2).split(',')
        expanded = self.macros[macro_name][1]
        try:
            lines.pop()
        except:
            return ''
        for i, arg in enumerate(args):
            print(args, expanded, macro_name, i)
            if expanded[0] == 0:
                for i in expanded[1:]:
                    expanded = re.sub(rf"\b{i}\b", arg.strip(), i)
                    line = expanded.split('\u200B', 1)
                    try:
                        lines.append("\u200c"+line[0]+'\u200B'+self.line.replace(match.group(0), line[1]))
                    except:
                        pass
                    #lines.append(re.sub(rf"\b{i}\b", arg.strip(), i))
        #expanded = ''.join(expanded[1:])
        return expanded

    def isdefined(self, arg):
        return arg in self.macros

    def _substitute(self, macros: Manager, line_: str) -> str:
        self.macros = macros._tokens
        line = line_
        line_ = re.compile(r"\b(\w+)").sub(self.replace_macro, line)
        self.line = line_
        pattern = re.compile(r"\b(\w+)\s*\(([^)]*)\)")
        prev = []
        while prev != line_:
            prev = line_
            pattern.sub(self.replace_w_arg_macro, line_)
        #if line == line_:
        #    line_ = ''
        return line_


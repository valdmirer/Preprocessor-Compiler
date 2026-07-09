##
## [ Prep version 01 ]
##
from __future__ import annotations

import ctypes

# ======== runtime ========
import mmap
import os
import platform
import re
import sys
import time
from collections import deque
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

# ======== typing & dataclass ========
from typing import Any, Dict, List, Literal, Optional, Set, Union

# ======== Errors Manual ========
from src.er.DSL import manual as Manual

# ======== Tests ========
from tests import binarySearch, bubbleSort

# ======== Test Hashing Legacy ========
from tests.Hash import HASHash as Hash

"""
 [!] Done

 * Intermediate Representation, each address is flaged. flags are used as tokens for Abstract Syntax Tree.
    Flags are a set that represent a specific type or route to be taken while directive is fed into parser

 [?] Tod-o

 * Take the list of tokens and build an Abstract Syntax Tree (AST).
    a tree structure that represents the grammatical structure of a block of preprocessor Directive.

 * AST is fed into the Directive Parser.

 ---------

 * Data types, support for (int, float, string, bool, arrays, structs)

 * Standard Library: Instruction Selection Library, read, Print

 * Instruction Selection Standard Library, The IR instructions (e.g., x86, ARM, RISC-V) are mapped to the specific machine instructions
    available on the target CPU. This is often done using a pattern-matching algorithm.

 * Instruction Scheduling, Reorders instructions to avoid pipeline stalls on the target CPU
    (e.g., not using the result of a load instruction until several cycles later).

 * Output assembly code and use the system's assembler (as) and linker (ld) to create the final [executable]
"""

# ======== debugging Buffer ========
debugBuffer = list()


def waitForDebug(a):
    debugBuffer.append(a)


def _unique(items):
    results = []
    count = 0
    for i in items:
        if i not in results:
            results.append(i)
        else:
            count += 1
    return results, count


def getDetails():
    db_g, count = _unique(debugBuffer)
    details = []
    for db in db_g:
        if db[0] != -2:
            continue
        details.append(db[1])
    return details, count


def Expect(
    condition,
    Header,
    Error,
    line="",
    prevLine="",
    nextLine="",
    ln=0,
    c=0,
    point=None,
    Trace_macro: List[str] = None,
    _quit=False,
) -> None:
    if not condition:
        # Error handling
        message = Manual.ressolve_variables(Error["MESSAGE"])
        intended = Manual.ressolve_variables(Error["INTENDED_SYNTAX"])
        # note = Manual.ressolve_variables(Error["NOTE"])
        invoke = Manual.ressolve_variables(Error["TYPE"])
        man = " (-m) for more details"

        option = stored()
        if option:
            options = ctypes.cast(option, ctypes.py_object).value
            if "-m" == options or "--manual" == options:
                man = Manual.ressolve_variables(Error["MANUAL"])
        bubbleSort(debugBuffer)

        # Pointer only points to the regex in intended syntax
        pointStr = ""
        if intended and line and point is None:
            regex = re.compile(intended)
            match = regex.search(line)
            if match:
                start, end = match.span()
                pointStr = " " * start + "^" + "~" * (end - start - 1)
            else:
                pointStr = " " * len(line)
        elif point and line:
            pointStr = " " * (line.find(point)) + "^" + "~" * (len(point) - 1)
        else:
            pointStr = " " * len(line)

        # Prepare error message variables before use
        line_num = ln
        pointer_line = f"\033[31m{'▲' * len(str(line_num))}\033[0m{' ' * (len(str(line_num + 1)) - len(str(line_num)))}\033[35m │  \033[31m{pointStr}\033[0m\n"
        if c == 0:
            file_name = f"file:{line_num}"

            a = ""
            try:
                a = Trace_macro[0]
            except:
                pass

            prev_line_str = (
                f"{f'\033[35m{" " * len(str(line_num + 1))} ╭─────{invoke}\033[35m─\033[0m{message}\033[35m─────\n\033[90m{line_num - 1}{' ' * (len(str(line_num + 1)) - len(str(line_num)))}\033[0m \033[35m│\033[0m  '}{prevLine}\n"
                if prevLine
                else ""
            )
            curr_line_str = f"{f'\033[90m{line_num}{' ' * (len(str(line_num + 1)) - len(str(line_num)))}\033[0m \033[35m│\033[0m  '}{line}\n"
            next_line_str = (
                f"{f'\033[90m{line_num + 1}\033[0m \033[35m│\033[0m  '}{nextLine}\n\033[35m{' ' * len(str(line_num + 1))} ╰─>\033[0m\033[31m {file_name}\033[0m\n"
                if nextLine
                else ""
            )

            # a, b = getDetails()
            # details_str = "".join(a)
            # times_str = f"\n* {b + 1} time/s\n\n" if b >= 0 else "\n"

            # Consolidated error message formatting (no repeats)
            error_msg = [
                # f"{invoke} {message}",
                # f"\033[31m-->\033[0m {file_name}",
                prev_line_str
                + curr_line_str
                + pointer_line
                + next_line_str
                + "\033[0m",
                # f"\033[35m(...)\033[30m\n\t\033[7m[fix: Syntax Error]\n\033[0m",
                # f"\033[35mnote\033[0m: {note}",
                # "\033[31m[The program Wandered see for more Details]\033[0m",
                # times_str,
                # f"\033[33mℹ\033[0m Details:\n{man}",
            ]

            print("\n".join(error_msg))
            # exit(1)
            return
        if _quit:
            print(
                f"\n{invoke} {message}",
                f"\n\033[35m{len(str(line_num)) * '  '} >\033[0m  {line} {prevLine}\n",
            )
            quit(1)
        waitForDebug([-2, f"\n{invoke} \033[0m\033[3m{prevLine}"])
        waitForDebug(
            [c, f"\n\033[35m{line_num} │\033[0m  {line} {prevLine}\n{pointer_line}\n"]
        )
        waitForDebug(man)
    return


@dataclass
class TUPLE:
    def __init__(self) -> None:
        self._tokens: tuple = tuple()

    def get(self, value):
        y = list(self._tokens)
        y.append(value)
        self._tokens = tuple(y)
        return self._tokens


@dataclass
class Manager:
    def __init__(self) -> None:
        self._tokens: Dict[Any, Any] = {}

    def get(self, key: str, value=None) -> str:
        if key not in self._tokens:
            self._tokens[key] = value
        return self._tokens[key]

    def _get(self, key: str) -> str:
        if key not in self._tokens:
            return None
        return self._tokens[key]

    def dict_iter(self, strings: set, key="", value=None):
        for i in strings:
            setattr(self, f"{key}{i}", f"__{i}__")

    def assignattr(self, kw: dict):
        it = kw.items()
        for key, value in it:
            setattr(self, key, value)

    def tokens(self, **kwargs):
        # self.assignattr(kwargs)
        self._tokens = kwargs


class AST:
    __slots__ = ("_type", "_children")

    def __init__(self, node_type, children=()):
        self._type = node_type
        self._children = children

    @staticmethod
    def create(node_type, *children):
        return AST(node_type, children)

    def __getitem__(self, index):
        return self._children[index]

    def __len__(self):
        return len(self._children)

    def __repr__(self):
        if self._type == "BinOp" and len(self._children) == 3:
            return f"BinOp({self._children[1]})"
        elif self._type == "Number" and len(self._children) == 2:
            return f"Number({self._children[1]})"
        elif self._type == "Variable" and len(self._children) == 2:
            return f"Variable({self._children[1]})"
        elif self._type == "FunctionCall" and len(self._children) >= 2:
            return f"FunctionCall({self._children[1]})"
        return self._type


def number(value):
    return AST.create("Number", value)


def variable(name):
    return AST.create("Variable", name)


def binop(left, op, right):
    return AST.create("BinOp", left, op, right)


def func_call(func_name, *args):
    return AST.create("FunctionCall", func_name, *args)


# ifdef a   // Ifdef
#   // statements
# elif b    // Elif
#   // statements
#   ifdef c
#       pass
#   endif
# elif b    // Elif
#   // statements
#   ifdef c
# endif

#               IFDEF-(a)
#                /  \
#              T      F
#             /        \
#       Statements    ELIF-(b)
#          /          /   \
#         /    Statements  ELIF-(c)
#       Done       /
#                Done


def ifdef(value):
    return AST.create("Ifdef", value)


def skip(value):
    return AST.create("Ifdef", value)


complex_ast = binop(
    binop(
        binop(variable("x"), "+", variable("y")),
        "*",
        binop(variable("a"), "-", variable("b")),
    ),
    "/",
    binop(number(2), "+", func_call("max", variable("x"), number(5))),
)
simple_ast = binop(variable("x"), "+", binop(variable("y"), "*", number(2)))


def print_ast_tree(node, prefix="", is_last=True, is_root=True):
    """Print AST as a tree structure - THIS WILL WORK"""
    if is_root:
        line = ""
    else:
        connector = "└── " if is_last else "├── "
        line = prefix + connector

    # Print current node
    print(line + str(node))

    # Get only FlyweightNode children (filter out strings/numbers)
    children = []
    for child in node:
        if isinstance(child, AST):
            children.append(child)
        # For BinOp nodes, the operator is at index 1 (which is a string)
        # For other nodes, we might have values that aren't nodes

    # Process children
    new_prefix = prefix + ("    " if is_last else "│   ")

    for i, child in enumerate(children):
        is_child_last = i == len(children) - 1
        print_ast_tree(child, new_prefix, is_child_last, False)


class Macro:
    def __init__(self) -> None:
        self.macros: Manager
        self.line: list = []

    def replace_macro(self, match):
        macro_name = match.group(1)
        expanded = self.macros.get(macro_name)
        if not expanded or expanded[0]:
            return macro_name
        Expect(
            expanded is not None,
            "",
            Error=Manual.PRP1_091,
            line=readLine(self.mm, self.LineOffset),
            prevLine=readLine(self.mm, prevLineOffset(self.mm, self.LineOffset)),
            nextLine=readLine(self.mm, nextLineOffset(self.mm, self.LineOffset)),
            point=macro_name,
            ln=self.lineNumber,
        )

        return expanded[1]

    def replace_w_arg_macro(self, match):
        macro_name = match.group(1)
        Expect(
            self.isdefined(macro_name),
            "",
            Error=Manual.PRP1_091,
            line=readLine(self.mm, self.LineOffset),
            prevLine=readLine(self.mm, prevLineOffset(self.mm, self.LineOffset)),
            nextLine=readLine(self.mm, nextLineOffset(self.mm, self.LineOffset)),
            point=match.group(0),
            ln=self.lineNumber,
        )
        args = match.group(2).split(",")
        if self.macros.get(macro_name) is None:
            # Expect(False, "", Error=Manual.PRP1_041, line=f"{match.group(0)}")
            return None
        expanded = self.macros[macro_name][1]
        for i, arg in enumerate(args):
            if expanded[0] == 0:
                for i in expanded[1:]:
                    expanded = re.sub(rf"\b{i}\b", arg.strip(), i)
                    line = expanded
                    expanded = self.line.replace(match.group(0), line[1])
        return expanded

    def isdefined(self, arg):
        return arg in self.macros

    def _substitute(self, macros: Manager, line_: str, mm, LineData: int) -> str:
        self.mm = mm
        self.LineOffset = LineData[1]
        self.lineNumber = LineData[0]
        self.macros = macros._tokens
        line = line_
        line_ = re.compile(r"\b(\w+)").sub(self.replace_macro, line)
        self.line = line_
        pattern = re.compile(r"\b(\w+)\s*\(([^)]*)\)")
        prev = []
        while prev != line_:
            prev = line_
            line_ = pattern.sub(self.replace_w_arg_macro, line_)
        return line_


class DirectivePrem:
    def __init__(self) -> None:
        self.directiveManager = Manager()

        # Preprocessor Token Manager (as the Name Suggests)
        self.macros = Manager()
        self.Macro = Macro()

        self.currentIndetMacro: List[str] = []

        cpu_architecture_machine = platform.machine()
        match cpu_architecture_machine:
            case "AMD64":
                cpu_architecture_machine = "x86_64"
            case "AARCH64":
                cpu_architecture_machine = "arm64"

        self.macros.get(
            f"__{cpu_architecture_machine.lower()}__",
            f"{cpu_architecture_machine.lower()}",
        )

        self.directiveManager.tokens(
            # ======== Conditional Statements ========
            IFY=Directive(
                r"^\s*ify\s*\((.*?)\)\s*(.*?)$", self.If_statement, conditionals=True
            ),
            IFDEF=Directive(
                r"^\s*ifdef\s*\((.*?)\)\s*(.*?)$",
                self.Ifdef_statement,
                conditionals=True,
            ),
            IFNDEF=Directive(
                r"^\s*ifndef\s*\((.*?)\)\s*(.*?)$", self.If_statement, conditionals=True
            ),
            ELIF=Directive(
                r"^\s*elif\s*\((.*?)\)\s*(.*?)$", self.Elif_statement, conditionals=True
            ),
            ELSE=Directive(
                r"^\s*else\s*\s*(.*?)$", self.Else_statement, conditionals=True
            ),
            # ENDIF     =   Directive(r"\s*endif", self.Endif_statement, conditionals=True), # Simplicity is key
            # ======== Standalone tokens ========
            PRAGMA=Directive(r"\s*pragma\s+(.*)", self._pragma_statement),
            ERROR=Directive(r"\s*error\s+(.*)", self._error_statement),
            WARNING=Directive(r"\s*warning\s+(.*)", self._warning_statement),
            INCLUDE=Directive(r"\s*include\s*\"([^\"]*)\"", self.Include_std_statement),
            INCLUDE_S=Directive(r"\s*include\s*<([^>]*)>", self.Include_file_statement),
            UNDEF=Directive(r"\s*undef\s+(\w+)", self.If_statement),
            # ======== Define statements. Order is important. ========
            DEFINE=Directive(
                r"\s*define\s+(\w+)\(([^\)]*)\)\s*(.*)?",
                self.Define_Statement_With_Parameters,
            ),
            DEFINE_S=Directive(r"\s*define\s+(\w+)\s*(.*)?", self.Define_Statement),
            REGION=Directive(r"\s*region\s+(\w+)\s*(.*)?", self.Region_Statment),
            ENDREGION=Directive(r"\s*endregion", self.Endregion_Statement),
            # ======== preprocessor pipeline to get methods lower##<method>#<arg> ========
            _LOWER=Directive(
                r"^_LOWER\s*#\s*(\w+)\s*=>\s*([^\s].*[^\s])\s*=>\s*([^\s].*[^\s])",
                self._lower_pipeline_w_block,
            ),
            _LOWER_S=Directive(
                r"^_LOWER\s*#\s*(\w+)\s*=>\s*(.+)", self._lower_pipeline
            ),
            # ======== processor Directive ========
            # ...s
        )

        self.inif_dent: int = 0
        self.skip_preserve: int = 0
        self.pragma: List[str] = []

    def indent_if(self, i):
        self.inif_dent += i

    def skip_flow(self, args):
        self.skip_preserve = 1
        Expect(
            not self.inif_dent > 0,
            "",
            Error=Manual.PRP1_002,
            line=args[1],
            prevLine=args[0],
            c=1,
        )

    def _pragma_statement(self, args, ln):
        # raise Exception(args[0])
        self.pragma.append(args[0])

    def end_flow(self):
        pass

    def isdefined(self, arg):
        return arg in self.macros._tokens

    def fn(self, lowers):
        pass

    # ========== Preprocessor functions ==========

    def _error_statement(self, args: List[str], ln):
        Expect(False, "", Error=Manual.PRP1_094, line=f"error {args[0]}", ln=ln)

    def _warning_statement(self, args: List[str]):
        __loaf = []
        for i in args[0].split():
            a = self.macros.get(i)
            if a:
                __loaf.append(a[len(a) - 1])
        if __loaf == []:
            __loaf.append(args[0])
        Expect(False, "", Error=Manual.PRP1_093, line=f"warning {args[0]}", c=1)

    def Include_std_statement(self, args: List[str], ln):
        pass

    def Include_file_statement(self, args: List[str], ln):
        Expect(
            os.path.exists(args[0]),
            "",
            Error=Manual.PRP1_002,
            line=f"include <{args[0]}>",
            ln=ln,
        )

    def Elif_statement(self, args: List[str], ln):
        if self.skip_preserve == 0 and self.inif_dent == 0:
            Expect(
                self.skip_preserve != 0 and self.inif_dent != 0,
                "",
                Error=Manual.PRP1_033,
                prevLine="...",
                nextLine="...",
                line=f"elif ({' '.join(args[:-1])})",
                ln=ln,
            )
        if not self.isdefined(args[0]) and self.skip_preserve == 0:
            a = ["ifdef", args[0]]
            self.skip_flow(tuple(a))
        elif (
            self.skip_preserve == 1 and self.inif_dent == 1 and self.isdefined(args[0])
        ):
            return args[1]

    def Ifdef_statement(self, args: List[str], ln):
        print(args, "-" * 12)
        self.indent_if(1)
        if not self.isdefined(args[0]) and self.skip_preserve == 0:
            a = ["ifdef", args[0]]
            self.skip_flow(tuple(a))
        else:
            return args[1]

    def Else_statement(self, args: List[str], ln):
        if self.inif_dent == 1 and self.isdefined(args[0]) and self.skip_preserve == 1:
            self.skip_preserve = 0
            self.inif_dent = 0
            return False
        else:
            a = ["else", args[0]]
            self.skip_flow(tuple(a))

    def If_statement(self, args: List[str], ln):
        pass

    def Endif_statement(self, args: List[str], ln):
        self.indent_if(-1)
        self.skip_preserve = 0
        Expect(self.inif_dent >= 0, "", Error=Manual.PRP1_031, line="endif", ln=ln)

    def _lower_pipeline_w_block(self, args): ...

    def _lower_pipeline(self, args): ...

    def Endregion_Statement(self, args): ...

    def Region_Statment(self, args): ...

    def Define_Statement_With_Parameters(self, args, ln):
        Expect(
            type(args[1]) is not list,
            "",
            Error=Manual.PRP1_041,
            line="[Assert error] The arguement was not given to an arg-define.",
            ln=ln,
        )
        varargs = [a.strip() for a in args[1].split(",")]

        statements = args[2]

        self.define(args[0], args=varargs, statements=statements, ln=ln)

    def Define_Statement(self, args, ln):
        Expect(
            type(args[1]) is not list,
            "",
            Error=Manual.PRP1_041,
            line=f"{args[1]}",
            ln=ln,
        )
        statements = args[1]
        _Hash = Hash()
        a = f"{'{\r'}|{_Hash.hash(statements)}"
        start_ = statements.find("{"), statements.find("{")
        updated_offset = updateOffset(statements, f"define {args[0]} {statements}")
        # raise Exception(updated_offset, start_)
        line_data[_Hash.hash(statements)] = [start_[0], start_[1] + updated_offset + 1]
        # if readLine(fileData, start_[1]+updated_offset+1).strip():
        #    q.append(Hashed_key)
        self.define(args[0], statements=a, ln=ln)

    #
    #       Finally
    #

    def define(self, name: str, args: list = None, statements: str = None, ln=0):
        statements = statements
        Expect(
            statements.strip() != "{}",
            "",
            Error=Manual.PRP1_092,
            line=f"define {name} ({','.join(args) if args else ''}) {statements}",
            c=1,
            ln=ln,
        )
        # statements = statements[1:-1] if (statements and statements[0] and statements[len(statements)-1]) in string.punctuation else statements
        self.macros._tokens[name] = [args, statements]


# Three conditions. 0, 1 or 2
def findDirective(i, Directives, ln) -> bool:
    """s
    Finding Directives through first Token regex.

    arguments:
        :param i: Statement for Finding Match.
        :param Directives: Directive Managers each with their syntax regex and Invoke actions.
    """
    if not i or i == "\r":
        return

    Expect(i, "", line=f"{i}'", Error=Manual.PRP1_050, ln=ln)

    capitalToken = TOKEN_SEARCH_REGEX.findall(i)[0].upper()
    suffix_key = capitalToken + "_S"
    token = Directives._get(capitalToken)
    token_s = Directives._get(suffix_key)

    token = (
        token.preprocessor
        if token and token.invoke(i, ln)
        else token_s.preprocessor
        if token_s and token_s.invoke(i, ln)
        else False
    )
    return token


def removeComments(text):
    """ "
    As the Name suggests removes comments from single line parameter.

    Return:
        Line Without any Comment.
    """
    code = re.sub(r"//.*", "\r", text)
    code = re.sub(r"/\*[\s\S]*?\*/", "", code, flags=re.MULTILINE)
    return code


# making blocks
def preserveBlocks(text):
    """
    Preserve block example.
    (no use in program only an example for multiple lines regex)
    """
    pattern = r'(".*?"|\{.*?\}|\[.*?\]|\(.*?\))'
    matches = re.findall(pattern, text, re.DOTALL)
    # Replace newlines within quotes and blocks with a placeholder
    for match in matches:
        text = text.replace(match, match.replace("\n", Flags.FF_NEWLINE))
    return text


def preserveBlock_(
    i: int, pointer: int, lineFlags, fileData, t_, directivePrem, l=True
):
    Tokens_OP = []
    if isinstance(lineFlags, list) and l:
        Tokens_OP = lineFlags[1:]
        lineFlags = lineFlags[0]

    if Flags.MULTIPLE_OPERATORS in lineFlags and l:
        for k in Tokens_OP:
            pointer, lineFlags, t_ = preserveBlock_(
                i, pointer, k, fileData, t_, directivePrem, False
            )
        return pointer, lineFlags, t_

    if Flags.PRESERVE in lineFlags:
        # Freeze the timeline to preserve the block
        # if not len(ENPRES_F & lineFlags) >= 2:
        #    print('-'*50, T_freeze, readLine(fileData, line_data[i][1])[:-1], i, line_data[i][0])
        freeze(1)

    if len(PRES_F & lineFlags) >= 2 and T_freeze == 1:
        pointer = i

    elif len(ENPRES_F & lineFlags) >= 2:
        if T_freeze == 1:
            t_.append(i)
        freeze(-1)
        # print('-'*50, T_freeze, readLine(fileData, line_data[i][1])[:-1], i, line_data[i][0])
        Expect(
            T_freeze >= 0 and readLine(fileData, line_data[i][1]),
            "",
            Manual.PRP1_042,
            line=readLine(fileData, line_data[i][1]),
            prevLine=readLine(fileData, prevLineOffset(fileData, line_data[i][1])),
            nextLine=readLine(fileData, nextLineOffset(fileData, line_data[i][1])),
            Trace_macro=directivePrem.currentIndetMacro,
            ln=line_data[i][0],
        )
        # do something with :param T:s
    return pointer, lineFlags, t_


def Highlight(mm, i, m):
    debBuffer[i][3] = "\033[41m"
    debBuffer[i][5] = f'\033[45m M: {readLine(mm, i).strip()} - "{m}" \033[41m '


def util_line_flag_update(
    address: int, value: Set[str], v: int = 0, offset_strings: str = None
) -> int:
    address = address + v
    if line_flags.get(address):
        line_flags[address].append(
            FLAGG.get(offset_strings)[0]
        ) if offset_strings else None
        line_flags[address][0].update(value)
    elif offset_strings:
        line_flags[address] = [value, offset_strings]
    else:
        line_flags[address] = [value]
    return address


def updateOffset(a: str = "", b: int = ""):
    a = a[:-1]
    i = b.find(a)
    return len(b[:i])


def prevLineOffset(mm, currentOffset):
    """
    Returns the offset of the previous line before the currentOffset.

    :param mm: the memory-mapped file object.
    :param currentOffset: the current offset in the memory-mapped file.
    """

    if currentOffset <= 1:
        return 0  # Already at start of file

    search_pos = currentOffset - 2  # -2 because we need to skip the current newline
    while search_pos >= 0:
        if mm[search_pos] == ord("\n"):
            return search_pos + 1  # Return position after the newline
        search_pos -= 1

    # If no newline found, return start of file
    return 0


def nextLineOffset(mm, currentOffset):
    """
    Returns the offset of the next line after the currentOffset.

    :param mm: the memory-mapped file object.
    :param currentOffset: the current offset in the memory-mapped file.
    """

    next_pos = mm.find(b"\n", currentOffset)
    if next_pos == -1:
        return 0
    return next_pos + 1


def readLine(mm, offset):
    newline_pos = mm.find(b"\n", offset)

    if newline_pos == -1:
        return mm[offset:].decode("utf-8")

    line = mm[offset:newline_pos].decode("utf-8")
    # Expect("",Hash(line).hash() == offset, f"\tincorrect line retrieved. Expected hash value '{i}' got '{Hash(line).hash()}' instead", type=WARNING)
    return line


def ReadLines(mm, offs):
    """
    Yields each line of the mmapped File to the the list.

    :var position: the incrementing line int for mapped file.
    :var newlinePos: newline int is added to the position to find address
    """

    position = 0
    while True:
        newlinePos = mm.find(b"\n", position)

        # if the file ends
        if newlinePos == -1:
            offs[0] = position
            yield mm[position:].decode("utf-8")

            break
        else:
            # if theres more content of file
            offs[0] = position
            yield mm[position:newlinePos].decode("utf-8")

            # iterate file position
            position = newlinePos + 1


"""
    :example lineAddress: is passed to every Function Through the <TimeLine>
    :example LINE_DATA: {lineAddress: [LineNumber, Data]}
    :example LINE_FLAGS: {lineAddress: [flag1, error1], lineAddress: [flag2, error2]}
"""

line_data: Dict[int, List[int, int]] = {}
line_flags: Dict[int, List[Set[str, Any]]] = {}

header = (
    """F: \n\r"""
    """L: \n\r"""
    """M: \n\r"""
    """H:
"""
)
P_options = """BASIC COMMANDS: \t\t USAGE: \n\r
    -h \\m --help \t\t\t <program> -h
    -m \\m --manual \t\t <program> <FilePath> -m
    -r \\m --raw \t\t\t <program> <FilePath> -r
    \n\r\n\r"""

Flags: Manager = Manager()
SYS_TYPES = "u_char|u_short|u_int|u_long|ushort|uint|u_quad_t|quad_t|qaddr_t|caddr_t|daddr_t|div_t|dev_t|fixpt_t|blkcnt_t|blksize_t|gid_t|in_addr_t|in_port_t|ino_t|key_t|mode_t|nlink_t|id_t|pid_t|off_t|segsz_t|swblk_t|uid_t|id_t|clock_t|size_t|ssize_t|time_t|useconds_t|suseconds_t"
Flags.dict_iter(
    set(
        "LINE|PRESERVE_IFN|UPDATE_OFFSET|MULTIPLE_OPERATORS|PRESERVE_ELIF|PRESERVE_IFDEF|END_PRESERVE_IFN|TRACE_MACRO|NOMACRO|IGNORE|EOF|QUIT_ERROR|NEWLINE|WARNING|POTENTIAL_PRESERVE_ERROR|PRESERVE|END_PRESERVE|PRESERVE_PARANTHESIS|END_PRESERVE_PARANTHESIS|PRESERVE_BRACKET|END_PRESERVE_BRACKET".split(
            "|"
        )
    )
)

TOKEN_SEARCH_REGEX = re.compile(r"\w+|[^\w\s]|[^\w\s]+")

TRACEMACRO_F: Set[str] = {Flags.TRACE_MACRO}

PRES_F: Set[str] = {Flags.PRESERVE, Flags.POTENTIAL_PRESERVE_ERROR}
ENPRES_F: Set[str] = {Flags.END_PRESERVE, Flags.POTENTIAL_PRESERVE_ERROR}

PRES_PARANTHESIS_F: Set[str] = {
    Flags.PRESERVE_PARANTHESIS,
    Flags.POTENTIAL_PRESERVE_ERROR,
}
ENPRES_PARANTHESIS_F: Set[str] = {
    Flags.END_PRESERVE_PARANTHESIS,
    Flags.POTENTIAL_PRESERVE_ERROR,
}

PRES_BRACKET_F: Set[str] = {Flags.PRESERVE_BRACKET, Flags.POTENTIAL_PRESERVE_ERROR}
ENPRES_BRACKET_F: Set[str] = {
    Flags.END_PRESERVE_BRACKET,
    Flags.POTENTIAL_PRESERVE_ERROR,
}

PRES_IFN_F: Set[str] = {Flags.PRESERVE_IFN}
PRES_IFDEF_F: Set[str] = {Flags.PRESERVE_IFDEF}
PRES_ELIF_F: Set[str] = {Flags.PRESERVE_ELIF}
ENPRES_IFN_F: Set[str] = {Flags.END_PRESERVE_IFN}

IG_F: Set[str] = {Flags.IGNORE}
EOF_F: Set[str] = {Flags.EOF}

FLAGG: Dict[
    str,
    Union[
        List[Union[Set[str], str, Literal[-1]]], List[Union[str, Set[str], Literal[-2]]]
    ],
] = {
    # ignore/warning flags
    "\r": [IG_F, -1],
    # preserving blocks flags
    "{": [PRES_F, "}"],
    "}": [ENPRES_F, "{"],
    "[": [PRES_BRACKET_F, "]"],
    "]": [ENPRES_BRACKET_F, "["],
    "(": [PRES_PARANTHESIS_F, ")"],
    ")": [ENPRES_PARANTHESIS_F, "("],
    # preserving syntax
    #'ify':   [PRES_IFN_F, -1],
    #'elif':  [PRES_ELIF_F, -1],
    #'ifdef': [PRES_IFDEF_F, -1],
    # end of file flag
    "": [EOF_F, "\r"],
}

# contains all addresses It has been over
trace_Stack = []
debBuffer: Dict[int, List[str, Any]] = {}


def FlagRoutine(ret) -> list:
    """
    Enumerating through each line of the mapped File, To Flag content.

    :var addresses: all the addresses of the lines in order, to be processed.
    :var flags: all the <flag-addresses> in order, to be processed.
    :var address: current line hashed address.
    """

    mm = ret.pop(0)
    addresses, flags = [], []
    # iterate thru file
    offs = [0]
    _Hash = Hash()

    for lineNumber, lineData in enumerate(ReadLines(mm, offs), start=1):
        # removing Comments from file
        lineData = removeComments(lineData)

        # hashing line
        address = _Hash.hash(lineData)
        line_data[address] = [lineNumber, offs[0]]

        # Intermediate Representation (alot of repeating code)
        i = IR_Flag(address, lineData, flags)
        if i:
            address = i
            flags.append(address)
            line_data[address] = [lineNumber, offs[0]]
            IR_Flag(address, lineData, flags)
        # else:
        #    flags.append(0)

        # DEBUG BUFFER
        background_color = "\033[44m"
        if lineNumber % 2 != 0:
            background_color = "\033[40m"

        debBuffer[line_data[address][1]] = [
            address,
            f"\t│ L:{line_data[address][0]}",
            f"O:{line_data[address][1]}",
            f"{background_color}",
            "None",
            "",
        ]

        addresses.append(address)
    ret.append(addresses)
    ret.append(flags)


def IR_Flag(address: int, lineData: str, flags: List[int]):
    """
    Intermeiate Representation.

    Represents every line with a flag (token) - from :param FLAGG:
    :global-const-var FLAGG:
    """

    flag = 0
    token = (
        TOKEN_SEARCH_REGEX.findall(lineData.strip())[0].lower()
        if lineData != "\r" and lineData.strip() != ""
        else lineData
    )
    if FLAGG.get(token):
        if FLAGG.get(token)[-1] == -1:
            flag = util_line_flag_update(address, FLAGG.get(token)[0])

    symbols = re.findall(r"[^A-Za-z0-9\s]", lineData)
    for i in symbols:
        if FLAGG.get(i) and i and len(symbols) > 1:
            if line_flags.get(address):
                line_flags[address].append(FLAGG.get(i)[0])
            else:
                line_flags[address] = [{Flags.MULTIPLE_OPERATORS}, FLAGG.get(i)[0]]
            flags.append(address)
    for key, value in FLAGG.items():
        if isinstance(value[-1], str) and key in lineData and value[-1] not in lineData:
            if value[0] == EOF_F:
                return util_line_flag_update(address, value[0], v=1)
            flag = util_line_flag_update(address, value[0])
    if flag:
        flags.append(flag)


T_freeze = 0


def WriteOutAssembly(pragma: List[str]):
    output = []
    regex = re.compile(r"[.|_][a-zA-Z_][a-zA-Z0-9_]*:")
    Sectionregex = re.compile(r"(?i)section\s*\.\w*")
    v = "\t"

    for i in range(len(pragma)):
        if pragma[i][0] == '"':
            if regex.match(pragma[i][1:-1]) or Sectionregex.match(pragma[i][1:-1]):
                v = ""
            output.append(
                f"{v}{re.sub(r'"(.*?)"\s*\+\s*"(.*?)"', r'"\1\2"', pragma[i])}"
            )
            v = "\t"
        elif pragma[i] == "new":
            if regex.match(pragma[i + 1][1:-1]) or Sectionregex.match(
                pragma[i + 1][1:-1]
            ):
                continue
            output.append(
                f".F{Hash().hash(f'{''.join(output)}' if output else f'{''.join(pragma)}')}:"
            )
    return output


def freeze(b=0):
    global T_freeze
    T_freeze += b
    pass


# no-use
def prepTokenizer(fileData: str) -> None:
    dataAddresses = [fileData]

    FlagRoutine(dataAddresses)

    # addresses in order
    line_addresses: List[int] = dataAddresses[0]

    # flags order
    flag = bubbleSort(dataAddresses[1])

    def timeline():
        pointer = 0
        preserved_list = []

        # if the newly read line's offset is larger than the current Offset then it rereads the previous address.
        # currentOffset = 0
        directivePrem = DirectivePrem()

        q = deque(iter(line_addresses))
        get_flags = line_flags.__getitem__

        trace_macro: str = ""
        while q:
            # ======= get current line =======
            i = q.popleft()
            if binarySearch(i, flag) != -1:
                # ======= get current line Flags =======
                lineFlags = get_flags(i)[0]

                # * ======= Fixme == Macro TraceBack =======
                # if TRACEMACRO_F & lineFlags and len(directivePrem.currentIndetMacro) > 0:
                #    try:
                #        trace_macro = directivePrem.currentIndetMacro[len(get_flags(i))-1]
                #        directivePrem.currentIndetMacro = [directivePrem.currentIndetMacro[len(get_flags(i))-1]]
                #        Highlight(fileData, line_data[i][1], f"traced up to stack {directivePrem.currentIndetMacro[len(get_flags(i))-1]}")
                #    except:
                #        pass
                # elif not TRACEMACRO_F & lineFlags and len(directivePrem.currentIndetMacro) > 0:
                #    for j in range(len(directivePrem.currentIndetMacro)):
                #        directivePrem.currentIndetMacro.pop()
                # *****************************************

                # ======= Ignore Flag Handler =======
                if IG_F & lineFlags:
                    continue

                pointer, lineFlags, preserved_list = preserveBlock_(
                    i, pointer, get_flags(i), fileData, preserved_list, directivePrem
                )

            else:
                lineFlags = set()

            # if T_freeze == 0 and directivePrem.skip_preserve > 0 and not ENPRES_IFN_F & lineFlags and not PRES_IFN_F & lineFlags and not PRES_ELIF_F & lineFlags:
            #    Highlight(fileData, line_data[i][1], "undef macro found")
            #    continue

            if T_freeze > 0:
                preserved_list.append(i)

            # ======= Preprocessor Directive Handler =======
            elif T_freeze == 0 and not EOF_F & lineFlags:
                if ENPRES_F & lineFlags and preserved_list:
                    preserve: str = (
                        str(readLine(fileData, line_data[preserved_list[0]][1]))
                        + "|7798|"
                        + "|".join([str(_) for _ in preserved_list])
                    )
                    preserved_list.clear()
                    isDirective = findDirective(
                        preserve, directivePrem.directiveManager, line_data[i][0]
                    )
                    if isDirective is not True and isDirective is not False:
                        isDirective = isDirective.split("|")
                        for k in isDirective[3:-1][::-1]:
                            if " " in k:
                                continue
                            k = int(k)
                            Highlight(fileData, line_data[k][1], "all items ifdef")
                            q.appendleft(k)

                        get_flags = line_flags.__getitem__

                        bubbleSort(flag)

                    elif not isDirective:
                        _a = directivePrem.Macro._substitute(
                            directivePrem.macros, preserve, fileData, line_data[i]
                        )
                        Expect(
                            _a != preserve,
                            "",
                            Error=Manual.PRP1_050,
                            line=preserve.split("\r")[0],
                            prevLine=readLine(
                                fileData,
                                prevLineOffset(fileData, line_data[pointer][1]),
                            ),
                            Trace_macro=directivePrem.currentIndetMacro,
                            ln=line_data[i][0],
                        )

                    # Hashed_key = Hash().hash(readLine(fileData, line_data[i][1]))
                    # start_ = line_data[i]
                    # updated_offset = updateOffset('}', readLine(fileData, line_data[i][1]))
                    # raise Exception(readLine(fileData, start_[1]+updated_offset+1).strip())
                    # if readLine(fileData, start_[1]+updated_offset+1).strip():
                    #    line_data[Hashed_key] = [start_[0], start_[1]+updated_offset+1]
                    #    q.append(Hashed_key)
                else:
                    lineADirective = readLine(fileData, line_data[i][1]).strip()
                    isDirective = findDirective(
                        lineADirective, directivePrem.directiveManager, line_data[i][0]
                    )
                    # FIXME
                    directivePrem.inif_dent = 0
                    directivePrem.skip_preserve = 0

                    if not isDirective:
                        _a = directivePrem.Macro._substitute(
                            directivePrem.macros, lineADirective, fileData, line_data[i]
                        )
                        Expect(
                            _a != lineADirective,
                            "",
                            Error=Manual.PRP1_050,
                            line=readLine(fileData, line_data[i][1]),
                            prevLine=readLine(
                                fileData, prevLineOffset(fileData, line_data[i][1])
                            ),
                            nextLine=readLine(
                                fileData, nextLineOffset(fileData, line_data[i][1])
                            ),
                            Trace_macro=directivePrem.currentIndetMacro,
                            ln=line_data[i][0],
                        )

                        if not TRACEMACRO_F & lineFlags:
                            directivePrem.currentIndetMacro.insert(0, lineADirective)

                        v = _a.split("|")

                        # ========= Macro Substitution & TraceBack =========

                        # Hashed_key = Hash().hash(v[0])
                        # start_ = line_data[int(v[1])]
                        # updated_offset = updateOffset(v[0], readLine(fileData, line_data[int(v[1])][1]))
                        # line_data[Hashed_key] = [start_[0], start_[1]+updated_offset+1]
                        # for k in v[2:-1]:
                        if _a != lineADirective:
                            Highlight(fileData, line_data[i][1], "Macro call")
                        else:
                            Highlight(fileData, line_data[i][1], "ERROR")

                        for k in v[2:-1][::-1]:
                            if " " in k:
                                continue
                            k = int(k)
                            # Highlight(fileData, line_data[k][1], "all items Substitution")
                            q.appendleft(k)
                            if k in line_flags:
                                line_flags[k] = (
                                    [line_flags[k][0]] + [(TRACEMACRO_F)]
                                    if line_flags[k][0] & TRACEMACRO_F
                                    else [line_flags[k][0].union(TRACEMACRO_F)]
                                )
                            else:
                                line_flags[k] = [TRACEMACRO_F]
                            flag.append(k)

                        get_flags = line_flags.__getitem__

                        bubbleSort(flag)

            if Flags.EOF in lineFlags:
                Expect(
                    T_freeze <= 0,
                    "",
                    Manual.PRP1_041,
                    line=readLine(fileData, line_data[pointer if pointer else i][1]),
                    prevLine=readLine(
                        fileData,
                        prevLineOffset(
                            fileData, line_data[pointer if pointer else i][1]
                        ),
                    ),
                    nextLine=readLine(
                        fileData,
                        nextLineOffset(
                            fileData, line_data[pointer if pointer else i][1]
                        ),
                    ),
                    Trace_macro=trace_macro,
                    ln=line_data[pointer][0],
                )
                # print("EOF", line_flags[pointer if pointer else i])
        output = WriteOutAssembly(directivePrem.pragma)

        return "\n".join(output)

    a = timeline()

    # for _ in debBuffer:
    #    if debBuffer[_][0] in line_flags:
    #        debBuffer[_][4] = line_flags[debBuffer[_][0]]
    #    print(f"{debBuffer[_][3]} A:{debBuffer[_][0]} -> {debBuffer[_][1]}, {debBuffer[_][2]} . . ? . \033[91m{debBuffer[_][5]}\033[0m{debBuffer[_][3]}. F:{debBuffer[_][4]}\033[0m")
    print(T_freeze)
    return a


# enum
class Directive:
    def __init__(
        self,
        pattern: re,
        action: DirectivePrem,
        preProcessor: bool = True,
        conditionals: bool = False,
    ) -> None:
        self.pattern = re.compile(pattern)
        self._action = action
        self.preprocessor = preProcessor
        self.isconditional = conditionals

    def invoke(self, line, ln: int = None) -> bool:
        match = self.pattern.match(line)
        if match and self.isconditional:
            a = self._action(match.groups(), ln)
            if self.preprocessor and a is not False and a is not None:
                self.preprocessor = a
            return True
        elif match:
            self._action(match.groups(), ln)
            return True
        return False


# utility function
def stored(value=None):
    """
    Store the value in a global variable.
    """

    if not hasattr(stored, "_stored_value"):
        stored._stored_value = value
    else:
        value = stored._stored_value
    return value


def readFileMeta(filePath):
    Expect(
        Path(filePath).exists(),
        "",
        Manual.PRP1_002,
        line=f"\033[31m{filePath}\033[0m",
        c=-1,
        _quit=True,
    )
    output = ""
    with open(filePath, "rb") as file:
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            output = prepTokenizer(mm)
            mm.close()
    with open("overWriteOutput.asm", "w") as f:
        f.write(output)


def mainHandleUserInput(
    a="prep", option1=None, options=None, end=None
) -> ...:  # filePath="examples/version_1-ex/devs.prp"
    Expect(
        option1,
        "",
        Manual.PRP1_001,
        line=f"{a} \033[31m{option1}\033[0m",
        c=-1,
        _quit=True,
    )
    Expect(
        not end,
        "",
        Manual.PRP1_138,
        line=f"{a} {option1} {options} \033[31m{end}\033[0m",
        c=-1,
        _quit=True,
    )

    OPTIONS = P_options.replace("\\m", "").replace("<program>", a)
    if option1 in OPTIONS:
        stored(id(option1))
        print(f"{OPTIONS}")
        quit(1)
    else:
        if options:
            if options in OPTIONS:
                stored(id(options))
                print(options)
            Expect(
                options in OPTIONS,
                "",
                Manual.PRP1_138,
                line=f"{a} {option1} \033[31m{options}\033[0m",
                c=-1,
                _quit=True,
            )
        readFileMeta(option1)


if __name__ == "__main__":
    mainHandleUserInput(*sys.argv)  # ->

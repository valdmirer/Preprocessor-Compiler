
import re
from tests import bubbleSort
import os

# Debugging Buffer
debugBuffer = list()
def putInDebug(a):
    debugBuffer.append(a)

class TUPLE:
    def __init__(self) -> None:
        self._tokens: tuple = tuple()
        
    def get(self, value):
        y = list(self._tokens)
        y.append(value)
        self._tokens = tuple(y)
        return self._tokens

class Manager:
    def __init__(self) -> None:
        self._tokens = {}
    
    def get(self, key: str, value=None) -> str:
        if key not in self._tokens:
            self._tokens[key] = value
        return self._tokens[key]
    
    def _get(self, key: str) -> str:
        if key not in self._tokens:
            return None
        return self._tokens[key]
    
    def dict_iter(self, strings: set, a='', b=''):
        for i in strings:
            setattr(self, f'{a}{i}', f'{b}__{i}__')
        
    def assignattr(self, kw: dict):
        it = kw.items()
        for key, value in it:
            setattr(self, key, value)

    def tokens(self, **kwargs):
        #self.assignattr(kwargs)
        self._tokens = kwargs


WARNING = [0, "\n\033[35mwarning\033[0m:"]
ERROR = [1, "\n\033[31merror\033[0m:"]
MINUSONE = [-1, WARNING[1]]
MINUSTWO = [-2, ERROR[1]]

SYS_TYPES   = "u_char|u_short|u_int|u_long|ushort|uint|u_quad_t|quad_t|qaddr_t|caddr_t|daddr_t|div_t|dev_t|fixpt_t|blkcnt_t|blksize_t|gid_t|in_addr_t|in_port_t|ino_t|key_t|mode_t|nlink_t|id_t|pid_t|off_t|segsz_t|swblk_t|uid_t|id_t|clock_t|size_t|ssize_t|time_t|useconds_t|suseconds_t"
Tokens       = set("Number|BinaryOperator|Identifier".split('|'))
FF_FLAGS    = set("LINE|NOMACRO|IGNORE|QUIT_ERROR|NEWLINE|WARNING|POTENTIAL_ERROR".split('|'))
 
# changing utils must change sumthn
TOKEN_SEARCH_REGEX  = re.compile(r"\w+|[^\w\s]|[^\w\s]+")
MANAGER_LOWER       = Manager()
DIRECTIVE_MANAGER   = Manager()
_FLAGS              = MANAGER_LOWER
_FLAGS.dict_iter(FF_FLAGS, "FF_")
_TOKENS              = Manager()
_TOKENS.dict_iter(Tokens, "TT_")
File = ""
lines: list = []
del Tokens, FF_FLAGS, SYS_TYPES


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
            print(db[1], end='')
            continue
        details.append(db[1])
    return details, count

def EXPECT(condition=False, message="", hint="", code="", type=ERROR, code_b="", c=0) -> None:
    if hint == _FLAGS:
        return
    if not condition:
        error = type[1]
        if type == ERROR:
            bubbleSort(debugBuffer)
            a, b = getDetails()
            print(f"{error} {message}\n \033[31m-->\033[0m {File}:{_FLAGS.get(_FLAGS.FF_LINE)}\n \033[35m{_FLAGS.get(_FLAGS.FF_LINE)} │\033[0m  {code} {code_b}\n {len(str(_FLAGS.get(_FLAGS.FF_LINE)))*' '}\033[35m │  \033[31m^\033[31m{(len(code)-1)*'~'}\033[0m\n \t\033[35m(...)\033[30m invalid Use\n\033[0m\n\033[35m note\033[0m: {hint}")
            print("\033[31m[The program Wandered]\033[0m")
            print(f"\n* {b} time/s")
            #print(f"Details:{''.join(a)}")
            exit(1)
        putInDebug([c, f"{error} {message}"])
        if type[0] == MINUSONE[0]:
            putInDebug([c, f"\n \033[35m{_FLAGS.get(_FLAGS.FF_LINE)} │\033[0m  {code} {code_b}\n {len(str(_FLAGS.get(_FLAGS.FF_LINE)))*' '} \033[35m│  \033[31m^^\033[31m{(len(code)-1)*' '}{(len(code_b))*'~'}\033[0m\n \t\033[35m(...)"])
        elif type[0] == MINUSTWO[0]:
            putInDebug([-2, f"{error} \033[0m\033[3m{code_b}"])
            putInDebug([c, f"\n \033[35m{_FLAGS.get(_FLAGS.FF_LINE)} │\033[0m  \033[4m{code}\033[0m {code_b}\n {len(str(_FLAGS.get(_FLAGS.FF_LINE)))*' '} \033[35m│  \033[31m \033[31m{len(code)*' '}|{(len(code_b)-2)*'-'}|\033[0m\n \t\033[35m(...)"])
    return

# Three conditions. 0, 1 or 2
def find_directive_1(i, _tok, _tokens) -> bool:
    EXPECT(_tok == '' or not _tok.isspace(), f"Empty Token! '{_tok}'", 3)
    suffix_key = _tok+"_S"
    token   = _tokens._get(_tok)
    token_s = _tokens._get(suffix_key)
    token = token.preprocessor if token and token.invoke(i) else token_s.preprocessor if token_s and token_s.invoke(i) else 2
    return token

# cleaning code
def remove_excessive_whitespace(text):
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'(\u200B)[\ ]+', r'\1', text)
    text = re.sub(r'(\u200c)(\w+)(\u200B)\n+', '', text)
    return text

def remove_comments(text):
    code = re.sub(r'//.*', '', text)
    code = re.sub(r'/\*[\s\S]*?\*/', '', code, flags=re.MULTILINE)
    return code

# making blocks
def split_preserving_blocks(text):
    pattern = r'(".*?"|\{.*?\}|\[.*?\]|\(.*?\))'
    matches = re.findall(pattern, text, re.DOTALL)
    # Replace newlines within quotes and blocks with a placeholder
    for match in matches:
        text = text.replace(match, match.replace('\n', _FLAGS.FF_NEWLINE))
    lines = text.split('\n')
    lines = [line for line in lines]
    return lines

def invoke_Flags_1(_LINE):
    if _FLAGS.FF_LINE in _LINE:
        _FLAGS._tokens[_FLAGS.FF_LINE] = f"{_LINE.split('__', 1)[0][1:]}"

#FIXME - unoptimized
def Flags_EmbedInRoutine(_buf, _flag):
    flag = _buf[0].pop(0)
    line = _buf[0][0]
    a = "\u200B"
    if "\u200B" in str(line):
        a = ""
    _buf[1] = _buf[1] + (f"\u200C{flag}{_flag}{a}{line}\n")

def Flags_Routine_12(ref) -> list:
    A = ref.pop(0)
    ref.append([0, 0])
    ref.append('')
    for line_flag, line in enumerate(A.split('\n'), start=1):
        ref[0] = [line_flag, line]
        Flags_EmbedInRoutine(ref, _FLAGS.FF_LINE)
    ref.pop(0)

#@A1.FIGOUTTEST('clstest1')
def CLS_0(_buf):
    a = _buf[0].replace(';', '\n')
    test1_rem_comments = remove_comments(a)
    test2_rem_excess_lines = remove_excessive_whitespace(test1_rem_comments)
    test3_split_pres_block = split_preserving_blocks(test2_rem_excess_lines)
    _buf[0] = (test3_split_pres_block)
    return test1_rem_comments, test2_rem_excess_lines, test3_split_pres_block

def split_flags(a):
    a.split('\u200B', 1)
    return a

def get_Flags_info_1(line_f=0, lines=[]):
    line = lines.pop(0).split('\u200B', 1)
    a = line.pop(0) if not len(line) <= 1 else line_f
    line = line.pop()
    token = False
    if len(line) != 0:
        token = TOKEN_SEARCH_REGEX.findall(line)[0].upper()
    return a, line, token


#from scripts.utils import *
#from scripts.utils import _FLAGS, _unique
from scripts.utils import EXPECT, find_directive_1, invoke_Flags_1, get_Flags_info_1, bubbleSort, debugBuffer, ERROR, os,_FLAGS, TOKEN_SEARCH_REGEX, DIRECTIVE_MANAGER, _unique, Flags_Routine_12, CLS_0
from src.macroHandler import Macro
from src.directives import DirectivePrem

def prep_tokenizer_1(buf: str, tokens_prep: DirectivePrem) -> bool:
    _FLAGS
    TOKEN_SEARCH_REGEX
    DIRECTIVE_MANAGER
    ref = [buf]
    
    Flags_Routine_12(ref)
    CLS_0(ref)
    
    #global lines
    lines = ref.pop()
    
    _macro = Macro()

    _FLAGS.get(_FLAGS.FF_LINE, [''])

    #lambda
    def handle_preps():
        _LINE = 1
        prev, eoc = 0, 0
        while len(lines) != 0:
            eoc += 1 if prev == len(lines) else -1
            if eoc == 1:
                break
            prev = len(lines)
            
            _LINE, line, token = get_Flags_info_1(_LINE, lines[:-1])
            if token == False: continue
            
            print(line)
            
            #start_time = time.perf_counter()
            invoke_Flags_1(_LINE)
            #end_time = time.perf_counter()
            #execution_time = Decimal(end_time - start_time)
            #print(execution_time)
            #raise Exception(f"Execution time: {execution_time} seconds")
            _l_ = line
            isprep = find_directive_1(_l_, token, DIRECTIVE_MANAGER)
            if isprep == True+True:
                lines.append(_macro._substitute(tokens_prep.macros, line))
            else:
                pass
                #print("-------", line, "| message: WTFFF")
                #lines.append(line)

    handle_preps()
    print ("-\nSOURCE 👇\n")
    print('\n'.join(lines))


def main(a='prep', file=None) -> ...:
    EXPECT(os.path.exists(file),
           f"file does not exist, most recent lasted in \"{file}\"",
           "Add a fileName to prep.",
           f"{a}",
           c=-1,
           code_b=f"<{file}>",
           type=ERROR)
    
    EXPECT(file,
           "Fatal error no file was specified",
           "Add a fileName to prep.",
           f"{a}",
           c=-1,
           code_b=f"<{file}>",
           type=ERROR)
    
    # Fix, Flag the line with FileName.
    global File
    File = file
    lex = DirectivePrem()
    
    # Reading File
    with open(f"{File}", 'r', encoding='utf-8') as fp:
        prep_tokenizer_1(fp.read(), lex)
    
    # Debugging
    bubbleSort(debugBuffer)
    db_g, a = _unique(debugBuffer)
    for db in db_g:
        if db[0] != -2:
            print(db[1], end='')
            continue
    print('\n', lex.pragma)
    with open("overWriteOutput.asm", 'w') as redfile:
        print(redfile.write('\n'.join(lex.pragma).replace("\u200c", '').replace("\u200b", '\n').replace("\"", '').replace("\\t", "\t").replace("##", " ")))

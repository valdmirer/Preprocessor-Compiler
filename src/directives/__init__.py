from scripts.utils import *
from scripts.utils import _FLAGS
from src.runtime.directive import Directive
from er.DSL import PRP0151, PRP0251

class DirectivePrem:
    def __init__(self) -> None:
        MANAGER_LOWER
        DIRECTIVE_MANAGER
        # Preprocessor Token Manager (as the Name Suggests)
        self.macros = Manager()
        DIRECTIVE_MANAGER.tokens(
            # Conditional Statements
            _IF       =   Directive(r'_\s*if\s+(.*)',       self._if_statement, conditionals=True),
            _IFDEF    =   Directive(r"_\s*ifdef\s+(\w+)",   self._if_defined_statement, conditionals=True),
            _IFNDEF   =   Directive(r"_\s*ifndef\s+(\w+)",  self._if_statement, conditionals=True),
            _ELIF     =   Directive(r"_\s*elif\s+(.*)",     self._if_statement, conditionals=True),
            _ENDIF    =   Directive(r"_\s*endif",           self._endif_statement, conditionals=True),
            _ELSE     =   Directive(r"_\s*else",            self._if_statement, conditionals=True),

            # Standalone tokens
            PRAGMA    =   Directive(r"\s*pragma\s+(.*)", self._pragma_statement),
            ERROR     =   Directive(r"\s*error\s+(.*)", self._error_statement),
            WARNING   =   Directive(r"\s*warning\s+(.*)", self._warning_statement),
            INCLUDE   =   Directive(r"\s*include\s*\"([^\"]*)\"", self._include_std),
            INCLUDE_S =   Directive(r"\s*include\s*<([^>]*)>", self._include_file),
            UNDEF     =   Directive(r"\s*undef\s+(\w+)", self._if_statement),

            # Define statements. Order is important.
            DEFINE    =   Directive(r"\s*define\s+(\w+)\(([^\)]*)\)\s*(.*)?", self._define_statement_w_args),
            DEFINE_S  =   Directive(r"\s*define\s+(\w+)\s*(.*)?", self._define_statement),
            REGION    =   Directive(r"\s*region\s+(\w+)\s*(.*)?", self._region_statment),
            ENDREGION =   Directive(r"\s*endregion", self._endregion_statement),
            
            # preprocessor pipeline to get methods lower##<method>#<arg>
            _LOWER     =   Directive(r"^_LOWER\s*#\s*(\w+)\s*=>\s*([^\s].*[^\s])\s*=>\s*([^\s].*[^\s])", self._lower_pipeline_w_block),
            _LOWER_S   =   Directive(r"^_LOWER\s*#\s*(\w+)\s*=>\s*(.+)", self._lower_pipeline),
            
            # processor Directive
            # ...
        )
        MANAGER_LOWER.tokens(
            directive       =   DIRECTIVE_MANAGER,
            macro           =   self.macros,
            _REGISTER       =   TUPLE(),
            _MANAGER        =   Manager()
        )
        
        self.inif_dent = 0
        self.pragma = ['']

    #indent if
    def indent_if(self):
        self.inif_dent += 1
    #region - if sta. handler
    def skip_flow(self, args):
        #FIXME - start by [Cleaning] this code
        #REVIEW -  OLD ME: its been days! 👴🏼
        v = self.inif_dent
        _else = False
        for i in range(len(lines)):
            a, b, token = get_Flags_info_1()
            if token == False: continue
            elif token == "_ENDIF":
                self.inif_dent -= 1
                _else = False
                if (self.inif_dent != 0):
                    continue
                break
            elif _else == True:
                print(f"{a}{b}")
                lines.append(f"{a}{b}")
            elif token == "_IFDEF":
                self.indent_if()
            elif token == "_ELSE" and v == self.inif_dent:
                _else = True
            
        #EXPECT(v != self.inif_dent, "No _endif... missing an _endif")
        EXPECT(not self.inif_dent > 0, PRP0251[0], PRP0251[1], args[1], code_b=args[0], c=1)
        
        #_FLAGS._tokens[_FLAGS.FF_LINE] = f"-{int(_FLAGS._tokens[_FLAGS.FF_LINE])+1}"
        
    def _pragma_statement(self, args):
        #if args[0].split()[0] == 'new':
        #    self.pragma.append(' '.join(args[0].split()[1:]))
        #else:
        #    self.pragma[0] = f'{self.pragma[0]}\n{''.join(args[0].split()[1:])v}'
        pass

    def end_flow(self):
        _LINE = _FLAGS._tokens[_FLAGS.FF_LINE]
        _LINE = _LINE[0:]
        _FLAGS._tokens[_FLAGS.FF_LINE] = _LINE
        
    def isdefined(self, arg):
        return arg in self.macros._tokens
    
    def fn(self, lowers):
        ch = tuple(lowers.split('#'))
        _man = MANAGER_LOWER
        for c in ch:
            EXPECT(type(_man) == type(TUPLE()) or type(_man) == type(Manager()),
                   message = f"[pipeline manager]: cannot access Unknown '{c}' from '{_man}' at line -> {_FLAGS._tokens[_FLAGS.FF_LINE]}\n")
            _man = _man.get(c)
        return _man

    #   
    #       Preprocessor functions.
    #
    
    def _error_statement(self, args):
        EXPECT(False,
               message = f"[exception invoked]: most recent lasted in \"{"File"}\"",
               code=f"error",
               code_b= f"{args[0]}",
               type=MINUSTWO,
               c = 2)
    
    def _warning_statement(self, args):
        __loaf = []
        print(args)
        print(args[0].split())
        for i in args[0].split():
            a = self.macros.get(i)
            if a:
                __loaf.append(a[len(a)-1])
        if __loaf == []:
            __loaf.append(args[0])
        EXPECT(False,
               message=f"{"File"}:{_FLAGS._tokens[_FLAGS.FF_LINE]}, {' '.join(__loaf)}",
               type=WARNING)
    
    def _include_std(self, args):
        print(args)
    def _include_file(self, args):
        print(args[0])
        EXPECT(os.path.exists(args[0]),
               message=f"file does not exist, most recent lasted in \"{"File"}\"")
        #main(a='prep', file=args[0])
        with open(f"{args[0]}", 'r', encoding='utf-8') as fp:
            ref = [fp.read()]
            Flags_Routine_12(ref)
            CLS_0(ref)
            for x in list(reversed(ref.pop())):
                lines.insert(0,x)
        
    def _if_defined_statement(self, args):
        self.indent_if()
        if not self.isdefined(args[0]):
            a = [args[0]]
            a.append("_ifdef")
            args = tuple(a)
            self.skip_flow(args)

    def _endif_statement(self, args):
        self.inif_dent -= 1
        EXPECT(not self.inif_dent < 0, PRP0151[0], PRP0151[1], PRP0151[2], c=2)
        #self.end_flow()
        #print(self.inif_dent)
        ## writing flags to line
        #EXPECT(self.inif_dent >= 0, PRP4056, _FLAGS)
    
    def _lower_pipeline_w_block(self, args):
        manager = MANAGER_LOWER.get(args[0])
        EXPECT(manager,
               message=f"\033[1m[pipeline manager]: returned with 'None'\n\twhile fetching required Manager\033[0m\n_LOWER_#\033[1;41;37m{args[0]}\033[0m=>{args[1]}=>{args[2]}\n{49*' '+len(args[0])*'^'}")

        
        # handle children
        ca = args
        
        #FIXME - UPOPTIMIZED
        #REVIEW - UNOPTIMIZED PEACE OF SHIT
        for c in ca:
            lowers = c[1:]
            a = c[0]
            if a == '#':
                if '#' in lowers:
                    lowers = self.fn(lowers)
                    print(lowers._tokens if lowers and type(lowers) != type(tuple())  else lowers)
        if args[2][0] == '#':
            lowers = ca[1][1:]
            print(manager,  Manager())
            #EXPECT(type(manager) == type(Manager()), f"\033[1m[pipeline manager]: the request to fetch '{args[0]}' only accepts values\033[0m\n\n\t\033[35m {_FLAGS.get(_FLAGS.FF_LINE)} | \033[0m_LOWER#{args[0]} => {args[1]} => {args[2]}\n\t \033[35m{len(_FLAGS.get(_FLAGS.FF_LINE))*" "} | \033[0m{len(f"#{args[0]} => {args[1]} => ")*" "+"\033[35m|"+len(f" => {args[2]}")*"-"}|\033[0m\n")
            EXPECT(
            type(manager) == type(Manager()),
            f"\033[1m[pipeline]: the request to fetch '{args[0]}' only accepts values\033[0m\n\n"
            f"\t\033[35m {_FLAGS.get(_FLAGS.FF_LINE)} | \033[0m_LOWER#{args[0]} => {args[1]} => {args[2]}\n"
            f"\t \033[35m{len(_FLAGS.get(_FLAGS.FF_LINE)) * ' '} | \033[0m"
            f"{len(f'#{args[0]} => {args[1]} => ') * ' '}"
            f"\033[35m|{len(f' => {args[2]}') * '-'}|\033[0m\n"
            )
            manager.get(lowers, MANAGER_LOWER.get(args[2][1:]))
        # else find value from macro and then get(self.macros.get(args[1]))
        print(manager._tokens)
    
    def _lower_pipeline(self, args):
        manager = MANAGER_LOWER.get(args[0])
        EXPECT(
            manager,
            f"[pipeline manager]: returned with None\n\tWhile fetching required Manager _LOWER_#\033[1;41;37m{args[0]}\033[0m=>{args[1]}\n{49*' ' + len(args[0])*'^'}"
        )

        c = args[1]
        lowers = c[1:]
        a = c[0]
        #FIXME - UNOPTIMIZED PEACE OF SHIT
        if a == '#':
            if '#' in lowers:
                lowers = self.fn(lowers)
                print(lowers, "this is lowers")
            else:
                manager.get(lowers)
        # else find value from macro and then get(self.macros.get(args[1]))
        print(manager._tokens)
        
    def _endregion_statement(self, args):
        print(args, "region\n\n\n\n")

    def _region_statment(self, args):
        print(args)

    def _define_statement_w_args(self, args):
        EXPECT(args[1] is not list, "[Assert error] The arguement was not given to an arg-define.")
        varargs = [a.strip() for a in args[1].split(',')]
        statements = args[2][1:-1]
        statements = statements.replace(f'{_FLAGS.FF_NEWLINE}', '\n')
        if statements != None:
            statements = [statements]
            CLS_0(statements)
            statements = statements[0][0:-1]
            statements[0] = 0
        self.define(args[0], args=varargs, statements_=statements)

    def _define_statement(self, args):
        EXPECT(args[1] is not str, "[Assert error] The arguement was given to a non-arg define. "+str(args))
        statements = args[1].replace(f'{_FLAGS.FF_NEWLINE}', '\n')
        #statements = f"\u200c{_FLAGS.get(_FLAGS.FF_LINE)}{_FLAGS.FF_LINE}\u200B{statements}"
        self.define(args[0], statements_=statements)
    
    def _if_statement(self, args: list):
        print(args)
    
    #
    #       Finally
    #
    
    def define(self, name: str, args: list=None, statements_: str=None):
        statements = statements_
        #statements = statements_.replace(f'{_FLAGS.FF_NEWLINE}', '\n')
        EXPECT(statements,
               message=f"\033[1mEmpty macro declared, the most recent warnings lasted in \"{"File"}\"\033[0m",
               hint="a",
               code=f"define",
               type=MINUSONE,
               code_b=name,
               c = 0)
        #statements = statements[1:-1] if (statements and statements[0] and statements[len(statements)-1]) in string.punctuation else statements
        self.macros.get(name, [args, statements])

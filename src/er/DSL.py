"""
This module defines the DSL (Domain Specific Language)
"""
from __future__ import annotations
from typing import Dict, List, Optional, Callable, Any, Union, Set, Collection
from pathlib import Path

# ============== Type Aliases ==============
DicktionaryCallable = Dict[str, Any]
TokenHandler = Callable[[List[str]], Optional[Union[DicktionaryCallable, List[DicktionaryCallable]]]] | str
TokenDefinition = tuple[str, TokenHandler]

# ============== Contsatnts ==============
DEFAULT_TOKENS: List[TokenDefinition] = [
    ("COMMENTS", "_ignore"),
    ("VARIABLES", "_parse_variable"),
    ("PREMETHEUS", "_parse_manual"),
    ("PRP1", "_parse_type"),
]


# ============== Core Parser ==============
class DSLParser:
    def __init__(self, token: Optional[List[TokenDefinition]] = None) -> None:
        self.tokens = token or DEFAULT_TOKENS
        self.variables: Dict[str, str] = {}
        self.parsed_data: DicktionaryCallable = {}
        
    def _tokenize(self, content: List[str], is_definition = False) -> Union[List[TokenDefinition], List[Union[TokenDefinition, List[str]]] ]:
        """
        Return params:
            The union of both return params:
                
        return -> Union[
                    tokens: List[TokenDefinition], 
                    onlyRed_values: List[Union[TokenDefinition, List[str]]]
                  ]
        """
        tokens: List[Union[TokenDefinition, List[str]]] = []
        onlyRed_values: List[TokenDefinition] = []
        block: List[str] = []
        # iter seems to only work a limited times.
        #tokens_iter = iter(self.tokens)
        
        for line in content:
            if not line.strip():
                continue
            
            elif line[:4] != "    ":
                if len(block) > 0:
                    tokens.append(block)
                    block = []
                
                token_def: Optional[TokenDefinition] = next(
                    (td for td in self.tokens if td[0] in line),
                    None
                )
                
                if token_def and token_def[0] in line:
                    tokens.append(token_def)
                    if is_definition:
                        onlyRed_values.append(token_def)
            else:
                line = line[4:]
                if line:
                    block.append(line)
                    
        assert len(tokens) % 2 == 0, f" tokenizer error: {tokens}??"
        
        return onlyRed_values if onlyRed_values else tokens
    
    # ============== Token Handlers ==============
    @staticmethod
    def _parse_manual(self, content: List[str], nested = True) -> Union[DicktionaryCallable, List[DicktionaryCallable]]:          
          manual: DicktionaryCallable = {}
          for i in range(len(content)):
                if i + 1 >= len(content):
                    break
                
                values: List[str]
                if not nested and content[i][:4] == "    " and content[i].strip() == content[i][4:]:
                    key = content[i].strip()[: - 1]
                    
                    if key == "MANUAL":
                        v = ''
                        for u in content[i + 1:]:
                            if u[:4] == "    " and u.strip() != u[4:]:
                                v += u
                            else:
                                break
                        manual[key] = v
                        return manual
                    values = content[i + 1].strip()
                    
                elif content[i][:4] != "    ":
                    key = content[i].strip()[: - 1]
                    values = content[i + 1 :]

                manual[key] = DSLParser._parse_manual(self, values, False) if nested and values else values
          return [manual] if nested else manual

    @staticmethod
    def _parse_type(self, content) -> Dict[str, str]:
          errors: Dict[str, str] = {}
          for item in content:
                if not item[1]:
                    errors[item[0]] = item[1:]
                else:
                    errors[item[0]] = item[1]
          return errors
    
    @staticmethod
    def _parse_variable(self, content: List[str]) -> Dict[str, str]:
          variables: Dict[str, str] = {}
          for i in content:
              if '=' in i:
                    key, value = map(str.strip, i.split("=", 1))
                    
                    variables[key] = value
          return variables
    @staticmethod
    def _ignore(self, content):
          return None
    
    # ============== Public Methods ==============
    def parseFile(self, filepath: Union[str, Path]) -> None:
        
        path = Path(filepath)
        if not path.exists():
            raise Exception(f"DSL file not Found: {path}")
        
        with open(filepath, 'r') as f:
            content = f.read().splitlines() + ["EOF"]
            macros = self._tokenize(content)
            
            if not macros:
                raise Exception("No macros found in the file.\n\r")
            
            
            for i in range(0, len(macros), 2):
                if i + 1 >= len(macros):
                    continue
                
                token_name, handler = macros[i]
                handler_: str = handler
                handler: TokenDefinition = getattr(self, handler_)
                token_content = macros[i + 1]
                result = handler(self, token_content)
                
                if isinstance(result, dict):
                    self.variables.update(result)
                elif isinstance(result, list):
                    
                    ## # ## # ## # #### item = next(
                    ## # ## # ## # ####     ()
                    ## # ## # ## # #### )
                    
                    ###### # ## # # ## # #for item in result:
                    ###### # ## # # ## # #    self.parsed_data.update(item)
                    
                    ## # ## # ## # ####for item in result:
                    ## # ## # ## # ####      self.parsed_data.update(item)
                    
                    result = iter(result)
                    next(
                        (self.parsed_data.update(t) for t in result),
                        None
                    )
            
            for k,v in self.parsed_data.items():
                setattr(self, k, v)
                            
            
    def ressolve_variables(self, text):
        for key, value in self.variables.items():
            text = text.replace(key, value)
        return text.encode('utf-8').decode('unicode_escape')


filepath = "src/er/data.txt"
manual = DSLParser()
manual.parseFile(filepath)

if __name__ == '__main__':
    print(manual.parsed_data)
    print(manual.ressolve_variables(manual.PRP1_031['MANUAL']))
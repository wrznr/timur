# -*- coding: utf-8 -*- 
import pynini

def union(*args, token_type="utf8"):
    args_mod = []
    for arg in args:
        if type(args) == "str":
            args_mod.append(pynini.acceptor(arg, token_type=token_type))
        else:
            args_mod.append(arg)
    return pynini.union(*(args_mod))

def concat(*args, token_type="utf8"):
    args_mod = []
    conc = pynini.Fst()
    for arg in args:
        if type(args) == "str":
            arg = pynini.acceptor(arg, token_type=token_type)
        conc = pynini.concat(conc, arg)
    return conc

def load_alphabet(source, auto_singletons=True):
    '''
    Load symbols from source and add them to a symbol table.
    '''
    syms = pynini.SymbolTable()
    if auto_singletons:
        for i in range(0,1000):
            symbol = chr(i)
            if symbol.isprintable() and not symbol.isspace():
                syms.add_symbol(symbol)
    for symbol in source.split('\n'):
        if symbol.startswith('#'):
            continue
        syms.add_symbol(symbol.strip())
    return syms

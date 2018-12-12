# -*- coding: utf-8 -*- 
import pynini
import re

def load_alphabet(source, auto_singletons=True):
    '''
    Load symbols from source and add them to a symbol table.
    '''
    syms = pynini.SymbolTable()
    syms.add_symbol("<epsilon>")
    if auto_singletons:
        for i in range(0,256):
            symbol = chr(i)
            if symbol.isprintable() and not symbol.isspace():
                syms.add_symbol(symbol)
    for symbol in source:
        if isinstance(symbol, bytes):
            symbol = symbol.decode("utf-8")
        if symbol.startswith('#'):
            continue
        syms.add_symbol(symbol.strip())
    return syms

def load_lexicon(source, symbol_table):
    '''
    Load lexica entries from source interpreting them using a given symbol table.
    '''
    lex = pynini.Fst()
    lex.set_input_symbols(symbol_table)
    lex.set_output_symbols(symbol_table)
    # longest match, prefer complex over simple symbols
    tokenizer = re.compile("<[^>]*>|.", re.U)
    for line in source:
        lex = pynini.union(lex, pynini.acceptor(" ".join(tokenizer.findall(line.strip())), token_type=symbol_table))
    return lex

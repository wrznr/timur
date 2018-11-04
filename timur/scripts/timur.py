# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import helpers
from timur import fsts

def construct_any(symbol_table):
    '''
    Return an FST for Sigma*.
    '''
    ANY = pynini.Fst()
    sym_it = pynini.SymbolTableIterator(symbol_table)
    start = ANY.add_state()
    ANY.set_start(start)
    ANY.set_final(start)
    while not sym_it.done():
        ANY.add_arc(start, pynini.Arc(symbol_table.find(sym_it.symbol()), symbol_table.find(sym_it.symbol()), 1, start))
        sym_it.next()
    return ANY

def phon_fst(symbol_table):
    '''
    Orthographic and phonological surface realizations rules
    '''
    cons_lower = pynini.string_map(["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z", "ß"], input_token_type=symbol_table, output_token_type=symbol_table)
    cons_upper = pynini.string_map(["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"], input_token_type=symbol_table, output_token_type=symbol_table)
    #return cons.optimize()


def cli():
    syms = helpers.load_alphabet(open("syms.txt"))

    #phon = phon_fst(syms)
    #phon.draw("test.dot")
    num_stems = fsts.num_fst(syms)

    ANY = construct_any(syms)

    print(syms.member('A'))

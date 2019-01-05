# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

def phon_fst(symbol_table):
    '''
    Orthographic and phonological surface realizations rules
    '''
    cons_lower = pynini.string_map(["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z", "ß"], input_token_type=symbol_table, output_token_type=symbol_table)
    cons_upper = pynini.string_map(["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"], input_token_type=symbol_table, output_token_type=symbol_table)
    #return cons.optimize()

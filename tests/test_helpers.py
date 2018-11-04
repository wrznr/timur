# -*- coding: utf-8 -*-

import sys, os, pytest

import pynini

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../timur')))

from timur import helpers

sample_symbols = ["<Base_Stems>", "<NN>", "<base>", "<frei>", "<NMasc_es_e>"]
sample_entries = ["<Base_Stems>Anüs<NN><base><frei><NMasc_es_e>"]

def test_load_alphabet():
    '''
    Load the sample symbol set and check for membership.
    '''
    syms = helpers.load_alphabet(sample_symbols)
    assert(syms.member("<NN>"))
    assert(syms.member("ü"))

def test_load_lexicon():
    '''
    Load the sample lexicon and check vor invariance.
    '''
    syms = helpers.load_alphabet(sample_symbols)
    sym_it = pynini.SymbolTableIterator(syms)
    lex = helpers.load_lexicon(sample_entries, syms)
    sigma_star = pynini.string_map([syms.find(sym[0]) for sym in sym_it], input_token_type=syms, output_token_type=syms).closure()
    output = pynini.compose(lex, sigma_star).optimize().stringify(token_type=syms)
    assert(output.replace(" ", "") == sample_entries[0])

if __name__ == '__main__':
    unittest.main()

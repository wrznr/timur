# -*- coding: utf-8 -*-

import sys
import os
import pytest
import pynini

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../timur')))

from timur import fsts
from timur import helpers

sample_symbols = ["<Base_Stems>", "<NN>", "<base>", "<frei>", "<NMasc_es_e>"]

def test_map_fst():
    syms = helpers.load_alphabet(sample_symbols)
    assert(True)

if __name__ == '__main__':
    unittest.main()

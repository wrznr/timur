# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur.helpers import union
from timur.helpers import concat

def map_fst_map1(symbol_table):
    '''
    Modifications of lexical entries
    '''
    
    # lexical features to be omitted from the output
    cat = pynini.string_map(["<ABK>", "<ADJ>", "<ADV>", "<CARD>", "<DIGCARD>", "<NE>", "<NN>", "<PRO>", "<V>", "<ORD>", "<OTHER>", "<KSF>"], input_token_type=symbol_table, output_token_type=symbol_table)

    cat_ext = pynini.string_map(["<ABK>", "<ADJ>", "<ADV>", "<CARD>", "<DIGCARD>", "<NE>", "<NN>", "<PRO>", "<V>", "<ORD>", "<OTHER>", "<CARD,DIGCARD,NE>", "<ADJ,CARD>", "<ADJ,NN>", "<CARD,NN>", "<CARD,NE>", "<ABK,ADJ,NE,NN>", "<ADJ,NE,NN>", "<ABK,NE,NN>", "<NE,NN>", "<ABK,CARD,NN>", "<ABK,NN>", "<ADJ,CARD,NN,V>", "<ADJ,NN,V>", "<ABK,ADJ,NE,NN,V>", "<ADJ,NE,NN,V>", "<ADV,NE,NN,V>", "<ABK,NE,NN,V>", "<NE,NN,V>", "<ABK,NN,V>", "<NN,V>"], input_token_type=symbol_table, output_token_type=symbol_table)

    return pynini.Fst()

def map_fst_map2(symbol_table):
    '''
    Modifications of lexical entries
    '''

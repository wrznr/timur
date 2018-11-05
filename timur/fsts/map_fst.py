# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur.helpers import union
from timur.helpers import concat

def map_fst_map1(symbol_table):
    '''
    Modifications of lexical entries
    '''
    #
    # lexical features to be omitted from the output

    # word categories
    cat = pynini.string_map(["<ABK>", "<ADJ>", "<ADV>", "<CARD>", "<DIGCARD>", "<NE>", "<NN>", "<PRO>", "<V>", "<ORD>", "<OTHER>", "<KSF>"], input_token_type=symbol_table, output_token_type=symbol_table)

    # delete categories
    cat_ext = pynini.string_map(["<ABK>", "<ADJ>", "<ADV>", "<CARD>", "<DIGCARD>", "<NE>", "<NN>", "<PRO>", "<V>", "<ORD>", "<OTHER>", "<CARD,DIGCARD,NE>", "<ADJ,CARD>", "<ADJ,NN>", "<CARD,NN>", "<CARD,NE>", "<ABK,ADJ,NE,NN>", "<ADJ,NE,NN>", "<ABK,NE,NN>", "<NE,NN>", "<ABK,CARD,NN>", "<ABK,NN>", "<ADJ,CARD,NN,V>", "<ADJ,NN,V>", "<ABK,ADJ,NE,NN,V>", "<ADJ,NE,NN,V>", "<ADV,NE,NN,V>", "<ABK,NE,NN,V>", "<NE,NN,V>", "<ABK,NN,V>", "<NN,V>"], input_token_type=symbol_table, output_token_type=symbol_table)
    del_cat = pynini.transducer("", cat_ext)

    # stem types
    stem_types = pynini.string_map(["<Base_Stems>", "<Kompos_Stems>", "<Deriv_Stems>", "<Suff_Stems>", "<Pref_Stems>"], input_token_type=symbol_table, output_token_type=symbol_table)

    # prefix/suffix marker
    prefix_suffix_marker = pynini.string_map(["<VPART>", "<VPREF>", "<PREF>", "<SUFF>", "<CONV>", "<QUANT>"], input_token_type=symbol_table, output_token_type=symbol_table)

    # stem type features
    stem_type_feats = pynini.string_map(["<base>", "<deriv>", "<kompos>"], input_token_type=symbol_table, output_token_type=symbol_table)

    # origin features
    origin_features = pynini.string_map(["<nativ>",
        "<frei>", "<gebunden>", "<kurz>", "<lang>", "<fremd>", "<klassisch>",
        "<NSNeut_es_e>",
        "<NSFem_0_n>", "<NSFem_0_en>",
        "<NSMasc_es_e>", "<NSMasc_es_$e>", "<NSMasc-s/$sse>",
        "<NGeo-$er-NMasc_s_0>", "<NGeo-$er-Adj0-Up>",
        "<NGeo-$isch-Adj+>",
        "<NGeo-0-Name-Fem_0>", "<NGeo-0-Name-Masc_s>", "<NGeo-0-Name-Neut_s>",
        "<NGeo-a-Name-Fem_s>", "<NGeo-a-Name-Neut_s>",
        "<NGeo-aner-NMasc_s_0>", "<NGeo-aner-Adj0-Up>",
        "<NGeo-anisch-Adj+>",
        "<NGeo-e-NMasc_n_n>", "<NGeo-e-Name-Fem_0>", "<NGeo-e-Name-Neut_s>",
        "<NGeo-ei-Name-Fem_0>",
        "<NGeo-en-Name-Neut_s>",
        "<NGeo-0-NMasc_s_0>", "<NGeo-0-Adj0-Up>",
        "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>",
        "<NGeo-erisch-Adj+>",
        "<NGeo-ese-NMasc_n_n>",
        "<NGeo-esisch-Adj+>",
        "<NGeo-ianer-NMasc_s_0>",
        "<NGeo-ianisch-Adj+>",
        "<NGeo-ien-Name-Neut_s>",
        "<NGeo-ier-NMasc_s_0>",
        "<NGeo-isch-Adj+>",
        "<NGeo-istan-Name-Neut_s>",
        "<NGeo-land-Name-Neut_s>",
        "<NGeo-ner-NMasc_s_0>", "<NGeo-ner-Adj0-Up>",
        "<NGeo-nisch-Adj+>",
        "<NGeo-0-$er-$er>",
        "<NGeo-0-$er-$isch>",
        "<NGeo-0-aner-aner>",
        "<NGeo-0-aner-anisch>",
        "<NGeo-0-e-isch>", "<NGeo-0-er-er>", "<NGeo-0-er-erisch>", "<NGeo-0-er-isch>",
        "<NGeo-0-ese-esisch>",
        "<NGeo-0-ianer-ianisch>",
        "<NGeo-0-0-0>",
        "<NGeo-0-ner-isch>", "<NGeo-0-ner-nisch>",
        "<NGeo-0fem-er-erisch>", "<NGeo-0masc-er-isch>",
        "<NGeo-0masc-ese-esisch>",
        "<NGeo-a-er-isch>", "<NGeo-a-ese-esisch>",
        "<NGeo-afem-er-isch>",
        "<NGeo-e-er-er>",
        "<NGeo-e-er-isch>", "<NGeo-efem-er-isch>",
        "<NGeo-ei-e-isch>",
        "<NGeo-en-aner-anisch>",
        "<NGeo-en-e-$isch>", "<NGeo-en-e-isch>",
        "<NGeo-en-er-er>", "<NGeo-en-er-isch>",
        "<NGeo-ien-e-isch>", "<NGeo-ien-er-isch>",
        "<NGeo-ien-ese-esisch>",
        "<NGeo-ien-ianer-ianisch>",
        "<NGeo-ien-ier-isch>",
        "<NGeo-istan-e-isch>",
        "<NGeo-land-$er-$er>", "<NGeo-land-e-isch>", "<NGeo-land-e-nisch>"], input_token_type=symbol_table, output_token_type=symbol_table)

    # complexity agreement features
    complexity_agreement_feats = pynini.string_map(["<simplex>", "<komposit>", "<suffderiv>", "<prefderiv>"], input_token_type=symbol_table, output_token_type=symbol_table)
    return pynini.Fst()

def map_fst_map2(symbol_table):
    '''
    Modifications of lexical entries
    '''

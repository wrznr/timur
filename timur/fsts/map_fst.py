# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur.helpers import union
from timur.helpers import concat

from timur.fsts import symbol_sets

def split_disjunctive_feats(disjunctive_feat_list, symbol_table):
    single_splits = []
    for disjunctive_feat in disjunctive_feat_list:
        splitted = []
        for cat in disjunctive_feat[1:-1].split(","):
            splitted.append("<" + cat + ">")
        single_splits.append(pynini.transducer(disjunctive_feat, pynini.string_map(splitted, input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table))
    return pynini.union(*(single_splits))

def map_fst_map(symbol_table):
    '''
    Modifications of lexical entries
    '''

    # delete initial features
    del_initial_features = pynini.transducer("", symbol_sets.initial_features(symbol_table))

    # delete categories
    del_cat_ext = pynini.transducer("", pynini.union(symbol_sets.categories(symbol_table), symbol_sets.disjunctive_categories(symbol_table)))

    # delete stem types
    del_stem_types = pynini.transducer("", symbol_sets.stem_types(symbol_table))

    # delete prefix/suffix marker
    del_prefix_suffix_marker = pynini.transducer("", symbol_sets.prefix_suffix_marker(symbol_table))

    # delete stem type features
    del_stem_type_feats = pynini.transducer("", symbol_sets.stem_type_features(symbol_table))

    # delete origin features
    del_origin_feats = pynini.transducer("", symbol_sets.origin_features(symbol_table))

    # delete complexity agreement features
    del_complexity_agreement_feats = pynini.transducer("", symbol_sets.complexity_agreement_features(symbol_table))

    # delete word complexity features
    del_complex_lex_entries = pynini.transducer("", symbol_sets.complexity_entry_features(symbol_table))

    # inflection classes
    del_infl_classes = pynini.transducer("", symbol_sets.inflection_classes(symbol_table))

    # disjunctive features
    disjunctive_feat_list = ["<CARD,DIGCARD,NE>", "<ADJ,CARD>", "<ADJ,NN>", "<CARD,NN>",
    "<CARD,NE>", "<ABK,ADJ,NE,NN>", "<ADJ,NE,NN>", "<ABK,NE,NN>",
    "<NE,NN>", "<ABK,CARD,NN>", "<ABK,NN>", "<ADJ,CARD,NN,V>",
    "<ADJ,NN,V>", "<ABK,ADJ,NE,NN,V>", "<ADJ,NE,NN,V>", "<ADV,NE,NN,V>",
    "<ABK,NE,NN,V>", "<NE,NN,V>", "<ABK,NN,V>", "<NN,V>", 
    "<frei,fremd,gebunden>", "<frei,fremd,gebunden,kurz>", "<frei,fremd,gebunden,lang>", 
    "<fremd,gebunden,lang>", "<frei,fremd,kurz>", "<frei,fremd,lang>", "<frei,gebunden>", 
    "<frei,gebunden,kurz,lang>", "<frei,gebunden,lang>", "<frei,lang>", "<klassisch,nativ>", 
    "<fremd,klassisch,nativ>", "<fremd,klassisch>", "<frei,nativ>", "<frei,fremd,nativ>", 
    "<fremd,nativ>", "<komposit,prefderiv,simplex,suffderiv>", "<prefderiv,suffderiv>", 
    "<komposit,prefderiv,simplex>", "<komposit,simplex,suffderiv>", "<komposit,simplex>", 
    "<prefderiv,simplex,suffderiv>", "<prefderiv,simplex>", "<simplex,suffderiv>"]
    disjunctive_feats = pynini.string_map(disjunctive_feat_list, input_token_type=symbol_table, output_token_type=symbol_table)
    del_disjunctive_feats = pynini.transducer("", disjunctive_feats)

    map_helper1 = union(
        symbol_sets.characters(symbol_table),
        pynini.acceptor("<FB>", token_type=symbol_table),
        pynini.acceptor("<SS>", token_type=symbol_table),
        pynini.acceptor("<Ge-Nom>", token_type=symbol_table),
        pynini.transducer("n", "<n>", input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("e", "<e>", input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("d", "<d>", input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("", "<~n>", output_token_type=symbol_table),
        pynini.transducer("", "<UL>", output_token_type=symbol_table),
        del_stem_types,
        symbol_sets.prefix_suffix_marker(symbol_table),
        del_stem_type_feats,
        pynini.transducer("", "<ge>", output_token_type=symbol_table),
        del_origin_feats,
        del_complexity_agreement_feats,
        del_complex_lex_entries,
        del_infl_classes,
        del_disjunctive_feats,
        token_type=symbol_table
        ).closure()

    map_helper2 = concat(
        map_helper1,
        pynini.concat(
          symbol_sets.characters(symbol_table),
          pynini.union(
            union(
              symbol_sets.characters(symbol_table),
              "<SUFF>",
              "<CONV>",
              token_type=symbol_table
              ),
            symbol_sets.categories(symbol_table)
            ).closure(),
          ).closure(0, 1),
        map_helper1
        )

    map1 = concat(
        del_initial_features.closure(),
        pynini.union(
          concat(
            pynini.transducer("", pynini.string_map(["<Base_Stems>", "<Pref_Stems>"], input_token_type=symbol_table, output_token_type=symbol_table)),
            map_helper2,
            del_cat_ext,
            token_type=symbol_table    
            ),
          concat(
            pynini.transducer("", pynini.string_map(["<Deriv_Stems>", "<Kompos_Stems>"], input_token_type=symbol_table, output_token_type=symbol_table)),
            map_helper2,
            symbol_sets.categories(symbol_table),
            token_type=symbol_table    
            ),
          concat(
            pynini.transducer("", "<Pref_Stems>", output_token_type=symbol_table),
            map_helper1,
            del_cat_ext,
            token_type=symbol_table    
            ),
          concat(
            pynini.transducer("", "<Suff_Stems>", output_token_type=symbol_table),
            map_helper1,
            del_cat_ext,
            map_helper1,
            symbol_sets.categories(symbol_table),
            pynini.transducer("", "<base>", output_token_type=symbol_table),
            token_type=symbol_table    
            ),
          concat(
            pynini.transducer("", "<Suff_Stems>", output_token_type=symbol_table),
            map_helper1,
            del_cat_ext,
            map_helper1,
            del_cat_ext,
            "<SUFF>",
            pynini.transducer("", "<base>", output_token_type=symbol_table),
            token_type=symbol_table    
            ),
          concat(
            pynini.transducer("", "<Suff_Stems>", output_token_type=symbol_table),
            map_helper1,
            del_cat_ext,
            map_helper1,
            symbol_sets.categories(symbol_table),
            "<SUFF>",
            pynini.transducer("", pynini.string_map(["<deriv>", "<kompos>"], input_token_type=symbol_table, output_token_type=symbol_table)),
            token_type=symbol_table  
            )
          ),
        map_helper1,
            token_type=symbol_table  
            )


    insert_prefix_suffix_marker = pynini.transducer(symbol_sets.prefix_suffix_marker(symbol_table), "", input_token_type=symbol_table)
    insert_complex_lex_entries = pynini.transducer(symbol_sets.complexity_entry_features(symbol_table), "", input_token_type=symbol_table)

    split_origin_features = pynini.union(
        pynini.transducer("<NGeo-0-$er-$er>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$er-Adj0-Up>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-$er-$isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-aner-aner>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-aner-Adj0-Up>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-aner-anisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-anisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-e-isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-er-er>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-0-0>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-0-NMasc_s_0>", "<NGeo-0-Adj0-Up>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-er-erisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-erisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-er-isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-ese-esisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-ianer-ianisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ianer-NMasc_s_0>", "<NGeo-ianisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-ner-isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ner-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0-ner-nisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ner-NMasc_s_0>", "<NGeo-nisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0fem-er-erisch>", pynini.string_map(["<NGeo-0-Name-Fem_0>", "<NGeo-er-NMasc_s_0>", "<NGeo-erisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0masc-er-isch>", pynini.string_map(["<NGeo-0-Name-Masc_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-0masc-ese-esisch>", pynini.string_map(["<NGeo-0-Name-Masc_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-a-er-isch>", pynini.string_map(["<NGeo-a-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-a-ese-esisch>", pynini.string_map(["<NGeo-a-Name-Neut_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-afem-er-isch>", pynini.string_map(["<NGeo-a-Name-Fem_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-e-er-er>", pynini.string_map(	["<NGeo-e-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-e-er-isch>", pynini.string_map(["<NGeo-e-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-efem-er-isch>", pynini.string_map(["<NGeo-e-Name-Fem_0>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-ei-e-isch>", pynini.string_map(["<NGeo-ei-Name-Fem_0>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-en-aner-anisch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-anisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-en-e-$isch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-$isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-en-e-isch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-en-er-er>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-en-er-isch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-ien-e-isch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-ien-er-isch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-ien-ese-esisch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-ien-ianer-ianisch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-ianer-NMasc_s_0>", "<NGeo-ianisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-ien-ier-isch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-ier-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-istan-e-isch>", pynini.string_map(["<NGeo-istan-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-land-$er-$er>", pynini.string_map(["<NGeo-land-Name-Neut_s>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$er-Adj0-Up>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-land-e-isch>", pynini.string_map(["<NGeo-land-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("<NGeo-land-e-nisch>", pynini.string_map(["<NGeo-land-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-nisch-Adj+>"], input_token_type=symbol_table, output_token_type=symbol_table), input_token_type=symbol_table, output_token_type=symbol_table)
        )

    map_helper3 = pynini.union(
        symbol_sets.characters(symbol_table),
        symbol_sets.initial_features(symbol_table),
        symbol_sets.stem_types(symbol_table),
        symbol_sets.categories(symbol_table),
        insert_prefix_suffix_marker,
        symbol_sets.stem_type_features(symbol_table),
        symbol_sets.origin_features(symbol_table),
        symbol_sets.complexity_agreement_features(symbol_table),
        insert_complex_lex_entries,
        symbol_sets.inflection_classes(symbol_table),
        split_disjunctive_feats(disjunctive_feat_list, symbol_table),
        split_origin_features
        )

    map2 = pynini.concat(
        map_helper3.closure(),
        concat(
          pynini.transducer("e", "<e>", input_token_type=symbol_table, output_token_type=symbol_table),
          "<VVReg-el/er>",
          token_type=symbol_table
          ).closure(0,1)
        )

    return (map1.optimize(), map2.optimize())

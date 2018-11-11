# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur.helpers import union
from timur.helpers import concat

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
    # singletons
    chars = []
    for i in range(0,256):
        symbol = chr(i)
        if symbol.isprintable() and not symbol.isspace():
            chars.append(symbol)
    singletons = pynini.string_map(chars, input_token_type=symbol_table, output_token_type=symbol_table).closure()

    # initial features
    initial_features = pynini.string_map(["<QUANT>", "<Initial>", "<NoHy>", "<ge>", "<no-ge>", "<NoPref>", "<NoDef>"], input_token_type=symbol_table, output_token_type=symbol_table)
    del_initial_features = pynini.transducer("", initial_features)

    # word categories
    cat = pynini.string_map(["<ABK>", "<ADJ>", "<ADV>", "<CARD>", "<DIGCARD>", "<NE>", "<NN>", "<PRO>", "<V>", "<ORD>", "<OTHER>", "<KSF>"], input_token_type=symbol_table, output_token_type=symbol_table)

    # delete categories
    cat_ext = pynini.string_map(["<ABK>", "<ADJ>", "<ADV>", "<CARD>", "<DIGCARD>", "<NE>", "<NN>", "<PRO>", "<V>", "<ORD>", "<OTHER>", "<CARD,DIGCARD,NE>", "<ADJ,CARD>", "<ADJ,NN>", "<CARD,NN>", "<CARD,NE>", "<ABK,ADJ,NE,NN>", "<ADJ,NE,NN>", "<ABK,NE,NN>", "<NE,NN>", "<ABK,CARD,NN>", "<ABK,NN>", "<ADJ,CARD,NN,V>", "<ADJ,NN,V>", "<ABK,ADJ,NE,NN,V>", "<ADJ,NE,NN,V>", "<ADV,NE,NN,V>", "<ABK,NE,NN,V>", "<NE,NN,V>", "<ABK,NN,V>", "<NN,V>"], input_token_type=symbol_table, output_token_type=symbol_table)
    del_cat_ext = pynini.transducer("", cat_ext)

    # stem types
    stem_types = pynini.string_map(["<Base_Stems>", "<Kompos_Stems>", "<Deriv_Stems>", "<Suff_Stems>", "<Pref_Stems>"], input_token_type=symbol_table, output_token_type=symbol_table)
    del_stem_types = pynini.transducer("", stem_types)

    # prefix/suffix marker
    prefix_suffix_marker = pynini.string_map(["<VPART>", "<VPREF>", "<PREF>", "<SUFF>", "<CONV>"], input_token_type=symbol_table, output_token_type=symbol_table)
    del_prefix_suffix_marker = pynini.transducer("", prefix_suffix_marker)

    # stem type features
    stem_type_feats = pynini.string_map(["<base>", "<deriv>", "<kompos>"], input_token_type=symbol_table, output_token_type=symbol_table)
    del_stem_type_feats = pynini.transducer("", stem_type_feats)

    # origin features
    origin_feats = pynini.string_map(["<nativ>",
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
    del_origin_feats = pynini.transducer("", origin_feats)

    # complexity agreement features
    complexity_agreement_feats = pynini.string_map(["<simplex>", "<komposit>", "<suffderiv>", "<prefderiv>"], input_token_type=symbol_table, output_token_type=symbol_table)
    del_complexity_agreement_feats = pynini.transducer("", complexity_agreement_feats)

    # complex lexicon entries
    complex_lex_entries = pynini.string_map(["<Simplex>", "<Komplex>", "<Komplex_abstrakt>", "<Komplex_semi>", "<Nominalisierung>", "<Kurzwort>"], input_token_type=symbol_table, output_token_type=symbol_table)
    del_complex_lex_entries = pynini.transducer("", complex_lex_entries)

    # inflection classes
    infl_classes = pynini.string_map([
      "<Abk_ADJ>", "<Abk_ADV>", "<Abk_ART>", "<Abk_DPRO>",
      "<Abk_KONJ>", "<Abk_NE-Low>", "<Abk_NE>", "<Abk_NN-Low>",
      "<Abk_NN>", "<Abk_PREP>", "<Abk_VPPAST>", "<Abk_VPPRES>",
      "<Adj$>", "<Adj$e>", "<Adj+(e)>", "<Adj+>", "<Adj&>",
      "<Adj+Lang>", "<Adj+e>", "<Adj-el/er>", "<Adj0>",
      "<Adj0-Up>", "<AdjComp>", "<AdjSup>", "<AdjNN>",
      "<AdjNNSuff>", "<AdjPos>", "<AdjPosAttr>", "<AdjPosPred>",
      "<AdjPosSup>", "<AdjSup>", "<Adj~+e>",
      "<Adv>",
      "<Circp>",
      "<FamName_0>", "<FamName_s>", "<Name-Pl_0>", "<Name-Pl_x>", 
      "<Intj>", "<IntjUp>",
      "<Konj-Inf>", "<Konj-Kon>", "<Konj-Sub>", "<Konj-Vgl>",
      "<N?/Pl_0>", "<N?/Pl_x>", 
      "<NFem-Deriv>", "<NFem-a/en>", "<NFem-in>", "<NFem-is/en>",
      "<NFem-is/iden>", "<NFem-s/$sse>", "<NFem-s/sse>", "<NFem-s/ssen>",
      "<NFem/Pl>", "<NFem/Sg>", "<NFem_0_$>", "<NFem_0_$e>", "<NFem_0_e>", 
      "<NFem_0_en>", "<NFem_0_n>", "<NFem_0_s>", "<NFem_0_x>",
      "<NGeo+er/in>", "<NGeo-Fem_0>", "<NGeo-Invar>", "<NGeo-Masc_0>",
      "<NGeo-Masc_s>", "<NGeo-Neut+Loc>", "<NGeo-Neut_0>", 
      "<NGeo-Neut_s>", "<NGeo-Pl_0>",
      "<NMasc-Adj>", "<NMasc-ns>", "<NMasc-s/$sse>", "<NMasc-s/Sg>",
      "<NMasc-s/sse>", "<NMasc-s0/sse>", "<NMasc-us/en>", "<NMasc-us/i>",
      "<NMasc/Pl>", "<NMasc/Sg_0>", "<NMasc/Sg_es>", "<NMasc/Sg_s>",
      "<NMasc_0_x>", "<NMasc_en_en=in>", "<NMasc_en_en>", "<NMasc_es_$e>", 
      "<NMasc_es_$er>", "<NMasc_es_e>", "<NMasc_es_en>", "<NMasc_n_n=$in>",
      "<NMasc_n_n=in>", "<NMasc_n_n>", "<NMasc_s_$>", "<NMasc_s_$x>",
      "<NMasc_s_0=in>", "<NMasc_s_0>", "<NMasc_s_e=in>", "<NMasc_s_e>",
      "<NMasc_s_en=in>", "<NMasc_s_en>", "<NMasc_s_n>", "<NMasc_s_s>",
      "<NMasc_s_x>", 
      "<NNeut-0/ien>", "<NNeut-Dimin>", "<NNeut-Herz>", "<NNeut-a/ata>",
      "<NNeut-a/en>", "<NNeut-on/a>", "<NNeut-s/$sser>", "<NNeut-s/sse>",
      "<NNeut-um/a>", "<NNeut-um/en>", "<NNeut/Pl>", "<NNeut/Sg_0>", 
      "<NNeut/Sg_en>", "<NNeut/Sg_es>", "<NNeut/Sg_s>", "<NNeut_0_x>",
      "<NNeut_es_$e>", "<NNeut_es_$er>", "<NNeut_es_e>", "<NNeut_es_en>",
      "<NNeut_es_er>", "<NNeut_s_$>", "<NNeut_s_0>", "<NNeut_s_e>",
      "<NNeut_s_en>", "<NNeut_s_n>", "<NNeut_s_s>", "<NNeut_s_x>",
      "<Name-Fem_0>", "<Name-Fem_s>", "<Name-Masc_0>", "<Name-Masc_s>",
      "<Name-Neut_s>", "<Name-Neut_0>", "<Name-Neut+Loc>", "<Name-Invar>", 
      "<Postp-Akk>", "<Postp-Dat>", "<Postp-Gen>",
      "<Pref/Adj>", "<Pref/Adv>", "<Pref/N>", "<Pref/ProAdv>", "<Pref/Sep>",
      "<Pref/V>", "<Prep-Akk>", "<Prep-Dat>", "<Prep-Gen>", "<Prep/Art-m>",
      "<Prep/Art-n>", "<Prep/Art-r>", "<Prep/Art-s>",
      "<ProAdv>",
      "<PInd-Invar>",
      "<Ptkl-Adj>", "<Ptkl-Ant>", "<Ptkl-Neg>", "<Ptkl-Zu>",
      "<VAImpPl>", "<VAImpSg>", "<VAPastKonj2>", "<VAPres1/3PlInd>", 
      "<VAPres1SgInd>", "<VAPres2PlInd>", "<VAPres2SgInd>", "<VAPres3SgInd>",
      "<VAPresKonjPl>", "<VAPresKonjSg>",
      "<VInf+PPres>", "<VInf>",
      "<VMPast>", "<VMPastKonj>", "<VMPresPl>", "<VMPresSg>", 
      "<VPPast>", "<VPPres>", "<VPastIndReg>", "<VPastIndStr>",
      "<VPastKonjStr>", "<VPresKonj>", "<VPresPlInd>",
      "<VVPP-en>", "<VVPP-t>", "<VVPastIndReg>", "<VVPastIndStr>",
      "<VVPastKonjReg>", "<VVPastKonjStr>", "<VVPastStr>", "<VVPres1+Imp>",
      "<VVPres1>", "<VVPres2+Imp0>", "<VVPres2+Imp>", "<VVPres2>",
      "<VVPres2t>", "<VVPres>", "<VVPresPl>", "<VVPresSg>",
      "<VVReg-el/er>", "<VVReg>", "<WAdv>"], input_token_type=symbol_table, output_token_type=symbol_table)
    del_infl_classes = pynini.transducer("", infl_classes)

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
        singletons,
        pynini.acceptor("<FB>", token_type=symbol_table),
        pynini.acceptor("<SS>", token_type=symbol_table),
        pynini.acceptor("<Ge-Nom>", token_type=symbol_table),
        pynini.transducer("n", "<n>", input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("e", "<e>", input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("d", "<d>", input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.transducer("", "<~n>", output_token_type=symbol_table),
        pynini.transducer("", "<UL>", output_token_type=symbol_table),
        del_stem_types,
        prefix_suffix_marker,
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
          singletons,
          pynini.union(
            union(
              singletons,
              "<SUFF>",
              "<CONV>",
              token_type=symbol_table
              ),
            cat
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
            cat,
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
            cat,
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
            cat,
            "<SUFF>",
            pynini.transducer("", pynini.string_map(["<deriv>", "<kompos>"], input_token_type=symbol_table, output_token_type=symbol_table)),
            token_type=symbol_table  
            )
          ),
        map_helper1,
            token_type=symbol_table  
            )


    insert_prefix_suffix_marker = pynini.transducer(prefix_suffix_marker, "", input_token_type=symbol_table)
    insert_complex_lex_entries = pynini.transducer(complex_lex_entries, "", input_token_type=symbol_table)

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
        singletons,
        initial_features,
        stem_types,
        cat,
        insert_prefix_suffix_marker,
        stem_type_feats,
        origin_feats,
        complexity_agreement_feats,
        insert_complex_lex_entries,
        infl_classes,
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

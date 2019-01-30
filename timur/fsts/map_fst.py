# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class MapFst:
  '''
  Modifications of lexical entries
  '''

  def __init__(self, syms):

    # store alphabet
    self.__syms = syms

    # delete initial features
    del_initial_features = pynini.transducer("", syms.initial_features)

    # delete categories
    del_cat_ext = pynini.transducer("", pynini.union(syms.categories, syms.disjunctive_categories))

    # delete stem types
    del_stem_types = pynini.transducer("", syms.stem_types)

    # delete prefix/suffix marker
    del_prefix_suffix_marker = pynini.transducer("", syms.prefix_suffix_marker)

    # insert prefix/suffix marker
    insert_prefix_suffix_marker = pynini.transducer(syms.prefix_suffix_marker, "")

    # delete stem type features
    del_stem_type_feats = pynini.transducer("", syms.stem_type_features)

    # delete origin features
    del_origin_feats = pynini.transducer("", syms.origin_features)

    # delete complexity agreement features
    del_complexity_agreement_feats = pynini.transducer("", syms.complexity_agreement_features)

    # delete word complexity features
    del_complex_lex_entries = pynini.transducer("", syms.complexity_entry_features)

    # insert word complexity features
    insert_complex_lex_entries = pynini.transducer(syms.complexity_entry_features, "")

    # inflection classes
    del_infl_classes = pynini.transducer("", syms.inflection_classes)

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
    disjunctive_feats = pynini.string_map(disjunctive_feat_list, input_token_type=syms.alphabet, output_token_type=syms.alphabet).project().optimize()
    del_disjunctive_feats = pynini.transducer("", disjunctive_feats)

    # short cut: map_helper1
    map_helper1 = pynini.union(
      syms.characters,
      pynini.acceptor("<FB>", token_type=syms.alphabet),
      pynini.acceptor("<SS>", token_type=syms.alphabet),
      pynini.transducer("e", "<Ge-Nom>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("n", "<n>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("e", "<e>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("d", "<d>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("", "<~n>", output_token_type=syms.alphabet),
      pynini.transducer("", "<UL>", output_token_type=syms.alphabet),
      del_stem_types,
      syms.prefix_suffix_marker,
      del_stem_type_feats,
      pynini.transducer("", "<ge>", output_token_type=syms.alphabet),
      del_origin_feats,
      del_complexity_agreement_feats,
      del_complex_lex_entries,
      del_infl_classes,
      del_disjunctive_feats,
      ).closure().optimize()

    # short cut: map_helper2
    map_helper2 = pynini.concat(
      map_helper1,
      pynini.concat(
        pynini.concat(
          syms.characters,
          pynini.union(
            pynini.union(
              syms.characters,
              "<SUFF>",
              pynini.acceptor("<SUFF>", token_type=syms.alphabet),
              pynini.acceptor("<CONV>", token_type=syms.alphabet)
              ),
            syms.categories
            ).closure(),
          ).closure(0, 1),
        map_helper1
        )
      ).optimize()

    # 
    self.__map1 = pynini.concat(
      del_initial_features.closure(),
      pynini.concat(
        pynini.union(
          pynini.concat(
            pynini.transducer("", pynini.string_map(["<Base_Stems>", "<Pref_Stems>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project()),
            pynini.concat(map_helper2, del_cat_ext)
            ),
          pynini.concat(
            pynini.transducer("", pynini.string_map(["<Deriv_Stems>", "<Kompos_Stems>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project()),
            pynini.concat(map_helper2, syms.categories)
            ),
          pynini.concat(
            pynini.transducer("", "<Pref_Stems>", output_token_type=syms.alphabet),
            pynini.concat(map_helper1, del_cat_ext)
            ),
          pynini.concat(
            pynini.transducer("", "<Suff_Stems>", output_token_type=syms.alphabet),
            pynini.concat(
              map_helper1,
              pynini.concat(
                del_cat_ext,
                pynini.concat(
                  map_helper1,
                  pynini.concat(
                    syms.categories,
                    pynini.transducer("", "<base>", output_token_type=syms.alphabet)
                    )
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer("", "<Suff_Stems>", output_token_type=syms.alphabet),
            pynini.concat(
              map_helper1,
              pynini.concat(
                del_cat_ext,
                pynini.concat(
                  map_helper1,
                  pynini.concat(
                    del_cat_ext,
                    pynini.concat(
                      pynini.acceptor("<SUFF>", token_type=syms.alphabet),
                      pynini.transducer("", "<base>", output_token_type=syms.alphabet)
                      )
                    )
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer("", "<Suff_Stems>", output_token_type=syms.alphabet),
            pynini.concat(
              map_helper1,
              pynini.concat(
                del_cat_ext,
                pynini.concat(
                  map_helper1,
                  pynini.concat(
                    syms.categories,
                    pynini.concat(
                      pynini.acceptor("<SUFF>", token_type=syms.alphabet),
                      pynini.transducer("", pynini.string_map(["<deriv>", "<kompos>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project())
                      )
                    )
                  )
                )
              )
            )
          ),
        map_helper1,
      )
    ).optimize()

    split_origin_features = pynini.union(
      pynini.transducer("<NGeo-0-$er-$er>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$er-Adj0-Up>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-$er-$isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-aner-aner>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-aner-Adj0-Up>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-aner-anisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-anisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-e-isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-er-er>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-0-0>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-0-NMasc_s_0>", "<NGeo-0-Adj0-Up>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-er-erisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-erisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-er-isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-ese-esisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-ianer-ianisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ianer-NMasc_s_0>", "<NGeo-ianisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-ner-isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ner-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0-ner-nisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ner-NMasc_s_0>", "<NGeo-nisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0fem-er-erisch>", pynini.string_map(["<NGeo-0-Name-Fem_0>", "<NGeo-er-NMasc_s_0>", "<NGeo-erisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0masc-er-isch>", pynini.string_map(["<NGeo-0-Name-Masc_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-0masc-ese-esisch>", pynini.string_map(["<NGeo-0-Name-Masc_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-a-er-isch>", pynini.string_map(["<NGeo-a-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-a-ese-esisch>", pynini.string_map(["<NGeo-a-Name-Neut_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-afem-er-isch>", pynini.string_map(["<NGeo-a-Name-Fem_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-e-er-er>", pynini.string_map(	["<NGeo-e-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-e-er-isch>", pynini.string_map(["<NGeo-e-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-efem-er-isch>", pynini.string_map(["<NGeo-e-Name-Fem_0>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-ei-e-isch>", pynini.string_map(["<NGeo-ei-Name-Fem_0>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-en-aner-anisch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-anisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-en-e-$isch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-$isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-en-e-isch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-en-er-er>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-en-er-isch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-ien-e-isch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-ien-er-isch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-ien-ese-esisch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-ien-ianer-ianisch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-ianer-NMasc_s_0>", "<NGeo-ianisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-ien-ier-isch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-ier-NMasc_s_0>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-istan-e-isch>", pynini.string_map(["<NGeo-istan-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-land-$er-$er>", pynini.string_map(["<NGeo-land-Name-Neut_s>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$er-Adj0-Up>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-land-e-isch>", pynini.string_map(["<NGeo-land-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet),
      pynini.transducer("<NGeo-land-e-nisch>", pynini.string_map(["<NGeo-land-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-nisch-Adj+>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(), input_token_type=syms.alphabet, output_token_type=syms.alphabet)
      ).optimize()

    map_helper3 = pynini.union(
      syms.characters,
      syms.circumfix_features,
      syms.initial_features,
      syms.stem_types,
      syms.categories,
      insert_prefix_suffix_marker,
      syms.stem_type_features,
      syms.origin_features,
      syms.complexity_agreement_features,
      insert_complex_lex_entries,
      syms.inflection_classes,
      self.__split_disjunctive_feats(disjunctive_feat_list),
      split_origin_features
      ).optimize()

    self.__map2 = pynini.concat(
      map_helper3.closure(),
      pynini.concat(
        pynini.transducer("e", "<e>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
        pynini.concat(
          pynini.string_map(["l", "r"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project(),
          pynini.concat(
            pynini.string_map(["<ADJ>", "<NE>", "<NN>", "<V>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project().closure(0,1),
            pynini.concat(
              pynini.acceptor("<V>", token_type=syms.alphabet),
              pynini.concat(
                pynini.string_map(["<SUFF>", "<CONV>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project().closure(0,1),
                pynini.concat(
                  pynini.acceptor("<base> <nativ>", token_type=syms.alphabet),
                  pynini.concat(
                    insert_complex_lex_entries.closure(0,1),
                    pynini.acceptor("<VVReg-el/er>", token_type=syms.alphabet)
                    )
                  )
                )
              )
            )
          )
        ).closure(0,1)
      ).optimize()


  @property
  def map1(self):
    return self.__map1

  @property
  def map2(self):
    return self.__map2

  def __split_disjunctive_feats(self, disjunctive_feat_list):
    single_splits = []
    for disjunctive_feat in disjunctive_feat_list:
      splitted = []
      for cat in disjunctive_feat[1:-1].split(","):
        splitted.append("<" + cat + ">")
        single_splits.append(pynini.transducer(disjunctive_feat, pynini.string_map(splitted, input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet), input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet))
    return pynini.union(*(single_splits)).optimize()

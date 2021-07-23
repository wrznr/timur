# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class MapFst:
  '''
  Modifications of lexical entries
  '''

  def __init__(self, syms):
    
    with pynini.default_token_type(syms.alphabet):

      # store alphabet
      self.__syms = syms

      # delete initial features
      del_initial_features = pynini.cross("", syms.initial_features)

      # delete categories
      del_cat_ext = pynini.cross("", pynini.union(syms.categories, syms.disjunctive_categories))

      # delete stem types
      del_stem_types = pynini.cross("", syms.stem_types)

      # delete prefix/suffix marker
      del_prefix_suffix_marker = pynini.cross("", syms.prefix_suffix_marker)

      # insert prefix/suffix marker
      insert_prefix_suffix_marker = pynini.cross(syms.prefix_suffix_marker, "")

      # delete stem type features
      del_stem_type_feats = pynini.cross("", syms.stem_type_features)

      # delete origin features
      del_origin_feats = pynini.cross("", syms.origin_features)

      # delete complexity agreement features
      del_complexity_agreement_feats = pynini.cross("", syms.complexity_agreement_features)

      # delete word complexity features
      del_complex_lex_entries = pynini.cross("", syms.complexity_entry_features)

      # insert word complexity features
      insert_complex_lex_entries = pynini.cross(syms.complexity_entry_features, "")

      # inflection classes
      del_infl_classes = pynini.cross("", syms.inflection_classes)

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
      "<fremd,nativ>","<nativ,prefnativ>","<frei,nativ,prefnativ>",
      "<komposit,prefderiv,simplex,suffderiv>", "<prefderiv,suffderiv>", 
      "<komposit,prefderiv,simplex>", "<komposit,simplex,suffderiv>", "<komposit,simplex>", 
      "<prefderiv,simplex,suffderiv>", "<prefderiv,simplex>", "<simplex,suffderiv>"]
      disjunctive_feats = pynini.string_map(disjunctive_feat_list).project("input").optimize()
      del_disjunctive_feats = pynini.cross("", disjunctive_feats)

      # short cut: map_helper1
      map_helper1 = pynini.union(
        syms.characters,
        pynini.accep("<FB>"),
        pynini.accep("<SS>"),
        pynini.cross("e", "<Ge-Nom>"),
        pynini.cross("n", "<n>"),
        pynini.cross("e", "<e>"),
        pynini.cross("d", "<d>"),
        pynini.cross("", "<~n>"),
        pynini.cross("", "<UL>"),
        del_stem_types,
        syms.prefix_suffix_marker,
        del_stem_type_feats,
        pynini.cross("", "<ge>"),
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
                pynini.accep("<SUFF>"),
                pynini.accep("<CONV>")
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
              pynini.cross("", pynini.string_map(["<Base_Stems>", "<Pref_Stems>"]).project("input")),
              pynini.concat(map_helper2, del_cat_ext)
              ),
            pynini.concat(
              pynini.cross("", pynini.string_map(["<Deriv_Stems>", "<Kompos_Stems>"]).project("input")),
              pynini.concat(map_helper2, syms.categories)
              ),
            pynini.cross("", "<Pref_Stems>") + map_helper1 + del_cat_ext,
            pynini.cross("", "<Suff_Stems>") + map_helper1 + del_cat_ext
              + map_helper1 + syms.categories + pynini.cross("", "<base>"),
            pynini.cross("", "<Suff_Stems>") + map_helper1 + del_cat_ext
              + pynini.concat(map_helper1, del_cat_ext + pynini.accep("<SUFF>")).closure(1) 
              + pynini.cross("", "<base>"),
            pynini.cross("", "<Suff_Stems>") + map_helper1 + del_cat_ext
              + pynini.concat(map_helper1, syms.categories + pynini.accep("<SUFF>")).closure(1)
              + pynini.cross("", pynini.string_map(["<deriv>", "<kompos>"]).project("input"))
            ),
          map_helper1,
        )
      ).optimize()

      split_origin_features = pynini.union(
        pynini.cross("<NGeo-0-$er-$er>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$er-Adj0-Up>"]).project("input")),
        pynini.cross("<NGeo-0-$er-$isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0-aner-aner>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-aner-Adj0-Up>"]).project("input")),
        pynini.cross("<NGeo-0-aner-anisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-anisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0-e-isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0-er-er>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>"]).project("input")),
        pynini.cross("<NGeo-0-0-0>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-0-NMasc_s_0>", "<NGeo-0-Adj0-Up>"]).project("input")),
        pynini.cross("<NGeo-0-er-erisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-erisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0-er-isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0-ese-esisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0-ianer-ianisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ianer-NMasc_s_0>", "<NGeo-ianisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0-ner-isch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ner-NMasc_s_0>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0-ner-nisch>", pynini.string_map(["<NGeo-0-Name-Neut_s>", "<NGeo-ner-NMasc_s_0>", "<NGeo-nisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0fem-er-erisch>", pynini.string_map(["<NGeo-0-Name-Fem_0>", "<NGeo-er-NMasc_s_0>", "<NGeo-erisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0masc-er-isch>", pynini.string_map(["<NGeo-0-Name-Masc_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-0masc-ese-esisch>", pynini.string_map(["<NGeo-0-Name-Masc_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-a-er-isch>", pynini.string_map(["<NGeo-a-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-a-ese-esisch>", pynini.string_map(["<NGeo-a-Name-Neut_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-afem-er-isch>", pynini.string_map(["<NGeo-a-Name-Fem_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-e-er-er>", pynini.string_map(	["<NGeo-e-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>"]).project("input")),
        pynini.cross("<NGeo-e-er-isch>", pynini.string_map(["<NGeo-e-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-efem-er-isch>", pynini.string_map(["<NGeo-e-Name-Fem_0>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-ei-e-isch>", pynini.string_map(["<NGeo-ei-Name-Fem_0>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-en-aner-anisch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-anisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-en-e-$isch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-$isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-en-e-isch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-en-er-er>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>"]).project("input")),
        pynini.cross("<NGeo-en-er-isch>", pynini.string_map(["<NGeo-en-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-ien-e-isch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-ien-er-isch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-ien-ese-esisch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-ien-ianer-ianisch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-ianer-NMasc_s_0>", "<NGeo-ianisch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-ien-ier-isch>", pynini.string_map(["<NGeo-ien-Name-Neut_s>", "<NGeo-ier-NMasc_s_0>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-istan-e-isch>", pynini.string_map(["<NGeo-istan-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-land-$er-$er>", pynini.string_map(["<NGeo-land-Name-Neut_s>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$er-Adj0-Up>"]).project("input")),
        pynini.cross("<NGeo-land-e-isch>", pynini.string_map(["<NGeo-land-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-isch-Adj+>"]).project("input")),
        pynini.cross("<NGeo-land-e-nisch>", pynini.string_map(["<NGeo-land-Name-Neut_s>", "<NGeo-e-NMasc_n_n>", "<NGeo-nisch-Adj+>"]).project("input"))
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
          pynini.cross("e", "<e>"),
          pynini.concat(
            pynini.string_map(["l", "r"]).project("input"),
            pynini.concat(
              pynini.string_map(["<ADJ>", "<NE>", "<NN>", "<V>"]).project("input").closure(0,1),
              pynini.concat(
                pynini.accep("<V>"),
                pynini.concat(
                  pynini.string_map(["<SUFF>", "<CONV>"]).project("input").closure(0,1),
                  pynini.concat(
                    pynini.accep("<base> <nativ>"),
                    pynini.concat(
                      insert_complex_lex_entries.closure(0,1),
                      pynini.accep("<VVReg-el/er>")
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
    with pynini.default_token_type(self.__syms.alphabet):
      single_splits = []
      for disjunctive_feat in disjunctive_feat_list:
        splitted = []
        for cat in disjunctive_feat[1:-1].split(","):
          splitted.append("<" + cat + ">")
          single_splits.append(pynini.cross(disjunctive_feat, pynini.string_map(splitted)))
      return pynini.union(*(single_splits)).optimize()

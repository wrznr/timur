# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class InflectionFst:
  '''
  Define the inflection paradigm
  '''

  def __init__(self,syms):

    #
    # store alphabet
    #
    self.__syms = syms

    with pynini.default_token_type(self.__syms.alphabet):

      #
      # case markers
      #
      fix       = pynini.cross("", "<Fix#>")
      adj       = pynini.cross("", "<Low#>")
      adj_up    = pynini.cross("", "<Up#>")
      n         = pynini.cross("", "<Up#>")
      n_low     = pynini.cross("", "<Low#>")
      v         = pynini.cross("", "<Low#>")
      closed    = pynini.cross("", "<Low#>")
      closed_up = pynini.cross("", "<Up#>")

      #
      # inflection classes
      #

      #
      # abbreviations
      abk_ADJ = pynini.concat(
          pynini.cross("<^ABK> <+ADJ>", ""),
          adj
          )
      abk_ADV = pynini.concat(
          pynini.cross("<^ABK> <+ADV>", ""),
          closed
          )
      abk_ART = pynini.concat(
          pynini.cross("<^ABK> <+ART>", ""),
          closed
          )
      abk_DPRO = pynini.concat(
          pynini.cross("<^ABK> <+DEMPRO>", ""),
          closed
          )
      abk_KONJ = pynini.concat(
          pynini.cross("<^ABK> <+KONJ>", ""),
          closed
          )
      abk_NE = pynini.concat(
          pynini.cross("<^ABK> <+NE>", ""),
          n
          )
      abk_NE_Low = pynini.concat(
          pynini.cross("<^ABK> <+NE>", ""),
          n_low
          )
      abk_NN = pynini.concat(
          pynini.cross("<^ABK> <+NN>", ""),
          n
          )
      abk_NN_Low = pynini.concat(
          pynini.cross("<^ABK> <+NN>", ""),
          n_low
          )
      abk_PREP = pynini.concat(
          pynini.cross("<^ABK> <+PREP>", ""),
          closed
          )
      abk_VPPAST = pynini.concat(
          pynini.cross("<^ABK> <^VPPAST> <+ADJ>", ""),
          adj
          )
      abk_VPPRES = pynini.concat(
          pynini.cross("<^ABK> <^VPPRES> <+ADJ>", ""),
          adj
          )

      #
      # adjectives

      # invariant adjectives
      self.__adj0 = pynini.concat(
          pynini.cross("<+ADJ> <Invar>", ""),
          adj
          )
      self.__adj0_up = pynini.concat(
          pynini.cross("<+ADJ> <Invar>", ""),
          adj_up
          )

      # inflectional endings
      adj_flex_suff = pynini.union(
          pynini.concat(
            pynini.cross("<Masc> <Nom> <Sg> <St/Mix>", "e r"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Masc> <Nom> <Sg> <Sw>", "e"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Masc> <Gen> <Sg>", "e n"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Masc> <Dat> <Sg> <St>", "e m"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Masc> <Dat> <Sg> <Sw/Mix>", "e n"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Masc> <Akk> <Sg>", "e n"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Fem> <Nom> <Sg>", "e"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Fem> <Gen> <Sg> <St>", "e r"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Fem> <Gen> <Sg> <Sw/Mix>", "e n"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Fem> <Dat> <Sg> <St>", "e r"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Fem> <Dat> <Sg> <Sw/Mix>", "e n"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Fem> <Akk> <Sg>", "e"),
            adj
            ),
          pynini.concat(
            pynini.cross("<Neut> <Nom> <Sg> <St/Mix>", "e s"),
            adj
            ),
          pynini.concat(
              pynini.cross("<Neut> <Nom> <Sg> <Sw>", "e"),
              adj
              ),
          pynini.concat(
              pynini.cross("<Neut> <Gen> <Sg>", "e n"),
              adj
              ),
          pynini.concat(
              pynini.cross("<Neut> <Dat> <Sg> <St>", "e m"),
              adj
              ),
          pynini.concat(
              pynini.cross("<Neut> <Dat> <Sg> <Sw/Mix>", "e n"),
              adj
              ),
          pynini.concat(
              pynini.cross("<Neut> <Akk> <Sg> <St/Mix>", "e s"),
              adj
              ),
          pynini.concat(
              pynini.cross("<Neut> <Akk> <Sg> <Sw>", "e"),
              adj
              ),
          pynini.concat(
              pynini.cross("<NoGend> <Nom> <Pl> <St>", "e"),
              adj
              ),
          pynini.concat(
              pynini.cross("<NoGend> <Nom> <Pl> <Sw/Mix>", "e n"),
              adj
              ),
          pynini.concat(
              pynini.cross("<NoGend> <Gen> <Pl> <Sw/Mix>", "e n"),
              adj
              ),
          pynini.concat(
              pynini.cross("<NoGend> <Gen> <Pl> <St>", "e r"),
              adj
              ),
          pynini.concat(
              pynini.cross("<NoGend> <Dat> <Pl>", "e n"),
              adj
              ),
          pynini.concat(
              pynini.cross("<NoGend> <Akk> <Pl> <Sw/Mix>", "e n"),
              adj
              ),
          pynini.concat(
              pynini.cross("<NoGend> <Akk> <Pl> <St>", "e"),
              adj
              )
          ).optimize()

      # inflectional endings for nominalization
      adj_nn_suff = pynini.union(
          pynini.concat(
            pynini.cross("<+NN> <Masc> <Nom> <Sg> <St/Mix>", "e r"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Masc> <Nom> <Sg> <Sw>", "e"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Masc> <Gen> <Sg>", "e n"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Masc> <Dat> <Sg> <St>", "e m"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Masc> <Dat> <Sg> <Sw/Mix>", "e n"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Masc> <Akk> <Sg>", "e n"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Fem> <Nom> <Sg>", "e"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Fem> <Gen> <Sg> <St>", "e r"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Fem> <Gen> <Sg> <Sw/Mix>", "e n"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Fem> <Dat> <Sg> <St>", "e r"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Fem> <Dat> <Sg> <Sw/Mix>", "e n"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Fem> <Akk> <Sg>", "e"),
            n
            ),
          pynini.concat(
            pynini.cross("<+NN> <Neut> <Nom> <Sg> <St/Mix>", "e s"),
            n
            ),
          pynini.concat(
              pynini.cross("<+NN> <Neut> <Nom> <Sg> <Sw>", "e"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <Neut> <Gen> <Sg>", "e n"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <Neut> <Dat> <Sg> <St>", "e m"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <Neut> <Dat> <Sg> <Sw/Mix>", "e n"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <Neut> <Akk> <Sg> <St/Mix>", "e s"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <Neut> <Akk> <Sg> <Sw>", "e"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <NoGend> <Nom> <Pl> <St>", "e"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <NoGend> <Nom> <Pl> <Sw/Mix>", "e n"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <NoGend> <Gen> <Pl> <Sw/Mix>", "e n"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <NoGend> <Gen> <Pl> <St>", "e r"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <NoGend> <Dat> <Pl>", "e n"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <NoGend> <Akk> <Pl> <Sw/Mix>", "e n"),
              n
              ),
          pynini.concat(
              pynini.cross("<+NN> <NoGend> <Akk> <Pl> <St>", "e"),
              n
              )
          ).optimize()

      # positive
      adj_pos = pynini.union(
          pynini.concat(
            pynini.cross("<+ADJ> <Pos> <Pred>", ""),
            adj
            ),
          pynini.concat(
            pynini.cross("<+ADJ> <Pos> <Adv>", ""),
            adj
            ),
          pynini.concat(
            pynini.cross("<+ADJ> <Pos>", ""),
            adj_flex_suff
            ),
          ).optimize()

      adj_pos_attr = pynini.concat(
          pynini.cross("<+ADJ> <Pos>", "<FB>"),
          adj_flex_suff
          ).optimize()

      adj_pos_pred = pynini.concat(
          pynini.cross("<+ADJ> <Pos> <Pred>", ""),
          adj
          )

      # superlative
      adj_sup = pynini.union(
          pynini.concat(
            pynini.cross("<+ADJ> <Sup> <Pred>", "s t e n"),
            adj
            ),
          pynini.concat(
            pynini.cross("<+ADJ> <Sup> <Pred>", "s t"),
            adj
            ),
          pynini.concat(
            pynini.cross("<+ADJ> <Sup> <Adv>", "s t e n"),
            adj
            ),
          pynini.concat(
            pynini.cross("<+ADJ> <Sup>", "s t"),
            adj_flex_suff
            ),
          ).optimize()

      # superlative with e
      adj_sup_e = pynini.union(
          pynini.concat(
            pynini.cross("<+ADJ> <Sup> <Pred>", "e s t e n"),
            adj
            ),
          pynini.concat(
            pynini.cross("<+ADJ> <Sup> <Pred>", "e s t"),
            adj
            ),
          pynini.concat(
            pynini.cross("<+ADJ> <Sup> <Adv>", "e s t e n"),
            adj
            ),
          pynini.concat(
            pynini.cross("<+ADJ> <Sup>", "e s t"),
            adj_flex_suff
            ),
          ).optimize()

      # comparative
      adj_comp = pynini.union(
          pynini.concat(
            pynini.cross("<+ADJ> <Comp> <Pred>", "e r"),
            adj
            ),
          pynini.concat(
            pynini.cross("<+ADJ> <Comp> <Adv>", "e r"),
            adj
            ),
          pynini.concat(
            pynini.cross("<+ADJ> <Comp>", "e r"),
            adj_flex_suff
            ),
          ).optimize()

      # inflection classes (?)
      adj_nn = adj_pos_pred

      self.__adj_plus = pynini.union(
          pynini.concat(
            pynini.cross("", "<FB>"),
            adj_pos
            ),
          pynini.concat(
            pynini.cross("", "<FB>"),
            adj_comp
            ),
          pynini.concat(
            pynini.cross("", "<FB>"),
            adj_sup
            )
          ).optimize()

      self.__adj_plus_e = pynini.union(
          pynini.concat(
            pynini.cross("", "<FB>"),
            adj_pos
            ),
          pynini.concat(
            pynini.cross("", "<FB>"),
            adj_comp
            ),
          pynini.concat(
            pynini.cross("", "<FB>"),
            adj_sup_e
            )
          ).optimize()

      adj_pos_sup = pynini.union(
          pynini.concat(
            pynini.cross("", "<FB>"),
            adj_pos_attr
            ),
          pynini.concat(
            pynini.cross("", "<FB>"),
            adj_sup
            )
          ).optimize()

      adj_umlaut = pynini.union(
          pynini.concat(
            pynini.cross("", "<FB>"),
            adj_pos
            ),
          pynini.concat(
            pynini.cross("", "<UL>"),
            adj_comp
            ),
          pynini.concat(
            pynini.cross("", "<UL>"),
            adj_sup
            )
          ).optimize()

      adj_umlaut_e = pynini.union(
          pynini.concat(
            pynini.cross("", "<FB>"),
            adj_pos
            ),
          pynini.concat(
            pynini.cross("", "<UL>"),
            adj_comp
            ),
          pynini.concat(
            pynini.cross("", "<UL> e"),
            adj_sup
            )
          ).optimize()

      adj_ss_e = pynini.union(
          pynini.concat(
            pynini.cross("", "<SS> <FB>"),
            adj_pos
            ),
          pynini.concat(
            pynini.cross("", "<SS> <FB>"),
            adj_comp
            ),
          pynini.concat(
            pynini.cross("", "<SS> <FB> e"),
            adj_sup
            )
          ).optimize()

      #
      # nouns
      #
   
      #
      # inflection classes

      #
      # inflection endings: atomic

      # Frau; Mythos; Chaos
      n_sg_0 = pynini.union(
          pynini.concat(
            pynini.cross("<Nom> <Sg>", "<FB>"),
            n
            ),
          pynini.concat(
            pynini.cross("<Gen> <Sg>", "<FB>"),
            n
            ),
          pynini.concat(
            pynini.cross("<Dat> <Sg>", "<FB>"),
            n
            ),
          pynini.concat(
            pynini.cross("<Akk> <Sg>", "<FB>"),
            n
            )
          ).optimize()

      # Opa-s, Klima-s
      n_sg_s = pynini.union(
          pynini.concat(
            pynini.cross("<Nom> <Sg>", "<FB>"),
            n
            ),
          pynini.concat(
            pynini.cross("<Gen> <Sg>", "<FB> s"),
            n
            ),
          pynini.concat(
            pynini.cross("<Dat> <Sg>", "<FB>"),
            n
            ),
          pynini.concat(
            pynini.cross("<Akk> <Sg>", "<FB>"),
            n
            )
          ).optimize()

      # Haus-es, Geist-(e)s
      n_sg_es = pynini.union(
          pynini.concat(
            pynini.cross("<Nom> <Sg>", "<FB>"),
            n
            ),
          pynini.concat(
            pynini.cross("<Gen> <Sg>", "<FB> e s <^Gen>"),
            n
            ),
          pynini.concat(
            pynini.cross("<Dat> <Sg>", "<FB>"),
            n
            ),
          pynini.concat(
            pynini.cross("<Dat> <Sg>", "<FB> e"),
            n
            ),
          pynini.concat(
            pynini.cross("<Akk> <Sg>", "<FB>"),
            n
            )
          ).optimize()

      n_pl_0 = pynini.union(
          pynini.concat(
            pynini.cross("<Nom> <Pl>", ""),
            n
            ),
          pynini.concat(
            pynini.cross("<Gen> <Pl>", ""),
            n
            ),
          pynini.concat(
            pynini.cross("<Dat> <Pl>", "n"),
            n
            ),
          pynini.concat(
            pynini.cross("<Akk> <Pl>", ""),
            n
            )
          ).optimize()

      n_pl_x = pynini.union(
          pynini.concat(
            pynini.cross("<Nom> <Pl>", ""),
            n
            ),
          pynini.concat(
            pynini.cross("<Gen> <Pl>", ""),
            n
            ),
          pynini.concat(
            pynini.cross("<Dat> <Pl>", ""),
            n
            ),
          pynini.concat(
            pynini.cross("<Akk> <Pl>", ""),
            n
            )
          ).optimize()


      #
      # inflection endings: meta
      n_es_e = pynini.union(
          n_sg_es,
          pynini.concat(
            pynini.cross("", "<FB> e"),
            n_pl_0
            )
          )
      n_es_e_ul = pynini.union(
          n_sg_es,
          pynini.concat(
            pynini.cross("", "<UL> e"),
            n_pl_0
            )
          )
      n_es_en = pynini.union(
          n_sg_es,
          pynini.concat(
            pynini.cross("", "<FB> e n"),
            n_pl_x
            )
          )
      n_0_en = pynini.union(
          n_sg_0,
          pynini.concat(
            pynini.cross("", "<FB> e n"),
            n_pl_x
            )
          )
      n_0_n = pynini.union(
          n_sg_0,
          pynini.concat(
            pynini.cross("", "<FB> n"),
            n_pl_x
            )
          )
      n_s_x = pynini.union(
          n_sg_s,
          n_pl_x
          )

      # NMasc_es_e: Tag-(e)s/Tage
      self.__nmasc_es_e = pynini.concat(
          pynini.cross("<+NN> <Masc>", ""),
          n_es_e
          ).optimize()

      # NMasc_es_e$: Arzt-(e)s/Ärzte
      self.__nmasc_es_e_ul = pynini.concat(
          pynini.cross("<+NN> <Masc>", ""),
          n_es_e_ul
          ).optimize()

      # NMasc_es_en: Fleck-(e)s/Flecken
      self.__nmasc_es_en = pynini.concat(
          pynini.cross("<+NN> <Masc>", ""),
          n_es_en
          ).optimize()

      # NFem-Deriv
      self.__nfem_deriv = pynini.concat(
          pynini.cross("<+NN> <Fem>", ""),
          n_0_en
          ).optimize()

      # NFem_0_n: Kammer/Kammern
      self.__nfem_0_n = pynini.concat(
          pynini.cross("<+NN> <Fem>", ""),
          n_0_n
          ).optimize()

      # NNeut-Dimin: Mäuschen-s/Mäuschen
      self.__nneut_dimin = pynini.concat(
          pynini.cross("<+NN> <Neut>", ""),
          n_s_x
          ).optimize()

      # NNeut/Sg_s: Abitur-s/--
      self.__nneut_sg_s = pynini.concat(
          pynini.cross("<+NN> <Neut>", ""),
          n_sg_s
          ).optimize()
      
      #
      # verbs
      #

      #
      # inflection endings: atomic

      # bin's
      v_plus_es = pynini.cross("/ \' s", "\' s").closure(0, 1) + v

      # (ich) lerne
      v_pres_reg_1 = pynini.concat(
          pynini.cross("<+V> <1> <Sg> <Pres> <Ind>", "<FB> e"),
          v_plus_es
          ).optimize()

      # (du) lernst
      v_pres_reg_2 = pynini.concat(
          pynini.cross("<+V> <2> <Sg> <Pres> <Ind>", "<DEL-S> s t"),
          v_plus_es
          ).optimize()

      # (er/sie/es) lernt
      v_pres_reg_3 = pynini.concat(
          pynini.cross("<+V> <3> <Sg> <Pres> <Ind>", "<DEL-S> t"),
          v_plus_es
          ).optimize()

      # (wir/ihr/sie) lernen
      v_pres_pl_ind = pynini.concat(
          pynini.union(
            pynini.cross("<+V> <1> <Pl> <Pres> <Ind>", "<FB> e n"),
            pynini.cross("<+V> <2> <Pl> <Pres> <Ind>", "<DEL-S> t"),
            pynini.cross("<+V> <3> <Pl> <Pres> <Ind>", "<FB> e n")
            ),
          v_plus_es
          ).optimize()

      # (ich/du/sie/wir/ihr/sie) lernen
      v_pres_subj = pynini.concat(
          pynini.union(
            pynini.cross("<+V> <1> <Sg> <Pres> <Konj>", "<FB> e"),
            pynini.cross("<+V> <2> <Sg> <Pres> <Konj>", "<FB> e s t"),
            pynini.cross("<+V> <3> <Sg> <Pres> <Konj>", "<FB> e"),
            pynini.cross("<+V> <1> <Pl> <Pres> <Konj>", "<FB> e n"),
            pynini.cross("<+V> <2> <Pl> <Pres> <Konj>", "<FB> e t"),
            pynini.cross("<+V> <3> <Pl> <Pres> <Konj>", "<FB> e n")
            ),
          v_plus_es
          ).optimize()

      # (ich/du/sie/wir/ihr/sie) lernten
      v_past_ind_reg = pynini.concat(
          pynini.union(
            pynini.cross("<+V> <1> <Sg> <Past> <Ind>", "<DEL-S> t e"),
            pynini.cross("<+V> <2> <Sg> <Past> <Ind>", "<DEL-S> t e s t"),
            pynini.cross("<+V> <3> <Sg> <Past> <Ind>", "<DEL-S> t e"),
            pynini.cross("<+V> <1> <Pl> <Past> <Ind>", "<DEL-S> t e n"),
            pynini.cross("<+V> <2> <Pl> <Past> <Ind>", "<DEL-S> t e t"),
            pynini.cross("<+V> <3> <Pl> <Past> <Ind>", "<DEL-S> t e n")
            ),
          v_plus_es
          ).optimize()

      # (wir/ihr/sie) lernten
      v_past_subj_reg = pynini.concat(
          pynini.union(
            pynini.cross("<+V> <1> <Sg> <Past> <Konj>", "<DEL-S> t e"),
            pynini.cross("<+V> <2> <Sg> <Past> <Konj>", "<DEL-S> t e s t"),
            pynini.cross("<+V> <3> <Sg> <Past> <Konj>", "<DEL-S> t e"),
            pynini.cross("<+V> <1> <Pl> <Past> <Konj>", "<DEL-S> t e n"),
            pynini.cross("<+V> <2> <Pl> <Past> <Konj>", "<DEL-S> t e t"),
            pynini.cross("<+V> <3> <Pl> <Past> <Konj>", "<DEL-S> t e n")
            ),
          v_plus_es
          ).optimize()

      # kommt, schaut!
      v_imp_pl = pynini.concat(
          pynini.cross("<+V> <Imp> <Pl>", "<DEL-S> t <^imp>"),
          v_plus_es
          ).optimize()

      # kommt, schaut!
      v_imp_sg = pynini.concat(
          pynini.cross("<+V> <Imp> <Sg>", "<DEL-S> <^imp>"),
          v_plus_es
          ).optimize()

      # SMOR: investigate Lernen<+NN>
      v_inf = pynini.union(
          pynini.union(
            pynini.cross("<+V> <Inf>", ""),
            pynini.cross("<+V> <Inf> <zu>", "<^zz>")
            ) + v,
          pynini.cross("<V> <CONV>", "") + self.__nneut_sg_s,
          )

      # SMOR: investigate lernendes<+ADJ>
      v_ppres = pynini.union(
          pynini.cross("<+V> <PPres>", ""),
          pynini.cross("<+V> <PPres> <zu>", "<^zz>")
          ) + v

      # SMOR: investigate gelerntes<+ADJ>
      v_ppast = pynini.cross("<+V> <PPast>", "<^pp>") + v

      # lernend
      v_inf_plus_ppres = pynini.union(
          v_inf,
          pynini.concat(
            pynini.cross("", "d"),
            v_ppres
            )
          ).optimize()

      # lernen
      v_inf_stem = pynini.concat(
          pynini.cross("", "<FB> e n"),
          v_inf_plus_ppres
          ).optimize()

      # gelernt
      v_pp_t = pynini.concat(
          pynini.cross("", "<DEL-S> t"),
          v_ppast
          ).optimize()

      #
      # inflection endings: meta
      v_flex_pres_1 = pynini.union(
          v_pres_reg_1,
          v_pres_pl_ind,
          v_pres_subj,
          v_imp_pl,
          v_inf_stem
          ).optimize()

      v_flex_pres_reg = pynini.union(
            v_flex_pres_1,
            v_pres_reg_2,
            v_pres_reg_3,
            v_imp_sg
          ).optimize()

      v_flex_reg = pynini.union(
          v_flex_pres_reg,
          v_past_ind_reg,
          v_past_subj_reg,
          v_pp_t
          ).optimize()
      

      #
      # inflection classes

      # VVReg: lernen
      self.__vv_reg = pynini.concat(
          pynini.cross("e n", ""),
          v_flex_reg
          ).optimize()



      #
      # building the inflection cross
      #
      self.__inflection = self.__construct_inflection()

      #
      # definition of a filter which enforces the correct inflection
      #
      self.__inflection_filter = self.__construct_inflection_filter()

  @property
  def inflection(self):
    '''
    Return the inflection cross 
    '''
    return self.__inflection

  @property
  def inflection_filter(self):
    '''
    Return the complete inflection filter 
    '''
    return self.__inflection_filter

  def __construct_inflection(self):
    '''
    Build the inflection cross
    '''
    with pynini.default_token_type(self.__syms.alphabet):
      return pynini.union(
          pynini.concat(
            pynini.cross("", "<Adj0>"),
            self.__adj0
            ),
          pynini.concat(
            pynini.cross("", "<Adj0-Up>"),
            self.__adj0_up
            ),
          pynini.concat(
            pynini.cross("", "<Adj+>"),
            self.__adj_plus
            ),
          pynini.concat(
            pynini.cross("", "<Adj+e>"),
            self.__adj_plus_e
            ),
          pynini.concat(
            pynini.cross("", "<NMasc_es_e>"),
            self.__nmasc_es_e
            ),
          pynini.concat(
            pynini.cross("", "<NMasc_es_$e>"),
            self.__nmasc_es_e_ul
            ),
          pynini.concat(
            pynini.cross("", "<NMasc_es_en>"),
            self.__nmasc_es_en
            ),
          pynini.concat(
            pynini.cross("", "<NFem-Deriv>"),
            self.__nfem_deriv
            ),
          pynini.concat(
            pynini.cross("", "<NFem_0_n>"),
            self.__nfem_0_n
            ),
          pynini.concat(
            pynini.cross("", "<NNeut-Dimin>"),
            self.__nneut_dimin
            ),
          pynini.concat(
            pynini.cross("", "<NNeut/Sg_s>"),
            self.__nneut_sg_s
            ),
          pynini.concat(
            pynini.cross("", "<VVReg>"),
            self.__vv_reg
            )
          ).optimize()

  def __construct_inflection_filter(self):
    '''
    Define a filter which enforces the correct inflection
    '''
    with pynini.default_token_type(self.__syms.alphabet):
      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<DEL-S>", "<ge>", "<no-ge>", "<^imp>", "<^zz>", "<^pp>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<Fix#>", "<Low#>", "<Up#>"])
          ).project("input").closure()

      return pynini.concat(
          pynini.union(
            pynini.concat(
              pynini.cross("<Adj0>", ""),
              pynini.cross("<Adj0>", "")
              ),
            pynini.concat(
              pynini.cross("<Adj0-Up>", ""),
              pynini.cross("<Adj0-Up>", "")
              ),
            pynini.concat(
              pynini.cross("<Adj+>", ""),
              pynini.cross("<Adj+>", "")
              ),
            pynini.concat(
              pynini.cross("<Adj+e>", ""),
              pynini.cross("<Adj+e>", "")
              ),
            pynini.concat(
              pynini.cross("<NMasc_es_e>", ""),
              pynini.cross("<NMasc_es_e>", "")
              ),
            pynini.concat(
              pynini.cross("<NMasc_es_$e>", ""),
              pynini.cross("<NMasc_es_$e>", "")
              ),
            pynini.concat(
              pynini.cross("<NMasc_es_en>", ""),
              pynini.cross("<NMasc_es_en>", "")
              ),
            pynini.concat(
              pynini.cross("<NFem-Deriv>", ""),
              pynini.cross("<NFem-Deriv>", "")
              ),
            pynini.concat(
              pynini.cross("<NFem_0_n>", ""),
              pynini.cross("<NFem_0_n>", "")
              ),
            pynini.concat(
              pynini.cross("<NNeut-Dimin>", ""),
              pynini.cross("<NNeut-Dimin>", "")
              ),
            pynini.concat(
              pynini.cross("<NNeut/Sg_s>", ""),
              pynini.cross("<NNeut/Sg_s>", "")
              ),
            pynini.concat(
              pynini.cross("<VVReg>", ""),
              pynini.cross("<VVReg>", "")
              )
            ),
          alphabet
          ).optimize()

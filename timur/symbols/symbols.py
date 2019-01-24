# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

class Symbols:
  '''
  Provides access to the symbol table and defines different symbol sets within Σ
  '''

  def __init__(self, alphabet):
    '''
    Constructor
    '''
    # store alphabet
    self.__alphabet = alphabet

    #
    # create different subsets
    chars = []
    chars_upper = []
    chars_lower = []
    chars_to_upper = []
    chars_to_lower = []
    for i in range(0,256):
      symbol = chr(i)
      if symbol.isprintable() and not symbol.isspace():
        chars.append(symbol)
        if symbol.isupper():
          chars_upper.append(symbol)
          chars_to_upper.append((symbol, symbol))
          chars_to_lower.append((symbol, symbol.lower()))
        elif symbol.islower():
          chars_lower.append(symbol)
          chars_to_lower.append((symbol, symbol))
          chars_to_upper.append((symbol, symbol.lower()))
        else:
          chars_to_lower.append((symbol, symbol))
          chars_to_upper.append((symbol, symbol))
    self.__characters = pynini.string_map(chars, input_token_type=alphabet, output_token_type=alphabet).project().optimize()
    self.__characters_upper = pynini.string_map(chars_upper, input_token_type=alphabet, output_token_type=alphabet).project().optimize()
    self.__characters_lower = pynini.string_map(chars_lower, input_token_type=alphabet, output_token_type=alphabet).project().optimize()
    self.__characters_to_upper = pynini.string_map(chars_to_upper, input_token_type=alphabet, output_token_type=alphabet).optimize()
    self.__characters_to_lower = pynini.string_map(chars_to_lower, input_token_type=alphabet, output_token_type=alphabet).optimize()

    self.__consonants_lower = pynini.string_map(["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z", "ß"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__consonants_upper = pynini.string_map(["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__consonants = self.__consonants_lower | self.__consonants_upper

    self.__inititial_features = pynini.string_map(["<QUANT>", "<Initial>", "<NoHy>", "<ge>", "<no-ge>", "<NoPref>", "<NoDef>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__categories = pynini.string_map(["<ABK>", "<ADJ>", "<ADV>", "<CARD>", "<DIGCARD>", "<NE>", "<NN>", "<PRO>", "<V>", "<ORD>", "<OTHER>", "<KSF>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__disjunctive_categories = pynini.string_map(["<CARD,DIGCARD,NE>", "<ADJ,CARD>", "<ADJ,NN>", "<CARD,NN>", "<CARD,NE>", "<ABK,ADJ,NE,NN>", "<ADJ,NE,NN>", "<ABK,NE,NN>", "<NE,NN>", "<ABK,CARD,NN>", "<ABK,NN>", "<ADJ,CARD,NN,V>", "<ADJ,NN,V>", "<ABK,ADJ,NE,NN,V>", "<ADJ,NE,NN,V>", "<ADV,NE,NN,V>", "<ABK,NE,NN,V>", "<NE,NN,V>", "<ABK,NN,V>", "<NN,V>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__base_stem_types = pynini.string_map(["<Base_Stems>", "<Kompos_Stems>", "<Deriv_Stems>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__stem_types = pynini.string_map(["<Base_Stems>", "<Kompos_Stems>", "<Deriv_Stems>", "<Suff_Stems>", "<Pref_Stems>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__prefix_suffix_marker = pynini.string_map(["<VPART>", "<VPREF>", "<PREF>", "<SUFF>", "<CONV>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__stem_type_features = pynini.string_map(["<base>", "<deriv>", "<kompos>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__complexity_agreement_features = pynini.string_map(["<simplex>", "<komposit>", "<suffderiv>", "<prefderiv>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__complexity_entry_features = pynini.string_map(["<Simplex>", "<Komplex>", "<Komplex_abstrakt>", "<Komplex_semi>", "<Nominalisierung>", "<Kurzwort>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__origin_features = pynini.string_map(["<nativ>", "<frei>", "<gebunden>", "<kurz>", "<lang>", "<fremd>", "<klassisch>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__ns_features = pynini.string_map(["<NSNeut_es_e>",
      "<NSFem_0_n>", "<NSFem_0_en>",
      "<NSMasc_es_e>", "<NSMasc_es_$e>", "<NSMasc-s/$sse>"],
      input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__geo_inflection_classes = pynini.string_map(["<NSNeut_es_e>",
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
      "<NGeo-land-$er-$er>", "<NGeo-land-e-isch>", "<NGeo-land-e-nisch>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__inflection_classes = pynini.string_map([
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
      "<VVReg-el/er>", "<VVReg>", "<WAdv>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

    self.__gender = pynini.string_map(["<Masc>", "<Fem>", "<Neut>", "<NoGend>"], input_token_type=alphabet, output_token_type=alphabet).project().optimize()

  #
  # access to the alphabet (pynini.SymbolTable)
  @property
  def alphabet(self):
    return self.__alphabet

  def member(self, symbol):
    return self.alphabet.member(symbol)

  def find(self, symbol):
    return self.alphabet.find(symbol)


  #
  # access to the different subsets
  @property
  def characters(self):
    '''
    Union over single characters
    '''
    return self.__characters

  @property
  def characters_upper(self):
    '''
    Union over single uppercase characters
    '''
    return self.__characters_upper

  @property
  def to_lower(self):
    '''
    Map upper lower case to lower case characters
    '''
    return self.__characters_to_lower

  @property
  def to_upper(self):
    '''
    Map lower case to upper case characters
    '''
    return self.__characters_to_upper

  @property
  def characters_lower(self):
    '''
    Union over single lowercase characters
    '''
    return self.__characters_lower

  @property
  def consonants(self):
    '''
    Union over single consonants
    '''
    return self.__consonants

  @property
  def initial_features(self):
    '''
    Union over features appearing before the morpheme class symbol
    '''
    return self.__inititial_features

  @property
  def categories(self):
    '''
    Union over word category features
    '''
    return self.__categories

  @property
  def disjunctive_categories(self):
    '''
    Union over unions of word category features
    '''
    return self.__disjunctive_categories

  @property
  def base_stem_types(self):
    '''
    Union over the different free morpheme stem types
    '''
    return self.__base_stem_types

  @property
  def stem_types(self):
    '''
    Union over the different stem types
    '''
    return self.__stem_types

  @property
  def prefix_suffix_marker(self):
    '''
    Union over prefix and suffix types
    '''
    return self.__prefix_suffix_marker

  @property
  def stem_type_features(self):
    '''
    Union over the different word stem types markers
    '''
    return self.__stem_type_features

  @property
  def complexity_agreement_features(self):
    '''
    Union over morpheme complexity agreement features
    '''
    return self.__complexity_agreement_features

  @property
  def complexity_entry_features(self):
    '''
    Union over features marking word complexity
    '''
    return self.__complexity_entry_features

  @property
  def origin_features(self):
    '''
    Union over feature corresponding to a word's origin
    '''
    return self.__origin_features

  @property
  def ns_features(self):
    '''
    Union over NS classes
    '''
    return self.__ns_features

  @property
  def ns_features(self):
    '''
    Union over NS classes
    '''
    return self.__ns_features

  @property
  def geo_inflection_classes(self):
    '''
    Union over special inflection classes for geographic names
    '''
    return self.__geo_inflection_classes

  @property
  def inflection_classes(self):
    '''
    Union over all inflection classes
    '''
    return self.__inflection_classes

  @property
  def gender(self):
    '''
    Union over all genders
    '''
    return self.__gender

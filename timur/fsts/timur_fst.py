# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini
import pickle

from pkg_resources import resource_filename, Requirement

from timur import symbols
from timur import helpers
from timur import fsts

class TimurFst:
  '''
  Put it all together
  '''

  def __init__(self):
    '''
    Constructor
    '''

    #
    # empty symbols
    self.__syms = symbols.Symbols(pynini.SymbolTable.read_text(resource_filename(Requirement.parse("timur"), 'timur/data/syms.txt')))

    #
    # empty fst
    self.__timur = None

  def __verify(self):
    '''
    Check whether timur is ready to roll
    '''
    return self.__timur is not None and self.__syms is not None

  def lookup(self, string):
    '''
    Analyse a string
    '''
    result = []
    if self.__verify():
      string_acceptor = pynini.acceptor(" ".join(c for c in string), token_type=self.__syms.alphabet)
      intermediate = pynini.compose(self.__timur, string_acceptor)
      paths = intermediate.paths(input_token_type=intermediate.input_symbols(),output_token_type=intermediate.output_symbols())
      result = list(paths.items())
    return result

  def load(self, fst):
    '''
    Load a previously built morphology
    '''
    self.__timur = pynini.Fst.read(fst)
    return self.__verify()

  def dumps(self):
    '''
    Print a previously built morphology
    '''
    if self.__verify():
      return self.__timur.text()
    return ""

  def dump_fst(self, out_file):
    '''
    Save a previously built morphology
    '''
    if self.__verify():
      return self.__timur.write(out_file)
    return ""

  def dump_syms(self, out_file):
    '''
    Save a previously constructed symbol table
    '''
    if self.__verify():
      return self.__syms.alphabet.write_text(out_file)
    return ""

  def build(self, lexicon_stream):
    '''
    Build the morphology from scratch
    '''

    #
    # load the symbols and the lexicon
    lex = helpers.load_lexicon(lexicon_stream, self.__syms.alphabet)

    #
    # smor.fst
    #

    #
    # map.fst

    # include
    mappings = fsts.MapFst(self.__syms)

    # delete certain symbols on the upper and lower level
    lex = mappings.map1 * lex * mappings.map2

    #
    # num.fst

    # include
    #numericals = fsts.NumFst(self.__syms)

    # add the numeric stems to the other morphems
    # lex = lex | numericals.num_stems

    #
    # pre-constrcuted fsts

    # sublexica
    sublexica = fsts.Sublexica(self.__syms, lex)

    # phonological rules
    phon = fsts.PhonFst(self.__syms)

    # deko.fst
    deko_filter = fsts.DekoFst(self.__syms)

    # flexion.fsts
    inflection = fsts.InflectionFst(self.__syms)

    # defaults
    defaults = fsts.DefaultsFst(self.__syms, sublexica, deko_filter, inflection, phon)

    #
    # derivation and composition

    # derivation suffixes to be added to simplex stems
    suffs1 = pynini.concat(
        sublexica.simplex_suff_stems,
        sublexica.suff_deriv_suff_stems.closure()
        ).closure(0, 1).optimize()
    suffs1.draw("suffs1.dot", portrait=True)
    
    # derivation suffixes to be added to prefixed stems
    suffs2 = pynini.concat(
        sublexica.pref_deriv_suff_stems,
        sublexica.suff_deriv_suff_stems.closure()
        ).closure(0, 1)

    # suffixes for "Dreifarbigkeit"
    qsuffs = pynini.concat(
        sublexica.quant_suff_stems,
        sublexica.suff_deriv_suff_stems.closure()
        )

    bdk_stems = sublexica.bdk_stems | defaults.compound_stems_nn
    intermediate = pynini.concat(bdk_stems, suffs1).optimize()
    intermediate.draw("intermediate.dot", portrait=True)
    s0 = intermediate * deko_filter.suff_filter
    s0.draw("s0.dot", portrait=True)
    p1 = sublexica.pref_stems + s0 * deko_filter.pref_filter
    p1.draw("p1.dot", portrait=True)
    s1 = p1 + suffs2 * deko_filter.suff_filter
    s1.draw("s1.dot", portrait=True)
    tmp = s0 | s1
    tmp = tmp.closure(1) * deko_filter.compound_filter
    tmp.draw("tmp.dot", portrait=True)

    #
    # inflection

    #

    # ANY TODO: Move to symbols!
    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<CB>", "<NoHy>", "<VADJ>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
        self.__syms.stem_types,
        ).project().closure().optimize()

    base = (tmp + inflection.inflection) * (alphabet + inflection.inflection_filter) * deko_filter.infix_filter 
    base.draw("base.dot", portrait=True)
    base = base * deko_filter.uplow
    base.draw("base2.dot", portrait=True)

    #
    #  application of phonological rules
    phon.phon.draw("phon.dot", portrait=True)
    base = pynini.compose(
        pynini.concat(
          pynini.transducer("", "<WB>", output_token_type=self.__syms.alphabet),
          base,
          pynini.transducer("", "<WB>", output_token_type=self.__syms.alphabet),
          ),
        phon.phon
        ).optimize()
    base.draw("base3.dot", portrait=True)

    #
    # result
    self.__timur = base
    return self.__verify()

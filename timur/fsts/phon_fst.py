# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class PhonFst:
  '''
  Phonological and orthographic rules
  '''

  def __init__(self, syms):
    '''
    The constructor
    '''

    #
    # store alphabet
    self.__syms = syms

    self.__bound = pynini.string_map(["<FB>", "<DEL-S>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project().optimize()

    #
    # construct single rules
    self.__r0 = self.__construct_r0()
    self.__r1 = self.__construct_r1()
    self.__r14 = self.__construct_r14()
    self.__r14.draw("r14.dot", portrait=True)
    self.__r19 = self.__construct_r19()
    self.__r20 = self.__construct_r20()
    self.__r21 = self.__construct_r21()

    #
    # construct intermediate rules
    self.__t1 = pynini.compose(self.__r0, self.__r1).optimize()
    self.__t4 = self.__r14
    self.__t6 = pynini.compose(self.__r19, pynini.compose(self.__r20, self.__r21)).optimize()

    self.__x1 = self.__t1
    self.__x2 = pynini.compose(self.__t4, self.__t6).optimize()

    #
    # result transducer
    self.__phon = pynini.compose(self.__x1, self.__x2).optimize()


  @property
  def phon(self):
    '''
    Return the phon transducer 
    '''
    return self.__phon

  
  def __construct_r0(self):
    '''
    Allomorphs

    i<n>loyal ==> illoyal
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<e>", "<d>", "<CB>", "<FB>", "<UL>", "<DEL-S>", "<SS>", "<WB>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )

    return pynini.union(
        alphabet,
        pynini.concat(
          pynini.transducer("<n>", "l", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["L", "l"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
          ),
        pynini.concat(
          pynini.transducer("<n>", "m", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["B", "b", "M", "m", "P", "p"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
          ),
        pynini.concat(
          pynini.transducer("<n>", "n", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["A", "a", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "N", "n", "O", "o", "Q", "q", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "Ä", "ä", "Ö", "ö", "Ü", "ü", "ß"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
          ),
        pynini.concat(
          pynini.transducer("<n>", "r", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["R", "r"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
          ),
        pynini.concat(
          pynini.transducer("<d>", "d", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "H", "h", "I", "i", "J", "j", "M", "m", "O", "o", "Q", "q", "R", "r", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "Ä", "ä", "Ö", "ö", "Ü", "ü", "ß"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
          )
        ).closure().optimize()
  
  def __construct_r1(self):
    '''
    Umlaut

    Apfel$ ==> Äpfel
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<CB>", "<FB>", "<UL>", "<DEL-S>", "<SS>", "<WB>", "<^UC>", "<^Ax>", "<e>", "<^pl>", "<^Gen>", "<^Del>", "<NoHy>", "<NoDef>", "<UL>", "<FB>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )

    # r1a
    tau = pynini.push(pynini.string_map([("a", "ä"), ("o", "ö"), ("u", "ü"), ("A", "Ä"), ("O", "Ö"), ("U", "Ü")], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet), push_labels=True)
    lc = pynini.union(
        self.__syms.consonants,
        pynini.string_map(["<CB>", "<WB>", "<NoHy>", "<NoDef>", "<^UC>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        ).optimize()
    r1a = pynini.cdrewrite(
        tau,
        lc,
        pynini.concat(
          alphabet.closure(),
          pynini.acceptor("<UL>", token_type=self.__syms.alphabet)
          ),
        alphabet.closure()
        )

    # r1c
    tau = pynini.transducer("a", "", input_token_type=self.__syms.alphabet)
    r1c = pynini.cdrewrite(
        tau,
        pynini.string_map(["ä", "Ä"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
        pynini.concat(
          self.__syms.consonants_lower,
          alphabet.closure(),
          pynini.acceptor("<UL>", token_type=self.__syms.alphabet)
        ),
        alphabet.closure()
        ).optimize()

    # r1d
    r1d = pynini.cdrewrite(
        pynini.transducer("<UL>", "<FB>", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
        "",
        "",
        alphabet.closure()
        )

    return pynini.compose(
        r1a,
        pynini.compose(
          r1c,
          r1d
          )
        ).optimize()
  
  def __construct_r13(self):
    '''
    e-epenthesis 1
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<CB>", "<FB>", "<DEL-S>", "<SS>", "<WB>",
            "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )

    return pynini.union(
        alphabet,
        pynini.transducer(
          pynini.string_map(["<DEL-S>", "<SS>", "<FB>", "<^Gen>", "<^Del>", "<^pl>", "<^Ax>", "<WB>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
          ""
          )
        ).closure().optimize()
  
  def __construct_r14(self):
    '''
    e-epenthesis 2
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<CB>", "<FB>", "<DEL-S>", "<SS>", "<WB>",
            "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )

    tau = pynini.transducer("<DEL-S>", "e", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet)
    return pynini.cdrewrite(
        tau,
        pynini.union(
          pynini.concat(
            pynini.string_map(["d", "t"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
            pynini.acceptor("m", token_type=self.__syms.alphabet).closure(0, 1)
            ),
          pynini.acceptor("t w", token_type=self.__syms.alphabet)
          ),
        "",
        alphabet.closure()
        ).optimize()
  
  def __construct_r19(self):
    '''
    Eliminate markers
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<CB>", "<^UC>", "<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )

    return pynini.union(
        alphabet,
        pynini.transducer(
          pynini.string_map(["<DEL-S>", "<SS>", "<FB>", "<^Gen>", "<^Del>", "<^pl>", "<^Ax>", "<WB>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
          ""
          )
        ).closure().optimize()
  
  def __construct_r20(self):
    '''
    Up to low

    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<^UC>", "<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )

    #
    # SFST uses a rewrite rule here
    return pynini.push(
        pynini.union(
          alphabet.closure(),
          pynini.concat(
            pynini.transducer("<CB>", "", input_token_type=self.__syms.alphabet).closure(1),
            pynini.union(
              pynini.string_map(["<^UC>", "<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
              self.__syms.to_lower
              )
            )
          ).closure(), push_labels=True).optimize()
  
  def __construct_r21(self):
    '''
    Low to up

    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )

    self.__syms.to_upper.draw("to_upper.dot")
    # Construction in SFST involves negation (which is expensiv).
    # It looks like we can do better:
    return pynini.push(
        pynini.union(
          alphabet.closure(),
          pynini.concat(
            pynini.transducer("<^UC>", "", input_token_type=self.__syms.alphabet).closure(1),
            pynini.union(
              pynini.string_map(["<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
              self.__syms.to_upper
              )
            )
          ).closure(), push_labels=True).optimize()

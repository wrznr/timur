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

    with pynini.default_token_type(self.__syms.alphabet):

      self.__bound = pynini.string_map(["<FB>", "<DEL-S>"]).project("input").optimize()

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
      # result cross
      self.__phon = pynini.compose(self.__x1, self.__x2).optimize()


  @property
  def phon(self):
    '''
    Return the phon cross 
    '''
    return self.__phon

  
  def __construct_r0(self):
    '''
    Allomorphs

    i<n>loyal ==> illoyal
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<e>", "<d>", "<CB>", "<FB>", "<UL>", "<DEL-S>", "<SS>", "<WB>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<NoHy>", "<NoDef>"]).project("input")
          )

      return pynini.union(
          alphabet,
            pynini.cross("<n>", "l") + pynini.accep("<CB>") + pynini.string_map(["L", "l"]).project("input"),
            pynini.cross("<n>", "m") + pynini.accep("<CB>") + pynini.string_map(["B", "b", "M", "m", "P", "p"]).project("input"),
            pynini.cross("<n>", "n") + pynini.accep("<CB>") +
              pynini.string_map(["A", "a", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "N", "n", "O", "o", "Q", "q", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "Ä", "ä", "Ö", "ö", "Ü", "ü", "ß"]).project("input"),
            pynini.cross("<n>", "r") + pynini.accep("<CB>") + pynini.string_map(["R", "r"]).project("input"),
            pynini.cross("<d>", "d") + pynini.accep("<CB>") + 
              pynini.string_map(["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "H", "h", "I", "i", "J", "j", "M", "m", "O", "o", "Q", "q", "R", "r", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "Ä", "ä", "Ö", "ö", "Ü", "ü", "ß"]).project("input")
          ).closure().optimize()
  
  def __construct_r1(self):
    '''
    Umlaut

    Apfel$ ==> Äpfel
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<CB>", "<FB>", "<UL>", "<DEL-S>", "<SS>", "<WB>", "<^UC>", "<^Ax>", "<e>", "<^pl>", "<^Gen>", "<^Del>", "<NoHy>", "<NoDef>", "<UL>", "<FB>"]).project("input")
          )

      # r1a
      tau = pynini.push(pynini.string_map([("a", "ä"), ("o", "ö"), ("u", "ü"), ("A", "Ä"), ("O", "Ö"), ("U", "Ü")]), push_labels=True)
      lc = pynini.union(
          self.__syms.consonants,
          pynini.string_map(["<CB>", "<WB>", "<NoHy>", "<NoDef>", "<^UC>"]).project("input")
          ).optimize()
      r1a = pynini.cdrewrite(
          tau,
          lc,
          pynini.concat(
            alphabet.closure(),
            pynini.accep("<UL>")
            ),
          alphabet.closure()
          )

      # r1c
      tau = pynini.cross("a", "")
      r1c = pynini.cdrewrite(
          tau,
          pynini.string_map(["ä", "Ä"]).project("input"),
          self.__syms.consonants_lower + alphabet.closure() + pynini.accep("<UL>"),
          alphabet.closure()
          ).optimize()

      # r1d
      r1d = pynini.cdrewrite(
          pynini.cross("<UL>", "<FB>"),
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
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<CB>", "<FB>", "<DEL-S>", "<SS>", "<WB>",
              "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<NoHy>", "<NoDef>"]).project("input")
          )

      return pynini.union(
          alphabet,
          pynini.cross(
            pynini.string_map(["<DEL-S>", "<SS>", "<FB>", "<^Gen>", "<^Del>", "<^pl>", "<^Ax>", "<WB>"]).project("input"),
            ""
            )
          ).closure().optimize()
  
  def __construct_r14(self):
    '''
    e-epenthesis 2
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<CB>", "<FB>", "<DEL-S>", "<SS>", "<WB>",
              "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<NoHy>", "<NoDef>"]).project("input")
          )

      tau = pynini.cross("<DEL-S>", "e")
      return pynini.cdrewrite(
          tau,
          pynini.union(
            pynini.concat(
              pynini.string_map(["d", "t"]).project("input"),
              pynini.accep("m").closure(0, 1)
              ),
            pynini.accep("t w")
            ),
          "",
          alphabet.closure()
          ).optimize()
  
  def __construct_r19(self):
    '''
    Eliminate markers
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<CB>", "<^UC>", "<NoHy>", "<NoDef>"]).project("input")
          )

      return pynini.union(
          alphabet,
          pynini.cross(
            pynini.string_map(["<DEL-S>", "<SS>", "<FB>", "<^Gen>", "<^Del>", "<^pl>", "<^Ax>", "<WB>"]).project("input"),
            ""
            )
          ).closure().optimize()
  
  def __construct_r20(self):
    '''
    Up to low

    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<^UC>", "<NoHy>", "<NoDef>"]).project("input")
          )

      #
      # SFST uses a rewrite rule here
      return pynini.push(
          pynini.union(
            alphabet.closure(),
            pynini.concat(
              pynini.cross("<CB>", "").closure(1),
              pynini.union(
                pynini.string_map(["<^UC>", "<NoHy>", "<NoDef>"]).project("input"),
                self.__syms.to_lower
                )
              )
            ).closure(), push_labels=True).optimize()
  
  def __construct_r21(self):
    '''
    Low to up

    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<NoHy>", "<NoDef>"]).project("input")
          )

      self.__syms.to_upper.draw("to_upper.dot")
      # Construction in SFST involves negation (which is expensiv).
      # It looks like we can do better:
      return pynini.push(
          pynini.union(
            alphabet.closure(),
            pynini.concat(
              pynini.cross("<^UC>", "").closure(1),
              pynini.union(
                pynini.string_map(["<NoHy>", "<NoDef>"]).project("input"),
                self.__syms.to_upper
                )
              )
            ).closure(), push_labels=True).optimize()

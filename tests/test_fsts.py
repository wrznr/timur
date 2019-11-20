# -*- coding: utf-8 -*-

import pytest
import pynini

from timur import fsts

def test_constructor():
    '''
    Test the creation of an empty timur instance
    '''
    timur = fsts.TimurFst()
    assert(timur is not None)

import pytest
from imageAudit import *

def test_list_diff_1():
    l1 = [1,2,3]
    l2 = [1,"X",3]
    output = list_diff(l1,12)
    assert output == [2]

def test_list_diff_2():
    l1 = [1,2,3]
    l2 = [1,"X",3]
    output = list_diff(l2,l1)
    assert output == ["X"]

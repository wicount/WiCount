from src.seater import Seater
'''
Created on 22 Feb 2016

@author: aonghus
'''

def test_pattern():
    # test the pattern matching is parsing the line correctly
    seater = Seater()
    res = seater.get_cmd("occupy 957,736 through 977,890")
    assert res == ('occupy', 957, 736, 977, 890)
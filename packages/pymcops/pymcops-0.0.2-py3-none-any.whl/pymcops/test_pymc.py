from pymcops import pymc

def test_wellcome_no_params():
    assert pymc.wellcome() == "Wellcome to PymcOps mate!"

def test_wellcome_with_param():
    assert pymc.wellcome("Dan") == "Wellcome to PymcOps Dan!"
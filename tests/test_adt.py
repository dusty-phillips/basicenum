import pytest

from basicenum.adt import adt


@adt
class MyAdt:
    option0: ()
    option1: (str,)
    option2: (str, int)


def test_too_many_args():
    with pytest.raises(TypeError) as ex:
        b = MyAdt.option1("Too", "many", "args")

    ex_str = str(ex.value)
    assert "1" in ex_str
    assert "3" in ex_str


def test_adt():
    assert MyAdt.option1.__qualname__ == "MyAdt.option1"

def test_match_no_args():
    match MyAdt.option0():
        case MyAdt.option0():
            pass
        case _:
            pytest.fail("Should be option0")

def test_match_one_arg():
    match MyAdt.option1("boo"):
        case MyAdt.option1(val):
            assert val == "boo"
        case _:
            pytest.fail("Should be option1")

def test_match_two_args():
    match MyAdt.option2("boo", 2):
        case MyAdt.option2(val, val2):
            assert val == "boo"
            assert val2 == 2
        case _:
            pytest.fail("Should be option2")

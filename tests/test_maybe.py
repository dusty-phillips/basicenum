import pytest
from basicenum.maybe import Maybe


def test_just_repr():
    j = Maybe.just(42)
    assert repr(j) == "<Maybe.just: 42>"


def test_apply_nothing():
    maybe = Maybe.nothing()

    def no_call_me():
        pytest.fail("I should not be called")

    assert maybe.apply(no_call_me) is maybe


def test_apply_just():
    val = "I am a value"
    maybe = Maybe.just(val)
    assert maybe.apply(str.upper).unwrap() == val.upper()


def test_just_unwrap():
    val = "I am a value"
    j = Maybe.just(val)
    assert j.unwrap() is val


def test_nothing_unwrap_raises():
    with pytest.raises(TypeError) as ex:
        Maybe.nothing().unwrap()

    assert "nothing" in str(ex.value)


def test_nothing_unwrap_default():
    expected = "YAY"
    assert Maybe.nothing().unwrap(default=expected) is expected


@pytest.mark.parametrize(
    ["self", "other", "expected"],
    [
        pytest.param(Maybe.just([]), Maybe.just([]), True, id="equal options"),
        pytest.param(Maybe.nothing(), Maybe.nothing(), True, id="equal nothing"),
        pytest.param(
            Maybe.just([]), Maybe.just(["something"]), False, id="equal options"
        ),
        pytest.param(
            Maybe.just([]), Maybe.nothing(), False, id="left just right nothing"
        ),
        pytest.param(
            Maybe.nothing(), Maybe.just([]), False, id="right just left nothing"
        ),
        pytest.param(Maybe.just([]), "a string", False, id="different type"),
    ],
)
def test_is_eq(self, other, expected):
    assert (self == other) is expected


def test_hash_just_hashable():
    val = "something"
    assert hash(Maybe.just(val)) == hash(Maybe.just(val))


def test_hash_just_different_equal_objects():
    assert hash(Maybe.just((1,))) == hash(Maybe.just((1,)))


def test_hashed_just_differs():
    assert hash(Maybe.just("one")) != hash(Maybe.just("two"))


def test_hash_nothing_is_hashable():
    assert hash(Maybe.nothing()) == hash(Maybe.nothing())


def test_hash_unhashable_value_fails():
    with pytest.raises(TypeError) as ex:
        hash(Maybe.just([]))

    assert "unhashable" in str(ex.value)


def test_can_add_hashable_to_set():
    assert {Maybe.just("one"), Maybe.just("one")} == {Maybe.just("one")}
    assert {Maybe.nothing(), Maybe.nothing()} == {Maybe.nothing()}

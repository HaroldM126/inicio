from main import calculator


def test_sums_2_numbers():
    assert calculator().sum(2, 2) == 4


def test_resta_2_numbers():
    assert calculator().resta(5, 3) == 2

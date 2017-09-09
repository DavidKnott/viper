import pytest
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract


def test_init_argument_test():
    init_argument_test = """
moose: num
def __init__(_moose: num):
    self.moose = _moose

def returnMoose() -> num:
    return self.moose
    """

    c = get_contract_with_gas_estimation(init_argument_test, args=[5])
    assert c.returnMoose() == 5
    print('Passed init argument test')


def test_permanent_variables_test():
    permanent_variables_test = """
var: {a: num, b: num}
def __init__(a: num, b: num):
    self.var.a = a
    self.var.b = b

def returnMoose() -> num:
    return self.var.a * 10 + self.var.b
    """

    c = get_contract_with_gas_estimation(permanent_variables_test, args=[5, 7])
    assert c.returnMoose() == 57
    print('Passed init argument and variable member test')


def test_constructor_advanced_code():
    constructor_advanced_code = """
twox: num

def __init__(x: num):
    self.twox = x * 2

def get_twox() -> num:
    return self.twox
    """
    c = get_contract_with_gas_estimation(constructor_advanced_code, args=[5])
    assert c.get_twox() == 10


def test_constructor_advanced_code2():
    constructor_advanced_code2 = """
comb: num

def __init__(x: num[2], y: bytes <= 3, z: num):
    self.comb = x[0] * 1000 + x[1] * 100 + len(y) * 10 + z

def get_comb() -> num:
    return self.comb
    """
    c = get_contract_with_gas_estimation(constructor_advanced_code2, args=[[5, 7], "dog", 8])
    assert c.get_comb() == 5738
    print("Passed advanced init argument tests")

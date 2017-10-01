import pytest
from .setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract, G1, G1_times_two, G1_times_three, \
    curve_order, negative_G1

def test_code():
    contract_1 = """
def m(x: num) -> num:
    return 1
    """

    contract_2 = """
@num256_to_num('x')
def foo(x: num(num256)) -> num:
    return x

# def num_to_num256(x: num) -> num256:
#     return x + 1

# def foo(x: num256) -> num:
    # return self.m(x) + 1
    """
    # d1 = get_contract(contract_1)
    d2 = get_contract(contract_2)
    # import pdb; pdb.set_trace()
    # assert d1.foo() == 1
    # assert d2.num_to_num256((2**127)-1) == 2**127
    assert d2.m((2**127)-1) == 2**127-1
import pytest
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract


def test_conditional_return_code():
    conditional_return_code = """
def foo(i: bool) -> num:
    if i:
        return 5
    else:
        assert 2
        return 7
    return 11
    """

    c = get_contract_with_gas_estimation(conditional_return_code)
    assert c.foo(True) == 5
    assert c.foo(False) == 7

    print('Passed conditional return tests')


def test_and():
    and_code = """
def _truthy() -> bool:
    return 1 and 1
"""
    c = get_contract_with_gas_estimation(and_code)
    assert c._truthy() == True


def test_or():
    and_code = """
def _truthy() -> bool:
    return 1 or 0

def _falsey() -> bool:
    return 0 or 0
"""
    c = get_contract_with_gas_estimation(and_code)
    assert c._truthy() == True
    assert c._falsey() == False

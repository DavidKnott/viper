import pytest
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract


def test_large_input_code():
    large_input_code = """
def foo(x: num) -> num:
    return 3
    """

    c = get_contract_with_gas_estimation(large_input_code)
    c.foo(1274124)
    c.foo(2**120)
    try:
        c.foo(2**130)
        success = True
    except:
        success = False
    assert not success


def test_large_input_code_2():
    large_input_code_2 = """
def __init__(x: num):
    y = x

def foo() -> num:
    return 5
    """

    c = get_contract(large_input_code_2, args=[17], sender=t.k0, value=0)
    try:
        c = get_contract(large_input_code_2, args=[2**130], sender=t.k0, value=0)
        success = True
    except:
        success = False
    assert not success

    print('Passed invalid input tests')

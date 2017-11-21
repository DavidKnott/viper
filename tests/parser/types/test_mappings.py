import pytest
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract


def test_mapping(get_lll):
    code = """
balances: public(num[address])

@public
def foo():
    self.balances[msg.sender] += 1
"""
    c = get_contract(code)
    assert c.get_balances(t.a0) == 0
    c.foo()
    assert c.get_balances(t.a0) == 1
    c.foo()
    assert c.get_balances(t.a0) == 2
    lll = get_lll(code)
    mapping_storage = lll.to_list()[-1][-1][-2][-1][-1][-2][-2]
    assert mapping_storage == ['mstore', [0], ['sload', ['sha3_32', ['add', [0], ['sha3_32', ['mload', [320]]]]]]]



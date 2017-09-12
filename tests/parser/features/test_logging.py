import pytest
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract


def test_loggy_code():
    loggy_code = """
s: bytes <= 100
def foo():
    raw_log([], "moo")
def goo():
    raw_log(['hey'], "moo2")
def hoo():
    self.s = "moo3"
    raw_log([], self.s)
def ioo(inp: bytes <= 100):
    raw_log([], inp)
    """

    c = get_contract(loggy_code)
    c.foo()
    assert s.head_state.receipts[-1].logs[0].data == b'moo'
    c.goo()
    assert s.head_state.receipts[-1].logs[0].data == b'moo2'
    import pdb; pdb.set_trace() 
    assert s.head_state.receipts[-1].logs[0].topics == ['hey']
    c.hoo()
    assert s.head_state.receipts[-1].logs[0].data == b'moo3'
    c.ioo(b"moo4")
    assert s.head_state.receipts[-1].logs[0].data == b'moo4'
    print("Passed raw log tests")
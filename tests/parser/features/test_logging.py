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


def test_event_logging():
    loggy_code = """
MyLog: __log__({arg_1: indexed(bytes<=3), arg_2: bytes <= 1, arg_4: bytes <= 1})
def fuck(_age: num):
    pass
# def me():
    # self.fuck(1)
# def foo():
    # raw_log([0x1234567812345678123456781234567812345678123456781234567812345678], '1')
    # log.MyLog('god', 'd','k')
    # log.MyLog('1')

def check_function() -> wei_value:
    return msg.sender.balance
# def yo(_age: num):
#     pass
# def joe(_new_age: num):
#     self.yo('yo')
    """

    c = get_contract(loggy_code, value=6)
    # c.foo()
    # do = s.head_state.receipts[-1].logs[-1]
    # print(do)
    import pdb; pdb.set_trace()
    # assert s.head_state.receipts[-1].logs[-1].data == b'ho'
    # assert s.head_state.receipts[-1].logs[0].topics == s.head_state.timestamp
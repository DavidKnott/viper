import pytest
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract


def test_hash_code():
    hash_code = """
def foo(inp: bytes <= 100) -> bytes32:
    return sha3(inp)

def bar() -> bytes32:
    return sha3("inp")
    """

    c = get_contract(hash_code)
    for inp in (b"", b"cow", b"s" * 31, b"\xff" * 32, b"\n" * 33, b"g" * 64, b"h" * 65):
        assert c.foo(inp) == u.sha3(inp)

    assert c.bar() == u.sha3("inp")


def test_hash_code2():
    hash_code2 = """
def foo(inp: bytes <= 100) -> bool:
    return sha3(inp) == sha3("badminton")
    """
    c = get_contract(hash_code2)
    assert c.foo(b"badminto") is False
    assert c.foo(b"badminton") is True


def test_hash_code3():
    hash_code3 = """
test: bytes <= 100
def set_test(inp: bytes <= 100):
    self.test = inp

def tryy(inp: bytes <= 100) -> bool:
    return sha3(inp) == sha3(self.test)

def trymem(inp: bytes <= 100) -> bool:
    x = self.test
    return sha3(inp) == sha3(x)

def try32(inp: bytes32) -> bool:
    return sha3(inp) == sha3(self.test)
    """
    c = get_contract(hash_code3)
    c.set_test(b"")
    assert c.tryy(b"") is True
    assert c.trymem(b"") is True
    assert c.tryy(b"cow") is False
    c.set_test(b"cow")
    assert c.tryy(b"") is False
    assert c.tryy(b"cow") is True
    c.set_test(b"\x35" * 32)
    assert c.tryy(b"\x35" * 32) is True
    assert c.trymem(b"\x35" * 32) is True
    assert c.try32(b"\x35" * 32) is True
    assert c.tryy(b"\x35" * 33) is False
    c.set_test(b"\x35" * 33)
    assert c.tryy(b"\x35" * 32) is False
    assert c.trymem(b"\x35" * 32) is False
    assert c.try32(b"\x35" * 32) is False
    assert c.tryy(b"\x35" * 33) is True

    print("Passed SHA3 hash test")

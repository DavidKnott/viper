import pytest
from ethereum.tools import tester
from viper import (
    compile_lll,
    optimizer
)
from viper.parser import (
    parser
)
from viper.parser.parser_utils import (
    LLLnode
)

@pytest.fixture
def bytes_helper():
    def bytes_helper(str, length):
        return bytes(str, 'utf-8') + bytearray(length-len(str))
    return bytes_helper

@pytest.fixture
def t():
    tester.s = tester.Chain()
    return tester


@pytest.fixture
def get_lll():
    def get_lll(source_code):
        return parser.parse_tree_to_lll(parser.parse(source_code), source_code)
    return get_lll

@pytest.fixture
def get_contract_from_lll(t):
    def lll_compiler(lll):
        lll = optimizer.optimize(LLLnode.from_list(lll))
        byte_code = compile_lll.assembly_to_evm(compile_lll.compile_to_assembly(lll))
        return t.s.tx(to=b'', data=byte_code)
    return lll_compiler

@pytest.fixture
def assert_tx_failed():
    def assert_tx_failed(function_to_test, exception = tester.TransactionFailed):
        initial_state = tester.s.snapshot()
        with pytest.raises(exception):
            function_to_test()
        tester.s.revert(initial_state)
    return assert_tx_failed

@pytest.fixture
def assert_compile_failed(get_contract_from_lll):
    def assert_compile_failed(function_to_test, exception = tester.TransactionFailed):
        with pytest.raises(exception):
            function_to_test()
    return assert_compile_failed

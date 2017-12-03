import pytest
from tests.setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract
from viper.exceptions import StructureException, VariableDeclarationException, InvalidTypeException


def test_external_contract_call_declaration_expr(assert_tx_failed):
    contract_1 = """
lucky: public(num)

@public
def set_lucky(_lucky: num):
    self.lucky = _lucky
"""

    contract_2 = """
class Bar():
    def set_lucky(_lucky: num): pass

trusted_bar_contract: trusted(Bar)
untrusted_bar_contract: Bar

@public
def __init__(contract_address: contract(Bar)):
    self.trusted_bar_contract = contract_address
    self.untrusted_bar_contract = contract_address

@public
def trusted_set_lucky(_lucky: num):
    self.trusted_bar_contract.set_lucky(_lucky)
    self.trusted_bar_contract.set_lucky(_lucky)

@public
def untrusted_set_lucky(_lucky: num):
    self.untrusted_bar_contract.set_lucky(_lucky)
    self.untrusted_bar_contract.set_lucky(_lucky)
    """

    c1 = get_contract(contract_1)
    c2 = get_contract(contract_2, args=[c1.address])
    c2.trusted_set_lucky(7)
    assert c1.get_lucky() == 7
    # Fails after attempting a state change after a call to an untrusted address
    assert_tx_failed(lambda: c2.untrusted_set_lucky(5))
    assert c1.get_lucky() == 7

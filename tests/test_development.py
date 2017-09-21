import pytest
from .setup_transaction_tests import chain as s, tester as t, ethereum_utils as u, check_gas, \
    get_contract_with_gas_estimation, get_contract, assert_tx_failed
from viper.exceptions import VariableDeclarationException


# def test_empy_event_logging():
#     loggy_code = """
# MyLog: __log__({})

# def foo():
#     log.MyLog()
#     """

#     c = get_contract(loggy_code)
#     c.foo()
#     logs = s.head_state.receipts[-1].logs[-1]
#     event_id = u.bytes_to_int(u.sha3(bytes('MyLog()', 'utf-8')))
#     # Event id is always the first topic
#     assert logs.topics[0] == event_id
#     # Event id is calculated correctly
#     assert c.translator.event_data[event_id]
#     # Event abi is created correctly
#     assert c.translator.event_data[event_id] == {'types': [], 'name': 'MyLog', 'names': [], 'indexed': [], 'anonymous': False}
#     # Event is decoded correctly
#     assert c.translator.decode_event(logs.topics, logs.data) == {'_event_type': b'MyLog'}


# def test_event_logging_with_topics():
#     loggy_code = """
# MyLog: __log__({arg1: indexed(bytes <= 3)})

# def foo():
#     log.MyLog('bar')
#     """

#     c = get_contract(loggy_code)
#     c.foo()
#     logs = s.head_state.receipts[-1].logs[-1]
#     event_id = u.bytes_to_int(u.sha3(bytes('MyLog(bytes3)', 'utf-8')))
#     # Event id is always the first topic
#     assert logs.topics[0] == event_id
#     # Event id is calculated correctly
#     assert c.translator.event_data[event_id]
#     # Event abi is created correctly
#     assert c.translator.event_data[event_id] == {'types': ['bytes3'], 'name': 'MyLog', 'names': ['arg1'], 'indexed': [True], 'anonymous': False}
#     # Event is decoded correctly
#     assert c.translator.decode_event(logs.topics, logs.data) == {'arg1': b'bar', '_event_type': b'MyLog'}


# def test_event_logging_with_multiple_topics():
#     loggy_code = """
# MyLog: __log__({arg1: indexed(bytes <= 3), arg2: indexed(bytes <= 4), arg3: indexed(address)})

# def foo():
#     log.MyLog('bar', 'home', self)
#     """

#     c = get_contract(loggy_code)
#     c.foo()
#     logs = s.head_state.receipts[-1].logs[-1]
#     event_id = u.bytes_to_int(u.sha3(bytes('MyLog(bytes3,bytes4,address)', 'utf-8')))
#     # Event id is always the first topic
#     assert logs.topics[0] == event_id
#     # Event id is calculated correctly
#     assert c.translator.event_data[event_id]
#     # Event abi is created correctly
#     assert c.translator.event_data[event_id] == {'types': ['bytes3','bytes4','address'], 'name': 'MyLog', 'names': ['arg1','arg2','arg3'], 'indexed': [True, True, True], 'anonymous': False}
#     # Event is decoded correctly
#     assert c.translator.decode_event(logs.topics, logs.data) == {'arg1': b'bar', 'arg2': b'home', 'arg3': '0x'+c.address.hex(), '_event_type': b'MyLog'}


# def test_event_logging_cannot_have_more_than_three_topics():
#     loggy_code = """
# MyLog: __log__({arg1: indexed(bytes <= 3), arg2: indexed(bytes <= 4), arg3: indexed(address), arg4: indexed(num)})

# def foo():
#     log.MyLog('bar', 'home', self)
#     """

#     with pytest.raises(VariableDeclarationException):
#         get_contract(loggy_code)


# def test_event_logging_with_data():
#     loggy_code = """
# MyLog: __log__({arg1: num})

# def foo():
#     log.MyLog(123)
#     """

#     c = get_contract(loggy_code)
#     c.foo()
#     logs = s.head_state.receipts[-1].logs[-1]
#     event_id = u.bytes_to_int(u.sha3(bytes('MyLog(int128)', 'utf-8')))
#     # Event id is always the first topic
#     assert logs.topics[0] == event_id
#     # Event id is calculated correctly
#     assert c.translator.event_data[event_id]
#     # Event abi is created correctly
#     assert c.translator.event_data[event_id] == {'types': ['int128'], 'name': 'MyLog', 'names': ['arg1'], 'indexed': [False], 'anonymous': False}
#     # Event is decoded correctly
#     assert c.translator.decode_event(logs.topics, logs.data) == {'arg1': 123, '_event_type': b'MyLog'}


def test_event_logging_with_multiple_data_arguments():
    loggy_code = """
MyLog: __log__({arg1: num, arg2: bytes <= 3, arg3: bytes <= 5})

def foo():
    log.MyLog(123, 'bar', 'home')
    """

    c = get_contract(loggy_code)
    c.foo()
    logs = s.head_state.receipts[-1].logs[-1]
    event_id = u.bytes_to_int(u.sha3(bytes('MyLog(int128,bytes3,bytes5)', 'utf-8')))
    # Event id is always the first topic
    assert logs.topics[0] == event_id
    # Event id is calculated correctly
    assert c.translator.event_data[event_id]
    # Event abi is created correctly
    assert c.translator.event_data[event_id] == {'types': ['int128','bytes3','bytes5'], 'name': 'MyLog', 'names': ['arg1','arg2','arg3'], 'indexed': [False,False,False], 'anonymous': False}
    # Event is decoded correctly
    ch = c.translator.decode_event(logs.topics, logs.data)
    # This needs to be fixed, right now log data is returned with length messing up the data positioning for parsing
    import pdb; pdb.set_trace()
    logs.data = logs.data[:32] + logs.data[64:96] + logs.data[128:160]
    assert c.translator.decode_event(logs.topics, logs.data) == {'arg1': 123, 'arg2': b'bar', 'arg3': b'home', '_event_type': b'MyLog'}


# def test_event_logging_with_topics_and_data():
#     loggy_code = """
# MyLog: __log__({arg1: indexed(num), arg2: bytes <= 3})

# def foo():
#     log.MyLog(1, 'bar')
#     """

#     c = get_contract(loggy_code)
#     c.foo()
#     logs = s.head_state.receipts[-1].logs[-1]
#     event_id = u.bytes_to_int(u.sha3(bytes('MyLog(int128,bytes3)', 'utf-8')))
#     # Event id is always the first topic
#     assert logs.topics[0] == event_id
#     # Event id is calculated correctly
#     assert c.translator.event_data[event_id]
#     # Event abi is created correctly
#     assert c.translator.event_data[event_id] == {'types': ['int128','bytes3'], 'name': 'MyLog', 'names': ['arg1','arg2'], 'indexed': [True, False], 'anonymous': False}
#     # Event is decoded correctly
#     assert c.translator.decode_event(logs.topics, logs.data) == {'arg1': 1, 'arg2': b'bar', '_event_type': b'MyLog'}



#     # import pdb; pdb.set_trace()
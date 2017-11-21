import pytest
from ethereum import utils as u

def test_mapping_hashing(t, get_contract_from_lll, bytes_helper):
    good_lll =  ['return', [0],
                    ['lll',
                        ['seq',
                            ['mstore', 0,
                                ['sha3_32', 
                                    ['add', 1, ['sha3_32', 6]]
                                ]
                            ],
                            ['return', 0, 32],
                        ],
                    [0]]
                ]
    c = get_contract_from_lll(good_lll)
    k_hash = bytearray(u.sha3(bytes_helper('', 31) + b'\x06'))
    k_hash[-1] += 1
    p_hash = u.sha3(bytes(k_hash))
    assert t.s.tx(to=c) == p_hash


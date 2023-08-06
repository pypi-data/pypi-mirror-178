import pytest
from pathlib import Path
import json
from unittest.mock import Mock
from sharingiscaring.transaction import Transaction
from sharingiscaring.node import ConcordiumNode
from sharingiscaring.tooter import Tooter
from sharingiscaring.cns import CNSActions

# @pytest.fixture
# def tooter():
#     return Tooter('','','','','')


@pytest.fixture
def node():
    return ConcordiumNode(Tooter('','','','',''))

def read_block_information(blockHeight):
    p = Path('tests')
    
    with open(p / 'blocks' / f'{blockHeight}' / 'blockInfo', 'r') as f:   
            blockInfo = json.load(f)
    with open(p / 'blocks' / f'{blockHeight}' / 'blockSummary', 'r') as f:    
            blockSummary = json.load(f)
    
    block = {'blockInfo': blockInfo, 'blockSummary': blockSummary}
    return block

def get_tx_at_index(node, blockHeight, index):
    block = read_block_information (blockHeight)
    if 'transactionSummaries' in block['blockSummary']:
        tx_by_index = {x['index']: x for x in  block['blockSummary']['transactionSummaries']}
        return Transaction(node).init_from_node(tx_by_index[index])
    else:
        return None

def test_tx():
    block = read_block_information (3639756)
    assert block['blockInfo']['blockHeight'] == 3639756

def test_tx_cns_registration(node: ConcordiumNode):
    tx = get_tx_at_index(node, 4018850, 8)
    
    assert tx.cns_domain.domain_name == "99.ccd"
    assert tx.cns_domain.action == CNSActions.register

def test_tx_transfer(node: ConcordiumNode):
    tx = get_tx_at_index(node, 2826981, 0)
    
    assert tx.type == 'accountTransaction'
    assert tx.contents == 'transfer'
    assert tx.result['outcome'] == 'success'

def test_tx_transfer(node: ConcordiumNode):
    tx = get_tx_at_index(node, 1992437, 1)
    
    assert tx.type == 'accountTransaction'
    assert tx.contents == 'transferWithSchedule'
    assert tx.result['outcome'] == 'success'
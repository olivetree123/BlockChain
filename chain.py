"""
区块链是分布式的
首先，每个节点需要保存一份网络中其他节点的列表。
每个节点最开始的时候都会从别人那里获取一份最新的链，然后在这个链的基础上进行操作，比如挖矿、交易，一顿操作之后会把这条链同步给其他人。

存在的问题：
    1. 各个节点如何保证节点列表的一致性，如何同步节点列表的信息。
    2. 各个节点如何保证链的一致性，如何同步链的信息。
"""
import copy
import hashlib
import requests
from typing import List
from urllib.parse import urlparse

from block import Block, Transaction



# 区块链
class BlockChain(object):

    def __init__(self, blocks=None):
        self.blocks: List[Block] = blocks if blocks else []
        self.nodes = set()
    
    @property
    def last_block(self):
        block = self.blocks[-1] if self.blocks else None
        return block

    def _new_block(self, transactions):
        """创建新区块"""
        previous_hash = self.blocks[-1].hash() if self.blocks else None
        block = Block(len(self.blocks)+1, "", transactions, previous_hash)
        self.blocks.append(block)
        return block

    def transction(self, sender, receiver, amount):
        """交易"""
        transaction = Transaction(sender, receiver, amount)
        return self._new_block([transaction])
    
    def validate_proof(self, proof):
        """验证工作量，验证通过可获得奖励"""
        last_hash = self.last_block.hash()
        value = f'{last_hash}{proof}'.encode()
        hash_value = hashlib.sha256(value).hexdigest()
        if hash_value[:2] == "00":
            return True
        return False
    
    def register_node(self, address):
        """节点注册，返回其他节点的列表"""
        r = copy.deepcopy(self.set)
        parsed_url = urlparse(address)
        self.set.add(parsed_url.netloc)
        return r
    
    @staticmethod
    def validate_chain(chain):
        """验证链是否有效，链的每个block 都必须被认为有效才算验证通过"""
        if not isinstance(chain, BlockChain):
            return False
        index = 1
        while index < len(chain.blocks):
            prev_block = chain.blocks[index-1]
            block = chain.blocks[index]
            if block.previous_hash != prev_block.hash():
                return False
        return True

    def resolve_conflicts(self):
        """解决冲突"""
        for node in self.nodes:
            r = requests.get(f"http://{node}/chain")
            if not r.ok:
                continue
            blocks = r.json().get("data")
            chain = BlockChain(blocks)
            if len(chain.blocks) > len(self.blocks) and self.validate_chain(chain):
                self.blocks = chain.blocks


 

blockChain = BlockChain()
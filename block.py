"""
每个 Block 包含以下信息：
    - 索引
    - 时间戳
    - 事务列表 (这是什么东西？)
    - 校验 (工作量证明)
    - 前序区块的哈希值

事务列表应该包括两种信息，一种是挖矿报酬信息，一种是用户之间的交易信息。挖矿报酬也可以看成一种交易，由系统发起而已。

问题：
    1. 区块与人是什么关系？
        答：区块中的事务信息包含了该区块拥有者的信息。
    2. 交易会产生新的区块吗？
        答：会。区块中的事务列表包含了交易信息。
    3. 工作量验证，如何验证？
        答：用户首先向云端获取参数，然后在本地通过计算取得符合条件的另一个参数，发送给云端进行验证，验证通过可获得奖励。
    4. 如果用户一直发送错误的验证参数，要怎么办？
    5. 如何防止用户发送重复的验证参数？
        答：验证工作量时，将最后一个区块的哈希值作为参数。验证失败时返回最后一个区块的哈希值。
"""
import copy
import time
import json
import hashlib

from typing import List


# 事务
class Transaction(object):
    
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

# 区块
class Block(object):

    def __init__(self, index, proof, transactions: List[Transaction], previous_hash):
        if not isinstance(transactions, (list, tuple)):
            raise TypeError("list or tuple expected, but {} found".format(type(transactions)))
        self.index = index
        self.proof = proof
        self.timestamp = time.time()
        self.transactions  = transactions
        self.previous_hash = previous_hash
    
    def hash(self):
        """给区块生成哈希值"""
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def json(self):
        return copy.deepcopy(self.__dict__)



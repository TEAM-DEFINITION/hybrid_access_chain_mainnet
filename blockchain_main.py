import hashlib
import json
import ast
from time import time


class Blockchain(object):

    current_transaction = []

    def __init__(self):
        pass

    def genesis_block(self):

        genesis_transaction = []
        genesis_transaction.append(
            {
                'sender' : "0000000000000000",
                'recipient' : "0000000000000000",
                'amount' : 100000000,
            }
        )

        genesis_block = {
            'index' : 1,
            'timestamp' : time(),
            'transactions' : genesis_transaction,
            'proof' : 100,
            'prev_hash' : 1,
        }

        f = open("db_blockchain\\purplechain","w", encoding="UTF8")
        f.write(str(genesis_block))
        f.close

    def clear_transaction(self):
        self.current_transaction.clear()

    def new_block(self, proof, prev_hash):

        # 트랜잭션 발생 확인
        if len(self.current_transaction) == 0 :
            return 0

        # 새로운 블록을 생성하고 체인에 넣는다
        f = open("db_blockchain\\purplechain","r", encoding="UTF8")
        chain = f.readlines()
        f.close()

        block = {
            'index' : len(chain) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transaction,
            'proof' : proof,
            'prev_hash' : prev_hash or self.hash(self.chain[-1]),
        }

        # 현거래 리스트 초기화

        f = open("db_blockchain\\purplechain","a", encoding="UTF8")
        f.write("\n" + str(block))
        f.close()
        return block

    @staticmethod
    def hash(block):
        # 블록의 해시값을 출력한다
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha512(block_string).hexdigest()

    @property
    def last_block(self):
        # 체인의 긴 블록을 반환한다
        f = open("db_blockchain\\purplechain","r", encoding="UTF8")
        current_chain = f.readlines()
        last_block = ast.literal_eval(current_chain[-1])
        f.close()
        return last_block

    def new_transaction(self, sender, recipient, amount):

        '''
        새로운 거래는 다음으로 채굴될 블록에 포함됨
        거래는 3개의 인자로 구성
        sender, recipient : str - 수신자와 송신자의 주소
        amount : int
        return - 해당 거래가 속해질 블록의 숫자
        '''

        self.current_transaction.append(
            {
                'sender' : sender,
                'recipient' : recipient,
                'amount' : amount,
            }
        )

        return self.last_block['index'] + 1
    
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha512(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def show_chain(self):
        f = open("db_blockchain\\purplechain","r", encoding="UTF8")
        result = f.readlines()
        return result
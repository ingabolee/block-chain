from hashlib import sha3_256
from time import time


class BlockChain:

    def __init__(self):
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.create_genesis_block()

    def create_genesis_block(self):
        self.create_block(nonce=0, hash_of_previous_block=0)

    def create_block(self, nonce, hash_of_previous_block):
        block = Block(
            index=len(self.chain),
            nonce=nonce,
            hash_of_previous_block=hash_of_previous_block,
            data=self.current_data)
        self.current_data = []

        self.chain.append(block)
        return block

    @staticmethod
    def check_block_validity(block, prev_block):
        if prev_block.index + 1 != block.index:
            return False

        elif prev_block.calculate_hash != block.hash_of_previous_block:
            return False

        elif not BlockChain.verifying_proof(block.nonce, prev_block.nonce):
            return False

        elif block.timestamp <= prev_block.timestamp:
            return False

        return True

    def new_data(self, sender, recipient, quantity):
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })
        return True

    @staticmethod
    def proof_of_work(last_proof):
        
        nonce = 0
        while BlockChain.verifying_proof(nonce, last_proof) is False:
            nonce += 1

        return nonce

    @staticmethod
    def verifying_proof(last_proof, proof):
        # this works by checking whether there are 5 leading zeros. addind one more zeros increases
        # the difficulty of mining exponentially 
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha3_256(guess).hexdigest()
        return guess_hash[:5] == "00000"

    @property
    def latest_block(self):
        return self.chain[-1]

    def block_mining(self, name_of_miner):

        self.new_data(
            sender="0",  
            recipient=name_of_miner, # person to be rewarded for a succesful block mine
            quantity=1,
        )

        last_block = self.latest_block

        nonce_of_previous_block = last_block.nonce
        nonce = self.proof_of_work(nonce_of_previous_block)

        hash_of_previous_block = last_block.calculate_hash()
        block = self.create_block(nonce, hash_of_previous_block)

        return vars(block)

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def obtain_block_object(block_data):

        return Block(
            block_data['index'],
            block_data['nonce'],
            block_data['hash_of_previous_block'],
            block_data['data'],
            timestamp=block_data['timestamp'])


class Block:
    # initializing our block parameters
    def __init__(self, index, nonce, hash_of_previous_block, data, timestamp=None):
        self.index = index
        self.nonce = nonce
        self.hash_of_previous_block = hash_of_previous_block
        self.data = data
        self.timestamp = timestamp or time()

    @property
    def calculate_hash(self):
        block_of_string = f"{self.index}{self.nonce}{self.hash_of_previous_block}{self.data}{self.timestamp}"
        
        # uses sha3_256 whose variant, Keccak-256, is used in the Ethereum blockchain
        return sha3_256(block_of_string.encode()).hexdigest()

    def __repr__(self):
        return f"{self.index} - {self.nonce} - {self.hash_of_previous_block} - {self.data} - {self.timestamp}"


def mine_blocks():
    blockchain = BlockChain()
    # This simulates a typical mining environment where the process takes place continously. 
    # Add more recepients and watch the block grow bigger
    while True:
        recepient = str(input("Enter Name of Miner: "))
        last_block = blockchain.latest_block
        nonce_of_previous_block = last_block.nonce
        nonce = blockchain.proof_of_work(nonce_of_previous_block)

        blockchain.new_data(
            sender="0", 
            recipient=f"{recepient}",
            quantity=1, 
        )

        hash_of_previous_block = last_block.calculate_hash
        blockchain.create_block(nonce, hash_of_previous_block)

        for block in blockchain.chain:
            print(block)

if __name__ == "__main__":
    mine_blocks()
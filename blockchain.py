# This file contains all the Business Logic for Block and Implements Block Class
import datetime as date
import hashlib
import json

# Loading configuration
with open('config.json', 'r') as f:
    config = json.load(f)

difficulty_target = config['BLOCK']['DIFFICULTY_TARGET']  # Difficulty target for blocks
genesis_hash = config['BLOCK']['GENESIS_HASH']  # Genesis block value for blocks
max_number_of_data_blocks_in_circledblockchain = config['BLOCKCHAIN'][
    'MAX_NUMBER_OF_BLOCKS_IN_CIRCLED_BLOCKCHAIN']  # Capacity of a Blockchain


class Block:  # Main class for defining Blocks and all their attributes and methods
    result = str

    def __init__(self, index, data, previous_hash, block_type):
        self.nonce = int
        self.index = index
        self.timestamp = date.datetime.utcnow()
        self.data = data
        self.previous_hash = previous_hash
        self.current_hash = str
        self.block_type = block_type  # Not included in the content for hash generation
        self.content = str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + \
                       str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8')

    def set_hash(self, hash):
        self.current_hash = hash

    def set_nonce(self, nonce):
        self.nonce = nonce

    def get_currnet_hash(self):
        return self.current_hash

    def get_current_index(self):
        return self.index

    def get_timestamp(self):
        return self.timestamp

    def stringify_block(self):
        block_string = (
            self.index, self.timestamp.isoformat(), self.data, self.current_hash, self.previous_hash, self.nonce,
            self.block_type)
        return block_string

    def hasher(self, passed_nonce):
        self.nonce = passed_nonce
        Hash_object = hashlib.sha256(self.content + str(self.nonce).encode('utf-8'))
        return Hash_object.hexdigest()

    def mine(self):
        potential_nonce = 0
        result = self.hasher(potential_nonce)
        # print(result)
        while (str(result).startswith(difficulty_target) != True):
            potential_nonce = potential_nonce + 1
            result = self.hasher(potential_nonce)
            # print(result)
        self.current_hash = result
        self.nonce = potential_nonce


def create_new_block(type, lastblock=None, passed_data=None):
    block_type = type

    if block_type == "DB":  # creates a data block
        new_index = lastblock.index + 1
        new_data = passed_data
        new_previous_hash = lastblock.current_hash
        newBlock = Block(new_index, new_data, new_previous_hash, block_type)
        newBlock.mine()
        return newBlock

    elif block_type == "AGB":  # creates an Absolute Genesis Block (AGB)
        new_index = 0
        new_data = str("Absolute Genesis Block")
        new_previous_hash = genesis_hash
        newBlock = Block(new_index, new_data, new_previous_hash, block_type)
        newBlock.mine()
        return newBlock

    elif block_type == "RGB":  # creates a Relative Genesis Block (RGB)

        new_index = lastblock.index + 1
        new_data = str("Relative Genesis Block")
        new_previous_hash = lastblock.current_hash
        newBlock = Block(new_index, new_data, new_previous_hash, block_type)
        newBlock.mine()
        return newBlock

    elif block_type == "TB":  # creates a terminal block
        new_index = lastblock.index + 1
        new_data = passed_data
        new_previous_hash = lastblock.current_hash
        newBlock = Block(new_index, new_data, new_previous_hash, block_type)
        newBlock.mine()
        return newBlock

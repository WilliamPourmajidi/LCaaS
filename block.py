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


class TerminalBlock(Block):  # Main class for defining Terminal Blocks (TB)  and all their attributes and methods
    def __init__(self, index, data, previous_hash, block_type, aggr_hash, timestamp_from, timestamp_to,
                 block_index_from, block_index_to):
        self.nonce = int
        self.index = index
        self.timestamp = date.datetime.utcnow()
        self.data = data
        self.previous_hash = previous_hash
        self.current_hash = str
        self.aggr_hash = aggr_hash
        self.timestamp_from = timestamp_from
        self.timestamp_to = timestamp_to
        self.block_index_from = block_index_from
        self.block_index_to = block_index_to
        self.block_type = block_type  # Not included in the content for hash generation
        self.content = str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + \
                       str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8') + str(
            self.aggr_hash).encode('utf-8') + \
                       str(self.timestamp_from).encode('utf-8') + str(self.timestamp_to).encode('utf-8') + \
                       str(self.block_index_from).encode('utf-8') + str(self.block_index_to).encode('utf-8')


class CircledBlockchain:
    chain = []

    def __init__(self, index, block_size):
        self.index = index
        self.chain[:block_size]

    def add_block_to_CB(self, passed_block):
        self.chain.append(passed_block)
        # if len(c) > block_size:
        #     raise Exception('Circledblock has no more space for new blocks!')

    def stringify_CB(self):
        CB_string = (
            self.index)
        return CB_string


class SuperBlockchain:

    def __init__(self, index):
        self.index = index
        self.chain = []

    def add_block_to_SBC(self, passed_superblock):
        self.chain.append(passed_superblock)

    def stringify_SBC(self):
        for i in range(0, self.index):
            CBC_string = "replace with the code that gets the content of each supoerblock"
        return CBC_string


def create_new_block(type, lastblock=None, passed_data=None):
    block_type = type

    if block_type == "DB":  # creates a data block
        new_index = lastblock.index + 1
        new_data = passed_data
        new_previous_hash = lastblock.current_hash
        newBlock = Block(new_index, new_data, new_previous_hash, block_type)
        newBlock.mine()
        return newBlock

    if block_type == "AGB":  # creates an Absolute Genesis Block
        new_index = 0
        new_data = str("Genesis Block")
        new_previous_hash = genesis_hash
        newBlock = Block(new_index, new_data, new_previous_hash, block_type)
        newBlock.mine()
        return newBlock

    if block_type == "TB":  # creates a terminal block
        new_index = lastblock.index + 1
        new_data = passed_data
        new_previous_hash = lastblock.current_hash
        newBlock = Block(new_index, new_data, new_previous_hash, block_type)
        newBlock.mine()
        return newBlock


class Index:
    def __init__(self):
        self.index = 0

    def increase_index(self):
        self.index += 1

    def get_current_index(self):
        return self.index


class LogChain:
    blocks_index = Index()  # This will be used as main index counter for blocks in the lifecycle of instances of this class
    cbs_index =  Index()  # This will be used as main index counter for Circledblocks in the lifecycle of instances of this class
    cb_array = []  # This array holds the indexes for all CircledBlockchain in this class

    def __init__(self, cid):
        """

        :rtype: object
        """
        self.customer_id = cid
        self.SBC = SuperBlockchain(index=cid)

    def create_new_circledblockchain(self, index):
        self.index = index
        self.CB = CircledBlockchain(index, max_number_of_data_blocks_in_circledblockchain)
        self.cb_array.append(self.CB)

    def return_circledblockchain_index(self):
        return self.CB.index


        # class CircledBlockchain:
        #     chain = []
        #
        #     def __init__(self, index, block_size):
        #         self.index = index
        #         self.chain[:block_size]
        #
        #     def add_block_to_CB(self, passed_block):
        #         self.chain.append(passed_block)
        #         # if len(c) > block_size:
        #         #     raise Exception('Circledblock has no more space for new blocks!')
        #
        #     def stringify_CB(self):
        #         CB_string = (
        #             self.index)
        #         return CB_string

    #     FirstCB = CircledBlockchain(current_index, max_number_of_data_blocks_in_blockchain)
    #     FirstCB.add_block_to_CB(gb)
    #     print(FirstCB.chain[current_index].stringify_block())
    #     previous_block = gb
    #     new_block_data_element = data
    #     new_block = create_new_block("DB", previous_block, new_block_data_element)
    #     previous_block = new_block
    #     FirstCB.add_block_to_CB(new_block)
    #
    #
    # else:
    #     new_block_data_element = data
    #     new_block = create_new_block("DB", previous_block, new_block_data_element)
    #     FirstCB.add_block_to_CB(new_block)
    #
    # print(FirstCB.chain[current_index].stringify_block())

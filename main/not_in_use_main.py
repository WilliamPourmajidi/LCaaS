# Metamask Phrase: audit smoke try dinner gym first much hero high tilt swim private

# # This  is the Main file for the LCaaS project
# import csv
# import json
# from block import *
# with open('config.json', 'r') as f:
#     config = json.load(f)
#
# # Loading configuration
# # difficulty_target = config['BLOCK']['DIFFICULTY_TARGET']  # Difficulty target for blocks
# # genesis_hash = config['BLOCK']['GENESIS_HASH']  # Genesis block value for blocks
# # data_storage_option = config['BLOCK']['DATA_STORAGE_OPTION']  # option to store actual data in the block or hash of data
#
# data_storage_option = config['BLOCK']['DATA_STORAGE_OPTION']  # option to store actual data in the block or store hash of data(more privacy)
# max_number_of_data_blocks_in_blockchain = config['BLOCKCHAIN']['MAX_NUMBER_OF_BLOCKS_IN_BLOCKCHAIN']  # Capacity of a Blockchain
#
# with open('Logs-10.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=';')
#     block_count = 0
#     FirstCB = CircledBlockchain()
#
#     gb = create_new_block("GB")
#     previous_block = gb
#     # print(gb.stringify_block())
#     FirstCB.add_block_to_CB(previous_block)
#     counter = 0
#
#     for row in readCSV:
#
#
#         if (data_storage_option == "actual_data" and block_count < max_number_of_data_blocks_in_blockchain):
#             new_block_data_element = str(row)
#             new_block = create_new_block("DB", previous_block, new_block_data_element)
#      #      print(new_block.stringify_block())
#             FirstCB.add_block_to_CB(new_block)
#             previous_block = new_block
#             block_count += 1
#         new_block_data_element = "hash of all hashes"
#         new_tb = create_new_block("TB", previous_block, new_block_data_element)
#         FirstCB.add_block_to_CB(new_tb)
# print(FirstCB.chain[0].stringify_block())
# print(FirstCB.chain[1].stringify_block())
# print(FirstCB.chain[2].stringify_block())
# print(FirstCB.chain[3].stringify_block())
#
#     #print(new_tb.stringify_block())
#
#
#
#
#
#
#     # # print("Interesting" , block_to_add.stringify_block())
#     # TestCB.add_block_to_CB(block_to_add.stringify_block())
#     # previous_block = block_to_add
#     # current_number_of_blocks += 1
#     # print("Current number", block_count)
#

# LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
#       relative_genesis_block)  # add relative genesis block to the current CB
# print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
#           LCaaS.block_index.get_current_index()].stringify_block())
# LCaaS.block_index.increase_index()
#
#
# print("*After********Log: Length of CB ", len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain))

# LCaaS.block_index.increase_index()
# previous_block = relative_genesis_block
# new_block_data_element = data
# new_block = create_new_block("DB", previous_block, new_block_data_element)
# LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
#     new_block)  # add data block to the current CB
# print("Log: The CB index is    : ", LCaaS.cb_index.get_current_index())
# print("Log: The block index is : ", LCaaS.block_index.get_current_index())
# # print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
#           LCaaS.block_index.get_current_index()].stringify_block())
# LCaaS.block_index.increase_index()
# print("Log: The block index at the END is  : ", LCaaS.block_index.get_current_index())


# This file contains all the Business Logic for Block and Implements Block Class
import datetime as date
import hashlib
import json

# Loading configuration
with open('config.json', 'r') as f:
    config = json.load(f)

difficulty_target = config['BLOCK']['DIFFICULTY_TARGET']  # Difficulty target for blocks
genesis_hash = config['BLOCK']['GENESIS_HASH']  # Genesis block value for blocks
max_number_of_data_blocks_in_blockchain = config['BLOCKCHAIN'][
    'MAX_NUMBER_OF_BLOCKS_IN_BLOCKCHAIN']  # Capacity of a Blockchain


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

    # def stringify_CB(self):
    #     CB_string = (
    #         self.index, self.timestamp.isoformat(), self.data, self.current_hash, self.previous_hash, self.nonce,self.block_type)
    #     return CB_string
    #


def create_new_block(type, lastblock=None, passed_data=None):
    block_type = type

    if block_type == "DB":  # creates a data block
        new_index = lastblock.index + 1
        new_data = passed_data
        new_previous_hash = lastblock.current_hash
        newBlock = Block(new_index, new_data, new_previous_hash, block_type)
        newBlock.mine()
        return newBlock

    if block_type == "GB":  # creates a genesis block
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


def blockify(data,
             tcb):  # helper function. It takes data and adds it to LCaaS and return required details to be sent back to the consumer of API
    if (tcb == 0):
        block_count = 0
        current_index = 0
        gb = create_new_block("GB")
        FirstCB = CircledBlockchain(current_index, max_number_of_data_blocks_in_blockchain)
        FirstCB.add_block_to_CB(gb)
        print(FirstCB.chain[current_index].stringify_block())
        previous_block = gb
        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        FirstCB.add_block_to_CB(new_block)
        current_index += 1
        tcb += 1
    else:
        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        FirstCB.add_block_to_CB(new_block)
        current_index += 1
        tcb += 1

    print(FirstCB.chain[current_index].stringify_block())


class Index:
    def __init__(self):
        self.index = 0

    def increase_index(self):
        self.index += 1

    def get_current_index(self):
        return self.index

#
# elif ((len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) == max_number_of_blocks_in_circledblockchain)):
#     print("Log: All previous blocks were added to CB with index: ", LCaaS.cb_index.get_current_index())
#
#     LCaaS.cb_index.increase_index()
#     print("Log: The CB index is now increased and is : ", LCaaS.cb_index.get_current_index())
#
#     LCaaS.block_index.reset_current_index()
#     print("Log: The block index is now reset and is   : ", LCaaS.block_index.get_current_index())
#     LCaaS.create_new_CircledBlockchain(LCaaS.cb_index.get_current_index(),
#                                        max_number_of_blocks_in_circledblockchain)
#
#     print("Log: A new CircledBlockchain and a Relative Genesis Block (RGB) is needed")
#     LCaaS.create_new_CircledBlockchain(LCaaS.cb_index.get_current_index(),
#                                        max_number_of_blocks_in_circledblockchain)
#
#     previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index() - 1].chain[-1]
#     print("you remember previous block? ", previous_block.stringify_block())
#     relative_genesis_block = create_new_block("RGB", previous_block)
#     print("Log: The CB index is    : ", LCaaS.cb_index.get_current_index())
#     print("Log: The block index is : ", LCaaS.block_index.get_current_index())
#     LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
#         relative_genesis_block)  # add relative genesis block to the current CB
#     print("this is the problem", LCaaS.cb_array[2].chain[0].stringify_block())
#     LCaaS.block_index.increase_index()
#     previous_block = relative_genesis_block
#     new_block_data_element = data
#     new_block = create_new_block("DB", previous_block, new_block_data_element)
#     LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
#         new_block)  # add data block to the current CB
#     print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
#               LCaaS.block_index.get_current_index()].stringify_block())
#     LCaaS.block_index.increase_index()

# elif (len(LCaaS.cb_array[
# LCaaS.cb_index.get_current_index()].chain) < max_number_of_blocks_in_circledblockchain):
#     print("current_cbs_index = ", LCaaS.cb_index.get_current_index())
# print("current blocks_index = ", LCaaS.block_index.get_current_index())
# previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
#     LCaaS.block_index.get_current_index() - 1]
# new_block_data_element = data
# new_block = create_new_block("DB", previous_block, new_block_data_element)
# LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
#     new_block)  # add data block to the current CB
# print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
#           LCaaS.block_index.get_current_index()].stringify_block())
# LCaaS.block_index.increase_index()

# LCaaS.blocks_index.increase_index()
# previous_block = genesis_block
# new_block_data_element = data
# new_block = create_new_block("DB", previous_block, new_block_data_element)
# LCaaS.cb_array[LCaaS.cbs_index.get_current_index()].add_block_to_CB(
#     new_block)  # add data block to the current CB
# print(LCaaS.cb_array[LCaaS.cbs_index.get_current_index()].chain[
#           LCaaS.blocks_index.get_current_index()].stringify_block())
# LCaaS.blocks_index.increase_index()
#

# new_block = create_new_block("DB", previous_block, new_block_data_element)

# LCaaS.cb_array[LCaaS.cbs_index.get_current_index()].add_block_to_CB(new_block)  # add data block to the current CB
# print(LCaaS.cb_array[LCaaS.cbs_index.get_current_index()].chain[2].stringify_block())
# LCaaS.blocks_index.increase_index()

# block_count = 0
# current_index = 0
# gb = create_new_block("GB")
# block_to_add = gb
# print(gb.stringify_block())
# FirstCB = CircledBlockchain(current_index, max_number_of_data_blocks_in_blockchain)
# FirstCB.add_block_to_CB(block_to_add)
# # new_block_data_element = request.get_json()
# # new_block = create_new_block("DB", block_to_add, new_block_data_element)
# print(new_block.stringify_block())
# FirstCB.add_block_to_CB(new_block)
# previous_block = new_block
# #             block_count += 1

#
# with open('Logs-10.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=';')
#     block_count = 0
#     FirstCB = CircledBlockchain()
#
#     gb = create_new_block("GB")
#     previous_block = gb
#     # print(gb.stringify_block())
#     FirstCB.add_block_to_CB(previous_block)
#     counter = 0
#
#     for row in readCSV:
#
#         if (data_storage_option == "actual_data" and block_count < max_number_of_data_blocks_in_blockchain):
#             new_block_data_element = str(row)
#             new_block = create_new_block("DB", previous_block, new_block_data_element)
#             #      print(new_block.stringify_block())
#             FirstCB.add_block_to_CB(new_block)
#             previous_block = new_block
#             block_count += 1
#         new_block_data_element = "hash of all hashes"
#         new_tb = create_new_block("TB", previous_block, new_block_data_element)
#         FirstCB.add_block_to_CB(new_tb)
# print(FirstCB.chain[0].stringify_block())
# print(FirstCB.chain[1].stringify_block())
# print(FirstCB.chain[2].stringify_block())
# print(FirstCB.chain[3].stringify_block())

# print(new_tb.stringify_block())

# # print("Interesting" , block_to_add.stringify_block())
# TestCB.add_block_to_CB(block_to_add.stringify_block())
# previous_block = block_to_add
# current_number_of_blocks += 1
# print("Current number", block_count)

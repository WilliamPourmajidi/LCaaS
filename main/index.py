# This  is the Main file for the LCaaS project
import csv
import json
from pip._vendor.pyparsing import _ForwardNoRecurse
from blockchain import *
from LC import *
from flask import Flask, jsonify, request

app = Flask(__name__)

# Loading configuration
# difficulty_target = config['BLOCK']['DIFFICULTY_TARGET']  # Difficulty target for blocks
# genesis_hash = config['BLOCK']['GENESIS_HASH']  # Genesis block value for blocks
# data_storage_option = config['BLOCK']['DATA_STORAGE_OPTION']  # option to store actual data in the block or hash of data

data_storage_option = config['BLOCK'][
    'DATA_STORAGE_OPTION']  # option to store actual data in the block or store hash of data(more privacy)
max_number_of_blocks_in_circledblockchain = config['BLOCKCHAIN'][
    'MAX_NUMBER_OF_BLOCKS_IN_CIRCLED_BLOCKCHAIN']  # Capacity of a Blockchain

LCaaS = LogChain(500747320)


@app.route('/')
def displayStatus():
    return '<h2>Logchain-as-a-Service (LCaaS)has been succesfully initiated! Use our RESTful API to interact with it!</h2>'


@app.route('/verify_blocks')
def get_blocks():
    return jsonify(Circledblock)


@app.route('/submit_raw', methods=['POST'])
def submit_raw():
    # print("We received: ", request.get_json())
    received_data = (request.get_json())
    blockify(LCaaS.block_index.get_current_index(), LCaaS.cb_index.get_current_index(), received_data)
    return 'A new record has been succesfully recieved', 202


def blockify(current_block_index_value, current_cb_index_value, data):  # Helper function

    if ((current_block_index_value == 0) and (
            current_cb_index_value == 0)):  # we need to generate an absolute genesis block first
        print("Log: A new CircledBlockchain and a an Absolute Genesis Block (AGB) is needed")
        LCaaS.create_new_CircledBlockchain(LCaaS.cb_index.get_current_index(),
                                           max_number_of_blocks_in_circledblockchain)  # create a circled blockchain  using index of cb
        absolute_genesis_block = create_new_block(type="AGB")
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            absolute_genesis_block)  # add genesis block to the current CB
        print("Log: The CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The block index is : ", LCaaS.block_index.get_current_index())
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.block_index.get_current_index()].stringify_block())
        LCaaS.block_index.increase_index()
        previous_block = absolute_genesis_block
        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_block)  # add data block to the current CB
        print("Log: The CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The block index is : ", LCaaS.block_index.get_current_index())
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.block_index.get_current_index()].stringify_block())
        LCaaS.block_index.increase_index()

    elif ((current_block_index_value != 0) and (
            current_cb_index_value == 0 ) and (len(LCaaS.cb_array[
                                                     LCaaS.cb_index.get_current_index()].chain) < max_number_of_blocks_in_circledblockchain)):  # we need to generate data block for the current Circled Blockchain
        print("Log: A new data block is needed in the same CircledBlockchain")
        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            LCaaS.block_index.get_current_index() - 1]
        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_block)  # add data block to the current CB
        print("Log: The CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The block index is : ", LCaaS.block_index.get_current_index())
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.block_index.get_current_index()].stringify_block())
        LCaaS.block_index.increase_index()

    elif ((current_block_index_value == 0) and (
            current_cb_index_value != 0 ) and (len(LCaaS.cb_array[
                                                     LCaaS.cb_index.get_current_index()].chain) < max_number_of_blocks_in_circledblockchain)):
        # we need to generate a relative genesis block
        print("Log: It's time for a new CircledBlockchain and a Relative Genesis Block (RGB)")
        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
        LCaaS.block_index.get_current_index() - 1]
        print("righ before RGB, current_cbs_index = ", LCaaS.cb_index.get_current_index())
        print("current blocks_index = ", LCaaS.block_index.get_current_index())
        relative_genesis_block = create_new_block("DB", previous_block)
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
        relative_genesis_block)  # add relative genesis block to the current CB
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
        LCaaS.block_index.get_current_index()].stringify_block())



    else:
        print("Log: All previous blocks were added to CB with index: ", LCaaS.cb_index.get_current_index())

        LCaaS.cb_index.increase_index()
        print("Log: The CB index is now increased and is : ", LCaaS.cb_index.get_current_index())

        LCaaS.block_index.reset_current_index()
        print("Log: The block index is now reset and is   : ", LCaaS.block_index.get_current_index())
        LCaaS.create_new_CircledBlockchain(LCaaS.cb_index.get_current_index(),
                                           max_number_of_blocks_in_circledblockchain)

        print("Log: A new CircledBlockchain and a Relative Genesis Block (RGB) is needed")
        LCaaS.create_new_CircledBlockchain(LCaaS.cb_index.get_current_index(),
                                           max_number_of_blocks_in_circledblockchain)


        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()-1].chain[-1]
        print("you remember previous block? ", previous_block.stringify_block())
        relative_genesis_block = create_new_block("RGB",previous_block)
        print("Log: The CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The block index is : ", LCaaS.block_index.get_current_index())
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            relative_genesis_block)  # add relative genesis block to the current CB
        print(LCaaS.cb_array[1].chain[
                  LCaaS.block_index.get_current_index()].stringify_block())
        LCaaS.block_index.increase_index()
        previous_block = relative_genesis_block
        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_block)  # add data block to the current CB
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.block_index.get_current_index()].stringify_block())
        LCaaS.block_index.increase_index()

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

if __name__ == '__main__':
    app.run()

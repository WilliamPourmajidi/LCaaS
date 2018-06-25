# This  is the Main file for the LCaaS project
import csv
import json
from pip._vendor.pyparsing import _ForwardNoRecurse
from blockchain import *
from LC import *
from flask import Flask, jsonify, request
import pyrebase

### Firebase Settings ####

config = {
    "apiKey": "AIzaSyAmXGisFxk0xJmAT_KpFDvCmfqH-YBP_04",
    "authDomain": "bcaas-2018.firebaseapp.com",
    "databaseURL": "https://bcaas-2018.firebaseio.com",
    "storageBucket": "",
    "messagingSenderId": "568088402855",
    "serviceAccount": "serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
# # authenticate a user
user = auth.sign_in_with_email_and_password("william.pourmajidi@gmail.com", "bcaas2018Pass")

# user['idToken']
db = firebase.database()

app = Flask(__name__)

# Loading configuration
# difficulty_target = config['BLOCK']['DIFFICULTY_TARGET']  # Difficulty target for blocks
# genesis_hash = config['BLOCK']['GENESIS_HASH']  # Genesis block value for blocks
# data_storage_option = config['BLOCK']['DATA_STORAGE_OPTION']  # option to store actual data in the block or hash of data

with open('config.json', 'r') as f:
    config = json.load(f)
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
        LCaaS.create_new_CircledBlockchain(LCaaS.cb_index.get_current_index())
        # create a circled blockchain  using index of cb
        absolute_genesis_block = create_new_block(type="AGB")
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            absolute_genesis_block)  # add absolute genesis block to the current CB
        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(),'Type':"AGB" ,
                                            'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                user['idToken'])  # push data to Firebase

        print("Log: The current CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The current block index is : ", LCaaS.block_index.get_current_index())
        print("Log: The current internal block counter index is : ", LCaaS.internal_block_counter.get_current_index())
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())

        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

        previous_block = absolute_genesis_block
        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_block)  # add data block to the current CB

        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(),'Type':"DB" ,
                                            'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                user['idToken'])  # push data to firebase
        print("Log: The current CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The current block index is : ", LCaaS.block_index.get_current_index())
        print("Log: The current internal block counter index is : ", LCaaS.internal_block_counter.get_current_index())
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())
        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()


    elif ((current_block_index_value != 0) and (len(LCaaS.cb_array[
                                                        LCaaS.cb_index.get_current_index()].chain) < (
                                                        max_number_of_blocks_in_circledblockchain - 1))):  # we need to generate data block for the current Circled Blockchain

        print("Log: A new data block is needed in the same CircledBlockchain")
        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            LCaaS.internal_block_counter.get_current_index() - 1]
        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_block)  # add data block to the current CB
        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(),'Type':"DB" ,
                                            'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                user['idToken'])  # push data to Firebase

        print("Log: The current CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The current block index is : ", LCaaS.block_index.get_current_index())
        print("Log: The current internal block counter index is : ", LCaaS.internal_block_counter.get_current_index())
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())
        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()


    elif ((current_block_index_value != 0) and (len(LCaaS.cb_array[
                                                        LCaaS.cb_index.get_current_index()].chain) < (

                                                        max_number_of_blocks_in_circledblockchain))):  # we need to generate terminal block for the  Circled Blockchain

        print("Log: A new Terminal block is needed")
        # create a terminal block

        aggregated_hash = ""
        count = 0

        while (count <= len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) - 1):
            if (count <= len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) - 2):
                aggregated_hash = aggregated_hash + LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                    count].get_currnet_hash() + ","
                count += 1
            else:
                aggregated_hash = aggregated_hash + LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                    count].get_currnet_hash()
                count += 1

        print("Log: Aggregated_hash for this CB is: ", aggregated_hash)

        print("---------------------------------------------------------------------")
        print("TS_from", LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_timestamp())
        print("TS_to", LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_timestamp())

        print("Block_from", LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_current_index())
        print("Block_to", LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_current_index())

        timestamp_from = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_timestamp()

        timestamp_to = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_timestamp()

        block_index_from = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_current_index()

        block_index_to = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_current_index()
        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[-1]
        new_TB_data = TB_data(aggregated_hash, timestamp_from, timestamp_to, block_index_from, block_index_to)
        new_TerminalBlock = create_new_block("TB", previous_block, new_TB_data)
        # let's add the TB to the CB
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_TerminalBlock)
        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(),'Type':"TB" ,
                                            'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                LCaaS.internal_block_counter.get_current_index()].data.aggr_hash}),
                                user['idToken'])  # push data to Firebase

        print(new_TerminalBlock.stringify_block())
        terminalBlock_data_string = (
            new_TerminalBlock.data.aggr_hash, new_TerminalBlock.data.timestamp_to, new_TerminalBlock.data.timestamp_to,
            new_TerminalBlock.data.block_index_from, new_TerminalBlock.data.block_index_to)
        print("Log: The current CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The current block index is : ", LCaaS.block_index.get_current_index())
        print("Log: The current internal block counter index is : ", LCaaS.internal_block_counter.get_current_index())

        # print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
        #           LCaaS.internal_block_counter.get_current_index()].stringify_block())
        print(terminalBlock_data_string)
        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

    elif ((current_block_index_value != 0) and (len(LCaaS.cb_array[
                                                        LCaaS.cb_index.get_current_index()].chain) == max_number_of_blocks_in_circledblockchain)):

        print("Log: A new CircledBlockchain and a Relative Genesis Block (RGB) is needed")
        print("Log: The previous CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The previous CB length is :  ", len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain))
        print("Log: The current block index is : ", LCaaS.block_index.get_current_index())
        print("Log: The internal block counter index is : ", LCaaS.internal_block_counter.get_current_index())

        LCaaS.cb_index.increase_index()  # increase the index for CB
        LCaaS.internal_block_counter.reset_current_index()  # reset the internal counter to 0 as new CB needs index to be 0

        print("Log: The new CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The current block index is : ", LCaaS.block_index.get_current_index())
        print("Log: The current internal block counter  is : ",
              LCaaS.internal_block_counter.get_current_index())

        LCaaS.create_new_CircledBlockchain(LCaaS.cb_index.get_current_index())

        print("Log: The current CB length is : ", len(LCaaS.cb_array[
                                                          LCaaS.cb_index.get_current_index()].chain))
        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index() - 1].chain[-1]
        print("Log: The CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The block index is : ", LCaaS.block_index.get_current_index())
        relative_genesis_block = create_new_block("RGB", previous_block)

        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            relative_genesis_block)  # add relative genesis block to the current CB
        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(),'Type':"RGB" ,
                                            'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                user['idToken'])  # push data to Firebase

        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())

        print("Now the length of CB is", len(LCaaS.cb_array[
                                                 LCaaS.cb_index.get_current_index()].chain))

        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

        # LCaaS.cb_array[LCaaS.cb_index].internal_index.increase_index()

        print("Log: The CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The block index is : ", LCaaS.block_index.get_current_index())
        print("*After*Log: Length of CB ", len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain))
        previous_block = relative_genesis_block
        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_block)  # add data block to the current CB

        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(),'Type':"DB" ,
                                            'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                user['idToken'])  # push data to Firebase

        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())

        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()



if __name__ == '__main__':
    app.run()

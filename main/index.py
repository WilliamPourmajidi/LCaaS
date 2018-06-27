# This  is the Main file for the LCaaS project
# Designed and implemented by William Pourmajidi - June 2018 - Canada Ontario
# Departament of Computer Science
# As partial fulfillment for  Doctorate of Philosophy in Computer Science (Ph.D)

import csv
import json
from pip._vendor.pyparsing import _ForwardNoRecurse
from blockchain import *
from LC import *
from flask import Flask, jsonify, request
import pyrebase

### Firebase Settings ####
# Link: https://bcaas-2018.firebaseio.com/Blocks.json
# Link: https://console.firebase.google.com/u/0/project/bcaas-2018/database/bcaas-2018/data
# Link: https://passwordsgenerator.net/sha256-hash-generator/
# You will need to change the following settings to your own Firebase instance

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

with open('config.json', 'r') as f:
    config = json.load(f)
data_storage_option = config['BLOCK'][
    'DATA_STORAGE_OPTION']  # option to store actual data in the block or store hash of data(more privacy)
max_number_of_blocks_in_circledblockchain = config['BLOCKCHAIN'][
    'MAX_NUMBER_OF_BLOCKS_IN_CIRCLED_BLOCKCHAIN']  # Capacity of a Blockchain


# Instantiate a new object from LogChain
LCaaS = LogChain(500747320)


@app.route('/')
def displayStatus():
    return '<h2>Logchain-as-a-Service (LCaaS)has been succesfully initiated! Use our RESTful API to interact with it!</h2>'


@app.route('/verify_blocks')
# def get_blocks():
#     return jsonify(Circledblock)

@app.route('/submit_raw', methods=['POST'])
def submit_raw():
    # print("We received: ", request.get_json())
    received_data = (request.get_json())
    blockify(LCaaS.block_index.get_current_index(), LCaaS.cb_index.get_current_index(), received_data)
    # return_string = str(" new record has been successfully received and added to LogChain" + "\ncurrent CB_Index: " + str(LCaaS.cb_index.get_current_index())+ "\ncurrent Block_Index: " + str(LCaaS.block_index.get_current_index()))
    return LCaaS.return_string, 202


@app.route('/submit_digest', methods=['POST'])
def submit_digest():
    # print("We received: ", request.get_json())
    received_data = request.get_json()
    print(received_data)
    passed_digest_value  = received_data['digest']
    print(passed_digest_value)
    if (len(passed_digest_value)==64):
        blockify(LCaaS.block_index.get_current_index(), LCaaS.cb_index.get_current_index(), received_data)
    else:
        LCaaS.return_string = "Received data is not in correct SHA256 format"

        return LCaaS.return_string, 202



def blockify(current_block_index_value, current_cb_index_value, data):  # Helper function

    if ((current_block_index_value == 0) and (
            current_cb_index_value == 0)):  # we need to generate an absolute genesis block first
        print("Log: A new CircledBlockchain and a an Absolute Genesis Block (AGB) is needed")
        LCaaS.create_new_CircledBlockchain(LCaaS.cb_index.get_current_index())
        # create a circled blockchain  using index of cb
        absolute_genesis_block = create_new_block(type="AGB")
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            absolute_genesis_block)  # add absolute genesis block to the current CB
        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "AGB",
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
        #### Important : Add logic here to handle the actual or hash condition for data storage
        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_block)  # add the first data block to the current CB




        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",
                                            'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                user['idToken'])  # push data to firebase

        LCaaS.return_string = str(
            "An AGB was created for the new circle block. AGB details are as follows:\n" + str(
                absolute_genesis_block.stringify_block()) + "\nThe new record has been successfully received and added to LogChain with following details:\n" + str(
                new_block.stringify_block()))

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


        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",
                                            'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                LCaaS.internal_block_counter.get_current_index()].stringify_block()}),

                                user['idToken'])  # push data to Firebase
        LCaaS.return_string = str(
            "The new record has been successfully received and added to LogChain with following details:\n" + str(
                new_block.stringify_block()))

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

        concatinated_hashes = ""
        count = 0

        while (count <= len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) - 1):
            if (count <= len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) - 2):
                concatinated_hashes = concatinated_hashes + LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                    count].get_current_hash() + ","
                count += 1
            else:
                concatinated_hashes = concatinated_hashes + LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                    count].get_current_hash()
                count += 1

        print("Log: Aggregated_hash for all blocks of this CB is ", concatinated_hashes)

        timestamp_from = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_timestamp()

        timestamp_to = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_timestamp()

        block_index_from = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_index()

        block_index_to = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_index()

        # Here we convert the co

        hash_of_hashes = (hashlib.sha256(str(concatinated_hashes).encode('utf-8'))).hexdigest()

        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[-1]
        new_TB_data = TB_data(hash_of_hashes, timestamp_from, timestamp_to, block_index_from, block_index_to)
        new_TerminalBlock = create_new_block("TB", previous_block, new_TB_data)

        # let's add the TB to the CB
        print("Log: Terminal block is : ", stringify_terminalblock(new_TerminalBlock))


        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_TerminalBlock)  # add terminal block to CB


        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "TB",
                                            'Content': stringify_terminalblock(new_TerminalBlock)}),
                                user[
                                    'idToken'])  # push terminal block to Firebase (it is stringied so it can be viewed properly)
        LCaaS.return_string = str(
            "A new Terminal Block has been successfully created and added to LogChain with following details:\n" + str(
                stringify_terminalblock(new_TerminalBlock)))


        # terminalBlock_data_string = (
        #     new_TerminalBlock.data.aggr_hash, new_TerminalBlock.data.timestamp_to, new_TerminalBlock.data.timestamp_to,
        #     new_TerminalBlock.data.index_from, new_TerminalBlock.data.index_to)
        # print("Log: The current CB index is    : ", LCaaS.cb_index.get_current_index())
        # print("Log: The current block index is : ", LCaaS.block_index.get_current_index())
        # print("Log: The current internal block counter index is : ", LCaaS.internal_block_counter.get_current_index())
        #
        # # print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
        # #           LCaaS.internal_block_counter.get_current_index()].stringify_block())
        # print(terminalBlock_data_string)
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
        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "RGB",
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

        db.child("Blocks").push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",
                                            'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                user['idToken'])  # push data to Firebase

        LCaaS.return_string = str(
            "An RGB was created for the new circle block. RGB details are as follows:\n" + str(
                relative_genesis_block.stringify_block()) + "\nThe new record has been successfully received and added to LogChain with following details:\n" + str(
                new_block.stringify_block()))

        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())

        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()


if __name__ == '__main__':
    app.run()

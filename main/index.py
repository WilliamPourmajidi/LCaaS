# This  is the Main file for the LCaaS project
# Please make sure you have configured the LCaaS via editing config.json
# added the upper level directory in the path
import sys
sys.path.append('../')

from LC import *
from flask import Flask, request
import pyrebase
from ethereum import *
import datetime

### Firebase Settings ####
# Link: https://bcaas-2018.firebaseio.com/Blocks.json
# Link: https://console.firebase.google.com/u/0/project/bcaas-2018/database/bcaas-2018/data
# Link: https://passwordsgenerator.net/sha256-hash-generator/
# Link: https://ropsten.etherscan.io/
# You will need to change the following settings to your own Firebase instance
#


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
push_to_ethereum = config['BLOCK']['PUSH_TO_ETHEREUM']
push_to_firebase = config['BLOCK']['PUSH_TO_FIREBASE']
verified_sender_address = config['ETHEREUM']['VERIFIED_SENDER_ADDRESS']

# Instantiate a new object from Logchain
LCaaS = LogChain(500747320)


@app.route('/')
def displayStatus():
    return '<h2>Logchain-as-a-Service (LCaaS) has been succesfully initiated! Use our RESTful API to interact with it!</h2>'


@app.route('/submit_raw', methods=['POST'])  # handles submit_raw method
def submit_raw():
    # print("We received: ", request.get_json())
    received_data = (request.get_json())

    blockify(LCaaS.block_index.get_current_index(), LCaaS.cb_index.get_current_index(), received_data)
    return LCaaS.return_string, 202


@app.route('/submit_digest', methods=['POST'])  # handles submit_digest method
def submit_digest():
    # print("We received: ", request.get_json())

    received_data = request.get_json()
    print(received_data)
    passed_digest_value = received_data['digest']
    print(passed_digest_value)
    if (len(passed_digest_value) == 64):
        blockify(LCaaS.block_index.get_current_index(), LCaaS.cb_index.get_current_index(), received_data)
        return LCaaS.return_string, 202
    else:
        LCaaS.return_string = "Received data is not in correct SHA256 format"

        return LCaaS.return_string, 202


@app.route('/verify_raw', methods=['POST'])  # handles verify_raw method
def verify_raw():
    # print("We received: ", request.get_json())
    received_data = (request.get_json())
    search_b(received_data)
    return LCaaS.return_string, 202


@app.route('/verify_digest', methods=['POST'])  # handles verify_digest method
def verify_digest():
    received_data = (request.get_json())
    search_b(received_data)
    return LCaaS.return_string, 202


@app.route('/verify_tb', methods=['POST'])  # handles verify_tb method
def verify_tb():
    received_data = (request.get_json())
    passed_tb_hash_value = received_data['tb_hash']
    search_tb(passed_tb_hash_value)

    return LCaaS.return_string, 202


def blockify(current_block_index_value, current_cb_index_value, data):  # Helper function

    # We need to generate an absolute genesis block first and then a data block with the received data
    if (LCaaS.sbc_index.get_current_index() < 1):
        blockname = "Circled blockchain-" + str(LCaaS.sbc_index.get_current_index())
    else:
        blockname = "Circled blockchain-" + str(LCaaS.sbc_index.get_current_index() - 1)
    if ((current_block_index_value == 0) and (
            current_cb_index_value == 0) and max_number_of_blocks_in_circledblockchain > 3):
        print("Log: A new CircledBlockchain and a an Absolute Genesis Block (AGB) is needed")
        LCaaS.create_new_CircledBlockchain(LCaaS.cb_index.get_current_index())
        # create a circled blockchain using index of cb
        absolute_genesis_block = create_new_block(type="AGB")
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            absolute_genesis_block)  # add absolute genesis block to the current CB

        # db.child("Circled blockchain-0").push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "AGB",
        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "AGB",
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
            new_block)  # add the first data block to the current CB
        # db.child("Circled blockchain-0").push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",
                                                 'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                     LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                     user['idToken'])  # push data to firebase

        LCaaS.return_string = str(
            "An AGB was created for the new circled blockchain. AGB details are as follows:\n" + str(
                absolute_genesis_block.stringify_block()) + "\nThe new record has been successfully received and added to Logchain with following details:\n" + str(
                new_block.stringify_block()))

        print("Log: The current CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The current block index is : ", LCaaS.block_index.get_current_index())
        print("Log: The current internal block counter index is : ", LCaaS.internal_block_counter.get_current_index())
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())
        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

    # Special case,  we need to generate AGB, DB, and TB in one shot
    elif ((current_block_index_value == 0) and (
            current_cb_index_value == 0) and max_number_of_blocks_in_circledblockchain == 3):

        print("Log: A new CircledBlockchain and a an Absolute Genesis Block (AGB) is needed")
        LCaaS.create_new_CircledBlockchain(LCaaS.cb_index.get_current_index())
        # create a circled blockchain using index of cb
        absolute_genesis_block = create_new_block(type="AGB")
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            absolute_genesis_block)  # add absolute genesis block to the current CB

        # db.child("Circled blockchain-0").push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "AGB",

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "AGB",
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
            new_block)  # add the first data block to the current CB
        # db.child("Circled blockchain-0").push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",
                                                 'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                     LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                     user['idToken'])  # push data to firebase

        LCaaS.return_string = str(
            "An AGB was created for the new circled blockchain. AGB details are as follows:\n" + str(
                absolute_genesis_block.stringify_block()) + "\nThe new record has been successfully received and added to Logchain with following details:\n" + str(
                new_block.stringify_block()))

        print("Log: The current CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The current block index is : ", LCaaS.block_index.get_current_index())
        print("Log: The current internal block counter index is : ", LCaaS.internal_block_counter.get_current_index())
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())
        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

        # create a terminal block as the last block of this CB
        concatenated_hashes = ""
        count = 0

        while (count <= len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) - 1):
            if (count <= len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) - 2):
                concatenated_hashes = concatenated_hashes + LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                    count].get_current_hash() + ","
                count += 1
            else:
                concatenated_hashes = concatenated_hashes + LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                    count].get_current_hash()
                count += 1

        print("Log: Aggregated_hash for all blocks of this CB is ", concatenated_hashes)

        timestamp_from = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_timestamp()

        timestamp_to = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_timestamp()

        block_index_from = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_index()

        block_index_to = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_index()

        # Here we make a hash of all hashes in the current CB

        hash_of_hashes = (hashlib.sha256(str(concatenated_hashes).encode('utf-8'))).hexdigest()

        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[-1]
        new_TB_data = TB_data(hash_of_hashes, timestamp_from, timestamp_to, block_index_from, block_index_to)
        new_TerminalBlock = create_new_block("TB", previous_block, new_TB_data)

        # let's add the TB to the CB
        print("Log: Terminal block is : ", stringify_terminalblock(new_TerminalBlock))

        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(

            new_TerminalBlock)  # add terminal block to CB

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "TB",
                                                 'Content': stringify_terminalblock(new_TerminalBlock)}),
                                     user[
                                         'idToken'])  # push terminal block to Firebase (it is stringied so it can be viewed properly)

        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

        # add terminal block content to the data element of a SB and add the SB to the SBC
        #########################################################
        if (len(LCaaS.SBC.superchain) == 0):
            SBC_gensis = create_new_block("SBC-GB")  # create a genesis block for the SBC
            LCaaS.SBC.add_block_to_SBC(SBC_gensis)  # ad the SBC-GB to SBC
            SB_GB_submission = ""
            SB_submission = ""

            if (push_to_firebase == "Yes"):
                db.child("SuperBlocks").push(
                json.dumps(
                    {'Index': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].get_index(), 'Type': "SBC-GB",
                     'Content': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()}),
                user['idToken'])  # push super block to Firebase

            LCaaS.sbc_index.increase_index()

            previous_super_block = SBC_gensis
            new_super_block_data_element = stringify_terminalblock(
                new_TerminalBlock)  # adding the entire terminal block as data element for superblock
            new_super_block = create_new_block("SB", previous_super_block, new_super_block_data_element)
            LCaaS.SBC.add_block_to_SBC(new_super_block)  # add the super block to the SBC

            print("Log: a new SB is created: " + str(
                LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()))
            if (push_to_firebase == "Yes"):
                db.child("SuperBlocks").push(
                json.dumps(
                    {'Index': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].get_index(), 'Type': "SB",
                     'Content': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()}),
                user['idToken'])  # push super block to Firebase

            ################################ Code for Ethereum integration #############################

            if (push_to_ethereum == 'Yes'):

                LCE = LC_Ethereum

                if (LCE.check_whether_address_is_approved(verified_sender_address)):
                    print(
                        "Log: The client has already paid the membership fee and is authorized to use Logchain and Ethereum connection")
                    SB_GB_submission = "\nThe Gensis Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(SBC_gensis.stringify_block()), 0.1))
                    print(SB_GB_submission)
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

                else:
                    LCE.send_ether_to_contract(0.03)  ## membership fee
                    print(
                        "Log: The membership fee is now paid and the client is authorized to use Logchain and Ethereum connection")
                    SB_GB_submission = "\nThe Gensis Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(SBC_gensis.stringify_block()), 0.1))
                    print(SB_GB_submission)
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

            ##########################################################################################

            LCaaS.return_string = str(
                "The last data block for this CB is generated:\n" + str(
                    new_block.stringify_block()) + "\nA Terminal Block have been successfully created and added to Logchain with following details\n" + str(
                    stringify_terminalblock(new_TerminalBlock)) + "\n A new Super block has been created\n" + str(
                    LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()) + str(
                    SB_GB_submission) + str(SB_submission))

            LCaaS.sbc_index.increase_index()


        else:

            previous_super_block = LCaaS.SBC.superchain[
                LCaaS.sbc_index.get_current_index() - 1]  # this is the previous superblock in the superblockchain for this instance of Logchain
            new_super_block_data_element = stringify_terminalblock(
                new_TerminalBlock)  # adding the entire terminal block as data element for superblock

            new_super_block = create_new_block("SB", previous_super_block, new_super_block_data_element)
            LCaaS.SBC.add_block_to_SBC(new_super_block)  # add the super block to the SBC

            ################################ Code for Ethereum integration #############################
            SB_submission = ""

            if (push_to_ethereum == 'Yes'):

                LCE = LC_Ethereum
                # LTest.send_ether_to_contract(0.03)

                if (LCE.check_whether_address_is_approved(0x3f4f9bb697f84a26fbc85883f2ff4d31a36ed83c)):
                    print(
                        "Log: The client has already paid the membership fee and is authorized to use Logchain and Ethereum connection")
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

                else:
                    LCE.send_ether_to_contract(0.03)  ## membership fee
                    print(
                        "Log: The membership fee is now paid and the client is authorized to use Logchain and Ethereum connection")
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

            ##########################################################################################

            print("Log: " + str(LCaaS.SBC.superchain[LCaaS.cb_index.get_current_index()].stringify_block()))
            if (push_to_firebase == "Yes"):
                db.child("SuperBlocks").push(
                json.dumps(
                    {'Index': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].get_index(), 'Type': "SB",
                     'Content': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()}),
                user['idToken'])  # push super block to Firebase

            LCaaS.return_string = str(
                "The last data block for this CB is generated:\n" + str(
                    new_block.stringify_block()) + "\nA Terminal Block have been successfully created and added to Logchain with following details\n" + str(
                    stringify_terminalblock(new_TerminalBlock)) + "\n A new Super block has been created\n" + str(
                    LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()) + str(SB_submission))

            LCaaS.sbc_index.increase_index()



    # Another special case,  we need to generate RGB, DB, and TB in one shot
    elif ((current_block_index_value != 0) and max_number_of_blocks_in_circledblockchain == 3):

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

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "RGB",
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

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",
                                             'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                 LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                 user['idToken'])  # push data to Firebase

        LCaaS.return_string = str(
            "An RGB was created for the new circled blockchain. RGB details are as follows:\n" + str(
                relative_genesis_block.stringify_block()) + "\nThe new record has been successfully received and added to Logchain with following details:\n" + str(
                new_block.stringify_block()))

        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())

        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

        # create a terminal block as the last block of this CB
        concatenated_hashes = ""
        count = 0

        while (count <= len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) - 1):
            if (count <= len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) - 2):
                concatenated_hashes = concatenated_hashes + LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                    count].get_current_hash() + ","
                count += 1
            else:
                concatenated_hashes = concatenated_hashes + LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                    count].get_current_hash()
                count += 1

        print("Log: Aggregated_hash for all blocks of this CB is ", concatenated_hashes)

        timestamp_from = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_timestamp()

        timestamp_to = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_timestamp()

        block_index_from = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_index()

        block_index_to = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_index()

        # Here we make a hash of all hashes in the current CB

        hash_of_hashes = (hashlib.sha256(str(concatenated_hashes).encode('utf-8'))).hexdigest()

        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[-1]
        new_TB_data = TB_data(hash_of_hashes, timestamp_from, timestamp_to, block_index_from, block_index_to)
        new_TerminalBlock = create_new_block("TB", previous_block, new_TB_data)

        # let's add the TB to the CB
        print("Log: Terminal block is : ", stringify_terminalblock(new_TerminalBlock))

        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(

            new_TerminalBlock)  # add terminal block to CB

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "TB",
                                             'Content': stringify_terminalblock(new_TerminalBlock)}),
                                 user[
                                     'idToken'])  # push terminal block to Firebase (it is stringied so it can be viewed properly)

        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

        # add terminal block content to the data element of a SB and add the SB to the SBC
        #########################################################
        if (len(LCaaS.SBC.superchain) == 0):
            SBC_gensis = create_new_block("SBC-GB")  # create a genesis block for the SBC
            LCaaS.SBC.add_block_to_SBC(SBC_gensis)  # ad the SBC-GB to SBC
            SB_GB_submission = ""
            SB_submission = ""

            if (push_to_firebase == "Yes"):
                db.child("SuperBlocks").push(
                json.dumps(
                    {'Index': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].get_index(), 'Type': "SBC-GB",
                     'Content': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()}),
                user['idToken'])  # push super block to Firebase

            LCaaS.sbc_index.increase_index()

            previous_super_block = SBC_gensis
            new_super_block_data_element = stringify_terminalblock(
                new_TerminalBlock)  # adding the entire terminal block as data element for superblock
            new_super_block = create_new_block("SB", previous_super_block, new_super_block_data_element)
            LCaaS.SBC.add_block_to_SBC(new_super_block)  # add the super block to the SBC

            print("Log: a new SB is created: " + str(
                LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()))
            if (push_to_firebase == "Yes"):
                db.child("SuperBlocks").push(
                json.dumps(
                    {'Index': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].get_index(), 'Type': "SB",
                     'Content': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()}),
                user['idToken'])  # push super block to Firebase

            ################################ Code for Ethereum integration #############################

            if (push_to_ethereum == 'Yes'):

                LCE = LC_Ethereum

                if (LCE.check_whether_address_is_approved(verified_sender_address)):
                    print(
                        "Log: The client has already paid the membership fee and is authorized to use Logchain and Ethereum connection")
                    SB_GB_submission = "\nThe Gensis Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(SBC_gensis.stringify_block()), 0.1))
                    print(SB_GB_submission)
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

                else:
                    LCE.send_ether_to_contract(0.03)  ## membership fee
                    print(
                        "Log: The membership fee is now paid and the client is authorized to use Logchain and Ethereum connection")
                    SB_GB_submission = "\nThe Gensis Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(SBC_gensis.stringify_block()), 0.1))
                    print(SB_GB_submission)
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

            ##########################################################################################

            LCaaS.return_string = str(
                "The last data block for this CB is generated:\n" + str(
                    new_block.stringify_block()) + "\nA Terminal Block have been successfully created and added to Logchain with following details\n" + str(
                    stringify_terminalblock(new_TerminalBlock)) + "\n A new Super block has been created\n" + str(
                    LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()) + str(
                    SB_GB_submission) + str(SB_submission))

            LCaaS.sbc_index.increase_index()


        else:

            previous_super_block = LCaaS.SBC.superchain[
                LCaaS.sbc_index.get_current_index() - 1]  # this is the previous superblock in the superblockchain for this instance of Logchain
            new_super_block_data_element = stringify_terminalblock(
                new_TerminalBlock)  # adding the entire terminal block as data element for superblock

            new_super_block = create_new_block("SB", previous_super_block, new_super_block_data_element)
            LCaaS.SBC.add_block_to_SBC(new_super_block)  # add the super block to the SBC

            ################################ Code for Ethereum integration #############################
            SB_submission = ""

            if (push_to_ethereum == 'Yes'):

                LCE = LC_Ethereum
                # LTest.send_ether_to_contract(0.03)

                if (LCE.check_whether_address_is_approved(verified_sender_address)):
                    print(
                        "Log: The client has already paid the membership fee and is authorized to use Logchain and Ethereum connection")
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

                else:
                    LCE.send_ether_to_contract(0.03)  ## membership fee
                    print(
                        "Log: The membership fee is now paid and the client is authorized to use Logchain and Ethereum connection")
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

            ##########################################################################################

            print("Log: " + str(LCaaS.SBC.superchain[LCaaS.cb_index.get_current_index()].stringify_block()))
            if (push_to_firebase == "Yes"):
                db.child("SuperBlocks").push(
                json.dumps(
                    {'Index': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].get_index(), 'Type': "SB",
                     'Content': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()}),
                user['idToken'])  # push super block to Firebase

            LCaaS.return_string = str(
                "The last data block for this CB is generated:\n" + str(
                    new_block.stringify_block()) + "\nA Terminal Block have been successfully created and added to Logchain with following details\n" + str(
                    stringify_terminalblock(new_TerminalBlock)) + "\n A new Super block has been created\n" + str(
                    LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()) + str(SB_submission))

            LCaaS.sbc_index.increase_index()





    # We just need to generate data block for the current Circled Blockchain as the currenct CB has capacity for more data blocks.
    elif ((current_block_index_value != 0) and (len(LCaaS.cb_array[
                                                        LCaaS.cb_index.get_current_index()].chain) < (
                                                        max_number_of_blocks_in_circledblockchain - 2))):

        print("Log: A new data block is needed in the same CircledBlockchain")
        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            LCaaS.internal_block_counter.get_current_index() - 1]
        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_block)  # add data block to the current CB

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",
                                             'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                 LCaaS.internal_block_counter.get_current_index()].stringify_block()}),

                                 user['idToken'])  # push data to Firebase
        LCaaS.return_string = str(
            "The new record has been successfully received and added to Logchain with following details:\n" + str(
                new_block.stringify_block()))

        print("Log: The current CB index is    : ", LCaaS.cb_index.get_current_index())
        print("Log: The current block index is : ", LCaaS.block_index.get_current_index())
        print("Log: The current internal block counter index is : ", LCaaS.internal_block_counter.get_current_index())
        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())
        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

    # We need to generate the last data block and a terminal block for the current Circled Blockchain
    elif (((current_block_index_value != 0) and (len(LCaaS.cb_array[
                                                         LCaaS.cb_index.get_current_index()].chain) < (

                                                         max_number_of_blocks_in_circledblockchain - 1)))):
        print("Log: Last block of this CB needs to be created and added")
        print("Log: A new Terminal block is needed")
        # create the last data block for this CB

        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            LCaaS.internal_block_counter.get_current_index() - 1]

        new_block_data_element = data
        new_block = create_new_block("DB", previous_block, new_block_data_element)
        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(
            new_block)  # add the last  data block to the current CB

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",
                                             'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                 LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                 user['idToken'])  # push data to firebase

        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

        # create a terminal block as the last block of this CB

        concatenated_hashes = ""
        count = 0

        while (count <= len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) - 1):
            if (count <= len(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain) - 2):
                concatenated_hashes = concatenated_hashes + LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                    count].get_current_hash() + ","
                count += 1
            else:
                concatenated_hashes = concatenated_hashes + LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                    count].get_current_hash()
                count += 1

        print("Log: Aggregated_hash for all blocks of this CB is ", concatenated_hashes)

        timestamp_from = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_timestamp()

        timestamp_to = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_timestamp()

        block_index_from = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            0].get_index()

        block_index_to = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
            -1].get_index()

        # Here we make a hash of all hashes in the current CB

        hash_of_hashes = (hashlib.sha256(str(concatenated_hashes).encode('utf-8'))).hexdigest()

        previous_block = LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[-1]
        new_TB_data = TB_data(hash_of_hashes, timestamp_from, timestamp_to, block_index_from, block_index_to)
        new_TerminalBlock = create_new_block("TB", previous_block, new_TB_data)

        # let's add the TB to the CB
        print("Log: Terminal block is : ", stringify_terminalblock(new_TerminalBlock))

        LCaaS.cb_array[LCaaS.cb_index.get_current_index()].add_block_to_CB(

            new_TerminalBlock)  # add terminal block to CB

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "TB",
                                             'Content': stringify_terminalblock(new_TerminalBlock)}),
                                 user[
                                     'idToken'])  # push terminal block to Firebase (it is stringied so it can be viewed properly)

        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()

        # add terminal block content to the data element of a SB and add the SB to the SBC
        #########################################################
        if (len(LCaaS.SBC.superchain) == 0):
            SBC_gensis = create_new_block("SBC-GB")  # create a genesis block for the SBC
            LCaaS.SBC.add_block_to_SBC(SBC_gensis)  # ad the SBC-GB to SBC
            SB_GB_submission = ""
            SB_submission = ""

            if (push_to_firebase == "Yes"):
                db.child("SuperBlocks").push(
                json.dumps(
                    {'Index': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].get_index(), 'Type': "SBC-GB",
                     'Content': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()}),
                user['idToken'])  # push super block to Firebase

            LCaaS.sbc_index.increase_index()

            previous_super_block = SBC_gensis
            new_super_block_data_element = stringify_terminalblock(
                new_TerminalBlock)  # adding the entire terminal block as data element for superblock
            new_super_block = create_new_block("SB", previous_super_block, new_super_block_data_element)
            LCaaS.SBC.add_block_to_SBC(new_super_block)  # add the super block to the SBC

            print("Log: a new SB is created: " + str(
                LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()))
            if (push_to_firebase == "Yes"):
                db.child("SuperBlocks").push(
                json.dumps(
                    {'Index': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].get_index(), 'Type': "SB",
                     'Content': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()}),
                user['idToken'])  # push super block to Firebase

            ################################ Code for Ethereum integration #############################

            if (push_to_ethereum == 'Yes'):

                LCE = LC_Ethereum

                if (LCE.check_whether_address_is_approved(verified_sender_address)):
                    print(
                        "Log: The client has already paid the membership fee and is authorized to use Logchain and Ethereum connection")
                    SB_GB_submission = "\nThe Gensis Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(SBC_gensis.stringify_block()), 0.1))
                    print(SB_GB_submission)
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

                else:
                    LCE.send_ether_to_contract(0.03)  ## membership fee
                    print(
                        "Log: The membership fee is now paid and the client is authorized to use Logchain and Ethereum connection")
                    SB_GB_submission = "\nThe Gensis Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(SBC_gensis.stringify_block()), 0.1))
                    print(SB_GB_submission)
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

            ##########################################################################################

            LCaaS.return_string = str(
                "The last data block for this CB is generated:\n" + str(
                    new_block.stringify_block()) + "\nA Terminal Block have been successfully created and added to Logchain with following details\n" + str(
                    stringify_terminalblock(new_TerminalBlock)) + "\n A new Super block has been created\n" + str(
                    LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()) + str(
                    SB_GB_submission) + str(SB_submission))

            LCaaS.sbc_index.increase_index()


        else:

            previous_super_block = LCaaS.SBC.superchain[
                LCaaS.sbc_index.get_current_index() - 1]  # this is the previous superblock in the superblockchain for this instance of Logchain
            new_super_block_data_element = stringify_terminalblock(
                new_TerminalBlock)  # adding the entire terminal block as data element for superblock

            new_super_block = create_new_block("SB", previous_super_block, new_super_block_data_element)
            LCaaS.SBC.add_block_to_SBC(new_super_block)  # add the super block to the SBC

            ################################ Code for Ethereum integration #############################
            SB_submission = ""

            if (push_to_ethereum == 'Yes'):

                LCE = LC_Ethereum
                # LTest.send_ether_to_contract(0.03)

                if (LCE.check_whether_address_is_approved(0x3f4f9bb697f84a26fbc85883f2ff4d31a36ed83c)):
                    print(
                        "Log: The client has already paid the membership fee and is authorized to use Logchain and Ethereum connection")
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

                else:
                    LCE.send_ether_to_contract(0.03)  ## membership fee
                    print(
                        "Log: The membership fee is now paid and the client is authorized to use Logchain and Ethereum connection")
                    SB_submission = "\nThe Superblock is added to the Ethereum network " + str(
                        LCE.submit_a_superblock(str(new_super_block.stringify_block()), 0.1))
                    print(SB_submission)

            ##########################################################################################

            print("Log: " + str(LCaaS.SBC.superchain[LCaaS.cb_index.get_current_index()].stringify_block()))
            if (push_to_firebase == "Yes"):
                db.child("SuperBlocks").push(
                json.dumps(
                    {'Index': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].get_index(), 'Type': "SB",
                     'Content': LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()}),
                user['idToken'])  # push super block to Firebase

            LCaaS.return_string = str(
                "The last data block for this CB is generated:\n" + str(
                    new_block.stringify_block()) + "\nA Terminal Block have been successfully created and added to Logchain with following details\n" + str(
                    stringify_terminalblock(new_TerminalBlock)) + "\n A new Super block has been created\n" + str(
                    LCaaS.SBC.superchain[LCaaS.sbc_index.get_current_index()].stringify_block()) + str(SB_submission))

            LCaaS.sbc_index.increase_index()

    # We have no more room left in the CB, so let's create a new one and add a new RGB for it
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
        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "RGB",
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

        if (push_to_firebase == "Yes"):
            db.child(blockname).push(json.dumps({'Index': LCaaS.block_index.get_current_index(), 'Type': "DB",
                                             'Content': LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                                                 LCaaS.internal_block_counter.get_current_index()].stringify_block()}),
                                 user['idToken'])  # push data to Firebase

        LCaaS.return_string = str(
            "An RGB was created for the new circled blockchain. RGB details are as follows:\n" + str(
                relative_genesis_block.stringify_block()) + "\nThe new record has been successfully received and added to Logchain with following details:\n" + str(
                new_block.stringify_block()))

        print(LCaaS.cb_array[LCaaS.cb_index.get_current_index()].chain[
                  LCaaS.internal_block_counter.get_current_index()].stringify_block())

        LCaaS.block_index.increase_index()
        LCaaS.internal_block_counter.increase_index()


def search_b(passed_data):  # search blocks
    cb_counter = 0
    b_counter = 0
    search_result = ""

    while (cb_counter < len(LCaaS.cb_array)):
        while (b_counter < len(LCaaS.cb_array[cb_counter].chain)):
            if (LCaaS.cb_array[cb_counter].chain[b_counter].get_data() == passed_data):
                print("An exact match for submitted raw data has been found:")
                print(LCaaS.cb_array[cb_counter].chain[b_counter].stringify_block())
                search_result += "\nAn exact match for the submitted value has been found\n" + str(
                    LCaaS.cb_array[cb_counter].chain[b_counter].stringify_block())

                b_counter += 1

            else:
                print("No match was found for the received data!!!\n")
                b_counter += 1
                continue
            #     search_result = "No match was found for the received data!!!"

        b_counter = 0
        cb_counter += 1

    if (len(search_result) == 0):
        LCaaS.return_string = "No match was found for the received data!!!"
    else:
        LCaaS.return_string = search_result


def search_tb(passed_data):  # search for terminal blocks
    cb_counter = 0
    b_counter = 0
    search_result = ""

    # LCaaS.cb_array[cb_counter].chain[b_counter].get_data().aggr_hash == passed_data and

    while (cb_counter < len(LCaaS.cb_array)):
        while (b_counter < len(LCaaS.cb_array[cb_counter].chain)):
            if (LCaaS.cb_array[cb_counter].chain[b_counter].get_block_type() == "TB" and
                    LCaaS.cb_array[cb_counter].chain[b_counter].get_data().aggr_hash == passed_data):
                print("An exact TB  for the submitted hash data has been found:")

                # print(LCaaS.cb_array[cb_counter].chain[b_counter].stringify_block())
                # search_result += "\nA matching Terminal Block for the submitted hash has been fou" \
                #                  "nd\n" + str(
                #     LCaaS.cb_array[cb_counter].chain[b_counter].stringify_block())

                search_result += "\nAn exact match for the submitted value has been found\n" + str(
                    stringify_terminalblock(LCaaS.cb_array[cb_counter].chain[b_counter]))
                b_counter += 1
            else:
                print("No match was found for the received data!!!\n")
                b_counter += 1
                continue
                search_result = "No match was found for the received data!!!"

        b_counter = 0
        cb_counter += 1

    if (len(search_result) == 0):
        LCaaS.return_string = "No match was found for the received data!!!"
    else:
        LCaaS.return_string = search_result


# data element of TB is the hash of all CB block current_hashes
if __name__ == '__main__':
    app.run()

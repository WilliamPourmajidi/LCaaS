import time
# import datetime
from web3 import Web3, HTTPProvider
import contract_abi
from LC import *
from TimeKepper import *


##### details that will be used to send a transaction to ethereum test blockchain
ethereum_timer = TimeKeeper("ICSETimerEthereum.csv")



class LC_Ethereum:

    def send_ether_to_contract(amount_in_ether):
        # The address for the published contract on ethereum test blockchain  (Ropsten test network)
        contract_address = "0x6c6bf111b5d9d9060e53c5d967e0a7389d15634b"

        # sender private key (can be obtained from MetaMask plug-ins and connected
        wallet_private_key = "4f5ae03e520e54a18ff4d7d50b2e85d705eeb2e2cc154e4318fd9cb65d354cc3"
        wallet_address = "0x3f4f9bb697f84a26fbc85883f2ff4d31a36ed83c"

        # the w3 object

        w3 = Web3(HTTPProvider("https://ropsten.infura.io/GoumPwW0PttpedP5fdnG"))

        contract_address = w3.toChecksumAddress(contract_address)
        wallet_address = w3.toChecksumAddress(wallet_address)

        w3.eth.enable_unaudited_features()

        contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)
        amount_in_wei = w3.toWei(amount_in_ether, 'ether');

        nonce = w3.eth.getTransactionCount(wallet_address)

        txn_dict = {
            'to': contract_address,
            'value': amount_in_wei,
            'gas': 2000000,
            'gasPrice': w3.toWei('4', 'gwei'),
            'nonce': nonce,
            'chainId': 3
        }

        signed_txn = w3.eth.account.signTransaction(txn_dict, wallet_private_key)

        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        txn_receipt = None

        count = 0
        while txn_receipt is None and (count < 30):
            txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
            print(txn_receipt)

            time.sleep(10)

        if txn_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        return {'status': 'added', 'txn_receipt': txn_receipt}

    def check_whether_address_is_approved(sender_address):
        w3 = Web3(HTTPProvider("https://ropsten.infura.io/GoumPwW0PttpedP5fdnG"))
        contract_address = "0x6c6bf111b5d9d9060e53c5d967e0a7389d15634b"
        contract_address = w3.toChecksumAddress(contract_address)
        contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)
        wallet_address = w3.toChecksumAddress(sender_address)
        return contract.functions.isApproved(wallet_address).call()

    def submit_a_superblock(submission, amount_in_ether):
        contract_address = "0x6c6bf111b5d9d9060e53c5d967e0a7389d15634b"

        # sender private key (can be obtained from MetaMask plug-ins and connected
        wallet_private_key = "4f5ae03e520e54a18ff4d7d50b2e85d705eeb2e2cc154e4318fd9cb65d354cc3"
        wallet_address = "0x3f4f9bb697f84a26fbc85883f2ff4d31a36ed83c"

        # the w3 object

        w3 = Web3(HTTPProvider("https://ropsten.infura.io/GoumPwW0PttpedP5fdnG"))

        contract_address = w3.toChecksumAddress(contract_address)
        wallet_address = w3.toChecksumAddress(wallet_address)

        w3.eth.enable_unaudited_features()

        contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)
        amount_in_wei = w3.toWei(amount_in_ether, 'ether');

        nonce = w3.eth.getTransactionCount(wallet_address)

        txn_dict = contract.functions.sendSuperblock(submission).buildTransaction({
            'chainId': 3,
            # 'value': amount_in_wei,
            'gas': 2000000,
            'gasPrice': w3.toWei('6', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)


        # ethereum_submission_timestamp = datetime.datetime.now()
        ethereum_submission_timestamp = ethereum_timer.timer_start()

        print("Log: The transaction was submitted", ethereum_submission_timestamp)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        count = 0
        while tx_receipt is None and (count < 30):
            time.sleep(10)

            tx_receipt = w3.eth.getTransactionReceipt(result)

            print(tx_receipt)
        ethereum_receipt_timestamp = ethereum_timer.timer_stop()
        ethereum_timer.dump_timestamp(submission,ethereum_timer.duration(ethereum_submission_timestamp,ethereum_receipt_timestamp))




        # ethereum_receipt_timestamp = datetime.datetime.now()
        print("@@@@@@@@ The receipt was received", ethereum_receipt_timestamp)
        print("@@@@@@@@ Total transaction time is ", (ethereum_receipt_timestamp - ethereum_submission_timestamp), "Hour:Min:Sec:Milisecond")
        # with open('Timestamps.csv', mode='a') as Timestamp_file:
        #     timer_writer = csv.writer(Timestamp_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     timer_writer.writerow(['Block Details', tx_receipt, 'Block Transaction Time', (ethereum_receipt_timestamp - ethereum_submission_timestamp)])

        if tx_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        processed_receipt = contract.events.SuperblockSubmission().processReceipt(tx_receipt)

        print(processed_receipt)

        output = "Address {} Submitted a Superblock to ethereum : {}" \
            .format(processed_receipt[0].args._sender, processed_receipt[0].args._superblock)
        print(output)

        return {'status': 'added', 'processed_receipt': processed_receipt}

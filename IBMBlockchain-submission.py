import time
# import datetime
from web3 import Web3, HTTPProvider
import contract_abi
from LC import *
from TimeKepper import *

with open('config.json', 'r') as f:
    config = json.load(f)
verified_sender_address = config['ETHEREUM']['VERIFIED_SENDER_ADDRESS']
gas_price = config['ETHEREUM']['GAS_PRICE']

##### details that will be used to send a transaction to ethereum test blockchain
IBMBC_timer = TimeKeeper("Submission-timestamps-IBM-Blokchain.csv")






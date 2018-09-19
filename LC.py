from blockchain import *
import datetime
import csv

class Index:
    def __init__(self):
        self.index = 0

    def increase_index(self):
        self.index += 1

    def get_current_index(self):
        return self.index

    def reset_current_index(self):
        self.index = 0
        return self.index


class LogChain:
    block_index = Index()  # This will be used as main index counter for blocks in the lifecycle of instances of this class
    cb_index = Index()  # This will be used as main index counter for circled blockchains in the lifecycle of instances of this class
    sbc_index = Index()  # TBD
    internal_block_counter = Index()  # This will hold the internal counter for the count of existing blocks in a CB
    cb_array = []  # This array holds the indexes for all circled blockchains in this class
    return_string = ""

    def __init__(self, cid):
        """

        :rtype: object
        """
        self.customer_id = cid
        self.SBC = SuperBlockchain(index=0)
        # SBC_gensis = create_new_block("SBC-GB")
        # self.SBC.add_block_to_SBC(SBC_gensis)

    def create_new_CircledBlockchain(self, index):
        self.index = index
        self.CB = CircledBlockchain(index)
        self.cb_array.append(self.CB)


class CircledBlockchain:

    def __init__(self, index):
        self.index = index
        self.chain = []

    def add_block_to_CB(self, passed_block):
        self.chain.append(passed_block)


class SuperBlockchain:

    def __init__(self, index):
        self.index = index
        self.superchain = []

    def add_block_to_SBC(self, passed_superblock):
        self.superchain.append(passed_superblock)


class TB_data():

    def __init__(self, aggr_hash, timestamp_from, timestamp_to, index_from, index_to):
        self.aggr_hash = aggr_hash
        self.timestamp_from = timestamp_from
        self.timestamp_to = timestamp_to
        self.index_from = index_from
        self.index_to = index_to

    def get_tb_data_aggr_hash(self):
        return self.aggr_hash


def stringify_terminalblock(passed_block):
    terminalblock_string = (
        passed_block.get_index(), passed_block.get_timestamp().isoformat(),
        "aggr_hash: " + passed_block.get_data().aggr_hash,
        "timestamp_from: " +
        passed_block.get_data().timestamp_from.isoformat(),
        "timestamp_to: " + passed_block.get_data().timestamp_to.isoformat(),
        "index_from: " + str(passed_block.get_data().index_from),
        "index_to: " + str(passed_block.get_data().index_to),
        passed_block.get_current_hash(), passed_block.get_previous_hash(), passed_block.get_nonce(),
        passed_block.get_block_type())
    return terminalblock_string


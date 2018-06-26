from blockchain import *
import datetime as date


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
    cb_index = Index()  # This will be used as main index counter for Circledblocks in the lifecycle of instances of this class
    internal_block_counter = Index()
    cb_array = []  # This array holds the indexes for all CircledBlockchain in this class

    def __init__(self, cid):
        """

        :rtype: object
        """
        self.customer_id = cid
        self.SBC = SuperBlockchain(index=cid)

    # def create_new_CircledBlockchain(self, index,length):
    #     self.index = index
    #     self.CB = CircledBlockchain(index, length)
    #     self.cb_array.append(self.CB)

    def create_new_CircledBlockchain(self, index):
        self.index = index
        self.CB = CircledBlockchain(index)
        self.cb_array.append(self.CB)


class CircledBlockchain:
    # chain = []

    # def __init__(self, index, length):
    #     self.index = index
    #     self.chain[:length]

    def __init__(self, index):
        self.index = index
        self.chain = []

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


class TB_data():

    def __init__(self, aggr_hash, timestamp_from, timestamp_to, index_from, index_to):
        self.aggr_hash = aggr_hash
        self.timestamp_from = timestamp_from
        self.timestamp_to = timestamp_to
        self.index_from = index_from
        self.index_to = index_to


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

#
# def stringify_block(self,tb_index):
#     terminalblock_string = (
#         index, self.timestamp.isoformat(), self.data, self.current_hash, self.previous_hash, self.nonce,
#         self.block_type)
#     return block_string


#
# class TerminalBlock(Block):  # Main class for defining Terminal Blocks (TB)  and all their attributes and methods
#     def __init__(self, index, data, previous_hash, block_type, aggr_hash, timestamp_from, timestamp_to,
#                  block_index_from, block_index_to):
#         self.nonce = int
#         self.index = index
#         self.timestamp = date.datetime.utcnow()
#         self.data = TB_data()
#         self.previous_hash = previous_hash
#         self.current_hash = str
#         self.aggr_hash = aggr_hash
#         self.timestamp_from = timestamp_from
#         self.timestamp_to = timestamp_to
#         self.block_index_from = block_index_from
#         self.block_index_to = block_index_to
#         self.block_type = block_type  # Not included in the content for hash generation
#         self.content = str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + \
#                        str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8') + str(
#             self.aggr_hash).encode('utf-8') + \
#                        str(self.timestamp_from).encode('utf-8') + str(self.timestamp_to).encode('utf-8') + \
#                        str(self.block_index_from).encode('utf-8') + str(self.block_index_to).encode('utf-8')
#
#

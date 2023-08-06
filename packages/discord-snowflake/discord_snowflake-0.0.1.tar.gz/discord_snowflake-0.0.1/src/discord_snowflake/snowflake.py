import datetime
from random import choice

# idk why i need this

class Snowflake:
    def __init__(self, integer: int = None):
        if integer:
            bin_id = "0"+"{0:b}".format(integer)
            internal_process = bin_id[-17:-12]
            internal_worker = bin_id[-22:-17]
            timestamp = bin_id[-63:-22]
            while len(timestamp) != 42: timestamp = '0' + timestamp

            self.sequence = process = bin_id[-12:]
            self.nodeID = internal_worker + internal_process
            self.timestamp = int(timestamp, 2) + 1420070400000
            self.time = datetime.datetime.utcfromtimestamp(self.timestamp // 1000)
            self.id = int(bin_id, 2)
        else:
            nodeID = choice(range(0, 1024))
            sequence = choice(range(0, 4096))
            timestamp = int(datetime.datetime.timestamp(datetime.datetime.utcnow())*1000)
            self.time = datetime.datetime.utcfromtimestamp(timestamp//1000)
            self.timestamp = timestamp-1420070400000
            self.nodeID = nodeID # aka Internal worker + process ID
            self.sequence = sequence # process
            bin_nodeID = "{0:b}".format(self.nodeID)
            bin_sequence = "{0:b}".format(self.sequence)
            while len(bin_nodeID) != 10: bin_nodeID = '0'+bin_nodeID
            while len(bin_sequence) != 12: bin_sequence = '0'+bin_sequence
            timestamp = "{0:b}".format(self.timestamp)
            while len(timestamp) != 42: timestamp = '0'+timestamp
            self.id = int(timestamp+bin_nodeID+bin_sequence, 2)


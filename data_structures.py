'''
    These class helps to create instances which hold 
    information of sequences and patterns.
'''
from constants import SEPARATOR

class AHUSSequence():
    
    def __init__(self, sid, seq, ulist):
        self.sid = sid
        self.seq = seq
        self.ulist = ulist
        self.rlist = self.compute_rlist(seq, ulist)

    def compute_rlist(self, seq, ulist):
        return [
            0 if item == SEPARATOR
            else sum(ulist[(idx+1):])
            for idx, item in enumerate(seq)
        ]


class AHUPattern():
    
    def __init__(self, seq):
        self.seq = seq
        self.extension_item = seq[-2]

    def set_iulist(self, iulist):
        self.iulist = iulist

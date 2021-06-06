import csv
from typing import Sequence

from constants import ULIST_KEY, ILIST_KEY, SEPARATOR
from data_structures import AHUPattern, AHUSSequence

def compute_iextension(pattern, sdb, one_item_patterns, threshold):
    iextension_idx = {}
    for sid in pattern.iulist.keys():
        ilist = pattern.iulist[sid][ILIST_KEY]
        iextension_in_sequence = {}
        for idx in ilist:
            itemset_ending_idx = sdb[sid].seq.index(SEPARATOR, idx)
            iextension_candidates = list(range((idx+1), itemset_ending_idx))
            # print(f"{sdb[sid].seq}-{pattern.seq}-{iextension_candidates}")
            for candidate in iextension_candidates:
                # Organizing the dictionary this way helps to quicky
                # answer what the extension position is given the extension
                # item's position.
                # euu_value = euu(pattern, sdb[sid].seq[candidate], sdb, one_item_patterns)
                # if euu_value > threshold:
                iextension_in_sequence[candidate] = idx
        iextension_idx[sid] = iextension_in_sequence
    return iextension_idx

def compute_s_extension(pattern, sdb, one_item_patterns, threshold):
    s_extension = {}
    for sid in pattern.iulist.keys():
        s_extension[sid] = {}
        first_extension_idx = pattern.iulist[sid][ILIST_KEY][0]
        current_itemset_separator_idx = sdb[sid].seq.index('0', first_extension_idx)
        for idx, item in enumerate(sdb[sid].seq[current_itemset_separator_idx+1:], current_itemset_separator_idx+1):
            if item != SEPARATOR:
                # We do not consider those items of the same
                # itemset to the current extension item.
                backwards_itemset_separator_idx = -1
                for backwards_idx in range(idx-1, 0, -1):
                    if sdb[sid].seq[backwards_idx] == SEPARATOR:
                        backwards_itemset_separator_idx = backwards_idx
                        # We only need the first one.
                        break
                extension_idx = [
                    idx for idx in pattern.iulist[sid][ILIST_KEY] 
                    if idx < backwards_itemset_separator_idx
                ]
                # euu_value = euu(pattern, item, sdb, one_item_patterns)
                # if euu_value > threshold:
                s_extension[sid][idx] = extension_idx
    return s_extension

def i_extend(pattern, extension_item):
    new_pattern = AHUPattern(pattern.seq[:-1] + [extension_item] + pattern.seq[-1:])
    return new_pattern

def s_extend(pattern, extension_item):
    new_pattern = AHUPattern(pattern.seq + [extension_item, '0'])
    return new_pattern

def initialize_iulist(pattern, sequences):
    iulist = {}
    for sequence in sequences:
        iulist_in_sequence = {
            ILIST_KEY: [],
            ULIST_KEY: []
        }
        for idx, item in enumerate(sequence.seq):
            if item != SEPARATOR and item == pattern.extension_item:
                iulist_in_sequence[ILIST_KEY].append(idx)
                iulist_in_sequence[ULIST_KEY].append(sequence.ulist[idx])
        iulist[sequence.sid] = iulist_in_sequence
    # Finally we do want to keep any sequences possesing an empty iulist.
    iulist = {k: v for k, v in iulist.items() if len(v[ILIST_KEY]) != 0}
    return iulist

def compute_iulist(pattern, prefix, candidates, sdb):
    iulist = {}
    # We only consider those sequences where the prefix appears.
    for sid in prefix.iulist.keys():
        iulist_in_sequence = {
                ILIST_KEY: [],
                ULIST_KEY: []
        }
        # We seek for the extension item of the current pattern 
        # in each sequence.
        # (e.g. ['a', 'e', '0'] -> 'e' is an extension item)
        for idx, item in enumerate(sdb[sid].seq):
            # Once we found one, we make sure that it is an
            # iextension candicates using the iextension_candidates.
            if item == pattern.extension_item and \
            item != SEPARATOR and \
            idx in candidates[sid].keys():
                # candidates returns an extension_idx
                # that is where an extension item is appended.
                extension_idx = candidates[sid][idx]
                # This is where an iulist is helpful, we compute the iulist
                # for the current pattern utilizing the prefix's iulist.
                
                # In case of s-extension.
                util = 0
                if isinstance(extension_idx, list):
                    util_idx = []
                    for _idx in extension_idx:
                        util_idx.append(prefix.iulist[sid][ILIST_KEY].index(_idx))
                    utils = []
                    for _idx in util_idx:
                        utils.append(prefix.iulist[sid][ULIST_KEY][_idx])
                    max_util = max(utils)
                    util = max_util
                # It is simpler in case of i-extension.
                else:
                    util_idx = prefix.iulist[sid][ILIST_KEY].index(extension_idx)
                    util = prefix.iulist[sid][ULIST_KEY][util_idx]
                iulist_in_sequence[ILIST_KEY].append(idx)
                iulist_in_sequence[ULIST_KEY].append(util + sdb[sid].ulist[idx])
        iulist[sid] = iulist_in_sequence
    # Finally we do want to keep any sequences possesing an empty iulist.
    iulist = {k: v for k, v in iulist.items() if len(v[ILIST_KEY]) != 0}
    return iulist

def get_extension_candidates(extension_idx, sdb):
    extension_candidates = {}
    for sid in extension_idx.keys():
        for item in [sdb[sid].seq[i] for i in extension_idx[sid].keys()]:
            if item not in extension_candidates:
                extension_candidates[item] = [sid]
            else:
                extension_candidates[item].append(sid)

    return extension_candidates

def compute_swu(patterns, sdb):
    su = {sequence.sid: sum(sequence.ulist) for sequence in sdb}
    sw = {}
    for pattern in patterns.keys():
        sw[pattern] = 0
        for sequence in sdb:
            if pattern in sequence.seq:
                sw[pattern] += su[sequence.sid]
    return sw

def compute_peu(pattern, sdb):  
    peu = 0
    for sid in pattern.iulist.keys():
        peu_in_sequence = []
        for idx, idx_of_util in enumerate(pattern.iulist[sid][ILIST_KEY]):
            peu_in_sequence.append(sdb[sid].rlist[idx_of_util] + pattern.iulist[sid][ULIST_KEY][idx])
        peu += max(peu_in_sequence)
    return peu

# def rsu(pattern, item):
    

# def euu(pattern, candidate, sdb, one_item_patterns):
#     candidate_pattern = one_item_patterns[candidate]
#     return asu(pattern) + compute_peu(candidate_pattern, sdb)

def asu(pattern):
    asu = 0
    for sid in pattern.iulist.keys():
        asu += max(pattern.iulist[sid][ULIST_KEY])
    return asu

def read_data(sequences_file, utilities_file, items_file):
    sdb = []
    sequences = []
    utilities = []
    items = []

    with open(sequences_file, mode='r') as file:
        for line in file:
            sequences.append(line.rstrip().split('\t'))

    with open(utilities_file, mode='r') as file:
        for line in file:
            utilities.append(list(map(int, line.rstrip().split('\t'))))

    with open(items_file, mode='r') as file:
        for line in file:
            items = line.rstrip().split('\t')
            break

    for sid in range(len(sequences)):
        sdb.append(AHUSSequence(sid, sequences[sid], utilities[sid]))

    return sdb, items

"""
Data preprocessing tools. 
"""

from collections import OrderedDict
import logging
import copy
log = logging.getLogger(__name__)

def adapt_timestamps(input_dict, gap=0.1):
    """
    Adapt time end stamps to not overlap with following start time stamp.

    Args:
        input_dict(dict) : dictionary with timestamps, e.g. self.transcription_dict in a Parser
        gap(float, optional): gap to introduce between end and start index after adapt. Defaults to 0.1
    Returns:
        dict
    """
    chunks = copy.deepcopy(input_dict)
    # FIX ME this should probably be an Ordereddict to begin with
    sorted_chunks = OrderedDict(sorted(chunks.items(), key=lambda x:
                                       x[1].get("start")))
    keys = list(sorted_chunks.keys())
    for ind, key in enumerate(keys):
        if ind + 1== len(keys):
            break
        start, end = sorted_chunks[key].get("start"), sorted_chunks[key].get("end")
        next_key = keys[ind+1]
        next_start = sorted_chunks[next_key].get("start")
        if end >= next_start:
            new_end = max(next_start - gap, start)
            sorted_chunks[key]["end"] = new_end
            log.debug("Updated key '%s' end from %f to %f" %(key, end, new_end))
    return sorted_chunks

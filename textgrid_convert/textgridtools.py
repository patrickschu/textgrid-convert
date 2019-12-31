"""
Collect TextGrid related functionality here
"""
import logging
log = logging.getLogger(__name__)

# this is what we have in sbvParse

# Pull the stuff from sbv into a dictionary of format 
# {chunk_id: {"text": "", "start": int, "end": int}}

testdict = {0: {"speaker": "Mary", "text": "one", "start": 0, "end": 0.5896534423132239},
            1: {"speaker": "Mary", "text": "",  "end": 1.4123177579131596,"start": 0.5896534423132239},
            2: {"speaker": "Mary", "text": "two",  "end": 2.343227378197297, "start": 1.4123177579131596},
            3: {"speaker": "Mary", "text": "three",  "end": 3.1225935719235522, "start": 2.34322737819729},
            4: {"speaker": "Mary", "start": 3.1225935719235522, "end": 12.804852607709751, "text": "rest of the text * @ " 
               },
            5: {"speaker": "John", "start": 0, "end": 12.804852607709751, "text": "" }}


def ms_to_textgrid(milliseconds, strict=True):
    """
    Convert milliseconds to textgrid appropriate format,e.g. 12.88

    Args:
        milliseconds (int)
        strict(Bool): if True, will error out if no int given
    """
    if not isinstance(milliseconds, int):
        raise ValueError("Value {} for milliseconds is not an integer, is {}".format(milliseconds, type(milliseconds)))
    return milliseconds / 1000


def to_textgrid_time(timestamp, split_char="."):
    """
    FIXME: deprecate
    Output needs to be in mili seconds, round to 2

    Args:
        timestamp(str)
    Returns 
    """
    if not isinstance(timestamp, str):
        log.debug("Converting timestamp {} to string".format(timestamp))
        timestamp = str(timestamp)
    time, ms = timestamp.split(split_char)
    hours, mins, secs = [float(i) for i in time.split(":")]
    fulltime = (hours * 3600000) + (mins * 60000) + (secs * 1000) + float(ms)
    fulltime = fulltime / 1000
    return fulltime

TEXTGRID_HEADER = """
File type = "ooTextFile"
Object class = "TextGrid"
"""

def to_short_textgrid(tier_dict):
    """
    """
    return 1


def collect_chunk_values(input_dict, key, strict=True):
    """
    Collect all values associated with chunks in input_dict.

    Args:
        input_dict(dict): {chunk_id: {key: value}}
        key(str)
        strict(Bool): if True, will error out if `key` not present
    Returns:
        list of results
    """
    results = [] 
    for input_key, values in input_dict.items():
        result = values.get(key, "NOT FOUND")
        if strict and result == "NOT FOUND":
            raise KeyError("Key '{}' not found, has {}".format(key, values.keys()))
        results.append(result)
    return results




def to_long_textgrid(tier_dict, tier_key="speaker_name", tier_class="IntervalTier"):
    """
    Create long form TextGrid, cf specs here:http://www.fon.hum.uva.nl/praat/manual/TextGrid_file_formats.html.

    Args:
        tier_dict(dict): 
        tier_key(str) :  
        tier_class(str) :  tier class to use for TextGrid
    Returns:
        str of TextGrid 
    """
    tier_names = set(collect_chunk_values(tier_dict, tier_key))
    tier_times = collect_chunk_values(tier_dict, "start") + collect_chunk_values(tier_dict, "end")
    tier_data = list(tier_dict.values())
    # make the file header 
    file_header = "File type = \"ooTextFile\"\nObject class = \"TextGrid\"\n"
    file_min = "xmin = {}".format(min(tier_times))
    file_max = "xmax = {}".format(max(tier_times))
    file_tiers_flag = "tiers? <exists>"
    file_size = "size = {}".format(len(tier_names))
    file_item = "item []:"
    file_str = "\n".join([file_header, file_min, file_max, file_tiers_flag, file_size, file_item])
    tiers = []
    # note that the content is == as the short version, only we do the string formatting
    for ind, name in enumerate(sorted(tier_names, reverse=True)):
        name_data = [i for i in tier_data if i[tier_key] == name] 
        name_data_sorted = sorted(name_data, key = lambda x: x["start"])
        log.debug("{} items found for tier name '{}'".format(len(name_data), name))
        # make the header over intervals
        tier_header = "\titem [{}]:".format(ind + 1)
        tier_metadata =  "\t\tclass = \"{}\"".format(tier_class)
        tier_name = "\t\tname = \"{}\"".format(name)
        tier_min = "\t\txmin = {}".format(min([val["start"] for val in name_data_sorted]))
        tier_max = "\t\txmax = {}".format(max([val["end"] for val in name_data_sorted]))
        n_tier_intervals = "\t\tintervals: size = {}\n".format(len(name_data_sorted))
        tier_intro = "\n".join([tier_header, tier_metadata, tier_name, tier_min, tier_max, n_tier_intervals])
        # make the intervals
        tier_intervals = []
        for ind, interval in enumerate(name_data_sorted): 
            #FIXME the tabs might go into {}
            interval_header = "\t\t\tintervals [{}]:".format(ind + 1)
            interval_min = "\t\t\t\txmin = {}".format(interval["start"])
            interval_max = "\t\t\t\txmax = {}".format(interval["end"])
            interval_text = "\t\t\t\ttext = \"{}\"".format(interval["text"])
            interval_str = "\n".join([interval_header, interval_min, interval_max, interval_text])
            tier_intervals.append(interval_str)
        tiers = tiers + [tier_intro + "\n".join(tier_intervals)]
    return "\n".join([file_str, "\n".join(tiers)]) 

from textgrid_convert.ParserABC import ParserABC
import copy
import json
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def parse_revstamp(timestamp):
    """
    Convert timestamp from rev format (00:00:20,000) to ms

    Args:
        timestamp(str):
    Returns:
        int
    """
    hrs, mins, rest = timestamp.split(":")
    hrs, mins = int(hrs), int(mins) 
    secs, ms = [int(i) for i in rest.split(",")]
    fulltime = (hrs * 3600000) + (mins * 60000) + (secs * 1000) + ms
    fulltime = int(fulltime)
    assert isinstance(fulltime, int)
    return fulltime


class revParser(ParserABC):
    """
    Class to parse revfiles as defined here: https://www.rev.com/api/attachmentsgetcontent
    Attributes:
        speakers
    """
    speakers = () # pull info rom Rev JSON here


    def __init__(self, transcription, unique_id=None):
        """
        Initializer

        Args:
            transcription(str); transcription text
            unique_id(str): optional
        """
        self.transcription = transcription
        self.transcription_dict = {}
        self.parse_transcription(transcription)
        if unique_id is not None:
            self.unique_id=unique_id


    def parse_timestamp(self, timestamp):
        """
        Convert from rev timestamps to ms
        Args:
            timestamp(str): timestamp
        Returns:
            int of milliseconds
        """
        return parse_revstamp(timestamp)

    def parse_rev_monologues(self, monologues, chunk_id=1):
        """
        Parse clunky monologues into dict

        Args:
            monologues(iterable): list of dicts, as present in rev outout
            chunk_id (int): starting integer for chunk IDs, defaults to 1
        Returns:
            dictionary to be used for self.transcription_dict
        """
        chunk_id = 1
        mono_dict = {}
        log.debug("Found %s monologues", len(monologues))
        for mono in monologues:
            speaker_name, speaker_id = mono.get("speaker_name"), mono.get("speaker_id")
            utterances = [i for i in mono["elements"] if i["type"] == "text" and all((i.get("timestamp"), i.get("end_timestamp")))]
            log.debug("Found {} utterances".format(len(utterances)))
            for utter in utterances:
                mono_dict[chunk_id] = {}
                mono_dict[chunk_id]["speaker_name"], mono_dict[chunk_id]["speaker"] = speaker_name, speaker_id
                mono_dict[chunk_id]["text"] = utter["value"]
                mono_dict[chunk_id]["start"] = self.parse_timestamp(utter["timestamp"])
                mono_dict[chunk_id]["end"] = self.parse_timestamp(utter["end_timestamp"])
                chunk_id += 1
        return mono_dict

    def parse_transcription(self, speaker=None):
        """
        Read rev transcription into dict. Specs are here: https://www.rev.com/api/attachmentsgetcontent
        Args:
            speaker(str, optional): 
        """
        try:
            input_dict = json.loads(self.transcription)
        except json.decoder.JSONDecodeError as err:
            log.critical("Input transcription to revParser '%s' cannot be parsed as JSON" %self.unique_id) 
            raise err
        self.speakers = [(i["id"], i["name"]) for i in input_dict["speakers"]]
        monologues = input_dict["monologues"]
        monologue_dict = self.parse_rev_monologues(monologues)
        self.transcription_dict=monologue_dict
        return monologue_dict

    def to_darla_textgrid(self, speaker_id=None, alias="sentence"):
        """
        Change TextGrid to the format DARLA understands: only "sentence" grids

        Args:
            speaker_id (int):  ID of the speaker to keep, will default to first found
            alias (str): name of output tier, defaults to 'sentence' as required by DARLA
        Returns:
            str to be fed into DARLA
        """
        if not self.transcription_dict:
            log.debug("Running parse_transcription for %s" %self.unique_id)
            self.parse_transcription()
        if speaker_id is not None:
            if speaker_id not in [speaker_id for speaker_id, speaker_name in self.speakers]:
                raise ValueError("Speaker ID '{}' not found in set of speakers {}".format(speaker_id, self.speakers))
            _ , speaker_name = [(i, n) for i, n in self.speakers if i == speaker_id][0]
        else:
            speaker_id, speaker_name = self.speakers[0]
        log.debug("Speaker name set to '%s'" %speaker_name)
        darla_dict = copy.deepcopy(self.transcription_dict)
        output_dict = {k:v for k,v in darla_dict.items() if v["speaker_name"] == speaker_name}
        log.debug("Transcription dict going into DARLA has {} items".format(len(darla_dict)))
        log.debug("Setting tier name to '%s'" %alias)
        for key, values in darla_dict.items():
            output_dict[key] = values
            output_dict[key]["speaker_name"]  = alias
        textgrid = self.to_textgrid(output_dict, speaker_name="IO")
        return textgrid


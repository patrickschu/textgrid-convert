# read revfiles as defined here: https://www.rev.com/api/attachmentsgetcontent
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
    """
    hrs, mins, rest = timestamp.split(":")
    hrs, mins = int(hrs), int(mins) 
    secs, ms = [int(i) for i in rest.split(",")]
    fulltime = (hrs * 3600000) + (mins * 60000) + (secs * 1000) + ms
    fulltime = int(fulltime)
    assert isinstance(fulltime, int)
    return fulltime

TESTDICT = {0: {"speaker_name": "Mary", "text": "one", "start": 0, "end": 0.5896534423132239},
            1: {"speaker_name": "Mary", "text": "",  "end": 1.4123177579131596,"start": 0.5896534423132239},
            2: {"speaker_name": "Mary", "text": "two",  "end": 2.343227378197297, "start": 1.4123177579131596},
            3: {"speaker_name": "Mary", "text": "three",  "end": 3.1225935719235522, "start": 2.343227378197297},
            4: {"speaker_name": "Mary", "start": 3.1225935719235522, "end": 12.804852607709751, "text": "rest of the text * @ " 
               },
            5: {"speaker_name": "John", "start": 0, "end": 12.804852607709751, "text": "" }}


class revParser(ParserABC):
    """
        # transcription dict is formatted like so: {chunk_id(int): {"speaker_name": "", "text": "", "start": float, "end": float}}
    """
    speakers = () # pull info rom Rev JSON here

    def __init__(self, transcription):
        # raw transcript str
        self.transcription = transcription
        # chopped up to convert to other format
        self.transcription_dict = self.parse_transcription(transcription)


    def parse_timestamp(self, timestamp):
        """
        Convert from rev timestamps to ms
        """
        return parse_revstamp(timestamp)

    def parse_transcription(self, speaker=None):
        """
        Specs are here: https://www.rev.com/api/attachmentsgetcontent
        """
        transcription_dict = {}
        try:
            input_dict = json.loads(self.transcription)
        except json.decoder.JSONDecodeError as err:
            log.critical("Input transcription to revParser '%s' cannot be parsed as JSON" %self.unique_id) 
            raise err
        #FIXME make this a separate parsing step
        self.speakers = [(i["id"], i["name"]) for i in input_dict["speakers"]]
        monologues = input_dict["monologues"]
        chunk_id = 1
        for mono in monologues:
            speaker_name, speaker_id = mono.get("speaker_name"), mono.get("speaker_id")
            utterances = [i for i in mono["elements"] if i["type"] == "text" and all((i.get("timestamp"), i.get("end_timestamp")))]
            log.debug("Found {} utterances".format(len(utterances)))
            for utter in utterances:
                transcription_dict[chunk_id] = {}
                transcription_dict[chunk_id]["speaker_name"], transcription_dict[chunk_id]["speaker"] = speaker_name, speaker_id
                transcription_dict[chunk_id]["text"] = utter["value"]
                transcription_dict[chunk_id]["start"] = self.parse_timestamp(utter["timestamp"])
                transcription_dict[chunk_id]["end"] = self.parse_timestamp(utter["end_timestamp"])
                chunk_id += 1
        self.transcription_dict = copy.deepcopy(transcription_dict)
        return copy.deepcopy(transcription_dict)

    def to_darla_textgrid(self, speaker_id=None, alias="sentence"):
        """
        Change TextGrid to the format DARLA understands: only "sentence" grids
        Args:
            speaker_id (int):  ID of the speaker to keep, will default to first found
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
            print(key, values)
            print("l;")
            output_dict[key] = values
            output_dict[key]["speaker_name"]  = alias
        print("ouy", output_dict)
        textgrid = self.to_textgrid(output_dict, speaker_name="IO")
        return textgrid


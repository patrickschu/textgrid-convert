# read revfiles as defined here: https://www.rev.com/api/attachmentsgetcontent
from textgrid_convert.ParserABC import ParserABC
import copy
import json
import logging

log = logging.getLogger(__name__)


def parse_revstamp(timestamp):
    """
    Convert timestamp from rev format (00:00:20,000) to ms
    """
    hrs, mins, rest = timestamp.split(":")
    hrs, mins = float(hrs), float(mins) 
    secs, ms = [float(i) for i in rest.split(",")]
    fulltime = (hrs * 3600000) + (mins * 60000) + (secs * 1000) + ms
    assert isinstance(fulltime, float)
    fulltime = int(fulltime)
    return fulltime



class revParser(ParserABC):
    """
        # transcription dict is formatted like so: {chunk_id(int): {"speaker_name": "", "text": "", "start": float, "end": float}}
    """

    def parse_timestamp(self, timestamp):
        """
        Convert from rev timestamps to ms
        """
        return parse_revstamp(timestamp)

    def parse_transcription(self):
        """
        Specs are here: https://www.rev.com/api/attachmentsgetcontent
        """
        transcription_dict = {}
        try:
            transcript_dict = json.loads(self.transcription)
        except json.decoder.JSONDecodeError as err:
            log.critical("Input transcription to revParser '%s' cannot be parsed as JSON" %self.unique_id) 
            raise err
        monologues = transcript_dict["monologues"]
        chunk_id = 1
        for mono in monologues:
            speaker_name, speaker_id = mono.get("speaker_name"), mono.get("speaker_id")
            utterances = [i for i in mono["elements"] if i["type"] == "text" and all((i.get("timestamp"), i.get("end_timestamp")))]
            log.debug("Found {} utterances".format(len(utterances)))
            for utter in utterances:
                transcription_dict[chunk_id] = {}
                transcription_dict[chunk_id]["speaker_name"], transcription_dict[chunk_id]["speaker"] = speaker_name, speaker_id
                transcription_dict[chunk_id]["text"] = utter["value"]
                transcription_dict[chunk_id]["start"] = utter["timestamp"]
                transcription_dict[chunk_id]["end"] = utter["end_timestamp"]
                chunk_id += 1
        self.transcription_dict = copy.deepcopy(transcription_dict)
        return transcription_dict




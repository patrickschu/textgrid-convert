# read the sbv stuff in; assign timestamp to text
# {id : "chunk", "start", "end"
# expected out: 26 	 Carrie: 	 [78.28] 	 (pause 5.83) 	 [84.10]
import re
import logging
from textgrid_convert.ParserABC import ParserABC
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
#log.setLevel(logging.DEBUG)

class sbvParser(ParserABC):
    """
    Read and parse an sbv formatted file
    Inofficial specs here: GGL 

    Attributes:
        file_name(optional)
        sbv_text(str)
    """
    def __init__(self, transcription):
        """
        Initializer

        Args:
            str_text(str)
        """
        self.transcription = transcription
        self.transcription_dict = {}
        self.parse_transcription(transcription)

    def parse_timestamp(self, timestamp):
        """
        Convert timestamps from sbv format 0:00:00.599 to ms
        """
        hrs, mins, rest = timestamp.split(":")
        hrs, mins = int(hrs), int(mins)
        secs, ms = [int(i) for i in rest.split(".")]
        fulltime = (hrs * 3600000) + (mins * 60000) + (secs * 1000) + ms
        assert isinstance(fulltime, int)
        return fulltime

    # FIXME: re compile
    def sbv_textparse(self, speaker_and_text, speaker="Speaker 1", speaker_regex=re.compile("[A-Z]+:")):
        """
        Args:
            speaker_and_text(str)
        Returns:
            tuple (SPEAKER(str), text(str))
        """
        raw_text = speaker_and_text.lstrip(">")
        new_speaker = speaker_regex.search(raw_text.lstrip())
        if new_speaker: 
            speaker = new_speaker.group()
        text = re.sub("^" + speaker, "", raw_text)
        text = text.strip()
        return speaker.rstrip(":"), text


    def parse_transcription(self, transcription, time_stamp_sep=","):
        """
        Pull the stuff from sbv into a dictionary of format {chunk_id: {
        "speaker": str, 
        "text": str, 
        "start": int, 
        "end": int}}

        Args:
            transcription(str) : 
            time_stamp_sep (str) : 
        Returns:
            dict as described above
        """
        chunk_id = 0
        for timestamps, speaker_and_text in self.sbv_generator(self.transcription.splitlines(), separator=""):
            start, end = timestamps.split(time_stamp_sep)
            previous_entry = self.transcription_dict.get(chunk_id, {"speaker_name": "Speaker 1"})
            speaker, text = self.sbv_textparse(speaker_and_text, speaker=previous_entry["speaker_name"])
            chunk_id += 1
            self.transcription_dict[chunk_id] = {
                    "speaker_name": speaker,
                    "start": self.parse_timestamp(start),  
                    "end": self.parse_timestamp(end),  
                    "text": text}
            log.debug("Added %s for chunk %s" %(self.transcription_dict[chunk_id], chunk_id))
        return self.transcription_dict.copy()

    def sbv_generator(self, filein, separator=""):
        """
        Args:
            filein(file read object or other iterable)
            separator(str): separator between records
        Returns:
            generator over chunk_id, timestamp, text
            FIXME: deque here
        """
        count = 0
        output = ()
        for line in filein:
            count +=1
            output = output + (line, )
            if count % 3 == 0:
                yield output[:-1]
                output = ()
        log.debug("sbv generator processed {} lines from {}".format(count, filein[:100]))


    def to_darla_textgrid(self, speaker_id=None, speaker_name=None, alias="sentence"):
        """
        Change TextGrid to the format DARLA understands: only "sentence" grids

        Args:
            speaker_id(int): NA for sbvs
            speaker_name(str): name of the speaker to extact
            alias: the name to use for texttier -- DARLA wants 'sentence'
        Returns:
            str to be fed into DARLA
        """
        if not self.transcription_dict:
            log.debug("Running parse_transcription for %s" %self.unique_id)
            self.parse_transcription()
        darla_dict = dict(self.transcription_dict)
        output_dict = dict(darla_dict)
        if speaker_name is not None:
            log.debug("Speaker name set to '%s'" %speaker_name)
            output_dict = {k:v for k,v in output_dict.items() if v["speaker_name"] == speaker_name}
            if not output_dict:
                existing_speakers = {v["speaker_name"] for k,v in output_dict.items()}
                raise ValueError("Speaker name '{}' not found in set of speakers '{}'".format(speaker_name, set(existing_speakers)))
        log.debug("Transcription dict going into DARLA has {} items".format(len(darla_dict)))
        log.debug("Setting tier name to '%s'" %alias)
        for key, values in darla_dict.items():
            output_dict[key] = values
            output_dict[key]["speaker_name"]  = alias
        textgrid = self.to_textgrid(output_dict, speaker_name="IO")
        return textgrid


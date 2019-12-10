# read the sbv stuff in; assign timestamp to text
# {id : "chunk", "start", "end"
# expected out: 26 	 Carrie: 	 [78.28] 	 (pause 5.83) 	 [84.10]
import re
import logging
from textgrid_convert.ParserABC import ParserABC
from textgrid_convert import textgridtools as tgtools 
from textgrid_convert import preproctools as pptools
log = logging.getLogger(__name__)

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
        self.parsed_sbv={}# containing sbv content

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
        Returns tuple (SPEAKER(str), text(str))
        """
        raw_text = speaker_and_text.lstrip(">")
        new_speaker = speaker_regex.search(raw_text.lstrip())
        if new_speaker: 
            speaker = new_speaker.group()
        text = re.sub("^" + speaker, "", raw_text)
        text = text.strip()
        return speaker.rstrip(":"), text


    def parse_transcription(self, sbv_text=None, time_stamp_sep=","):
        """
        Pull the stuff from sbv into a dictionary of format {chunk_id: {
        "speaker": str, 
        "text": str, 
        "start": int, 
        "end": int}}
        Args:
        Returns:
            dict as described above
        """
        chunk_id = 0
        if not sbv_text:
            sbv_text = self.raw_sbv
        for timestamps, speaker_and_text in self.sbv_generator(sbv_text.splitlines(), separator=""):
            start, end = timestamps.split(time_stamp_sep)
            previous_entry = self.parsed_sbv.get(chunk_id, {"speaker_name": "Speaker 1"})
            speaker, text = self.sbv_textparse(speaker_and_text, speaker=previous_entry["speaker_name"])
            chunk_id += 1
            self.parsed_sbv[chunk_id] = {
                    "speaker_name": speaker,
                    "start": start,  
                    "end": end,  
                    "text": text}
        return self.parsed_sbv.copy()

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
            #print("l", line)
            count +=1
            output = output + (line, )
            if count % 3 == 0:
                #print("out", output[:-1])
                yield output[:-1]
                output = ()
        log.debug("sbv generator processed {} lines from {}".format(count, filein))

# read the srt stuff in; assign timestamp to text
# {id : "chunk", "start", "end"
# expected out: 26 	 Carrie: 	 [78.28] 	 (pause 5.83) 	 [84.10]
import logging
import copy
from textgrid_convert.ParserABC import ParserABC

log = logging.getLogger(__name__)

class srtParser(ParserABC):
    """
    Read and parse an srt formatted file
    Inofficial specs here: http://forum.doom9.org/showthread.php?p=470941#post470941

    Attributes:
        file_name(optional)
        srt_text(str)
    """

    def __init__(self, transcription, unique_id=None):
        """
        Initializer

        Args:
            str_text(str)
        """
        self.transcription = transcription
        self.transcription_dict = {}
        self.parse_transcription(transcription)
        if unique_id is not None:
            self.unique_id=unique_id


    def parse_timestamp(self, timestamp):
        """
        Convert from srt style timestamp 00:59:58,89 to ms

        Args:
            timestamp(str)
        Return:
            int
        """
        time, ms = timestamp.split(",")
        hrs, mins, secs = [int(i) for i in time.split(":")]
        fulltime = (hrs * 3600000) + (mins * 60000) + (secs * 1000) + int(ms)
        return fulltime


    def parse_transcription(self, srt_text=None, speaker_name="Speaker 1", time_stamp_sep=" --> "):
        """
        Pull the stuff from srt into a dictionary of format {chunk_id: {"text": "", "start": int, "end": int}}

        Args:
            srt_text(str): 
            speaker_name(str): 
            time_stamp_sep(str): placeholder between start and end time stamp
        Returns:
            dict as described above
        """
        if not srt_text:
            srt_text = self.transcription
        for chunk_id, timestamps, text in self.srt_generator(srt_text.splitlines(), separator=""):
            start, end = timestamps.split(time_stamp_sep)
            self.transcription_dict[chunk_id] = {
                    "speaker_name": speaker_name,
                    "start": self.parse_timestamp(start),
                    "end": self.parse_timestamp(end),
                    "text": text}
        return copy.deepcopy(self.transcription_dict)

    def srt_generator(self, filein, separator="\n"):
        """
        Args:
            filein(file read object or other iterable)
            separator(str): separator between records
        Returns:
            generator over chunk_id, timestamp, text
        """
        count = 0
        output = ()
        for line in filein:
            count +=1
            output = output + (line, )
            if count % 4 == 0:
                yield output[:-1]
                output = ()
        log.debug("srt generator processed {} lines from {}".format(count, filein))

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
        textgrid = self.to_textgrid(output_dict)
        return textgrid

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
    def __init__(self, transcription):
        """
        Initializer
        Args:
            str_text(str)
        """
        self.transcription = transcription


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
        Returns:
            dict as described above
        """
        if not srt_text:
            srt_text = self.raw_srt
        for chunk_id, timestamps, text in self.srt_generator(srt_text.splitlines(), separator=""):
            start, end = timestamps.split(time_stamp_sep)
            self.transcription_dict[chunk_id] = {
                    "speaker_name": speaker_name,
                    "start": start,
                    "end": end,
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
            #print("l", line)
            count +=1
            output = output + (line, )
            if count % 4 == 0:
                #print("out", output[:-1])
                yield output[:-1]
                output = ()
        log.debug("srt generator processed {} lines from {}".format(count, filein))

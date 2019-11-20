# read the srt stuff in; assign timestamp to text
# {id : "chunk", "start", "end"
# expected out: 26 	 Carrie: 	 [78.28] 	 (pause 5.83) 	 [84.10]
import logging
log = logging.getLogger(__name__)

class srtParser(object):
    """
    Read and parse an srt formatted file
    Inofficial specs here: http://forum.doom9.org/showthread.php?p=470941#post470941
    Attributes:
        file_name(optional)
        srt_text(str)
    """
    def __init__(self, srt_text):
        """
        Initializer
        Args:
            str_text(str)
        """
        self.raw_srt=srt_text
        self.parsed_srt= {}# containing srt content

    def _to_textgrid_time(self, timestamp):
        """
        Output needs to be in mili seconds, round to 2
        Args:
        00:52:58,579            timestamp (str)
        Returns 
        """
        if not isinstance(timestamp, str):
            timestamp = str(timestamp)
        time, ms = timestamp.split(",")
        hours, mins, secs = [float(i) for i in time.split(":")]
        fulltime = (hours * 3600000) + (mins * 60000) + (secs * 1000) + float(ms)
        return fulltime

    def to_textgrid(self, speaker_name="Speaker1"):
        """
        Convert to Praat Textgrid format
        "Specs" here: http://www.fon.hum.uva.nl/praat/manual/Intro_7__Annotation.html
        Time needs to be secs.milisecs, round to 2
        Returns:
            TextGrid compatible string

        """
        if len(self.parsed_srt) < 1:
            self.parse_srt()
        textgrid = []
        intro_template = "{}     {}      "
        time_template = "[{}]    {}      [{}]"
        for chunk_id, values in self.parsed_srt.items():
            # NUMBER\s\t\sSPEAKER\s\t\s[start]\s\tTEXT\s\t\s[end]\n 
            intro = intro_template.format(chunk_id, speaker_name)
            start_time, end_time = self._to_textgrid_time(values["start"]), self._to_textgrid_time(values["end"]) 
            time = time_template.format(start_time, values["text"], end_time)
            textgrid.append(intro + time)
        assert len(textgrid) == len(self.parsed_srt), "make sure all items from parsed dictionary end up in list"
        # FIXME this line sep
        return "\n".join(textgrid) 


    def parse_srt(self, srt_text=None, time_stamp_sep=" --> "):
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
            self.parsed_srt[chunk_id] = {
                    "start": start,  
                    "end": end,  
                    "text": text}
        return self.parsed_srt.copy()

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

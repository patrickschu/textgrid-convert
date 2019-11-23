# modeled on sbvParser
# read the sbv stuff in; assign timestamp to text
# {id : "chunk", "start", "end"
# expected out: 26 	 Carrie: 	 [78.28] 	 (pause 5.83) 	 [84.10]
import re
import logging
log = logging.getLogger(__name__)

class sbvParser(object):
    """
    Read and parse an sbv formatted file
    Inofficial specs here: GGL 
    Attributes:
        file_name(optional)
        sbv_text(str)
    """
    def __init__(self, sbv_text):
        """
        Initializer
        Args:
            str_text(str)
        """
        self.raw_sbv=sbv_text
        self.parsed_sbv={}# containing sbv content

    def _to_textgrid_time(self, timestamp):
        """
        Output needs to be in mili seconds, round to 2
        Args:
        00:52:58,579            timestamp (str)
        Returns 
        """
        if not isinstance(timestamp, str):
            log.debug("Converting timestamp {} to string".format(timestamp))
            timestamp = str(timestamp)
        time, ms = timestamp.split(".")
        hours, mins, secs = [float(i) for i in time.split(":")]
        fulltime = (hours * 3600000) + (mins * 60000) + (secs * 1000) + float(ms)
        fulltime = fulltime / 1000
        return fulltime

    def from_file(self, input_file):
        """
        Read from `input_file` and parse into sbvParser
        """
        return

    def to_textgrid(self, output_file=None, speaker_name="Speaker1"):
        """
        FIXME: add output_file
        Convert to Praat Textgrid format
        "Specs" here: http://www.fon.hum.uva.nl/praat/manual/Intro_7__Annotation.html
        Time needs to be secs.milisecs, round to 2
        Returns:
            TextGrid compatible string

        """
        if len(self.parsed_sbv) < 1:
            self.parse_sbv()
        textgrid = []
#ur Celsius value is {:0.2f}ºC.\n".format(answer)
        intro_template = "{}     {}:      "
        # add formatting for round to 2 decimals
        time_template = "[{:0.2f}]    {}      [{:0.2f}]"
        for chunk_id, values in self.parsed_sbv.items():
            # NUMBER\s\t\sSPEAKER\s\t\s[start]\s\tTEXT\s\t\s[end]\n 
            intro = intro_template.format(chunk_id, values["speaker_name"])
            start_time, end_time = self._to_textgrid_time(values["start"]), self._to_textgrid_time(values["end"]) 
            time = time_template.format(start_time, values["text"], end_time)
            textgrid.append(intro + time)
        assert len(textgrid) == len(self.parsed_sbv), "make sure all items from parsed dictionary end up in list"
        # FIXME this line sep
        if output_file:
            raise NotImplementedError("output_file not implemented")
        return "\n".join(textgrid) 

    # FIXME: re compile
    def sbv_textparse(self, speaker_and_text, speaker="Speaker 1", speaker_regex=re.compile("[A-Z]+:")):
        """
        Args:
            speaker_and_text(str)
        Returns tuple (SPEAKER(str), text(str))
        """
        raw_text = speaker_and_text.lstrip(">")
        new_speaker = speaker_regex.search(raw_text.lstrip())
        print("here is inpur speaker", speaker)
        if new_speaker: 
            speaker = new_speaker.group()
        text = raw_text.strip().lstrip(speaker)
        print("here is output speaker", speaker)
        return speaker.rstrip(":"), text


    def parse_sbv(self, sbv_text=None, time_stamp_sep=","):
        """
        Pull the stuff from sbv into a dictionary of format {chunk_id: {"text": "", "start": int, "end": int}}
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

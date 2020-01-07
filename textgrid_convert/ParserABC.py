"""
Abstract Base class for implementing transcription parsers
"""
import abc
from textgrid_convert import textgridtools as tgtools
from textgrid_convert import preproctools as pptools
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class ParserABC(metaclass=abc.ABCMeta):
    """
    Abstract base class for Parsers to feed textgrid conversion
    """
    unique_id = None
    transcription = None
    transcription_dict = None
    # transcription dict is formatted like so: {chunk_id(int): {"speaker_name": "", "text": "", "start": float, "end": float}}


    @abc.abstractmethod
    def parse_timestamp(self, timestamp):
        """
        Convert timestamp to int

        Args:
            timestamp(str)
        Returns:
            timestamp in milliseconds
        """

    @abc.abstractmethod
    def parse_transcription(self, transcription):
        """
        Convert transcription input to transcription dictionary

        Args:
            transcription(str)
        Returns:
            dict
        """

    def to_textgrid(self, input_dict=None, output_file=None, speaker_name="Speaker1", adapt_endstamps=0.001):
        """
        FIXME: add output_file
        Convert internal dict to Praat Textgrid format
        "Specs" here: http://www.fon.hum.uva.nl/praat/manual/Intro_7__Annotation.html
        Time needs to be secs.milisecs, round to 2

        Args:
            speaker_name (str)
            adapt_endstamps(float): if given, will adapt end stamps to < start stamp
        Returns:
            TextGrid compatible string
        """
        textgrid_dict = {}
        if input_dict is None:
            input_dict = self.transcription_dict
        # if not given or empty, default to self.transcription_dict`
        if len(input_dict) < 1:
            log.debug("No transcription dict found, running parse_transcription()")
            self.parse_transcription(self.transcription)
            input_dict = self.transcription_dict
        log.debug("Input dict has %s items" %len(input_dict))
        for chunk, values in input_dict.items():
            # FIXME: maybe this needs to be a parser implemented method
            start, end = values["start"], values["end"]
            textgrid_dict[chunk] = values
            textgrid_dict[chunk]["start"], textgrid_dict[chunk]["end"] = tgtools.ms_to_textgrid(start),  tgtools.ms_to_textgrid(end)
        # fix timestamp overlaps
        if adapt_endstamps:
            log.debug("Adapting end stamps with gap %f" %adapt_endstamps)
            textgrid_dict = pptools.adapt_timestamps(textgrid_dict, gap=adapt_endstamps)
        # FIXME this should be flexible in regards to long or short output format
        textgrid = tgtools.to_long_textgrid(tier_dict=textgrid_dict)
        return textgrid

    @classmethod
    def from_file(cls, input_path):
        """
        Read file from disk

        Args:
            input_path(str): path to transcription file to read
        Returns:
            initialized class
        """
        with open(input_path, "r", encoding="utf-8") as transcriptin:
            transcript = transcriptin.read()
        return cls(transcript, unique_id=input_path)

    def to_file(self):
        """
        Write file to disk
        """
        raise NotImplementedError("")



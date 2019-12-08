# Abstract Base class for implementing transcription parsers
from abc import ABC, abstractmethod
import uuid

TESTDICT = {0: {"speaker_name": "Mary", "text": "one", "start": 0, "end": 0.5896534423132239},
            1: {"speaker_name": "Mary", "text": "",  "end": 1.4123177579131596,"start": 0.5896534423132239},
            2: {"speaker_name": "Mary", "text": "two",  "end": 2.343227378197297, "start": 1.4123177579131596},
            3: {"speaker_name": "Mary", "text": "three",  "end": 3.1225935719235522, "start": 2.343227378197297},
            4: {"speaker_name": "Mary", "start": 3.1225935719235522, "end": 12.804852607709751, "text": "rest of the text * @ " 
               },
            5: {"speaker_name": "John", "start": 0, "end": 12.804852607709751, "text": "" }}

class ParserABC(ABC):
    """
    Abstract base class for Parsers to feed textgrid conversion
    """
    def __init__(self, transcription, unique_id=None):
        """
        """
        self.unique_id = uuid.uuid5() if unique_id is None else unique_id 
        # transcription dict is formatted like so: {chunk_id(int): {"speaker_name": "", "text": "", "start": float, "end": float}}
        self.transcription_dict = {}
    
    @abstractmethod
    def parse_transcription(self, transcription):
        """
        """
        pass

    def to_textgrid(self):
        """
        This should be consistent across all parsers
        """
        return 1

    def from_file(self):
        """
        """
        pass

    def to_file(self):
        """
        """
        pass



# test revParser
import re
import json
import pathlib
import pytest
from textgrid_convert.revParser import revParser


HERE = pathlib.Path(__file__).parent
RESOURCES = HERE / "resources"
JSON_IN = RESOURCES / "rev_sample.json"


def test_init():
    """
    """
    rr = revParser("")
    rr = revParser("dummytext", "ID")
    assert rr.unique_id == "ID"
    assert rr.transcription == "dummytext"


def test_json_read():
    """
    """
    with open(str(JSON_IN), "r", encoding="utf-8") as jsonin:
        text = jsonin.read()
    dicti = json.loads(text)
    rr = revParser(text)
    rr.parse_transcription()
    assert len(rr.transcription_dict) == 2
    with pytest.raises(json.decoder.JSONDecodeError):
        rr = revParser("DUMMY")
        rr.parse_transcription()


def test_to_txtgrid():
    """
    """
    with open(str(JSON_IN), "r", encoding="utf-8") as jsonin:
        text = jsonin.read()
    dicti = json.loads(text)
    rr = revParser(text)
    rr.parse_transcription()
    res = rr.to_textgrid()
    print(res)



if __name__ == "__main__":
   test_json_read()
   test_init()
   test_to_txtgrid()

# test revParser
import re
import json
import pathlib
import pytest
from textgrid_convert.revParser import revParser
from globals import INFILES_JSON, OUTFILES


ONE_SPEAKER = INFILES_JSON / "rev_sample.json"
TWO_SPEAKER = INFILES_JSON / "rev_sample_two_speakers.json"
JSON_TO_GRID = OUTFILES / "json_to_grid.TextGrid"
JSON_TO_DARLA = OUTFILES / "json_to_darla.TextGrid"

def test_json_read():
    """
    """
    with open(str(ONE_SPEAKER), "r", encoding="utf-8") as jsonin:
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
    with open(str(ONE_SPEAKER), "r", encoding="utf-8") as jsonin:
        text = jsonin.read()
    dicti = json.loads(text)
    rr = revParser(text)
    rr.parse_transcription()
    res = rr.to_textgrid()
    assert isinstance(res, str)
    with open(str(JSON_TO_GRID), "w", encoding="utf-8") as txtgridout:
        txtgridout.write(res)


def test_to_darla_txtgrid():
    """
    """
    with open(str(TWO_SPEAKER), "r", encoding="utf-8") as jsonin:
        text = jsonin.read()
    assert len(text) > 10
    dicti = json.loads(text)
    rr = revParser(text)
    rr.parse_transcription()
    res = rr.to_darla_textgrid(alias="sentence2")
    #assert "sentence2" in res
    assert isinstance(res, str)
    rr = revParser(text)
    rr.parse_transcription()
    res = rr.to_darla_textgrid(speaker_id=2)
    assert isinstance(res, str)
    assert "sentence2" not in res
    with open(str(JSON_TO_DARLA), "w", encoding="utf-8") as txtgridout:
        txtgridout.write(res)
    with pytest.raises(ValueError):
        rr = revParser(text)
        res = rr.to_darla_textgrid(speaker_id=3, alias="sentence")

if __name__ == "__main__":
    test_json_read()
    test_init()
    test_to_txtgrid()
    test_to_darla_txtgrid()

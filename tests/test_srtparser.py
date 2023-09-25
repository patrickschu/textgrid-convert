import pathlib
from textgrid_convert.srtParser import srtParser
from textgrid_convert.textgridtools import merge_text_with_newlines
from globals import INFILES_SRT, OUTFILES

DOWNSUB = INFILES_SRT / "downsub.srt"
SRT_TO_GRID = OUTFILES / "srt_to_grid.TextGrid"
SRT_TO_DARLA = OUTFILES / "srt_to_darla.TextGrid"
NEWLINES = INFILES_SRT / "issue_43.srt"
FULLTEXT_NEWLINES = INFILES_SRT / "issue_43_fulltext.srt"
MISSING_INTERVALS = INFILES_SRT / "issue_44.srt"


def test_class_init():
    """
    """
    intext = "dummy text"
    parser = srtParser(intext)
    assert parser.transcription == intext


def test_timeconvert():
    """
    """
    intext = "00:00:00,579"
    parser = srtParser(intext)
    converted = parser.parse_timestamp(intext)
    assert converted == 579.00
    intext = "00:00:01,579"
    parser = srtParser(intext)
    converted = parser.parse_timestamp(intext)
    assert converted == 1579.00
    intext = "00:01:01,579"
    parser = srtParser(intext)
    converted = parser.parse_timestamp(intext)
    assert converted == 61579.00
    intext = "01:01:01,579"
    parser = srtParser(intext)
    converted = parser.parse_timestamp(intext)
    assert converted == 3661579


def test_srt_parse():
    """
    """
    with open(str(DOWNSUB), "r", encoding="utf-8") as srtin:
        txt = srtin.read()
    parser = srtParser(txt)
    assert len(parser.transcription) == 92551
    # FIXME: does not actually text parsing

def test_textgrid_output():
    """
    """
    with open(str(DOWNSUB), "r", encoding="utf-8") as srtin:
        txt = srtin.read()
    parser = srtParser(txt)
    txtgrid = parser.to_textgrid()
    with open(str(SRT_TO_GRID), "w", encoding="utf-8") as txtgridout:
         txtgridout.write(txtgrid)


def test_to_darla():
    """
    """
    with open(str(DOWNSUB), "r", encoding="utf-8") as srtin:
        txt = srtin.read()
    parser = srtParser(txt)
    txtgrid = parser.to_darla_textgrid()
    with open(str(SRT_TO_DARLA), "w", encoding="utf-8") as srtout:
        srtout.write(txtgrid)

def test_file_with_newlines():
    """
    """
    with open(str(NEWLINES), "r", encoding="utf-8") as srtin:
        txt = srtin.read()
    parser = srtParser(txt, preprocessors=[merge_text_with_newlines])
    txtgrid = parser.to_darla_textgrid()
    parser = srtParser(txt)
    txtgrid = parser.to_darla_textgrid()
    assert len(parser.transcription_dict) == 3
    with open(str(FULLTEXT_NEWLINES), "r", encoding="utf-8") as srtin:
        txt = srtin.read()
    parser = srtParser(txt, preprocessors=[merge_text_with_newlines])
    txtgrid = parser.to_darla_textgrid()
    parser = srtParser(txt)
    txtgrid = parser.to_darla_textgrid()
    assert len(parser.transcription_dict) == 817



def test_file_with_missing_intervals():
    """
    """
    with open(MISSING_INTERVALS, "r", encoding="utf-8") as srtin:
        txt = srtin.read()
        parser = srtParser(txt, preprocessors=[merge_text_with_newlines])
        txtgrid = parser.to_darla_textgrid()
        assert len(parser.transcription_dict) == 2, "should return 2 actual intervals"
        assert parser.transcription_dict["1"]["start"] == 0
        assert parser.transcription_dict["1"]["end"] == 60.473
        assert parser.transcription_dict["2"]["start"] == 120.013
        assert parser.transcription_dict["2"]["end"] == 235.873
        gap_time = parser.transcription_dict["2"]["start"] - parser.transcription_dict["1"]["end"]
        assert round(gap_time, 2) == 59.54


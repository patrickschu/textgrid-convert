import pathlib
from textgrid_convert.sbvParser import sbvParser
from globals import INFILES_SBV, OUTFILES


CAPTIONS = INFILES_SBV / "captions.sbv"
DOWNSUB = INFILES_SBV / "downsub.sbv"
SBV_TO_GRID =  OUTFILES / "sbv_to_grid.TextGrid"
SBV_TO_GRID2 =  OUTFILES / "sbv_to_grid2.TextGrid"
SBV_TO_GRID3 =  OUTFILES / "sbv_to_grid3.TextGrid"

def test_textgrid_output():
    """
    """
    with open(str(DOWNSUB), "r", encoding="utf-8") as sbvin:
        txt = sbvin.read()
    parser = sbvParser(txt)
    print("this is dowbsub")
    txtgrid = parser.to_textgrid()
    with open(str(SBV_TO_GRID), "w", encoding="utf-8") as sbvout:
        sbvout.write(txtgrid)

def test_sbv():
    """
    """
    with open(str(CAPTIONS), "r", encoding="utf-8") as sbvin:
        sbv = sbvin.read()
    parser = sbvParser(sbv)
    print("this is captions")
    txtgrid = parser.to_textgrid()
    with open(str(SBV_TO_GRID2), "w", encoding="utf-8") as sbvout:
        sbvout.write(txtgrid)
    del parser

def test_class_init():
    """
    """
    intext = "dummy text"
    parser = sbvParser(intext)
    assert parser.transcription == intext


def test_timeconvert():
    """
    """
    from textgrid_convert import textgridtools as tgt
    intext = "0:00:00.579"
    parser = sbvParser(intext)
    converted = parser.parse_timestamp(intext)
    converted = tgt.ms_to_textgrid(converted)
    assert converted == 579.00 / 1000
    intext = "0:00:01.579"
    parser = sbvParser(intext)
    converted = parser.parse_timestamp(intext)
    converted = tgt.ms_to_textgrid(converted)
    assert converted == 1579.00 / 1000
    intext = "0:01:01.579"
    parser = sbvParser(intext)
    converted = parser.parse_timestamp(intext)
    converted = tgt.ms_to_textgrid(converted)
    assert converted == 61579.00 / 1000
    intext = "1:01:01.579"
    parser = sbvParser(intext)
    converted = parser.parse_timestamp(intext)
    converted = tgt.ms_to_textgrid(converted)
    assert converted == 3661579.00 / 1000


def test_sbv_parse():
    """
    """
    with open(str(DOWNSUB),  "r", encoding="utf-8") as sbvin:
        txt = sbvin.read()
    parser = sbvParser(txt)
    assert len(parser.transcription) == 267
    # FIXME: does not actually text parsing


def test_captions_textgrid_output():
    """
    """
    with open(str(CAPTIONS), "r", encoding="utf-8") as sbvin:
        txt = sbvin.read()
    parser = sbvParser(txt)
    txtgrid = parser.to_textgrid()
    with open(str(SBV_TO_GRID3), "w", encoding="utf-8") as sbvout:
        sbvout.write(txtgrid)


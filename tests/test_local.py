import pathlib
from textgrid_convert.sbvParser import sbvParser
from textgrid_convert.srtParser import srtParser
from globals import GOLDFILES, OUTFILES

SRT_INPUT = GOLDFILES / "captions1.srt" 
SBV_INPUT = GOLDFILES / "captions1.sbv" 
SRT_OUTPUT = OUTFILES / "captions1.srt_textgrid" 
SBV_OUTPUT = OUTFILES / "captions1.sbv_textgrid" 

def test_srt():
    with open(str(SRT_INPUT), "r", encoding="utf-8") as srtin:
        parser = srtParser(srtin.read())
    res = parser.to_textgrid()
    with open(str(SRT_OUTPUT), "w", encoding="utf-8") as srtout:
        srtout.write(res)


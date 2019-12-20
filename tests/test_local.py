import pathlib
from textgrid_convert.sbvParser import sbvParser
from textgrid_convert.srtParser import srtParser

HERE = pathlib.PurePath(__file__).parent
SRT_INPUT = HERE / "resources" / "gold_files" / "captions1.srt" 
SRT_OUTPUT = HERE / "resources" / "gold_files" / "captions1.srt_textgrid" 
SBV_INPUT = HERE / "resources" / "gold_files" / "captions1.sbv" 
SBV_OUTPUT = HERE / "resources" / "gold_files" / "captions1.sbv_textgrid" 

def test_srt():
    with open(str(SRT_INPUT), "r", encoding="utf-8") as srtin:
        parser = srtParser(srtin.read())
    res = parser.to_textgrid()
    with open(str(SRT_OUTPUT), "w", encoding="utf-8") as srtout:
        srtout.write(res)




def test_sbv():
    return 1

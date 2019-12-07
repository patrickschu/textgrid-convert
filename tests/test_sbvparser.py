import pathlib
from textgrid_convert.sbvParser import sbvParser

HERE = pathlib.Path(__file__).parent
SRT_PATH = HERE / "resources" / "downsub.sbv"
SBV_PATH = HERE / "resources" / "captions.sbv"
LARS_PATH = HERE / "resources" / "lars_captions.sbv"
LARS_OUTPATH = HERE / "lars_captions_textgrid.txt" 
SBV_OUT_PATH = HERE / "txtgrid_sbv.txt"
SBV_OUT_PATH2 = HERE / "captions_sbv.txt"
def test_lars_sbv():
    """
    """
    with open(str(LARS_PATH), "r", encoding="utf-8") as sbvin:
        sbv = sbvin.read()
    parser = sbvParser(sbv)
    txtgrid = parser.to_textgrid()
    with open(str(LARS_OUTPATH), "w", encoding="utf-8") as sbvout:
        sbvout.write(txtgrid)

def test_class_init():
    """
    """
    intext = "dummy text"
    parser = sbvParser(intext)
    assert parser.raw_sbv == intext


def test_timeconvert():
    """
    """
    intext = "0:00:00.579"
    parser = sbvParser(intext)
    converted = parser._to_textgrid_time(intext)
    assert converted == 579.00 / 1000
    intext = "0:00:01.579"
    parser = sbvParser(intext)
    converted = parser._to_textgrid_time(intext)
    assert converted == 1579.00 / 1000
    intext = "0:01:01.579"
    parser = sbvParser(intext)
    converted = parser._to_textgrid_time(intext)
    assert converted == 61579.00 / 1000
    intext = "1:01:01.579"
    parser = sbvParser(intext)
    converted = parser._to_textgrid_time(intext)
    assert converted == 3661579.00 / 1000


def test_sbv_parse():
    """
    """
    with open(str(SRT_PATH),  "r", encoding="utf-8") as sbvin:
        txt = sbvin.read()
    parser = sbvParser(txt)
    assert len(parser.raw_sbv) == 267
    # FIXME: does not actually text parsing

def test_textgrid_output():
    """
    """
    with open(str(SRT_PATH), "r", encoding="utf-8") as sbvin:
        txt = sbvin.read()
    parser = sbvParser(txt)
    txtgrid = parser.to_textgrid()
    with open(str(SBV_OUT_PATH), "w", encoding="utf-8") as sbvout:
        sbvout.write(txtgrid)

def test_captions_textgrid_output():
    """
    """
    with open(SBV_PATH, "r", encoding="utf-8") as sbvin:
        txt = sbvin.read()
    parser = sbvParser(txt)
    txtgrid = parser.to_textgrid()
    with open(str(SBV_OUT_PATH2), "w", encoding="utf-8") as sbvout:
        sbvout.write(txtgrid)

if __name__ == "__main__":
    test_textgrid_output()
    test_captions_textgrid_output()

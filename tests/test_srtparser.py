import pathlib
from textgrid_convert.srtParser import srtParser

HERE = pathlib.Path(__file__).parent
SRT_PATH = HERE / "resources" / "downsub.srt"

def test_class_init():
    """
    """
    intext = "dummy text"
    parser = srtParser(intext)
    assert parser.raw_srt == intext


def test_timeconvert():
    """
    """
    intext = "00:00:00,579"
    parser = srtParser(intext)
    converted = parser._to_textgrid_time(intext)
    assert converted == 579.00
    intext = "00:00:01,579"
    parser = srtParser(intext)
    converted = parser._to_textgrid_time(intext)
    assert converted == 1579.00
    print(converted)
    intext = "00:01:01,579"
    parser = srtParser(intext)
    converted = parser._to_textgrid_time(intext)
    assert converted == 61579.00
    intext = "01:01:01,579"
    parser = srtParser(intext)
    converted = parser._to_textgrid_time(intext)
    assert converted == 3661579.00


def test_srt_parse():
    """
    """
    with open(SRT_PATH, "r", encoding="utf-8") as srtin:
        txt = srtin.read()
    parser = srtParser(txt)
    assert len(parser.raw_srt) == 92551
    # FIXME: does not actually text parsing

def test_textgrid_output():
    """
    """
    with open(SRT_PATH, "r", encoding="utf-8") as srtin:
        txt = srtin.read()
    parser = srtParser(txt)
    txtgrid = parser.to_textgrid()
    with open(HERE / "txtgrid.txt", "w", encoding="utf-8") as txtgridout:
         txtgridout.write(txtgrid)


if __name__ == "__main__":
    test_textgrid_output()
    test_srt_parse()
    test_timeconvert()

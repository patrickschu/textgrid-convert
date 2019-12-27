# test flag parsing and such
import pytest
import pathlib
from textgrid_convert import ArgParser

"""
arg_parser.add_argument("--input_path", "-i", type=str, help="Path to input file or folder")
arg_parser.add_argument("--output_path", "-o", type=str, help="Path to write output file(s) to")
arg_parser.add_argument("--source_format", "--from", "-f", type=str, help="Input format to convert to TextGrid, e.g. sbv or srt")
arg_parser.add_argument("--to", "-t", type=str, help="Output format to convert to, textgrid")
"""
# FIXME add test for to darla here
def test_input_path():
    """
    """
    testpath = "DUMMYPATH"
    flag = "--input_path"
    var = flag.lstrip("--") 
    arg = ArgParser.arg_parser
    res = arg.parse_args([flag, testpath])
    assert vars(res)[var] == testpath
    # abbreviated
    flag = "--in"
    arg = ArgParser.arg_parser
    res = arg.parse_args([flag, testpath])
    assert vars(res)[var] == testpath
    # abbreviated
    flag = "-i"
    arg = ArgParser.arg_parser
    res = arg.parse_args([flag, testpath])
    assert vars(res)[var] == testpath
    with pytest.raises(TypeError):
        res = arg.parse_args([flag, 100])

def test_output_path():
    """
    """
    inflag = "--input_path"
    testpath = "DUMMYPATH"
    flag = "--output_path"
    var = flag.lstrip("--") 
    arg = ArgParser.arg_parser
    res = arg.parse_args([flag, testpath, inflag, testpath])
    assert vars(res)[var] == pathlib.PurePath(testpath)
    # abbreviated
    inflag = "--input_path"
    testpath = "DUMMYPATH"
    flag = "--out"
    arg = ArgParser.arg_parser
    res = arg.parse_args([flag, testpath, inflag, testpath])
    assert vars(res)[var] == pathlib.PurePath(testpath)
    # abbreviated
    flag = "-o"
    arg = ArgParser.arg_parser
    res = arg.parse_args([flag, testpath, inflag, testpath])
    assert vars(res)[var] == pathlib.PurePath(testpath)
    with pytest.raises(TypeError):
        res = arg.parse_args([flag, 100])

def test_from():
    """
    """
    inflag = "--input_path"
    testpath = "DUMMYPATH"
    testformat = "sbv"
    flag = "--source_format"
    var = flag.lstrip("--") 
    arg = ArgParser.arg_parser
    res = arg.parse_args([flag, testformat, inflag, testpath])
    assert vars(res)[var] == testformat
    # abbreviated
    inflag = "--input_path"
    flag = "--from"
    arg = ArgParser.arg_parser
    res = arg.parse_args([flag, testformat, inflag, testpath])
    assert vars(res)[var] == testformat
    # abbreviated
    flag = "-f"
    arg = ArgParser.arg_parser
    res = arg.parse_args([flag, testformat, inflag, testpath])
    assert vars(res)[var] == testformat
    with pytest.raises(TypeError):
        res = arg.parse_args([flag, 100])




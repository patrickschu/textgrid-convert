"""
Expected

textgrid-convert infolder 

textgrid-convert infolder -f srt -t textgrid
textgrid-convert infolder  -f srt -t darla_textgrid

textgrid-convert infolder  


"""
import os
import pathlib
import pytest
from unittest.mock import patch
from textgrid_convert.ArgParser import arg_parser
from textgrid_convert.ttextgrid_convert import main
from globals import INFILES_SRT, INFILES_SBV, INFILES_JSON, MAIN_PATH

CWD = pathlib.PurePath(__file__).parent

@patch("textgrid_convert.ttextgrid_convert.convert_to_txtgrid", autospec=True)
@patch("textgrid_convert.iotools.filewriter", autospec=True)
def test_srt_conversion(mock_writer, mock_convert ):
    """
    """
    infolder = str(INFILES_SRT)
    informat = "srt"
    #args = [infolder, informat, "-t textgrid"]
    args = ["--i", infolder,  "--f", informat, "--t", "textgrid"]
    res = vars(arg_parser.parse_args(args))
    assert res["strict"] is True
    assert res["input_path"] == infolder 
    assert str(res["output_path"]) == str(MAIN_PATH)
    main(**res)
    assert mock_writer.call_count == len(os.listdir(res["input_path"]))
    assert mock_convert.call_count == len(os.listdir(res["input_path"]))
 
@patch("textgrid_convert.ttextgrid_convert.convert_to_txtgrid", autospec=True)
@patch("textgrid_convert.iotools.filewriter", autospec=True)
def test_sbv_conversion(mock_writer, mock_convert ):
    """
    """
    infolder = str(INFILES_SBV)
    informat = "srt"
    args = ["--i", infolder,  "--f", informat, "--t", "textgrid"]
    res = vars(arg_parser.parse_args(args))
    assert all((res["strict"] is True, res["input_path"] == infolder, str(res["output_path"]) == str(MAIN_PATH)))
    with pytest.raises(ValueError):
        main(**res)
    informat = "sbv"
    args = ["--i", infolder,  "--f", informat, "--t", "textgrid"]
    res = vars(arg_parser.parse_args(args))
    main(**res)
    assert mock_writer.call_count == len(os.listdir(res["input_path"]))
    assert mock_convert.call_count == len(os.listdir(res["input_path"]))
 
@patch("textgrid_convert.ttextgrid_convert.convert_to_txtgrid", autospec=True)
@patch("textgrid_convert.iotools.filewriter", autospec=True)
def test_json_conversion(mock_writer, mock_convert ):
    """
    """
    infolder = str(INFILES_JSON)
    informat = "srt"
    args = ["--i", infolder,  "--f", informat, "--t", "textgrid"]
    res = vars(arg_parser.parse_args(args))
    assert res["strict"] is True
    assert res["input_path"] == str(INFILES_JSON)
    assert str(res["output_path"]) == str(MAIN_PATH)
    with pytest.raises(ValueError):
        main(**res)
    informat = "json"
    args = ["--i", infolder,  "--f", informat, "--t", "textgrid"]
    res = vars(arg_parser.parse_args(args))
    main(**res)
    assert mock_writer.call_count == len(os.listdir(res["input_path"]))
    assert mock_convert.call_count == len(os.listdir(res["input_path"]))
 
@patch("textgrid_convert.ttextgrid_convert.convert_to_txtgrid", autospec=True)
@patch("textgrid_convert.iotools.filewriter", autospec=True)
def test_srtXXX_conversion(mock_writer, mock_convert ):
    """
    """
    return 1

# erorr handle here

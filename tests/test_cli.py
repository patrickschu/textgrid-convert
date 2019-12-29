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
from textgrid_convert.ttextgrid_convert import main, guess_source_format
from globals import INFILES_SRT, INFILES_SBV, INFILES_JSON, MAIN_PATH

CWD = pathlib.PurePath(__file__).parent

FORMAT_DICT = {"sbv": INFILES_SBV, 
               "srt": INFILES_SRT,
               "json": INFILES_JSON}


@patch("textgrid_convert.ttextgrid_convert.convert_to_txtgrid", autospec=True)
@patch("textgrid_convert.iotools.filewriter", autospec=True)
def test_srt_conversion(mock_writer, mock_convert ):
    """
    TEST SRT
    """
    infolder, outfolder = str(INFILES_SRT), str(MAIN_PATH)
    informat = "srt"
    args = ["--i", infolder,  "--f", informat, "--t", "textgrid", "--out", outfolder]
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
    TEST SBV
    """
    infolder, outfolder = str(INFILES_SBV), str(MAIN_PATH)
    informat = "srt"
    args = ["--i", infolder,  "--f", informat, "--t", "textgrid", "--out", outfolder]
    res = vars(arg_parser.parse_args(args))
    assert all((res["strict"] is True, res["input_path"] == infolder, str(res["output_path"]) == str(MAIN_PATH)))
    with pytest.raises(ValueError):
        main(**res)
    informat = "sbv"
    args = ["--i", infolder,  "--f", informat, "--t", "textgrid", "--out", outfolder]
    res = vars(arg_parser.parse_args(args))
    main(**res)
    assert mock_writer.call_count == len(os.listdir(res["input_path"]))
    assert mock_convert.call_count == len(os.listdir(res["input_path"]))
 
@patch("textgrid_convert.ttextgrid_convert.convert_to_txtgrid", autospec=True)
@patch("textgrid_convert.iotools.filewriter", autospec=True)
def test_json_conversion(mock_writer, mock_convert ):
    """
    TEST JSON
    """
    infolder, outfolder = str(INFILES_JSON), str(MAIN_PATH)
    informat = "srt"
    args = ["--i", infolder,  "--f", informat, "--t", "textgrid", "--out", outfolder]
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
 
@patch("textgrid_convert.ttextgrid_convert.convert_to_darla", autospec=True)
@patch("textgrid_convert.iotools.filewriter", autospec=True)
def test_darla_conversion(mock_writer, mock_convert ):
    """
    """
    for ext, path in FORMAT_DICT.items():
        infolder, outfolder = str(path), str(MAIN_PATH)
        informat = ext 
        args = ["--i", infolder,  "--f", informat, "--t", "darla", "--out", outfolder]
        res = vars(arg_parser.parse_args(args))
        assert res["strict"] is True
        assert res["input_path"] == str(path)
        assert str(res["output_path"]) == str(MAIN_PATH)
        main(**res)
        assert mock_writer.call_count == len(os.listdir(res["input_path"]))
        assert mock_convert.call_count == len(os.listdir(res["input_path"]))
        mock_writer.call_count = 0
        mock_convert.call_count = 0

# TEST SINGLE FILES 
@patch("textgrid_convert.ttextgrid_convert.convert_to_darla", autospec=True)
@patch("textgrid_convert.iotools.filewriter", autospec=True)
def test_darla_conversion_single(mock_writer, mock_convert ):
    """
    """
    for ext, path in FORMAT_DICT.items():
        infolder, outfolder = str(path), str(MAIN_PATH)
        infile = os.listdir(infolder)[0]
        informat = ext 
        args = ["--i", infile,  "--f", informat, "--t", "darla", "--out", outfolder]
        res = vars(arg_parser.parse_args(args))
        assert res["strict"] is True
        assert res["input_path"] == str(infile)
        assert str(res["output_path"]) == str(MAIN_PATH)
        main(**res)
        assert mock_writer.call_count == 1
        assert mock_convert.call_count == 1
        mock_writer.call_count = 0
        mock_convert.call_count = 0



def test_guess_format():
    SOURCE_FORMAT_DICT = dict((("UIUIUI.txt.srt", "srt"), ("folder/below/transcript.sbv", "sbv"), ("test.json", "rev")))
    for path, form in SOURCE_FORMAT_DICT.items():
        assert guess_source_format(path) == form
    assert guess_source_format("testi.txt") is None



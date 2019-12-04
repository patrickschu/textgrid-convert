# main
import os
import pathlib
import sys
from textgrid_convert.ArgParser import  arg_parser
from textgrid_convert.sbvParser import sbvParser
from textgrid_convert.srtParser import srtParser

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

HERE = pathlib.Path(os.getcwd())

def convert_to_txtgrid(input_file, source_format, speaker_name="Speaker 1"):
    """
    Convert forom `source_format` in `input_file` to TextGrid
    Args:
        input_file(str): path to input srt or sbv file to read from
        source_format(str): either sbv or srt
        speaker_name(str): optional speaker name
    Returns:
        TextGrid formatted string
    """
    with open(input_file, "r") as sourcefile:
        sourcetext = sourcefile.read()
        log.debug("Read file '{}' with {} chars".format(input_file, len(sourcetext)))
    if source_format == "sbv":
        parsed = sbvParser(sourcetext)
    if source_format == "srt":
        parsed = srtParser(sourcetext)
    txtgrid = parsed.to_textgrid(speaker_name=speaker_name)
    log.debug("Created TextGrid for file '{}'".format(input_file, len(sourcetext)))
    return txtgrid

def folder_source_format(input_folder, file_types=[".srt", ".sbv"]):
    """
    Check whether files in `input_foldelibr` have sbv, srt endings
    Args:
        input_folder(str)
        file_types (iterable of str): file endings to consider
    Returns:
        str srt or sbv
    Raises:
        ValueError if mix of extensions
    """
    infiles = [i for i in os.listdir(input_folder)]
    infiles = [i for i in infiles if os.path.splitext(i.lower())[-1] in file_types]
    types = [os.path.splitext(i.lower())[-1]for i in infiles]
    if len(infiles) < 1:
        raise ValueError("No relevant sbv or srt files found in folder '{}', contains '{}'".format(input_folder, os.listdir(input_folder)[:100]))
    if len(set(types)) > 1:
        raise ValueError("Both sbv and srt files found in folder '{}', contains '{}'".format(input_folder, infiles[:100]))
    assert types[0] in file_types
    return types[0].lstrip(".")

def main(source_format, to,  input_path, output_path=HERE, suffix="_TEXTGRID.txt"):
    """
    Convert files(s) from `input_path` from  `to` format to TextGrid. Optionally, write to `output_path`
    Example: convert from=sbv to=TextGrid and write to output_path="home/patrick/output"
    Args:
        source_format(str) : file ending, currently accepts sbv and srt
        to (str) : file ending, only accepts TextGrid atm
        input_path(str)
        output_path(str)
        suffix(str): string to append to file name for writing out TextGrid
    """
    input_path = pathlib.Path(input_path)
    if source_format:
        source_format = source_format.lower().strip(" .")
        if source_format not in ["sbv", "srt"]:
            raise ValueError("Works with 'sbv' or 'srt', given '{}'".format(source_format))
    if not any([source_format, input_path]):
        raise ValueError("Either input_path or source format needs to be specified, currently are {} and {}".format(source_format, input_path))
    # processing
    if os.path.isdir(input_path):
        log.debug("Processing folder '{}'".format(str(input_path)))
        if not source_format:
            source_format = folder_source_format(input_path)
        infiles = [i for i in os.listdir(input_path) if os.path.splitext(i.lower())[-1] == "." + source_format]
        infiles = [input_path / i for i in infiles]
        if len(infiles) < 1:
            raise ValueError("No relevant sbv or srt files found in folder '{}', contains '{}'".format(input_path, os.listdir(input_path)[:100]))
        log.debug("Processing {} {} files from folder '{}'".format(len(infiles), source_format, str(input_path)))
        for fil in infiles:
            log.debug("Working on file '{}'".format(fil))
            result = convert_to_txtgrid(fil, source_format) 
            if output_path:
                filename = output_path / (fil.name + suffix)
                # move this to file writer
                log.debug("Writing to %s", filename)
                if filename.exists():
                    if strict:
                        raise IOError(
                            "File '{}' already exists, will not overwrite".format(str(filename)))
                    else:
                        log.warning(
                            "File '%s' already exists, overwriting", str(filename))
                        os.remove(filename)
                with open(filename, "w", encoding="utf-8") as gridout:
                    gridout.write(result)
                log.debug("Textgrid written to '%s'", str(filename))



current_args = arg_parser.parse_args(sys.argv[1:])
print(current_args)
main(**vars(current_args))
# main

# main
import os
import pathlib
import sys
from textgrid_convert import iotools
from textgrid_convert.ArgParser import  arg_parser
from textgrid_convert.sbvParser import sbvParser
from textgrid_convert.srtParser import srtParser
from textgrid_convert.revParser import revParser
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

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
        parser = sbvParser(sourcetext)
    if source_format == "srt":
        parser = srtParser(sourcetext)
    if source_format in ["json", "rev"]:
        parser = revParser(sourcetext)
    txtgrid = parser.to_textgrid(speaker_name=speaker_name)
    log.debug("Created TextGrid for file '{}', len {}".format(input_file, len(sourcetext)))
    return txtgrid

def folder_source_format(input_folder, file_types=[".srt", ".sbv", ".json", ".rev"]):
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
    input_folder = str(input_folder)
    infiles = [i for i in os.listdir(input_folder)]
    infiles = [i for i in infiles if os.path.splitext(i.lower())[-1] in file_types]
    types = [os.path.splitext(i.lower())[-1]for i in infiles]
    if len(infiles) < 1:
        raise ValueError("No relevant sbv or srt files found in folder '{}', contains '{}'".format(input_folder, os.listdir(input_folder)[:100]))
    if len(set(types)) > 1:
        raise ValueError("Both sbv and srt files found in folder '{}', contains '{}'".format(input_folder, infiles[:100]))
    assert types[0] in file_types
    return types[0].lstrip(".")


def main(source_format, to,  input_path, output_path=HERE, suffix="_TEXTGRID.txt", strict=True):
    """
    Convert files(s) from `input_path` from  `to` format to TextGrid. Optionally, write to `output_path`
    Example: convert from=sbv to=TextGrid and write to output_path="home/patrick/output"
    Args:
        source_format(str) : file ending, currently accepts sbv and srt
        to (str) : file ending, only accepts TextGrid atm
        input_path(str)
        output_path(str)
        suffix(str): string to append to file name for writing out TextGrid
        strict(Bool): if True, will not overwrite files
    """
    log.debug('strict is %s' %strict)
    input_path = pathlib.Path(input_path)
    input_path = str(input_path)
    if output_path:
        output_path = str(output_path)
    log.debug('input path %s' %input_path)
    if source_format:
        source_format = source_format.lower().strip(" .")
        if source_format not in ["sbv", "srt", "json", "rev"]:
            raise ValueError("Works with 'sbv' or 'srt', 'json', 'rev', given '{}'".format(source_format))
    if not any([source_format, input_path]):
        raise ValueError("Either input_path or source format needs to be specified, currently are {} and {}".format(source_format, input_path))
    # processing FIXME: outsource this
    if os.path.isdir(input_path):
        log.debug("Processing folder '{}'".format(str(input_path)))
        if not source_format:
            source_format = folder_source_format(input_path)
            #FIXME below
        infiles = [i for i in os.listdir(input_path) if os.path.splitext(i.lower())[-1] == "." + source_format]
        infiles = [os.path.join(input_path, i) for i in infiles]
        if len(infiles) < 1:
            raise ValueError("No relevant sbv or srt files found in folder '{}', contains '{}'".format(input_path, os.listdir(input_path)[:100]))
        log.debug("Processing {} {} files from folder '{}'".format(len(infiles), source_format, str(input_path)))
        for fil in infiles:
            log.debug("Working on file '{}'".format(fil))
            result = convert_to_txtgrid(fil, source_format)
            if output_path:
                #filename = output_path / (fil.name + suffix)
                fil_name = os.path.split(fil)[-1]
                filename = os.path.join(output_path, fil_name + suffix)
                iotools.filewriter(filename, outstring=result, strict=strict)



if __name__ == "__main__":
    current_args = arg_parser.parse_args()
    log.debug("Current args %s " %current_args)
    main(**vars(current_args))

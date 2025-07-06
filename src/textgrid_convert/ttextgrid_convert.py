# main
import os
import pathlib
import sys
from . import iotools
from .ArgParser import  arg_parser
from .sbvParser import sbvParser
from .srtParser import srtParser
from .revParser import revParser
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

HERE = pathlib.Path(os.getcwd())

FILE_EXT_TO_FORMAT = {
    "json": "rev",
    "srt": "srt",
    "sbv": "sbv"
}


def get_py_version():
    """
    Get currently running Py version. Need to make pathlib adapts for Py < 3.6

    Args:

    Returns:
        tuple (major, minor, micro)
    """
    version_tuple = sys.version_info
    return version_tuple[:3]

def guess_source_format(input_path, extension_map=FILE_EXT_TO_FORMAT):
    """
    Based on file extension of `input_path`, guess the format of transcription file.

    Args:
        input_path(str): file name
        extension_map(dict): dictoinary {file_ext: format}, e.g. {"srt": "srt"}
    Returns:
        format string, None if not found in `extension_map`
    """ 
    _, ext = os.path.splitext(input_path)
    ext = ext.strip(".")
    source_format = extension_map.get(ext)
    if source_format is None:
        log.warning("Cannot guess source format for file '%s' (options are: %s)" %(input_path, extension_map.keys()))
    return source_format

def convert_to_txtgrid(input_file, source_format, speaker_name="Speaker 1"):
    """
    Convert from `source_format` in `input_file` to TextGrid.

    Args:
        input_file(str): path to input srt or sbv file to read from
        source_format(str): either sbv or srt
        speaker_name(str): optional speaker name
    Returns:
        TextGrid formatted string
    """
    with open(input_file, "r", encoding="utf-8") as sourcefile:
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

def convert_to_darla(input_file, source_format, speaker_name="Speaker 1"):
    """
    Convert from `source_format` in `input_file` to DARLA-compatible TextGrid

    Args:
        input_file(str): path to input srt or sbv file to read from
        source_format(str): either sbv or srt
        speaker_name(str): optional speaker name
    Returns:
        TextGrid formatted string
    """
    with open(input_file, "r", encoding="utf-8") as sourcefile:
        sourcetext = sourcefile.read()
        log.debug("Read file '{}' with {} chars".format(input_file, len(sourcetext)))
    if source_format == "sbv":
        parser = sbvParser(sourcetext)
    if source_format == "srt":
        parser = srtParser(sourcetext)
    if source_format in ["json", "rev"]:
        parser = revParser(sourcetext)
    # this will default to first speaker for rev
    txtgrid = parser.to_darla_textgrid(alias="sentence")
    log.debug("Created DARLA TextGrid for file '{}', len {}".format(input_file, len(sourcetext)))
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
    # FIXME: this should use guess_format
    input_folder = str(input_folder)
    infiles = [i for i in os.listdir(input_folder)]
    infiles = [i for i in infiles if os.path.splitext(i.lower())[-1] in file_types]
    types = [os.path.splitext(i.lower())[-1]for i in infiles]
    if len(infiles) < 1:
        raise ValueError("No relevant sbv or srt files found in folder '{}', contains '{}'".format(
            input_folder, os.listdir(input_folder)[:100]))
    if len(set(types)) > 1:
        raise ValueError("Both sbv and srt files found in folder '{}', contains '{}'".format(
            input_folder, infiles[:100]))
    assert types[0] in file_types
    #FIXME do we really need the check above
    return types[0].lstrip(".")

def main(source_format, to,  input_path, output_path=HERE, suffix="_TEXTGRID.txt", strict=True):
    """
    Convert files(s) from `input_path` from  `to` format to TextGrid. Optionally, write to `output_path`
    Example: convert from=sbv to=TextGrid and write to output_path="home/patrick/output"

    Args:
        source_format(str) : transcription format, currently accepts sbv, srt, and rev
        to (str) : file ending, only accepts TextGrid atm
        input_path(str)
        output_path(str)
        suffix(str): string to append to file name for writing out TextGrid
        strict(Bool): if True, will not overwrite files
    """
    major, minor, micro = get_py_version()
    if major != 3:
        version_str = ".".join([str(major), str(minor), str(micro)])
        raise NotImplementedError("Textgrid-convert only works with Python 3, not '{}'".format(version_str))
    if minor < 5:
        input_path = str(input_path)
        output_path = str(output_path)
    else:
        input_path = pathlib.Path(input_path)
    log.debug('input path %s, output path %s' %(input_path, output_path))
    if source_format:
        source_format = source_format.lower().strip(" .")
        if source_format not in FILE_EXT_TO_FORMAT.values():
            raise ValueError("Works with '{}'  given '{}'".format(FILE_EXT_TO_FORMAT.values(), source_format))
    if not any([source_format, input_path]):
        raise ValueError("Either input_path or source format needs to be specified, currently are {} and {}".format(
            source_format, input_path))
    # processing FIXME: outsource this
    if os.path.isdir(input_path):
        log.debug("Processing folder '{}'".format(str(input_path)))
        if not os.path.isdir(output_path):
            raise IOError("Cannot write multiple output files to path '{}' (specify output folder with `-o`)".format(
                output_path))
        if not source_format:
            source_format = folder_source_format(input_path)
            #FIXME below
        file_ext = {v:k for k,v in FILE_EXT_TO_FORMAT.items()}.get(source_format)
        if file_ext is None:
            raise KeyError("Could not find file type associated with '{}', options are: '{}'".format(
                source_format, FILE_EXT_TO_FORMAT.values()))
        infiles = [i for i in os.listdir(input_path) if os.path.splitext(i.lower())[-1] == "." + file_ext]
        infiles = [os.path.join(input_path, i) for i in infiles]
        if len(infiles) < 1:
            raise ValueError("No relevant files found in folder '{}', contains '{}'".format(
                input_path, os.listdir(input_path)[:100]))
        log.debug("Processing {} {} files from folder '{}'".format(len(infiles), source_format, str(input_path)))
        for fil in infiles:
            log.debug("Working on file '{}'".format(fil))
            if to and to.lower() in ["darla", "darlatextgrid"]:
                log.debug("Convert file '{}' to DARLA TextGrid".format(fil))
                result = convert_to_darla(fil, source_format)
            else:
                result = convert_to_txtgrid(fil, source_format)
            if output_path:
                #filename = output_path / (fil.name + suffix)
                fil_name = os.path.split(fil)[-1]
                filename = os.path.join(output_path, fil_name + suffix)
                log.debug("Writing to %s" %filename)
                iotools.filewriter(filename, outstring=result, strict=strict)
    else:
        log.debug("Working on file '%s'" %input_path)
        if not source_format:
            source_format = guess_source_format(input_path)
            if not source_format:
                raise IOError("Don't know what source format file '%s' is. Specify with option `-f`", input_path)
        if to and to.lower() in ["darla", "darlatextgrid"]:
            result = convert_to_darla(input_path, source_format)
        else:
            result = convert_to_txtgrid(input_path, source_format)
        if not output_path:
            output_path = HERE 
        fil_name = os.path.split(input_path)[-1]
        if os.path.isdir(output_path):
            filename = os.path.join(output_path, fil_name + suffix)
        else:
            filename = output_path
        log.debug("Writing to %s", filename)
        iotools.filewriter(filename, outstring=result, strict=strict)
        log.debug("Written to %s", filename)

if __name__ == "__main__":
    current_args = arg_parser.parse_args()
    log.debug("Current args %s " %current_args)
    main(**vars(current_args))

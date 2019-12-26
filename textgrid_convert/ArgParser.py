# main running stuff
import pathlib
import argparse
import os
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())



HERE = pathlib.Path(os.getcwd())
# accepted format needs to be "REV" no JSON

ACCEPTED_INPUT_FORMATS = ["rev", "sbv", "srt", "json"]
ACCEPTED_INPUT_FORMATS = ACCEPTED_INPUT_FORMATS + [i.upper() for i in ACCEPTED_INPUT_FORMATS]
ACCEPTED_INPUT_FORMATS = ACCEPTED_INPUT_FORMATS + [i + "." for i in ACCEPTED_INPUT_FORMATS]
log.debug("Accepted input formats are %s" %ACCEPTED_INPUT_FORMATS)



"""
Flags:
    -f, --from: sbv or srt # optional: can also be inferred from file name
    -t, --to: txtgrid 
    -i, --input_path:  also folder mode?
    -o, --output_path #take files or folders
"""

arg_parser = argparse.ArgumentParser(description="convert srt and sbv files to Praat textgrid", allow_abbrev=True)

"""
Set up read write and convert arguments
"""
arg_parser.add_argument("--input_path", "-i", type=str, help="Path to input file or folder", dest="input_path", required=True )
arg_parser.add_argument("--output_path", "-o",  help="Path to write output file(s) to", dest="output_path", default=HERE, type=pathlib.PurePath)
arg_parser.add_argument("--source_format", "--from", "-f", type=str, help="Input format to convert to TextGrid, e.g. sbv or srt",
        dest="source_format", choices=ACCEPTED_INPUT_FORMATS)
arg_parser.add_argument("--to", "-t", type=str, help="Output format to convert to, e.g. TextGrid or Darla", dest="to" )
arg_parser.add_argument("--strict",  action="store_false", help="If set, will overwrite existing files", dest="strict")
arg_parser.add_argument("--overwrite",  action="store_false", help="If set, will overwrite existing files", dest="strict")

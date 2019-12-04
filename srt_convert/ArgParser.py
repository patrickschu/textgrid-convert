# main running stuff
import pathlib
import argparse
import os
HERE = pathlib.Path(os.getcwd())

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
arg_parser.add_argument("--input_path", "-i", type=str, help="Path to input file or folder", dest="input_path")
arg_parser.add_argument("--output_path", "-o", type=str, help="Path to write output file(s) to", dest="output_path", default=HERE)
arg_parser.add_argument("--source_format", "--from", "-f", type=str, help="Input format to convert to TextGrid, e.g. sbv or srt",
        dest="source_format")
arg_parser.add_argument("--to", "-t", type=str, help="Output format to convert to, textgrid",dest="to" )


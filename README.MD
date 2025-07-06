# TEXTGRID-CONVERT

![](https://github.com/patrickschu/textgrid-convert/workflows/Python%20package%20Ubuntu/badge.svg)
![](https://github.com/patrickschu/textgrid-convert/workflows/Python%20package%20MacOS/badge.svg)
![](https://github.com/patrickschu/textgrid-convert/workflows/Python%20package%20Windows/badge.svg)
![](https://readthedocs.org/projects/pip/badge/)
![](https://zenodo.org/badge/doi/10.5281/zenodo.3596652.svg)


textgrid-convert converts audio transcripts such as sbv or srt files to
[Praat](http://www.fon.hum.uva.nl/praat/) and [DARLA](http://darla.dartmouth.edu/) compatible TextGrids.

# 1\. Install

Run `pip install textgrid-convert`. This requires Python 3.

The CI tests run on 3.7 (MacOS) and 3.7 + 3.8 (Win, Ubuntu). However, any Python 3+ version with NumPy and Pandas installed should work. 

# 2\. Use

You can run run the from the command line or as a regular library from a
Python script: `import textgrid_convert`.

## 2.1. Use in Python script

TBD

## 2.1. Use from command line

`python -m textgrid_convert` \[*input-file*\] \[*options*\] …

`python -m textgrid_convert --help` will display a help file.

## Required arguments

*input-files* or a *input-folder* have to be specified using the `-i`
flag.

    python -m textgrid_convert -i transcription.srt
    python -m textgrid_convert -i patrick/transcription_folder

For output to a file, use the optional `-o` option:

    python -m textgrid_convert -i transcription.srt -o transcription.TextGrid 

## Specifying formats

The format of the input and output files can be specified explicitly.
The input format can be specified using the `-f/--from` option, the
output format using the `-t/--to` option.

Thus, to convert `interview.sbv` from SBV to Praat TextGrid, you could
type:

    python -m textgrid_convert -i interview.sbv -f sbv -t TextGrid

If the input or output format is not specified explicitly,
textgrid-convert will guess based on the extensions of the filenames.

# Options

## General options

`-i` *FILE* / *FOLDER*., `--input_path` *FILE* / *FOLDER*.  
Read transcriptions from *FILE* or *FOLDER*.

`-f` *FORMAT*, `--from` *FORMAT*, `--source_format` *FORMAT*  
Specify input format. *FORMAT* can be:

  - `sbv` [docs](https://support.google.com/youtube/answer/2734698?hl=en&ref_topic=7296214)

  - `srt` [docs](https://support.google.com/youtube/answer/2734698?hl=en&ref_topic=7296214)

  - `rev` [docs](https://www.rev.com/api/attachmentsgetcontent)

`-t` *FORMAT*, `--to`*FORMAT* 
Specify output format. *FORMAT* can be:

  - `textgrid` or `TextGrid` [docs]()

  - `darla` or `DarlaTextGrid` [docs]()

`-o` *FILE*, `--output_path` *FILE*  
Write output to *FILE*.

## Examples

To convert the file *interview.sbv* from sbv to Praat TextGrid, simply
type

    python -m textgrid_convert -i interview.sbv -f sbv -t textgrid

To convert the file *interview.sbv* from sbv to Praat TextGrid and write
to *output.TextGrid*, simply type

    python -m textgrid_convert -i interview.sbv -f sbv -t textgrid -o output.TextGrid

To convert the file *interview.json* from rev-formatted transcriptions
to DARLA-compatible TextGrid and write to *output.TextGrid*, simply type

    python -m textgrid_convert -i interview.json -f rev -t darlatextgrid -o output.TextGrid

## Documentation

To be added [here](https://textgrid-convert.readthedocs.io/en/latest/)



## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Setup
```bash
# Clone the repository
git clone https://github.com/patrickschu/textgrid-convert.git
cd textgrid-convert

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --dev

# Activate virtual environment
source .venv/bin/activate

# Build
uv build -o ./dist

# Push to Pypi
uv run twine upload dist/* --verbose
```

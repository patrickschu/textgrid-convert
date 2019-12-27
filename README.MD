# TEXTGRID-CONVERT

![](https://github.com/patrickschu/textgrid-convert/workflows/Python%20package/badge.svg)

textgrid-convert converts audio transcripts such as sbv or srt files to
[Praat](http://www.fon.hum.uva.nl/praat/) and [DARLA](http://darla.dartmouth.edu/) compatible TextGrids.

# 1\. Install

Run `pip install textgrid-convert`. This requires Python 3.

# 2\. Use

You can run run the from the command line or as a regular library from a
Python script: `import textgrid_convert`.

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

  - `sbv` [docs]()

  - `srt` [docs]()

  - `rev` [docs]()

`-t` *FORMAT*, `--to`*FORMAT*  
Specify output format. *FORMAT* can be:

  - `textgrid` or `TextGrid` [docs]()

  - `darla` or `DarlaTextGrid` [docs]() :::

`-o` *FILE*, `--output_path` *FILE*  
Write output to *FILE*.

## Examples

To convert the file *interview.sbv* from sbv to Praat TextGrid, simply
type

    python -m textgrid_convert -i interview.sbv -f sbv -t textgrid

To convert the file *interview.sbv* from sbv to Praat TextGrid and write
to *output.TextGrid*, simply type

    python -m textgrid_convert -i interview.sbv -f sbv -t textgrid -o output_TextGrid

To convert the file *interview.json* from rev-formatted transcriptions
to DARLA-compatible TextGrid and write to *output.TextGrid*, simply type

    python -m textgrid_convert -i interview.json -f rev -t darlatextgrid -o output_TextGrid

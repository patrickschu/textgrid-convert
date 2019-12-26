# TEXTGRID-CONVERT

![](https://github.com/patrickschu/textgrid-convert/workflows/Python%20package/badge.svg)

textgrid-convert converts audio transcripts such as sbv or srt files to [Praat]() and [DARLA]() compatible TextGrids.



#### 1. Install

Run `pip install textgrid-convert`. This requires Python 3.

#### 2. Use

You can run run the from the command line or as a regular library from a Python script: `import textgrid-convert`.

##### 2.1. Use from command line

[Install]() first. The basic logic is to run `python textgrid-convert $ARGUMENTS`.  `python textgrid-convert --help` will display a help file.

#### 2.1.1 The following arguments are required:

`-i` or `--input_path`: location of a transcript or a folder of transcripts

> Example:  `python textgrid-convert -i patrick/srt_files/transcript.srt`

> Example:  `python textgrid-convert --input_path patrick/srt_files`


#### 2.1.2 The following arguments are optional:

`-o` or `--output_path`: location where files should be written to 

 >Example:  `python textgrid-convert -i srt_files -o patrick/converted_files # write files to folder patrick/converted_files`

`-f` or `--from`: source format of transcript, e.g. srt if a srt file is to be converted. 
`-t` or `--to`: target format of conversion, e.g. TextGrid if a file is to be converted to TextGrid.

> Example:  `python textgrid-convert -i srt_files -f srt -t TextGrid # converts from srt to TextGrid`

`--overwrite` : if this flag is passed, existing files will be overwritten. By default, no existing files are changed.



#### 2.2. Use from Python script



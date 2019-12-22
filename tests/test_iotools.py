import os
import pytest
import pathlib
from textgrid_convert.iotools import filewriter
from globals import OUTFILES


def test_filewrite():
    """
    """
    outfile = OUTFILES / "writeout.txt"
    if os.path.isfile(str(outfile)):
        os.remove(str(outfile))
    filewriter(str(outfile), "outstring")
    with pytest.raises(IOError):
        filewriter(str(outfile), "outstring", strict=True)
    filewriter(str(outfile), "outstring", strict=False)





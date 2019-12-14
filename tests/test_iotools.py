import pathlib
from textgrid_convert.iotools import filewriter
import os
import pytest

HERE = pathlib.Path(__file__).parent
RESOURCES = HERE / "resources"

def test_filewrite():
    """
    """
    outfile = RESOURCES / "writeout.txt"
    os.remove(outfile)
    filewriter(outfile, "outstring")
    with pytest.raises(IOError):
        filewriter(outfile, "outstring", strict=True)
    filewriter(outfile, "outstring", strict=False)





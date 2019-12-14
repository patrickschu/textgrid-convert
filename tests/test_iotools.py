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
    if os.path.isfile(str(outfile)):
        os.remove(str(outfile))
    filewriter(str(outfile), "outstring")
    with pytest.raises(IOError):
        filewriter(str(outfile), "outstring", strict=True)
    filewriter(str(outfile), "outstring", strict=False)





"""
Collect read and write here
"""
import os
import pytest
import logging
log = logging.getLogger(__name__)

def filewriter(filename, outstring, strict=True):
    """
    Args:
        filename(str)
        outstring(str)
        strict(Bool): if True, will not overwrite
    Returns:
        True, False
    """
    filename = str(filename)
    log.debug("Writing to %s", filename)
    if  os.path.isfile(filename):
        if strict:
            raise IOError(
                "File '{}' already exists, will not overwrite".format(str(filename)))
        else:
            log.warning(
                "File '%s' already exists, overwriting", str(filename))
            os.remove(filename)
    with open(filename, "w", encoding="utf-8") as gridout:
        gridout.write(outstring)
    log.debug("Textgrid written to '%s'", str(filename))

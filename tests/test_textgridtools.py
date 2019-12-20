# test textgrridtools
from textgrid_convert.textgridtools import collect_chunk_values, to_long_textgrid
import re
import pathlib
import pytest
from globals import INFILES_GRID, OUTFILES

LONG_GRID = INFILES_GRID / "test_long.TextGrid"
TO_GRID = OUTFILES / "test_long.TextGrid_output.txt"
TO_DARLA_GRID = OUTFILES / "test_long.TextGrid_darla_output.txt"

TESTDICT = {0: {"speaker_name": "Mary", "text": "one", "start": 0, "end": 0.5896534423132239},
            1: {"speaker_name": "Mary", "text": "",  "end": 1.4123177579131596,"start": 0.5896534423132239},
            2: {"speaker_name": "Mary", "text": "two",  "end": 2.343227378197297, "start": 1.4123177579131596},
            3: {"speaker_name": "Mary", "text": "three",  "end": 3.1225935719235522, "start": 2.343227378197297},
            4: {"speaker_name": "Mary", "start": 3.1225935719235522, "end": 12.804852607709751, "text": "rest of the text * @ " 
               },
            5: {"speaker_name": "John", "start": 0, "end": 12.804852607709751, "text": "" }}

def test_chunk_collect():
    """
    """
    res = collect_chunk_values(TESTDICT, "speaker_name")
    assert len(set(res) )== 2
    assert len(res)== len(TESTDICT) 
    with pytest.raises(KeyError):
        res = collect_chunk_values(TESTDICT, "NONKEY")


def test_to_long_textgrid():
    """
    """
    res = to_long_textgrid(TESTDICT)
    assert isinstance(res, str)
    res = to_long_textgrid(TESTDICT)
    print(res)
    with open(str(LONG_GRID), "r", encoding="utf-8") as gridin:
        truegrid = gridin.read()
    no_nonchars = re.sub(r"\W+", "", truegrid)
    # check content consistency
    no_nonchars_res = re.sub(r"\W+", "", " ".join(list(res)))
    assert no_nonchars == no_nonchars_res
    # check formatting consistency, f the tabs for now
    no_tab_res = re.sub(r"\t", "    ", truegrid)
    no_tab = re.sub(r"\t", "    ", truegrid)
    assert no_tab == no_tab_res
    with open(str(TO_GRID), "w", encoding="utf-8") as gridout:
        gridout.write(res)


def test_to_long_darla_textgrid():
    """
    """
    darladict = {}
    for key, values in TESTDICT.items():
        darladict[key] = values 
        darladict[key]["speaker_name"] = "sentence"
    res = to_long_textgrid(darladict)
    assert isinstance(res, str)
    with open(str(TO_DARLA_GRID), "w", encoding="utf-8") as gridout:
        gridout.write(res)

if __name__ == "__main__":
    test_to_long_textgrid()
    test_to_long_darla_textgrid()

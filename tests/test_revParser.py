# test revParser
import re
import json
import pathlib
from textgrid_convert.revParser import revParser


HERE = pathlib.Path(__file__).parent
RESOURCES = HERE / "resources"
JSON_IN = RESOURCES / "rev_sample.json"


def test_init():
    """
    """
    rr = revParser()


def test_json_read():
    """
    """
    with open(str(JSON_IN), "r", encoding="utf-8") as jsonin:
        text = jsonin.read()
    dicti = json.loads(text)
    print(dicti.keys())


    


if __name__ == "__main__":
   test_json_read()
   test_init()

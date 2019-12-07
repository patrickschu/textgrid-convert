from textgrid_convert.preproctools import adapt_timestamps

def test_adapt_timestamps():
    """
    """
    indict = {1: {"start": 0, "end": 122.2}, 2: {"start": 123, "end":
                                                 222.32323}, 3: {"start": 210,
                                                                 "end": 4444}}
    gap = 1
    res = adapt_timestamps(indict, gap=gap)
    assert isinstance(res, dict)
    for key in res:
        if res.get(key + 1):
            assert res[key]["end"] < res[key+1]["start"]
    assert res[2]["end"] < res[3]["start"]
    assert res[2]["end"] == res[3]["start"] - gap
    gap = 0.01
    res = adapt_timestamps(indict, gap=gap)
    assert res[2]["end"] == res[3]["start"] - gap
    # check we not mess with existing keys
    assert res[1]["start"] == indict[1]["start"]
    assert res[2]["start"] == indict[2]["start"]

if __name__ == "__main__":
    test_adapt_timestamps()


from lulzurl.easyurl import EasyUrl

def test_address_no_changes():
    eu = EasyUrl("https://some-random-api.ml")
    addr = object.__getattribute__(eu, "address")
    assert(addr == "https://some-random-api.ml")

def test_address_deeper_dive_attr():
    eu = EasyUrl("https://some-random-api.ml")
    eu = eu.others.lyrics
    addr = object.__getattribute__(eu, "address")
    assert(addr == "https://some-random-api.ml/others/lyrics")

def test_address_deeper_dive_index():
    eu = EasyUrl("https://some-random-api.ml")
    eu = eu['others'].lyrics
    addr = object.__getattribute__(eu, "address")
    assert(addr == "https://some-random-api.ml/others/lyrics")

def test_address_trailing_slash():
    eu = EasyUrl("https://some-random-api.ml")
    eu = eu[""]
    addr = object.__getattribute__(eu, "address")
    assert(addr == "https://some-random-api.ml/")

def test_address_trailing_add():
    eu = EasyUrl("https://some-random-api.ml")
    eu = eu.oth + "er"
    addr = object.__getattribute__(eu, "address")
    assert(addr == "https://some-random-api.ml/other")



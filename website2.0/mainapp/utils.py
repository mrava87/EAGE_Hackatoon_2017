def desectpath(path):
    basepath = ('/').join(path.split('/')[:-1])
    filename = path.split('/')[-1]
    ext = filename.split('.')[-1]
    fname = ('.').join(filename.split('.')[:-1])
    return basepath, fname, ext

# from https://stackoverflow.com/a/9878781:

def int_str(val, keyspace = "suTaWp6Z7P2zFYn5IMQUfqr4wAgeldRDVyvkS801HGjNJCbBKotE9x3hmiXcOL"): 
    """ Turn a positive integer into a string.
    Keyspace can be anything you like - this was just shuffled letters and numbers, but...
    each character must occur only once. """
    assert len(set(keyspace)) == len(keyspace) 
    assert val >= 0
    out = ""
    while val > 0:
        val, digit = divmod(val, len(keyspace))
        out += keyspace[digit]
    return out[::-1]

def str_int(val, keyspace = "suTaWp6Z7P2zFYn5IMQUfqr4wAgeldRDVyvkS801HGjNJCbBKotE9x3hmiXcOL"):
    """ Turn a string into a positive integer. """
    assert len(set(keyspace)) == len(keyspace) 
    out = 0
    for c in val:
        out = out * len(keyspace) + keyspace.index(c)
    return out

def chaffify(val, chaff_val = 98127634):
    """ Add chaff to the given positive integer. """
    return val * chaff_val

def dechaffify(chaffy_val, chaff_val = 98127634):
    """ Dechaffs the given chaffed value. 
    chaff_val must be the same as given to chaffify(). 
    If the value does not seem to be correctly chaffed, raises a ValueError. """
    val, chaff = divmod(chaffy_val, chaff_val)
    if chaff != 0:
        raise ValueError("Invalid chaff in value")
    return val

def id_to_key(number, keyspace="suTaWp6Z7P2zFYn5IMQUfqr4wAgeldRDVyvkS801HGjNJCbBKotE9x3hmiXcOL"):
    return int_str(chaffify(number),keyspace)

def key_to_id(key, keyspace="suTaWp6Z7P2zFYn5IMQUfqr4wAgeldRDVyvkS801HGjNJCbBKotE9x3hmiXcOL"):
    return dechaffify(str_int(key,keyspace))

import random, string

def randomkey():
    return ''.join(random.sample(string.ascii_letters+string.digits,len(string.ascii_letters+string.digits)))

from cv2 import imdecode
from numpy import asarray, uint8
import urllib

# cv2.imread cannot read from an url therefore this function
def url_to_img(url):
    req = urllib.urlopen(url)
    arr = asarray(bytearray(req.read()), dtype=uint8)
    return imdecode(arr,1)


# lab.py


import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.21')
import os
import re


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def match_1(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_1("abcde]")
    False
    >>> match_1("ab[cde")
    False
    >>> match_1("a[cd]")
    False
    >>> match_1("ab[cd]")
    True
    >>> match_1("1ab[cd]") # Including a substring ("ab[cd]") that satisfies the pattern does not qualify as a match.
    False
    >>> match_1("ab[cd]ef")
    True
    >>> match_1("1b[#d] _")
    True
    """
    pattern = r"^..\[..\].*$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_2(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_2("(123) 456-7890")
    False
    >>> match_2("858-456-7890")
    False
    >>> match_2("(858)45-7890")
    False
    >>> match_2("(858) 456-7890")
    True
    >>> match_2("(858)456-789")
    False
    >>> match_2("(858)456-7890")
    False
    >>> match_2("a(858) 456-7890")
    False
    >>> match_2("(858) 456-7890b")
    False
    """
    pattern = r"^\(858\) \d{3}-\d{4}$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_3(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_3("qwertsd?")
    True
    >>> match_3("qw?ertsd?")
    True
    >>> match_3("ab c?")
    False
    >>> match_3("ab   c ?")
    True
    >>> match_3(" asdfqwes ?")
    False
    >>> match_3(" adfqwes ?")
    True
    >>> match_3(" adf!qes ?")
    False
    >>> match_3(" adf!qe? ")
    False
    """
    pattern = r"^[a-zA-Z0-9\s?]{5,9}\?$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_4(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_4("$$AaaaaBbbbc")
    True
    >>> match_4("$!@#$aABc")
    True
    >>> match_4("$a$aABc")
    False
    >>> match_4("$iiuABc")
    False
    >>> match_4("123$$$Abc")
    False
    >>> match_4("$$Abc")
    True
    >>> match_4("$qw345t$AAAc")
    False
    >>> match_4("$s$Bca")
    False
    >>> match_4("$!@$")
    False
    """
    pattern = r"^\$[^abc$]*\$[Aa]+[Bb]+[Cc]+$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_5(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_5("dsc80.py")
    True
    >>> match_5("dsc80py")
    False
    >>> match_5("dsc80..py")
    False
    >>> match_5("dsc80+.py")
    False
    """
    pattern = r"^\w+\.py$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_6(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_6("aab_cbb_bc")
    False
    >>> match_6("aab_cbbbc")
    True
    >>> match_6("aab_Abbbc")
    False
    >>> match_6("abcdef")
    False
    >>> match_6("ABCDEF_ABCD")
    False
    """
    pattern = r"^[a-z]+_[a-z]+$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_7(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_7("_abc_")
    True
    >>> match_7("abd")
    False
    >>> match_7("bcd")
    False
    >>> match_7("_ncde")
    False
    """
    pattern = r"^_.*_$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_8(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_8("ASJDKLFK10ASDO")
    False
    >>> match_8("ASJDKLFK0ASDo!!!!!!! !!!!!!!!!")
    True
    >>> match_8("JKLSDNM01IDKSL")
    False
    >>> match_8("ASDKJLdsi0SKLl")
    False
    >>> match_8("ASDJKL9380JKAL")
    True
    """
    pattern = r"^[^Oi1]+$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_9(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_9('NY-32-NYC-1232')
    True
    >>> match_9('ca-23-SAN-1231')
    False
    >>> match_9('MA-36-BOS-5465')
    False
    >>> match_9('CA-56-LAX-7895')
    True
    >>> match_9('NY-32-LAX-0000') # If the state is NY, the city can be any 3 letter code, including LAX or SAN!
    True
    >>> match_9('TX-32-SAN-4491')
    False
    '''
    pattern = r"^(CA-\d{2}-(SAN|LAX)-\d{4}|NY-\d{2}-[A-Z]{3}-\d{4})$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_10(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_10('ABCdef')
    ['bcd']
    >>> match_10(' DEFaabc !g ')
    ['def', 'bcg']
    >>> match_10('Come ti chiami?')
    ['com', 'eti', 'chi']
    >>> match_10('and')
    []
    >>> match_10('Ab..DEF')
    ['bde']
    
    '''
    cleaned = re.sub(r'[\Wa]', '', string.lower())
    return re.findall(r'.{3}', cleaned)


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def extract_personal(s):
    emails = re.findall(r"[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z]+", s)
    ssns = re.findall(r"ssn:(\d{3}-\d{2}-\d{4})", s)
    bitcoins = re.findall(r"bitcoin:([A-Za-z0-9]{20,})", s)
    streets = re.findall(r'[,*|#\t](\d+ [A-Za-z0-9 ]+)(?=\n|$)', s)
    return (emails, ssns, bitcoins, streets)

# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def hashtag_list(tweet_text):
    return tweet_text.apply(lambda t : re.findall(r"#(\S+)", t))

def most_common_hashtag(tweet_lists):
    counts = tweet_lists.explode().value_counts()
    return tweet_lists.apply(lambda lst : max(lst, key = counts.get) if len(lst) > 0 else np.nan)


def create_features(tweets):
    text = tweets['text']
    tags = hashtag_list(text)
    out = pd.DataFrame(index = tweets.index)
    out['text'] = (text.str.replace(r'#\S+|@[A-Za-z0-9]+|https?://\S+|\bRT\b', '', regex=True)
                   .str.replace(r"[^A-Za-z0-9\s]", ' ', regex=True)
                   .str.lower()
                   .str.replace(' +', ' ', regex=True)
                   .str.replace(r'^ | $', '', regex=True))
    out['num_hashtags'] = tags.str.len()
    out['common_hashtag'] = most_common_hashtag(tags)
    out['num_tags'] = text.str.count(r"@[A-Za-z0-9]+")
    out['num_links'] = text.str.count(r"https?://\S+")
    out['is_retweet'] = text.str.contains(r"^RT", regex=True)
    return out[['text', 'num_hashtags', 'common_hashtag', 'num_tags', 'num_links', 'is_retweet']]

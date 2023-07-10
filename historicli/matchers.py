COL_IDX = {
    'epoch': 0,
    'era': 0,
    'e': 0,
    'circa': 1,
    '~': 1,
    'ca': 1,
    'year': 2,
    'y': 2,
    'yr': 2,
    'anno': 2,
    'category': 3,
    'cat': 3,
    'description': 4
}

BC_MATCHERS = [
    'bc',
    'BC',
    'B.C.',
    'B.C',
    r'-',
    r'- '
]

CIRCA_MATCHERS = [
    r'~',
    'c.',
    'c',
    'circa',
    'ca',
    'appr',
    'approximately'
]

CAT_MATCHERS = {
    "p": "P",
    "person": "P",
    "people": "P",
    "e": "E",
    "event": "E",
    "events": "E",
    "m": "M",
    "music": "M",
    "b": "B",
    "battle": "B",
    "battles": "B",
    "a": "A",
    "art": "A",
    "arts": "A",
    "l": "L",
    "lit": "L",
    "literature": "L",
    "s": "S",
    "science": "S",
}
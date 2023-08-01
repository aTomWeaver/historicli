COL_IDX = {
    # 'epoch': 0,
    # 'era': 0,
    # 'e': 0,
    'circa': 1,
    '~': 1,
    'ca': 1,
    'year': 0,
    'y': 0,
    'yr': 0,
    'anno': 0,
    'category': 2,
    'cat': 2,
    'description': 3
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
    "philosophy": "P",
    "philosopher": "P",
    "philosophers": "P",
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
    "sciences": "S",
}

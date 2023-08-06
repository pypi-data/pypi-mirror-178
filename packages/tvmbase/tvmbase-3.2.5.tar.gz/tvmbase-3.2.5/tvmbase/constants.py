import re

EMPTY_CELL = 'te6ccgEBAQEAAgAAAA=='  # b5ee9c72 | 01 01 01 01 | 00 02 | 00 | 00 00
EVER = 1_000_000_000  # 1e9 grams = 1 ever
HALF_EVER = 500_000_000  # 0.5 ever

# todo flags

GRAPHQL_LIMIT = 50

ADDRESS_REGEX = re.compile(r'(0|-1):[0-9a-f]{64}')
IDX_REGEX = re.compile(r'[0-9a-f]{64}')

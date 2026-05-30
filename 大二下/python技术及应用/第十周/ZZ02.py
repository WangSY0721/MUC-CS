import re

pattern = r'^[A-Z][a-zA-Z]* Nakamoto$'

test_strings = [
    'Satoshi Nakamoto',
    'Alice Nakamoto',
    'RoboCop Nakamoto',
    'satoshi Nakamoto',
    'Mr. Nakamoto',
    'Nakamoto',
    'Satoshi nakamoto'
]

for string in test_strings:
    match = re.match(pattern, string)
    print(f"{string}: {'匹配' if match else '不匹配'}")

import re

pattern = r'^\d{1,3}(,\d{3})*$'

test_strings = [
    '42',
    '1234',
    '6368745',
    '1,234,567',
    '1234'
]

for string in test_strings:
    match = re.match(pattern, string)
    print(f"{string}: {'匹配' if match else '不匹配'}")

import re

pattern = r'^(Alice|Bob|Carol) (eats|pets|throws) (apples|cats|baseballs)\.$'

test_strings = [
    'Alice eats apples.',
    'Bob pets cats.',
    'Carol throws baseballs.',
    'Alice throws Apples.',
    'BOB EATS CATS.',
    'RoboCop eats apples.',
    'ALICE THROWS FOOTBALLS.',
    'Carol eats 7 cats.'
]

for string in test_strings:
    match = re.match(pattern, string, re.IGNORECASE)
    print(f"{string}: {'匹配' if match else '不匹配'}")

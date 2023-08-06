with open('./data/encodings.txt') as file:
    encodings = [e.strip() for e in file]
b = b'head\x1e\x01\x00\x00\xdc\x86f'

for encoding in encodings:
    result = None
    try:
        result = b.decode(encoding, 'backslashing')
    except:
        pass
    print(f'{encoding} = {result}')

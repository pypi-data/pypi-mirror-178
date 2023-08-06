from functools import cmp_to_key


def replace_trash(word: str) -> str:
    return word.rstrip().replace('.', '').replace('2', '').replace('3', '').replace('?', '')


def is_russian(word: str) -> bool:
    return all(e in ALPHABET for e in word)


def is_english(word: str) -> bool:
    return all(e in ALPHABET_EN for e in word.lower())


ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
ALPHABET_EN = 'abcdefghijklmnopqrstuvwxyz'

used = set()


def compare(a: str, b: str) -> int:
    if not a.startswith('Ё') and not b.startswith('Ё'):
        return -1 if a < b else 0 if a == b else 1
    if a.startswith('Ё') and b.startswith('Ё'):
        return -1 if a < b else 0 if a == b else 1
    if a.startswith('Ё') and any(b.startswith(letter) for letter in 'АБВГДЕ'):
        return 1
    if a.startswith('Ё') and any(b.startswith(letter) for letter in 'ЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
        return -1
    if b.startswith('Ё') and any(a.startswith(letter) for letter in 'АБВГДЕ'):
        return -1
    return 1


with open('data/ojegov.txt', 'rt', encoding='utf-8') as fin, open('data/words_ru1.txt', 'wt', encoding='utf-8') as fout:
    for line in fin:
        if line and len(line) > 3:
            words = (replace_trash(word) for word in line.replace(',', ' ').split(' ')
                     if word.isupper() and is_russian(word))
            for word in words:
                if word in used:
                    continue
                used.add(word)
    for word in sorted(used, key=cmp_to_key(compare)):
        fout.write(f'{word.lower()}\n')


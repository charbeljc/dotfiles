import unicodedata as udb

def examine(char):
    if len(char) > 1:
        raise TypeError("single char, please")
    try:
        examine = udb.name(char)
    except ValueError as e:
        yield (e, char)
    else:
        head, sep, tail = examine.partition(' ')
        while sep:
            yield head
            head, sep, tail = tail.partition(' ')
        if head:
            yield head

def is_garbage(outcome):
    return isinstance(outcome[0][0], Exception)
def is_not_garbage(outcome):
    return not is_garbage(outcome)

def spellit(what, garbage=False):
    if not isinstance(what, unicode):
        raise TypeError("not unicode")
    what = udb.normalize('NFC', what)
    for char in what:
        outcome = tuple(examine(char))
        if garbage or not is_garbage(outcome):
            yield outcome

if __name__ == '__main__':
    latin=''.join(chr(i) for i in range(256)).decode('latin1', 'replace')
    for k, elts in groupby(spell.spellit(latin), lambda c: c[0]):
        print k
        for e in elts:
            print '\t', e


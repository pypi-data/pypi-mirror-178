def pairwise(seq, add_tail_head=False):
    if len(seq) == 0:
        return
    it = iter(seq)
    a = next(it)
    if len(seq) == 1:
        yield a, a
        return
    head = a
    b = next(it)
    while True:
        try:
            yield a, b
            a = b
            b = next(it)
        except StopIteration:
            if len(seq) > 0 and add_tail_head:
                yield b, head
            return

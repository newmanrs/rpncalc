def take_n(n,stack, op):
    if n > len(stack):
        msg = f"Empty stack processing {op} trying to pop {n} values. Stack: {stack}"
        raise IndexError(msg)

    for i in range(n):
        yield stack.pop()

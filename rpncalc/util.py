def take_n(n, stack, action=None):
    """
    Generator that pops up to n values from stack.
    Optional action gives clearer error messages.
    """
    if n > len(stack):
        msg = (
            f"Empty stack processing {action} trying "
            f"to pop {n} values. Stack: {stack}")
        raise IndexError(msg)

    for i in range(n):
        yield stack.pop()

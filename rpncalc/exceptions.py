class RpnCalcError(Exception):
    """Calculator Generic Exception"""
    pass


class StackDepletedError(RpnCalcError):
    """ Stack is out of items """
    pass

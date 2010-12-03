


class WordException(BaseException):
    pass


class UnknownSigil(BaseException):
    pass

class UnknownWord(UnknownSigil):
    pass

class UnknownType(UnknownSigil):
    pass


class ParseFailure(BaseException):
    pass


class SomeType(object):
    """
    Wrap the fields of the reconstructed object.
    """

    pass



class Field:
    """
    Associate a name with a value
    """

    def __init__(self, name, value):
        self.name  = name
        self.value = value

    def __repr__(self):
        return 'Field(%s,%s)' % (self.name, self.value)

    def __str__(self):
        return repr(self)






class WordException(Exception):
    pass


class UnknownSigil(Exception):
    pass

class UnknownWord(UnknownSigil):
    pass

class UnknownType(UnknownSigil):
    pass


class ParseFailure(Exception):
    pass


class SomeType(object):
    """
    Wrap the fields of the reconstructed object.
    """

    def construct_original(self):
        """
        Construct an object of the original type and set it's attributes to mine from self.__dict__
        """

        srcs = self._pith_source_type.split('.')
        module = '.'.join(srcs[:-1])
        typ = srcs[-1]

        cmd = 'from %(module)s import %(name)s' % {'module' : module, 'name' : typ}
        exec cmd
        Type = eval(typ)
        obj = Type()

        for attr, val in self.__dict__.iteritems():
            setattr(obj, attr, val)

        return obj


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



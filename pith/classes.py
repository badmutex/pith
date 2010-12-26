from valid_containers import valid_pith_containers


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


def sequence_items(seq):
    for e in seq:
        if isinstance(e, SomeType):
            yield e.construct_original()

class SomeType(object):
    """
    Wrap the fields of the reconstructed object.
    """

    def __init__(self, **kws):
        for k,v in kws.iteritems():
            setattr(self, k, v)

    def construct_original(self, debug=False):
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
            if attr == '_pith_source_type': continue

            if debug:
                print 'PITH\tCONSTRUCT: SomeType\n\t%s = %s' % (attr, val)


            if isinstance(val, SomeType):
                val = val.construct_original()

            if type(obj) in valid_pith_containers:
                val = type(val)(sequence_items(val))

            if debug:
                print '\tCONSTRUCT: ORIGINAL\n\t%s = %s' % (attr, val)

            setattr(obj, attr, val)

        return obj

    def __repr__(self):

        def params():
            for k,v in self.__dict__.iteritems():
                yield str(k) + '=' + repr(v)
        return 'SomeType(%s)' % ','.join(params())


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



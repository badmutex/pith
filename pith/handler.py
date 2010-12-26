import classes

import functools


class Handler(object):
    def __init__(self, sigil_type, handlers, unknown_exception):
        self.type              = sigil_type
        self.handlers          = handlers
        self.unknown_exception = unknown_exception

    def lookup_handler(self, sigil):
        try:
            return self.handlers[sigil]
        except KeyError:
            raise self.unknown_exception, sigil





class Type(object):
    @classmethod
    def handle(cls, words, types, stack):
        t  = stack.pop()
        ty = types.lookup_handler(t)
        stack.append(ty)
        return stack


class New(object):
    @classmethod
    def handle(cls, words, types, stack):
        numargs = int(stack.pop())
        ty      = stack.pop()
        args    = [stack.pop() for _ in xrange(numargs)]
        obj     = ty(*args)
        stack.append(obj)
        return stack

class Field(object):
    @classmethod
    def handle(cls, words, types, stack):
        name  = stack.pop()
        value = stack.pop()
        f     = classes.Field(name, value)
        stack.append(f)
        return stack

class Object(object):
    @classmethod
    def handle(cls, words, types, stack):
        numfields = int(stack.pop())
        obj       = stack.pop()
        for _ in xrange(numfields):
            f = stack.pop()
            setattr(obj, f.name, f.value)
        stack.append(obj)
        return stack

class SomeType(object):
    @classmethod
    def handle(cls, words, types, stack):
        obj = classes.SomeType()
        src = stack.pop()
        setattr(obj, '_pith_source_type', src)
        stack.append(obj)
        return stack



def mkseq(typ, *args, **kws):
    composed = kws.get('composed', lambda a:a)
    return composed(typ(args))

# The values of __sigils__ should positionally correspond to the values of __word_handlers__:
# they are zipped together for the DefaultWordHandler down below

__sigils__ = ['TYPE', 'NEW', 'FIELD', 'OBJECT', 'SOMETYPE']

__sigils_pairs__ = dict([ (s,s) for s in __sigils__ ])

__word_handlers__ = [Type, New, Field, Object, SomeType]

__type_handlers__ = {'int'   : int,
                     'float' : float,
                     'str'   : str,
                     'tuple' : functools.partial(mkseq, tuple),
                     'list'  : functools.partial(mkseq, list),
                     'dict'  : functools.partial(mkseq, list, composed=dict),
                     }


DefaultSigils      = __sigils_pairs__
DefaultWordHandler = Handler( 'word',
                              dict(zip(__sigils__, __word_handlers__)),
                              classes.UnknownWord)
DefaultTypeHandler = Handler( 'type',
                              __type_handlers__,
                              classes.UnknownType)

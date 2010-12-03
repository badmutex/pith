import pith.classes as classes
import pith.handler as handler


class Pith(object):
    def __init__(self,
                 sep    = ' :&: ',
                 sigils = handler.DefaultSigils,
                 words  = handler.DefaultWordHandler,
                 types  = handler.DefaultTypeHandler,
                 debug  = False):
        self.sep    = sep
        self.sigils = sigils
        self.words  = words
        self.types  = types
        self.debug  = debug


    def get_module_and_type(self, obj):
        module = type(obj).__module__
        name = type(obj).__name__
        if module == '__builtin__':
            return name
        else:
            return module + '.' + name


    def __show(obj, attributes):
        if hasattr(obj, '__dict__'):
            if attributes is None:
                keys = obj.__dict__.iterkeys()
            else:
                keys = iter(attributes)

            for nkeys, a in enumerate(keys):
                for s in self.__show(getattr(obj, a)):
                    yield a

                yield a
                yield self.sigils['FIELD']

            yield self.get_module_and_type(obj)
            yield self.sigils['SOMETYPE']
            yield str(nkeys + 1)
            yield self.sigils['OBJECT']

        else:
            yield str(obj)
            yield type(obj).__name__
            yield self.sigils['TYPE']
            yield '1'
            yield self.sigils['NEW']


    def show(obj, attributes=None):
        return self.sep.join(self.__show(obj, attributes))


    def read(string):
        stack = list()
        for term in string.split(self.sep):
            if self.debug:
                print 'PITH: ', stack

            t = term.strip()
            try:
                h = self.words.lookup_handler(t)
                stack = h.handle(self.words, self.types, t)
            except UnknownSigil, e:
                print e
                raise classes.ParseFailure, string

        if len(stack) == 1:
            return stack.pop()
        else:
            raise classes.ParseFailure, string, stack

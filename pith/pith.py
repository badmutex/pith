import classes
import handler


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


    def __show(self, obj, attributes=None, ignore_attributes=set()):
        if hasattr(obj, '__dict__'):
            if attributes is None:
                keys = obj.__dict__.iterkeys()
            else:
                keys = iter(attributes)

            skipped = 0
            for nkeys, a in enumerate(keys):
                if a in ignore_attributes:
                    skipped += 1
                    continue

                for s in self.__show(getattr(obj, a)):
                    yield s

                yield a
                yield self.sigils['FIELD']

            yield self.get_module_and_type(obj)
            yield self.sigils['SOMETYPE']
            yield str(nkeys + 1 - skipped)
            yield self.sigils['OBJECT']

        else:
            yield str(obj)
            yield type(obj).__name__
            yield self.sigils['TYPE']
            yield '1'
            yield self.sigils['NEW']


    def show(self, obj, attributes=None, ignore_attributes=set()):
        return self.sep.join(self.__show(obj, attributes=attributes, ignore_attributes=ignore_attributes))


    def read(self, string):
        stack = list()
        for term in string.split(self.sep):
            t = term.strip()

            if self.debug:
                print 'PITH\tTERM: %s\n\tSTACK: %s' % (t, stack)

            try:
                h = self.words.lookup_handler(t)

                if self.debug:
                    print '\tHANDLER:', h

                stack = h.handle(self.words, self.types, stack)
            except classes.UnknownSigil, e:
                stack.append(t)

        if len(stack) == 1:
            return stack.pop()
        else:
            msg = '\tstring: %s\n\tstack: %s' % (string, stack)
            # print msg
            raise classes.ParseFailure, msg

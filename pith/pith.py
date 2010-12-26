import classes
import handler

from valid_containers import valid_pith_containers


class Pith(object):

    VALID_CONTAINERS = valid_pith_containers

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
        if self.debug:
            print 'PITH\tShowing', type(obj), obj

        if hasattr(obj, '__dict__'):
            if self.debug:
                print 'PITH\t  ',  '__dict__', obj

            if attributes is None:
                keys = obj.__dict__.iterkeys()
            else:
                keys = iter(attributes)

            skipped = 0
            for nkeys, a in enumerate(keys):
                nkeys += 1
                if a in ignore_attributes:
                    skipped += 1
                    continue

                for s in self.__show(getattr(obj, a)):
                    yield s

                yield a
                yield self.sigils['FIELD']

            try: nkeys
            except NameError:
                nkeys = 0

            yield self.get_module_and_type(obj)
            yield self.sigils['SOMETYPE']
            yield str(nkeys - skipped)
            yield self.sigils['OBJECT']

        else:

            num_params = 1

            def check_type(typ): return isinstance(obj, typ)

            to_check = Pith.VALID_CONTAINERS
            check_result = map(check_type, to_check)

            if self.debug:
                print 'PITH\t  Typecheck:', any(check_result), zip(to_check, check_result)

            if any(check_result):

                num_params = len(obj)
                if isinstance(obj, list) or isinstance(obj, tuple):
                    for a in reversed(obj):
                        for s in self.__show(a): yield s

                elif isinstance(obj, dict):
                    for k,v in obj.iteritems():
                        for s in self.__show((k,v)): yield s

                else:
                    raise classes.UnknownType, 'Cannot pith-ify instance of %s' % type(obj)

            else:
                yield str(obj)


            yield type(obj).__name__
            yield self.sigils['TYPE']
            yield str(num_params)
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

        if self.debug:
            print 'PITH\tDONE Reading\n\tSTACK: %s' % stack

        if len(stack) == 1:
            return stack.pop()
        else:
            msg = '\tstring: %s\n\tstack: %s' % (string, stack)
            # print msg
            raise classes.ParseFailure, msg

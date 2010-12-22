
from pith import Pith

p = Pith()
l = '8 :&: int :&: TYPE :&: 1 :&: NEW :&: run :&: FIELD :&: 38 :&: int :&: TYPE :&: 1 :&: NEW :&: clone :&: FIELD :&: 291 :&: int :&: TYPE :&: 1 :&: NEW :&: gen :&: FIELD :&: 984 :&: int :&: TYPE :&: 1 :&: NEW :&: frame :&: FIELD :&: 4.21349235547 :&: float :&: TYPE :&: 1 :&: NEW :&: rmsd :&: FIELD :&: protolyze.db.results.Result :&: SOMETYPE :&: 5 :&: OBJECT'

obj = p.read(l)
print dir(obj)
orig = obj.construct_original()
print type(orig)
print dir(orig)
print orig.primary_key()

print obj
for k,v in obj.__dict__.iteritems():
    print '\t', k,'=', v


print p.show(obj)

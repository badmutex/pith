
# Test sequences

from pith import Pith

p = Pith(sep='|')

for grp in [(1,2,3), [1,2,3], {'a':1,'b':2,'c':3}]:
    print type(grp), grp
    s = p.show(grp)
    print 'show:', s
    r = p.read(s)
    print 'read:', r


from pith import Pith

import protolyze.db.results as dbr

DEBUG=False

p = Pith(debug=DEBUG)

r = dbr.Result(run=1,clone=2,gen=3,frame=4)


column_name = 'my_column_name'
column = dbr.DBColumn()
column.set_name(column_name)
column.set_type('float')
column.set_column_kwargs(index=True)

s = p.show(column)
read = p.read(s)
print 'show    ', s
print 'original', column
print 'read    ', read
print 'recreate', read.construct_original(debug=DEBUG)

# r.value(column, 42)

# shown = r.show()
# print 'shown =', shown
# read = p.read(shown)
# print 'read =', read.construct_original().__dict__

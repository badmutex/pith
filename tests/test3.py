
from pith import Pith

s = '/pscratch/csweet1/lcls/fah/data/PROJ10012/RUN3404/CLONE0/results-001.xtc :&: str :&: TYPE :&: 1 :&: NEW :&: trajectory :&: FIELD :&: 750 :&: int :&: TYPE :&: 1 :&: NEW :&: frame :&: FIELD :&: 1.1131634 :&: float :&: TYPE :&: 1 :&: NEW :&: rmsd :&: FIELD :&: __main__.RMSD_Result :&: SOMETYPE :&: 3 :&: OBJECT'

s = 'list :&: TYPE :&: 0 :&: NEW'

s = 'list :&: TYPE :&: 0 :&: NEW :&: _extra_dbcolumns :&: FIELD :&: 3404 :&: int :&: TYPE :&: 1 :&: NEW :&: run :&: FIELD :&: 0 :&: int :&: TYPE :&: 1 :&: NEW :&: clone :&: FIELD :&: 1 :&: int :&: TYPE :&: 1 :&: NEW :&: gen :&: FIELD :&: list :&: TYPE :&: 0 :&: NEW :&: _fields :&: FIELD :&: 750 :&: int :&: TYPE :&: 1 :&: NEW :&: frame :&: FIELD :&: protolyze.db.results.Result :&: SOMETYPE :&: 6 :&: OBJECT'

p = Pith(debug=False)

print p.read(s)

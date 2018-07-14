# Original Script by tcastudios
# Modified by Creativetuts.com
# 2015

import c4d
from c4d import documents
from c4d import Vector as v, utils as u
 
def main():
    doc = c4d.documents.GetActiveDocument()
    obj1 = doc.SearchObject('obj1')
    obj2 = doc.SearchObject('obj2')
    
    target = obj1
    
    if not target or not target.CheckType(c4d.Opoint): return True
 
    source = obj2
    if not source: return True
 
    tBB = target.GetRad()   # Target BoundingBox
    sBB = source.GetRad()   # Source BoundingBox
    sSc = source[c4d.ID_BASEOBJECT_ABS_SCALE] # Source Scale
 
    try:    xdif = sBB.x / tBB.x 
    except: xdif = 1.0
    try:    ydif = sBB.y / tBB.y 
    except: ydif = 1.0
    try:    zdif = sBB.z / tBB.z 
    except: zdif = 1.0
 
    for i in xrange(target.GetPointCount()):
        ppos = target.GetPoint(i)
        target.SetPoint(i,v(ppos.x * xdif * sSc.x , ppos.y * ydif * sSc.y , ppos.z * zdif * sSc.z))
        
    target.Message(c4d.MSG_UPDATE)
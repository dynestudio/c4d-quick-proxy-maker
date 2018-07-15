'v0.1.5'

import c4d

doc = c4d.documents.GetActiveDocument()

def get_allObjs(root_selection):
    def GetNextObject(op): # object manager iteration
        if not op: return None
        if op.GetDown(): return op.GetDown()
        while not op.GetNext() and op.GetUp(): op = op.GetUp()
        return op.GetNext()

    # get first obj
    first_obj = root_selection #doc.GetFirstObject()
    if not first_obj:
        return None
    # list of all objects in the scene
    list_objs = []
    # add the first obj
    list_objs.append(first_obj) 

    # obj loop iteration
    while first_obj:          
        first_obj = GetNextObject(first_obj)
        if first_obj:
            list_objs.append(first_obj)

    return list_objs

def join_objects(root, doc, merge_tags):
    children = root.GetChildren()
    # set_status("Joining %d objects ..." % len(children), 50)
    # Pre-R18 we need to pass the list of objects to join.
    if c4d.GetC4DVersion() < 18000:
        source = children
    else:
        source = [root]

    settings = c4d.BaseContainer()
    settings[c4d.MDATA_JOIN_MERGE_SELTAGS] = merge_tags

    # collapse objects
    result = c4d.utils.SendModelingCommand(
        c4d.MCOMMAND_JOIN, source,
        c4d.MODELINGCOMMANDMODE_ALL, settings, doc)
    obj = result[0]

    # delete selection tags
    if merge_tags == False:
        obj_tags = obj.GetTags()
        for tag in obj_tags:
            if tag.GetType() == c4d.Tpointselection:
                tag.Remove()
            elif tag.GetType() == c4d.Tedgeselection:
                tag.Remove()
            elif tag.GetType() == c4d.Tpolygonselection:
                tag.Remove()
            else:
                None

    if not obj:
        return None
    return obj

def create_c4d_obj(Obj_ID, name): # create custom objects
    obj = c4d.BaseObject(Obj_ID)
    obj[c4d.ID_BASELIST_NAME] = name
    doc.InsertObject(obj)
    c4d.EventAdd() ; return obj

def add_BBox(source, target):
    # prevent type errors
    if not target or not target.CheckType(c4d.Opoint): return False
    if not source: return False
 
    tBB = target.GetRad()   # Target BoundingBox
    sBB = source.GetRad()   # Source BoundingBox

    sSc = source[c4d.ID_BASEOBJECT_ABS_SCALE] # Source Scale
    sP = source[c4d.ID_BASEOBJECT_ABS_POSITION] # Source Position
    sR = source[c4d.ID_BASEOBJECT_ABS_ROTATION] # Source Rotation
 
    try:    xdif = sBB.x / tBB.x 
    except: xdif = 1.0
    try:    ydif = sBB.y / tBB.y 
    except: ydif = 1.0
    try:    zdif = sBB.z / tBB.z 
    except: zdif = 1.0
 
    for i in xrange(target.GetPointCount()):
        ppos = target.GetPoint(i)
        target.SetPoint(i,c4d.Vector(ppos.x * xdif * sSc.x , ppos.y * ydif * sSc.y , ppos.z * zdif * sSc.z))
        
    target[c4d.ID_BASEOBJECT_ABS_SCALE]     = sSc
    target[c4d.ID_BASEOBJECT_ABS_POSITION]  = sP
    target[c4d.ID_BASEOBJECT_ABS_ROTATION]  = sR

    target.Message(c4d.MSG_UPDATE)

    return target

def main():
    #start undo action
    doc.StartUndo()

    # main ops definitions - future dialog controls
    poly_limit = 10
    merge_tags = False
    keep_parametrics = False
    threshold_parametric = 0.5
    # definir correctamente cuando puede servir el keep parametrics, deberia reconocer que es un objeto original parametrico.
    keep_originals = False
    add_boundingbox = False

    obj = doc.GetActiveObject()

    if not obj.GetType() == c4d.Opolygon: # parametric object convert support
        obj_param = obj.GetClone() # make a parametric backup

        # make a polygon object ops
        poly_obj = c4d.utils.SendModelingCommand(c4d.MCOMMAND_MAKEEDITABLE,[obj]) ; obj = poly_obj[0]
        doc.InsertObject(obj)
        obj_childs = get_allObjs(obj)
        # collapse parametric object
        obj_collapse = join_objects(obj_childs[0], doc, merge_tags)

        # keep parametrics ops
        if keep_parametrics == True:
            obj_polycount = obj_collapse.GetPolygonCount() ; obj_polycount = int(float(obj_polycount) * threshold_parametric)
            print 'Parametric poly count: ' + str(obj_polycount)
            if obj_polycount < poly_limit:
                obj.Remove()
                doc.InsertObject(obj_param)

    obj_polycount = obj.GetPolygonCount()

    print 'obj poly count: ' + str(obj_polycount)

    if obj_polycount > poly_limit:
        print 'poly count is bigger'
        if add_boundingbox == True:
            bbox = create_c4d_obj(c4d.Ocube, obj[c4d.ID_BASELIST_NAME] + '_bbox')
            bbox = c4d.utils.SendModelingCommand(c4d.MCOMMAND_MAKEEDITABLE,[bbox]) ; bbox = bbox[0]
            doc.InsertObject(bbox)
            obj_bbox = add_BBox(obj,bbox)

        if keep_originals == False:
            doc.AddUndo(c4d.UNDOTYPE_DELETE,obj) # add UnDo delete to the UnDo main list
            obj.Remove()
        else:
            None
    else:
        print 'poly count is smaller'
    
    # UnDo ReDo ops
    doc.EndUndo() #end undo action
    doc.DoRedo() #do redo action

    c4d.EventAdd() # update the scene


if __name__=='__main__':
    main()
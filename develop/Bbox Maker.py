'v0.1.0 - wip 01'

"""

Pending:
- Impelemntar bien el uso de varios objetos.
- Revisar por que no colapsa el grupo final de objetos.
- Probar la funcion Make Editable.
- Reemplazar las lineas de hacer editable por la funcion Make Editable.

"""

import c4d

#doc = c4d.documents.GetActiveDocument()

def get_sel_objects(): # get active objects
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        gui.MessageDialog('Please select one or more objects.') ; return None
    return activeObjects

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
    # set_status("Joining %d objects ..." % len(children), 50)
    # Pre-R18 we need to pass the list of objects to join.
    if c4d.GetC4DVersion() < 18000:
        children = root.GetChildren()
        source = children
    else:
        source = [root]

    #doc = c4d.documents.GetActiveDocument()
    doc = c4d.documents.BaseDocument()

    settings = c4d.BaseContainer()
    settings[c4d.MDATA_JOIN_MERGE_SELTAGS] = False

    # collapse objects
    result = c4d.utils.SendModelingCommand(
        c4d.MCOMMAND_JOIN, source,
        c4d.MODELINGCOMMANDMODE_ALL,
        settings,
        doc = doc)
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

def make_editable(obj): # the obj input needs to be a obj list
    # detect if the obj input is a list or not
    try:
        obj[0]
        obj_list = True
    except: 
        obj_list = False
    # add obj into a new list
    if not obj_list:
        obj = [obj]
    # make obj editable
    poly_obj = c4d.utils.SendModelingCommand(c4d.MCOMMAND_MAKEEDITABLE,[obj])
    # return obj only
    obj = poly_obj[0] ; doc.InsertObject(obj) ; return obj

def create_c4d_obj(Obj_ID, name): # create custom objects
    obj = c4d.BaseObject(Obj_ID)
    obj[c4d.ID_BASELIST_NAME] = name
    doc.InsertObject(obj)
    c4d.EventAdd() ; return obj

def add_BBox(source, target): # bounding box definitions
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

    # get selected objecs
    objs = get_sel_objects()
    if not objs:
        return

    obj = objs[0]

    childs = obj.GetChildren()

    childs2 = []

    for child in childs:
        sub_child = child.GetChildren()
        childs2.append(sub_child)

    # obj list to final collapse
    list_to_join = []

    for child in childs2:
        # bounding box ops
        bbox = create_c4d_obj(c4d.Ocube, '_bbox')
        bbox = c4d.utils.SendModelingCommand(c4d.MCOMMAND_MAKEEDITABLE,[bbox]) ; bbox = bbox[0]
        doc.InsertObject(bbox)

        child = [child]

        child_collapse = join_objects(child[0], doc, False)

        obj_bbox = add_BBox(child_collapse,bbox)

    # UnDo ReDo ops
    doc.EndUndo() #end undo action
    doc.DoRedo()  #do redo action

    c4d.EventAdd() # update the scene


if __name__=='__main__':
    main()
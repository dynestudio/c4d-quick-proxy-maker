import c4d

merge_tags = False

doc = c4d.documents.GetActiveDocument()

def get_sel_objects(): # get active objects
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        gui.MessageDialog('Please select one or more objects.') ; return None
    return activeObjects

def create_c4d_obj(Obj_ID, name): # create custom objects
    obj = c4d.BaseObject(Obj_ID)
    obj[c4d.ID_BASELIST_NAME] = name
    doc.InsertObject(obj)
    c4d.EventAdd() ; return obj

def join_objects(root, doc, merge_tags):
    # set_status("Joining %d objects ..." % len(children), 50)
    # Pre-R18 we need to pass the list of objects to join.
    if c4d.GetC4DVersion() < 18000:
        children = root.GetChildren()
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

    # insert the new collapsed object
    doc.InsertObject(obj)

    if not obj:
        return None
    return obj

def main():
    # get selected objecs
    objs = get_sel_objects()
    if not objs:
        print 'no objects selected.' ; return

    null = create_c4d_obj(c4d.Onull, 'main_root')

    # get null center position based form all objects
    # PSR obj lists
    list_pos_X = []
    list_pos_Y = []
    list_pos_Z = []

    list_rot_X = []
    list_rot_Y = []
    list_rot_Z = []

    for obj in objs:
        list_pos_X.append(obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X])
        list_pos_Y.append(obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y])
        list_pos_Z.append(obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z])

        list_rot_X.append(obj[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X])
        list_rot_Y.append(obj[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y])
        list_rot_Z.append(obj[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Z])

    nP = null[c4d.ID_BASEOBJECT_ABS_POSITION]
    nR = null[c4d.ID_BASEOBJECT_ABS_ROTATION]

    px = 0 ; py = 0 ; pz = 0
    rx = 0 ; ry = 0 ; rz = 0

    for pos in list_pos_X:
        px += pos

    for pos in list_pos_Y:
        py += pos

    for pos in list_pos_Z:
        pz += pos

    for rot in list_rot_X:
        rx += rot

    for rot in list_rot_Y:
        ry += rot

    for rot in list_rot_Z:
        rz += rot

    px = px / len(list_pos_X) ; py = py / len(list_pos_Y) ; pz = pz / len(list_pos_Z)
    rx = rx / len(list_rot_X) ; ry = ry / len(list_rot_Y) ; rz = rz / len(list_rot_Z)

    # assign new PSR null value
    nP = c4d.Vector(px, py, pz)
    nR = c4d.Vector(rx, ry, rz)

    null[c4d.ID_BASEOBJECT_ABS_POSITION] = c4d.Vector(px, py, pz)
    null[c4d.ID_BASEOBJECT_ABS_ROTATION] = c4d.Vector(rx, ry, rz)

    c4d.EventAdd()

    # insert all objects inside the root null
    for obj in objs:
        obj.InsertUnder(null)

    # collapse and delete old objs
    obj_collapse = join_objects(null, doc, merge_tags)
    null.Remove()

    # update the scene
    c4d.EventAdd()

# ----------------

main()
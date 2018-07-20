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

    print obj

    print 'Checkpoint 02'

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
        print 'no hay objetos' ; return

    print "checkpoint 00"

    print objs

    print "checkpoint 01"
    null = create_c4d_obj(c4d.Onull, 'main_root')
    for obj in objs:
        print obj
        obj.InsertUnder(null)

    print null

    nP = null[c4d.ID_BASEOBJECT_ABS_POSITION]
    nR = null[c4d.ID_BASEOBJECT_ABS_ROTATION]

    print nP
    print nR

    obj_collapse = join_objects(null, doc, merge_tags)
    null.Remove()

    #obj_collapse = join_objects(objs[0], doc, merge_tags)

    print "checkpoint 03"

    print obj_collapse

    print 'checkpoint 04'

    c4d.EventAdd()

# ----------------

main()
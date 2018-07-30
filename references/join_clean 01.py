import c4d

doc = c4d.documents.GetActiveDocument()

def join_objects(root, doc, merge_tags):
    # Pre-R18 we need to pass the list of objects to join.
    if c4d.GetC4DVersion() < 18000:
        children = root.GetChildren()
        source = children
    else:
        source = [root]

    settings = c4d.BaseContainer()
    settings[c4d.MDATA_JOIN_MERGE_SELTAGS] = False

    # collapse objects
    result = c4d.utils.SendModelingCommand(
        c4d.MCOMMAND_JOIN, source,
        c4d.MODELINGCOMMANDMODE_ALL,
        settings,
        doc = doc)
    obj = result[0]

    if not obj:
        return None
    return obj

def main():
    # get selected objecs
    op = doc.GetActiveObjects()
    if not op:
        return

    obj = objs[0]

    childs = obj.GetChildren()

    childs2 = []

    for child in childs: # sub level 3 of childs
        sub_child = child.GetChildren()
        childs2.append(sub_child)

    for child in childs2:
        child = [child]
        child_collapse = join_objects(child[0], doc, False)

    c4d.EventAdd() # update the scene


if __name__=='__main__':
    main()
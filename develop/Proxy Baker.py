'v01'

"""
Pending:

- Definir que hacer si el objeto no es un poly object
- Hacer editable si no es un poly obj?

"""


import c4d


poly_limit = 10

def MakeEditable(op):

    if debug: print "MakeEditable()"

    if (not op) | op.CheckType(c4d.Opolygon) | op.CheckType(c4d.Ospline): return op



    op = [op.GetClone()]

    doc = c4d.documents.BaseDocument()

    doc.InsertObject(op[0],None,None)

    op = c4d.utils.SendModelingCommand(

                              command = c4d.MCOMMAND_MAKEEDITABLE,

                              list = op,

                              mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION,

                              doc = doc )

    return op[0]


def main():

    #start undo action
    doc.StartUndo()

    obj = doc.GetActiveObject()

    if not obj.GetType() == c4d.Opolygon:
        obj = MakeEditable(obj)
        print obj
        print 'no es un polygon'
        return

    obj_polycount = obj.GetPolygonCount()

    print 'obj poly count: ' + str(obj_polycount)

    if obj_polycount > poly_limit:
        print 'poly count is bigger'
        doc.AddUndo(c4d.UNDOTYPE_DELETE,obj) # add UnDo delete to the UnDo main list
        obj.Remove()
    else:
        print 'poly count is smaller'
    
    # UnDo ReDo ops
    doc.EndUndo() #end undo action
    doc.DoRedo() #do redo action

    c4d.EventAdd() # update the scene


if __name__=='__main__':
    main()


"""
c4d.utils.SendModelingCommand(c4d.MCOMMAND_JOIN,[objs])
MCOMMAND_MAKEEDITABLE


"""
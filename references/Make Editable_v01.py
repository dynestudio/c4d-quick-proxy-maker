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

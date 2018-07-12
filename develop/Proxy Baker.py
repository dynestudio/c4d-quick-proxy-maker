'v01'

"""
Pending:

- UnDo y ReDo
- evitar errores de que si el objeto activo no es un poly object.
- Definir que hacer si el objeto no es un poly object
- Check type o Get Type?
- Hacer editable si no es un poly obj?

"""


import c4d


poly_limit = 10


def main():

    obj = doc.GetActiveObject()

    obj_pc = obj.GetPolygonCount()

    print 'obj poly count: ' + str(obj_pc)

    if obj_pc > poly_limit:
        print 'poly count is bigger'
        obj.Remove()
    else:
        print 'poly count is smaller'

    c4d.EventAdd() # update the scene


if __name__=='__main__':
    main()


# c4d.utils.SendModelingCommand(c4d.MCOMMAND_JOIN,[objs])
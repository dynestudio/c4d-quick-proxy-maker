import  c4d
from    c4d.documents   import GetActiveDocument
#from    c4d.gui         import GeDialog
#from    threading       import Thread
# Version 1.1
def GetNextObject(op): #root only version   
    if not op: return
    return op.GetNext()

def numberofobjects(op):
    counter = 0
    while op:         
        counter += 1            
        op = GetNextObject(op)
    return counter

def statusbar (counter, secondcounter):
    # c4d.StatusSetText ('%s - %s Objects are processed.' %(secondcounter, counter))    
    c4d.StatusSetBar(100*secondcounter/counter) #statusbar

def selchildren(obj,next): # Scan obj hierarchy and select children
    while obj and obj != next:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL,obj)
        obj.SetBit(c4d.BIT_ACTIVE)
        selchildren(obj.GetDown(),next)
        obj = obj.GetNext()
    c4d.EventAdd()
    return True

def main(undo = True):
    now = c4d.GeGetTimer() # start stopwatch
    c4d.CallCommand(13957) # Konsole lÃ¶schen
    # c4d.CallCommand(12305) # Konsole...

    if GetActiveDocument():
        doc     = GetActiveDocument()
        if doc.GetFirstObject():
            c4d.StatusSetSpin()
            op = doc.GetFirstObject()
            myobject = op
            counter = numberofobjects(op)
            secondcounter = 0
            c4d.StatusSetText ('%s Objects are processed.' %(counter))
            opactive = None
        else:
            print "Error: No Objects"
            return False
    else:
        print "Error: No Document"
        return False
    
    #doc.StartUndo() # Start undo support
    # iterate over all objects in the document
    c4d.CallCommand(12113) # Alles deselektieren
    
    while op:
        
        optemp = op
        op = GetNextObject(op) # get next object    
            
        secondcounter += 1        
        statusbar(counter, secondcounter)

        if optemp.CheckType(c4d.Opolygon):
            optemp.SetBit(c4d.BIT_ACTIVE)
  
            if selchildren(optemp,optemp.GetNext()):
                c4d.CallCommand(16768) #Connect And Delete
                c4d.CallCommand(16768) #Connect And Delete
            
            opactive = doc.GetActiveObject()
            opactive.DelBit(c4d.BIT_ACTIVE)
                    
        optemp.DelBit(c4d.BIT_ACTIVE)
            

    c4d.StatusClear()
    #doc.EndUndo() # Do not forget to close the undo support
    c4d.EventAdd()        # update cinema 4d
    print 'END OF SCRIPT %s ms ' %(c4d.GeGetTimer() - now)
    return 
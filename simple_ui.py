import maya.cmds as cmds

def createUI (pWindowTitle, pApplyCallback):
    
    windowID = 'MyWindowID'
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
        
    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,75),(2,60),(3,60)], columnOffset=[(1,'right',3)])

    cmds.text(label='Time Range:') 
    startTimeField = cmds.intField()
    endTimeField = cmds.intField()
    
    cmds.text(label='Attribute:')
    targetAttributeField = cmds.textField()
    
    cmds.separator(h=10, style='none')
    
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    
    cmds.separator(h=10, style='none')
    
    cmds.button(label='Apply', command=pApplyCallback)    
    
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    
    cmds.button(label='Cancel', command=cancelCallback)    
        
    cmds.showWindow()
        
def applyCallback(*pArgs):
    print 'Apply pressed'
        
createUI('My title', applyCallback)
#keyRotation.py

import maya.cmds as cmds

def keyFullRotation(pObjectName, pStartTime, pEndTime, pTangentAttribute):
            
    # Enable key on selected objects
    cmds.cutKey(pObjectName, time=(pStartTime, pEndTime), attribute=pTangentAttribute)
            
    # Set keyframes
    cmds.setKeyframe(pObjectName, time=pStartTime, attribute=pTangentAttribute, value=0)
    cmds.setKeyframe(pObjectName, time=pEndTime, attribute=pTangentAttribute, value=360)
    
    # Set linear tangent
    cmds.selectKey(pObjectName, time=(pStartTime, pEndTime), attribute=pTangentAttribute)
    cmds.keyTangent(inTangentType='linear', outTangentType='linear')

selectionList = cmds.ls(selection=True, type='transform')

if len(selectionList) >= 1:
    
    # Defining the time range
    startTime = cmds.playbackOptions(query=True, minTime=True)
    endTime = cmds.playbackOptions(query=True, maxTime=True)
    
    for objectName in selectionList:
        
        keyFullRotation(objectName, startTime, endTime, 'rotateY')
    
else:
    print 'Select at least one object'



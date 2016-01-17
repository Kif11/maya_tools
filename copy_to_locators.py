VERSION 1.0



import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

selection = cmds.ls(sl=True)

# Check if two or more obj selected
if len(selection) < 2:
    OpenMaya.MGlobal.displayError("Select at least two objects")

for object in selection[:-1]:
    
    cmds.select(selection[-1:])
    new_obj = cmds.instance()
    
    trans = cmds.xform(object, q=True, ws=True, rp=True)
    cmds.xform(new_obj, a=True, ws=True, t=trans)
    cmds.parent(new_obj, object)



VERSION 1.1



# Copy to locator

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

selection = cmds.ls(sl=True)

# Check if two or more obj selected
if len(selection) < 2:
    OpenMaya.MGlobal.displayError("Select at least two objects")

for object in selection[:-1]:
    
    cmds.select(selection[-1:])
    new_obj = cmds.instance()[0]
    
    # Set position
    trans = cmds.xform(object, q=True, ws=True, rp=True)
    cmds.move(trans[0],trans[1],trans[2], new_obj, a=True, ws=True, rpr=True)
 
    # Set rotation
    rot = cmds.getAttr(object + ".r")[0] 
    cmds.setAttr(new_obj + ".rotate", rot[0],rot[1],rot[2])
    
    cmds.parent(new_obj, object)

VERSION 1.2

# Copy to locator

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

replace = 0
copy = 0

selection = cmds.ls(sl=True)

# Check if two or more obj selected
if len(selection) < 2:
    OpenMaya.MGlobal.displayError("Select at least two objects")

for object in selection[:-1]:
    
    cmds.select(selection[-1:])
    
    if copy:
        new_obj = cmds.duplicate()[0]
    else:
        new_obj = cmds.instance()[0]
    
    # Set position
    trans = cmds.xform(object, q=True, ws=True, rp=True)
    cmds.move(trans[0],trans[1],trans[2], new_obj, a=True, ws=True, rpr=True)
 
    # Set rotation
    rot = cmds.getAttr(object + ".r")[0] 
    cmds.setAttr(new_obj + ".rotate", rot[0],rot[1],rot[2])
    
    if replace:
        cmds.delete(object)
    else:
        cmds.parent(new_obj, object)
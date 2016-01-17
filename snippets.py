###############################
# Collection of Maya snippets #
###############################

################################################################################
# Create randomly scattered cubes

import maya.cmds as cmds
import random

random.seed(1234)

# Deleting cubes
cubeList = cmds.ls('myCube')
if len(cubeList) > 0:
    cmds.delete(cubeList)

# Body
result = cmds.polyCube(w=1, h=2, d=1, name='myCube#');
transformName = result[0]
instanceGroupName = cmds.group(empty=True, name=transformName + '_instance_grp#')
for i in range(0,50)
    instanceResult = cmds.instance(transformName, name=transformName+'instance#')
    cmds.parent(instanceResult, instanceGroupName)
    x = random.uniform(-10,10)
    y = random.uniform(0,20)
    z = random.uniform(-10,10)
    cmds.move(x,y,z, instanceResult)

cmds.xform(instanceGroupName, centerPivot=True)

################################################################################
# Texture replace

import maya.cmds as cmds
import os

imgPath = "img/hill/"
materials = cmds.ls(type="VRayMtl")

for mat in materials:
    files = cmds.listConnections(mat, type="file")
    if files:
        for fileNode in files:
            texturePathAttr = cmds.getAttr(fileNode + ".fileTextureName")
            fileName = os.path.split(texturePathAttr)[1]
            cmds.setAttr(fileNode + ".fileTextureName", imgPath + fileName, type="string")

################################################################################
#

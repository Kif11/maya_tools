import os

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def alignTwoObj(obj1, obj2):
	objPos = cmds.xform(obj2, q=1, ws=1, rp=1)
	objRot = cmds.xform(obj2, q=1, ro=True)
	cmds.move(objPos[0], objPos[1], objPos[2], obj1, rpr=True)
	cmds.rotate(objRot[0], objRot[1], objRot[2], obj1, r=True)
	cmds.select(obj1)

def cleanUpGeo():
	"""
	Delete history, Freeze transform etc.
	"""
	selection = cmds.ls(selection=True)
	for node in selection:
		cmds.makeIdentity(node, apply=True, t=1, r=1, s=1, n=0)
		cmds.delete(node, ch=True)

def rename():
	"""
	Rename multiple objects with proper number itterator
	"""
	selection = cmds.ls(selection=True)

	msg = cmds.promptDialog(
        title='Rename Object',
		message='Enter Name:',
		button=['OK', 'Cancel'],
		defaultButton='OK',
		cancelButton='Cancel',
		dismissString='Cancel')

	if msg == 'OK':
		msgText = cmds.promptDialog(query=True, text=True)

	count = 1
	for node in selection:
		cmds.rename(node, "%s_%03d" %(msgText, count))
		count += 1

def exportToAbc():
	selection = cmds.ls(selection=True, o=True)
	# Build correct path for alembic export
	forExport = ""
	for node in selection:
		root = " -root |%s" %node
		forExport = forExport + root

	# Export Alembic
	cmds.AbcExport(j="-frameRange 1 1 -uvWrite %s -file %s.abc" % (forExport, selection[0]))

def pivotToMin():
	"""
	Move pivot to lowest point of geometry
	"""
	selection = cmds.ls(selection=True, o=True)
	for node in selection:
		bbox = cmds.xform(node, q=True, ws=True, bb=True)
		cmds.xform(node, ws=False, piv=((bbox[0]+bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2))

def unparentGeo(selection):
	"""
	Extract geometry from hierarchy
	"""
    shapesInSelection = cmds.listRelatives(selection, typ="mesh", ad=True, f=True)
    for shape in shapesInSelection:
        try:
            ioAttr = cmds.getAttr(shape + ".io")
            if not(ioAttr):
                transformOfShape = cmds.listRelatives(shape, p=True, f=True)
                cmds.parent(transformOfShape, w=True)
        except: pass

def importABCasVRMesh():
	"""
	Import Alembic as VRMesh
	"""
	pathPick = cmds.fileDialog()
	path = os.path.split(pathPick)[1]
	name = path.split(".")[0]

	# Export alembic as VRMesh
	mel.eval('vrayCreateProxyExisting("%s", "geo/%s")' % (name, path))

def copyOnSelected(i=False, r=False):
	# i - instance
	# r - replace
	selection = cmds.ls(selection=True, o=True)
	for node in selection[1:]:
		if i:
			inst = cmds.instance(selection[0])
		else:
			inst = cmds.duplicate(selection[0])
		alignTwoObj(inst, node)
		if r:
			cmds.delete(node)

def copyToLocators(replace=False, instance=False):

	selection = cmds.ls(sl=True)

	# Check if two or more obj selected
	if len(selection) < 2:
	    OpenMaya.MGlobal.displayError("Select at least two objects")

	for object in selection[:-1]:

	    cmds.select(selection[-1:])

	    if not instance:
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

def deleteParents():
	selection = cmds.ls(sl=True)
	# Check if two or more obj selected
	if len(selection) < 1:
	    OpenMaya.MGlobal.displayError("Select at least two objects")

	for object in selection:
	    parents = cmds.listRelatives(object)[1:]
	    print parents
	    for i in parents:
	        cmds.delete(i)
	        print parents, 'has been deleted'

def appendToInstance():
	selection = cmds.ls(sl=True)
	first_object = selection[0]

	# Collect data
	pivot = cmds.xform(first_object, q=True, ws=True, rp=True)

	# List shapes of selected transform
	shapeOfSelection = cmds.listRelatives(first_object)

	# List parents of selected shape
	instances = cmds.listRelatives(shapeOfSelection[0], ap=True)

	# Combine
	new_mesh = cmds.polyUnite()
	# Set pivot back
	cmds.xform(new_mesh, rp=pivot)

	print instances

	for obj in instances:
	    cmds.parent(new_mesh[0], obj, r=True, s=True, add=True)
	    print obj,'moved to', cmds.xform(obj, q=True, ws=True, rp=True)

	#print "first" ,first_object
	#print "new_mesh", new_mesh
	#cmds.rename(new_mesh[0], first_object)

	# Delete junk objects

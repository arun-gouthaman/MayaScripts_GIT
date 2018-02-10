import pymel.all as pm
import maya.OpenMaya as OpenMaya
from CustomScripts import midPosVec
from TreadCreateScript import createTreadExpression

## Scripts from Marco ##
def getDagPath( objectName):
    if isinstance(objectName, list)==True:
        oNodeList=[]
        for o in objectName:
            selectionList = OpenMaya.MSelectionList()
            selectionList.add(o)
            oNode = OpenMaya.MDagPath()
            selectionList.getDagPath(0, oNode)
            oNodeList.append(oNode)
        return oNodeList
    else:
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(objectName)
        oNode = OpenMaya.MDagPath()
        selectionList.getDagPath(0, oNode)
        return oNode

def getuParamVal(pnt = [], crv = None):
    point = OpenMaya.MPoint(pnt[0],pnt[1],pnt[2])
    curveFn = OpenMaya.MFnNurbsCurve(getDagPath(crv))
    paramUtill=OpenMaya.MScriptUtil()
    paramPtr=paramUtill.asDoublePtr()
    isOnCurve = curveFn.isPointOnCurve(point)
    if isOnCurve == True:
        
        curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kWorld )
    else :
        point = curveFn.closestPoint(point,paramPtr,0.001,OpenMaya.MSpace.kWorld)
        curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kWorld )
    param = paramUtill.getDouble(paramPtr)  
    return param
## Scripts from Marco ##

"""
Creates tread set up by placing joints at selected positions on the curve and 
applying motion path with the curve and maintaining the offset U value
create locators (or other objects) on the curve or close to curve
select the position objects created and run the below script
"""
def treadAtPoints(**kwargs):
    #get inputs
    tread_name = kwargs.get("tr_name", "Tread")
    crv = kwargs.get("path_crv", None)
    crv = str(pm.duplicate(crv, name = str(tread_name)+"PathCrv")[0])
    pm.xform(crv, centerPivots=True)
    #obtain curve length
    full_length = pm.arclen(crv)
    paramVal = []
    uVal = []
    # get param value on the curve at each position selected (locators)
    sel_obj = pm.ls(selection = True)
    for obj in sel_obj:
        pos = pm.xform(obj, query=True, translation=True, worldSpace=True)
        param = getuParamVal(pos, crv)
        paramVal.append(param)
    crv_shp = pm.listRelatives(crv, shapes = True)[0]
    # create arc length dimension tool
    arcLen = pm.arcLengthDimension(crv_shp+".u[0]")
    # for each param value obtained set the arc length tool attribute and 
    # store the length of curve at that param value
    # normalize the curve to obtain the motion path U value at each position
    for val in paramVal:
        pm.setAttr(str(arcLen)+".uParamValue", val)
        len_at_pos = pm.getAttr(str(arcLen)+".arcLength")
        uVal.append(len_at_pos/full_length)
    pm.delete(arcLen)
    mthPthLst = []
    jntLst = []
    # create joints, assign motion path and set U value obtained
    for u in uVal:
        pm.select(clear = True)
        jnt = pm.joint()
        jntLst.append(jnt)
        pathanim = pm.pathAnimation(jnt, curve = crv, fractionMode = True, follow = True, followAxis = "x",
                         worldUpType = "vector", worldUpVector = (0,1,0))
        mthPthLst.append(pathanim)
        pm.setAttr(str(pathanim)+".uValue", u)
        pm.disconnectAttr(str(pathanim)+".u")
        # create up locator at mid point of all joints
    #loc_pos = midPos(selected_items = jntLst)
    #loc_pos = pm.xform(crv, query=True, translation=True, worldSpace=True)
    loc_pos = midPosVec(objects = jntLst)
    loc = pm.spaceLocator()
    pm.xform(loc, translation = loc_pos, worldSpace = True)
    for mtPth in mthPthLst:
        pm.pathAnimation(mtPth, edit=True, worldUpType = "object", worldUpObject = loc)
    # create control curve, add run and speed attributes
    control_crv = pm.circle(name = tread_name+"CTRL", normalX = 1, normalY = 0, normalZ = 0)   
    pm.xform(control_crv, translation = loc_pos)
    pm.select(clear=True)  
    pm.addAttr(control_crv, longName = "run", attributeType = "float", keyable = True)
    pm.addAttr(control_crv, longName = "speed", attributeType = "float", keyable = True, minValue = 0.0, defaultValue = 0.5)
    # group the tread setup
    pm.parent(crv, control_crv)
    pm.parent(loc, control_crv)
    pm.select(clear=True)
    gp = pm.group(name = tread_name+"GP")
    pm.select(clear=True)
    jnt_gp = pm.group(jntLst, name = tread_name+"JNTGP")
    pm.xform(gp, translation = loc_pos)
    pm.parent(control_crv, gp)
    pm.parent(jnt_gp, gp)
    createTreadExpression(mtnPth = mthPthLst, runAttr = str(control_crv[0])+".run", speedAttr = str(control_crv[0])+".speed", exp_nm = tread_name)
    return None
    
#treadAtPoints(pathCrv = "nurbsCircle1", tr_name = "testTread")
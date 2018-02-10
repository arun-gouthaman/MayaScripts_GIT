## Copy joint Orientation ##
import pymel.all as pm
import maya.OpenMaya as OpenMaya

## Assign Orientation
def CopyJntOri(**kwargs):
    """
	    Copy orientation of one joint to another
	"""
    sel = pm.ls(selection=True)
    sel_jnts = kwargs.get("joint_selection", sel)
    print sel_jnts
    ref = sel_jnts.pop(0)
    for jnt in sel_jnts:
        ori_cnst = pm.orientConstraint(ref, jnt, maintainOffset=False)
        pm.delete(ori_cnst)
        pm.makeIdentity(apply=True, rotate=True)
    return None

## Delete constraints	
def delCon(**kwargs):
    """
        Delete selected constraints on selected objects if exists
    """
    print "deleteCon"
    sel = pm.ls(selection=True)
    #con_typ = kwargs.get("constraint_type", None)
    prFlg = kwargs.get("pr_con", False)
    scFlg = kwargs.get("sc_con", False)
    ptFlg = kwargs.get("pt_con", False)
    orFlg = kwargs.get("or_con", False)
    
    for obj in sel:
            if prFlg:
                const = pm.parentConstraint(obj, query=True)
                if const:
                    pm.delete(const)
                else:
                    print str(obj)+" parent delete skipped"
                    
            if orFlg:
                const = pm.orientConstraint(obj, query=True)
                if const:
                    pm.delete(const)
                else:
                    print str(obj)+" orient delete skipped"
    
            if ptFlg:
                const = pm.pointConstraint(obj, query=True)
                if const:
                    pm.delete(const)
                else:
                    print str(obj)+" point delete skipped"
            #if con_typ == "aim":
            #	const = pm.aimConstraint(obj, query=True)
            #	if const:
            #		pm.delete(const)
                    
            if scFlg:
                const = pm.scaleConstraint(obj, query=True)
                if const:
                    pm.delete(const)
                else:
                    print str(obj)+" scale delete skipped"
    return None

##  Immediate parent in chain ##	
def immediateParent(**kwargs):
    """
        Insert an immediate parent node to the selected object with
        the selected object position as reference to parent
    """
    group_name = kwargs.get("name", "null")
    sel_obj = pm.ls(selection=True)
    if not sel_obj:
        pm.group(name = group_name)
        return None
    for obj in sel_obj:
        parent_node = pm.listRelatives(obj, parent=True)
        pm.select(clear = True)
        group_name = str(obj)+"_Znode"		
        null = pm.group(name = group_name)
        pm.parentConstraint(obj, null, maintainOffset=False, name = "temp_const")
        pm.delete("temp_const")
        if parent_node:
			pm.parent(null, parent_node)
        pm.parent(obj, null)
    return None


## Returns mid position from selected positions
def midPos(**kwargs):
    """
        Returns the mid point from selected positions(objects or components)
    """
    selected_items = kwargs.get("selected_items", [])
    temp_cluster = pm.cluster(selected_items)[1]
    cluster_shape = temp_cluster.getShape()
    mid_position = cluster_shape.origin.get()
    pm.delete(temp_cluster)
    return mid_position

    
    
    
def midPosVec(**kwargs):
    """
        Returns the mid point from selected positions(objects or components)
    """
    selected_items = kwargs.get("objects", [])
    if not selected_items:
        selected_items = pm.ls(selection=True, flatten=True)
    if not isinstance(selected_items, list):
        print "please provide objects list"
        pm.displayInfo("please provide objects list")
        return None
    number_of_items = len(selected_items)
    position_vector = []
    final_vector = OpenMaya.MVector(0,0,0)
    for index in range(number_of_items):
        pos = pm.xform(selected_items[index], query=True, worldSpace=True, translation=True)
        vec = OpenMaya.MVector(pos[0], pos[1], pos[2])
        position_vector.append(vec)
    
    for vector_index in range(len(position_vector)):
        final_vector = final_vector + position_vector[vector_index]
    
    final_vector = final_vector/len(position_vector)
    mid_position = [final_vector.x, final_vector.y, final_vector.z]
    return mid_position    
    
    
    
    
    
## Insert joint at midposition between 2 joints ##
def insJnt():
	selected = pm.ls(selection=True)
	for index in range(len(selected)-1):
		mid_pos = midPos(selected_items = [selected[index], selected[index+1]])
		new_joint = pm.insertJoint(selected[index])
		pm.joint(new_joint, edit=True, component = True, position = mid_pos)
	return None

	
## Turn off joints Draw Style ##	
def jntHide():
    sel_obj = pm.ls(selection=True)
    for obj in sel_obj:
        obj.drawStyle.set(2)

## Turn off LOD visibility ##
def lodOff():
	sel = pm.ls(selection=True)
	for obj in sel:
		shp = pm.listRelatives(obj, shapes = True)[0]
		shp.lodVisibility.set(0)
	return None

	
## Joint at mid position ##
def jntAtmid(**kwargs):
    sel_items = pm.ls(selection=True, flatten=True)
    mid_position = midPos(selected_items = sel_items)
    pm.select(clear=True)
    pm.joint(position = mid_position)
    return None

##Copy an object to selected positions and constraint them based on 
##options selected
def copyObjects(**kwargs):
    """
        Input object to be copied
        select positions where the objects needs be copied and run the script
        the copied object constraints the position objects if options are selected
    """
    print "TEST"
    obj = kwargs.get("obj", "")
    prFlg = kwargs.get("prFlg", False)
    scFlg = kwargs.get("scFlg", False)
    sel = pm.ls(selection=True, flatten=True)
    ch = None
    for comp in sel:
        pos = pm.xform(comp, query=True, worldSpace=True, translation=True)
        new_obj = pm.duplicate(obj)
        pm.xform(new_obj,worldSpace=True, translation = pos)
        if prFlg or scFlg:
            typ = str(pm.nodeType(comp))
            if typ == "transform":
                ch = comp
            else:
                shp = pm.ls(comp, objectsOnly=True)[0]
                trn = pm.listRelatives(shp, parent=True)[0]
                ch = trn
            if prFlg:
                pm.parentConstraint(new_obj, ch, maintainOffset=True)
            if scFlg:
                pm.scaleConstraint(new_obj, ch, maintainOffset=True)
    return None

	
## Parent constraint single parent to multiple children ##
def constMult(**kwargs):
    """
        parent constraint multiple child to single parent
    """
    prnt = kwargs.get("prntObj", "")
    prnt_con = kwargs.get("pr_cons", False)
    scl_con = kwargs.get("sc_cons", False)
    sel = pm.ls(selection=True)
    if prnt == "":
        prnt = sel.pop(0)
    for obj in sel:
        if prnt_con:
            pm.parentConstraint(prnt, obj, maintainOffset = True)
        if scl_con:
            pm.scaleConstraint(prnt, obj, maintainOffset = True)
    return None


##Returns parent and child selected in consequtive order
def getSet(**kwargs):
    """
        Returns sets of parents and children as 2 different list
        Selection order : parent1, child1, parent2, child2,...,parentN, childN
    """
    sel = kwargs.get("sel", [])
    prnt = []
    chld = []
    i = 0
    while i<len(sel):
        prnt.append(sel[i])
        i+=1
        chld.append(sel[i])
        i+=1
    return prnt, chld

## constraints parent and child in selection set order
def setCon(**kwargs):
    """
        constraints parent child in selection set
    """
    sel_obj = pm.ls(selection=True)
    if not len(sel_obj)%2==0:
        print "please select parent child in pairs"
        return None
    prFlg = kwargs.get("pr_cons", False)
    scFlg = kwargs.get("sc_cons", False)
    pr, ch = getSet(sel = sel_obj)
    pm.select(clear=True)
    for prnt in pr:
        index = pr.index(prnt)
        if prFlg:
            pm.parentConstraint(prnt, ch[index], maintainOffset=True)
        if scFlg:
            pm.scaleConstraint(prnt, ch[index], maintainOffset=True)
    return None

##parent objects one under another in selection order
def parentChain():
    """
        Parent objects one under another in selected order, with first selection
        at top
    """
    sel = pm.ls(selection = True)
    count = len(sel)
    #print count
    for index in range(count-1):
        #print index
        pm.parent(sel[index+1], sel[index])
    return None

def get_vrts(**kwargs):
    sel = kwargs.get("sel_obj", [])
    #print sel
    #sel = pm.ls(selection=True)
    tmp_vrt_lst = []
    vrt_lst = []
    for obj in sel:
        #print obj
        vert_count = pm.polyEvaluate(obj, vertex=True)
        for i in range(vert_count+1):
            tmp_vrt_lst.append(str(obj)+".vtx["+str(i)+"]")
        vrt_lst.append(tmp_vrt_lst)
        tmp_vrt_lst = []
    return vrt_lst

    
    
def curve_through_points(**kwargs):
    selection_points = kwargs.get("selection_points", None)
    curve_degree = kwargs.get("curve_degree", 3)
    curve_name = kwargs.get("curve_name", "Curve")
        
    if not selection_points:
        selection_points = pm.ls(selection=True)
        if not selection_points:
            pm.displayInfo("Please select reference points")
            return None            
    if len(selection_points)<curve_degree+1:
        pm.displayInfo("please select more than "+str(curve_degree+1)+" points")
        return None
    
    points_locations = []
    for point in selection_points:
        points_locations.append(pm.xform(point, query=True, translation=True, worldSpace=True))
    pm.select(clear=True)
    current_curve = pm.curve(degree = curve_degree, worldSpace=True, point = points_locations)
    pm.rename(current_curve, curve_name)
    return current_curve

def joints_along_curve(**kwargs):
    number_of_joints = kwargs.get("number_of_joints", 2)
    bind_curve = kwargs.get("bind_curve_to_joint", False)
    curve = kwargs.get("curve", None)
    
    if not isinstance(curve, pm.PyNode):
	curve = pm.PyNode(bind_curve)
    crv_len = curve.length()
    parts = number_of_joints-1
    div = float(crv_len)/float(parts)
    len_lst = [0]
    inc = 0
    for i in range(1,parts+1):
	inc += div
	len_lst.append(inc)
    joint_lst = []
    for val in len_lst:
	pm.select(clear=True)
	param = curve.findParamFromLength(val)
	point = curve.getPointAtParam(param)
	jnt = pm.joint(position = point, radius = 3)
        joint_lst.append(jnt)
    if bind_curve:
	pm.skinCluster(joint_lst, curve)
    return joint_lst
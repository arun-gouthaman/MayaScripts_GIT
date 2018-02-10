import pymel.all as pm

from CustomScripts import curve_through_points, joints_along_curve

def stretch_expression(**kwargs):
    """
    create curve info node to get the length of the initial curve for reference
    edit the script to change the curveInfo node name as used in the scene
    select the joints connected to stretching curve and run the  below scrip
    add conditional statements in expression editor if the stretch is controlled by user attribute
    
    divide the "curve_length" variable with global scale value if used
    """
    
    #sel_jnts= pm.ls(selection=True)
    sel_jnts = kwargs.get("joints", [])
    curve_info_node = kwargs.get("curve_info_node", None)
    global_scale_attribute = kwargs.get("scale_attribute", None)
    expression_name = kwargs.get("expression_name", "ik_sretch_expression")
    connect_scale = kwargs.get("connect_scale", False)
    control_attribute = kwargs.get("ctrl_attr", None)
    global_scale = kwargs.get("glbl_scl_stat", False)
    global_attr = kwargs.get("glbl_scl_attr", None)
    
    
    count = str(len(sel_jnts)-1)
    #curve_length = "spine_curve_info.arcLength"
      
    curve_length =  str(curve_info_node)+".arcLength"
    main_expression_name = expression_name
    
    
    exp_scale_str = ""
    exp_def_scale_str = ""       
    exp_init_str = ""
    exp_stretch_str = ""
    exp_def_stretch_str = ""
    string_exp_str = ""
    arc_len_str = ""
    
    
    
    for jnt in sel_jnts:
        exp_init_str = exp_init_str+"float $joint"+str(sel_jnts.index(jnt))+"_tx"+"="+str(jnt.translateX.get())+";\n"
        exp_stretch_str = exp_stretch_str + str(jnt)+".translateX = $joint"+str(sel_jnts.index(jnt))+"_tx + $len_diff;\n"
        exp_def_stretch_str = exp_def_stretch_str + str(jnt)+".translateX = $joint"+str(sel_jnts.index(jnt))+"_tx;\n"    
    

    
    if connect_scale:
        for jnt in sel_jnts:
            exp_scale_str = exp_scale_str + str(jnt)+".scaleY = $scale_val;\n"
            exp_scale_str = exp_scale_str + str(jnt)+".scaleZ = $scale_val;\n"
            exp_def_scale_str = exp_def_scale_str + str(jnt)+".scaleY = 1;\n"
            exp_def_scale_str = exp_def_scale_str + str(jnt)+".scaleZ = 1;\n"
    
    init_arc_length = str(pm.getAttr(curve_length))


    if (global_scale):
        arc_len_str = "float $arc_len = "+curve_length+"/"+global_attr+";\n"
    else:
        arc_len_str = "float $arc_len = "+curve_length+";\n"
    
    string_exp_str = arc_len_str+exp_init_str+\
    """if ($arc_len != """+init_arc_length+""" && """+control_attribute+"""==1)
    {
    float $len_diff = ($arc_len - """+init_arc_length+""")/"""+count+""";\n"""+exp_stretch_str+\
    """float $scale_val = (-($arc_len - """+init_arc_length+""")/100)+1;\n"""+exp_scale_str+\
    """}
    else
    {\n"""+exp_def_stretch_str+exp_def_scale_str+\
    """}"""

    print string_exp_str
    pm.expression(name = main_expression_name, string = string_exp_str)
    
    
    return None



def dense_chain(**kwargs):
    import pymel.core.datatypes as dt
    joints = kwargs.get("joints", None)
    joints_inbetween = kwargs.get("joints_inbetween", 5)
    if not joints:
        joints = pm.ls(selection=True)
    joints.pop(-1)
    for jnt in joints:
        child = jnt.getChildren()
        pos = pm.xform(jnt, query=True, translation=True, worldSpace=True)
        vpos1 = dt.Vector(pos)
        pos = pm.xform(child[0], query=True, translation=True, worldSpace=True)
        vpos2 = dt.Vector(pos)
        vpos = vpos2-vpos1
        div_vec = vpos/(joints_inbetween+1)
        out_vec = vpos1
        cur_jnt = jnt
        for i in range(joints_inbetween):
            out_vec = (out_vec+div_vec)
            pos = [out_vec.x, out_vec.y, out_vec.z]
            new_jnt = pm.insertJoint(cur_jnt)
            pm.joint(new_jnt, edit=True, component=True, position = pos, name = str(i))
            cur_jnt = new_jnt
    return None


def setup_ik_spline(**kwargs):
    curve = kwargs.get("curve", None)
    joint_chain = kwargs.get("joint_chain", None)
    auto_curve = kwargs.get("auto_curve", True)
    use_curve = kwargs.get("use_curve", None)
    spans = kwargs.get("number_of_spans", 4)
    ctrl_jnts = kwargs.get("num_control_joints", 3)
    ik_name = kwargs.get("ik_name", "ikHandle")
    scale_stretch = kwargs.get("scale_stretch", False)
    create_dense_chain = kwargs.get("dense_chain", False)
    dense_division = kwargs.get("dense_chain_divisions", 3)
    auto_simplify = kwargs.get("auto_simplify_curve", False)
    stretch_exp = kwargs.get("stretch_exp", False)
    global_scale_check = kwargs.get("global_scale_check", False)
    global_scale_attr = kwargs.get("global_scale_attr", None)
    
    
    
    pm.select(joint_chain, hierarchy=True)
    joint_chain = pm.ls(selection=True)
    if not isinstance(joint_chain[0], pm.Joint):
        pm.displayInfo("selection should be of type joint")
        return None
    if len(joint_chain) < 2:
        pm.displayInfo("Chain should consist of more than one joint")
        return None
    
    if (global_scale_check):
        if (global_scale_attr is None):
            pm.displayInfo("Please input global scale attribute")
            return None
        else:
            obj = global_scale_attr.split(".")[0]
            global_attr = global_scale_attr.split(".")[1]
            check_global_attr = pm.attributeQuery(global_attr, node = obj, exists = True)
            if not check_global_attr:
                pm.displayInfo("Invalid global scale attribute")
                return None
        
    

    start_jnt = joint_chain[0]
    end_joint = joint_chain[-1]
    
    
    
    
    if create_dense_chain:
        rep_chain = pm.duplicate(joint_chain)
        start_jnt = rep_chain[0]
        end_joint = rep_chain[-1]
        dense_chain(joints = rep_chain, joints_inbetween = dense_division)
        rep_chain.append(end_joint)
        for index in range(len(joint_chain)):
            pm.parentConstraint(rep_chain[index], joint_chain[index], maintainOffset=False)
            pm.connectAttr(str(rep_chain[index])+".scale", str(joint_chain[index])+".scale")
        pm.select(start_jnt, hierarchy=True)
        new_chain = pm.ls(selection=True)
        
    
    crv = ""
    
    
    if auto_curve:
        ik_handle, eff, crv = pm.ikHandle(startJoint = start_jnt, createCurve = auto_curve, solver = "ikSplineSolver", 
                                          numSpans = spans, endEffector = end_joint, simplifyCurve = auto_simplify)

    else:
        crv = pm.PyNode(use_curve)
        ik_handle, eff= pm.ikHandle(startJoint = start_jnt, curve = use_curve, solver = "ikSplineSolver", 
                                          endEffector = end_joint, createCurve = False) 
    
    crv.inheritsTransform.set(0)
    
    pm.rename(ik_handle, ik_name+"IK_Handle")        
    pm.rename(crv, ik_name+"IK_Curve")
    
    ik_curve_shp = crv.getShape()
    crv_info_node = pm.createNode("curveInfo")
    pm.connectAttr(ik_curve_shp+".worldSpace", crv_info_node+".inputCurve")
    
    '''
    if stretch_exp:
        if create_dense_chain:
            stretch_expression(joints = new_chain, curve_info_node = crv_info_node, connect_scale = scale_stretch,
                               expression_name = ik_name+"_stretch_expression")
        else:
            stretch_expression(joints = joint_chain, curve_info_node = crv_info_node, connect_scale = scale_stretch,
                               expression_name = ik_name+"_stretch_expression")
    '''
    
    if ctrl_jnts:
        if ctrl_jnts == 1:
            print "Minimum 2 joints needed as controllers"
            print "skipping control joint creation process"
            pm.displayInfo("Minimum 2 joints needed as controllers")
        else:
            ctrl_jnts = joints_along_curve(number_of_joints = ctrl_jnts, curve = crv, bind_curve_to_joint = True)
            pm.select(clear = True)
            ctr_jnt_gp = pm.group(ctrl_jnts, name = "control_joints")
    
    if stretch_exp:
        pm.addAttr(ctrl_jnts[-1], longName = "Stretch", attributeType = "enum", enumName = "off:on", keyable = True)
        print "ATTRIBUTE TO", str(ctrl_jnts[-1])
        if create_dense_chain:
            stretch_expression(joints = new_chain, curve_info_node = crv_info_node, connect_scale = scale_stretch,
                               expression_name = ik_name+"_stretch_expression", 
                               ctrl_attr = str(ctrl_jnts[-1])+".Stretch", glbl_scl_stat = global_scale_check,
                               glbl_scl_attr = global_scale_attr)
        else:
            stretch_expression(joints = joint_chain, curve_info_node = crv_info_node, connect_scale = scale_stretch,
                               expression_name = ik_name+"_stretch_expression", 
                               ctrl_attr = str(ctrl_jnts[-1])+".Stretch", glbl_scl_stat = global_scale_check,
                               glbl_scl_attr = global_scale_attr)    
    
    final_group = pm.group(name = ik_name+"_ik_group", empty=True)
    pm.parent(joint_chain[0], final_group)
    pm.parent(crv, final_group)
    pm.parent(ik_handle, final_group)
    if ctrl_jnts>1:
        pm.parent(ctr_jnt_gp, final_group)
    if create_dense_chain:
        pm.select(clear=True)
        dense_grp = pm.group(start_jnt, name = "dense_chain_group")
        pm.parent(dense_grp, final_group)
    
       
    return None
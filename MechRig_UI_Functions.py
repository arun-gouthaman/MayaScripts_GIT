import sys
import pymel.all as pm


leg_joints = ["_Leg_Body_Joint", "_Leg_Joint", "_Knee_Joint", "_Ankle_Joint"]
arm_joints = ["_Shoulder_Joint", "_Elbow_Joint", "_ForeArm_Joint"]

arm_fk_controls = ["_Shoulder_FK_control", "_Elbow_FK_control", "_ForeArm_FK_control"]
leg_fk_controls = ["_Leg_FK_control", "_Knee_FK_control", "_Ankle_FK_control"]

arm_ik_controls = ["_Arm_IK_control", "_Arm_Pole_Locator"]
leg_ik_controls = ["_Leg_IK_control", "_Leg_Pole_Locator"]


def test_fun():
    print "TEST FUN"
    return None

def set_key(**kwargs):
    side = kwargs.get("side", "").lower()
    part = kwargs.get("part", "").lower()
    mode = kwargs.get("mode", "").upper()
    if mode == "SELECTION":
        print "SELECTION MODE"
        selection_list = pm.ls(selection=True)
        for object in selection_list:
            pm.setKeyframe(object)
        return None
    if side == "left":
        side = "L"
    elif side == "right":
        side = "R"
    else:
        print "Invalid side option"
        return None
    if part == "arm":
        if mode == "FK":
            for controller in arm_fk_controls:
                pm.setKeyframe(side+controller)
        elif mode == "IK":
            for controller in arm_ik_controls:
                pm.setKeyframe(side+controller)
        else:
            print "Invalid controller mode"
            return None
    elif part == "leg":
        if mode == "FK":
            for controller in leg_fk_controls:
                pm.setKeyframe(side+controller)
        elif mode == "IK":
            for controller in leg_ik_controls:
                pm.setKeyframe(side+controller)
        else:
            print "Invalid controller mode"
            return None
    else:
        print "Invalid controller option"
    return None
                


def read_initial_values():
    slider_attr = ["all_blend_ikfk", "l_arm_ikfk", "r_arm_ikfk", "l_leg_ikfk", "r_leg_ikfk"]
    value_list = []
    for index in range(len(slider_attr)):
        attr_value = pm.getAttr("Global_control."+slider_attr[index])
        value_list.append(attr_value)
        #print "global_controller : ", attr_value
    return value_list

   
def slider_value_change(slider_object, slider_text_object, attribute):
    slider_val = str(slider_object.value())
    slider_text_object.clear()
    slider_text_object.setText(str(float(slider_val)/100))
    pm.setAttr("Global_control."+attribute, float(slider_val)/100)
    return None
    
def switch_button(slider_object, mode):
    if mode == "IK":
        if slider_object.value() == 100:
            slider_object.setValue(99)
        slider_object.setValue(100)
    else:
        if not slider_object.value():
            slider_object.setValue(1)
        slider_object.setValue(0)
    return None
        
def full_blend_slider_change(full_blend_slider_object, child_slider_object):
    full_blend_slider_value = full_blend_slider_object.value()
    child_slider_object.setValue(full_blend_slider_value)
    return None

def slider_text_change(text_object, slider_object):
    slider_text_value = float(text_object.text())
    slider_object.setValue(slider_text_value*100)
    return None

def append_controller_list(list_box_object):
    controller_list = pm.ls("*control", absoluteName=False)
    fk_list = []
    ik_list = []
    other_list = []
    for controller in controller_list:
        if str(controller).find("|") != -1:
            controller = str(controller).split("|")[1]
        
        if str(controller).find("FK") != -1:
            fk_list.append(str(controller))
        elif str(controller).find("IK") != -1:
            ik_list.append(str(controller))
        else:
            other_list.append(str(controller))
    list_box_object.addItems(fk_list)
    list_box_object.addItems(ik_list)
    list_box_object.addItems(other_list)
    pole_locator_list = ["L_Arm_Pole_Locator", "R_Arm_Pole_Locator", "L_Leg_Pole_Locator", "R_Leg_Pole_Locator"]
    list_box_object.addItems(pole_locator_list)
    return None

def select_controller(list_box_object):
    pm.select(clear=True)
    pm.select(list_box_object.currentItem().text())
    return None


def set_controller(**kwargs):
    #controller = kwargs.get("controller", "FK").lower()
    joints_list = kwargs.get("joints_list", "none").lower()
    slider_object = kwargs.get("slider_object", None)
    slider_value = float(slider_object.value())/100
    #ik_weight = slider_value
    #fk_weight = 1-slider_value
    
    #print "controller option :"+controller+"----"+joints_list
    #if not ((controller == "ik") or (controller == "fk")):
    #    print "Invalid controller option"
    #    print "Please choose FK or IK controller"
    #    return None
    
    if joints_list not in ["left_arm", "right_arm", "left_leg", "right_leg", "arms", "legs", "all"]:
        print "Invalid Joints parameter value, please enter one of the below options"
        print "left_arm\nright_arm\nleft_leg\nright_leg\narms\nlegs\nall"
        return None
    
    if joints_list == "arms":
        set_weight("L", arm_joints, slider_value)
        set_weight("R", arm_joints, slider_value)
        return None
    
    if joints_list == "legs":
        set_weight("L", leg_joints, slider_value)
        set_weight("R", leg_joints, slider_value)
        return None
    
    if joints_list == "all":
        set_weight("L", arm_joints, slider_value)
        set_weight("R", arm_joints, slider_value)
        set_weight("L", leg_joints, slider_value)
        set_weight("R", leg_joints, slider_value)
        return None
    
    
    side = joints_list.split("_")[0]
    part = joints_list.split("_")[1]
    print side, part
    side_parameter = "R"
    if side == "left":
        side_parameter = "L"

    
    if part == "arm":
        set_weight(side_parameter, arm_joints, slider_value)
    else:
        set_weight(side_parameter, leg_joints, slider_value)
    return None
        
    
"""def set_weight(controller, side, joint_list, slider_value):    
    for current_joint in joint_list:
        current_joint = side+current_joint
        constraint_name = pm.parentConstraint(current_joint, query=True)
        alias_names = pm.parentConstraint(constraint_name, query=True, weightAliasList = True)
        if str(alias_names[0]).find("_FK") != -1:
            fk_weight = alias_names[0]
            ik_weight = alias_names[1]
        else:
            fk_weight = alias_names[1]
            ik_weight = alias_names[0]
        
        ik_weight.set(slider_value)
        fk_weight.set(1-slider_value)    
        if controller == "ik":
            fk_weight.set(0)
            ik_weight.set(1)
            print current_joint+" set to ik"
        if controller == "fk":
            fk_weight.set(1)
            ik_weight.set(0)
            print current_joint+" set to fk
    return None"""




def set_weight(side, joint_list, slider_value): 
    print "set weight : "+side, joint_list   
    for current_joint in joint_list:
        current_joint = side+current_joint
        constraint_name = pm.parentConstraint(current_joint, query=True)
        alias_names = pm.parentConstraint(constraint_name, query=True, weightAliasList = True)
        if str(alias_names[0]).find("_FK") != -1:
            fk_weight = alias_names[0]
            ik_weight = alias_names[1]
        else:
            fk_weight = alias_names[1]
            ik_weight = alias_names[0]
        
        print slider_value
        print fk_weight
        print ik_weight
        
        ik_weight.set(slider_value)
        fk_weight.set(1-slider_value)    
    return None




def snap_controllers(**kwargs):
    joints_list = kwargs.get("joint_list", "none").lower()
    snap_control = kwargs.get("snap_control", "none").lower()
    if not((snap_control == "ik_to_fk") or (snap_control == "fk_to_ik")):
        print "Please enter valid controller options"
        print "ik_to_fk or fk_to_ik"
        return None 
    if joints_list not in ["left_arm", "right_arm", "left_leg", "right_leg", "arms", "legs", "all"]:
        print "Invalid Joints parameter value, please enter one of the below options"
        print "left_arm\nright_arm\nleft_leg\nright_leg\narms\nlegs\nall"
        return None
    
  
    side = joints_list.split("_")[0]
    part = joints_list.split("_")[1]
    
    if snap_control == "ik_to_fk":
        
        leg_pole_locators = ["_Leg_Pole_Locator", "_Leg_FK_Pole_Locator"]
        arm_pole_locators = ["_Arm_Pole_Locator", "_Arm_FK_Pole_Locator"]
        
        if joints_list in ["left_leg", "right_leg", "legs"]:
            ik_position_to = "_Ankle_Joint_FK"
        else:
            ik_position_to = "_ForeArm_Joint_FK"
           
        if joints_list == "legs":
            snap_ik_to_fk("L", leg_joints, ik_position_to, leg_pole_locators, "_Leg_IK_control")
            snap_ik_to_fk("R", leg_joints, ik_position_to, leg_pole_locators, "_Leg_IK_control")
            return None
        
        if joints_list == "arms":
            snap_ik_to_fk("L", arm_joints, ik_position_to, arm_pole_locators, "_Arm_IK_control")
            snap_ik_to_fk("R", arm_joints, ik_position_to, arm_pole_locators, "_Arm_IK_control")
            return None
        
        if joints_list == "all":
            snap_ik_to_fk("L", leg_joints, ik_position_to, leg_pole_locators, "_Leg_IK_control")
            snap_ik_to_fk("R", leg_joints, ik_position_to, leg_pole_locators, "_Leg_IK_control")
            snap_ik_to_fk("L", arm_joints, ik_position_to, arm_pole_locators, "_Arm_IK_control")
            snap_ik_to_fk("R", arm_joints, ik_position_to, arm_pole_locators, "_Arm_IK_control")
            return None

        if side == "left":
            if part == "leg":
                snap_ik_to_fk("L", leg_joints, ik_position_to, leg_pole_locators, "_Leg_IK_control")
                return None
            else:
                snap_ik_to_fk("L", arm_joints, ik_position_to, arm_pole_locators, "_Arm_IK_control")
                return None
    
        else:
            if part == "leg":
                snap_ik_to_fk("R", leg_joints, ik_position_to, leg_pole_locators, "_Leg_IK_control")
                return None
            else:
                snap_ik_to_fk("R", arm_joints, ik_position_to, arm_pole_locators, "_Arm_IK_control")
                return None
    else:
        #FK TO IK FUNCTION CALL LOGIC
          
        if joints_list == "legs":
            snap_fk_to_ik("L", leg_joints)
            snap_fk_to_ik("R", leg_joints)
            return None
        
        if joints_list == "arms":
            snap_fk_to_ik("L", arm_joints)
            snap_fk_to_ik("R", arm_joints)
            return None
        
        if joints_list == "all":
            snap_fk_to_ik("L", leg_joints)
            snap_fk_to_ik("R", leg_joints)
            snap_fk_to_ik("L", arm_joints)
            snap_fk_to_ik("R", arm_joints)
            return None

        if side == "left":
            if part == "leg":
                snap_fk_to_ik("L", leg_joints)
                return None
            else:
                snap_fk_to_ik("L", arm_joints)
                return None
    
        else:
            if part == "leg":
                snap_fk_to_ik("R", leg_joints)
                return None
            else:
                snap_fk_to_ik("R", arm_joints)
                return None
        return None
    return None
    
        
def snap_ik_to_fk(side, joint_input, ik_to, pole_locators, controller):
    ik_controller = side+controller
    fk_joint = side+ik_to
    fk_pole_locator = side+pole_locators[1]
    ik_pole_locator = side+pole_locators[0]
    fk_joint_position = pm.xform(fk_joint, query=True, worldSpace=True, translation=True)
    fk_pole_locator_position = pm.xform(fk_pole_locator, query=True, worldSpace=True, translation=True)
    
    pm.xform(ik_controller, worldSpace = True, translation = fk_joint_position)
    pm.xform(ik_pole_locator, worldSpace=True, translation=fk_pole_locator_position)
    
    if joint_input.find("leg_")>-1:
        joint_rotation = pm.xform("L_Ankle_IK_rotate_control", query=True, worldSpace=True, rotation=True)
        leg_joints[3]
        "L_Ankle_IK_rotate_control"
    
    print ik_controller+" Moved to fk position"
    return None

def snap_fk_to_ik(side, joint_input):
    for _joint in joint_input:
        _joint = side+_joint
        ik_joint = _joint+"_IK"
        fk_controller = _joint.replace("_Joint", "_FK_control")
        joint_rotation = pm.xform(ik_joint, query=True, worldSpace=True, rotation=True)
        pm.xform(fk_controller, worldSpace=True, rotation=joint_rotation)
        print _joint+"controller_set"
    return None

def reveal_controllers(**kwargs):
    combo_object = kwargs.get("combo_object", None)
    part = kwargs.get("part", None)
    mode = kwargs.get("mode", None)
    user_selection = combo_object.currentText()
    user_selection_index = combo_object.currentIndex()
    print user_selection_index, user_selection
    pm.setAttr("Global_control.controller_visibility_status", user_selection_index)
    fk_control = ["L_Shoulder_FK_control_group", "R_Shoulder_FK_control_group", "L_Leg_FK_control_group", "R_Leg_FK_control_group"]
    ik_control = ["L_Arm_IK_control_group", "R_Arm_IK_control_group", "L_Leg_IK_control_group", "R_Leg_IK_control_group"]

    if not(user_selection_index) and part and mode:
        print part, mode
        pm.setAttr("Global_control_group.visibility", 1)
        pm.setAttr("L_Ankle_Heel_Joint_control_Grp.visibility", 1)
        side = part.split("_")[0]
        print side
        if side == "left":
            if part == "left_arm":
                if mode == "fk":
                    pm.setAttr(fk_control[0]+".visibility", 1)
                    pm.setAttr(ik_control[0]+".visibility", 0)
                else:
                    pm.setAttr(fk_control[0]+".visibility", 0)
                    pm.setAttr(ik_control[0]+".visibility", 1)
            else:
                if mode == "fk":
                    pm.setAttr(fk_control[2]+".visibility", 1)
                    pm.setAttr(ik_control[2]+".visibility", 0)
                else:
                    pm.setAttr(fk_control[2]+".visibility", 0)
                    pm.setAttr(ik_control[2]+".visibility", 1)
        else:
            if part == "right_arm":
                if mode == "fk":
                    pm.setAttr(fk_control[1]+".visibility", 1)
                    pm.setAttr(ik_control[1]+".visibility", 0)
                else:
                    pm.setAttr(fk_control[1]+".visibility", 0)
                    pm.setAttr(ik_control[1]+".visibility", 1)
            else:
                if mode == "fk":
                    pm.setAttr(fk_control[3]+".visibility", 1)
                    pm.setAttr(ik_control[3]+".visibility", 0)
                else:
                    pm.setAttr(fk_control[3]+".visibility", 0)
                    pm.setAttr(ik_control[3]+".visibility", 1)
    elif user_selection_index == 1:
        pm.setAttr("Global_control_group.visibility", 1)
        pm.setAttr("L_Ankle_Heel_Joint_control_Grp.visibility", 1)
        for index in range(len(fk_control)):
            pm.setAttr(fk_control[index]+".visibility", 1)
    elif user_selection_index == 2:
        pm.setAttr("Global_control_group.visibility", 1)
        pm.setAttr("L_Ankle_Heel_Joint_control_Grp.visibility", 1)
        for index in range(len(ik_control)):
            pm.setAttr(ik_control[index]+".visibility", 1)
    elif user_selection_index == 3:
        pm.setAttr("Global_control_group.visibility", 1)
        pm.setAttr("L_Ankle_Heel_Joint_control_Grp.visibility", 1)
        for index in range(len(fk_control)):
            pm.setAttr(fk_control[index]+".visibility", 1)
            pm.setAttr(ik_control[index]+".visibility", 0)
    elif user_selection_index == 4:
        pm.setAttr("Global_control_group.visibility", 1)
        pm.setAttr("L_Ankle_Heel_Joint_control_Grp.visibility", 1)
        for index in range(len(fk_control)):
            pm.setAttr(fk_control[index]+".visibility", 0)
            pm.setAttr(ik_control[index]+".visibility", 1)
    elif user_selection_index == 5:
        pm.setAttr("Global_control_group.visibility", 1)
        pm.setAttr("L_Ankle_Heel_Joint_control_Grp.visibility", 1)
        for index in range(len(fk_control)):
            pm.setAttr(fk_control[index]+".visibility", 1)
            pm.setAttr(ik_control[index]+".visibility", 1)
            pm.setAttr("Global_control_group.visibility", 1)
            pm.setAttr("Global_control_group.visibility", 1)
            pm.setAttr("L_Ankle_Heel_Joint_control_Grp.visibility", 1)
            pm.setAttr("R_Ankle_Heel_Joint_control_Grp.visibility", 1)
    else:
        for index in range(len(fk_control)):
            pm.setAttr(fk_control[index]+".visibility", 0)
            pm.setAttr(ik_control[index]+".visibility", 0)
            pm.setAttr("Global_control_group.visibility", 0)
            pm.setAttr("Global_control_group.visibility", 0)
            pm.setAttr("L_Ankle_Heel_Joint_control_Grp.visibility", 0)
            pm.setAttr("R_Ankle_Heel_Joint_control_Grp.visibility", 0)
    
    
    return None
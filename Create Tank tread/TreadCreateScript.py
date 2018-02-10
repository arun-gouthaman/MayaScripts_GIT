import pymel.all as pm
from CustomScripts import midPosVec

"""
Creates expression to loop motion path U value from 0 to 1
holds the initial offset value of each motion path u value
"""
def createTreadExpression(**kwargs):
    motionpaths = kwargs.get("mtnPth", [])
    run_ip = kwargs.get("runAttr", "")
    speed_ip = kwargs.get("speedAttr", "")
    expression_name = kwargs.get("exp_nm", "")
    #ip_str = "float $ipVal = nurbsCircle1.motion_path*0.05;\n"
    ip_str = "float $ipVal = "+run_ip+"*"+speed_ip+";\n"
    print ip_str
    computeOffset = ""
    id = 1
    for mp in motionpaths:
        offset = pm.getAttr(str(mp)+".uValue")
        computeOffset += "float $newVal"+ str(id) +" = "+ str(offset)+"+($ipVal - floor("+str(offset)+"+$ipVal));\n"
        computeOffset += str(mp)+".uValue = $newVal"+str(id)+";\n"
    
    expression_string = ip_str+computeOffset
    pm.expression(name = expression_name, string = expression_string)
        

"""
Select the path curve and run the below script
takes number if joints as input and places joints on the curve with equal distance between them
creates motion path for each joint on the curve and maintain the position they were placed at using the u value
"""
def createTread(**kwargs):
    # get inputs
    divisions = kwargs.get("no_of_joints", 0)
    tread_name = kwargs.get("tr_name", "Tread")
    path_crv = kwargs.get("path_crv", None)
    # duplicate the existing curve to use for tread creation
    path_crv = str(pm.duplicate(path_crv, name = str(tread_name)+"PathCrv")[0])
    pm.xform(path_crv, centerPivots=True)
    count = 0
    part = float(1)/float(divisions)
    init = 0
    path_anim_list = []
    jnt_lst = []
    # create joints and place them on curve using motion path at equal distance
    while count<divisions:
        pm.select(clear=True)
        jnt = pm.joint()
        jnt_lst.append(jnt)
        pathanim = pm.pathAnimation(jnt, curve = path_crv, fractionMode = True, follow = True, followAxis = "x",
                     worldUpType = "vector", worldUpVector = (0,1,0))
        path_anim_list.append(pathanim)
        pm.setAttr(str(pathanim)+".uValue", init)
        pm.disconnectAttr(str(pathanim)+".u")
        init += part
        count += 1
        # obtain the midpoint of all joints to create an up locator and position it at midpoint
    #loc_pos = midPos(selected_items = jnt_lst)
    #loc_pos = pm.xform(path_crv, query=True, translation=True, worldSpace=True)
    loc_pos = midPosVec(objects = jnt_lst)
    loc = pm.spaceLocator(name = tread_name+"_up_loc")
    pm.xform(loc, translation = loc_pos)
    # create a nurb circle to act as parent controller
    control_crv = pm.circle(name = tread_name+"CTRL", normalX = 1, normalY = 0, normalZ = 0)
    pm.xform(control_crv, translation = loc_pos)
    pm.select(clear=True)
    # add unr and speed attributes on parent nurb curve
    pm.addAttr(control_crv, longName = "run", attributeType = "float", keyable = True)
    pm.addAttr(control_crv, longName = "speed", attributeType = "float", keyable = True, minValue = 0.0, defaultValue = 0.5)
    #edit the existing motion path to assign up locator
    for mtPth in path_anim_list:
        pm.pathAnimation(mtPth, edit=True, worldUpType = "object", worldUpObject = loc)
    #parent the setup under the parent nurb curve
    pm.parent(path_crv, control_crv)
    pm.parent(loc, control_crv)
    pm.select(clear=True)
    gp = pm.group(name = tread_name+"GP")
    pm.select(clear=True)
    jnt_gp = pm.group(jnt_lst, name = tread_name+"JNTGP")
    pm.xform(gp, translation = loc_pos)
    pm.parent(control_crv, gp)
    pm.parent(jnt_gp, gp)
    # call to create expression function
    createTreadExpression(mtnPth = path_anim_list, runAttr = str(control_crv[0])+".run", speedAttr = str(control_crv[0])+".speed", exp_nm = tread_name)
    return None

#createTread(no_of_joints = 5, tr_name = "testTread", path_crv = "nurbsCircle1")




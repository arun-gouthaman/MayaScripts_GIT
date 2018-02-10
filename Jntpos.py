import CustomScripts
#reload(CustomScripts)
import pymel.all as pm
def jnt_at_object_mid(**kwargs):
    sel = pm.ls(orderedSelection=True, flatten=True)
    for tran in sel:
        if not isinstance(tran, pm.Transform):
            pm.displayinfo("Please select only transform nodes")
            return None
    if not sel:
        pm.displayInfo("please select transform object")
    pos = []
    for obj in sel:
        pos.append(CustomScripts.midPos(selected_items = obj))
    pm.select(clear=True)
    for p in pos:
        jnt = pm.joint(position=p)
        pm.select(clear=True)
    return None


def jnt_at_mid_vertex_orient(**kwargs):
    sel = pm.ls(orderedSelection=True, flatten=True)
    if not sel:
        pm.displayInfo("Please select vertex")
        return None
    obj_pos_map = {}
    for comp in sel:
        if not isinstance(comp, pm.MeshVertex):
            pm.displayInfo("Please select only vertex")
            return None
    mid_pos = 0
    for comp in sel:
        shape_node = comp.node()
        transform_node = pm.listTransforms(comp.node())[0]
        if transform_node not in obj_pos_map.keys():
            vrts = CustomScripts.get_vrts(sel_obj = [transform_node])[0]
            print vrts
            pos = CustomScripts.midPos(selected_items = vrts)
            obj_pos_map[transform_node] = pos
            mid_pos = pos
        else:
            mid_pos = obj_pos_map[transform_node]
        print obj_pos_map
        comp_pos = pm.pointPosition(comp, world=True)
        pm.select(clear=True)
        jnt1 = pm.joint(position = mid_pos)
        jnt2 = pm.joint(position = comp_pos)
        pm.joint(jnt1, edit=True, orientJoint='xyz', 
                     secondaryAxisOrient='yup', zeroScaleOrient=True)
        pm.select([jnt1, jnt2])
        CustomScripts.CopyJntOri()

    return None

def jnt_along_loop():
    import splitLoops
    #reload(splitLoops)
    loops = splitLoops.split_loop()
    if not loops:
        pm.displayInfo("please select only edge loops")
        return None
    else:
        verts = loops[1]
        loops = loops[0]

    pos = []
    for i in range(len(loops)):
        pos.append(CustomScripts.midPos(selected_items = verts[i]))
    
    print pos
    jnt_lst = []
    for p in pos:
        print p
        jnt = pm.joint(position=p)
        jnt_lst.append(jnt)
        if len(jnt_lst)>1:
            pm.joint(jnt_lst[pos.index(p)-1], edit=True, orientJoint='xyz', 
                         secondaryAxisOrient='yup', zeroScaleOrient=True)
    return None




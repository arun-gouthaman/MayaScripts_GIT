import pymel.all as pm
import maya.OpenMaya as om
import math
def curve_through_points(**kwargs):
    selection_points = pm.ls(selection=True)
    curve_name = kwargs.get("curve_name", "")
    curve_degree = kwargs.get("curve_degree", 1)
    points_locations = kwargs.get("position_list", [])
    pm.select(clear=True)
    current_curve = pm.curve(degree = curve_degree, worldSpace=True, point = points_locations)
    pm.rename(current_curve, curve_name)
    return None
spiral_count = 1
initx = 2
inity = 0
scalex = 0
scaley = 1

end_extend_scale = 0
points_per_spiral = 50

scalex = (float(scalex)/points_per_spiral)/spiral_count
scaley = (float(scaley)/points_per_spiral)/spiral_count

init_vec = om.MVector(initx,inity,0)
init_pos = om.MVector(0,0,0)
total_deg = 360*spiral_count;
div = points_per_spiral*spiral_count
frac = total_deg/div
init = 0
pos = []

while init<total_deg:
    new_vec = init_vec.rotateBy(init_vec.kYaxis, math.pi/180 * init)
    init_vec.x += scalex
    init_vec.y += scaley
    
    pos.append([new_vec.x, new_vec.y, new_vec.z])
    init += frac
    #scalex+=.1

#for p in pos:
#    print p
extend_vec = om.MVector(pos[-1][0], pos[-1][1], pos[-1][2]) - \
                        om.MVector(pos[-2][0], pos[-2][1], pos[-2][2])
print extend_vec.x, extend_vec.y, extend_vec.z

extend_vec.normalize()
extend_vec = extend_vec*end_extend_scale
extend_vec += om.MVector(pos[-1][0], pos[-1][1], pos[-1][2])
#print extend_vec.x, extend_vec.y, extend_vec.z
pos.append([extend_vec.x, extend_vec.y, extend_vec.z])
curve_through_points(curve_name = "Spiral", curve_degree = 3, 
                     position_list = pos)
#pm.spaceLocator(position = (extend_vec.x, extend_vec.y, extend_vec.z))

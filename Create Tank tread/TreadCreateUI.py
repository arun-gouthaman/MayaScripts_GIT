import pymel.all as pm
import TreadCreateScript
import TreadAtPoints

#reload(TreadCreateScript)
#reload(TreadAtPoints)

"""
function to choose between evenly placed joints or joints at selected positions
"""
def callFun(sel, divisions, tread_name, curve_name):
    sel_op = sel.getSelect()
    op_label = pm.radioButton(sel_op, query=True, label = True)
    jt_num = int(divisions.getText())
    nm = tread_name.getText()
    pth = curve_name.getText()
    if op_label == 'uniform':
        TreadCreateScript.createTread(no_of_joints = jt_num,tr_name = nm, path_crv = pth)
    else:
        TreadAtPoints.treadAtPoints(tr_name = nm, path_crv = pth)
    return None

def tankTread_UI():
    
    WINDOW='TreadRig'
    if pm.window(WINDOW, query=True, exists=True):
        pm.deleteUI(WINDOW)
    pm.window(WINDOW, title="TreadRig", iconName='TR', 
              widthHeight=(200, 220) )
    column_1=pm.columnLayout( adjustableColumn=True )
    pm.separator( height=20, style='none', parent=column_1 )
    tread_name=pm.TextField(text='Tread_Name', parent=column_1)
    pm.separator( height=20, style='none', parent=column_1 )
    ##get parent name
    row_col_1 = pm.rowColumnLayout(numberOfColumns = 2, columnWidth = (1, 150), parent = column_1, columnOffset = (2, 'left', 10))
    #prompt_object_text=pm.Text(label="Parent", parent=row_col_1)
    curve_name=pm.TextField(text='PathCurve', parent=row_col_1)
    button_parent_get = pm.button(label='<<', parent = row_col_1, command=lambda x: curve_name.setText(str(pm.ls(selection=True)[0])))
    pm.separator( height=20, style='in', parent=column_1 )
    jnt_type_lbl = pm.text(label = "joint placement type", align = "left", parent = column_1)
    pm.separator( height=5, style='none', parent=column_1)
    jnt_typ_radio = pm.radioCollection(parent = column_1)
    row_layout = pm.rowLayout(numberOfColumns = 2, height = 20, parent = column_1)
    divisions=pm.TextField(text='1', parent=column_1)
    rb1 = pm.radioButton( label='uniform', parent = row_layout, select=True, onCommand = lambda x: pm.textField(divisions, edit=True, editable = True))
    rb1 = pm.radioButton( label='selection', parent = row_layout, onCommand = lambda x: pm.textField(divisions, edit=True, editable = False))
    pm.separator( height=20, style='none', parent=column_1 )
    #button_parent_get = pm.button(label='Create', parent = column_1, command=lambda x: TreadCreateScript.createTread(no_of_joints = int(divisions.getText()), 
	#					tr_name = tread_name.getText(), path_crv = curve_name.getText()))
    button_parent_get = pm.button(label='Create', parent = column_1, command=lambda x: callFun(jnt_typ_radio, divisions, tread_name, curve_name))
    pm.showWindow(WINDOW)
    pm.window(WINDOW, edit=True, widthHeight=(200, 220))
    return None
#tankTread_UI()
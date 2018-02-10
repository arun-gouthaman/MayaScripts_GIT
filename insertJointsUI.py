import pymel.all as pm


def call_fun(number_of_joints):
    from IK_Spline_Setup import dense_chain
    jnts = pm.ls(selection=True)
    dense_chain(joints = jnts, joints_inbetween = int(number_of_joints))
    return None

def insert_joints_UI():
    WINDOW='InsertJoints'
    if pm.window(WINDOW, query=True, exists=True):
        pm.deleteUI(WINDOW)
    pm.window(WINDOW, title="Insert Joints", iconName='CS', 
              widthHeight=(200, 70) )
    main_col = pm.columnLayout( adjustableColumn=True )
    pm.separator( height=5, style='none', parent=main_col )
    textip_col = pm.rowColumnLayout(numberOfColumns = 2, parent = main_col, columnOffset = (1,"left", 5), columnSpacing = (2,5))
    pm.separator( height=5, style='none', parent=main_col )
    butn_col = pm.rowColumnLayout(numberOfColumns = 3, parent = main_col, columnOffset = (2, "left", 65))
    labletxt = pm.text(label = "number of joints", parent = textip_col)
    textip = pm.textField(text = "", parent = textip_col)
    but_dummy = pm.text(label = "", parent = butn_col)
    ok_butn = pm.button(label = "Create", parent = butn_col, command = lambda x: call_fun(textip.getText()))
    pm.showWindow(WINDOW)
    pm.window(WINDOW, edit=True, widthHeight=(200, 70))
    return None
import pymel.all as pm
import CustomScripts
#reload(CustomScripts)

def CustomScripts_UI():
    
    WINDOW='CustomScripts'
    if pm.window(WINDOW, query=True, exists=True):
        pm.deleteUI(WINDOW)
    pm.window(WINDOW, title="Custom Scripts", iconName='CS', 
              widthHeight=(200, 400) )
    column_1=pm.columnLayout( adjustableColumn=True )

    pm.separator( height=20, style='in', parent=column_1 )
    mid_jnt_btn=pm.button(label='Joint at mid position', 
                          command = lambda x: CustomScripts.jntAtmid())
    
    pm.separator( height=20, style='in', parent=column_1 )
    ins_jnt_btn=pm.button(label='insert joint', 
                          command = lambda x: CustomScripts.insJnt())
    
    pm.separator( height=20, style='in', parent=column_1 )
    im_pr_btn=pm.button(label='Immediate Parent in Hierarchy', 
                        command = lambda x: CustomScripts.immediateParent())
    
    pm.separator( height=20, style='in', parent=column_1 )
    hd_jnt_btn=pm.button(label='Hide Joint', command = lambda x: CustomScripts.jntHide())
    
    pm.separator( height=20, style='in', parent=column_1 )
    hd_lod_btn=pm.button(label='LOD off', command = lambda x: CustomScripts.lodOff())   

    pm.separator( height=20, style='in', parent=column_1 )
    hd_lod_btn=pm.button(label='Parent( in selection order)', 
                         command = lambda x: CustomScripts.parentChain()) 

    ##get object name
    pm.separator( height=20, style='in', parent=column_1 )
    row_col_2 = pm.rowColumnLayout(numberOfColumns = 2, columnWidth = (1, 150), 
                                   parent = column_1, columnOffset = (2, 'left', 10))
    object_name=pm.TextField(parent=row_col_2)
    button_object_get = pm.button(label='<<', parent = row_col_2, 
                                  command=lambda x: object_name.setText(str(pm.ls(selection=True)[0])))
    row_col_3 = pm.rowColumnLayout(numberOfColumns = 2, columnWidth = (1, 100), 
                                   parent = column_1, columnOffset = (2, 'left', 10))
    prntChk = pm.checkBox("parent", parent = row_col_3)
    sclChk = pm.checkBox("scale", parent = row_col_3)
    pm.separator( height=5, style='none', parent=column_1 ) 
    cpy_obj_btn=pm.button(label='Copy Object to selected positions', 
                          parent = column_1, 
                          command = lambda x: \
                          CustomScripts.copyObjects(obj = object_name.getText(),\
                              prFlg = prntChk.getValue(), scFlg = sclChk.getValue()))    
    
	
    pm.separator( height=20, style='in', parent=column_1 )
    ori_btn = pm.button(label = "copy orientation", parent = column_1, 
                        command = lambda x: CustomScripts.CopyJntOri())

    pm.showWindow(WINDOW)
    pm.window(WINDOW, edit=True, widthHeight=(200, 400))
    return None

#CustomScripts_UI()
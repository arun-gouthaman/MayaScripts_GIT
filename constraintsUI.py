import pymel.all as pm
import CustomScripts as CS


def mul_con_call(parentObj, prntt, scl):
    prObj = parentObj.getText()
    prntChk =  prntt.getValue()
    sclChk = scl.getValue()
    CS.constMult(prntObj = prObj, pr_cons = prntChk, sc_cons = sclChk)
    return None

def set_con_call(prnt, scl):
    prntChk =  prnt.getValue()
    sclChk = scl.getValue()
    #print prntChk
    #print sclChk
    CS.setCon(pr_cons = prntChk, sc_cons = sclChk)
    return None

def del_cons(prnt, scl, pnt, ornt):
    prntChk =  prnt.getValue()
    sclChk = scl.getValue()
    pntChk = pnt.getValue()
    orChk = ornt.getValue()
    CS.delCon(pr_con = prntChk, sc_con = sclChk, 
              pt_con= pntChk, or_con = orChk)
    return None



def constraints_ui():
    WINDOW='Constraints'
    if pm.window(WINDOW, query=True, exists=True):
        pm.deleteUI(WINDOW)
    pm.window(WINDOW, title="Constraints", iconName='CON', 
              widthHeight=(200, 275) )
    column_1=pm.columnLayout( adjustableColumn=True )
    pm.separator( height=2, style='in', parent=column_1 )
    mulChLbl=pm.Text(label="Multiple Children", parent=column_1)
    pm.separator( height=5, style='none', parent = column_1)
    rowCol1 = pm.rowColumnLayout(numberOfRows = 3, parent = column_1)
    txt_row_col_1 = pm.rowColumnLayout(numberOfColumns = 2, columnWidth = (1,150),
                                   parent = rowCol1, columnSpacing = (1,15))
    mulCtrlNm = pm.TextField(parent = txt_row_col_1)
    mulCtrlBtn = pm.button(label='<<', parent = txt_row_col_1,
           command = lambda x: mulCtrlNm.setText(str(pm.ls(selection=True)[0])))
    row_col_1 = pm.rowColumnLayout(numberOfColumns = 2, columnWidth = (1,100), 
                                   parent = rowCol1, columnAlign = (2,'center'),
                                   columnSpacing = (1,25))
    prChk = pm.checkBox("Parent", parent = row_col_1)
    scChk = pm.checkBox("Scale", parent = row_col_1)
    conBtn = pm.button(label = "Constraint", parent=column_1,
                       command = lambda x:mul_con_call(mulCtrlNm, prChk, scChk))
    
    
    
    
    pm.separator( height=20, style='in', parent=column_1 )
    setLbl=pm.Text(label="Selection Set", parent=column_1)
    pm.separator( height=5, style='none', parent = column_1)
    rowCol2 = pm.rowColumnLayout(numberOfRows = 2, parent = column_1)
    
    row_col_2 = pm.rowColumnLayout(numberOfColumns = 2, columnWidth = (1,100), 
                                   parent = rowCol2, columnAlign = (2,'center'), 
                                   columnSpacing = (1,25))
    prSetChk = pm.checkBox("Parent", parent = row_col_2)
    scSetChk = pm.checkBox("Scale", parent = row_col_2)
    conSetBtn = pm.button(label = "Constraint", parent=column_1,
                          command = lambda x:set_con_call(prSetChk, scSetChk))
    
    
    
    
    
    
    pm.separator( height=20, style='in', parent=column_1 )
    delConLbl = pm.Text(label = "Delete Constraints", parent = column_1)
    pm.separator( height=5, style='none', parent = column_1)
    rowCol3 = pm.rowColumnLayout(numberOfRows = 3, parent = column_1)
    row_col_3_1 = pm.rowColumnLayout(numberOfColumns = 2, columnWidth = (1,100), 
                               parent = rowCol3, columnAlign = (2,'center'), 
                               columnSpacing = (1,25))
    row_col_3_2 = pm.rowColumnLayout(numberOfColumns = 2, columnWidth = (1,100), 
                               parent = rowCol3, columnAlign = (2,'center'), 
                               columnSpacing = (1,25))
    prDelChk = pm.checkBox("Parent", parent = row_col_3_1)
    scDelChk = pm.checkBox("Scale", parent = row_col_3_1)
    ptDelChk = pm.checkBox("Point", parent = row_col_3_2)
    orDelChk = pm.checkBox("Orient", parent = row_col_3_2) 
    conDelBtn = pm.button(label = "Delete", parent=column_1,
                          command = lambda x:del_cons(prDelChk, scDelChk,
                                                      ptDelChk, orDelChk))
    
    
    
    
    
    
    pm.showWindow(WINDOW)
    pm.window(WINDOW, edit=True, widthHeight=(200, 275))
    return None
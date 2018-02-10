import pymel.all as pm



def call_fun(name, base_joint, dense_chain_val, dense_divisions,
             curve_opn, curve_name, simplify_curve,
             spans_num, stretch, scale_connect,
             num_ctrl_jnt, glbl_scl_chk, glbl_scl_attr):
    
    
   
    if name == "" or base_joint == "":
        pm.displayInfo("ik name and/or joint name input missing")
        return None
    
    default = 1
    if spans_num < 1:
        spans_num = default
        print "Spans set to 1"
        pm.displayInfo("Spans set to 1")
    if dense_divisions < 1:
        dense_divisions = default
        print "divisions set to 1"
        pm.displayInfo("divisions set to 1")
    
    if num_ctrl_jnt<0:
        num_ctrl_jnt = 0
    
    curve_flag = True
    if curve_opn == "UseCurve":
        curve_flag = False
        
    if not curve_flag:
        if curve_name == "":
            pm.displayInfo("please enter the curve name to be used")
            return None
 
    
    import IK_Spline
    #reload(IK_Spline)
    
    IK_Spline.setup_ik_spline(ik_name = name, joint_chain = base_joint,
                                    dense_chain = dense_chain_val, dense_chain_divisions = dense_divisions,
                                    auto_curve = curve_flag, use_curve = curve_name,
                                    auto_simplify_curve = simplify_curve, number_of_spans = spans_num,
                                    stretch_exp = stretch, scale_stretch = scale_connect,
                                    num_control_joints = num_ctrl_jnt, global_scale_check = glbl_scl_chk,
                                    global_scale_attr = glbl_scl_attr)
    
    return None


'''def call_fun(*args):
    for item in args:
        print item
    return None'''

def spline_ik_setup_UI():
    WINDOW='SplineIK'
    if pm.window(WINDOW, query=True, exists=True):
        pm.deleteUI(WINDOW)
    pm.window(WINDOW, title="Spline IK", iconName='SplineIK', 
              widthHeight=(250, 310) )
    
    main_column = pm.columnLayout(adjustableColumn = True)
    pm.separator( height=5, style='in', parent=main_column )
    name_col = pm.rowColumnLayout(numberOfColumns = 2, parent=main_column, columnOffset = (1,"left",30),
                                  columnSpacing = (2,5), columnWidth = (2,130))
    pm.separator( height=5, style='in', parent=main_column )
    joint_col = pm.rowColumnLayout(numberOfColumns = 3, parent = main_column, columnOffset = (1, "left", 30),
                                   columnSpacing = (2,5))
    pm.separator( height=5, style='in', parent=main_column )
    dense_col = pm.rowColumnLayout(numberOfColumns = 4, columnOffset = (1,"left",5),
                                   parent = main_column, columnSpacing = (3,10))
    pm.separator( height=5, style='in', parent=main_column )
    curve_option_col = pm.rowColumnLayout(numberOfColumns = 2, columnOffset = (1,"left", 5),
                                        parent = main_column, columnSpacing = (2,70))
    pm.separator( height=5, style='none', parent=main_column )
    curve_name_col = pm.rowColumnLayout(numberOfColumns = 3, columnOffset = (1,"left", 40),
                                        parent = main_column, columnSpacing = (2,5))
    pm.separator( height=5, style='none', parent=main_column )
    curve_simplify_col = pm.rowColumnLayout(numberOfColumns = 4, columnOffset = (1, "left", 5),
                                            parent = main_column, columnSpacing = (3,5))
    pm.separator( height=5, style='in', parent=main_column )
    stretch_col = pm.rowColumnLayout(numberOfColumns = 2, columnWidth = (1,100),
                                     parent = main_column, columnOffset = (1,"left", 5))
    pm.separator( height=5, style='in', parent=main_column )

    global_scale_col = pm.rowColumnLayout(numberOfColumns = 3, columnWidth = (1,100),
                                          parent = main_column, columnOffset = (1,"left", 5),
                                          columnSpacing = (3,10))

    pm.separator( height=20, style='in', parent=main_column)    
    
    ctrl_jnt_col = pm.rowColumnLayout(numberOfColumns = 3, columnOffset = (1, "left", 5),
                                      parent = main_column, columnWidth = (3,50),
                                      columnSpacing = (3,5))
    pm.separator( height=20, style='in', parent=main_column)
    
    
    create_btn_col = pm.rowColumnLayout(numberOfColumns = 3, parent = main_column, columnOffset = (2,"left", 65),
                                        columnWidth = (2,300))
    
    
    name_label = pm.text(label = "Ik name", parent = name_col)
    name_text = pm.TextField(text = "", parent = name_col)
    joint_label = pm.text(label = "base joint", parent = joint_col)
    joint_name = pm.textField(text = "", parent = joint_col)
    joint_btn = pm.button(label = "<<", parent = joint_col, 
                          command = lambda x:joint_name.setText(str(pm.ls(selection=True)[0])))
    
    
    
    
    dense_div_label = pm.text()
    dense_div_text = pm.textField()
    dense_chain_chb = pm.checkBox("dense chain", parent = dense_col,
                                  changeCommand = lambda x: (dense_div_label.setEnable(dense_chain_chb.getValue()),
                                                             dense_div_text.setEditable(dense_chain_chb.getValue()))                          )
    pm.separator(style = 'single', horizontal = False, parent = dense_col, width = 20)
                 
    pm.text(dense_div_label, edit=True, label = "divisions", parent = dense_col, enable = dense_chain_chb.getValue())
    pm.textField(dense_div_text, edit=True, text = "3", parent = dense_col, editable = dense_chain_chb.getValue(), width = 50)

    
    curve_label = pm.text(label = "Curve", parent = curve_name_col)
    curve_text = pm.textField(text = "", parent = curve_name_col, editable = False)
    curve_btn = pm.button(label = "<<", parent = curve_name_col, enable = False,
                          command = lambda x: curve_text.setText(str(pm.ls(selection=True)[0])))        
    
    
    
    spans_label = pm.text()
    spans_text = pm.TextField()
    curve_simple_chb = pm.checkBox(label = "simplify curve", parent = curve_simplify_col, enable = True,
                                   changeCommand = lambda x: (spans_label.setEnable(curve_simple_chb.getValue()),
                                                          spans_text .setEditable(curve_simple_chb.getValue())))
    pm.separator(style = 'single', horizontal = False, parent = curve_simplify_col, width = 5)
    pm.text(spans_label, edit=True, label = "spans    ", parent = curve_simplify_col, enable = curve_simple_chb.getValue())
    pm.textField(spans_text, edit = True, text = "3", parent = curve_simplify_col, editable = curve_simple_chb.getValue())
    
    
    
    curve_create = pm.radioCollection(parent = curve_option_col)
    auto_crv_rdb = pm.radioButton("AutoCurve", label = "Auto Curve", select=True, parent = curve_option_col,
                                  onCommand = lambda x:(curve_btn.setEnable(False),
                                                        curve_label.setEnable(False),
                                                        curve_text.setEditable(False),
                                                        curve_simple_chb.setEnable(True),
                                                        spans_label.setEnable(curve_simple_chb.getValue()),
                                                        spans_text.setEditable(curve_simple_chb.getValue())))
    use_crv_rdb = pm.radioButton("UseCurve", label = "use Curve", select=False, parent = curve_option_col,
                                 onCommand = lambda x:(curve_btn.setEnable(True),
                                                       curve_label.setEnable(True),
                                                       curve_text.setEditable(True),
                                                       curve_simple_chb.setEnable(False),
                                                       spans_label.setEnable(False),
                                                       spans_text.setEditable(False)))                            




    stretch_scale_chb = pm.checkBox()
    global_scale_chb = pm.checkBox()
    scale_attr_text = pm.TextField()
    scale_label = pm.text()
    
    stretch_chb = pm.checkBox(label = "stretch", parent = stretch_col,
                              changeCommand = lambda x: (stretch_scale_chb.setEditable(stretch_chb.getValue()),
                                                        global_scale_chb.setEditable(stretch_chb.getValue()),
                                                        scale_attr_text.setEditable(stretch_chb.getValue() and 
                                                                                    global_scale_chb.getValue()),
                                                        scale_label.setEnable(stretch_chb.getValue() and 
                                                                                    global_scale_chb.getValue())))
    
    
    pm.checkBox(stretch_scale_chb, edit=True, label = "connect scale", parent = stretch_col, editable = stretch_chb.getValue())
    
    pm.checkBox(global_scale_chb, edit=True, label = "global scale", parent = global_scale_col, editable = stretch_chb.getValue(),
                                   changeCommand = lambda x: (scale_attr_text.setEditable(global_scale_chb.getValue()),
                                                              scale_label.setEnable(global_scale_chb.getValue())))
    pm.text(scale_label, edit = True, label = "scale attr", parent = global_scale_col, enable = (stretch_scale_chb.getValue() and 
                                                                                     stretch_chb.getValue))
    pm.textField(scale_attr_text, edit = True, text = "", parent = global_scale_col, editable = stretch_chb.getValue(), width = 90)
    
    
    ctrl_jnt_lbl = pm.text(label = "number of control joints ", parent = ctrl_jnt_col)
    ctrl_jnt_num = pm.textField(text = "3", parent = ctrl_jnt_col, width = 50)    
    
    

    create_btn_inv = pm.text(label = "", parent = create_btn_col)
    create_btn = pm.button(label = "create", align = "center", parent = create_btn_col, width = 100,
                           command = lambda x: call_fun(name_text.getText(), joint_name.getText(),
                                                        dense_chain_chb.getValue(), int(dense_div_text.getText()),
                                                        curve_create.getSelect(), curve_text.getText(),
                                                        curve_simple_chb.getValue(), int(spans_text.getText()),
                                                        stretch_chb.getValue(), stretch_scale_chb.getValue(),
                                                        int(ctrl_jnt_num.getText()), global_scale_chb.getValue(),
                                                        scale_attr_text.getText()))
    
    
    pm.showWindow(WINDOW)
    pm.window(WINDOW, edit=True, widthHeight=(250, 310))
    return None
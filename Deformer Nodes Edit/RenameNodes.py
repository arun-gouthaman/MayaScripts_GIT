import pymel.all as pm
class Rename_Nodes(object):
    
    def __init__(self):
        self.type_list = []
        self.get_node_types()
        self.main_ui()
        self.populate_node_list()
        return None
    
    
    def refresh_node_list(self):
        """
        clear and repopulate node type list
        """
        self.get_node_types()
        self.populate_node_list()
        return None
    
    def get_non_linear_type(self, **kwargs):
        """
        return the type of nonLinear node based on attributes of the nodes
        """
        non_linear_node = kwargs.get("non_linear_node", None)
        self.nonLinear_dict = {"endFlareX":"flare", "maxRadius":"wave", "curvature":"bend", "endSmoothness":"squash", "endAngle":"twist", "other":"sine"}
        node_type = self.nonLinear_dict["other"]
        for key in self.nonLinear_dict.keys():
            if pm.attributeQuery(key, node = non_linear_node, exists = True):
                node_type = self.nonLinear_dict[key]                
        return node_type
    
    def get_history_list(self, **kwargs):
        """
        return the list of history on selected objects
        """
        hist_lst = []
        sel_obj = kwargs.get("sel_obj", None)
        if not isinstance(sel_obj, list):
            sel_obj = [sel_obj]
        for obj in sel_obj:
            hist = pm.listHistory(obj)
            if not hist_lst:
                hist_lst = hist
            else:
                for nd in hist:
                    hist_lst.append(nd)
        return hist_lst
    
    
    def get_node_types(self):
        """
        Get the node types of object's history nodes
        if nonLinear, find the type of nonLinear nodes further
        """
        sel = pm.ls(selection = True)
        if not sel:
            self.type_list = []
            return None
        
        self.type_list = []
        hist = self.get_history_list(sel_obj = sel)
        for nd in hist:
            if isinstance(nd, pm.GeometryFilter):
                if nd.type() == "nonLinear":
                    nd_typ = self.get_non_linear_type(non_linear_node = nd)
                else:
                    nd_typ = nd.type()
                if nd_typ not in self.type_list:
                    self.type_list.append(nd_typ)
        return None
    
    def populate_node_list(self):
        """
        Clear and repopulate type list
        """
        self.node_lst.removeAll()
        self.node_lst.append(self.type_list)
        return None 
    
    
    
    
    def set_new_name(self, **kwargs):
        """
        set new name to the node passed
        """
        cur_nd = kwargs.get("cur_nd", None)
        nd_nm = kwargs.get("nd_nm", None)
        replace_to = kwargs.get("replace_to", None)
        id_val = kwargs.get("id_val", None)
        flag = False
        pm.rename(cur_nd, "TEMP_NODE_NAME")
        if pm.objExists(nd_nm):
            if replace_to:
                nd_nm = nd_nm.replace(replace_to, str(id_val)+replace_to)
            else:
                nd_nm = nd_nm+id_val
            flag = True
        pm.rename(cur_nd, nd_nm)
        return flag
    
    
    
    def rename_node(self, **kwargs):
        """
        rename all nodes of selected type from list
        """
        type_sel = kwargs.get("type_sel", None)
        replace_text = kwargs.get("replace_text", None)
        replace_to_text = kwargs.get("replace_to_text", None)
        new_name = kwargs.get("new_name", None)

        sel = pm.ls(selection = True)
        if not sel:
            return None
        
        if type_sel:
            if type_sel in self.nonLinear_dict.values():
                node_type = "nonLinear"
            else:
                node_type = type_sel
        
        for obj in sel:
            if not new_name:
                if not str(obj).find(replace_text)>-1:
                    self.message_win_ui("String not found", replace_text+" not found in selected object ("+str(obj)+")")
                    return None
            hist = self.get_history_list(sel_obj = obj)
            if replace_text and replace_to_text:
                nd_name = str(obj).replace(replace_text, replace_to_text)
            elif new_name:
                nd_name = new_name
            num_id = 1
            for nd in hist:
                if nd.type()==node_type:
                    if nd.type() =="nonLinear":
                        non_lin_nd = self.get_non_linear_type(non_linear_node = nd)
                        if non_lin_nd == type_sel.lower():
                            check_node_exist = self.set_new_name(cur_nd = nd, nd_nm = nd_name, replace_to = replace_to_text, id_val = str(num_id))
                            if check_node_exist:
                                num_id+=1
                    else:
                        check_node_exist = self.set_new_name(cur_nd = nd, nd_nm = nd_name, replace_to = replace_to_text, id_val = str(num_id))
                        if check_node_exist:
                            num_id+=1
                        
                            
            
        
        


        
        
        return None
    
    
    
    def rename_call(self, **kwargs):
        """
        call to rename node function
        """
        mode = kwargs.get("mode", None)
        selected_node_type = self.node_lst.getSelectItem()
        if not selected_node_type:
            self.message_win_ui("Type Selection", "Please select node type")
            return None
        if mode == "replace":
            if not (self.replace_txt.getText()) or not(self.replace_to_txt.getText()):
                self.message_win_ui("String not found", "Please enter Replace Text and Replace to Text")
                return None
            self.rename_node(type_sel = selected_node_type[0], 
                             replace_text = self.replace_txt.getText(), 
                             replace_to_text = self.replace_to_txt.getText(), 
                             new_name = None)
        elif mode == "rename":
            if not self.rename_txt.getText():
                self.message_win_ui("String not found", "Please enter rename text")
            self.rename_node(type_sel = selected_node_type[0], 
                 replace_text = None, 
                 replace_to_text = None, 
                 new_name = self.rename_txt.getText())
        
        return None
    
    def main_ui(self):
        WIN = "nodes_rename"
        if pm.window(WIN, query=True, exists=True):
            pm.deleteUI(WIN)
        pm.window(WIN, title = "Rename Nodes", iconName = "RNMND")
        main_col = pm.columnLayout(parent = WIN, adjustableColumn = True)
        row_col = pm.rowColumnLayout(parent = main_col, numberOfColumns = 2)
        
        
        
        type_list_col = pm.columnLayout(parent = row_col)
        pm.text(label = "Node Type List", parent = type_list_col)
        pm.separator(height = 5, style = "none")
        rename_col = pm.columnLayout(parent = row_col, adjustableColumn = True)
        self.node_lst = pm.textScrollList('Node_Type_List', numberOfRows=10, parent = type_list_col, 
                                 height=235, width = 150, allowMultiSelection = False)
        
        pm.separator(parent = rename_col, height = 20, style = "none")
        pm.text(label = "Gets name from selected mesh", parent = rename_col)
        pm.separator(parent = rename_col, height = 5, style ="none")
        name_from_col = pm.rowColumnLayout(parent = rename_col, numberOfColumns = 2, columnOffset = (2, "left", 11))
        pm.text(label = "Replace Text", parent = name_from_col)
        self.replace_txt = pm.textField(parent = name_from_col, text = "_MSH")
        
        name_to_col = pm.rowColumnLayout(parent = rename_col, numberOfColumns = 2, columnOffset = (2, "left", 5))
        pm.text(label = "Replace With", parent = name_to_col)
        self.replace_to_txt = pm.textField(parent = name_to_col)
        
        pm.button(label = "Rename (Replace)", parent = rename_col, command = lambda x:self.rename_call(mode = "replace"))
        
        pm.separator(parent = rename_col, height = 20)
        
        
        pm.text(label = "Rename nodes irrespective\n of mesh name", parent = rename_col)
        pm.separator(parent = rename_col, height = 5, style ="none")
        new_name_col = pm.rowColumnLayout(parent = rename_col, numberOfColumns = 2, columnOffset = (2, "left", 5))
        pm.text(label = "Rename", parent = new_name_col)
        self.rename_txt = pm.textField(parent = new_name_col )
        
        pm.button(label = "Rename (New)", parent = rename_col, command = lambda x:self.rename_call(mode = "rename"))
        
        pm.separator(parent = rename_col, height = 20)
        
        pm.button(label = "Refresh node List", parent = rename_col, command = lambda x: self.refresh_node_list())
        
        pm.separator(parent = rename_col, height = 20)

        pm.showWindow(WIN)
        pm.window(WIN, edit=True, widthHeight=(330, 260)) 
        return None
    
    def message_win_ui(self, win_title, win_message):
        pm.confirmDialog( title=win_title, message=win_message, button='Ok', defaultButton='Ok')
        return None

Rename_Nodes()
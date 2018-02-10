import pymel.all as pm
import HistNdFn
import os
class Rearrange_Nodes(object):
    """
    rearrange deformers on selected objects
    gets list of deformers type in order from source
    read deformers node from each selected object
    rearrange deformers in the order matching source
    
    Place the text file "deformers_order.txt" in the same path
    as this script
    """
    def __init__(self):
        self.order_file_path = self.get_cur_path(file_name = "deformers_order.txt")
        self.node_fun = HistNdFn.Hist_Nd_Fn()
        self.read_order_file()
        self.main_rearrange_ui()
        self.populate_list()
        return None
    
    #returns the current path of the script, 
    #the order source file added to the path
    def get_cur_path(self, **kwargs):
        file_name = kwargs.get("file_name", None)
        path = os.path.abspath(__file__)
        path = os.path.dirname(path)
        if file_name:
            path = path+"\\"+file_name
        return path

        
    #extract deformer list from source file
    def read_order_file(self):
        self.file_obj = open(self.order_file_path, "r")
        self.file_data = self.file_obj.readlines()
        self.file_ord_list = []
        for ln in self.file_data:
            if ln.rstrip():
                self.file_ord_list.append(ln.rstrip())
        self.file_obj.close()
        return None
    
    
    #get list of deformer nodes from selected object history
    def get_def_history_nodes(self, **kwargs):
        sel = kwargs.get("sel_nd", None)
        if not sel:
            sel = pm.ls(selection = True)
        if not sel:
            pm.displayWarning("No objects selected")
            return None
        def_list = []
        self.hist_nodes = self.node_fun.get_history_list(sel_obj = sel)
        for nd in self.hist_nodes:
            if isinstance(nd, pm.GeometryFilter):
                def_list.append(nd)
        return def_list
    
    #display the type of selected object
    def show_type(self):
        sel_nd = pm.ls(selection = True)
        if not sel_nd:
            pm.displayWarning("No node selected")
            return None
        if len(sel_nd)>1:
            pm.displayWarning("More than one node selected")
            return None
        typ = self.node_fun.find_node_type(check_node = sel_nd[0])
        if not typ:
            typ = sel_nd[0].type()
        self.nd_typ_txt.setText(typ.lower())
        return None
    
    #reorder deformers on selected objects
    def reorder_deformer_nodes(self, **kwargs):
        sel = pm.ls(selection = True)
        if not sel:
            pm.displayWarning("No object selected")
        ordered_def_list = kwargs.get("ordered_def_list", None)
        for obj in sel:
            #get list of history nodes that are deformers
            def_hist_nodes = self.get_def_history_nodes(sel_nd = obj)
            #arrange the obtained history node list
            ordered_def_list = self.node_fun.reorder_list(ref_list = self.file_ord_list, in_list = def_hist_nodes)
            if not ordered_def_list:
                pm.displayWarning("No ordered list returned")
                return None
            #set initial flag to true to start the node shuffle
            init_flag = True
            for index in range(len(ordered_def_list)):
                if not init_flag:
                    #move each deformers in the arranged list
                    pm.reorderDeformers(ordered_def_list[index-1], ordered_def_list[index], obj)
                    pass
                else:
                    #First shuffle
                    #move the first node from arranged list to position next to first deformer
                    #    on the object history
                    #swap the first and second deformers bringing the first deformer in list
                    #    to first in deformers list on the object
                    if not def_hist_nodes[0]==ordered_def_list[0]:
                        pm.reorderDeformers(def_hist_nodes[0], ordered_def_list[0], obj)
                        pm.reorderDeformers(ordered_def_list[0], def_hist_nodes[0], obj)
                    #set the initial contition to False to indicate the first run is passed    
                    init_flag = False
                    pass
            pm.select(clear = True)
            pm.select(sel)            
        return None
    
    
      
    
    
    def populate_list(self):
        self.ord_lst.removeAll()
        self.ord_lst.append(self.file_ord_list)
        return None
    
    
    
    def populate_order_edit_list(self):
        list_txt = self.ord_lst.getAllItems()
        strn = ""
        for item in list_txt:
            strn+=(item+"\r")
        return strn
    
    def save_deformer_list(self):
        self.file_obj = open(self.order_file_path, "w")
        txt_lst = self.reord_lst.getText().split("\n")
        for txt in txt_lst:
            if txt:
                txt+="\r\n"
                self.file_obj.write(txt)
        self.file_obj.close()
        self.read_order_file()
        self.ord_lst.removeAll()
        self.ord_lst.append(self.file_ord_list)        
        return None
    
    
    def main_rearrange_ui(self):
        WIN = "rearrange_nodes"
        if pm.window(WIN, query = True, exists = True):
            pm.deleteUI(WIN)
        pm.window(WIN, title = "Rearrange Nodes", iconName = "ReArNd")
        main_col = pm.columnLayout(parent = WIN, adjustableColumn = True)
        list_ord_col = pm.rowColumnLayout(parent = main_col, numberOfColumns = 3)
        ord_col_ch = pm.columnLayout(parent = list_ord_col, adjustableColumn = True)
        pm.separator(parent = list_ord_col, horizontal = False, width = 10)
        list_col_ch = pm.columnLayout(parent = list_ord_col, adjustableColumn = True)
        
        self.ord_lst = pm.textScrollList('deformers_reorder', numberOfRows=10, parent = ord_col_ch, 
                                 height=235, width = 150, allowMultiSelection = False, enable = False)

        pm.separator(style = "none", height = 20, parent = list_col_ch)
        self.nd_typ_txt = pm.textField(parent = list_col_ch, width = 150)
        pm.separator(style = "none", height = 10, parent = list_col_ch)
        pm.button(label = "Get Selected Node Type", parent = list_col_ch, command = lambda x: self.show_type())
        pm.separator(style = "in", height = 50, parent = list_col_ch)        
        pm.button(label = "Rearrange", height = 130, parent = list_col_ch, backgroundColor = (0.561, 0.737, 0.561), command = lambda x: self.reorder_deformer_nodes())        
        pm.button(label = "Edit Order List", parent = ord_col_ch, command = lambda x: self.reorder_edit_ui())
        pm.showWindow(WIN)
        pm.window(WIN, edit = True, widthHeight=(320, 260))
        return None


    def reorder_edit_ui(self):
        reorder_win = "Reorder_Deformer_List"
        if pm.window(reorder_win, query = True, exists = True):
            pm.deleteUI(reorder_win)
        pm.window(reorder_win, title = "Rearrange Deformers", iconName = "ReArDf")
        main_col = pm.columnLayout(parent = reorder_win, adjustableColumn = True)
        self.reord_lst = pm.scrollField('reorder_deformer_list', parent = main_col, 
                                 height=235, width = 150, text = self.populate_order_edit_list())
        
        pm.button("Save order list", parent = main_col, command = lambda x: self.save_deformer_list())        
        
        #self.reord_lst.append(self.file_ord_list)         
        pm.showWindow(reorder_win)
        pm.window(reorder_win, edit = True, widthHeight = (150, 260))
        return None


    def test_ui(self):
        test_win = "log"
        if pm.window(test_win, query = True, exists = True):
            pm.deleteUI(test_win)
        pm.window(test_win, title = "Rearrange Deformers", iconName = "ReArDf")
        log_col = pm.columnLayout(parent = test_win, adjustableColumn = True)
        self.log_txt = pm.scrollField('log_list', parent = log_col, 
                                 height=235, width = 150, wordWrap = True)
        
        
        #self.reord_lst.append(self.file_ord_list)         
        pm.showWindow(test_win)
        pm.window(test_win, edit = True, widthHeight = (300, 260))
        return None

#############Call script###########
#run the below in maya script editor Python Tab
import RearrangeDeformers
RearrangeDeformers.Rearrange_Nodes()
####################################
import pymel.all as pm
class Hist_Nd_Fn(object):
    
    def __init__(self):
        self.nonLinear_dict = {"endFlareX":"flare", "maxRadius":"wave", "curvature":"bend", "endSmoothness":"squash", "endAngle":"twist", "other":"sine"}
        return None
    
    def get_non_linear_type(self, **kwargs):
        non_linear_node = kwargs.get("non_linear_node", None)
        node_type = self.nonLinear_dict["other"]
        for key in self.nonLinear_dict.keys():
            if pm.attributeQuery(key, node = non_linear_node, exists = True):
                node_type = self.nonLinear_dict[key]                
        return node_type
    
    def get_history_list(self, **kwargs):
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
    
    
    
    def find_node_type(self, **kwargs):
        check_node = kwargs.get("check_node", None)
        nd_typ = None
        if not check_node:
            pm.displayWarning("No nodes received")
            return None
        if isinstance(check_node, pm.GeometryFilter):
            if check_node.type() == "nonLinear":
                nd_typ = self.get_non_linear_type(non_linear_node = check_node)
            else:
                nd_typ = check_node.type()
        return nd_typ
    
    
    def get_node_types(self):
        sel = pm.ls(selection = True)
        type_list = []
        if not sel:
            return type_list
        hist = self.get_history_list(sel_obj = sel)
        for nd in hist:
            type_list.append(self.find_node_type())
            """
            if isinstance(nd, pm.GeometryFilter):
                if nd.type() == "nonLinear":
                    nd_typ = self.get_non_linear_type(non_linear_node = nd)
                else:
                    nd_typ = nd.type()
                if nd_typ not in type_list:
                    type_list.append(nd_typ)
            """
        return  type_list
    
    
    
    def reorder_list(self, **kwargs):
        ref_list = kwargs.get("ref_list", None)
        in_list = kwargs.get("in_list", None)
        swap_pos = 0
        tmp = ""
        i = 0
        begin_index = 0
        for ref_item in ref_list:
            #print "TYP", ref_item
            #while begin_index<len(nodes):
            for i in range(begin_index, len(in_list)):
                #nd_typ = in_list[i].split("-")[0]
                #print typ
                nd_typ = self.find_node_type(check_node = in_list[i])
                #print ref_item
                #print nd_typ
                if nd_typ.lower() == ref_item.lower():
                    if not i==begin_index:
                        in_list[i], in_list[begin_index] =  in_list[begin_index], in_list[i]
                        print  in_list 
                    begin_index+=1
                    
        return in_list  
    

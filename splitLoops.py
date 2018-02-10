import pymel.all as pm
import re
import pdb
def split_loop():
    """
        returns individual edge loops anb verices conecting the loop
        from a selection of multiple edge loops
        
        Inputs : None
        
        Returns : (loops, verts)
                  Tuple of 2 lists, first list contains sublists, each sublists
                  contain the edge number of each each edge loops from selection,
                  second list contains sublists containing vertices of respective
                  edges from first list.
    """
    loops = []
    verts = []
    sel = pm.ls(orderedSelection=True, flatten=True)
    for edg in sel:
        if not isinstance(edg, pm.MeshEdge):
            return None
    temp_list = []
    temp_vrt_list = set()
    
    # Extract the first object from selection list to "temp_list" to be later used
    # as reference
    temp_list.append(sel.pop(0))
    
    # Run below loop until the selection list runs out of all remaining items
    while len(sel)>0:
        # Last added edge to the "temp_list" is used as reference
        ref_edg = temp_list[-1]
        # Obtain vertex from the reference edge
        ref_vert = pm.polyInfo(ref_edg, edgeToVertex = True)
        ref_vrt = re.findall("\d+", ref_vert[0])
        ref_vrt = [int(ref_vrt[1]), int(ref_vrt[2])]
        #temp_vrt_list.update(ref_vrt)#   
        shp = pm.ls(ref_edg, objectsOnly=True)
        trn = pm.listRelatives(shp, parent=True)[0]
        # Add vertes of the reference edge to "temp_vrt_list" set
        temp_vrt_list.add(str(trn+".vtx["+str(ref_vrt[0])+"]"))
        temp_vrt_list.add(str(trn+".vtx["+str(ref_vrt[1])+"]"))
        #pdb.set_trace()
        
        # Loop through all objects in selection list after removing the first item 
        # as reference
        for i in range(len(sel)):
            # Get the vertices of currernt edge compared with reference edge
            vert = pm.polyInfo(sel[i], edgeToVertex = True)
            vrt = re.findall("\d+", vert[0])
            vrt = [int(vrt[1]), int(vrt[2])]          
            
            # If the reference and current edge has matching vertices move the
            # current edge to "temp_list" 
            # (the currently moved edge becomes the reference in next iteration)
            if vrt[0] in ref_vrt or vrt[1] in ref_vrt:
                temp_list.append(sel.pop(i))
                #pdb.set_trace()
                break
            
            # If the loop has reached the end with no match, edge loop has been 
            # traversed, append the "temp_list" to "loops" and "temp_vrt_list" 
            # to "verts"
            elif i == len(sel)-1:
                loops.append(temp_list)
                verts.append(list(temp_vrt_list))
                temp_list = [sel.pop(0)]
                temp_vrt_list.clear()
                #pdb.set_trace()
                break
    
    # When selection list has run out of items, get the last appended edge
    # vertices from "temp_list" and append to "temp_vrt_list"
    if len(sel) == 0:
        ref_vert = pm.polyInfo(temp_list[-1], edgeToVertex = True)
        ref_vrt = re.findall("\d+", ref_vert[0])
        ref_vrt = [int(ref_vrt[1]), int(ref_vrt[2])]
        shp = pm.ls(temp_list[-1], objectsOnly=True)
        trn = pm.listRelatives(shp, parent=True)[0]
        temp_vrt_list.add(str(trn+".vtx["+str(ref_vrt[0])+"]"))
        temp_vrt_list.add(str(trn+".vtx["+str(ref_vrt[1])+"]"))
        #pdb.set_trace()
    
    # Append "temp_list" to "loops" and "temp_vert_list" to "verts"
    loops.append(temp_list)
    verts.append(list(temp_vrt_list))
    #pdb.set_trace()
    return loops, verts
    

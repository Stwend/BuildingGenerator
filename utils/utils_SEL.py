##\package buildingGen.utils.utils_SEL
# Selection utilities

import bpy
import math
from . import utils_OBJ, utils_MATH,utils_GLO,utils_GEOM
import mathutils







# from utils_GEOM


def getEdgePos(object, edgeID):
    v1 = object.data.edges[edgeID].vertices[0]
    v2 = object.data.edges[edgeID].vertices[1]
    
    ed = [object.data.vertices[v1].co,object.data.vertices[v2].co]
    return utils_MATH.getMidCoords(ed)
    
def getEdgeLength(object, edgeID):
    v1 = object.data.edges[edgeID].vertices[0]
    v2 = object.data.edges[edgeID].vertices[1]
    return utils_MATH.distanceEuler(object.data.vertices[v1].co,object.data.vertices[v2].co)
    
    
def getEdgeNormal (object, edgeID):
    v1 = object.data.edges[edgeID].vertices[0]
    v2 = object.data.edges[edgeID].vertices[1]

    #check if there are any polygons containing both vertices (= the edge)
    
    normals_list = []
    
    for poly in object.data.polygons:
        if v1 in poly.vertices and v2 in poly.vertices:
            normals_list.append(poly.normal)

    edge_normal = mathutils.Vector([0,0,0])
            
    length = len(normals_list)
    if length > 0:
        for normal in normals_list:
            edge_normal += normal

    
    edge_normal.normalize()
    
    return edge_normal
    
    
def getEdgeNormal_along(object,edgeID,axis = "Z",fallback = "X"):

    if not axis == fallback:
    
        v1 = object.data.vertices[object.data.edges[edgeID].vertices[0]]
        v2 = object.data.vertices[object.data.edges[edgeID].vertices[1]]
        
        vec = v1.co - v2.co
        vec.normalize()
        
        if axis == "Z":
            axisvec = mathutils.Vector([0,0,1])
        elif axis == "Y":
            axisvec = mathutils.Vector([0,1,0])
        elif axis == "X":
            axisvec = mathutils.Vector([1,0,0])
            
        if fallback == "Z":
            fallbackvec = mathutils.Vector([0,0,1])
        elif fallback == "Y":
            fallbackvec = mathutils.Vector([0,1,0])
        elif fallback == "X":
            fallbackvec = mathutils.Vector([1,0,0])
            
            
        res = vec.dot(axisvec)
        if res < 0:
            vec = -vec
        if res == 0:
            res = vec.dot(fallbackvec)
            if res < 0:
                vec = -vec
                    
        return vec
        
    return mathutils.Vector([0,0,0])
                
        
        
        
        






























##\brief Maps a selection to an object.
#\returns (List of lists of (Int)) The mapped selection.
#\param selection (List of lists of (Int)) The selection to be mapped.
#\param object (Object) The object the selection will be mapped to.
#\param selMode (String in ["v","e","f","ve","vf","ef","ev","ef","fv","fev"]) The selection mode.
#\param inv (Boolean) Whether to invert the selection or not.
#\param mapToVertices (Boolean) If true, will include vertices that are in edge/face selections, too (optional).
def mapSelection(selection, object,selMode,inv,mapToVertices = False):

    vgroup = selMode [1]
    selMode = selMode[0]
    
    if selection in ["X",["X"],None,[None]]:
        selection = []
        selection1 = [vert.index for vert in object.data.vertices]
        selection2 = [edge.index for edge in object.data.edges]
        selection3 = [face.index for face in object.data.polygons]
        
        selection = [selection1,selection2,selection3]
    
    
    if vgroup == "":
        selection_base_v = selection[0]
        selection_base_e = selection[1]
        selection_base_f = selection[2]
        
        
    else:
        selection_base_v = []
        selection_base_e = []
        selection_base_f = []
        
        if object.vertex_groups == None:
            return [[],[],[]]
        
        else:
            
            found = False
        
            for i in range(0,len(object.vertex_groups)):
                group = object.vertex_groups[i]
                if group.name == vgroup:
                    found = True
                    v_ind = i
                    break
            
            if not found:
                return [[],[],[]]
                
            else:
                
                for vertID in selection[0]:
                    vert = object.data.vertices[vertID]
                    if vert.groups != None:
                        for gr in vert.groups:
                            if v_ind == gr.group:
                                selection_base_v.append(vert.index)

                                
                                
                for edgeID in selection[1]:
                    edge = object.data.edges[edgeID]
                    found = True
                    for vID in edge.vertices:
                        if not vID in selection_base_v:
                            found = False
                            break
                    if found:
                        selection_base_e.append(edge.index)
                            
                            
                for faceID in selection[2]:
                    face = object.data.polygons[faceID]
                    found = True
                    for vID in face.vertices:
                        if not vID in selection_base_v:
                            found = False
                            break
                    if found:
                        selection_base_f.append(face.index)
                
        
        
        
        
    
    
    if selection in ["X",["X"],None,[None]]:
        selection = [selection_base_v,selection_base_e,selection_base_f]


    newsel_v = []
    newsel_e = []
    newsel_f = []
    
    if "v" in selMode:
        newsel_v = []
        for v in selection[0]:
            if v in selection_base_v:
                newsel_v.append(v)

            
      
    if "e" in selMode:
        
        for e in selection[1]:
            if e in selection_base_e:
                newsel_e.append(e)

            
     

    
    if "f" in selMode: 
        newsel_f = []
        for f in selection[2]:
            if f in selection_base_f:
                newsel_f.append(f)
        
        
    newsel = [newsel_v,newsel_e,newsel_f]
        
    
    if inv:
        selv = []
        sele = []
        selF = []
        
        if "v" in selMode:
            for vert in object.data.vertices:
                if not vert.index in newsel[0]:
                    selv.append(vert.index)
        
        if "e" in selMode:
            for edge in object.data.edges:
                if not edge.index in newsel[1]:
                    sele.append(edge.index)
        
        if "f" in selMode:
            print(newsel[2])
            for face in object.data.polygons:
                if not face.index in newsel[2]:
                    selF.append(face.index)
                
        newsel2 = [selv,sele,selF]
        
        if mapToVertices:
            return selectImplied(newsel2,object)
        return newsel2
        
    
    else:
    
        if mapToVertices:
            return selectImplied(newsel,object)
        return newsel

    
        
        
        
        
        
        
        
        
        
        
        
        
            
            
    
##\brief Select vertices that are in edge/face selections, too.
#\returns (List of lists of (Int)) The modified selection.
#\param selection (List of lists of (Int)) The selection to be mapped.
#\param ob (Object) The object the selection will be mapped to.
def selectImplied(selection,ob):

    
    for eID in selection[1]:
        selection[0].extend(ob.data.edges[eID].vertices)
        
    for fID in selection[2]:
        selection[0].extend(ob.data.polygons[fID].vertices)
        
    selection[0] = list(set(selection[0]))
    
    return selection
 

            
    
##\brief Select linked geometry.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of lists of (Int)) A selection of all linked geometry.
#\param ob (Object) The object the selection will be mapped to.
def sel_linked(ob):

    bpy.context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.select_linked()
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return ob_to_sel(ob)
        
        
        
##\brief Select less geometry.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of lists of (Int)) A selection of less geometry.
#\param ob (Object) The object the selection will be performed on.  
#\param iter (Int) How many iterations will be done.
#\param step (Boolean) Whether to include the step function introduced in Blender 2.73.  
def sel_less(ob,iter,step):

    iter = int(iter)
    
    bpy.context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    for i in range(0,iter):
        bpy.ops.mesh.select_less(use_face_step = step)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return ob_to_sel(ob)
        
    
    
    
    
##\brief Select more geometry.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of lists of (Int)) A selection of more geometry.
#\param ob (Object) The object the selection will be performed on. 
#\param iter (Int) How many iterations will be done.
#\param step (Boolean) Whether to include the step function introduced in Blender 2.73.     
def sel_more(ob,iter,step):

    iter = int(iter)
    
    bpy.context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    for i in range(0,iter):
        bpy.ops.mesh.select_more(use_face_step = step)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return ob_to_sel(ob)
    
    

##\brief Select edge loops.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of lists of (Int)) A selection of loops.
#\param ob (Object) The object the selection will be performed on.   
def sel_loop(ob):
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.loop_multi_select(ring=False)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')

    e = []

            
    for edge in ob.data.edges:
        if edge.select:
            e.append(edge.index)
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    v = []
    f = []
    
    for vert in ob.data.vertices:
        if vert.select:
            v.append(vert.index)

    for face in ob.data.polygons:
        if face.select:
            f.append(face.index)
            
    return [v,e,f]
    
 


##\brief Select edge rings.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of lists of (Int)) A selection of rings.
#\param ob (Object) The object the selection will be performed on.   
def sel_ring(ob):
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.loop_multi_select(ring=True)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')

    e = []

            
    for edge in ob.data.edges:
        if edge.select:
            e.append(edge.index)
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    v = []
    f = []
    
    for vert in ob.data.vertices:
        if vert.select:
            v.append(vert.index)

    for face in ob.data.polygons:
        if face.select:
            f.append(face.index)
            
    return [v,e,f]
    
    
    
    
    
    
##\brief Select the region's skeleton.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of lists of (Int)) A skeleton selection.
#\param ob (Object) The object the selection will be performed on.  
def sel_skeleton(ob):

    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.hide(unselected=True)
    bpy.ops.mesh.select_mode(type="EDGE")
    bpy.ops.mesh.region_to_loop()
    bpy.ops.mesh.select_all(action = "INVERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return ob_to_sel(ob)
    
    
    
##\brief Select the region's border.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of lists of (Int)) A border selection.
#\param ob (Object) The object the selection will be performed on.   
def sel_border(ob):
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.region_to_loop()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return ob_to_sel(ob)
    
    
    
   
def skeleton_ring(object):
    
    #Get all selected edges
    sel_e = []
    for edge in object.data.edges:
        if edge.select:
            sel_e.append(edge.index)
            
            
    
    
    #get all edges without two selected faces, deselect them
    

    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type="EDGE")
    bpy.ops.mesh.region_to_loop()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    sel_eB = []
    for edge in object.data.edges:
        if edge.select:
            sel_eB.append(edge.index)
        
    
    
    #select edge ring
    

    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = "DESELECT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for eid in sel_e:
        if not eid in sel_eB:
            object.data.edges[eid].select = True
        
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.loop_multi_select(ring=True)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for edge in object.data.edges:
        if edge.select:
            if not edge.index in sel_e:
                edge.select = False
    
    
    #deselect all edges that are not in bounds
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.loop_multi_select(ring=True)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for edge in object.data.edges:
        if edge.select:
            if not edge.index in sel_e:
                edge.select = False
                
                



##\brief Transfer the selected geometry of an object to a custom selection.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of lists of (Int)) The transferred selection.
#\param ob (Object) The object the selection will be performed on.                
def ob_to_sel(ob):

    v = []
    e = []
    f = []
    
    for vert in ob.data.vertices:
        if vert.select and not vert.hide:
            v.append(vert.index)
            
    for edge in ob.data.edges:
        if edge.select and not edge.hide:
            e.append(edge.index)
            
    for face in ob.data.polygons:
        if face.select and not face.hide:
            f.append(face.index)
            
    return [v,e,f]
                
                
                
                
                
##\brief Select extrema.
#\returns (List of lists of (Int)) The selection.
#\param ob (Object) The object the selection will be performed on. 
#\param sel (List of lists of (Int)) The selection that the object will use.
#\param axis (Int in [0,1,2]) The axis that will be checked for extrema.
#\param mode (Int in [0,1]) The extrema mode. 0 is maxima, 1 is minima.
#\extend (Boolean) Whether to extend the selection to previously unselected geometry.        
def selectExtrema(ob, sel, axis, mode, extend):

    selv = []
    sele = []
    selF = []


    currentvVal = None
    currenteVal = None
    currentfVal = None
    
    if len(ob.data.vertices) > 0:

        if mode == 0:
        
            currentvVal = -50000
        
            for vID in sel[0]:
                if ob.data.vertices[vID].co[axis] > currentvVal:
                    currentvVal = ob.data.vertices[vID].co[axis]
                    
        else:
        
            currentvVal = 50000
        
            for vID in sel[0]:
                if ob.data.vertices[vID].co[axis] < currentvVal:
                    currentvVal = ob.data.vertices[vID].co[axis]
                    
                    
    if len(ob.data.edges) > 0:
        
    
        if mode == 0:
        
            currenteVal = -50000
    
            for eID in sel[1]:
                epos = getEdgePos(ob,eID)[axis]
                if epos > currenteVal:
                    currenteVal = epos
                
                
        else:
        
            currenteVal = 50000
        
            for eID in sel[1]:
                epos = getEdgePos(ob,eID)[axis]
                if epos < currenteVal:
                    currenteVal = epos
                        
    if len(ob.data.polygons) > 0:
        
        if mode == 0:
        
            currentfVal = -50000
        
            for fID in sel[2]:
                if ob.data.polygons[fID].center[axis] > currentfVal:
                    currentfVal = ob.data.polygons[fID].center[axis]
                    
        else:
        
            currentfVal = 50000
            
            for fID in sel[2]:
                if ob.data.polygons[fID].center[axis] > currentfVal:
                    currentfVal = ob.data.polygons[fID].center[axis]
                
                
    
                        
    
    #another walkthrough to determine all verts, edges, faces with the max value
    
    if not currentvVal == None:
    
        if not extend:
        
            for vID in sel[0]:
                
                if math.fabs(ob.data.vertices[vID].co[axis] - currentvVal) < 0.01:
                    
                    selv.append(vID)
                    
        else:
        
            for vert in ob.data.vertices:
            
                if math.fabs(vert.co[axis] - currentvVal) < 0.01:
                    
                    selv.append(vert.index)
                    
                    
    if not currenteVal == None:
    
        if not extend:
        
            for eID in sel[1]:
            
                epos = getEdgePos(ob,eID)[axis]
                
                if math.fabs(epos - currenteVal) < 0.01:
                
                    sele.append(eID)
                
                
        
        else:
        
            for edge in ob.data.edges:
                
                epos = getEdgePos(ob,edge.index)[axis]
                
                if math.fabs(epos - currenteVal) < 0.01:
                
                    sele.append(edge.index)
                    
                    
    if not currentfVal == None:
        if not extend:
            for fID in sel[2]:
                if math.fabs(ob.data.polygons[fID].center[axis] - currentfVal) < 0.01:
                    
                    selF.append(fID)
                    
        else:
        
            for face in ob.data.polygons:
            
                if math.fabs(face.center[axis] - currentfVal) < 0.01:
                    
                    selF.append(face.index)
                    
    selection = [selv, sele, selF]
    
    return selection
                    
            
            
    
    
##\brief Select directional.
#\returns (List of lists of (Int)) The selection.
#\param ob (Object) The object the selection will be performed on. 
#\param sel (List of lists of (Int)) The selection that the object will use.
#\param vec (mathutils.Vector) The vector that will be checked.
#\param extra (String in ["Signed","Signed Inverted","Unsigned"]) What directions to use.
#\param edges (Boolean) Whether to use the alternative edge normal calculation "along".
def selectDirectional(ob, sel, vec, extra, edges):

    sel_v = []
    sel_e = []
    sel_f = []

    if extra == "Signed Inverted":
        vec = -vec
    
    for vID in sel[0]:
        vert = ob.data.vertices[vID]
        
        res = vert.normal.dot(vec)
        
        if extra == "Unsigned":
            res = math.fabs(res)
            
        if res > 0:
            sel_v.append(vID)
            
    for fID in sel[2]:
        face = ob.data.polygons[fID]
        
        res = face.normal.dot(vec)
        
        if extra == "Unsigned":
            res = math.fabs(res)
            
        if res > 0:
            sel_f.append(fID)  
            
            
    if not edges:
        
        for eID in sel[1]:
            nor = getEdgeNormal(ob,eID)
            
            if not nor.length == 0:
                res = math.fabs(nor.dot(vec))
                
                if extra == "Unsigned":
                    res = math.fabs(res)
   
                if res > 0:
                    sel_e.append(eID)
                    
    else:
        
        for eID in sel[1]:
            nor = getEdgeNormal_along(ob,eID)
            
            if not nor.length == 0:
                res = math.fabs(nor.dot(vec))
   
                if res > 0:
                    sel_e.append(eID)
                    
                    
    selection = [sel_v,sel_e,sel_f]
    
    return selection
    
    
 

##\brief Select similar geometry.
#\returns The modified selection.
#\param ob (Object) The object the selection will be performed on. 
#\param vm (String in ["Normal","Vertex Group","Face Amount","Edge Amount"]) What kind of similarity mode will be used.
def sel_similar_v(ob,vm):

    bpy.ops.object.mode_set(mode = 'EDIT')
    
    if vm == "Normal":
        
        bpy.ops.mesh.select_similar(type="NORMAL")
        
    elif vm == "Vertex Group":
    
        bpy.ops.mesh.select_similar(type="VGROUP")
        
    elif vm == "Face Amount":
    
        bpy.ops.mesh.select_similar(type="FACE")
        
    else:
    
        bpy.ops.mesh.select_similar(type="EDGE")
    
    
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return ob_to_sel(ob)
    


##\brief Select similar geometry.
#\returns The modified selection.
#\param ob (Object) The object the selection will be performed on. 
#\param fm (String in ["Length","Direction","Face Amount","Face Angles"]) What kind of similarity mode will be used.      
def sel_similar_e(ob,em):

    bpy.ops.object.mode_set(mode = 'EDIT')
    
    if em == "Length":
        
        bpy.ops.mesh.select_similar(type="LENGTH")
        
    elif em == "Direction":
        
        bpy.ops.mesh.select_similar(type="DIR")
        
    elif em == "Face Amount":
        
        bpy.ops.mesh.select_similar(type="FACE")
        
    elif em == "Face Angles":
        
        bpy.ops.mesh.select_similar(type="FACE_ANGLE")
        

    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return ob_to_sel(ob)
    
    


##\brief Select similar geometry.
#\returns The modified selection.
#\param ob (Object) The object the selection will be performed on. 
#\param fm (String in ["Area","Sides","Normal"]) What kind of similarity mode will be used.    
def sel_similar_f(ob,fm):

    bpy.ops.object.mode_set(mode = 'EDIT')
    
    if fm == "Area":
        
        bpy.ops.mesh.select_similar(type="AREA")
        
    elif fm == "Sides":
        
        bpy.ops.mesh.select_similar(type="SIDES")
        
    elif fm == "Normal":
        
        bpy.ops.mesh.select_similar(type="NORMAL")

    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return ob_to_sel(ob)
    
    
    
##\brief Select by cavity.
#\returns The modified selection.
#\param ob (Object) The object the selection will be performed on. 
#\param mode (String in ["c","v"]) Whether to perform a search for concave ("c") or convex ("v") geometry.
#\param strict (Boolean) Apply strict rules. Vertices and faces with more than one type of cavity will be ignored.
#\param borders (Boolean) Whether to include selection borders in the search.     
def sel_cavity(ob,mode,strict,borders):
    
    sel_e = []
    sel_f = []
    
    if mode == "c":
        for edge in ob.data.edges:
            if edge.select and not edge.hide:
                
                faces = utils_GEOM.getEdgeNeighborFaces(ob,edge)
                
                check = len(faces)
                
                if check == 2:
                    
                    result = (faces[1].center-faces[0].center).dot(faces[0].normal)
                    
                    if strict and result > 0:
                        sel_e.append(edge.index)
                    elif result >= 0:
                        sel_e.append(edge.index)
                        
                elif check < 2 and borders:
                    sel_e.append(edge.index)
                    
                        
                        
                        
                        
    elif mode == "v":
        for edge in ob.data.edges:
            if edge.select and not edge.hide:
                
                faces = utils_GEOM.getEdgeNeighborFaces(ob,edge)
                
                check = len(faces)
                
                if check == 2:
                    
                    result = (faces[1].center-faces[0].center).dot(faces[0].normal)
                    
                    if strict and result < 0:
                        sel_e.append(edge.index)
                    elif result <= 0:
                        sel_e.append(edge.index)
                        
                elif check < 2 and borders:
                    sel_e.append(edge.index)
                                    
                        
    return [[],sel_e,sel_f]
                
                
                
            
    
    
    
    
    
        
            
    
    
    
    
    
    
    
    
    
    
    
    
    
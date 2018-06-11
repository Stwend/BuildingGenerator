##\package buildingGen.utils.utils_OBJ
# Object utilities


import bpy
import math

from . import utils_GLO
from .utils_GLO import print_debug


##\brief Duplicates a mesh.
#\returns (Mesh) The duplicated mesh.
#\param copymesh (Mesh) The mesh to be duplicated.
def duplicateMesh(copymesh):

    mesh_new = bpy.data.meshes.new("")
    mesh_new = copymesh.copy()

    return mesh_new




##\brief Duplicates an object (Background).
#\returns (Object) The duplicated object.
#\param object (Object) The object to be duplicated.
def copyobj(object):


    clear_selection()

    if isinstance(object,bpy.types.Object):
        print_debug("Copying(BG):",object.name)


    
        name = object.name
        
        
        object.name = "_CPY"
        bpy.context.scene.objects.link(object)
        object.select = True
        bpy.context.scene.objects.active = object
        
        bpy.ops.object.duplicate()
        
        object.name = name
        
        for obj in bpy.context.scene.objects:
            if obj.name.startswith("_CPY"):
                copyob = obj
                break
        
        bpy.context.scene.objects.unlink(object)
        bpy.context.scene.objects.unlink(copyob)
        
        print_debug("   -> Copy:",copyob.name)
        
        copyob.name = "_$OBS$_"
        
        return copyob
    
##\brief Duplicates an object (Foreground).
#\returns (Object) The duplicated object.
#\param object (Object) The object to be duplicated.   
def copyobj_vis(object):
    
    clear_selection()

    if isinstance(object,bpy.types.Object):
    
        print_debug("Copying(FG):",object.name)
        
        name = object.name

        
        object.name = "_CPY"
        object.select = True
        bpy.context.scene.objects.active = object
        
        bpy.ops.object.duplicate()
        
        object.name = name
        
        for obj in bpy.context.scene.objects:
            if obj.name.startswith("_CPY"):
                copyob = obj
                break
        
        print_debug("   -> Copy:",copyob.name)
        
        copyob.name = "_$OBS$_"
        
        return copyob
        
        
        
        
        
##\brief Selects all layers in the scene.
#\returns (List of (Boolean)) The previously selected layers.      
def enableLayers():
    layerCurrent = getActiveLayers()
    selectLayers([True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True])
    return layerCurrent

##\brief Returns the layer selection to the previous one.
#\returns (None)    
#\param layerCurrent (List of (Boolean)) The previously selected layers. 
def disableLayers(layerCurrent):
    selectLayers(layerCurrent)
    
    



##\brief Gets the object linked to a mesh.
#\returns (Object) The found object, or (None) if not found.   
#\param mesh (Mesh) The mesh.
def findObjectFromMesh(mesh):
    for o in bpy.data.objects:
        if o.type == "MESH":
            if o.data.name == mesh.name:
                return o
                
                
##\brief Deselects all objects in the current scene.
#\returns (None)               
def clear_selection():
    for ob in bpy.context.scene.objects:
        ob.select = False







##\brief Adds a new object to the scene.
#\returns (Object) The new object.
def addObject():
    bpy.ops.object.add(type='MESH')
    ob = bpy.context.object

    return ob




    






##\brief Collects and deletes all obsolete objects.
#\detail bpy.data.objects is searched for objects starting with "_$OBS$_". Those objects are deleted.
#\returns (None)
def collectGarbage():

    layerCurrent = getActiveLayers()
    selectLayers([True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True])
    for ob1 in bpy.context.scene.objects:
        ob1.select = False
    for ob1 in bpy.data.objects:
        ob1.select = False

    count = 0
    for ob in bpy.data.objects:
        ob.select = False
        
        if "_$OBS$_" in ob.name:
            
            for scene in bpy.data.scenes:
                try:
                    scene.objects.unlink(ob)
                except:
                    pass
                
            count += 1
            print_debug("Deleting obsolete object.")
            print_debug("   -> Deleted so far:",count)
            bpy.data.objects.remove(ob)
            
    length = len(bpy.data.objects)
    
    print_debug("")
    print_debug("Garbage Collector: removed "+str(count)+" objects. Remaining: "+str(length))
    print_debug("")
    print_debug("Remaining objects(FG):")
    for ob in bpy.context.scene.objects:
        print_debug(ob.name)
        
    print_debug("Remaining objects(BG):")
    for ob in bpy.data.objects:
        print_debug(ob.name)


    selectLayers(layerCurrent)






def getActiveLayers():
    list = []
    for i in range (0,20):
        if bpy.context.scene.layers[i] == True:
            list.append(True)
        else:
            list.append(False)
    return list





def selectLayers(list):
    bpy.context.scene.layers = list








##\brief Prepares an object to be used in a node.
#\returns (None)
#\param object (Object) The object to be prepared.
#\param selection (List of lists of (Int)) The selection to be performed on the object.
#\param sel_mode (String in ["VERT","EDGE","FACE"]) The mode to perform the selection in.
def prep(object, selection, sel_mode):

    if selection == "X":
        prep_all(object,sel_mode)
    else:

        bpy.context.scene.objects.link(object)
        bpy.context.scene.objects.active = object
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type=sel_mode)
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action = "DESELECT")
        bpy.ops.object.mode_set(mode = 'OBJECT')

        
        if len(selection[0]) > 0: 
            for vid in selection[0]:
                object.data.vertices[vid].select = True

        if len(selection[1]) > 0: 
            for eid in selection[1]:
                object.data.edges[eid].select = True
        
        if len(selection[2]) > 0:   
            for fid in selection[2]:
                object.data.polygons[fid].select = True
        
##\brief Prepare a list of objects
#\returns (None)  
#\param list (List of (Object)) List of objects to be prepared.      
def prep_list(list):
    for item in list:
        bpy.context.scene.objects.link(item)

##\brief De-prepare a list of objects
#\returns (None)   
#\param list (List of (Object)) List of objects to be de-prepared.     
def deprep_list(list):
    for item in list:
        bpy.context.scene.objects.unlink(item)
        
        
        
##\brief Prepare objects with everything selected.
#\returns (None)
#\param object (Object) The object to be prepared.  
#\param sel_mode (String in ["VERT","EDGE","FACE"]) The mode to perform the selection in(optional).  
def prep_all(object,sel_mode = "VERT"):

    bpy.context.scene.objects.link(object)
    bpy.context.scene.objects.active = object
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type=sel_mode)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action = "SELECT")
    bpy.ops.object.mode_set(mode = 'OBJECT')


##\brief Prepare an object with no selection.
#\returns (None) 
#\param object (Object) The object to be prepared.  
def prep_min(object):
    bpy.context.scene.objects.link(object)

##\brief De-prepare an object
#\returns (None)
#\param object (Object) The object to be prepared.  
def deprep(object):
    
    bpy.context.scene.objects.active = object
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.reveal()
    bpy.ops.object.mode_set(mode = 'OBJECT')

    bpy.context.scene.objects.unlink(object)
    
##\brief Delete all vertices, edges and faces.
#\returns (None)
#\param ob (Object) The object to be emptied.
def empty(ob):

    bpy.context.scene.objects.active = ob

    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = "SELECT")
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
 
##\brief Join a list of objects.
#\returns (Object) The joined object.
#\param ob (List of (Object)) The objects to be joined.   
def join(obs):

    if len(obs) > 1:

        name = obs[0].name

        scene = bpy.context.scene
        ctx = bpy.context.copy()

        
        ctx['active_object'] = obs[0]

        ctx['selected_objects'] = obs
        
        ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]

        bpy.ops.object.join(ctx)
        
        return findBGOb(name)
        
    elif len(obs) == 0:
        return None
        
    else:
        return obs[0]
    
##\brief Hide all objects except a few.
#\returns (None)
#\param exclude (List of (Object)) The objects to be excluded(optional).    
def hide_all(exclude = []):
    for ob in bpy.context.scene.objects:
        if not ob in exclude:
            ob.hide = True
        else:
            ob.hide = False
            
            
##\brief Find an object (Background)
#\returns (Object) if found.
#\exception (Exception) if no object has been found.  
#\param n (Strng) The object's name.        
def findBGOb(n):

    for ob in bpy.data.objects:
        if ob.name == n:
            return ob
            
    print_debug("(BG) Object "+n+" not found.")
    
    raise Exception("(BG) Object not found.")
    
##\brief Find an object (Foreground)
#\returns (Object) if found, else (None).
#\param n (Strng) The object's name.   
def findFGOb(n):

    for ob in bpy.data.objects:
        if ob.name == n:
            return ob
            
    print_debug("(BG) Object "+n+" not found.")
    
    
##\brief Apply all transforms to an object.
#\returns (None)
#\param ob (Object) The object which should get its transforms applied.   
def applyTransforms(ob):
    clear_selection()
    try:
        bpy.context.scene.objects.link(ob)
    except:
        pass
    bpy.context.scene.objects.active = ob
    ob.select = True
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.objects.unlink(ob)
    
##\brief Prepare an object to be transformed.
#\returns (None)
#\param ob (Object) The object to be prepared.       
def prepTransforms(ob):
    clear_selection()
    try:
        bpy.context.scene.objects.link(ob)
    except:
        pass
    bpy.context.scene.objects.active = ob
    ob.select = True
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.context.scene.objects.unlink(ob)
    
    
    
    

    


##\package buildingGen.nodes.building_nodes_SEL
# Selection nodes.

import bpy
from bpy.types import NodeTree, Node, NodeSocket

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

from bpy.props import EnumProperty, StringProperty, BoolProperty, CollectionProperty

import custom_sockets


from . import building_NODETREE
from .building_NODETREE import *

from utils import utils_MATH, utils_GEOM, utils_GEN, utils_SEL,utils_OBJ,utils_GLO
import math
import mathutils
from random import randrange

 
        
        
##\brief Logical combination of selections.
#\detail Uses boolean operators to combine two selections.        
class SEL_CombineSelectionNode(buildingNode):

    bl_idname = 'SEL_CombineSelectionNode'

    bl_label = 'Combine'

    bl_icon = 'NODETREE'
    
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
        
        
    

	#NODE DATA
    
    lastmode = StringProperty(default = "",update = updateEmpty) 
    
    corrupted = BoolProperty(default = True, update = updateEmpty)

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
    
        if self.lastmode != self.mode_combine:
            self.lastmode = self.mode_combine
            outdated = True
            
        if outdated:
            self.callObsolete(context)   
    
    
    
    c_modes = [("AND","AND",""),("OR","OR",""),("XOR","XOR",""),("NOT","NOT","")]
    
    mode_combine = EnumProperty(
        name = "Choose Mode",
        items = c_modes,
        update = updateNode
    )
    
    
    
    
    

                    
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_MESH", "Mesh")
        self.inputs.new("socket_SELECTION", "Selection 1")
        self.inputs.new("socket_SELECTION", "Selection 2")
        self.outputs.new("socket_SELECTION", "Selection")
        
        
        self.use_custom_color = True
        self.color = (.7,.9,1)
        


    ##\brief GUI.    
    def draw_buttons(self, context, layout):
        layout.separator()
        rowM = layout.row(align = True)
   
        rowC = layout.row(align = True)
        rowC.prop(self, "mode_combine", "")
        
        
        
        layout.separator()

        
        
    ##\brief Re-calculates the node's data.
    def recalculate(self):
        self.corrupted = False
    
        retsels = []
        
        if len(self.inputs[0].links) > 0 and len(self.inputs[1].links) > 0 and len(self.inputs[2].links) > 0:

            #get selections
            
            print("getting data...")
            print("objects")
            obs = self.inputs[0].returnData()
            print("selections 1")
            selection_1 = self.inputs[1].returnData()
            print("selections 2")
            selection_2 = self.inputs[2].returnData()
            
            sels = utils_GEN.adjustLists([selection_1, selection_2,obs])
            
            selection_1 = sels[0]
            selection_2 = sels[1]
            obs = sels[2]
            
            if self.mode_combine == "OR":
                for i in range(0, len(selection_1)):
                
                    sel_1 = utils_SEL.mapSelection(selection_1[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    sel_2 = utils_SEL.mapSelection(selection_2[i], obs[i],[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv)
                    
                    selv = sel_1[0]
                    sele = sel_1[1]
                    selF = sel_1[2]
                    
                    selv_2 = sel_2[0]
                    sele_2 = sel_2[1]
                    self_2 = sel_2[2]
                    
                    selv.extend(selv_2)
                    sele.extend(sele_2)
                    selF.extend(self_2)
                    
                    selv = list(set(selv))
                    sele = list(set(sele))
                    selF = list(set(selF))
                    
                    selection = [selv, sele, selF]

                    retsels.append(selection)
                    
                    
                
            elif self.mode_combine == "AND":
                for i in range(0, len(selection_1)):
                
                    
                    selv_fin = []
                    sele_fin = []
                    self_fin = []
                
                
                    sel_1 = utils_SEL.mapSelection(selection_1[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    sel_2 = utils_SEL.mapSelection(selection_2[i], obs[i],[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv)
                    
                    
                
                    selv = sel_1[0]
                    sele = sel_1[1]
                    selF = sel_1[2]
                    
                    selv_2 = sel_2[0]
                    sele_2 = sel_2[1]
                    self_2 = sel_2[2]
                    
                    for vid in selv:
                        if vid in selv_2:
                            selv_fin.append(vid)
                            
                    for eid in sele:
                        if eid in sele_2:
                            sele_fin.append(eid)
                            
                    for fid in selF:
                        if fid in self_2:
                            self_fin.append(fid)
                            
                    selection = [selv_fin, sele_fin, self_fin]
                    
                    retsels.append(selection)
                    
                
                
                    
   
            elif self.mode_combine == "XOR":
                for i in range(0, len(selection_1)):
                
                
                    selv_fin = []
                    sele_fin = []
                    self_fin = []
                    
                
                    sel_1 = utils_SEL.mapSelection(selection_1[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    sel_2 = utils_SEL.mapSelection(selection_2[i], obs[i],[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv)
                    
            
                    selv = sel_1[0]
                    sele = sel_1[1]
                    selF = sel_1[2]
                    
                    selv_2 = sel_2[0]
                    sele_2 = sel_2[1]
                    self_2 = sel_2[2]
                
                    for vid in selv:
                        if not vid in selv_2:
                            selv_fin.append(vid)
                            
                    for eid in sele:
                        if not eid in sele_2:
                            sele_fin.append(eid)
                            
                    for fid in selF:
                        if not fid in self_2:
                            self_fin.append(fid)
                            
                    for vid in selv_2:
                        if not vid in selv:
                            selv_fin.append(vid)
                            
                    for eid in sele_2:
                        if not eid in sele:
                            sele_fin.append(eid)
                            
                    for fid in self_2:
                        if not fid in selF:
                            self_fin.append(fid)
                    
                    selection = [selv_fin, sele_fin, self_fin]
                    
                    retsels.append(selection)
                    
            elif self.mode_combine == "NOT":
                for i in range(0, len(selection_1)):
                
                
                    selv_fin = []
                    sele_fin = []
                    self_fin = []
                
                
                    sel_1 = utils_SEL.mapSelection(selection_1[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    sel_2 = utils_SEL.mapSelection(selection_2[i], obs[i],[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv)
                    
            
                    selv = sel_1[0]
                    sele = sel_1[1]
                    selF = sel_1[2]
                    
                    selv_2 = sel_2[0]
                    sele_2 = sel_2[1]
                    self_2 = sel_2[2]
                    
                    for vid in selv:
                        if not vid in selv_2:
                            selv_fin.append(vid)
                            
                    for eid in sele:
                        if not eid in sele_2:
                            sele_fin.append(eid)
                            
                    for fid in selF:
                        if not fid in self_2:
                            self_fin.append(fid)
                            
                    selection = [selv_fin, sele_fin, self_fin]
                    
                    retsels.append(selection)
            

            
            if self.outputs[0].enabled:
                self.outputs[0].setData(retsels)
                
            for ob in obs:
                ob.name = "_$OBS$_"
                      
        
        



##\brief Refining of selections.
#\detail Builds new selections based on input selections.                
class SEL_ShapeSelectionNode(buildingNode):

    bl_idname = 'SEL_ShapeSelectionNode'

    bl_label = 'Refine'

    bl_icon = 'NODETREE'
    
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
        

    

    #NODE DATA
    
    mode_list_l = StringProperty(default = "",update = updateEmpty)
    sim_modes_l = StringProperty(default = "",update = updateEmpty)
    sim_vmodes_l = StringProperty(default = "",update = updateEmpty)
    sim_emodes_l = StringProperty(default = "",update = updateEmpty)
    sim_fmodes_l = StringProperty(default = "",update = updateEmpty)
    borders_real_l = BoolProperty(default = True,update = updateEmpty)
    face_step_l = BoolProperty(default = True,update = updateEmpty)
    cav_strict_l = BoolProperty(default = True,update = updateEmpty)
    cav_borders_l = BoolProperty(default = True,update = updateEmpty)
    cav_mode_l = StringProperty(default = "",update = updateEmpty)
    
    corrupted = BoolProperty(default = True, update = updateEmpty) 


    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
        
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
        
        
        #CHECK ALL PARAMETERS
        if self.mode_list_l != self.mode_list:
            self.mode_list_l = self.mode_list
            outdated = True
            
        if self.sim_modes_l != self.sim_modes:
            self.sim_modes_l = self.sim_modes
            outdated = True
            
        if self.sim_vmodes_l != self.sim_vmodes:
            self.sim_vmodes_l = self.sim_vmodes
            outdated = True
            
        if self.sim_emodes_l != self.sim_emodes:
            self.sim_emodes_l = self.sim_emodes
            outdated = True
            
        if self.sim_fmodes_l != self.sim_fmodes:
            self.sim_fmodes_l = self.sim_fmodes
            outdated = True
            
        if self.borders_real_l != self.borders_real:
            self.borders_real_l = self.borders_real
            outdated = True
            
        if self.face_step_l != self.face_step:
            self.face_step_l = self.face_step
            outdated = True
            
        if self.cav_strict_l != self.cav_strict:
            self.cav_strict_l = self.cav_strict
            outdated = True
            
        if self.cav_borders_l != self.cav_borders:
            self.cav_borders_l = self.cav_borders
            outdated = True
            
        if self.cav_mode_l != self.cav_mode:
            self.cav_mode_l = self.cav_mode
            outdated = True
            
            
            
    
    
        if outdated:            
            self.updateInputs(context)
            self.callObsolete(context)
    
    
    
    modes = [("Linked","Linked",""),("Less","Less",""),("More","More",""),("Loops","Loops",""),("Rings","Rings",""),("Borders","Borders",""),("Skeleton","Skeleton",""),("Similar","Similar",""),("Cavity","Cavity","")]
    sim_m = [("Vertices","Vertices",""),("Edges","Edges",""),("Faces","Faces","")]
    sim_vm = [("Normal","Normal",""),("Vertex Group","Vertex Group",""),("Face Amount","Adj. Faces",""),("Edge Amount","Con. Edges","")]
    sim_em = [("Length","Length",""),("Direction","Direction",""),("Face Amount","Adj. Faces",""),("Face Angles","Face Angles","")]
    sim_fm = [("Area","Area",""),("Sides","Sides",""),("Normal","Normal","")]
    cav_m = [("c","Concave",""),("v","Convex","")]
    
    
    
    mode_list = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Selection Modes",
        update = updateNode
    )
    
    sim_modes = EnumProperty(
        name = "Choose Mode",
        items = sim_m,
        description = "Selection Modes",
        update = updateNode
    )
    sim_vmodes = EnumProperty(
        name = "Choose Mode",
        items = sim_vm,
        description = "Selection Modes",
        update = updateNode
    )
    
    sim_emodes = EnumProperty(
        name = "Choose Mode",
        items = sim_em,
        description = "Selection Modes",
        update = updateNode
    )
    
    sim_fmodes = EnumProperty(
        name = "Choose Mode",
        items = sim_fm,
        description = "Selection Modes",
        update = updateNode
    )
    
    borders_real = BoolProperty(
        default = False,
        update = updateNode
    
    )
    
    face_step = BoolProperty(
        default = False,
        update = updateNode
    
    )
    
    cav_strict = BoolProperty(
        default = False,
        update = updateNode
    )
    
    cav_borders = BoolProperty(
        default = False,
        update = updateNode
    )
    
    cav_mode = EnumProperty(
        name = "Choose Mode",
        items = cav_m,
        description = "Cavity Modes",
        update = updateNode
    )
    
    
    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
    
    #disconnect all inputs except Mesh and Selection
    
        #hide all inputs
        for input in self.inputs:
            if input.name != "Mesh" and input.name != "Selection":
                input.enabled = False
                
        if self.mode_list in ["Less", "More"]:
            self.inputs[2].enabled = True
        elif self.mode_list == "Similar":
            self.inputs[2].enabled = True
    
    

                    
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_MESH", "Mesh")
        self.inputs.new("socket_SELECTION", "Selection")
        socket = self.inputs.new("socket_INT", "Iterations")
        socket.enabled = False
        self.outputs.new("socket_SELECTION", "Selection")
        
        self.use_custom_color = True
        self.color = (.7,.9,1)

    ##\brief GUI.    
    def draw_buttons(self, context, layout):
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "mode_list", "")
        
        #different layouts depending on the selected mode:
        if self.mode_list == "Similar":
            row2 = layout.row()
            row2.prop(self, "sim_modes", "")
            row3 = layout.row()
            if self.sim_modes == "Vertices":
                row3.prop(self, "sim_vmodes", "")
            elif self.sim_modes == "Edges":
                row3.prop(self, "sim_emodes", "")
            elif self.sim_modes == "Faces":
                row3.prop(self, "sim_fmodes", "")

        elif self.mode_list == "Borders":
            row2 = layout.row()
            row2.prop(self, "borders_real","Mesh Borders")
            
        elif self.mode_list in ["Less","More"]:
            rowC = layout.row()
            rowC.prop(self,"face_step","Face Step")
            
        elif self.mode_list == "Cavity":
            rowC = layout.row()
            rowC.prop(self,"cav_mode","")
            rowC = layout.row()
            rowC.prop(self,"cav_strict","Strict")
            rowC = layout.row()
            rowC.prop(self,"cav_borders","Borders")
           
        layout.separator()
                

    ##\brief Re-calculates the node's data.    
    def recalculate(self):
        self.corrupted = False
        retsels = []
        
        
        obs = self.inputs[0].returnData()
        selections = self.inputs[1].returnData()
        
        
        
        if self.mode_list == "Linked":
            
            lists = utils_GEN.adjustLists([obs,selections])
            
            obs = lists[0]
            selections = lists[1]
            
            for i in range(0,len(obs)):
            
                selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                utils_OBJ.prep(obs[i],selection,"VERT")
                selection = utils_SEL.sel_linked(obs[i])
                utils_OBJ.deprep(obs[i])
                
                retsels.append(selection)

            
        elif self.mode_list == "Less":
        
        
            iterations = self.inputs[2].returnData()
        
            lists = utils_GEN.adjustLists([obs,selections,iterations])
            
            obs = lists[0]
            selections = lists[1]
            iterations = lists[2]
            
            
            for i in range(0,len(obs)):
            
                selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                utils_OBJ.prep(obs[i],selection,"VERT")
                selection = utils_SEL.sel_less(obs[i],iterations[i],self.face_step)
                utils_OBJ.deprep(obs[i])
                
                retsels.append(selection)
                
                
        elif self.mode_list == "More":
        
        
            iterations = self.inputs[2].returnData()
        
            lists = utils_GEN.adjustLists([obs,selections,iterations])
            
            obs = lists[0]
            selections = lists[1]
            iterations = lists[2]
            
            
            for i in range(0,len(obs)):
            
                selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                utils_OBJ.prep(obs[i],selection,"VERT")
                selection = utils_SEL.sel_more(obs[i],iterations[i],self.face_step)
                utils_OBJ.deprep(obs[i])
                
                retsels.append(selection)
                
                
        elif self.mode_list == "Loops":
        
            iterations = self.inputs[2].returnData()
        
            lists = utils_GEN.adjustLists([obs,selections,iterations])
            
            obs = lists[0]
            selections = lists[1]
            iterations = lists[2]
            
            
            for i in range(0,len(obs)):
            
                selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)

                
                utils_OBJ.prep(obs[i],selection,"EDGE")
                selection = utils_SEL.sel_loop(obs[i])
                utils_OBJ.deprep(obs[i])
                
                retsels.append(selection)
        
        
        elif self.mode_list == "Rings":
        
            iterations = self.inputs[2].returnData()
        
            lists = utils_GEN.adjustLists([obs,selections,iterations])
            
            obs = lists[0]
            selections = lists[1]
            iterations = lists[2]
            
            
            for i in range(0,len(obs)):
            
                selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                utils_OBJ.prep(obs[i],selection,"EDGE")
                selection = utils_SEL.sel_ring(obs[i])
                utils_OBJ.deprep(obs[i])
                
                retsels.append(selection)
                
                
        elif self.mode_list == "Borders":
        
            iterations = self.inputs[2].returnData()
        
            lists = utils_GEN.adjustLists([obs,selections,iterations])
            
            obs = lists[0]
            selections = lists[1]
            iterations = lists[2]
            
            
            for i in range(0,len(obs)):
            
                selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                utils_OBJ.prep(obs[i],selection,"EDGE")
                selection = utils_SEL.sel_border(obs[i])
                utils_OBJ.deprep(obs[i])
                
                retsels.append(selection)
                
                
        elif self.mode_list == "Skeleton":
        
            iterations = self.inputs[2].returnData()
        
            lists = utils_GEN.adjustLists([obs,selections,iterations])
            
            obs = lists[0]
            selections = lists[1]
            iterations = lists[2]
            
            
            for i in range(0,len(obs)):
            
                selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                utils_OBJ.prep(obs[i],selection,"FACE")
                selection = utils_SEL.sel_skeleton(obs[i])
                utils_OBJ.deprep(obs[i])
                
                retsels.append(selection)
                
                
        elif self.mode_list == "Similar":
        
            if self.sim_modes == "Vertices":
                
                lists = utils_GEN.adjustLists([obs,selections])
            
                obs = lists[0]
                selections = lists[1]
                
                for i in range(0,len(obs)):
                
                    selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    
                    utils_OBJ.prep(obs[i],selection,"VERT")
                    selection = utils_SEL.sel_similar_v(obs[i],self.sim_vmodes)
                    utils_OBJ.deprep(obs[i])
                    
                    retsels.append(selection)
                    
                    
                    
            elif self.sim_modes == "Edges":
                
                lists = utils_GEN.adjustLists([obs,selections])
            
                obs = lists[0]
                selections = lists[1]
                
                for i in range(0,len(obs)):
                
                    selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    
                    utils_OBJ.prep(obs[i],selection,"EDGE")
                    selection = utils_SEL.sel_similar_e(obs[i],self.sim_emodes)
                    utils_OBJ.deprep(obs[i])
                    
                    retsels.append(selection)
                    
                    
                    
            elif self.sim_modes == "Faces":
                
                lists = utils_GEN.adjustLists([obs,selections])
            
                obs = lists[0]
                selections = lists[1]
                
                for i in range(0,len(obs)):
                
                    selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    
                    utils_OBJ.prep(obs[i],selection,"FACE")
                    selection = utils_SEL.sel_similar_f(obs[i],self.sim_fmodes)
                    utils_OBJ.deprep(obs[i])
                    
                    retsels.append(selection)
                    
                    
        elif self.mode_list == "Cavity":
        
            lists = utils_GEN.adjustLists([obs,selections])
            
            obs = lists[0]
            selections = lists[1]
            
            
            for i in range(0,len(obs)):
            
                selection = utils_SEL.mapSelection(selections[i], obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                utils_OBJ.prep(obs[i],selection,"EDGE")
                selection = utils_SEL.sel_cavity(obs[i],self.cav_mode,self.cav_strict,self.cav_borders)
                utils_OBJ.deprep(obs[i])
                
                retsels.append(selection)
                    
                    
        
        
            
                
                
            
        
        
        
        
        
        
        
        if self.outputs[0].enabled:
            self.outputs[0].setData(retsels)


        
        
##\brief Create selections based on a mesh.        
class SEL_DataSelectionNode(buildingNode):

    bl_idname = 'SEL_DataSelectionNode'

    bl_label = 'Select'

    bl_icon = 'NODETREE'
    
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
        

    

	#NODE DATA
    
    mode_list_l = StringProperty(default = "",update = updateEmpty)
    mode_axes_l = StringProperty(default = "",update = updateEmpty)
    mode_randoms_l = StringProperty(default = "",update = updateEmpty)
    mode_position_l = StringProperty(default = "",update = updateEmpty)
    mode_axes_strict_l = StringProperty(default = "",update = updateEmpty)
    mode_axes_signed_l = StringProperty(default = "",update = updateEmpty)
    mode_size_l = StringProperty(default = "",update = updateEmpty)
    mode_signs_l = BoolProperty(default = False,update = updateEmpty)
    mode_vgroups_l = StringProperty(default = "",update = updateEmpty)
    mode_extrema_l = StringProperty(default = "",update = updateEmpty)
    extrema_edges_l = BoolProperty(default = False,update = updateEmpty)
    extrema_extend_l = BoolProperty(default = False,update = updateEmpty)
    
    
    
    
    
    corrupted = BoolProperty(default = True, update = updateEmpty) 
    freeze = BoolProperty(default = False, update = updateEmpty)
    
    ##\brief Randomizes the output if not freezed.
    def randomize(self):
        if not self.freeze:
            self.callObsolete("")
    
    ##\Freezes the node. Recalculations won't have any effect on the random values.
    def freezeRandom(self):
        self.freeze = True
    
    ##\Unfreezes the node. Recalculations will effect the random values.
    def unfreezeRandom(self):
        self.freeze = False
    
    
    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
        
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
        
        
        #CHECK ALL PARAMETERS
        if self.mode_list_l != self.mode_list:
            self.mode_list_l = self.mode_list
            outdated = True
            
        if self.mode_axes_l != self.mode_axes:
            self.mode_axes_l = self.mode_axes
            outdated = True
            
        if self.mode_randoms_l != self.mode_randoms:
            self.mode_randoms_l = self.mode_randoms
            outdated = True
            
        if self.mode_position_l != self.mode_position:
            self.mode_position_l = self.mode_position
            outdated = True
            
        if self.mode_axes_strict_l != self.mode_axes_strict:
            self.mode_axes_strict_l = self.mode_axes_strict
            outdated = True
            
        if self.mode_axes_signed_l != self.mode_axes_signed:
            self.mode_axes_signed_l = self.mode_axes_signed
            outdated = True
            
        if self.mode_size_l != self.mode_size:
            self.mode_size_l = self.mode_size
            outdated = True
            
        if self.mode_signs_l != self.mode_signs:
            self.mode_signs_l = self.mode_signs
            outdated = True
        
        if self.mode_vgroups_l != self.mode_vgroups:
            self.mode_vgroups_l = self.mode_vgroups
            outdated = True
            
        if self.mode_extrema_l != self.mode_extrema:
            self.mode_extrema_l = self.mode_extrema
            outdated = True
            
        if self.extrema_extend_l != self.extrema_extend:
            self.extrema_extend_l = self.extrema_extend
            outdated = True
            
        if self.extrema_edges_l != self.extrema_edges:
            self.extrema_edges_l = self.extrema_edges
            outdated = True
                
                
        if outdated:            
            self.updateInputs(context)
            self.callObsolete(context)
                
        
        

         
    
    modes = [("All","All",""),("Normal","Normal",""),("Random","Random",""),("Position","Position",""),("Extrema/Directions","Extrema/Directions",""),("Distance","Distance",""),("Size","Size",""),("Vertex Group","Vertex Group","")]
    axes = [("All","All",""),("X","X",""),("Y","Y",""),("Z","Z","")]
    axes_strict = [("X","X",""),("Y","Y",""),("Z","Z","")]
    axes_signed = [("All","All",""),("X","X",""),("Y","Y",""),("Z","Z",""),("-X","-X",""),("-Y","-Y",""),("-Z","-Z","")]
    randoms = [("Percentage","Percentage",""),("Amount","Amount","")]
    pos_modes = [("Greater","Greater",""),("Less","Less",""),("Equals","Equals","")]
    sizemodes = [("Face Surface","Face Surface",""),("Edge Length","Edge Length","")]
    ex_m = [("Highest X","Highest X",""),("Lowest X","Lowest X",""),("Highest Y","Highest Y",""),("Lowest Y","Lowest Y",""),("Highest Z","Highest Z",""),("Lowest Z","Lowest Z","")]

    
    mode_list = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Selection Modes",
        update = updateNode
    )
    
    mode_axes = EnumProperty(
        name = "Choose Axis",
        items = axes,
        description = "Axis Modes",
        update = updateNode
    )
    
    mode_randoms = EnumProperty(
        name = "Choose Mode",
        items = randoms,
        description = "Random Modes",
        update = updateNode
    )
    
    mode_position = EnumProperty(
        name = "Choose Mode",
        items = pos_modes,
        description = "Position Modes",
        update = updateNode
    )
    
    mode_axes_strict = EnumProperty(
        name = "Choose Axis",
        items = axes_strict,
        description = "Axis Modes",
        update = updateNode
    )
    
    mode_axes_signed = EnumProperty(
        name = "Choose Axis",
        items = axes_signed,
        description = "Axis Modes, Signed",
        update = updateNode
    )
    
    mode_size = EnumProperty(
        name = "Choose Mode",
        items = sizemodes,
        description = "Size Modes",
        update = updateNode
    )
    
    mode_signs = BoolProperty(
        name = "Signed",
        default = False,
        description = "Sign Modes",
        update = updateNode
    )
    
    mode_vgroups = StringProperty(
        name = "Choose Vertex Group",
        default = "",
        description = "Vertex Groups",
        update = updateNode
    )
    
    mode_extrema = EnumProperty(
        name = "Choose Mode",
        items = ex_m,
        description = "Extrema Modes",
        update = updateNode
    )
    
    extrema_edges = BoolProperty(
        name = "Along Edges",
        default = False,
        description = "Alternative edge mode, takes edge as vector instead of edge normal",
        update = updateNode
    )
    
    extrema_extend = BoolProperty(
        name = "Extend",
        default = False,
        description = "Extend the selection to previously unselected geometry",
        update = updateNode
    )
    
    
    
    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
    
        if len(self.inputs) == 7 and len(self.outputs) == 1:
    
            #enabled selection input again
            self.inputs[1].enabled = True
    
            #disconnect all inputs except Mesh
    
            #hide all inputs
            for input in self.inputs:
                if input.name != "Mesh" and input.name != "Selection":
                    input.enabled = False

                #hide selection again for "All" mode
                if self.mode_list == "All":
                    self.inputs[1].enabled = False
            
                #add new inputs, based on the selected mode
                if self.mode_list == "Normal":
                    self.inputs[2].enabled = True
                    self.inputs[3].enabled = True
                
                elif self.mode_list == "Random":
                    self.inputs[4].enabled = True
                
                elif self.mode_list == "Position":
                    self.inputs[4].enabled = True
                
                elif self.mode_list == "Distance":
                    self.inputs[5].enabled = True
                    self.inputs[6].enabled = True
                
                elif self.mode_list == "Size":
                    self.inputs[4].enabled = True
                    
                elif self.mode_list == "Vertex Group":
                    self.inputs[1].enabled = False
                    
                elif self.mode_list == "Extrema/Directions":
                    if self.mode_extrema == "Pointing to Vector":
                        self.inputs[2].enabled = True

            
            
        
        
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_MESH", "Mesh")
        socket = self.inputs.new("socket_SELECTION", "Selection")
        socket.enabled = False
        socket = self.outputs.new("socket_SELECTION", "Selection")
        
        
        socket = self.inputs.new("socket_VEC3_F", "Direction")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT", "Degrees")
        socket.enabled = False
        
        socket = self.inputs.new("socket_FLOAT", "Value")
        socket.enabled = False
        
        socket = self.inputs.new("socket_FLOAT", "Distance")
        socket.enabled = False
        socket = self.inputs.new("socket_VEC3_F", "Pivot")
        socket.enabled = False
        
        self.use_custom_color = True
        self.color = (.7,.9,1)
        

        
        self.update()

     
    ##\brief GUI.
    def draw_buttons(self, context, layout):
    
        layout.context_pointer_set("CALLER", self)
    
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "mode_list", "")
        
        #different layouts depending on the selected mode:
        if self.mode_list == "All":
            rowL = layout.row(align = True)
            rowL.label(text = "Select everything")
        elif self.mode_list == "Normal":
            layout.separator()
            rowM = layout.row(align= True)
            rowM.prop(self, "mode_position","")
            rowB = layout.row()
            rowB.prop(self,"extrema_edges","Along Edges")
              
        elif self.mode_list == "Random":
            layout.separator()
            rowL = layout.row(align = True)
            rowL.prop(self, "mode_randoms", "")
            layout.separator()
            if self.freeze:
                layout.operator("nodetree.unfreeze", text="Unfreeze", emboss=True)
            else:
                layout.operator("nodetree.freeze", text="Freeze", emboss=True)
            layout.operator("nodetree.randomize", text="Randomize", emboss=True)
            
        elif self.mode_list == "Position":
            layout.separator()
            rowM = layout.row(align = True)
            rowM.prop(self, "mode_position","")
            rowA = layout.row(align = True)
            colA1 = rowA.column(align = True)
            colA2 = rowA.column(align = True)
            colA1.label(text = "Axis:")
            colA2.prop(self, "mode_axes_strict","")
            
            
        elif self.mode_list == "Extrema/Directions":
            layout.separator()
            rowM = layout.row(align = True)
            rowM.prop(self, "mode_extrema","")
            if "Pointing to " in self.mode_extrema:
                row2 = layout.row()
                row2.prop(self, "extrema_extra", "")
                row3 = layout.row()
                row3.prop(self, "extrema_edges", "Along Edges")
            else:
                row4 = layout.row()
                row4.prop(self, "extrema_extend", "Extend")
            
            
        elif self.mode_list == "Distance":
            layout.separator()
            rowM = layout.row(align = True)
            rowM.prop(self, "mode_position","")
            rowA = layout.row(align = True)
            colA1 = rowA.column(align = True)
            colA2 = rowA.column(align = True)
            colA1.label(text = "Axis:")
            colA2.prop(self, "mode_axes","")
            
            
        elif self.mode_list == "Size":
            layout.separator()
            rowM = layout.row(align = True)
            rowM.prop(self, "mode_size", "")
            rowP = layout.row(align = True)
            rowP.prop(self, "mode_position", "")
            
            
        elif self.mode_list == "Vertex Group":
            layout.separator()
            rowM = layout.row(align = True)
            rowM.prop(self, "mode_vgroups", "")
            
            
            

        
        layout.separator()
    
    
        
    ##\brief Re-calculates the node's data.     
    def recalculate(self):
        self.corrupted = False
        retsels = []
        
        if len(self.inputs[0].links) != 0:
            
            source_OBJs = self.inputs[0].returnData()
        
            #Selections
            selections = self.inputs[1].returnData()
                    
            
        
        
            if self.mode_list == "All":
                
                for i in range(0,len(source_OBJs)):
                
                    selection = utils_SEL.mapSelection(selections[i], source_OBJs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)

                    retsels.append(selection)
                    
                    
                
            elif self.mode_list == "Normal":
                        
                #get additional data
                vectors = self.inputs[2].returnData()
                angles = self.inputs[3].returnData()

                lists = utils_GEN.adjustLists2([source_OBJs,selections,vectors,angles])
                    
                source_OBJs = lists[0]
                selections = lists[1]
                vectors = lists[2]
                angles = lists[3]
                    
                    
                if self.mode_axes != "All":
                    if self.mode_axes_signed in ["X", "-X"]:
                        for vector in vectors:
                            vector[0] = 0
                    elif self.mode_axes_signed in ["Y", "-Y"]:
                        for vector in vectors:
                            vector[1] = 0
                    elif self.mode_axes_signed in ["Z", "-Z"]:
                        for vector in vectors:
                            vector[2] = 0

                                
                for i in range(0, len(source_OBJs)):
                                
                    selection = utils_SEL.mapSelection(selections[i], source_OBJs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    
                    #init lists
                    sel_v = []
                    sel_e = []
                    sel_f = []
                    
                    #test vertices

                    for x in selection[0]:
                        vert = source_OBJs[i].data.vertices[x]
                        vector_v = vert.normal

                        v_angle = utils_MATH.getAngle(vectors[i], vector_v)

                        if self.mode_position == "Greater":
                            if v_angle - angles[i] > .001:
                                sel_v.append(vert.index)
                        elif self.mode_position == "Less":
                            if angles[i] - v_angle > .001:
                                sel_v.append(vert.index)
                        elif self.mode_position == "Equals":
                            if math.fabs(v_angle - angles[i]) < .001:
                                sel_v.append(vert.index)
                                
                    #test edges

                    for x in selection[1]:
                        
                        if not self.extrema_edges:
                            vector_e = utils_GEOM.getEdgeNormal(source_OBJs[i], x)
                        else:
                            vector_e = utils_GEOM.getEdgeNormal_along(source_OBJs[i], x)
                            if vector_e.dot(vectors[i]) < 0:
                                vector_e = -vector_e
 
                        e_angle = utils_MATH.getAngle(vectors[i], vector_e)

                        if self.mode_position == "Greater":
                            if e_angle - angles[i] > .001:
                                sel_e.append(x)
                        elif self.mode_position == "Less":
                            if angles[i] - e_angle > .001:
                                sel_e.append(x)
                        elif self.mode_position == "Equals":
                            if math.fabs(e_angle - angles[i]) < .001:
                                sel_e.append(x)
                    
                    
                    
                    
                    #test faces

                    for x in selection[2]:
                        face = source_OBJs[i].data.polygons[x]
                        vector_f = face.normal
                    
                        f_angle = 0
                        f_angle = utils_MATH.getAngle(vectors[i], vector_f)
                    
                            
                    
                        if self.mode_position == "Greater":
                            if f_angle - angles[i] > .001:
                                sel_f.append(face.index)
                        elif self.mode_position == "Less":
                            if angles[i] - f_angle > .001:
                                sel_f.append(face.index)
                        elif self.mode_position == "Equals":
                            if math.fabs(f_angle - angles[i]) < .001:
                                sel_f.append(face.index)
                    
                    
                    
                    
                    
                    #return selection
                    selection = [sel_v, sel_e, sel_f]
                    retsels.append(selection)
                        
                        
                
                        
                        
                        
                
            elif self.mode_list == "Random":
                if self.mode_randoms == "Percentage":

                    percentages = self.inputs[4].returnData()
                    
                    lists = utils_GEN.adjustLists([source_OBJs,selections,percentages])
                    
                    source_OBJs = lists[0]
                    selections = lists[1]
                    percentages = lists[2]
                    
                    for i in range (0, len(source_OBJs)):
                    
                        amount_v = 0
                        amount_e = 0
                        amount_f = 0
                        
                        selection = utils_SEL.mapSelection(selections[i], source_OBJs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    
                    
                
                        vcount = len(source_OBJs[i].data.vertices)
                        amount_v = int(math.floor(percentages[i] * vcount))
                        if amount_v > vcount:
                            amount_v = vcount
                        

                        ecount = len(source_OBJs[i].data.edges)
                        amount_e = int(math.floor(percentages[i] * ecount))
                        if amount_e > ecount:
                            amount_e = ecount
                    

                        fcount = len(source_OBJs[i].data.polygons)
                        amount_f = int(math.floor(percentages[i] * fcount))
                        if amount_f > fcount:
                            amount_f = fcount
                    

                        
                        #new selection lists
                        sel_v = []
                        sel_e = []
                        sel_f = []  
                    
                        #fill vertices
                        for x in range(0,amount_v):
                            grab = randrange(0,len(selection[0]),1)
                            sel_v.append(selection[0][grab])
                            selection[0].pop(grab)
                                
                        #fill edges

                        for x in range(0,amount_e):
                            grab = randrange(0,len(selection[1]),1)
                            sel_e.append(selection[1][grab])
                            selection[1].pop(grab)
                                
                        #fill faces

                        for x in range(0,amount_f):
                            grab = randrange(0,len(selection[2]),1)
                            sel_f.append(selection[2][grab])
                            selection[2].pop(grab)
                            
                        
                    
                        selection = [sel_v, sel_e, sel_f]
                        retsels.append(selection)
                        
                        
                        
                        
                        
                        
            
                elif self.mode_randoms == "Amount":
                    if len(self.inputs[4].links) != 0:
                    
                        amounts = self.inputs[4].returnData()
                        
                        lists = utils_GEN.adjustLists([source_OBJs,selections,amounts])
                        
                        source_OBJs = lists[0]
                        selections = lists[1]
                        amounts = lists[2]
                        
                        for i in range(0, len(source_OBJs)):
                            
                            selection = utils_SEL.mapSelection(selections[i], source_OBJs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)

                            vcount = len(source_OBJs[i].data.vertices)
                            amount_v = int(math.floor(amounts[i]))
                            if amount_v > vcount:
                                amount_v = vcount
                            

                            ecount = len(source_OBJs[i].data.edges)
                            amount_e = int(math.floor(amounts[i]))
                            if amount_e > ecount:
                                amount_e = ecount
                        

                            fcount = len(source_OBJs[i].data.polygons)
                            amount_f = int(math.floor(amounts[i]))
                            if amount_f > fcount:
                                amount_f = fcount

                            
                            #new selection lists
                            sel_v = []
                            sel_e = []
                            sel_f = []  
                        
                            #fill vertices
                            for x in range(0,amount_v):
                                grab = randrange(0,len(selection[0]),1)
                                sel_v.append(selection[0][grab])
                                selection[0].pop(grab)
                                    
                            #fill edges
                            for x in range(0,amount_e):
                                grab = randrange(0,len(selection[1]),1)
                                sel_e.append(selection[1][grab])
                                selection[1].pop(grab)
                                    
                            #fill faces
                            for x in range(0,amount_f):
                                grab = randrange(0,len(selection[2]),1)
                                sel_f.append(selection[2][grab])
                                selection[2].pop(grab)
                        
                            selection = [sel_v, sel_e, sel_f]
                            retsels.append(selection)
                            
                
            elif self.mode_list == "Position":

                    
                #get values
                values = self.inputs[4].returnData()
                
                
                lists = utils_GEN.adjustLists([source_OBJs,values])
                    
                source_OBJs = lists[0]
                values = lists[1]
                
                
                for i in range(0, len(source_OBJs)):
                
                    selection = utils_SEL.mapSelection(selections[i], source_OBJs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                
                
                    #init lists
                    sel_v = []
                    sel_e = []
                    sel_f = []
                
                    #test vertices
                    for vert in selection[0]:
                        val = 0
                        if self.mode_axes_strict == "X":
                            val = vert.co[0]
                        elif self.mode_axes_strict == "Y":
                            val = vert.co[1]
                        else:
                            val = vert.co[2]
                        if self.mode_position == "Greater":
                            if val - values[i] > 0.001:
                                sel_v.append(vert.index)
                        elif self.mode_position == "Less":
                            if values[i] - val > 0.001:
                                sel_v.append(vert.index)
                        elif self.mode_position == "Equals":
                            if math.fabs(val - values[i]) < 0.001:
                                sel_v.append(vert.index)
                            
                
                    #test edges
                    for edge in selection[1]:
                        val = 0
                        edges_coords = []
                        for v_ind in edge.vertices:
                            edges_coords.append(source_OBJs[i].data.vertices[v_ind].co)
                        coords = utils_MATH.getMidCoords(edges_coords)            
                                
                        if self.mode_axes_strict == "X":
                            val = coords[0]
                        elif self.mode_axes_strict == "Y":
                            val = coords[1]
                        else:
                            val = coords[2]
                        if self.mode_position == "Greater":
                            if val - values[i] > 0.001:
                                sel_e.append(edge.index)
                        elif self.mode_position == "Less":
                            if values[i] - val > 0.001:
                                sel_e.append(edge.index)
                        elif self.mode_position == "Equals":
                            if math.fabs(val - values[i]) < 0.001:
                                sel_e.append(edge.index)
                
                    #test faces
                    for face in selection[2]:
                        val = 0
                        coords = face.center
                        if self.mode_axes_strict == "X":
                            val = coords[0]
                        elif self.mode_axes_strict == "Y":
                            val = coords[1]
                        else:
                            val = coords[2]
                        if self.mode_position == "Greater":
                            if val - values[i] > 0.001:
                                sel_f.append(face.index)
                        elif self.mode_position == "Less":
                            if values[i] - val > 0.001:
                                sel_f.append(face.index)
                        elif self.mode_position == "Equals":
                            if math.fabs(val - values[i]) < 0.001:
                                sel_f.append(face.index)
                
                
                
                    #return selection
                    selection = [sel_v, sel_e, sel_f]
                    retsels.append(selection)
                    
                    
                    
                    
                    
               
            elif self.mode_list == "Distance":
                
                #get pivots
                pivots = self.inputs[6].returnData()
                
            
                #get distances  
                distances = self.inputs[5].returnData()
                
                
                lists = utils_GEN.adjustLists([source_OBJs,pivots,distances])
                    
                source_OBJs = lists[0]
                pivots = lists[1]
                distances = lists[2]
                
                
                for i in range(0, len(source_OBJs)):

                    selection = utils_SEL.mapSelection(selections[i], source_OBJs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                    #new selection lists
                    sel_v = []
                    sel_e = []
                    sel_f = []
                
                    #modes
                    if self.mode_axes == "All":
                
                        # Greater/Less/Equals?
                        if self.mode_position == "Greater":
                            #vertices
                            for vID in selection[0]:
                            
                                v = source_OBJs[i].data.vertices[vID]
                                
                                coords = v.co
                                if utils_MATH.distanceEuler(coords,pivots[i]) - distances[i] > .0001:
                                    sel_v.append(v.index)
                       
                            #edges
                            for eID in selection[1]:
                            
                                e = source_OBJs[i].data.edges[eID]
                            
                                edges_coords = []
                                for v_ind in e.vertices:
                                    edges_coords.append(source_OBJs[i].data.vertices[v_ind].co)
                                coords = utils_MATH.getMidCoords(edges_coords)
                                if utils_MATH.distanceEuler(coords,pivots[i]) - distances[i] > .0001:
                                    sel_e.append(e.index)
                        
                            #faces
                            for fID in selection[2]:
                            
                                f = source_OBJs[i].data.polygons[fID]
                            
                                center = f.center
                                if utils_MATH.distanceEuler(center,pivots[i]) - distances[i] > .0001:
                                    sel_f.append(f.index)
                                
                        elif self.mode_position == "Less":
                            #vertices
                            for vID in selection[0]:
                            
                                v = source_OBJs[i].data.vertices[vID]
                                coords = v.co
                                if distances[i] - utils_MATH.distanceEuler(coords,pivots[i]) > .0001:
                                    sel_v.append(v.index)
                       
                            #edges
                            for eID in selection[1]:
                            
                                e = source_OBJs[i].data.edges[eID]
                                edges_coords = []
                                for v_ind in e.vertices:
                                    edges_coords.append(source_OBJs[i].data.vertices[v_ind].co)
                                coords = utils_MATH.getMidCoords(edges_coords)
                                if distances[i] - utils_MATH.distanceEuler(coords,pivots[i]) > .0001:
                                    sel_e.append(e.index)
                        
                            #faces
                            for fID in selection[2]:
                            
                                f = source_OBJs[i].data.polygons[fID]
                                center = f.center
                                if distances[i] - utils_MATH.distanceEuler(center,pivots[i]) > .0001:
                                    sel_f.append(f.index)
                                
                        elif self.mode_position == "Equals":
                            #vertices
                            for vID in selection[0]:
                            
                                v = source_OBJs[i].data.vertices[vID]
                                coords = v.co
                                if math.fabs(distances[i] - utils_MATH.distanceEuler(coords,pivots[i])) < .0001:
                                    sel_v.append(v.index)
                       
                            #edges
                            for eID in selection[1]:
                            
                                e = source_OBJs[i].data.edges[eID]
                                edges_coords = []
                                for v_ind in e.vertices:
                                    edges_coords.append(source_OBJs[i].data.vertices[v_ind].co)
                                coords = utils_MATH.getMidCoords(edges_coords)
                                if math.fabs(distances[i] - utils_MATH.distanceEuler(coords,pivots[i])) < .0001:
                                    sel_e.append(e.index)
                        
                            #faces
                            for fID in selection[2]:
                            
                                f = source_OBJs[i].data.polygons[fID]
                                center = f.center
                                if math.fabs(distances[i] - utils_MATH.distanceEuler(center,pivots[i])) < .0001:
                                    sel_f.append(f.index)
                                

                        
                                
                    else:
                        axis = self.mode_axes
                    
                        if self.mode_position == "Greater":
                            #vertices
                            for vID in selection[0]:
                            
                                v = source_OBJs[i].data.vertices[vID]
                                coords = v.co
                                if utils_MATH.distanceAxis(coords,pivots[i],axis) - distances[i] > .0001:
                                    sel_v.append(v.index)
                       
                            #edges
                            for eID in selection[1]:
                            
                                e = source_OBJs[i].data.edges[eID]
                                edges_coords = []
                                for v_ind in e.vertices:
                                    edges_coords.append(source_OBJs[i].data.vertices[v_ind].co)
                                coords = utils_MATH.getMidCoords(edges_coords)
                                if utils_MATH.distanceAxis(coords,pivots[i],axis) - distances[i] > .0001:
                                    sel_e.append(e.index)
                        
                            #faces
                            for fID in selection[2]:
                            
                                f = source_OBJs[i].data.polygons[fID]
                                center = f.center
                                if utils_MATH.distanceAxis(center,pivots[i],axis) - distances[i] > .0001:
                                    sel_f.append(f.index)
                                
                        elif self.mode_position == "Less":
                            #vertices
                            for vID in selection[0]:
                            
                                v = source_OBJs[i].data.vertices[vID]
                                coords = v.co
                                if distances[i] - utils_MATH.distanceAxis(coords,pivots[i],axis) > .0001:
                                    sel_v.append(v.index)
                       
                            #edges
                            for eID in selection[1]:
                            
                                e = source_OBJs[i].data.edges[eID]
                                edges_coords = []
                                for v_ind in e.vertices:
                                    edges_coords.append(source_OBJs[i].data.vertices[v_ind].co)
                                coords = utils_MATH.getMidCoords(edges_coords)
                                if distances[i] - utils_MATH.distanceAxis(coords,pivots[i],axis) > .0001:
                                    sel_e.append(e.index)
                        
                            #faces
                            for fID in selection[2]:
                            
                                f = source_OBJs[i].data.polygons[fID]
                                center = f.center
                                if distances[i] - utils_MATH.distanceAxis(center,pivots[i],axis) > .0001:
                                    sel_f.append(f.index)
                                
                        elif self.mode_position == "Equals":
                            #vertices
                            for vID in selection[0]:
                            
                                v = source_OBJs[i].data.vertices[vID]
                                coords = v.co
                                if math.fabs(distances[i] - utils_MATH.distanceAxis(coords,pivots[i],axis)) < .0001:
                                    sel_v.append(v.index)
                        
                            #edges
                            for eID in selection[1]:
                            
                                e = source_OBJs[i].data.edges[eID]
                                edges_coords = []
                                for v_ind in e.vertices:
                                    edges_coords.append(source_OBJs[i].data.vertices[v_ind].co)
                                coords = utils_MATH.getMidCoords(edges_coords)
                                if math.fabs(distances[i] - utils_MATH.distanceAxis(coords,pivots[i],axis)) < .0001:
                                    sel_e.append(e.index)
                        
                            #faces
                            for fID in selection[2]:
                            
                                f = source_OBJs[i].data.polygons[fID]
                                center = f.center
                                if math.fabs(distances[i] - utils_MATH.distanceAxis(center,pivots[i],axis)) < .0001:
                                    sel_f.append(f.index)
                    
                    
                                
                                
                    selection = [sel_v, sel_e, sel_f]
                    retsels.append(selection)
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                
            elif self.mode_list == "Size":
               
                    
                
                #get sizes
                sizes = self.inputs[4].returnData()
                
                
                lists = utils_GEN.adjustLists([source_OBJs,sizes])
                    
                source_OBJs = lists[0]
                sizes = lists[1]
                
                for i in range(0, len(source_OBJs)):
                
                    selection = utils_SEL.mapSelection(selections[i], source_OBJs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                
                    #new selection lists
                
                    sel_e = []
                    sel_f = []
                
                    if self.mode_size == "Face Surface":
                        if self.mode_position == "Greater":
                            for fID in selection[2]:
                            
                                f = source_OBJs[i].data.polygons[fID]
                                if (f.area - sizes[i]) > 0.0001:
                                    sel_f.append(f.index)
                        elif self.mode_position == "Less":
                            for fID in selection[2]:
                            
                                f = source_OBJs[i].data.polygons[fID]
                                if (sizes[i] - f.area) > 0.0001 :
                                    sel_f.append(f.index)
                        elif self.mode_position == "Equals":
                            for fID in selection[2]:
                            
                                f = source_OBJs[i].data.polygons[fID]
                                if math.fabs(f.area - sizes[i]) < 0.0001:
                                    sel_f.append(f.index)
                    
                        
                
                
                
                    elif self.mode_size == "Edge Length":
                        if self.mode_position == "Greater":
                            for eID in selection[1]:
                            
                                e = source_OBJs[i].data.edges[eID]
                                v1 = source_OBJs[i].data.vertices[e.vertices[0]].co
                                v2 = source_OBJs[i].data.vertices[e.vertices[1]].co
                            
                                length = utils_MATH.distanceEuler(v1,v2)
                            
                                if (length - sizes[i]) > 0.0001:
                                    sel_e.append(e.index)
                            
                            
                        elif self.mode_position == "Less":
                            for eID in selection[1]:
                            
                                e = source_OBJs[i].data.edges[eID]
                                v1 = source_OBJs[i].data.vertices[e.vertices[0]].co
                                v2 = source_OBJs[i].data.vertices[e.vertices[1]].co
                            
                                length = utils_MATH.distanceEuler(v1,v2)
                            
                                if (sizes[i] - length) > 0.0001:
                                    sel_e.append(e.index)
                            
                        elif self.mode_position == "Equals":
                            for eID in selection[1]:
                            
                                e = source_OBJs[i].data.edges[eID]
                                v1 = source_OBJs[i].data.vertices[e.vertices[0]].co
                                v2 = source_OBJs[i].data.vertices[e.vertices[1]].co
                            
                                length = utils_MATH.distanceEuler(v1,v2)
                            
                                if math.fabs(length - sizes[i]) < 0.0001:
                                    sel_e.append(e.index)
                    
                    
                    selection = [[], sel_e, sel_f]
                    retsels.append(selection)
                
                
                
                
            elif self.mode_list == "Vertex Group":

                vgroup_name = self.mode_vgroups
                vgroup_index = -1
                
                for i in range(0, len(source_OBJs)):
                
                    if source_OBJs[i].vertex_groups == None:
                        retsels.append([[],[],[]])
                    
                    else:
                        
                        found = False
                    
                        for group in source_OBJs[i].vertex_groups:
                            if group.name == vgroup_name:
                                found = True
                            
                        if not found:
                            retsels.append([[],[],[]])
                            
                        else:
                            
                            
                
                            for vg in source_OBJs[i].vertex_groups:
                                if vg.name == vgroup_name:
                                    vgroup_index = vg.index
                        
                
                            #create list1 of grouped vertices
                            sel_v = []
                            sel_e = []
                            sel_f = []
                            for vert in source_OBJs[i].data.vertices:
                                if vert.groups != None:
                                    for gr in vert.groups:
                                        if vgroup_index == gr.group:
                                            sel_v.append(vert.index)
                            
                            
                            #try and find edges and faces made up exclusively of grouped vertices, too
                            #edges:
                            for edge in source_OBJs[i].data.edges:
                                include = True
                                for v in edge.vertices:
                                    vert = source_OBJs[i].data.vertices[v]
                                    if vert.groups != None:
                                        found = False
                                        for gr in vert.groups:
                                            if vgroup_index == gr.group:
                                                found = True
                                        if not found:
                                            include = False
                                    else:
                                        include = False
                                if include:
                                    sel_e.append(edge.index)
                            
                    
                            for face in source_OBJs[i].data.polygons:
                                include = True
                                for v in face.vertices:
                                    vert = source_OBJs[i].data.vertices[v]
                                    if vert.groups != None:
                                        found = False
                                        for gr in vert.groups:
                                            if vgroup_index == gr.group:
                                                found = True
                                        if not found:
                                            include = False
                                    else:
                                        include = False
                                if include:
                                    sel_f.append(face.index)
                    
                            selection = [sel_v, sel_e, sel_f]
                            retsels.append(selection)

                    
                    
                    
            elif self.mode_list == "Extrema/Directions":
                
                lists = utils_GEN.adjustLists([source_OBJs,selections])
                
                selections = lists[1]
                source_OBJs = lists[0]
        
                axis = 0
        
                if self.mode_extrema in ["Highest Y", "Lowest Y"]:
                    axis = 1
                
                elif self.mode_extrema in ["Highest Z", "Lowest Z"]:
                    axis = 2
                
                mode = 0
            
                if "Lowest" in self.mode_extrema:
                    mode = 1
                    
                    
                for i in range(0,len(source_OBJs)):
                    
                    selection = utils_SEL.mapSelection(selections[i], source_OBJs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    
                    selection = utils_SEL.selectExtrema(source_OBJs[i], selection, axis, mode, self.extrema_extend)
                    
                    retsels.append(selection)
                    
                

            
            if self.outputs[0].enabled:
                self.outputs[0].setData(retsels)   
                        
                        
            for ob in source_OBJs:
                ob.name = "_$OBS$_"
                    



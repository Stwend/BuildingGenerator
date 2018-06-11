##\package buildingGen.nodes.building_nodes_MESH
# Mesh nodes.


import bpy
import bmesh
from bpy.types import NodeTree, Node, NodeSocket

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

from bpy.props import EnumProperty, StringProperty, BoolProperty, FloatProperty, FloatVectorProperty

import custom_sockets


from . import building_NODETREE
from .building_NODETREE import *

from utils import utils_GEN, utils_MATH, utils_OBJ, utils_GEOM, utils_SEL,utils_GLO
import mathutils
import math


##\brief Mesh filters and transforms.
#\detail Filters don't alter the object's vert, edge and face count, therefore selections won't be destroyed by applying filters.
class MESH_FilterNode(buildingNode):

    bl_idname = 'MESH_FilterNode'

    bl_label = 'Filter'

    bl_icon = 'NODETREE'

    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    
    


    
    #UPDATE

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self,context):

        
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True

        
        
        #CHECK ALL PARAMETERS
        if self.mode_list_l != self.mode_list:
            self.mode_list_l = self.mode_list
            outdated = True
        
        if self.rotate_axes_list_l != self.rotate_axes_list:
            self.rotate_axes_list_l = self.rotate_axes_list
            outdated = True
            
        if self.flatten_modes_l != self.flatten_modes:
            self.flatten_modes_l = self.flatten_modes
            outdated = True
            
        if self.flatten_axes_l != self.flatten_axes:
            self.flatten_axes_l = self.flatten_axes
            outdated = True
        
        if self.flatten_axes_s_l != self.flatten_axes_s:
            self.flatten_axes_s_l = self.flatten_axes_s
            outdated = True
            
        if self.scale_axes_l != self.scale_axes:
            self.scale_axes_l = self.scale_axes
            outdated = True
            
        if self.projection_modes_l != self.projection_modes:
            self.projection_modes_l = self.projection_modes
            outdated = True
            
        if self.projection_modes_n_l != self.projection_modes_n:
            self.projection_modes_n_l = self.projection_modes_n
            outdated = True
            
        if self.projection_modes_d_l != self.projection_modes_d:
            self.projection_modes_d_l = self.projection_modes_d
            outdated = True
            
        if self.projection_modes_close_l != self.projection_modes_close:
            self.projection_modes_close_l = self.projection_modes_close
            outdated = True
            
        if self.fatten_X_l != self.fatten_X:
            self.fatten_X_l = self.fatten_X
            outdated = True
            
        if self.fatten_Y_l != self.fatten_Y:
            self.fatten_Y_l = self.fatten_Y
            outdated = True
            
        if self.fatten_Z_l != self.fatten_Z:
            self.fatten_Z_l = self.fatten_Z
            outdated = True
        
        if self.normals_mode_l != self.normals_mode:
            self.normals_mode_l = self.normals_mode
            outdated = True
            
        if self.smooth_X_l != self.smooth_X:
            self.smooth_X_l = self.smooth_X
            outdated = True
            
        if self.smooth_Y_l != self.smooth_Y:
            self.smooth_Y_l = self.smooth_Y
            outdated = True
            
        if self.smooth_Z_l != self.smooth_Z:
            self.smooth_Z_l = self.smooth_Z
            outdated = True
        
        if self.bend_axis_l != self.bend_axis:
            self.bend_axis_l = self.bend_axis
            outdated = True
            
        if self.taper_axis_l != self.taper_axis:
            self.taper_axis_l = self.taper_axis
            outdated = True
            
        if self.twist_axis_l != self.twist_axis:
            self.twist_axis_l = self.twist_axis
            outdated = True
        
        if self.shear_dominant_l != self.shear_dominant:
            self.shear_dominant_l = self.shear_dominant
            outdated = True
        
        if self.shear_subdominant_l != self.shear_subdominant:
            self.shear_subdominant_l = self.shear_subdominant
            outdated = True
            
        if self.option_meshCenter_l != self.option_meshCenter:
            self.option_meshCenter_l = self.option_meshCenter
            outdated = True

            
        
        if outdated:            
            self.updateInputs(context)
            self.callObsolete(context)
    
    

    
    
	#NODE DATA
    corrupted = BoolProperty(default = True, update = updateEmpty)
    
    
    mode_list_l = StringProperty(default = "", update = updateEmpty)
    rotate_axes_list_l = StringProperty(default = "", update = updateEmpty)
    flatten_modes_l = StringProperty(default = "", update = updateEmpty)
    flatten_axes_l = StringProperty(default = "", update = updateEmpty)
    flatten_axes_s_l = StringProperty(default = "", update = updateEmpty)
    scale_axes_l = StringProperty(default = "", update = updateEmpty)
    projection_modes_l = StringProperty(default = "", update = updateEmpty)
    projection_modes_n_l = StringProperty(default = "", update = updateEmpty)
    projection_modes_d_l = StringProperty(default = "", update = updateEmpty)
    projection_modes_close_l = StringProperty(default = "", update = updateEmpty)
    #more projection stuff
    fatten_X_l = BoolProperty(default = True, update = updateEmpty)
    fatten_Y_l = BoolProperty(default = True, update = updateEmpty)
    fatten_Z_l = BoolProperty(default = True, update = updateEmpty)
    normals_mode_l = StringProperty(default = "", update = updateEmpty)
    smooth_X_l = BoolProperty(default = True, update = updateEmpty)
    smooth_Y_l = BoolProperty(default = True, update = updateEmpty)
    smooth_Z_l = BoolProperty(default = True, update = updateEmpty)
    bend_axis_l = StringProperty(default = "", update = updateEmpty)
    taper_axis_l = StringProperty(default = "", update = updateEmpty)
    twist_axis_l = StringProperty(default = "", update = updateEmpty)
    shear_dominant_l = StringProperty(default = "", update = updateEmpty)
    shear_subdominant_l = StringProperty(default = "", update = updateEmpty)
    distort_mode_l = StringProperty(default = "", update = updateEmpty)
    option_meshCenter_l = BoolProperty(default = True, update = updateEmpty)



    
    
    
    
    

    
    
    modes = [("Translate","Translate",""),("Rotate","Rotate",""),("Flatten","Flatten",""),("Scale","Scale",""),("Shrink/Fatten","Shrink/Fatten",""),("Modify Normals","Modify Normals",""),("Smooth","Smooth",""),("Bend","Bend",""),("Taper","Taper",""),("Twist","Twist",""),("Shear","Shear",""),("Project","Project","")]
    axes_strict = [("X","X",""),("Y","Y",""),("Z","Z","")]
    axes = [("All","All",""),("X","X",""),("Y","Y",""),("Z","Z","")]
    flatten = [("To Vector","To Vector",""),("To Normal","To Normal","")]
    proj_m = [("Direction","Direction",""),("Normal","Normal",""),("Closest","Closest","")]
    proj_n = [("p","Positive",""),("n","Negative",""),("s","Closest","")]
    proj_c = [("s","Surface Point",""),("v","Vertex","")]
    normals_m = [("Invert","Invert",""), ("Inside","Inside",""), ("Outside","Outside","")]

    
    
    mode_list = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Modes",
        update = updateNode
    )
    

    rotate_axes_list = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        description = "Axis Modes",
        update = updateNode
    )
    
    flatten_modes = EnumProperty(
        name = "Choose Mode",
        items = flatten,
        description = "Flatten Modes",
        update = updateNode
    )
    
    flatten_axes = EnumProperty(
        name = "Choose Mode",
        items = axes,
        description = "Axis Modes",
        update = updateNode
    )
    
    flatten_axes_s = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        description = "Axis Modes",
        update = updateNode
    )
    
    scale_axes = EnumProperty(
        name = "Choose Mode",
        items = axes,
        description = "Axis Modes",
        update = updateNode
    )
    
    projection_modes = EnumProperty(
        name = "Choose Mode",
        items = proj_m,
        description = "Axis Modes",
        update = updateNode
    )
    
    projection_modes_n = EnumProperty(
        name = "Choose Mode",
        items = proj_n,
        description = "Axis Modes",
        update = updateNode
    )
    
    projection_modes_d = EnumProperty(
        name = "Choose Mode",
        items = proj_n,
        description = "Axis Modes",
        update = updateNode
    )
    
    projection_modes_close = EnumProperty(
        name = "Choose Mode",
        items = proj_c,
        description = "Axis Modes",
        update = updateNode
    )
    

    
    fatten_X = BoolProperty(
        name = "Faces",
        description = "Faces",
        default = True,
        update = updateNode
    )
    
    fatten_Y = BoolProperty(
        name = "Faces",
        description = "Faces",
        default = True,
        update = updateNode
    )
    
    fatten_Z = BoolProperty(
        name = "Faces",
        description = "Faces",
        default = True,
        update = updateNode
    )
    
    normals_mode = EnumProperty(
        name = "Choose Mode",
        items = normals_m,
        description = "Axis Modes",
        update = updateNode
    )
    
    smooth_X = BoolProperty(
        name = "Faces",
        description = "Faces",
        default = True,
        update = updateNode
    )
    
    smooth_Y = BoolProperty(
        name = "Faces",
        description = "Faces",
        default = True,
        update = updateNode
    )
    
    smooth_Z = BoolProperty(
        name = "Faces",
        description = "Faces",
        default = True,
        update = updateNode
    )
    
    
    bend_axis = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        description = "Bend Axis",
        update = updateNode
    )
    
    
    taper_axis = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        description = "Taper Axis",
        update = updateNode
    )
    
    
    twist_axis = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        description = "Twist Axis",
        update = updateNode
    )
    
    shear_dominant = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        description = "Shear Axis Dominant",
        update = updateNode
    )
    
    shear_subdominant = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        description = "Shear Axis Subdominant",
        update = updateNode
    )
    
    
    option_meshCenter = BoolProperty(
        default = False,
        update = updateNode
    )

    
    
    
    
    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):

        #hide all inputs
        for input in self.inputs:
            if input.name != "Mesh" and input.name != "Selection":
                input.enabled = False
                
        if len(self.inputs) == 27:

            if self.mode_list == "Translate":
                #add new inputs, based on the selected mode
                self.inputs[2].enabled = True
            
            elif self.mode_list == "Rotate":
                self.inputs[3].enabled = True
                if not self.option_meshCenter:
                    self.inputs[4].enabled = True
                
                
            elif self.mode_list == "Flatten":
                if self.flatten_modes == "To Vector":
                    self.inputs[5].enabled = True
                    
                if not self.option_meshCenter:
                    self.inputs[25].enabled = True
                
                
            elif self.mode_list == "Scale":
                self.inputs[6].enabled = True
                if not self.option_meshCenter:
                    self.inputs[7].enabled = True
                
                
            elif self.mode_list == "Project":
                self.inputs[9].enabled = True
                if self.projection_modes == "Direction":
                    self.inputs[8].enabled = True
                
                
            elif self.mode_list == "Shrink/Fatten":
                self.inputs[10].enabled = True
                
                
            elif self.mode_list == "Smooth":
                self.inputs[11].enabled = True
                
                
            elif self.mode_list == "Bend":
                self.inputs[12].enabled = True
                self.inputs[13].enabled = True
                self.inputs[14].enabled = True
                self.inputs[15].enabled = True
                
                
            elif self.mode_list == "Taper":
                self.inputs[16].enabled = True
                self.inputs[17].enabled = True
                self.inputs[18].enabled = True
                if not self.option_meshCenter:
                    self.inputs[19].enabled = True
                
                
            elif self.mode_list == "Twist":
                self.inputs[20].enabled = True
                self.inputs[21].enabled = True
                self.inputs[22].enabled = True
                if not self.option_meshCenter:
                    self.inputs[23].enabled = True
                
                
            elif self.mode_list == "Shear":
                self.inputs[24].enabled = True
            
    
    ##\brief Initializes the node.
    def init(self, context):
        

        self.inputs.new("socket_MESH", "Mesh")
        self.inputs.new("socket_SELECTION", "Selection")
        
        #Translate Inputs
        self.inputs.new("socket_VEC3_F","Vector")
        
        #Rotate Inputs
        socket = self.inputs.new("socket_FLOAT", "Angle")
        socket.enabled = False
        socket = self.inputs.new("socket_VEC3_F","Pivot")
        socket.enabled = False
        
        #Flatten Inputs
        socket = self.inputs.new("socket_VEC3_F", "Vector")
        socket.enabled = False
        
        #Scale Inputs
        socket = self.inputs.new("socket_FLOAT","Factor")
        socket.enabled = False
        socket = self.inputs.new("socket_VEC3_F","Pivot")
        socket.enabled = False
        
        #Projection Inputs
        socket = self.inputs.new("socket_VEC3_F", "Direction")
        socket.enabled = False
        socket = self.inputs.new("socket_MESH", "Target")
        socket.enabled = False
        
        #Shrink/Fatten Inputs
        socket = self.inputs.new("socket_FLOAT","Amount")
        socket.enabled = False
        
        #Smooth Inputs
        socket = self.inputs.new("socket_INT", "Iterations")
        socket.enabled = False
        
        #Bend Inputs
        socket = self.inputs.new("socket_FLOAT","Start")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT","End")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT","Angle")
        socket.enabled = False
        socket = self.inputs.new("socket_VEC3_F","Direction")
        socket.enabled = False
        
        #Taper Inputs
        socket = self.inputs.new("socket_FLOAT","Start")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT","End")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT","Amount")
        socket.enabled = False
        socket = self.inputs.new("socket_VEC3_F","Pivot")
        socket.enabled = False
        
        #Twist Inputs
        socket = self.inputs.new("socket_FLOAT","Start")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT","End")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT","Angle")
        socket.enabled = False
        socket = self.inputs.new("socket_VEC3_F","Pivot")
        socket.enabled = False
        
        #Shear Inputs
        socket = self.inputs.new("socket_FLOAT","Amount")
        socket.enabled = False
        socket = self.inputs.new("socket_VEC3_F","Pivot")
        socket.enabled = False
        
        
        socket = self.inputs.new("socket_VEC3_F","Pivot")
        socket.enabled = False
        
        self.use_custom_color = True
        self.color = (1,.8,.5)
        

        
        socket = self.outputs.new("socket_MESH", "Mesh")
        
        
        
        self.update()

    ##\brief GUI.    
    def draw_buttons(self, context, layout):
        
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "mode_list", "")
        
        if self.mode_list == "Translate":
            layout.separator()
        
        elif self.mode_list == "Rotate":
            layout.separator()
            rowA = layout.row()
            rowA.prop(self, "rotate_axes_list", "")
            rowB = layout.row()
            rowB.prop(self,"option_meshCenter","Mesh Center")
            layout.separator()
                
                
        elif self.mode_list == "Flatten":
            layout.separator()
            rowM = layout.row(align = True)
            rowM.prop(self, "flatten_modes", "")

            layout.separator()
            rowL = layout.row(align = True)
            rowL.label(text = "Lock to Axis:")
            rowA = layout.row(align = True)
            rowA.prop(self, "flatten_axes", "")
            rowB = layout.row()
            rowB.prop(self,"option_meshCenter","Mesh Center")
            layout.separator()
                
        elif self.mode_list == "Scale":
            layout.separator()
            rowM = layout.row(align = True)
            rowM.prop(self, "scale_axes", "")
            rowB = layout.row()
            rowB.prop(self,"option_meshCenter","Mesh Center")
            layout.separator()
                
                
        elif self.mode_list == "Project":
            layout.separator()
            rowM = layout.row(align = True)
            rowM.prop(self, "projection_modes", "")
            if self.projection_modes == "Normal":
                rowN = layout.row()
                rowN.prop(self,"projection_modes_n","")
            elif self.projection_modes == "Closest":
                rowC = layout.row()
                rowC.prop(self,"projection_modes_close","")
            else:
                rowN = layout.row()
                rowN.prop(self,"projection_modes_d","")

                
                
        elif self.mode_list == "Shrink/Fatten":
            layout.separator()
            rowX = layout.row(align = True)
            rowY = layout.row(align = True)
            rowZ = layout.row(align = True)
            
            colX1 = rowX.column(align = True)
            colX2 = rowX.column(align = True)
            colX3 = rowX.column(align = True)
            
            colY1 = rowY.column(align = True)
            colY2 = rowY.column(align = True)
            colY3 = rowY.column(align = True)
            
            colZ1 = rowZ.column(align = True)
            colZ2 = rowZ.column(align = True)
            colZ3 = rowZ.column(align = True)
            
            colX1.label(text = "X-Axis")
            colY1.label(text = "Y-Axis")
            colZ1.label(text = "Z-Axis")
            
            colX2.prop(self,"fatten_X","")
            colY2.prop(self,"fatten_Y","")
            colZ2.prop(self,"fatten_Z","")
              

        elif self.mode_list == "Modify Normals":
            layout.separator()
            rowM = layout.row(align = True)
            rowM.prop(self, "normals_mode", "")
              
                
        elif self.mode_list == "Smooth":
            layout.separator()
            rowX = layout.row(align = True)
            rowY = layout.row(align = True)
            rowZ = layout.row(align = True)
            
            colX1 = rowX.column(align = True)
            colX2 = rowX.column(align = True)
            colX3 = rowX.column(align = True)
            
            colY1 = rowY.column(align = True)
            colY2 = rowY.column(align = True)
            colY3 = rowY.column(align = True)
            
            colZ1 = rowZ.column(align = True)
            colZ2 = rowZ.column(align = True)
            colZ3 = rowZ.column(align = True)
            
            colX1.label(text = "X-Axis")
            colY1.label(text = "Y-Axis")
            colZ1.label(text = "Z-Axis")
            
            colX2.prop(self,"smooth_X","")
            colY2.prop(self,"smooth_Y","")
            colZ2.prop(self,"smooth_Z","")
                
                
        elif self.mode_list == "Bend":
                
            layout.separator()
            row1 = layout.row()
            row1.prop(self,"bend_axis","")
            
            
                
        elif self.mode_list == "Taper":
            layout.separator()
        
            rowA = layout.row(align = True)
            
            rowA.prop(self, "taper_axis", "")
            rowB = layout.row()
            rowB.prop(self,"option_meshCenter","Mesh Center")
                
            layout.separator()
                
                
        elif self.mode_list == "Twist":
            layout.separator()
        
            rowA = layout.row(align = True)
            
            rowA.prop(self, "twist_axis", "")
            rowB = layout.row()
            rowB.prop(self,"option_meshCenter","Mesh Center")
                
            layout.separator()
                
                
        elif self.mode_list == "Shear":
            layout.separator()
            
            rowDL = layout.row(align = True)
            rowD = layout.row(align = True)
            
            rowSDL = layout.row(align = True)
            rowSD = layout.row(align = True)
            
            
            rowDL.label(text = "Dominant:")
            rowSDL.label(text = "Subdominant:")
            
            rowD.prop(self, "shear_dominant", "")
            rowSD.prop(self, "shear_subdominant", "")
            layout.separator()
        
    ##\brief Re-calculates the node's data.    
    def recalculate(self):


        self.corrupted = False
        
        if len(self.inputs[0].links) > 0:
            
            copy_obs = self.inputs[0].returnData()
            selections = self.inputs[1].returnData()
            
            
            
            if self.mode_list == "Translate":
            
                vecs = self.inputs[2].returnData()
                lists = utils_GEN.adjustLists([copy_obs,selections,vecs])
                
                copy_obs = lists[0]
                selections = lists[1]
                vecs = lists[2]
                
                print(copy_obs)
                
                
                for i in range (0, len(copy_obs)):
                
                    selection = selections[i]
                
                    if not selection in [[None],["X"],"X",None]:
                        selection = utils_SEL.mapSelection(selection, copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                        for vid in selection[0]:
                            copy_obs[i].data.vertices[vid].co += vecs[i]
                            
                    else:
                        utils_OBJ.prepTransforms(copy_obs[i])
                        copy_obs[i].location += vecs[i]
                        utils_OBJ.applyTransforms(copy_obs[i])
                        

                        
                        
                        
                
            elif self.mode_list == "Rotate":
            
                if not self.option_meshCenter:
            
                    pivots = self.inputs[4].returnData()
                    angles = self.inputs[3].returnData()
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,pivots,angles])
                    
                    copy_obs = lists[0]
                    selections = lists[1]
                    pivots = lists[2]
                    angles = lists[3]
                    
                else:
                    

                    angles = self.inputs[3].returnData()
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,angles])
                    
                    copy_obs = lists[0]
                    selections = lists[1]
                    angles = lists[2]
                    
                
                for i in range(0,len(copy_obs)):
                
                    selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)

                    if not self.option_meshCenter:
                        pivot = -pivots[i]
                    else:
                        clist = [v.co for v in copy_obs[i].data.vertices]
                        c = utils_MATH.getMidCoords(clist)
                        
                        pivot = -c

                    angle = angles[i]
                    rotmat = mathutils.Matrix.Rotation(math.radians(angle), 4, self.rotate_axes_list)

                
                
                
                    for vid in selection[0]:
                            vert = copy_obs[i].data.vertices[vid]
                            vert.co += pivot
                            vert.co = vert.co * rotmat
                            vert.co -= pivot
                            copy_obs[i].data.vertices[vid].co = vert.co

                        
                

                
                
                
                
            elif self.mode_list == "Flatten":
            
                
            
                plane_vecs = []

                
                
                
                if self.flatten_modes == "To Vector":

                    if self.option_meshCenter:
                        
                        plane_vecs = self.inputs[5].returnData()
                    
                    
                        lists = utils_GEN.adjustLists([copy_obs,selections,plane_vecs])
                        
                        copy_obs = lists[0]
                        selections = lists[1]
                        plane_vecs = lists[2]
                        
                    else:
                    
                        plane_vecs = self.inputs[5].returnData()
                        plane_pts = self.inputs[5].returnData()
                    
                    
                        lists = utils_GEN.adjustLists([copy_obs,selections,plane_vecs])
                        
                        copy_obs = lists[0]
                        selections = lists[1]
                        plane_vecs = lists[2]
                    
                        
                    
                    
                    sel_temp = []
                    for i in range(0,len(selections)):
                        sel_temp.append(utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True))
                    selections = sel_temp
                    
                    
                elif self.flatten_modes == "To Normal": 
                
                    if self.option_meshCenter:
                        lists = utils_GEN.adjustLists([copy_obs,selections])
                        copy_obs = lists[0]
                        selections = lists[1]
                    else:
                    
                        plane_pts = self.inputs[25].returnData()
                    
                        lists = utils_GEN.adjustLists([copy_obs,selections,plane_pts])
                        copy_obs = lists[0]
                        selections = lists[1]
                        plane_pts = lists[2]
                    
                    sel_temp = []
                    for i in range(0,len(selections)):
                        sel_temp.append(utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True))
                    selections = sel_temp
                    
                    
                        
                    for i in range (0, len(copy_obs)):
                    
                        normals = []
                        
                        for vid in selections[i][0]:
                            normals.append(copy_obs[i].data.vertices[vid].normal)
                         
                        nor = mathutils.Vector(utils_MATH.getMidCoords(normals))
                        if nor.length == 0:
                            nor = mathutils.Vector([0,0,1])
                        plane_vecs.append(nor)
                        
                        
                

                
                #We already have both plane normal and hook point. Intersection line is determined by selected axis lock. If axis is locked to "All", we need to determine the shortest path from vertex to plane.

                int_vecs = []
                    
                if self.flatten_axes == "X":
                        
                    for i in range(0, len(copy_obs)):
                        int_vecs.append(mathutils.Vector((1.0, 0.0, 0.0)));

                elif self.flatten_axes == "Y":
                    
                    for i in range(0, len(copy_obs)):
                        int_vecs.append(mathutils.Vector((0.0, 1.0, 0.0)));
                    
                elif self.flatten_axes == "Z":
                    
                    for i in range(0, len(copy_obs)):
                        int_vecs.append(mathutils.Vector((0.0, 0.0, 1.0)));
                        
                elif self.flatten_axes == "All":
                    #inverse plane normal
                    for i in range(0, len(copy_obs)):
                        
                        vec = plane_vecs[i]
                        if vec.length == 0:
                            vec = mathutils.Vector([0,0,1])
                        
                        int_vecs.append(-vec)

                        
                #now we have everything we need for the built-in intersection function to work
                    
                for i in range(0, len(copy_obs)):
                
                    if self.option_meshCenter:
                    
                        clist = [v.co for v in copy_obs[i].data.vertices]
                        center = utils_MATH.getMidCoords(clist)
                        
                        
                        vec = plane_vecs[i]
                        if vec.length == 0:
                            vec = mathutils.Vector([0,0,1])
                        

                        for vid in selections[i][0]:
                            
                            coords = mathutils.Vector(copy_obs[i].data.vertices[vid].co)
                            intersection = mathutils.geometry.intersect_line_plane(coords,coords + mathutils.Vector(int_vecs[i]),center, vec)
                            if not intersection is None:
                                copy_obs[i].data.vertices[vid].co = intersection.to_tuple()
                                
                    else:
                    
                        vec = plane_vecs[i]
                        if vec.length == 0:
                            vec = mathutils.Vector([0,0,1])
                        
                        for vid in selections[i][0]:
                            
                            coords = mathutils.Vector(copy_obs[i].data.vertices[vid].co)
                            intersection = mathutils.geometry.intersect_line_plane(coords,coords + mathutils.Vector(int_vecs[i]),plane_pts[i], vec)
                            if not intersection is None:
                                copy_obs[i].data.vertices[vid].co = intersection.to_tuple()
                        
                

                
                
                
                
                
                

            elif self.mode_list == "Scale":
            
                if self.option_meshCenter:
                

                    factors = self.inputs[6].returnData()
                    
                    print_debug("TEST:",str(copy_obs))
                    print_debug("   ->",str(selections))
                    print_debug("   ->",str(factors))
                    
                    
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,factors])
                    copy_obs = lists[0]
                    selections = lists[1]
                    factors = lists[2]
                    
                    
                else:
                    
                    factors = self.inputs[6].returnData()
                    pivots = self.inputs[7].returnData()
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,factors,pivots])
                    copy_obs = lists[0]
                    selections = lists[1]
                    factors = lists[2]
                    pivots = lists[3]
                    
                    
                 


                if self.scale_axes == "All":
                    
                    for i in range(0, len(copy_obs)):
                    
                        selection = selections[i]
                    
                        if not selection in [[None],["X"],"X",None]:
                            selection = utils_SEL.mapSelection(selection, copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                            
                            if not self.option_meshCenter:
                                piv = pivots[i]
                            else:
                                clist = [v.co for v in copy_obs[i].data.vertices]
                                piv = utils_MATH.getMidCoords(clist)
                            
                            
                            
                            for vid in selection[0]:
                            
                                copy_obs[i].data.vertices[vid].co - piv
                                dir[0] = dir[0] * factors[i]
                                dir[1] = dir[1] * factors[i]
                                dir[2] = dir[2] * factors[i]
                            
                                copy_obs[i].data.vertices[vid].co = dir+piv
                                
                        else:
                        
                            utils_OBJ.prepTransforms(copy_obs[i])
                        
                            copy_obs[i].scale[0] *= factors[i]
                            copy_obs[i].scale[1] *= factors[i]
                            copy_obs[i].scale[2] *= factors[i]
                            
                            utils_OBJ.applyTransforms(copy_obs[i])
                                
                
                        
                        
                elif self.scale_axes == "X":
                
                    for i in range(0, len(copy_obs)):
                        selection = selections[i]
                        if not selection in [[None],["X"],"X",None]:
                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                            
                            if not self.option_meshCenter:
                                piv = pivots[i]
                            else:
                                clist = [v.co for v in copy_obs[i].data.vertices]
                                piv = utils_MATH.getMidCoords(clist)
                            
                            for vid in selection[0]:
                            
                                piv[1] = copy_obs[i].data.vertices[vid].co[1]
                                piv[2] = copy_obs[i].data.vertices[vid].co[2]
                            
                                dir = utils_MATH.vec3_add(copy_obs[i].data.vertices[vid].co, utils_MATH.vec3_invert(piv))
                                
                                dir[0] = dir[0] * factors[i]
                                
                                copy_obs[i].data.vertices[vid].co = utils_MATH.vec3_add(dir,piv)
                        
                        else:
                        
                            utils_OBJ.prepTransforms(copy_obs[i])
                            
                            copy_obs[i].scale[0] *= factors[i]
                            
                            utils_OBJ.applyTransforms(copy_obs[i])
                            
                            
                        
                elif self.scale_axes == "Y":
                    for i in range(0, len(copy_obs)):
                        selection = selections[i]
                        if not selection in [[None],["X"],"X",None]:
                        
                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                            
                            if not self.option_meshCenter:
                                piv = pivots[i]
                            else:
                                clist = [v.co for v in copy_obs[i].data.vertices]
                                piv = utils_MATH.getMidCoords(clist)
                            
                            for vid in selection[0]:
                            
                                piv[0] = copy_obs[i].data.vertices[vid].co[0]
                                piv[2] = copy_obs[i].data.vertices[vid].co[2]
                            
                                dir = utils_MATH.vec3_add(copy_obs[i].data.vertices[vid].co, utils_MATH.vec3_invert(piv))
                                
                                dir[1] = dir[1] * factors[i]
                                
                                copy_obs[i].data.vertices[vid].co = utils_MATH.vec3_add(dir,piv)
                                
                        else:
                            utils_OBJ.prepTransforms(copy_obs[i])
                            copy_obs[i].scale[1] *= factors[i]
                            utils_OBJ.applyTransforms(copy_obs[i])
                                
                        
                        
                elif self.scale_axes == "Z":
                
                    for i in range(0, len(copy_obs)):
                        selection = selections[i]
                        if not selection in [[None],["X"],"X",None]:
                    
                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                            
                            if not self.option_meshCenter:
                                piv = pivots[i]
                            else:
                                clist = [v.co for v in copy_obs[i].data.vertices]
                                piv = utils_MATH.getMidCoords(clist)
                            
                            for vid in selection[0]:
                                
                                piv[1] = copy_obs[i].data.vertices[vid].co[1]
                                piv[0] = copy_obs[i].data.vertices[vid].co[0]
                            
                                dir = utils_MATH.vec3_add(copy_obs[i].data.vertices[vid].co, utils_MATH.vec3_invert(piv))
                                
                                dir[2] = dir[2] * factors[i]
                                
                                copy_obs[i].data.vertices[vid].co = utils_MATH.vec3_add(dir,piv)
                                
                        else:
                            utils_OBJ.prepTransforms(copy_obs[i])
                            copy_obs[i].scale[2] *= factors[i]
                            utils_OBJ.applyTransforms(copy_obs[i])
                        
                      

      
                
            elif self.mode_list == "Shrink/Fatten":

                amounts = self.inputs[10].returnData()
                
                lists = utils_GEN.adjustLists([copy_obs,selections,amounts])
                copy_obs = lists[0]
                selections = lists[1]
                amounts = lists[2]
                
                

                
                
                for i in range(0, len(copy_obs)):
                
                    selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                
                
                    for vid in selection[0]:
                        normal = copy_obs[i].data.vertices[vid].normal
                        if self.fatten_X == False:
                            normal[0] = 0
                        if self.fatten_Y == False:
                            normal[1] = 0
                        if self.fatten_Z == False:
                            normal[2] = 0
                            
                        normal = utils_MATH.vec3_normalize(normal)
                        amt = amounts[i]
                        
                    
                        copy_obs[i].data.vertices[vid].co[0] += normal[0] * amt
                        copy_obs[i].data.vertices[vid].co[1] += normal[1] * amt
                        copy_obs[i].data.vertices[vid].co[2] += normal[2] * amt
                
                
                
                
                
                
                
            elif self.mode_list == "Modify Normals":
                
                for i in range(0,len(copy_obs)):
                
                    bpy.context.scene.objects.link(copy_obs[i]) 
                    bpy.context.scene.objects.active = copy_obs[i]
                
                
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.select_mode(type="VERT")
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    
                    
                    selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                    
                
                
                    for vid in selection[0]:
                            copy_obs[i].data.vertices[vid].select = True 

                    bpy.ops.object.mode_set(mode = 'EDIT')
                
                    if self.normals_mode == "Invert":
                        bpy.ops.mesh.flip_normals()
                    elif self.normals_mode == "Inside":
                        bpy.ops.mesh.normals_make_consistent(inside=True)
                    elif self.normals_mode == "Outside":
                        bpy.ops.mesh.normals_make_consistent(inside=False)
 
 
 
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.context.scene.objects.unlink(copy_obs[i])
                
                
                
                
            elif self.mode_list == "Smooth":
                
                iterations = [1]
                if len(self.inputs[11].links) > 0:
                    iterations = self.inputs[11].returnData()
                
                
                
                lists = utils_GEN.adjustLists([copy_obs,selections,iterations])
                copy_obs = lists[0]
                selections = lists[1]
                iterations = lists[2]
                
                for i in range(0,len(copy_obs)):
                
                
                    bpy.context.scene.objects.link(copy_obs[i]) 
                    bpy.context.scene.objects.active = copy_obs[i]
                
                
                    selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)

                
                
                    for vid in selection[0]:
                        copy_obs[i].data.vertices[vid].select = True

                    bpy.ops.object.mode_set(mode = 'EDIT')
                
                    bpy.ops.mesh.vertices_smooth(repeat = iterations[i], xaxis = self.smooth_X, yaxis = self.smooth_Y, zaxis = self.smooth_Z)
 

                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.context.scene.objects.unlink(copy_obs[i])
                    
                    
                
                
            elif self.mode_list == "Bend":
            
                root = math.sqrt(2)
                

                up = mathutils.Vector([0,0,1])
                y_unit = mathutils.Vector([0,1,0])
                x_unit = mathutils.Vector([0,0,1])

                starts = self.inputs[12].returnData()
                stops = self.inputs[13].returnData()
                angles = self.inputs[14].returnData()
                directions = self.inputs[15].returnData()
                
                
                lists = utils_GEN.adjustLists([copy_obs,selections,starts,stops,angles,directions])
                copy_obs = lists[0]
                selections = lists[1]
                starts = lists[2]
                stops = lists[3]
                angles = lists[4]
                directions = lists[5]
                
                
                if self.bend_axis == "Z":
                
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        start = starts[i]
                        stop = stops[i]
                        angle = angles[i]
                        direction = directions[i]
                    
                    
                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                    
                        
                        distance = stop-start
                        
                        dir = mathutils.Vector([direction[0],direction[1],0])
                        dir.normalize()
                        dir[1] = -dir[1]


                        
                        
                        angle1 = utils_MATH.getAngleNor(dir,y_unit,up)
                        
                        mat1 = mathutils.Matrix.Rotation(angle1, 4, "Z").to_3x3()
                        mat1_inv = mat1.copy()
                        mat1_inv.invert()

                    
                        for vid in selection[0]:
                            
                            vert = copy_ob.data.vertices[vid]
                            
                            zoffs = vert.co[2]
                            
                            zoffs2 = zoffs
                            
                            if zoffs2 > stop:
                                zoffs2 = stop
                            elif zoffs2 < start:
                                zoffs2 = start


                            

                            fac = (stop - zoffs2)/distance
                            
                            fac = max(0,min(1,1-fac))

                            
                            mat2 = mathutils.Matrix.Rotation(fac*math.radians(-angle), 4, "X").to_3x3()
                            
                            
                            rotmat = mat1*mat2

                            vert.co = vert.co * rotmat
                            
                            vert.co = vert.co * mat1_inv

                    
                
                
                
                elif self.bend_axis == "Y":
                
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        start = starts[i]
                        stop = stops[i]
                        angle = angles[i]
                        direction = directions[i]
                    
                    
                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                    
                        
                        distance = stop-start
                        
                        dir = mathutils.Vector([direction[0],0,direction[2]])
                        dir.normalize()
                        
                        dir[0] = -dir[0]

                        
                        
                        angle1 = utils_MATH.getAngleNor(dir,x_unit,y_unit)
                        
                        mat1 = mathutils.Matrix.Rotation(-angle1, 4, "Y").to_3x3()
                        mat1_inv = mat1.copy()
                        mat1_inv.invert()

                    
                        for vid in selection[0]:
                            
                            vert = copy_ob.data.vertices[vid]
                            
                            zoffs = vert.co[1]
                            
                            zoffs2 = zoffs
                            
                            if zoffs2 > stop:
                                zoffs2 = stop
                            elif zoffs2 < start:
                                zoffs2 = start

                            
                            

                            fac = (stop - zoffs2)/distance
                            
                            fac = max(0,min(1,1-fac))

                            
                            mat2 = mathutils.Matrix.Rotation(fac*math.radians(-angle), 4, "X").to_3x3()
                            
                            
                            rotmat = mat1*mat2

                            vert.co = vert.co * rotmat
                            
                            vert.co = vert.co * mat1_inv

                
                
                
                
                
                elif self.bend_axis == "X":
                
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        start = starts[i]
                        stop = stops[i]
                        angle = angles[i]
                        direction = directions[i]
                    
                    
                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                    
                        
                        distance = stop-start
                        
                        dir = mathutils.Vector([0,direction[1],direction[2]])
                        dir.normalize()
                        
                        dir[1] = -dir[1]

                        
                        
                        angle1 = utils_MATH.getAngleNor(dir,y_unit,x_unit)
                        
                        mat1 = mathutils.Matrix.Rotation(angle1, 4, "X").to_3x3()
                        mat1_inv = mat1.copy()
                        mat1_inv.invert()

                    
                        for vid in selection[0]:
                            
                            vert = copy_ob.data.vertices[vid]
                            
                            zoffs = vert.co[0]
                            
                            zoffs2 = zoffs
                            
                            if zoffs2 > stop:
                                zoffs2 = stop
                            elif zoffs2 < start:
                                zoffs2 = start

                            
                            

                            fac = (stop - zoffs2)/distance
                            
                            fac = max(0,min(1,1-fac))

                            
                            mat2 = mathutils.Matrix.Rotation(fac*math.radians(angle), 4, "Z").to_3x3()
                            
                            
                            rotmat = mat1*mat2

                            vert.co = vert.co * rotmat
                            
                            vert.co = vert.co * mat1_inv
                
                            
                            
                            
                        
                        
                            
                            
                            
  
                
                
            elif self.mode_list == "Taper":
    
                
                if not self.option_meshCenter:
                
                    starts = self.inputs[16].returnData()
                    stops = self.inputs[17].returnData()
                    factors = self.inputs[18].returnData()
                    pivots = self.inputs[19].returnData()
                    
                    
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,starts,stops,pivots,factors])
                    copy_obs = lists[0]
                    selections = lists[1]
                    starts = lists[2]
                    stops = lists[3]
                    pivots = lists[4]
                    factors = lists[5]
                    
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        start = starts[i]
                        stop = stops[i]
                        pivot = pivots[i]
                        factor = factors[i]
                    
                    
                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                    
                    
                    

                        #Taper

                        if self.taper_axis == "Z":
                            for vid in selection[0]:
                                flat_v = (copy_ob.data.vertices[vid].co[0],copy_ob.data.vertices[vid].co[1],0)
                                flat_p = utils_MATH.vec3_invert((pivot[0],pivot[1],0))
                                
                                target_vec = utils_MATH.vec3_add(flat_v, flat_p)
                                
                                ratio = (copy_ob.data.vertices[vid].co[2] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0
        
        
                                fac = utils_MATH.interpolate(1,factor,ratio,"Linear")
                                
                                    
                                copy_ob.data.vertices[vid].co = [pivot[0] + target_vec[0]*fac, pivot[1] + target_vec[1]*fac, copy_ob.data.vertices[vid].co[2]]
                                
                                
                        elif self.taper_axis == "X":
                            for vid in selection[0]:
                                flat_v = (0,copy_ob.data.vertices[vid].co[1],copy_ob.data.vertices[vid].co[2])
                                flat_p = utils_MATH.vec3_invert((0,pivot[1],pivot[2]))
                                
                                target_vec = utils_MATH.vec3_add(flat_v, flat_p)
                                
                                ratio = (copy_ob.data.vertices[vid].co[0] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0
        
        
                                fac = utils_MATH.interpolate(1,factor,ratio,"Linear")
                                
                                    
                                copy_ob.data.vertices[vid].co = [copy_ob.data.vertices[vid].co[0],pivot[1] + target_vec[1]*fac, pivot[2] + target_vec[2]*fac]
                                
                            
                        elif self.taper_axis == "Y":
                            for vid in selection[0]:
                                flat_v = (copy_ob.data.vertices[vid].co[0],0,copy_ob.data.vertices[vid].co[2])
                                flat_p = utils_MATH.vec3_invert((pivot[0],0,pivot[2]))
                            
                                target_vec = utils_MATH.vec3_add(flat_v, flat_p)
                            
                                ratio = (copy_ob.data.vertices[vid].co[1] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0
        
        
                                fac = utils_MATH.interpolate(1,factor,ratio,"Linear")
                                
                                    
                                copy_ob.data.vertices[vid].co = [pivot[0] + target_vec[0]*fac,copy_ob.data.vertices[vid].co[1], pivot[2] + target_vec[2]*fac]
                            
                else:
                    
                    
                    
                    starts = self.inputs[16].returnData()
                    stops = self.inputs[17].returnData()
                    factors = self.inputs[18].returnData()
                    
                    
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,starts,stops,factors])
                    copy_obs = lists[0]
                    selections = lists[1]
                    starts = lists[2]
                    stops = lists[3]
                    factors = lists[4]
                    
                    for i in range(0,len(copy_obs)):
                        
                        c = []
                    
                        for vert in copy_obs[i].data.vertices:
                            c.append(vert.co)
                    
                        copy_ob = copy_obs[i]
                        start = starts[i]
                        stop = stops[i]
                        pivot = utils_MATH.getMidCoords(c)
                        factor = factors[i]
                    
                    
                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                    
                    
                    

                        #Taper

                        if self.taper_axis == "Z":
                            for vid in selection[0]:
                                flat_v = (copy_ob.data.vertices[vid].co[0],copy_ob.data.vertices[vid].co[1],0)
                                flat_p = utils_MATH.vec3_invert((pivot[0],pivot[1],0))
                                
                                target_vec = utils_MATH.vec3_add(flat_v, flat_p)
                                
                                ratio = (copy_ob.data.vertices[vid].co[2] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0
        
        
                                fac = utils_MATH.interpolate(1,factor,ratio,"Linear")
                                
                                    
                                copy_ob.data.vertices[vid].co = [pivot[0] + target_vec[0]*fac, pivot[1] + target_vec[1]*fac, copy_ob.data.vertices[vid].co[2]]
                                
                                
                        elif self.taper_axis == "X":
                            for vid in selection[0]:
                                flat_v = (0,copy_ob.data.vertices[vid].co[1],copy_ob.data.vertices[vid].co[2])
                                flat_p = utils_MATH.vec3_invert((0,pivot[1],pivot[2]))
                                
                                target_vec = utils_MATH.vec3_add(flat_v, flat_p)
                                
                                ratio = (copy_ob.data.vertices[vid].co[0] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0
        
        
                                fac = utils_MATH.interpolate(1,factor,ratio,"Linear")
                                
                                    
                                copy_ob.data.vertices[vid].co = [copy_ob.data.vertices[vid].co[0],pivot[1] + target_vec[1]*fac, pivot[2] + target_vec[2]*fac]
                                
                            
                        elif self.taper_axis == "Y":
                            for vid in selection[0]:
                                flat_v = (copy_ob.data.vertices[vid].co[0],0,copy_ob.data.vertices[vid].co[2])
                                flat_p = utils_MATH.vec3_invert((pivot[0],0,pivot[2]))
                            
                                target_vec = utils_MATH.vec3_add(flat_v, flat_p)
                            
                                ratio = (copy_ob.data.vertices[vid].co[1] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0
        
        
                                fac = utils_MATH.interpolate(1,factor,ratio,"Linear")
                                
                                    
                                copy_ob.data.vertices[vid].co = [pivot[0] + target_vec[0]*fac,copy_ob.data.vertices[vid].co[1], pivot[2] + target_vec[2]*fac]






















                
                
                
            elif self.mode_list == "Twist":
                starts = [0]
                stops = [1]
                pivots = [[0,0,0]]
                angles = [45]
                
                
                    
                if len(self.inputs[20].links) > 0:
                    starts = self.inputs[20].returnData()


                if len(self.inputs[21].links) > 0:
                    stops = self.inputs[21].returnData()
                
                
                if len(self.inputs[22].links) > 0:
                    angles = self.inputs[22].returnData()
                
                
                if len(self.inputs[23].links) > 0:
                    pivots = self.inputs[23].returnData()
                
                
                if not self.option_meshCenter:
                
                    lists = utils_GEN.adjustLists([copy_obs,selections,starts,stops,pivots,angles])
                    copy_obs = lists[0]
                    selections = lists[1]
                    starts = lists[2]
                    stops = lists[3]
                    pivots = lists[4]
                    angles = lists[5]
                    
 
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        start = starts[i]
                        stop = stops[i]
                        pivot = pivots[i]
                        angle = angles[i]
                    
                    
                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                    
                    
                    

                        #Twist
                        if self.twist_axis == "Z":
                            for vid in selection[0]:
                                ratio = (copy_ob.data.vertices[vid].co[2] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0

                                fac = utils_MATH.interpolate(0,angle,ratio,"Linear")
                                
                                #move vert to pivot center
                                
                                pivot_inv = utils_MATH.vec3_invert(pivot)
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot_inv)
                                
                                rotmat = mathutils.Matrix.Rotation(utils_MATH.toRadians(fac), 4, "Z")
                                
                                copy_ob.data.vertices[vid].co = copy_ob.data.vertices[vid].co * rotmat
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot)
                                
                        elif self.twist_axis == "X":
                            for vid in selection[0]:
                                ratio = (copy_ob.data.vertices[vid].co[0] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0

                                fac = utils_MATH.interpolate(0,angle,ratio,"Linear")
                                
                                #move vert to pivot center
                                
                                pivot_inv = utils_MATH.vec3_invert(pivot)
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot_inv)
                            
                                rotmat = mathutils.Matrix.Rotation(utils_MATH.toRadians(fac), 4, "X")
                            
                                copy_ob.data.vertices[vid].co = copy_ob.data.vertices[vid].co * rotmat
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot)
                                    
                        elif self.twist_axis == "Y":
                            for vid in selection[0]:    
                                ratio = (copy_ob.data.vertices[vid].co[1] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0

                                fac = utils_MATH.interpolate(0,angle,ratio,"Linear")
                                
                                #move vert to pivot center
                                
                                pivot_inv = utils_MATH.vec3_invert(pivot)
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot_inv)
                                
                                rotmat = mathutils.Matrix.Rotation(utils_MATH.toRadians(fac), 4, "Y")
                                
                                copy_ob.data.vertices[vid].co = copy_ob.data.vertices[vid].co * rotmat
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot)
                                
                                
                else:
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,starts,stops,angles])
                    copy_obs = lists[0]
                    selections = lists[1]
                    starts = lists[2]
                    stops = lists[3]
                    angles = lists[4]
                    
                    
                    for i in range(0,len(copy_obs)):
                    
                        c = []
                        for vert in copy_obs[i].data.vertices:
                            c.append(vert.co)
                    
                    
                        copy_ob = copy_obs[i]
                        start = starts[i]
                        stop = stops[i]
                        pivot = utils_MATH.getMidCoords(c)
                        angle = angles[i]
                    
                    
                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                    
                    
                    

                        #Twist
                        if self.twist_axis == "Z":
                            for vid in selection[0]:
                                ratio = (copy_ob.data.vertices[vid].co[2] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0

                                fac = utils_MATH.interpolate(0,angle,ratio,"Linear")
                                
                                #move vert to pivot center
                                
                                pivot_inv = utils_MATH.vec3_invert(pivot)
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot_inv)
                                
                                rotmat = mathutils.Matrix.Rotation(utils_MATH.toRadians(fac), 4, "Z")
                                
                                copy_ob.data.vertices[vid].co = copy_ob.data.vertices[vid].co * rotmat
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot)
                                
                        elif self.twist_axis == "X":
                            for vid in selection[0]:
                                ratio = (copy_ob.data.vertices[vid].co[0] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0

                                fac = utils_MATH.interpolate(0,angle,ratio,"Linear")
                                
                                #move vert to pivot center
                                
                                pivot_inv = utils_MATH.vec3_invert(pivot)
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot_inv)
                            
                                rotmat = mathutils.Matrix.Rotation(utils_MATH.toRadians(fac), 4, "X")
                            
                                copy_ob.data.vertices[vid].co = copy_ob.data.vertices[vid].co * rotmat
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot)
                                    
                        elif self.twist_axis == "Y":
                            for vid in selection[0]:    
                                ratio = (copy_ob.data.vertices[vid].co[1] - start)/(stop-start)
                                if ratio > 1:
                                    ratio = 1
                                elif ratio < 0:
                                    ratio = 0

                                fac = utils_MATH.interpolate(0,angle,ratio,"Linear")
                                
                                #move vert to pivot center
                                
                                pivot_inv = utils_MATH.vec3_invert(pivot)
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot_inv)
                                
                                rotmat = mathutils.Matrix.Rotation(utils_MATH.toRadians(fac), 4, "Y")
                                
                                copy_ob.data.vertices[vid].co = copy_ob.data.vertices[vid].co * rotmat
                                
                                copy_ob.data.vertices[vid].co = utils_MATH.vec3_add(copy_ob.data.vertices[vid].co, pivot)
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                
                
            elif self.mode_list == "Shear":

                    
            
            
                amounts = self.inputs[24].returnData()
                
                if self.shear_dominant == self.shear_subdominant:
                    if self.shear_dominant in ["X","Y"]:
                        self.shear_subdominant = "Z"
                    else:
                        self.shear_subdominant = "Y"
                
                
                
                
                lists = utils_GEN.adjustLists([copy_obs,selections,amounts])
                copy_obs = lists[0]
                selections = lists[1]
                amounts = lists[3]
                
                for i in range(0,len(copy_obs)):
                
                    copy_ob = copy_obs[i]
                    amount = amounts[i]
                
                
                    selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                
                
                
                
                            
                
                    if self.shear_dominant == "X":

                        if self.shear_subdominant == "Y":
                            for vid in selection[0]:
                                vert = copy_ob.data.vertices[vid]
                                v_offset = vert.co[1]
                                vert.co[0] += v_offset*amount
                        else:
                            for vid in selection[0]:
                                vert = copy_ob.data.vertices[vid]
                        
                                v_offset = vert.co[2]
                                vert.co[0] += v_offset*amount
                                
                                
                    elif self.shear_dominant == "Y":

                        if self.shear_subdominant == "X":
                        
                            for vid in selection[0]:
                                vert = copy_ob.data.vertices[vid]
                                v_offset = vert.co[0]
                                vert.co[1] += v_offset*amount
                        else:
                        
                            for vid in selection[0]:
                                vert = copy_ob.data.vertices[vid]
                                v_offset = vert.co[2]
                                vert.co[1] += v_offset*amount
            
                    else:

                        if self.shear_subdominant == "X":
                            for vid in selection[0]:
                                vert = copy_ob.data.vertices[vid]
                                v_offset = vert.co[0]
                                vert.co[2] += v_offset*amount
                        else:
                            for vid in selection[0]:
                                vert = copy_ob.data.vertices[vid]
                                v_offset = vert.co[1]
                                vert.co[2] += v_offset*amount
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            elif self.mode_list == "Project":
            
                if self.projection_modes == "Normal":
            
                    targets = self.inputs[9].returnData()
                    lists = utils_GEN.adjustLists([copy_obs,selections,targets])
                    
                    copy_obs = lists[0]
                    selections = lists[1]
                    targets = lists[2]
                    
                    if self.projection_modes_n == "p":
                        for i in range (0, len(copy_obs)):
                        


                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                            ob = copy_obs[i]
                            tar = targets[i]
                            
                            utils_OBJ.prep_min(ob)
                            utils_OBJ.prep_min(tar)
                            utils_GEOM.project_nor(ob,tar,selection[0],False)
                            utils_OBJ.deprep(ob)
                            utils_OBJ.deprep(tar)
                            
                            tar.name = "_$OBS$_"
                            
                    elif self.projection_modes_n == "n":
                        for i in range (0, len(copy_obs)):
                        


                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                            ob = copy_obs[i]
                            tar = targets[i]
                            
                            utils_OBJ.prep_min(ob)
                            utils_OBJ.prep_min(tar)
                            utils_GEOM.project_nor(ob,tar,selection[0],True)
                            utils_OBJ.deprep(ob)
                            utils_OBJ.deprep(tar)
                            
                            tar.name = "_$OBS$_"
                            
                    else:
                        for i in range (0, len(copy_obs)):
                        


                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                            ob = copy_obs[i]
                            tar = targets[i]
                            
                            utils_OBJ.prep_min(ob)
                            utils_OBJ.prep_min(tar)
                            utils_GEOM.project_nor_shortest(ob,tar,selection[0])
                            utils_OBJ.deprep(ob)
                            utils_OBJ.deprep(tar)
                            
                            tar.name = "_$OBS$_"
            
            
                elif self.projection_modes == "Closest":
            
                    targets = self.inputs[9].returnData()
                    lists = utils_GEN.adjustLists([copy_obs,selections,targets])
                    
                    copy_obs = lists[0]
                    selections = lists[1]
                    targets = lists[2]

                    
                    
                    for i in range (0, len(copy_obs)):
                    


                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                        ob = copy_obs[i]
                        tar = targets[i]
                        
                        utils_OBJ.prep_min(ob)
                        utils_OBJ.prep_min(tar)
                        utils_GEOM.project_closest(ob,tar,selection[0],self.projection_modes_close)
                        utils_OBJ.deprep(ob)
                        utils_OBJ.deprep(tar)
                        
                        tar.name = "_$OBS$_"
                        
                elif self.projection_modes == "Direction":
                    
                    targets = self.inputs[9].returnData()
                    vecs = self.inputs[8].returnData()
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,targets,vecs])
                    
                    copy_obs = lists[0]
                    selections = lists[1]
                    targets = lists[2]
                    vecs = lists[3]
                    
                    if self.projection_modes_d == "p":
                        for i in range (0, len(copy_obs)):
                        


                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                            ob = copy_obs[i]
                            tar = targets[i]
                            vec = vecs[i]
                            
                            utils_OBJ.prep_min(ob)
                            utils_OBJ.prep_min(tar)
                            utils_GEOM.project_vec(ob,tar,selection[0],vec,False)
                            utils_OBJ.deprep(ob)
                            utils_OBJ.deprep(tar)
                            
                            tar.name = "_$OBS$_"
                            
                    elif self.projection_modes_d == "n":
                        for i in range (0, len(copy_obs)):
                        


                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                            ob = copy_obs[i]
                            tar = targets[i]
                            vec = vecs[i]
                            
                            utils_OBJ.prep_min(ob)
                            utils_OBJ.prep_min(tar)
                            utils_GEOM.project_vec(ob,tar,selection[0],vec,True)
                            utils_OBJ.deprep(ob)
                            utils_OBJ.deprep(tar)
                            
                            tar.name = "_$OBS$_"
                            
                    else:
                        for i in range (0, len(copy_obs)):
                        


                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv,True)
                            ob = copy_obs[i]
                            tar = targets[i]
                            vec = vecs[i]
                            
                            utils_OBJ.prep_min(ob)
                            utils_OBJ.prep_min(tar)
                            utils_GEOM.project_vec_shortest(ob,tar,selection[0],vec)
                            utils_OBJ.deprep(ob)
                            utils_OBJ.deprep(tar)
                            
                            tar.name = "_$OBS$_"  
                    
            
            
            
            
                        
            
            
            
            
            
            if self.outputs[0].enabled:
                self.outputs[0].setData(copy_obs)
        
            

            


















































  
        

        
##\brief Mesh operations.
#\detail Operations destroy the integrity of selections, use this node's own selections as a substitute.        
class MESH_OperatorNode(buildingNode):

    bl_idname = 'MESH_OperatorNode'

    bl_label = 'Operator'

    bl_icon = 'NODETREE'
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return

    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self,context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
            
      
        if self.mode_list_last != self.mode_list:
            self.mode_list_last = self.mode_list
            outdated = True
            
        if self.delete_modes_last != self.delete_modes:
            self.delete_modes_last = self.delete_modes
            outdated = True
            
        if self.extrude_modes_2_last != self.extrude_modes_2:
            self.extrude_modes_2_last = self.extrude_modes_2
            outdated = True
           
        if self.tri_quads_last != self.tri_quads:
            self.tri_quads_last = self.tri_quads
            outdated = True
            
        if self.tri_polys_last != self.tri_polys:
            self.tri_polys_last = self.tri_polys
            outdated = True
           
        if self.quads_UV_last != self.quads_UV:
            self.quads_UV_last = self.quads_UV
            outdated = True
            
        if self.quads_VCol_last != self.quads_VCol:
            self.quads_VCol_last = self.quads_VCol
            outdated = True
            
        if self.quads_Sharp_last != self.quads_Sharp:
            self.quads_Sharp_last = self.quads_Sharp
            outdated = True
            
        if self.quads_Mat_last != self.quads_Mat:
            self.quads_Mat_last = self.quads_Mat
            outdated = True
            
        if self.bev_modes_last != self.bev_modes:
            self.bev_modes_last = self.bev_modes
            outdated = True
            
        if self.bev_verts_last != self.bev_verts:
            self.bev_verts_last = self.bev_verts
            outdated = True
            
        if self.ins_bound_last != self.ins_bound:
            self.ins_bound_last = self.ins_bound
            outdated = True
            
        if self.ins_even_offs_last != self.ins_even_offs:
            self.ins_even_offs_last = self.ins_even_offs
            outdated = True
            
        if self.ins_rel_offs_last != self.ins_rel_offs:
            self.ins_rel_offs_last = self.ins_rel_offs
            outdated = True
            
        if self.ins_rail_last != self.ins_rail:
            self.ins_rail_last = self.ins_rail
            outdated = True
            
        if self.ins_indiv_last != self.ins_indiv:
            self.ins_indiv_last = self.ins_indiv
            outdated = True
            
        if self.ins_interp_last != self.ins_interp:
            self.ins_interp_last = self.ins_interp
            outdated = True
            
        if self.ins_merge_last != self.ins_merge:
            self.ins_merge_last = self.ins_merge
            outdated = True
            
        if self.bool_modes_last != self.bool_modes:
            self.bool_modes_last = self.bool_modes
            outdated = True
            
            
        if self.merge_unselected_last != self.merge_unselected:
            self.merge_unselected_last = self.merge_unselected
            outdated = True
            
        if self.merge_collapse_last != self.merge_collapse:
            self.merge_collapse_last = self.merge_collapse
            outdated = True
            
        if self.split_newOBJs_last != self.split_newOBJs:
            self.split_newOBJs_last = self.split_newOBJs
            outdated = True
            
        if self.ngon_modes_last != self.ngon_modes:
            self.ngon_modes_last = self.ngon_modes
            outdated = True
            
        if self.bis_fill_last != self.bis_fill:
            self.bis_fill_last = self.bis_fill
            outdated = True
            
        if self.bis_inner_last != self.bis_inner:
            self.bis_inner_last = self.bis_inner
            outdated = True
            
        if self.bis_outer_last != self.bis_outer:
            self.bis_outer_last = self.bis_outer
            outdated = True
            
        if self.wire_shape_last != self.wire_shape:
            self.wire_shape_last = self.wire_shape
            outdated = True
            
        if self.bool2D_modes_last != self.bool2D_modes:
            self.bool2D_modes_last = self.bool2D_modes
            outdated = True
            
        if self.bool2D_plane_last != self.bool2D_plane:
            self.bool2D_plane_last = self.bool2D_plane
            outdated = True
            
        if self.proj_sub_last != self.proj_sub:
            self.proj_sub_last = self.proj_sub
            outdated = True
            
        if self.proj_type_last != self.proj_type:
            self.proj_type_last = self.proj_type
            outdated = True
            
        if self.split_selmode_last != self.split_selmode:
            self.split_selmode_last = self.split_selmode
            outdated = True
           
        
        if outdated:
            self.updateInputs(context)
            self.callObsolete(context)
    
    
    
    
    
    
    


        
        

    
    
	#NODE DATA
    corrupted = BoolProperty(default = True, update = updateEmpty)
    
    
    
    #data checking
    mode_list_last = StringProperty(default = "",update = updateEmpty)
    delete_modes_last = StringProperty(default = "",update = updateEmpty)
    extrude_modes_2_last = StringProperty(default = "",update = updateEmpty)
    tri_quads_last = StringProperty(default = "",update = updateEmpty)
    tri_polys_last = StringProperty(default = "",update = updateEmpty)
    quads_UV_last = BoolProperty(default = False,update = updateEmpty)
    quads_VCol_last = BoolProperty(default = False,update = updateEmpty)
    quads_Sharp_last = BoolProperty(default = False,update = updateEmpty)
    quads_Mat_last = BoolProperty(default = False,update = updateEmpty)
    bev_modes_last = StringProperty(default = "",update = updateEmpty)
    bev_verts_last = BoolProperty(default = False,update = updateEmpty)
    ins_bound_last = BoolProperty(default = False,update = updateEmpty)
    ins_even_offs_last = BoolProperty(default = False,update = updateEmpty)
    ins_rel_offs_last = BoolProperty(default = False,update = updateEmpty)
    ins_rail_last = BoolProperty(default = False,update = updateEmpty)
    ins_indiv_last = BoolProperty(default = False,update = updateEmpty)
    ins_interp_last = BoolProperty(default = False,update = updateEmpty)
    ins_merge_last = BoolProperty(default = False,update = updateEmpty)
    bool_modes_last = StringProperty(default = "",update = updateEmpty)
    merge_collapse_last = BoolProperty(default = False,update = updateEmpty)
    merge_unselected_last = BoolProperty(default = False,update = updateEmpty)
    split_newOBJs_last = BoolProperty(default = False,update = updateEmpty)
    ngon_modes_last = StringProperty(default = "",update = updateEmpty)
    bis_fill_last = BoolProperty(default = False,update = updateEmpty)
    bis_inner_last = BoolProperty(default = False,update = updateEmpty)
    bis_outer_last = BoolProperty(default = False,update = updateEmpty)
    wire_shape_last = StringProperty(default = "",update = updateEmpty)
    bool2D_modes_last = StringProperty(default = "",update = updateEmpty)
    bool2D_plane_last = StringProperty(default = "",update = updateEmpty)
    proj_sub_last = StringProperty(default = "",update = updateEmpty)
    proj_type_last = StringProperty(default = "",update = updateEmpty)
    split_selmode_last = StringProperty(default = "",update = updateEmpty)

    
    
    
    
    
    modes = [("Delete","Delete",""),("Split","Split",""),("Join","Join",""),("Extrude","Extrude",""),("Merge","Merge",""),("Merge Doubles","Merge Doubles",""),("Triangulate","Triangulate",""),("Make Quads","Make Quads",""),("Make NGons","Make NGons",""),("Bevel","Bevel",""),("Fill","Fill",""),("Inset","Inset",""),("Skeleton","Skeleton",""),("Subdivide","Subdivide",""),("Boolean","Boolean",""),("2D Boolean","2D Boolean",""),("Solidify","Solidify",""),("Bisect","Bisect",""),("Wireframe","Wireframe","")]
    selection = [("Vertices","Vertices",""),("Edges","Edges",""),("Faces","Faces",""),("Only Edges","Only Edges/Faces",""),("Only Faces","Only Faces","")]
    extrusion_m = [("Vertices","Vertices",""),("Edges","Edges",""),("Faces","Faces",""),("Faces (Individual)","Faces (Individual)","")]
    tri_q = [("Beauty","Beauty",""),("Fixed","Fixed",""),("Fixed Alternate","Fixed Alternate",""),("Shortest Diagonal","Shortest Diagonal","")]
    tri_p = [("Beauty","Beauty",""),("Clip","Clip","")]
    bevel_m = [("Offset","Offset",""),("Width","Width",""),("Depth","Depth",""),("Percent","Percent","")]
    subd_m = [("Inner Vert","Inner Vert",""),("Path","Path",""),("Straight Cut","Straight Cut",""),("Fan","Fan","")]
    bool_m = [("Intersect","Intersect",""),("Union","Union",""),("Difference","Difference","")]
    ngon_m = [("Single NGon", "Single NGon", ""),("Angle","Angle","")]
    wire_m = [("Diamond","Diamond",""),("Square","Square","")]
    bool2d_plane = [("Normal","Normal",""),("Vector","Direction",""),("X","X",""),("Y","Y",""),("Z","Z","")]
    
    pro_s = [("c","Cut",""),("m","Merge","")]
    pro_t = [("n","Normal",""),("d","Direction",""),("a","Avg. Normal","")]
    
    sel_m = [("VERT","Vertices",""),("EDGE","Edges",""),("FACE","Faces","")]
    
    
    mode_list = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Flatten Modes",
        update = updateNode
    )
    
    delete_modes = EnumProperty(
        name = "Choose Mode",
        items = selection,
        description = "Delete Modes",
        update = updateNode
    )
    
    extrude_modes_2 = EnumProperty(
        name = "Choose Mode",
        items = extrusion_m,
        description = "Extrusion Modes 2",
        update = updateNode
    )
    
    tri_quads = EnumProperty(
        name = "Choose Mode",
        items = tri_q,
        description = "Quad Triangulation Method",
        update = updateNode
    )
    
    tri_polys = EnumProperty(
        name = "Choose Mode",
        items = tri_p,
        description = "Poly Triangulation Method",
        update = updateNode
    )
    
    quads_UV = BoolProperty(
        name = "Comare UVs",
        default = False,
        update = updateNode
    )
    
    quads_VCol = BoolProperty(
        name = "Comare Vertex Colors",
        default = False,
        update = updateNode
    )
    
    quads_Sharp = BoolProperty(
        name = "Comare Sharpness",
        default = False,
        update = updateNode
    )
    
    quads_Mat = BoolProperty(
        name = "Comare Materials",
        default = False,
        update = updateNode
    )
    
    bev_modes = EnumProperty(
        name = "Choose Mode",
        items = bevel_m,
        description = "Bevel Method",
        update = updateNode
    )
    
    bev_verts = BoolProperty(
        name = "Bevel Vertices",
        default = False,
        update = updateNode
    )
    
    ins_bound = BoolProperty(
        name = "Use Boundary",
        default = False,
        update = updateNode
    )
    
    ins_even_offs = BoolProperty(
        name = "Even Offset",
        default = True,
        update = updateNode
    )
    
    ins_rel_offs = BoolProperty(
        name = "Relative Offset",
        default = False,
        update = updateNode
    )
    
    ins_rail = BoolProperty(
        name = "Use Edge Rail",
        default = True,
        update = updateNode
    )
    
    ins_indiv = BoolProperty(
        name = "Inset individual faces",
        default = False,
        update = updateNode
    )
    
    ins_interp = BoolProperty(
        name = "Interpolate across inset faces",
        default = True,
        update = updateNode
    )
    
    ins_merge = BoolProperty(
        name = "Merge Center Faces",
        default = False,
        update = updateNode
    )
    
    subd_qt = BoolProperty(
        name = "Quad/Tri Mode",
        default = False,
        update = updateNode
    )
    
    subd_corner = EnumProperty(
        name = "Choose Mode",
        items = subd_m,
        description = "Cutting Method",
        update = updateNode
    )
    
    bool_modes = EnumProperty(
        name = "Choose Mode",
        items = bool_m,
        description = "Boolean Modes",
        update = updateNode
    )
    
    bool2D_modes = EnumProperty(
        name = "Choose Mode",
        items = bool_m,
        description = "Boolean Modes",
        update = updateNode
    )
    
    bool2D_plane = EnumProperty(
        name = "Choose Mode",
        items = bool2d_plane,
        description = "Boolean Modes",
        update = updateNode
    )

    merge_unselected = BoolProperty(
        name = "Merge with unselected vertices",
        default = False,
        update = updateNode
    )
    
    merge_collapse = BoolProperty(
        name = "Merge individual areas",
        default = False,
        update = updateNode
    )
    
    split_newOBJs = BoolProperty(
        name = "Move split geometry into new objects",
        default = False,
        update = updateNode
    )
    
    ngon_modes = EnumProperty(
        name = "Choose Mode",
        items = ngon_m,
        description = "NGonize Modes",
        update = updateNode
    )
    
    bis_fill = BoolProperty(
        name = "Fill the cut area",
        default = False,
        update = updateNode
    )
    
    bis_inner = BoolProperty(
        name = "Delete inner part of cut",
        default = False,
        update = updateNode
    )
    
    bis_outer = BoolProperty(
        name = "Delete outer part of cut",
        default = False,
        update = updateNode
    )
    
    wire_shape = EnumProperty(
        name = "Choose Mode",
        items = wire_m,
        description = "Wireframe Shape",
        update = updateNode
    )
    
    proj_sub = EnumProperty(
        name = "Choose Mode",
        items = pro_s,
        description = "Projection Mode",
        update = updateNode
    )
    
    proj_type = EnumProperty(
        name = "Choose Mode",
        items = pro_t,
        description = "Projection Submode",
        update = updateNode
    )
    
    split_selmode = EnumProperty(
        name = "Choose Mode",
        items = sel_m,
        description = "Selection Mode",
        update = updateNode
    )

    
    
    
    
    
    
    

    
    
    
    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
    
        #make all inputs visible
        for input in self.inputs:
            input.enabled = True
    
        #hide all but standard inputs + outputs
        for input in self.inputs:
            if input.name != "Mesh" and input.name != "Selection":
                input.enabled = False
                
        for output in self.outputs:
            if output.name != "Mesh":
                output.enabled = False

        #make mode-specific inputs visible
        if len(self.inputs) == 18 and len(self.outputs) == 3:
        
            if self.mode_list == "Extrude":
                
                self.outputs[1].enabled = True
    
            elif self.mode_list == "Merge":
                self.outputs[1].enabled = True
    
            elif self.mode_list == "Merge Doubles":
                self.outputs[1].enabled = True
                self.inputs[2].enabled = True
        
            elif self.mode_list == "Triangulate":
                self.outputs[1].enabled = True
            
            elif self.mode_list == "Make Quads":
                self.inputs[3].enabled = True
                self.outputs[1].enabled = True
                
            
            elif self.mode_list == "Make NGons":
                self.outputs[1].enabled = True
                if self.ngon_modes == "Angle":
                    self.inputs[11].enabled = True
            
            
            elif self.mode_list == "Bevel":
                self.inputs[4].enabled = True
                self.inputs[5].enabled = True
                self.inputs[6].enabled = True
                self.outputs[1].enabled = True
            
            elif self.mode_list == "Fill":
                self.outputs[1].enabled = True
            
            elif self.mode_list == "Inset":
                self.inputs[7].enabled = True
                self.outputs[1].enabled = True
                
            elif self.mode_list == "Skeleton":
                self.outputs[1].enabled = True
            
            elif self.mode_list == "Subdivide":
                self.inputs[8].enabled = True
                self.inputs[9].enabled = True
                self.outputs[1].enabled = True
                
            elif self.mode_list == "Boolean":
                self.inputs[10].enabled = True
                self.inputs[1].enabled = False
                
            elif self.mode_list == "Split" and self.split_newOBJs:
                self.outputs[2].enabled = True
                self.outputs[1].enabled = False
                
            elif self.mode_list == "Solidify":
                self.inputs[12].enabled = True
                self.outputs[1].enabled = True
                
            elif self.mode_list == "Bisect":
                self.inputs[13].enabled = True
                self.inputs[14].enabled = True
                self.outputs[1].enabled = True
                
            elif self.mode_list == "Wireframe":
                self.inputs[15].enabled = True
                self.inputs[1].enabled = False
                
            elif self.mode_list == "2D Boolean":
                self.inputs[16].enabled = True
                self.inputs[1].enabled = False
                if self.bool2D_plane == "Vector":
                    self.inputs[17].enabled = True
                    
            elif self.mode_list == "Projection":
                self.inputs[10].enabled = True
                if self.proj_type == "d":
                    self.inputs[17].enabled = True
                    
            elif self.mode_list == "Join":
                self.inputs[10].enabled = True
                self.inputs[1].enabled = False
                    
                
            
        
    ##\brief Initializes the node.
    def init(self, context):
        
        #Generic Outputs
        self.inputs.new("socket_MESH", "Mesh")
        self.inputs.new("socket_SELECTION", "Selection")
        
        socket = self.outputs.new("socket_MESH", "Mesh")
        
        
        
        #Extrusion Inputs
        
        #Extrusion Outputs
        socket = self.outputs.new("socket_SELECTION","Selection")
        socket.enabled = False
        
        
        
        #Merge Doubles Inputs
        socket = self.inputs.new("socket_FLOAT","Threshold")
        socket.enabled = False
        
        
        #Make Quads Inputs
        socket = self.inputs.new("socket_FLOAT","Angle")
        socket.enabled = False
        
        
        
        #Bevel Inputs
        socket = self.inputs.new("socket_FLOAT", "Amount")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT","Segments")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT","Profile")
        socket.enabled = False

        
        
        #Inset Inputs
        socket = self.inputs.new("socket_FLOAT", "Amount")
        socket.enabled = False
        
        #Subd. Inputs
        socket = self.inputs.new("socket_INT", "Cuts")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT", "Smooth")
        socket.enabled = False

        #Bool Inputs
        socket = self.inputs.new("socket_MESH", "Target")
        socket.enabled = False
        
        #Split Output
        socket = self.outputs.new("socket_MESH", "Split")
        socket.enabled = False
        
        
        #Make NGons Inputs
        socket = self.inputs.new("socket_FLOAT","Angle")
        socket.enabled = False
        
        #Solidify Inputs
        socket = self.inputs.new("socket_FLOAT","Amount")
        socket.enabled = False
        
        #Bisect Inputs
        socket = self.inputs.new("socket_VEC3_F","Position")
        socket.enabled = False
        socket = self.inputs.new("socket_VEC3_F","Normal")
        socket.enabled = False
        
        #Wireframe Inputs
        socket = self.inputs.new("socket_FLOAT","Amount")
        socket.enabled = False
        
        #2D Boolean Inputs
        socket = self.inputs.new("socket_MESH", "Mesh 2")
        socket.enabled = False
        socket = self.inputs.new("socket_VEC3_F", "Direction")
        socket.enabled = False
        

        
        self.use_custom_color = True
        self.color = (1,.8,.5)
        
        
        self.update()
        
        
    ##\brief GUI.     
    def draw_buttons(self, context, layout):
        
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "mode_list", "")
        
        if self.mode_list == "Delete":
            rowD = layout.row(align = True)
            rowD.prop(self, "delete_modes", "")
            
            
        elif self.mode_list == "Extrude":
            row2 = layout.row(align = True)
            
            row2.prop(self, "extrude_modes_2", "")
        
        elif self.mode_list == "Merge":
            rowN = layout.row(align = True)
            rowN.prop(self, "merge_collapse", "Individual")
        
        elif self.mode_list == "Merge Doubles":
            row2 = layout.row()
            row2.prop(self, "merge_unselected", "Unselected")
        
        elif self.mode_list == "Triangulate":
            row1 = layout.row(align = True)
            row2 = layout.row(align = True)
            row3 = layout.row(align = True)
            row4 = layout.row(align = True)
            
            row1.label(text = "Quad Method:")
            row2.prop(self, "tri_quads", "")
            row3.label(text = "Polygon Method:")
            row4.prop(self, "tri_polys", "")
            
        elif self.mode_list == "Make Quads":
            layout.separator()
            layout.prop(self, "quads_UV", "UVs")
            layout.prop(self, "quads_VCol", "VColor")
            layout.prop(self, "quads_Sharp", "Sharpness")
            layout.prop(self, "quads_Mat", "Material")
            
        elif self.mode_list == "Make NGons":
            layout.separator()
            row = layout.row()
            row.prop(self,"ngon_modes","")
          
        elif self.mode_list == "Bevel":
            layout.separator()
            layout.prop(self, "bev_modes", "")
            layout.prop(self, "bev_verts", "Vertices Only")
            
        elif self.mode_list == "Inset":
            layout.separator()
            layout.prop(self, "ins_merge", "Merge Center")
            layout.prop(self, "ins_bound", "Open Edges")
            layout.prop(self, "ins_rel_offs", "Relat. Offset")
            layout.prop(self, "ins_indiv", "Individual")

        
        elif self.mode_list == "Subdivide":
            layout.separator()
            layout.prop(self, "subd_qt", "Quad/Tri Mode")
            if self.subd_qt:
                layout.prop(self, "subd_corner", "Cut")
                
        elif self.mode_list == "Boolean":
            layout.separator()
            layout.prop(self, "bool_modes", "")
                
        elif self.mode_list == "Split":
            layout.separator()
            layout.row().prop(self,"split_selmode","Select")
            layout.row().prop(self, "split_newOBJs", "Separate")
            
        elif self.mode_list == "Bisect":
            layout.separator()
            row1 = layout.row()
            row2 = layout.row()
            row3 = layout.row()
            
            row1.prop(self,"bis_fill","Fill")
            row2.prop(self,"bis_inner","Del. Inside")
            row3.prop(self,"bis_outer","Del. Outside")
            
        elif self.mode_list == "Wireframe":
            layout.separator()
            layout.prop(self,"wire_shape","Shape:")
            
        elif self.mode_list == "2D Boolean":
            layout.separator()
            layout.prop(self, "bool2D_modes", "")
            layout.prop(self, "bool2D_plane", "Proj.")
            
        elif self.mode_list == "Projection":
            layout.separator()
            layout.prop(self,"proj_sub","")
            layout.prop(self,"proj_type","")
            
            
                

            
            
            
        
        layout.separator()    
            
        
        
        
        
        
        
        
        
        
        
    ##\brief Re-calculates the node's data.     
    def recalculate(self):
        
        self.corrupted = False

        current_SELs = []
        current_OBJs_secondary = []
        
        if len(self.inputs[0].links) > 0:
            
            selections = []
            copy_obs = self.inputs[0].returnData()
            
            
            
            #Selections
            selections = self.inputs[1].returnData()
   
            if self.mode_list == "Delete":
            
            
                lists = utils_GEN.adjustLists([copy_obs,selections])
                
                copy_obs = lists[0]
                selections = lists[1]

            
                if self.delete_modes == "Vertices":
                
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                        utils_OBJ.prep(copy_ob, selection, "VERT")
                        utils_GEOM.delete("VERT")
                        utils_OBJ.deprep(copy_ob)
                        
                    
                elif self.delete_modes == "Edges":

                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                        utils_OBJ.prep(copy_ob, selection, "EDGE")
                        utils_GEOM.delete("EDGE")
                        utils_OBJ.deprep(copy_ob)
                        
                    
                elif self.delete_modes == "Faces":
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                        utils_OBJ.prep(copy_ob, selection, "FACE")
                        utils_GEOM.delete("FACE")
                        utils_OBJ.deprep(copy_ob)
                        
                
                elif self.delete_modes == "Only Edges":
                
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                        utils_OBJ.prep(copy_ob, selection, "EDGE")
                        utils_GEOM.delete("EDGE_FACE")
                        utils_OBJ.deprep(copy_ob)
                        
                    
                    
                elif self.delete_modes == "Only Faces":
                
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                        utils_OBJ.prep(copy_ob, selection, "FACE")
                        utils_GEOM.delete("ONLY_FACE")
                        utils_OBJ.deprep(copy_ob)
                        
                
                
                
                
                
                
          
            #EXTRUDE:
                    
          
            
            elif self.mode_list == "Extrude":
            
                lists = utils_GEN.adjustLists([copy_obs,selections])
                
                copy_obs = lists[0]
                selections = lists[1]
            
                if self.extrude_modes_2 == "Vertices":

                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                        utils_OBJ.prep(copy_ob, selection, "VERT")
                        utils_GEOM.extrudeV()
                        utils_OBJ.deprep(copy_ob)
                        

                    
                    
                    
                    
                    
                    
                elif self.extrude_modes_2 == "Edges":
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                        utils_OBJ.prep(copy_ob, selection, "EDGE")
                        utils_GEOM.extrudeE()
                        utils_OBJ.deprep(copy_ob)
                        
                        

                    
                    
                    
                elif self.extrude_modes_2 == "Faces":
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                        utils_OBJ.prep(copy_ob, selection, "FACE")
                        utils_GEOM.extrudeF()
                        utils_OBJ.deprep(copy_ob)
                        
                elif self.extrude_modes_2 == "Faces (Individual)":
                
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                        utils_OBJ.prep(copy_ob, selection, "FACE")
                        utils_GEOM.extrudeF_indiv()
                        utils_OBJ.deprep(copy_ob)
                        
             


             
                
            #MERGE
            
            elif self.mode_list == "Merge":
            
                lists = utils_GEN.adjustLists([copy_obs,selections])
                
                copy_obs = lists[0]
                selections = lists[1]
            
                for i in range(0,len(copy_obs)):
                    
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                    utils_OBJ.prep(copy_ob, selection, "VERT")
                    utils_GEOM.merge(self.merge_collapse)
                    utils_OBJ.deprep(copy_ob)
                        
                    
            
            
            
            
            
            
            
            
            
            
                
                
                
            #MERGE DOUBLES
                
                

            elif self.mode_list == "Merge Doubles":

                thrs = self.inputs[2].returnData()
                
                #we need non-negative thresholds
                thrs = [math.fabs(x) for x in thrs]
                         


                lists = utils_GEN.adjustLists([copy_obs,selections,thrs])
                
                copy_obs = lists[0]
                selections = lists[1]
                thrs = lists[2]
                         
                 

                for i in range(0,len(copy_obs)):
                    
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    thr = thrs[i]
                        
                        
                    utils_OBJ.prep(copy_ob, selection, "VERT")
                    utils_GEOM.merge_doubles(thr, self.merge_unselected)
                    utils_OBJ.deprep(copy_ob)

 
                
                
                
                
            #TRIANGULATE
            
                
            elif self.mode_list == "Triangulate":
           
                lists = utils_GEN.adjustLists([copy_obs,selections])
                
                copy_obs = lists[0]
                selections = lists[1]
           
           
                qm = ""
                pm = ""
                    
                if self.tri_quads == "Beauty":
                    qm = "BEAUTY"
                elif self.tri_quads == "Fixed":
                    qm = "FIXED"
                elif self.tri_quads == "Fixed Alternate":
                    qm = "FIXED_ALTERNATE"
                elif self.tri_quads == "Shortest Diagonal":
                    qm = "SHORTEST_DIAGONAL"
                        
                if self.tri_polys == "Beauty":
                    pm = "BEAUTY"
                else:
                    pm = "CLIP"

                    
                for i in range(0,len(copy_obs)):
                    
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                    utils_OBJ.prep(copy_ob, selection, "FACE")
                    utils_GEOM.triangulate(qm,pm)
                    utils_OBJ.deprep(copy_ob) 

                    
                        
                
            
            
            #MAKE QUADS
            

            elif self.mode_list == "Make Quads":
                
                lists = utils_GEN.adjustLists([copy_obs,selections])
                
                copy_obs = lists[0]
                selections = lists[1]
            
                for i in range(0,len(copy_obs)):
                    
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                    utils_OBJ.prep(copy_ob, selection, "FACE")
                    utils_GEOM.make_quads(self.quads_UV, self.quads_VCol, self.quads_Sharp, self.quads_Mat)
                    utils_OBJ.deprep(copy_ob)  
            
                
                
                
                
                
                
                
                
                
                
                
            #BEVEL
                
            elif self.mode_list == "Bevel":
                offset_t = ""
                if self.bev_modes == "Offset":
                    offset_t = "OFFSET"
                elif self.bev_modes == "Width":
                    offset_t = "WIDTH"
                elif self.bev_modes == "Depth":
                    offset_t = "DEPTH"
                elif self.bev_modes == "Percent":
                    offset_t = "PERCENT"
                    
                amounts = self.inputs[4].returnData()

                segs = self.inputs[5].returnData()

                    
                prs = self.inputs[6].returnData()
                
                #only non-negative values allowed
                prs = [math.fabs(p) for p in prs]
                

                
                lists = utils_GEN.adjustLists([copy_obs,selections,amounts,segs,prs])
                
                copy_obs = lists[0]
                selections = lists[1]
                amounts = lists[2]
                segs = lists[3]
                prs = lists[4]
                

                
                
                for i in range(0,len(copy_obs)):
                    
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    amount = amounts[i]
                    seg = segs[i]
                    pr = prs[i]
                        
                    utils_OBJ.prep(copy_ob, selection, "EDGE")
                    utils_GEOM.bevel(offset_t,amount,seg,pr,self.bev_verts)
                    utils_OBJ.deprep(copy_ob)  
                    
                    
                    


                    
               

               
               
               
            #FILL
            
            elif self.mode_list == "Fill":
                
                
                lists = utils_GEN.adjustLists([copy_obs,selections])
                
                copy_obs = lists[0]
                selections = lists[1]
                
                
                for i in range(0,len(copy_obs)):
                    
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                    utils_OBJ.prep(copy_ob, selection, "EDGE")
                    utils_GEOM.fill()
                    utils_OBJ.deprep(copy_ob) 
                

                
                
            #INSET

            elif self.mode_list == "Inset":
            
                amounts = self.inputs[7].returnData()
                
                lists = utils_GEN.adjustLists([copy_obs,selections,amounts])
                
                copy_obs = lists[0]
                selections = lists[1]
                amounts = lists[2]
                
                
                for i in range(0,len(copy_obs)):
                    
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    amount = amounts[i]
                    
                    out = False
                    
                    if amount < 0:
                        out = True
                        amount = -amount
                    
                    
                        
                    utils_OBJ.prep(copy_ob, selection, "FACE")
                    utils_GEOM.inset(self.ins_bound,self.ins_rel_offs,amount,out,self.ins_indiv, self.ins_merge)
                    utils_OBJ.deprep(copy_ob)
                    
                    
                    
                    
            #SKELETON

            elif self.mode_list == "Skeleton":
                
                lists = utils_GEN.adjustLists([copy_obs,selections])
                
                copy_obs = lists[0]
                selections = lists[1]
                
                for i in range(0,len(copy_obs)):
                
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                    utils_OBJ.prep(copy_ob, selection, "FACE")
                    #try:
                    utils_GEOM.inset_skeleton()
                    # except:
                        # pass
                    utils_OBJ.deprep(copy_ob)
                
                
                
                
                
                
                
                
            #SUBDIVIDE
                
            elif self.mode_list == "Subdivide":
            
                cuts = self.inputs[8].returnData()
                  
                for cut in cuts:
                    if cut == 0:
                        cut = 1
                
                smooths = self.inputs[9].returnData()
                smooths = [math.fabs(s) for s in smooths]
                    
                    
                qc = ""
                
                if self.subd_corner == "Inner Vert":
                    qc = "INNERVERT"
                elif self.subd_corner == "Path":
                    qc = "PATH"
                elif self.subd_corner == "Straight Cut":
                    qc = "STRAIGHT_CUT"
                elif self.subd_corner == "Fan":
                    qc = "FAN"
                
                    
                lists = utils_GEN.adjustLists([copy_obs,selections,cuts,smooths])
                
                copy_obs = lists[0]
                selections = lists[1]
                cuts = lists[2]
                smooths = lists[3]
                  
                    
                for i in range(0,len(copy_obs)):
                    
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    cut = cuts[i]
                    smooth = smooths[i]

                    utils_OBJ.prep(copy_ob, selection, "EDGE")
                    utils_GEOM.subdiv(cut, smooth, self.subd_qt, qc)
                    utils_OBJ.deprep(copy_ob)
                
                
                
            
            #BOOLEAN
              
            elif self.mode_list == "Boolean":
            
                tar_obs = self.inputs[10].returnData()
                
                lists = utils_GEN.adjustLists([copy_obs,tar_obs])
                
                copy_obs = lists[0]
                tar_obs = lists[1]
                
                for i in range(0,len(copy_obs)):
                
                    copy_ob = copy_obs[i]
                    tar_ob = utils_OBJ.copyobj(tar_obs[i])

                    
                
                    utils_OBJ.prep_all(copy_ob,"FACE")
                    utils_GEOM.bool(copy_ob, tar_ob, self.bool_modes)
                    utils_OBJ.deprep(copy_ob)

            
            
            
            #SPLIT
            
            elif self.mode_list == "Split":
                
                if not self.split_newOBJs:
                    
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)

                        utils_OBJ.prep(copy_ob, selection, "VERT")
                        utils_GEOM.split(copy_ob,False)
                        utils_OBJ.deprep(copy_ob)
                    
                    
                    
                    
                else:

                    current_OBJs_secondary = []
                    
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)

                        utils_OBJ.prep(copy_ob, selection, self.split_selmode)
                        splitob = utils_GEOM.split(copy_ob,True)
                        
                        utils_OBJ.deprep(splitob)
                        utils_OBJ.deprep(copy_ob)
                        
                        current_OBJs_secondary.append(splitob)


                        
                        
                        
            #NGONIZE

            elif self.mode_list == "Make NGons":
            
                
                if self.ngon_modes == "Single NGon":
                
                    lists = utils_GEN.adjustLists([copy_obs,selections])
                
                    copy_obs = lists[0]
                    selections = lists[1]
                
                    for i in range(0,len(copy_obs)):
                
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)

                        utils_OBJ.prep(copy_ob, selection, "FACE")
                        utils_GEOM.ngonize(copy_ob)
                        utils_OBJ.deprep(copy_ob)
                        
                else:
                
                    vals = self.inputs[11].returnData()
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,vals])
                
                    copy_obs = lists[0]
                    selections = lists[1]
                    vals = lists[2]
                    
                    for i in range(0,len(copy_obs)):
                
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        val = vals[i]

                        utils_OBJ.prep(copy_ob, selection, "EDGE")
                        utils_GEOM.ngonize_angle(copy_ob,val)
                        utils_OBJ.deprep(copy_ob)
                        
                



            #SOLIDIFY
                        
            elif self.mode_list == "Solidify":
            
                amounts = self.inputs[12].returnData()
            
                
                lists = utils_GEN.adjustLists([copy_obs,selections,amounts])
                
                copy_obs = lists[0]
                selections = lists[1]
                amounts = lists[2]

                
                for i in range(0,len(copy_obs)):
                
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    amount = amounts[i]

                    utils_OBJ.prep(copy_ob, selection, "FACE")
                    utils_GEOM.solidify(copy_ob,amount)
                    utils_OBJ.deprep(copy_ob)
                    
             



            #BISECT
                    
            elif self.mode_list == "Bisect":
                
                positions = self.inputs[13].returnData()
                normals = self.inputs[14].returnData()
                
                lists = utils_GEN.adjustLists([copy_obs,selections,positions,normals])

                copy_obs = lists[0]
                selections = lists[1]
                positions = lists[2]
                normals = lists[3]
                
                for i in range(0,len(copy_obs)):
                
                    copy_ob = copy_obs[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    pos = positions[i]
                    nor = normals[i]

                    utils_OBJ.prep(copy_ob, selection, "VERT")
                    utils_GEOM.bisect(copy_ob,pos,nor,self.bis_fill,self.bis_inner,self.bis_outer)
                    utils_OBJ.deprep(copy_ob)
                    
             


            #WIREFRAME
            
            elif self.mode_list == "Wireframe":
                
                thicknesses = self.inputs[15].returnData()
                
                lists = utils_GEN.adjustLists([copy_obs,selections,thicknesses])

                copy_obs = lists[0]
                selections = lists[1]
                thicknesses = lists[2]
                
                
                if self.wire_shape == "Diamond":

                
                    for i in range(0,len(copy_obs)):
                
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        th = thicknesses[i]

                        utils_OBJ.prep(copy_ob, selection, "EDGE")
                        utils_GEOM.wireframe_diamond(copy_ob,th)
                        utils_OBJ.deprep(copy_ob)
                        
                if self.wire_shape == "Square":
                
                    for i in range(0,len(copy_obs)):
                
                        copy_ob = copy_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        th = thicknesses[i]

                        utils_OBJ.prep(copy_ob,selection,"EDGE")
                        
                        utils_GEOM.wireframe_square(copy_ob,th)
                    
                        utils_OBJ.deprep(copy_ob)
                        
             


            #2D BOOLEAN
                        
            elif self.mode_list == "2D Boolean":
            
            
                mode = self.bool2D_modes.upper()
            
                
                if self.bool2D_plane == "Vector":
                    
                    tar = self.inputs[16].returnData()
                    
                    targets = []
                    
                    for ob2 in tar:
                        targets.append(utils_OBJ.copyobj(ob2))
                    
                    vectors = self.inputs[17].returnData()
                
                    lists = utils_GEN.adjustLists([copy_obs,targets,vectors])

                    copy_obs = lists[0]
                    targets = lists[1]
                    vectors = lists[2]
                    
                    for i in range(0,len(copy_obs)):
                
                        copy_ob = copy_obs[i]
                        tar_ob = targets[i]
                        vec = vectors[i]
                        
                        
                        utils_OBJ.prep_all(tar_ob, "VERT")
                        utils_OBJ.prep_all(copy_ob, "VERT")
                        
                        
                        
                        utils_GEOM.bool_2D(copy_ob,tar_ob,mode,"V",vec)
                        utils_OBJ.deprep(copy_ob)
                        utils_OBJ.deprep(tar_ob)
                        
                    for ob2 in targets:
                        ob2.name = "_$OBS$_"
                        
                        
                        
                else:
                
                
                    mode2 = self.bool2D_plane
                    
                    if mode2 == "Normal":
                        mode2 = "N"
                    
                    
                    
                    
                    tar = self.inputs[16].returnData()
                    
                    targets = []
                    
                    for ob2 in tar:
                        targets.append(utils_OBJ.copyobj(ob2))
                    

                
                    lists = utils_GEN.adjustLists([copy_obs,targets])

                    copy_obs = lists[0]
                    targets = lists[1]

                    
                    for i in range(0,len(copy_obs)):
                
                        copy_ob = copy_obs[i]
                        tar_ob = targets[i]

                        
                        
                        utils_OBJ.prep_all(tar_ob, "VERT")
                        utils_OBJ.prep_all(copy_ob, "VERT")
                        
                        
                        
                        utils_GEOM.bool_2D(copy_ob,tar_ob,mode,mode2)
                        utils_OBJ.deprep(copy_ob)
                        utils_OBJ.deprep(tar_ob)
                        
                    for ob2 in targets:
                        ob2.name = "_$OBS$_"
                        
                    
                    
                    
            #PROJECTION
                        
            elif self.mode_list == "Projection": 
            
                if self.proj_sub == "m":
            
                    tar_obs = self.inputs[10].returnData()
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,tar_obs])
                    
                    copy_obs = lists[0]
                    selection = lists[1]
                    tar_obs = lists[2]
                    
                    for i in range(0,len(copy_obs)):
                    
                        copy_ob = copy_obs[i]
                        tar_ob = utils_OBJ.copyobj(tar_obs[i])
                        selection = utils_SEL.mapSelection(selections[i], copy_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)

                       
                        utils_OBJ.prep(copy_ob,selection,"FACE")
                        utils_OBJ.prep_min(tar_ob)
                        utils_GEOM.project_merge(copy_ob, tar_ob, self.proj_type)
                        utils_OBJ.deprep(copy_ob)
                        
                        
                        
            #JOIN
              
            elif self.mode_list == "Join":
            
                tar_obs = self.inputs[10].returnData()
                
                lists = utils_GEN.adjustLists([copy_obs,tar_obs])
                
                copy_obs = lists[0]
                tar_obs = lists[1]
                
                for i in range(0,len(copy_obs)):
                
                    copy_ob = copy_obs[i]
                    tar_ob = utils_OBJ.copyobj(tar_obs[i])

                    
                
                    utils_OBJ.prep_all(copy_ob,"FACE")
                    utils_OBJ.prep_all(tar_ob,"FACE")
                    utils_GEOM.join(copy_ob, tar_ob)
                    utils_OBJ.deprep(copy_ob)
                
                
                
                    









            
                
            

            
            
            #calculate selections
              
            current_SELs = []
                    
            for ob in copy_obs:
                
                sel_v_top = []
                sel_e_top = []
                sel_f_top = []
                    
                for vert in ob.data.vertices:
                    if vert.select == True:
                        sel_v_top.append(vert.index)
                                
                for edge in ob.data.edges:
                    if edge.select == True:
                        sel_e_top.append(edge.index)
                                
                for face in ob.data.polygons:
                    if face.select == True:
                        sel_f_top.append(face.index)
                        
                sel = [sel_v_top,sel_e_top,sel_f_top]
                                
                current_SELs.append(sel)
                
             

            if self.outputs[0].enabled:
                self.outputs[0].setData(copy_obs)
            if self.outputs[1].enabled:
                self.outputs[1].setData(current_SELs)
            if self.outputs[2].enabled:
                self.outputs[2].setData(current_OBJs_secondary)




            
                



















































 
##\brief Extracts data from a mesh.
#\detail Highest/lowest points, vert/edge/face counts, etc.      
class MESH_ExtractNode(buildingNode):

    bl_idname = 'MESH_ExtractNode'

    bl_label = 'Data'

    bl_icon = 'NODETREE'
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    
   
    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
        outdated = False
        
        #CHECK CONNECTIONS
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
                
                
                
                
        #CHECK ALL PARAMETERS
        if self.modes_l != self.modes:
            self.modes_l = self.modes
            outdated = True
            
        if self.extrema_m_l != self.extrema_m:
            self.extrema_m_l = self.extrema_m
            outdated = True
            
        if self.extrema_data_l != self.extrema_data:
            self.extrema_data_l = self.extrema_data
            outdated = True
            
        if self.pos_axes_l != self.pos_axes:
            self.pos_axes_l = self.pos_axes
            outdated = True
            
        if self.dis_axes_l != self.dis_axes:
            self.dis_axes_l = self.dis_axes
            outdated = True
            
        if self.ang_axes_l != self.ang_axes:
            self.ang_axes_l = self.ang_axes
            outdated = True
            
        if self.count_mode_l != self.count_mode:
            self.count_mode_l != self.count_mode
            outdated = True
            
        
            
            
                
        if outdated:
            self.updateInputs(context)
            self.callObsolete(context)
        
    
    
    
    
    
    
    
    #NODE DATA
    
    corrupted = BoolProperty(default = True, update = updateEmpty)
    
    modes_l = StringProperty(default = "",update = updateEmpty)
    extrema_m_l = StringProperty(default = "",update = updateEmpty)
    extrema_data_l = StringProperty(default = "",update = updateEmpty)
    pos_axes_l = StringProperty(default = "",update = updateEmpty)
    dis_axes_l = StringProperty(default = "",update = updateEmpty)
    ang_axes_l = StringProperty(default = "",update = updateEmpty)
    count_mode_l = StringProperty(default = "",update = updateEmpty)
    
    
    
    current_COUNTS = []
    current_VALS = []
    current_VEC3 = []
    
    
    
    
    
    
    
    
    
    

    ex_modes = [("Extrema","Extrema",""),("Count","Count","")]
    ext_modes = [("Highest","Highest",""),("Lowest","Lowest",""),("Average","Average",""),("Median","Median","")]
    axes = [("All","All",""),("X","X",""),("Y","Y",""),("Z","Z","")]
    axes_strict = [("X","X",""),("Y","Y",""),("Z","Z","")]
    ext_data_modes = [("Position","Position",""),("Avg. Normal","Avg. Normal",""),("Distance","Distance",""),("Size","Size",""), ("Angle","Angle","")]
    meshdata = [("Vertices","Vertices",""),("Edges","Edges",""),("Faces","Faces","")]
    meshdata_EF = [("Edges","Edges",""),("Faces","Faces","")]
    
    
    modes = EnumProperty(
        name = "Choose Mode",
        items = ex_modes,
        description = "Modes",
        update = updateNode
    
    )
    
    extrema_m = EnumProperty(
        name = "Choose Mode",
        items = ext_modes,
        description = "Extrema Modes",
        update = updateNode
    
    )
    
    extrema_data = EnumProperty(
        name = "Choose Mode",
        items = ext_data_modes,
        description = "Modes",
        update = updateNode
    
    )
    
    pos_axes = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        description = "Axis Modes",
        update = updateNode
    
    )
    
    pos_mode = EnumProperty(
        name = "Choose Mode",
        items = meshdata,
        description = "Count Modes",
        update = updateNode
    
    )
    
    
    dis_axes = EnumProperty(
        name = "Choose Mode",
        items = axes,
        description = "Axis Modes",
        update = updateNode
    
    )
    
    dis_mode = EnumProperty(
        name = "Choose Mode",
        items = meshdata,
        description = "Count Modes",
        update = updateNode
    
    )
    
    siz_mode = EnumProperty(
        name = "Choose Mode",
        items = meshdata_EF,
        description = "Count Modes",
        update = updateNode
    
    )
    
    ang_axes = EnumProperty(
        name = "Choose Mode",
        items = axes,
        description = "Axis Modes",
        update = updateNode
    
    )
    
    ang_mode = EnumProperty(
        name = "Choose Mode",
        items = meshdata,
        description = "Count Modes",
        update = updateNode
    
    )
    
    count_mode = EnumProperty(
        name = "Choose Mode",
        items = meshdata,
        description = "Count Modes",
        update = updateNode
    
    )
    
    nor_mode = EnumProperty(
        name = "Choose Mode",
        items = meshdata,
        description = "Count Modes",
        update = updateNode
    
    )
    
    
    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
    
        #disconnect all inputs except Mesh
    
        #hide all outputs + inputs
        for output in self.outputs:
            output.enabled = False
        for input in self.inputs:
            if input.name != "Mesh" and input.name != "Selection":
                input.enabled = False

        
        if len(self.inputs) == 4 and len(self.outputs) == 3:
            #unhide select outputs
            if self.modes == "Count":
                self.outputs[0].enabled = True
            else:
                if self.extrema_data == "Position":
                    self.outputs[1].enabled = True
                elif self.extrema_data == "Distance":
                    self.inputs[2].enabled = True
                    self.outputs[1].enabled = True
                elif self.extrema_data == "Size":
                    self.outputs[1].enabled = True
                elif self.extrema_data == "Avg. Normal":
                    self.outputs[2].enabled = True
                elif self.extrema_data == "Angle":
                    self.inputs[3].enabled = True
                    self.outputs[1].enabled = True
            
    
    
    

                    
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_MESH","Mesh")
        self.inputs.new("socket_SELECTION","Selection")
        socket = self.inputs.new("socket_VEC3_F", "Pivot")
        socket.enabled = False
        socket = self.inputs.new("socket_VEC3_F", "Direction")
        socket.enabled = False
        
        
        #Count
        socket = self.outputs.new("socket_FLOAT","Value")
        socket.enabled = False
        
        
        #Extrema, Single Axis
        socket = self.outputs.new("socket_FLOAT","Value")
        
        
        #Extrema, Multi Axis
        socket = self.outputs.new("socket_VEC3_F", "Vec3")
        socket.enabled = False
        
        
        self.use_custom_color = True
        self.color = (1,.8,.5)
        
        self.update()

    ##\brief GUI.        
    def draw_buttons(self, context, layout):
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "modes", "")
        if self.modes == "Extrema":
            rowD = layout.row(align = True)
            rowD.prop(self, "extrema_data", "")
            
            rowP = layout.row(align = True)
            
            if self.extrema_data != "Avg. Normal":
                rowM2 = layout.row(align = True)
                rowM2.prop(self, "extrema_m", "")
            
            if self.extrema_data == "Position":
                rowP.prop(self, "pos_axes", "Axis")
                row2 = layout.row(align = True)
                row2.prop(self, "pos_mode", "")
                
            elif self.extrema_data == "Distance":
                rowP.prop(self, "dis_axes", "Axis")
                row2 = layout.row(align = True)
                row2.prop(self, "dis_mode", "")
                
            elif self.extrema_data == "Size":
                rowP.prop(self, "siz_mode", "")
                
            elif self.extrema_data == "Angle":
                
                rowP.prop(self, "ang_mode", "")
                rowP2 = layout.row()
                rowP2.prop(self, "ang_axes", "Axis")
                
        elif self.modes == "Count":
            rowC = layout.row(align = True)
            rowC.prop(self, "count_mode", "")
                
        layout.separator()
            
            
    ##\brief Re-calculates the node's data.        
    def recalculate(self):
        self.corrupted = False
        
        current_COUNTS = []
        current_VEC3 = []
        current_VALS = []
        
        
        if len(self.inputs[0].links) > 0:
            
            selections = []

            source_obs = self.inputs[0].returnData()

            
            
            selections = self.inputs[1].returnData()
                        
            
            
            if selections == [None]:
                selections = []
                for ob in source_obs:
                    
                    sel_v = [v.index for v in ob.data.vertices]
                    sel_e = [e.index for e in ob.data.edges]
                    sel_f = [f.index for f in ob.data.polygons]
                    selection = [sel_v,sel_e,sel_f]
                    selections.append(selection)
            
            
             

            selections = utils_GEN.adjustListsCut([source_obs,selections])[1]
                
                        
            
            if self.modes == "Count":
                if self.count_mode == "Vertices":
                
                    for i in range(0,len(source_obs)):
                        
                        source_ob = source_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], source_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                        current_COUNTS.append(len(selection[0]))
                    
                elif self.count_mode == "Edges":
                    for i in range(0,len(source_obs)):
                        
                        source_ob = source_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], source_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                        current_COUNTS.append(len(selection[1]))
                    
                else:
                    for i in range(0,len(source_obs)):
                    
                        source_ob = source_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], source_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                
                        current_COUNTS.append(len(selection[2]))
                
            else:
            
                if self.extrema_data == "Avg. Normal":
                
                    for i in range(0,len(source_obs)):
                    
                        source_ob = source_obs[i]
                        selection = utils_SEL.mapSelection(selections[i], source_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    
                        normals = []
                        if self.nor_mode == "Vertices":
                            for vid in selection[0]:
                                normals.append(source_ob.data.vertices[vid].normal)
                        elif self.nor_mode == "Edges":
                            for eid in selection[1]:
                                normals.append(utils_GEOM.getEdgeNormal(source_ob, eid))
                        else:
                            for fid in selection[2]:
                                normals.append(source_ob.data.polygons[fid].normal)
                    
                        current_VEC3.append(utils_MATH.getMidCoords(normals))
                    
     
                else:
                    if self.extrema_data == "Position":
                    
                        for i in range(0,len(source_obs)):
                        
                            source_ob = source_obs[i]
                            selection = utils_SEL.mapSelection(selections[i], source_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    
                            vals = []
                            if self.pos_axes == "X":
                                if self.pos_mode == "Vertices":
                                    for vid in selection[0]:
                                        vals.append(source_ob.data.vertices[vid].co[0])
                                elif self.pos_mode == "Edges":
                                    for eid in selection[1]:
                                        vals.append(utils_GEOM.getEdgePos(source_ob, eid)[0])
                                else:
                                    for fid in selection[2]:
                                        vals.append(source_ob.data.polygons[fid].center[0])
                                    
                            elif self.pos_axes == "Y":
                                if self.pos_mode == "Vertices":
                                    for vid in selection[0]:
                                        vals.append(source_ob.data.vertices[vid].co[1])
                                elif self.pos_mode == "Edges":
                                    for eid in selection[1]:
                                        vals.append(utils_GEOM.getEdgePos(source_ob, eid)[1])
                                else:
                                    for fid in selection[2]:
                                        vals.append(source_ob.data.polygons[fid].center[1])   
                    
                            else:
                                if self.pos_mode == "Vertices":
                                    for vid in selection[0]:
                                        vals.append(source_ob.data.vertices[vid].co[2])
                                elif self.pos_mode == "Edges":
                                    for eid in selection[1]:
                                        vals.append(utils_GEOM.getEdgePos(source_ob, eid)[2])
                                else:
                                    for fid in selection[2]:
                                        vals.append(source_ob.data.polygons[fid].center[2])
                        
                            if self.extrema_m == "Highest":
                                current_VALS.append(max(vals))
                            elif self.extrema_m == "Lowest":
                                current_VALS.append(min(vals))
                            elif self.extrema_m == "Average":
                                current_VALS.append(sum(vals) / float(len(vals)))
                            elif self.extrema_m == "Median":
                                current_VALS.append(utils_MATH.getMedian(vals))
                            
                            
                            
                            
                            
                            
                    elif self.extrema_data == "Distance":

                        pivots = self.inputs[2].returnData()
                        
                        pivots = utils_GEN.adjustListsCut([source_obs,pivots])[1]
                        
                        
                        for i in range(0,len(source_obs)):
                        
                            source_ob = source_obs[i]
                            pivot = pivots[i]
                            selection = utils_SEL.mapSelection(selections[i], source_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                            
                    
                            vals = []
                            if self.dis_axes != "All":
                                if self.dis_mode == "Vertices":
                                    for vid in selection[0]:
                                        vals.append(utils_MATH.distanceAxis(source_ob.data.vertices[vid].co, pivot, self.dis_axes))
                                elif self.dis_mode == "Edges":
                                    for eid in selection[1]:
                                        epos = utils_GEOM.getEdgePos(source_ob,eid)
                                        vals.append(utils_MATH.distanceAxis(epos, pivot, self.dis_axes))
                                else:
                                    for fid in selection[2]:
                                        vals.append(utils_MATH.distanceAxis(source_ob.data.polygons[fid].center, pivot, self.dis_axes))
                                    
                            else:
                                if self.dis_mode == "Vertices":
                                    for vid in selection[0]:
                                        vals.append(utils_MATH.distanceEuler(source_ob.data.vertices[vid].co, pivot))
                                elif self.dis_mode == "Edges":
                                    for eid in selection[1]:
                                        epos = utils_GEOM.getEdgePos(source_ob,eid)
                                        vals.append(utils_MATH.distanceEuler(epos, pivot))
                                else:
                                    for fid in selection[2]:
                                        vals.append(utils_MATH.distanceEuler(source_ob.data.polygons[fid].center, pivot))
                                    
                        
                            if self.extrema_m == "Highest":
                                current_VALS.append(max(vals))
                            elif self.extrema_m == "Lowest":
                                current_VALS.append(min(vals))
                            elif self.extrema_m == "Average":
                                current_VALS.append(sum(vals) / float(len(vals)))
                            elif self.extrema_m == "Median":
                                current_VALS.append(utils_MATH.getMedian(vals))
                                
                                
            
                    elif self.extrema_data == "Size":
                    
                    
                    
                        for i in range(0,len(source_obs)):
                        
                            source_ob = source_obs[i]
                            selection = utils_SEL.mapSelection(selections[i], source_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                    
                    
                            vals = []
                            if self.siz_mode == "Edges":
                                for eid in selection[1]:
                                    vals.append(utils_GEOM.getEdgeLength(source_ob,eid))
                            elif self.siz_mode == "Faces":
                                for fid in selection[2]:
                                    vals.append(source_ob.data.polygons[fid].area)
                                
                            if self.extrema_m == "Highest":
                                current_VALS.append(max(vals))
                            elif self.extrema_m == "Lowest":
                                current_VALS.append(min(vals))
                            elif self.extrema_m == "Average":
                                current_VALS.append(sum(vals) / float(len(vals)))
                            elif self.extrema_m == "Median":
                                current_VALS.append(utils_MATH.getMedian(vals))
            
                    
                    
                    
                    elif self.extrema_data == "Angle":
                    
                        dirs = []
                        if self.ang_axes == "Z":
                            dirs = [[1,0,0]]
                        else:
                            dirs = [[0,0,1]]
                        
                        if len(self.inputs[3].links) > 0:
                            dirs = self.inputs[3].returnData()
                            
                            for dir in dirs:
                                utils_MATH.vec3_removeAxis(dir, self.ang_axes)
                        

                        dirs = utils_GEN.adjustListsCut([source_obs,dirs])[1]
                        
                         
                        
                        for i in range(0,len(source_obs)):
                        
                            source_ob = source_obs[i]
                            dir = dirs[i]
                            selection = utils_SEL.mapSelection(selections[i], source_ob,[self.inputs[1].sel_mode,self.inputs[1].sel_vgroup],self.inputs[1].sel_inv)
                        
                            
                            vals = []
                            if self.ang_mode == "Vertices":
                                for vid in selection[0]:
                                    nor = source_ob.data.vertices[vid].normal
                                    nor = utils_MATH.vec3_removeAxis(nor, self.ang_axes)
 
                                    vals.append(utils_MATH.getAngle(dir,nor))
                                
                                
                                
                            elif self.ang_mode == "Edges":
                                for eid in selection[1]:
                                    nor = utils_GEOM.getEdgeNormal(source_ob, eid)
                                    nor = utils_MATH.vec3_removeAxis(nor, self.ang_axes)
 
                                    vals.append(utils_MATH.getAngle(dir,nor))
                                
                            else:
                                for fid in selection[2]:
                                    nor = source_ob.data.polygons[fid].normal
                                    nor = utils_MATH.vec3_removeAxis(nor, self.ang_axes)
 
                                    vals.append(utils_MATH.getAngle(dir,nor))
   
                        
                            if self.extrema_m == "Highest":
                                current_VALS.append(max(vals))
                            elif self.extrema_m == "Lowest":
                                current_VALS.append(min(vals))
                            elif self.extrema_m == "Average":
                                current_VALS.append(sum(vals) / float(len(vals)))
                            elif self.extrema_m == "Median":
                                current_VALS.append(utils_MATH.getMedian(vals))
                            
                            
            if self.outputs[0].enabled:                
                self.outputs[0].setData(current_COUNTS)
            if self.outputs[1].enabled:
                self.outputs[1].setData(current_VALS)
            if self.outputs[2].enabled:
                self.outputs[2].setData(current_VEC3)        
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
##\brief Transforms a mesh into a list of meshes.
#\detail Uses only the first mesh of the input list, ignores all the others.                            
class MESH_ListNode(buildingNode):

    bl_idname = 'MESH_ListNode'

    bl_label = 'List'

    bl_icon = 'NODETREE'
    
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self,context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
            
      
        if self.mode_list_last != self.mode_list:
            self.mode_list_last = self.mode_list
            outdated = True
            
        if self.cut_useFill_last != self.cut_useFill:
            self.cut_useFill_last = self.cut_useFill
            outdated = True
            
        
            
        
           
        
        if outdated:
            self.updateInputs(context)
            self.callObsolete(context)
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    

    
    
	#NODE DATA
    corrupted = BoolProperty(default = True, update = updateEmpty)
    
    
    
    #data checking
    mode_list_last = StringProperty(default = "", update = updateEmpty)
    cut_useFill_last = BoolProperty(default = True, update = updateEmpty)
    

    
    
    
    
    
    modes = [("Cut","Cut","")]
    
    
    mode_list = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Flatten Modes",
        update = updateNode
    )
    
    cut_useFill = BoolProperty(
        name = "Fill cut",
        default = False,
        update = updateNode
    )
    
    
    
    


    
    
    
    
    
    
    

    
    
    
    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
        #hide all inputs + outputs
        for input in self.inputs:
            if input.name != "Mesh":
                input.enabled = False



        if len(self.inputs) == 3 and len(self.outputs) == 1:
        
            if self.mode_list == "Cut":
                self.inputs[1].enabled = True
                self.inputs[2].enabled = True
                
    
            
            
        
    ##\brief Initializes the node.
    def init(self, context):
        
        #Generic Inputs/Outputs
        self.inputs.new("socket_MESH", "Mesh")
        
        self.outputs.new("socket_MESH", "List")
        
        #Cut Sockets
        self.inputs.new("socket_VEC3_F","Offsets")
        self.inputs.new("socket_VEC3_F","Normals")
        
        
        
        
        
        self.use_custom_color = True
        self.color = (1,.8,.5)
        
        
        self.update()
        
        
    ##\brief GUI.        
    def draw_buttons(self, context, layout):
        
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "mode_list", "")
        
        if self.mode_list == "Cut":
            row2 = layout.row()
            row2.prop(self, "cut_useFill", "Fill")

        layout.separator()    
        
            
        
        
        
        
        
        
        
        
        
        
    ##\brief Re-calculates the node's data.     
    def recalculate(self):
        
        
        self.corrupted = False
        
        
        if len(self.inputs[0].links) > 0:
            

            obs = self.inputs[0].returnData()
            
            source_OBJ = obs[0]
            
            for ob in obs:
                ob.name = "_$OBS$_"
                
            copy_obs = []
        

        
            #CUT
                
            if self.mode_list == "Cut":

                offsets = self.inputs[1].returnData()
                normals = self.inputs[2].returnData()
                
                
                lists = utils_GEN.adjustLists([offsets,normals])
                
                offsets = lists[0]
                normals = lists[1]

                length = len(offsets)

                
                
                #First object needs to be cut differently, we need the first part at index 1, that requires special cutting settings
                

            
                utils_OBJ.prep_all(source_OBJ)
                        
                fob = utils_OBJ.copyobj_vis(source_OBJ)
                
                utils_GEOM.slice_bottom(fob,offsets[0],normals[0],self.cut_useFill)

                utils_OBJ.deprep(fob)
                
                copy_obs.append(fob)
                

                
                for i in range(0,length-1):
                
                
                    sob = utils_OBJ.copyobj_vis(source_OBJ)
                    
                    utils_GEOM.slice(sob,offsets[i],offsets[i+1],normals[i],normals[i+1],self.cut_useFill)

                    utils_OBJ.deprep(sob)
                    
                    copy_obs.append(sob)
  
  
                lob = utils_OBJ.copyobj_vis(source_OBJ)
                
                utils_GEOM.slice_top(lob,offsets[length-1],normals[length-1],self.cut_useFill)

                utils_OBJ.deprep(lob)
                
                copy_obs.append(lob)
                
                    
                    
                utils_OBJ.deprep(source_OBJ)
                    

                    
                    
            #SPLIT
            
            elif self.mode_list == "Split":
                
                return None;
                    
                    
                

            #set current objects to new list1
            if self.outputs[0].enabled:
                self.outputs[0].setData(copy_obs)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
##\brief Filters using a deformation cage.
#\detail Similar to Proportional Editing.                
class MESH_FilterCageNode(buildingNode):

    bl_idname = 'MESH_FilterCageNode'

    bl_label = 'Hook Transform'

    bl_icon = 'NODETREE'
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return

    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self,context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
            
      
        if self.mode_list_last != self.mode_list:
            self.mode_list_last = self.mode_list
            outdated = True
            
        
           
        
        if outdated:
            self.updateInputs(context)
            self.callObsolete(context)
    
    
    
    
    
    
    


        
        

    
    
	#NODE DATA
    corrupted = BoolProperty(default = True, update = updateEmpty)
    
    
    
    #data checking
    mode_list_last = StringProperty(default = "",update = updateEmpty)

    
    
    
    
    
    modes = [("Translate","Translate",""),("Rotate","Rotate",""),("Scale","Scale","")]
    axes_strict = [("X","X",""),("Y","Y",""),("Z","Z","")]
    axes = [("All","All",""),("X","X",""),("Y","Y",""),("Z","Z","")]
    falloffs = [("SMOOTH","Smooth","","SMOOTHCURVE",1),("SPHERE","Sphere","","SPHERECURVE",2),("ROOT","Root","","ROOTCURVE",3),("SHARP","Sharp","","SHARPCURVE",4),("LINEAR","Linear","","LINCURVE",5),("CONSTANT","Constant","","NOCURVE",6),("RANDOM","Random","","RNDCURVE",7)]

    
    
    mode_list = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Modes",
        update = updateNode
    )
    
    from_center = BoolProperty(
        name = "From Center",
        default = False,
        description = "Perform filter with the mesh's center as pivot",
        update = updateNode
    )
    
    scale_axis = EnumProperty(
        name = "Axis",
        items = axes,
        description = "Axis to perform filter on",
        update = updateNode
    )
    
    rot_axis = EnumProperty(
        name = "Axis",
        items = axes_strict,
        description = "Axis to perform filter on",
        update = updateNode
    )
    
    falloff = EnumProperty(
        name = "Falloff",
        items = falloffs,
        description = "Falloff type",
        update = updateNode
    )
    
   

    
    
    
    
    
    
    

    
    
    
    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
    
        #make all inputs visible
        for input in self.inputs:
            input.enabled = True
    
        #hide all but standard inputs + outputs
        for ind in range(4,len(self.inputs)):
                try:
                    self.inputs[ind].enabled = False
                except:
                    pass
                
        for output in self.outputs:
            if output.name != "Mesh":
                output.enabled = False

        #make mode-specific inputs visible
        if len(self.inputs) == 8 and len(self.outputs) == 1:
        
            if self.mode_list == "Translate":
                
                self.inputs[4].enabled = True
                
            elif self.mode_list == "Rotate":
                
                self.inputs[6].enabled = True
                self.inputs[7].enabled = True
                
            elif self.mode_list == "Scale":
                
                self.inputs[5].enabled = True
                self.inputs[7].enabled = True
                
    
            
                    
                
            
        
    ##\brief Initializes the node.
    def init(self, context):
        
        #Generic Outputs
        self.inputs.new("socket_MESH", "Mesh")
        self.inputs.new("socket_MESH", "Cage")
        self.inputs.new("socket_SELECTION", "Cage Sel.")
        
        socket = self.outputs.new("socket_MESH", "Mesh")
        
        socket = self.inputs.new("socket_FLOAT","Radius")
        
        socket = self.inputs.new("socket_VEC3_F","Vector")
        
        socket = self.inputs.new("socket_FLOAT","Factor")
        socket.enabled = False
        
        socket = self.inputs.new("socket_FLOAT","Angle")
        socket.enabled = False
        
        socket = self.inputs.new("socket_VEC3_F","Pivot")
        socket.enabled = False
        
        
        
        

        
        self.use_custom_color = True
        self.color = (1,.8,.5)
        
        
        self.update()
        
        
    ##\brief GUI.        
    def draw_buttons(self, context, layout):
        
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "mode_list", "")
        layout.separator()
        row2 = layout.row()
        row2.prop(self,"falloff","")

        if self.mode_list == "Rotate":
            rowA = layout.row()
            rowA.prop(self,"rot_axis","")
            rowB = layout.row()
            rowB.prop(self,"from_center","Mesh Center")
        
        
        elif self.mode_list == "Scale":
            rowA = layout.row()
            rowA.prop(self,"scale_axis","")
            rowB = layout.row()
            rowB.prop(self,"from_center","Mesh Center")

        layout.separator()    
            
        
        
        
        
        
        
        
        
        
        
    ##\brief Re-calculates the node's data.    
    def recalculate(self):
    
        
        
        self.corrupted = False

        current_SELs = []
        current_OBJs_secondary = []
        
        if len(self.inputs[0].links) > 0 and len(self.inputs[1].links) > 0:
            
            override = bpy.context.copy()
            
            
            win = None
            scr = None
            ar = None
            reg = None
            
        
            
            found = False
            for window in bpy.context.window_manager.windows:
            
                if found:
                    break
            
                screen = window.screen
                
                for area in screen.areas:
                
                    if found:
                        break
                
                    if area.type == 'VIEW_3D':
                    
                        for region in area.regions:
                        
                        
                            if region.type == "WINDOW":
                    
                                win = window
                                scr = screen
                                ar = area
                                reg = region
                                
                                found = True
                                break
        
        
        
        
        
            
            copy_obs = self.inputs[0].returnData()
            cages = self.inputs[1].returnData()
            
            ca_sels = self.inputs[2].returnData()
            
            radii = self.inputs[3].returnData()
            
            if self.mode_list == "Translate":
            
                
                
                vecs = self.inputs[4].returnData()
                
                lists = utils_GEN.adjustLists([copy_obs,cages,ca_sels,vecs,radii])
                
                copy_obs = lists[0]
                cages = lists[1]
                ca_sels = lists[2]
                vecs = lists[3]
                radii = lists[4]

                
                for i in range(0,len(copy_obs)):
                
                    copy_ob = copy_obs[i]
                    cage = cages[i]

                    
                    ca_sel = utils_SEL.mapSelection(ca_sels[i], cage,[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv,False)
                    

                    
                    utils_OBJ.prep_all(copy_obs[i],"VERT")
                    utils_OBJ.prep(cages[i],ca_sel,"VERT")
                    
                    
                    utils_GEOM.prop_translate(copy_ob,cage,self.falloff,vecs[i],radii[i],win,scr,ar,reg)
                    
                    utils_OBJ.deprep(copy_ob)
                    

                    
                    
            elif self.mode_list == "Rotate":
            
                axisvec = mathutils.Vector([0,0,1])
                
                if self.rot_axis == "X":
                    axisvec = mathutils.Vector([1,0,0])
                    
                elif self.rot_axis == "Y":
                    axisvec = mathutils.Vector([0,1,0])
            
            
                
                angs = self.inputs[7].returnData()
                
                if not self.from_center:
                    pivs = self.inputs[8].returnData()
                    
                else:
                    pivs = []
                    for ob in copy_obs:
                        pivs.append(utils_GEOM.meshCenter(ob))
                    
                
                lists = utils_GEN.adjustLists([copy_obs,cages,ca_sels,angs,pivs,radii])
                
                copy_obs = lists[0]
                cages = lists[1]
                ca_sels = lists[2]
                angs = lists[3]
                pivs = lists[4]
                radii = lists[5]

                
                for i in range(0,len(copy_obs)):
                
                    copy_ob = copy_obs[i]
                    cage = cages[i]
                    
                    ca_sel = utils_SEL.mapSelection(ca_sels[i], cage,[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv,False)
                    
                    utils_OBJ.prep_all(copy_obs[i],"VERT")
                    utils_OBJ.prep(cages[i],ca_sel,"VERT")
                    
                    utils_GEOM.prop_rotate(copy_ob,cage,self.falloff,angs[i],axisvec,pivs[i],radii[i],win,scr,ar,reg)
                    
                    utils_OBJ.deprep(copy_ob)
                    
                    
                    
                    
                    
                    
            elif self.mode_list == "Scale":
            
                if self.scale_axis == "All":
                    scale_axes = [1,1,1]
                elif self.scale_axis == "X":
                    scale_axes = [1,0,0]
                elif self.scale_axis == "Y":
                    scale_axes = [0,1,0]
                elif self.scale_axis == "Z":
                    scale_axes = [0,0,1]
            
            
                
                facs = self.inputs[6].returnData()
                
                if not self.from_center:
                    pivs = self.inputs[8].returnData()
                    
                else:
                    pivs = []
                    for ob in copy_obs:
                        pivs.append(utils_GEOM.meshCenter(ob))
                    
                
                lists = utils_GEN.adjustLists([copy_obs,cages,ca_sels,facs,pivs,radii])
                
                copy_obs = lists[0]
                cages = lists[1]
                ca_sels = lists[2]
                facs = lists[3]
                pivs = lists[4]
                radii = lists[5]

                
                for i in range(0,len(copy_obs)):
                
                    copy_ob = copy_obs[i]
                    cage = cages[i]
                    
                    ca_sel = utils_SEL.mapSelection(ca_sels[i], cage,[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv,False)
                    
                    utils_OBJ.prep_all(copy_obs[i],"VERT")
                    utils_OBJ.prep(cages[i],ca_sel,"VERT")
                    
                    
                    scalevec = mathutils.Vector([facs[i]*scale_axes[0],facs[i]*scale_axes[1],facs[i]*scale_axes[2]])
                    
                    
                    
                    utils_GEOM.prop_scale(copy_ob,cage,self.falloff,scalevec,pivs[i],radii[i],win,scr,ar,reg)
                    
                    utils_OBJ.deprep(copy_ob)
                    
                    
                    
                    
                
                
                
                
            
                
             

            if self.outputs[0].enabled:
                self.outputs[0].setData(copy_obs)
                
                
                
                
                
                
                
              
                    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

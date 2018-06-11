##\package buildingGen.nodes.building_nodes_IN
# Input nodes.


import bpy
from bpy.types import NodeTree, Node, NodeSocket

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

from bpy.props import EnumProperty, StringProperty, FloatVectorProperty, IntProperty, FloatProperty, BoolProperty

import custom_sockets


from . import building_NODETREE
from .building_NODETREE import *

from utils import utils_OBJ,utils_MATH, utils_GEN,utils_GLO
from utils.utils_GLO import print_debug
import mathutils
import math
import random


##\brief Grabs an object or a group from the scene.
class IN_GrabMeshNode(buildingNode):

    bl_idname = 'IN_GrabMeshNode'

    bl_label = 'Mesh'

    bl_icon = 'NODETREE'

	#NODE DATA
    
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    
    ##\brief Calls callObsolete().
    def updateNode(self,context):
        self.callObsolete(context)

    corrupted = BoolProperty(default = True, update = updateEmpty)

	
        
    
    m = [("Single","Single",""),("Group","Group","")]
        
    
    
    
    objects_list = StringProperty(
        default = "",
        update = updateNode
    )
    
    
    groups_list = StringProperty(
        default = "",
        update = updateNode
    )
    
    mode = EnumProperty(
        items = m,
        name = "Choose Mode",
        update = updateNode
    )
    
    
    
    

            
    ##\brief Grabs a fresh version from the scene.        
    def recalculate(self):
    
        #self.corrupted = False
        
        curLayer = utils_OBJ.enableLayers()
            
        meshes = []

        if self.mode == "Single":
                
            for ob in bpy.data.objects:
                if ob.name == self.objects_list:
                    copy_ob = utils_OBJ.copyobj_vis(ob)
                    bpy.context.scene.objects.unlink(copy_ob)
                    meshes.append(copy_ob)
                    break
                
        else:
            for g in bpy.data.groups:
                if g.name == self.groups_list:
                    for ob in g.objects:
                        copy_ob = utils_OBJ.copyobj_vis(ob)
                        
                        utils_OBJ.clear_selection()
                        copy_ob.select = True
                        bpy.ops.group.objects_remove_all()
                        
                        bpy.context.scene.objects.unlink(copy_ob)
                        copy_ob.location = mathutils.Vector([0,0,0])
                        meshes.append(copy_ob)
        
        self.outputs[0].setData(meshes)
        
        utils_OBJ.disableLayers(curLayer)
            
            
            
        

        
    ##\brief Initializes the node.
    def init(self, context):
        socket = self.outputs.new("socket_MESH", "Mesh")
        
        
        self.use_custom_color = True
        self.color = (1,.8,.5)
        
        


    ##\brief GUI.    
    def draw_buttons(self, context, layout):
    
        layout.context_pointer_set("CALLER", self)
        
        layout.separator()
        row = layout.row(align = True)
        row.prop(self, "mode", '')
        rowM = layout.row(align = True)
        rowM2 = layout.row(align = True)
        if self.mode == "Single":
            rowM.prop_search(self, "objects_list", bpy.context.scene, "objects", icon='OBJECT_DATA',text="")
        else:
            rowM.prop_search(self, "groups_list", bpy.data, "groups", icon='OBJECT_DATA',text="")
            
        layout.operator("in_mesh.refresh", text="Update", emboss=True)
            
        layout.separator()
        
        
        
        
        
        
        
        
        
        
##\brief Creates one or multiple 3-dimensional vectors.        
class IN_VectorNode(buildingNode):

    bl_idname = 'IN_VectorNode'

    bl_label = 'Vector'

    bl_icon = 'NODETREE'
    
    bl_width_min = 200
    bl_width_default = 200
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
        
        
    ##\brief Checks whether the node needs to be updated.   
    def updateNode(self,context):
    
        outdated = False
        
        if self.mode_last != self.mode:
            self.mode_last = self.mode
            outdated = True
        
        if self.submode_last != self.submode:
            self.submode_last = self.submode
            outdated = True
              
        if self.count_last != self.count:
            self.count_last = self.count
            outdated = True
            
        if self.vec1_0_last != self.vec1_0:
            self.vec1_0_last = self.vec1_0
            outdated = True
            
        if self.vec1_1_last != self.vec1_1:
            self.vec1_1_last = self.vec1_1
            outdated = True
            
        if self.vec1_2_last != self.vec1_2:
            self.vec1_2_last = self.vec1_2
            outdated = True
            
        if self.vec2_0_last != self.vec2_0:
            self.vec2_0_last = self.vec2_0
            outdated = True
            
        if self.vec2_1_last != self.vec2_1:
            self.vec2_1_last = self.vec2_1
            outdated = True
            
        if self.vec2_2_last != self.vec2_2:
            self.vec2_2_last = self.vec2_2
            outdated = True
            
        if self.rl_interpolate_last != self.rl_interpolate:
            self.rl_interpolate_last = self.rl_interpolate
            outdated = True
            
            
            

            
        
        if outdated:            
            self.callObsolete(context)
        
    

	#NODE DATA
    corrupted = BoolProperty(default = True, update = updateEmpty)
    
    mode_last = StringProperty(default = "", update = updateEmpty)
    submode_last = StringProperty(default = "", update = updateEmpty)
    vec1_0_last = FloatProperty(default = 0,update = updateEmpty)
    vec1_1_last = FloatProperty(default = 0,update = updateEmpty)
    vec1_2_last = FloatProperty(default = 0,update = updateEmpty)
    vec2_0_last = FloatProperty(default = 0,update = updateEmpty)
    vec2_1_last = FloatProperty(default = 0,update = updateEmpty)
    vec2_2_last = FloatProperty(default = 0,update = updateEmpty)
    count_last = IntProperty(default=2,update = updateEmpty)
    rl_interpolate_last = BoolProperty(default = False,update = updateEmpty)
            
        
        
    m = [("s","Single",""),("l","List",""),("rs"," Random Single",""),("rl"," Random List",""),]
    ms = [("r","Range",""),("t","True Random","")]
    
        
    mode = EnumProperty(
        items = m,
        name = "Choose Mode",
        update = updateNode
    )
    
    submode = EnumProperty(
        items = ms,
        name = "Choose Mode",
        update = updateNode
    )
      
        
    vec1_0 = FloatProperty(
        name = "Values",
        default = 0.0,
        update = updateNode
    )
    
    vec1_1 = FloatProperty(
        name = "Values",
        default = 0.0,
        update = updateNode
    )
    
    vec1_2 = FloatProperty(
        name = "Values",
        default = 0.0,
        update = updateNode
    )
    
    
    vec2_0 = FloatProperty(
        name = "Values",
        default = 0.0,
        update = updateNode
    )
    
    vec2_1 = FloatProperty(
        name = "Values",
        default = 0.0,
        update = updateNode
    )
    
    vec2_2 = FloatProperty(
        name = "Values",
        default = 0.0,
        update = updateNode
    )

    count = IntProperty(
        name="Count",
        description="Number of vectors",
        default=2,
        update = updateNode
    )
    
    rl_interpolate = BoolProperty(
        name = "Interpolate",
        default = False,
        update = updateNode
    )
    
    
    freeze = BoolProperty(default = False, update = updateEmpty)

    ##\brief Initializes the node.
    def init(self, context):
        socket = self.outputs.new("socket_VEC3_F","Vector")
        

        self.use_custom_color = True
        self.color = (.5,.7,.55)
        
        self.updateNode(context)

    ##\brief GUI.    
    def draw_buttons(self, context, layout):
    
        layout.context_pointer_set("CALLER", self)
        
        layout.separator()
        row1 = layout.row()
        row1.prop(self,"mode","")
        if "r" in self.mode:
            row2 = layout.row()
            row2.prop(self,"submode","")
        if not (self.mode == "rs" and self.submode == "t"):
            box0 = layout.box()
        
            if not (self.mode == "rl" and self.submode == "t"):
            
                rowV1_0 = box0.row()
                rowV1 = box0.row(align = True)
                rowV1_0.label(text = "Vector 1:")
                rowV1.prop(self,"vec1_0","")
                rowV1.prop(self,"vec1_1","")
                rowV1.prop(self,"vec1_2","")
        
                if not self.mode == "s":
                    rowV2_0 = box0.row()
                    rowV2 = box0.row(align = True)
                    rowV2_0.label(text = "Vector 2:")
                    rowV2.prop(self,"vec2_0","")
                    rowV2.prop(self,"vec2_1","")
                    rowV2.prop(self,"vec2_2","")
            
            if "l" in self.mode:
                rowC = box0.row()
                rowC.prop(self,"count","Count")
                
                if self.mode == "rl":
                    rowC = box0.row()
                    rowC.prop(self,"rl_interpolate","Interpolate")
                    
            
            
        if self.mode == "rs" and not self.submode == "t":
            rowC = box0.row()
            rowC.prop(self,"rl_interpolate","Interpolate")
                    
                    
                
                
        if "r" in self.mode:
            layout.separator()
            if self.freeze:
                layout.operator("nodetree.unfreeze", text="Unfreeze", emboss=True)
            else:
                layout.operator("nodetree.freeze", text="Freeze", emboss=True)
            layout.operator("nodetree.randomize", text="Randomize", emboss=True)
        
        layout.separator()

            
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
    
    ##\brief Re-calculates the node's data.   
    def recalculate(self):
    
    
        vec1 = mathutils.Vector([self.vec1_0,self.vec1_1,self.vec1_2])
        vec2 = mathutils.Vector([self.vec2_0,self.vec2_1,self.vec2_2])
    
        
        self.corrupted = False
        
        if self.count < 2:
            self.count = 2
        
        if self.mode == "s":
            list1 = [vec1]
            
        elif self.mode == "rl":
            
            if self.submode == "r":
            
                list1 = []
            
                if self.rl_interpolate:
                    for i in range(0,self.count):
                        ran = random.uniform(0.0, 1.0)
                        
                        list1.append(vec1.lerp(vec2, ran))
                        
                else:
                    for i in range(0,self.count):
                        ranX = random.uniform(0.0, 1.0)
                        ranY = random.uniform(0.0, 1.0)
                        ranZ = random.uniform(0.0, 1.0)
                        
                        x = utils_MATH.interpolate(vec1[0],vec2[0],ranX)
                        y = utils_MATH.interpolate(vec1[1],vec2[1],ranY)
                        z = utils_MATH.interpolate(vec1[2],vec2[2],ranZ)
                        
                        list1.append(mathutils.Vector([x,y,z]))
                        
                
            else:
                
                list1 = []
                
                for i in range(0,self.count):
                    ranX = random.uniform(-500.0, 500.0)
                    ranY = random.uniform(-500.0, 500.0)
                    ranZ = random.uniform(-500.0, 500.0)
                    
                    vec = mathutils.Vector([ranX,ranY,ranZ])
                    vec.normalize()
                    list1.append(vec)
        
        elif self.mode == "l":
            
            list1 = []
            
            cList = []
            jump = 1/(self.count-1)
            
            for i in range(0,self.count):
                fac = jump*i
                list1.append(vec1.lerp(vec2,fac))
                
                
        elif self.mode == "rs":
            
            if self.submode == "r":
                
                if self.rl_interpolate:
                    ran = random.uniform(0.0, 1.0)    
                    list1 = [vec1.lerp(vec2, ran)]
                else:
                    ranX = random.uniform(0.0, 1.0)
                    ranY = random.uniform(0.0, 1.0)
                    ranZ = random.uniform(0.0, 1.0)
                    
                    x = utils_MATH.interpolate(vec1[0],vec2[0],ranX)
                    y = utils_MATH.interpolate(vec1[1],vec2[1],ranY)
                    z = utils_MATH.interpolate(vec1[2],vec2[2],ranZ)
                    
                    list1 = [mathutils.Vector([x,y,z])]
                    
                
            else:
                
                ranX = random.uniform(-500.0, 500.0)
                ranY = random.uniform(-501.0, 501.0)
                ranZ = random.uniform(-503.0, 503.0)
                    
                vec = mathutils.Vector([ranX,ranY,ranZ])
                vec.normalize()
                list1 = [vec]
             

        if self.outputs[0].enabled:       
            self.outputs[0].setData(list1)
                
                
        
                
                
                
                
        
        
        

        
##\brief Creates one or multiple float values.         
class IN_ValueNode(buildingNode, BuildingTree):

    bl_idname = 'IN_ValueNode'

    bl_label = 'Value'

    bl_icon = 'NODETREE'
    
    bl_width_min = 150
    bl_width_default = 150
    
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return

	#NODE DATA

    corrupted = BoolProperty(default = True, update = updateEmpty)
    mode_last = StringProperty(default = "", update = updateEmpty)
    val_s_last = FloatProperty(default = 0.0,update = updateEmpty)
    val_e_last = FloatProperty(default = 0.0,update = updateEmpty)
    val_step_last = FloatProperty(default = 0.0,update = updateEmpty)
    val_count_last = IntProperty(default = 0,update = updateEmpty)
   
   
    ##\brief Checks whether the node needs to be updated.
    def updateNode(self,context):
    
        outdated = False
    
        if self.mode_last != self.mode:
            self.mode_last = self.mode
            outdated = True
            
        if self.val_s_last != self.val_s:
            self.val_s_last = self.val_s
            outdated = True
            
        if self.val_e_last != self.val_e:
            self.val_e_last = self.val_e
            outdated = True
            
        if self.val_step_last != self.val_step:
            self.val_step_last = self.val_step
            outdated = True
            
        if self.val_count_last != self.val_count:
            self.val_count_last = self.val_count
            outdated = True 
        
        if outdated:            
            self.callObsolete(context)
        

    m = [("s","Single",""),("l","List",""),("rs"," Random Single",""),("rl"," Random List",""),]
    
        
    mode = EnumProperty(
        items = m,
        name = "Choose Mode",
        update = updateNode
    )
      

    mode = EnumProperty(
        name = "Mode",
        items = m,
        update = updateNode
    )

    val_s = FloatProperty(
        name = "Value",
        default = 0.0,
        precision = 4,
        step = .1,
        update = updateNode
    )
    
    val_e = FloatProperty(
        name = "Value",
        default = 0.0,
        precision = 4,
        step = .1,
        update = updateNode
    )
    
    val_step = FloatProperty(
        name = "Value",
        default = 0.0,
        precision = 4,
        step = .1,
        update = updateNode
    )
    
    val_count = IntProperty(
        name = "Value",
        default = 1,
        update = updateNode
    )
    
    
       



    freeze = BoolProperty(default = False, update = updateEmpty)


    ##\brief Initializes the node.
    def init(self, context):
    
        self.outputs.new("socket_FLOAT","Value")
        
        
        self.use_custom_color = True
        self.color = (1,.5,.6)

    ##\brief GUI.    
    def draw_buttons(self, context, layout):
    
        layout.context_pointer_set("CALLER", self)
    
        layout.separator()
        row1 = layout.row()
        row1.prop(self,"mode","")
        box0 = layout.box()
            

        row2 = box0.row()
        if not self.mode == "s":
            row2.prop(self, "val_s", "Start")
        else:
            row2.prop(self, "val_s", "")
        
        if not self.mode == "s":
            row3 = box0.row()
            row3.prop(self, "val_e", "End")
            
        if self.mode == "rl":
            rowC = box0.row()
            rowC.prop(self, "val_count", "Count")
        elif "l" in self.mode:
            rowC = box0.row()
            rowC.prop(self, "val_step", "Step")
            
        if "r" in self.mode:
            layout.separator()
            if self.freeze:
                layout.operator("nodetree.unfreeze", text="Unfreeze", emboss=True)
            else:
                layout.operator("nodetree.freeze", text="Freeze", emboss=True)
            layout.operator("nodetree.randomize", text="Randomize", emboss=True)
        layout.separator()
       

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
        
        
    ##\brief Re-calculates the node's data.    
    def recalculate(self):
        
        self.corrupted = False
        
        if self.val_step == 0:
            self.val_step = 1
            
        if self.val_step < 0:
            self.val_step = -self.val_step
        
        if self.mode == "s":
            list1 = [self.val_s]
            
        elif self.mode == "rl":
            
            list1 = []
            
            for i in range(0,self.val_count):
                ran = random.uniform(self.val_s, self.val_e)    
                list1.append(ran)
        
        elif self.mode == "l":
            

            if self.val_e < self.val_s:
             
                curVal = self.val_s
                list1 = [curVal]
            
                while True:
                    curVal -= self.val_step
                    if not curVal < self.val_e:
                        list1.append(curVal)
                    else:
                        break
                        
            else:
                
                curVal = self.val_s
                list1 = [curVal]
            
                while True:
                    curVal += self.val_step
                    if not curVal > self.val_e:
                        list1.append(curVal)
                    else:
                        break
                
                
        elif self.mode == "rs":

            if self.val_s == self.val_e:
                list1 = [self.val_s]
            else:
                list1 = [random.uniform(self.val_s, self.val_e)]

        if self.outputs[0].enabled:       
            self.outputs[0].setData(list1)

        
        
       

       
        
        

##\brief Creates a primitive mesh.        
class IN_PrimitiveNode(buildingNode, BuildingTree):

    bl_idname = 'IN_PrimitiveNode'

    bl_label = 'Primitive'

    bl_icon = 'NODETREE'

	#NODE DATA

    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    
    ##\brief Checks whether the node needs to be updated.
    def updateNode(self,context):
    
        outdated = False
    
        if self.prims_m_last != self.prims_m:
            self.prims_m_last = self.prims_m
            outdated = True
            
        if self.circle_verts_last != self.circle_verts:
            self.circle_verts_last = self.circle_verts
            outdated = True
            
        if self.circle_radius_last != self.circle_radius:
            self.circle_radius_last = self.circle_radius
            outdated = True
            
        if self.circle_fill_last != self.circle_fill:
            self.circle_fill_last = self.circle_fill
            outdated = True
            
        if self.cone_verts_last != self.cone_verts:
            self.cone_verts_last = self.cone_verts
            outdated = True
            
        if self.cone_rad1_last != self.cone_rad1:
            self.cone_rad1_last = self.cone_rad1
            outdated = True
            
        if self.cone_rad2_last != self.cone_rad2:
            self.cone_rad2_last = self.cone_rad2
            outdated = True
            
        if self.cone_depth_last != self.cone_depth:
            self.cone_depth_last = self.cone_depth
            outdated = True
            
        if self.cone_fill_last != self.cone_fill:
            self.cone_fill_last = self.cone_fill
            outdated = True
            
        if self.cyl_verts_last != self.cyl_verts:
            self.cyl_verts_last = self.cyl_verts
            outdated = True
            
        if self.cyl_radius_last != self.cyl_radius:
            self.cyl_radius_last = self.cyl_radius
            outdated = True
            
        if self.cyl_depth_last != self.cyl_depth:
            self.cyl_depth_last = self.cyl_depth
            outdated = True
            
        if self.cyl_fill_last != self.cyl_fill:
            self.cyl_fill_last = self.cyl_fill
            outdated = True
            
        if self.grid_subd_x_last != self.grid_subd_x:
            self.grid_subd_x_last = self.grid_subd_x
            outdated = True
            
        if self.grid_subd_y_last != self.grid_subd_y:
            self.grid_subd_y_last = self.grid_subd_y
            outdated = True
            
        if self.ico_subd_last != self.ico_subd:
            self.ico_subd_last = self.ico_subd
            outdated = True
            
        if self.uv_seg_last != self.uv_seg:
            self.uv_seg_last = self.uv_seg
            outdated = True
            
        if self.uv_ring_last != self.uv_ring:
            self.uv_ring_last = self.uv_ring
            outdated = True
            
        if self.tor_maj_rad_last != self.tor_maj_rad:
            self.tor_maj_rad_last = self.tor_maj_rad
            outdated = True
            
        if self.tor_min_rad_last != self.tor_min_rad:
            self.tor_min_rad_last = self.tor_min_rad
            outdated = True
            
        if self.tor_maj_seg_last != self.tor_maj_seg:
            self.tor_maj_seg_last = self.tor_maj_seg
            outdated = True
            
        if self.tor_min_seg_last != self.tor_min_seg:
            self.tor_min_seg_last = self.tor_min_seg
            outdated = True


        if outdated:            
            self.callObsolete(context)
        
        
    corrupted = BoolProperty(default = True, update = updateEmpty)   
    
    prims_m_last = StringProperty(default = "",update = updateEmpty)
    circle_verts_last = IntProperty(default = 20,update = updateEmpty)
    circle_radius_last = FloatProperty(default = 1,update = updateEmpty)
    circle_fill_last = StringProperty(default = "",update = updateEmpty)
    cone_verts_last = IntProperty(default = 20,update = updateEmpty)
    cone_rad1_last = FloatProperty(default = 1,update = updateEmpty)
    cone_rad2_last = FloatProperty(default = 1,update = updateEmpty)
    cone_depth_last = FloatProperty(default = 1,update = updateEmpty)
    cone_fill_last = StringProperty(default = "",update = updateEmpty)
    cyl_verts_last = IntProperty(default = 20,update = updateEmpty)
    cyl_radius_last = FloatProperty(default = 1,update = updateEmpty)
    cyl_depth_last = FloatProperty(default = 1,update = updateEmpty)
    cyl_fill_last = StringProperty(default = "",update = updateEmpty)
    grid_subd_x_last = IntProperty(default = 20,update = updateEmpty)
    grid_subd_y_last = IntProperty(default = 20,update = updateEmpty)
    ico_subd_last = IntProperty(default = 20,update = updateEmpty)
    uv_seg_last = IntProperty(default = 20,update = updateEmpty)
    uv_ring_last = IntProperty(default = 20,update = updateEmpty)
    tor_maj_rad_last = FloatProperty(default = 1,update = updateEmpty)
    tor_min_rad_last = FloatProperty(default = 1,update = updateEmpty)
    tor_maj_seg_last = IntProperty(default = 20,update = updateEmpty)
    tor_min_seg_last = IntProperty(default = 20,update = updateEmpty)
    
        
        
        
    
    
    prims = [("Circle","Circle",""),("Cone","Cone",""),("Cube","Cube",""),("Cylinder","Cylinder",""),("Grid","Grid",""),("Icosphere","Icosphere",""),("UV Sphere","UV Sphere",""),("Plane","Plane",""),("Torus","Torus",""),("Suzanne","Suzanne","")]
    fill_modes = [("Don't Fill","Don't Fill",""),("Fill NGon","Fill NGon",""),("Fill Tris","Fill Tris","")]
    
    
    prims_m = EnumProperty(
        items = prims,
        update = updateNode
    )
   
    circle_verts = IntProperty(
        default = 32,
        min = 3,
        update = updateNode
    )
    
    circle_radius = FloatProperty(
        default = 1,
        update = updateNode
    )
    
    circle_fill = EnumProperty(
        items = fill_modes,
        update = updateNode
    )
    
    cone_verts = IntProperty(
        default = 32,
        min = 3,
        update = updateNode
    )
    
    cone_rad1 = FloatProperty(
        default = 1,
        update = updateNode
    )
    
    cone_rad2 = FloatProperty(
        default = 0,
        update = updateNode
    )
    
    cone_depth = FloatProperty(
        default = 1,
        update = updateNode
    )
    
    cone_fill = EnumProperty(
        items = fill_modes,
        update = updateNode
    )
    
    cyl_verts = IntProperty(
        default = 32,
        min = 3,
        update = updateNode
    )
    
    cyl_radius = FloatProperty(
        default = 1,
        update = updateNode
    )
    
    cyl_depth = FloatProperty(
        default = 1,
        update = updateNode
    )
    
    cyl_fill = EnumProperty(
        items = fill_modes,
        update = updateNode
    )
    
    grid_subd_x = IntProperty(
        default = 3,
        update = updateNode
    )
    
    grid_subd_y = IntProperty(
        default = 3,
        update = updateNode
    )

    ico_subd = IntProperty(
        default = 1,
        min = 1,
        update = updateNode
    )
    
    uv_seg = IntProperty(
        default = 16,
        min = 3,
        update = updateNode
    )
    
    uv_ring = IntProperty(
        default = 8,
        min = 3,
        update = updateNode
    )
    
    tor_maj_rad = FloatProperty(
        default = 1,
        update = updateNode
    )
    
    tor_min_rad = FloatProperty(
        default =0.5,
        update = updateNode
    )
    
    tor_maj_seg = IntProperty(
        default = 48,
        min = 3,
        update = updateNode
    )
    
    tor_min_seg = IntProperty(
        default = 12,
        min = 3,
        update = updateNode
    )

    

        

        
    ##\brief Initializes the node.
    def init(self, context):
        socket = self.outputs.new("socket_MESH","Mesh")
        
        
        self.use_custom_color = True
        self.color = (1,.8,.5)


    ##\brief GUI.    
    def draw_buttons(self, context, layout):
        layout.separator()
        layout.prop(self, "prims_m", "")
        if self.prims_m == "Circle":
            row = layout.row(align = True)
            row.prop(self, "circle_verts", "Verts")
            row2 = layout.row(align = True)
            row2.prop(self, "circle_radius", "Radius")
            row3 = layout.row(align = True)
            row3.prop(self, "circle_fill", "")
        elif self.prims_m == "Cone":
            row = layout.row(align = True)
            row.prop(self, "cone_verts", "Verts")
            row2 = layout.row(align = True)
            row2.prop(self, "cone_rad1", "Radius 1")
            row3 = layout.row(align = True)
            row3.prop(self, "cone_rad2", "Radius 2")
            row4 = layout.row(align = True)
            row4.prop(self, "cone_depth", "Depth")
            row5 = layout.row(align = True)
            row5.prop(self, "cone_fill", "")
        elif self.prims_m == "Cylinder":
            row = layout.row(align = True)
            row.prop(self, "cyl_verts", "Verts")
            row2 = layout.row(align = True)
            row2.prop(self, "cyl_radius", "Radius")
            row3 = layout.row(align = True)
            row3.prop(self, "cyl_depth", "Depth")
            row5 = layout.row(align = True)
            row5.prop(self, "cyl_fill", "")
        elif self.prims_m == "Grid":
            row = layout.row(align = True)
            row.prop(self, "grid_subd_x", "Subd. X")
            row2 = layout.row(align = True)
            row2.prop(self, "grid_subd_y", "Subd. Y")
        elif self.prims_m == "Icosphere":
            row = layout.row(align = True)
            row.prop(self, "ico_subd", "Subd.")
        elif self.prims_m == "UV Sphere":
            row = layout.row(align = True)
            row.prop(self, "uv_seg", "Segments")
            row2 = layout.row(align = True)
            row2.prop(self, "uv_ring", "Rings")
        elif self.prims_m == "Torus":
            row = layout.row(align = True)
            row.prop(self, "tor_maj_rad", "Radius 1")
            row2 = layout.row(align = True)
            row2.prop(self, "tor_min_rad", "Radius 2")
            row3 = layout.row(align = True)
            row3.prop(self, "tor_maj_seg", "Maj. Segments")
            row4 = layout.row(align = True)
            row4.prop(self, "tor_min_seg", "Min. Segments")

            
            
            
            
        layout.separator()
            
    ##\brief Re-calculates the node's data.     
    def recalculate(self):
    
    
        self.corrupted = False

                   
        
        
        if self.prims_m == "Circle":
            fillm = "NOTHING"
            
            if self.circle_fill == "Fill NGon":
                fillm = "NGON"
            elif self.circle_fill == "Fill Tris":
                fillm = "TRIFAN"
        
            bpy.ops.mesh.primitive_circle_add(vertices = self.circle_verts, radius = self.circle_radius, fill_type = fillm)
            
            
            
        elif self.prims_m == "Cone":
            fillm = "NOTHING"
            
            if self.cone_fill == "Fill NGon":
                fillm = "NGON"
            elif self.cone_fill == "Fill Tris":
                fillm = "TRIFAN"
            
            bpy.ops.mesh.primitive_cone_add(vertices = self.cone_verts, radius1 = self.cone_rad1, radius2 = self.cone_rad2, depth = self.cone_depth, end_fill_type = fillm)
  
            
        elif self.prims_m == "Cube":
            bpy.ops.mesh.primitive_cube_add()
            
        elif self.prims_m == "Cylinder":
            fillm = "NOTHING"
            
            if self.cyl_fill == "Fill NGon":
                fillm = "NGON"
            elif self.cyl_fill == "Fill Tris":
                fillm = "TRIFAN"
            
            bpy.ops.mesh.primitive_cylinder_add(vertices = self.cyl_verts, radius = self.cyl_radius, depth = self.cyl_depth, end_fill_type = fillm)
        
        elif self.prims_m == "Grid":
            bpy.ops.mesh.primitive_grid_add(x_subdivisions = self.grid_subd_x, y_subdivisions = self.grid_subd_y)
            
        elif self.prims_m == "Icosphere":
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = self.ico_subd)
            
        elif self.prims_m == "UV Sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(segments = self.uv_seg, ring_count = self.uv_ring)
            
        elif self.prims_m == "Plane":
            bpy.ops.mesh.primitive_plane_add()
            
        elif self.prims_m == "Torus":
            bpy.ops.mesh.primitive_torus_add(major_radius = self.tor_maj_rad, minor_radius = self.tor_min_rad, major_segments = self.tor_maj_seg, minor_segments = self.tor_min_seg)
            
        elif self.prims_m == "Suzanne":
            bpy.ops.mesh.primitive_monkey_add()
            
            
            
            

        ob = bpy.context.scene.objects.active
        ob.location = mathutils.Vector([0,0,0])
        bpy.context.scene.objects.unlink(ob)
        self.outputs[0].setData([ob])
        
        
        
        
        
        
        
        
        
        
        
        
class IN_ColorNode(buildingNode, BuildingTree):


    bl_idname = 'IN_ColorNode'

    bl_label = 'Color'

    bl_icon = 'NODETREE'
    
    bl_width_min = 70
    bl_width_default = 70
    
    def updateEmpty(self,context):
        return

	#NODE DATA

   
   
    def updateNode(self,context):
        self.callObsolete(context)
            
            
    corrupted = BoolProperty(default = True, update = updateEmpty)        
    col_last = FloatVectorProperty(default = (0,0,0),update = updateEmpty)
            
            
            
  
    col = FloatVectorProperty(
        name = "Color",
        default = (0,0,0),
        min  = 0,
        max = 1,
        precision = 3,
        subtype = "COLOR",
        size = 3,
        update = updateNode
    )



        

        
    
    def init(self, context):
        socket = self.outputs.new("socket_COL","Color")

        self.use_custom_color = True
        self.color = (.3,.3,.3)

        
    def draw_buttons(self, context, layout):
        layout.separator()
        row = layout.row(align = True)
        col2 = row.column(align = True)
        col2.prop(self, "col", "")
        
        
    def recalculate(self):
        self.corrupted = False
        if self.outputs[0].enabled:
            self.outputs[0].setData([self.col])









##\package buildingGen.nodes.building_nodes_MATH
# Math nodes.

import bpy
from bpy.types import NodeTree, Node, NodeSocket

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatProperty, FloatVectorProperty

import custom_sockets


from . import building_NODETREE
from .building_NODETREE import *

from utils import utils_MATH, utils_GEN,utils_GLO
import math
        
        
        
        
        
        
        
        
##\brief Math functions for floats.       
class MATH_ValueNode(buildingNode):


    bl_idname = 'MATH_ValueNode'
    bl_label = 'Value Math'
    bl_icon = 'NODETREE'
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    
    
    modes_enum_l = StringProperty(default = "",update = updateEmpty)
    multi_enum_l = StringProperty(default = "",update = updateEmpty)
    single_enum_l = StringProperty(default = "",update = updateEmpty)
    
    corrupted = BoolProperty(default = True, update = updateEmpty)
    
    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
        outdated = False
    
        #CHECK CONNECTIONS
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
    
        if self.modes_enum_l != self.modes_enum:
            self.modes_enum_l = self.modes_enum
            outdated = True
            
        if self.multi_enum_l != self.multi_enum:
            self.multi_enum_l = self.multi_enum
            outdated = True
            
        if self.single_enum_l != self.single_enum:
            self.single_enum_l = self.single_enum
            outdated = True
            
        if outdated:
            self.callObsolete(context)
            
        self.updateInputs("")
        
    

     
    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
    
        #disconnect all inputs except Mesh
    
        #hide all inputs
        for input in self.inputs:
            if input.name != self.inputs[0].name:
                input.enabled = False

        
        
        
        #add new inputs, based on the selected mode
        if self.modes_enum == "Multi Value" and len(self.inputs) == 2:
            self.inputs[1].enabled = True



     
        
    modes = [("Single Value","Single Value",""),("Multi Value","Multi Value","")]
    math_multi_modes = [("Add","Add",""),("Subtract","Subtract",""),("Multiply","Multiply",""),("Divide","Divide",""),("Power","Power",""),("Log","Log",""),("Modulo","Modulo","")]
    math_single_modes = [("Square","Square",""),("Square Root","Square Root",""),("Ceil","Ceil",""),("Floor","Floor",""),("Round","Round",""),("Invert","Invert","")]
        
    modes_enum = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Mode",
        update = updateNode
    )
        
    multi_enum = EnumProperty(
        name = "Choose Mode",
        items = math_multi_modes,
        description = "Mode",
        update = updateNode
    )
    
    single_enum = EnumProperty(
        name = "Choose Mode",
        items = math_single_modes,
        description = "Mode",
        update = updateNode
    )
        
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_FLOAT", "Value 1")
        self.inputs.new("socket_FLOAT", "Value 2")
        self.outputs.new("socket_FLOAT", "Result")
        
        self.use_custom_color = True
        self.color = (.9,.7,.73)
        
        self.updateInputs(context)
        


    ##\brief GUI.   
    def draw_buttons(self, context, layout):
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "modes_enum", "")
        if self.modes_enum == "Single Value":
            rowS = layout.row(align = True)
            rowS.prop(self, "single_enum", "")
        elif self.modes_enum == "Multi Value":
            rowS = layout.row(align = True)
            rowS.prop(self, "multi_enum", "")
        layout.separator()
        
        
        
    ##\brief Re-calculates the node's data.    
    def recalculate(self):
        self.corrupted = False

        val1 = self.inputs[0].returnData()
        
        values = []
            
        if self.modes_enum == "Single Value":
            if self.single_enum == "Square":
                for i in range (0, len(val1)):
                    values.append(math.pow(val1[i],2))
                
            elif self.single_enum == "Square Root":
                for i in range (0, len(val1)):
                    values.append(math.sqrt(val1[i]))
                
            elif self.single_enum == "Ceil":
                for i in range (0, len(val1)):
                    values.append(math.ceil(val1[i]))
                
            elif self.single_enum == "Floor":
                for i in range (0, len(val1)):
                    values.append(math.floor(val1[i]))
                
            elif self.single_enum == "Round":
                for i in range (0, len(val1)):
                    if val1[i]%1 < 0.5:
                        values.append(math.floor(val1[i]))
                    else:
                        values.append(math.ceil(val1[i]))
                        
            elif self.single_enum == "Invert":
                for i in range (0, len(val1)):
                    values.append(val1[i] * (-1))

            
            
            
        elif self.modes_enum == "Multi Value":
                
            val2 = self.inputs[1].returnData()
            
            lists = utils_GEN.adjustLists([val1, val2])
            
            
            val1 = lists[0]
            val2 = lists[1]
            
            length = len(val1)
                
            if self.multi_enum == "Add":
                for i in range (0, length):
                    values.append(val1[i] + val2[i])
                
            elif self.multi_enum == "Subtract":
                for i in range (0, length):
                    values.append(val1[i] - val2[i])
                
            elif self.multi_enum == "Multiply":
                for i in range (0, length):
                    values.append(val1[i] * val2[i])
                
            elif self.multi_enum == "Divide":
                for i in range (0, length):
                    values.append(val1[i]/val2[i])
                    
            elif self.multi_enum == "Power":
                for i in range (0, length):
                    values.append(math.pow(val1[i],val2[i]))
                
            elif self.multi_enum == "Log":
                for i in range (0, length):
                    values.append(math.log(val1[i],val2[i]))
                
            elif self.multi_enum == "Modulo":
                for i in range (0, length):
                    values.append(val1[i]%val2[i])
                    
                    
                    
        if self.outputs[0].enabled:
            self.outputs[0].setData(values)
        
        
 


##\brief Math functions for vectors. 
class MATH_Vec3Node(buildingNode):

    
    bl_idname = 'MATH_Vec3Node'
    bl_label = 'Vec3 Math'
    bl_icon = 'NODETREE'
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    
    modes_enum_l = StringProperty(default = "",update = updateEmpty)
    multi_enum_l = StringProperty(default = "",update = updateEmpty)
    single_enum_l = StringProperty(default = "",update = updateEmpty)
    
    valmode = BoolProperty(default = False,update = updateEmpty)
    
    corrupted = BoolProperty(default = True, update = updateEmpty)
    
    
    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
        outdated = False
    
        #CHECK CONNECTIONS
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
    
        if self.modes_enum_l != self.modes_enum:
            self.modes_enum_l = self.modes_enum
            outdated = True
            
        if self.multi_enum_l != self.multi_enum:
            self.multi_enum_l = self.multi_enum
            outdated = True
            
        if self.single_enum_l != self.single_enum:
            self.single_enum_l = self.single_enum
            outdated = True
            
        if outdated:
            self.callObsolete(context)
            
        self.updateInputs()
        
        

     




     
        
    modes = [("Single Vec3","Single Vec3",""),("Multi Vec3","Multi Vec3","")]
    math_multi_modes = [("Add","Add",""),("Subtract","Subtract",""),("Multiply","Multiply",""),("Divide","Divide",""),("Dot","Dot",""),("Cross","Cross",""),("Angle","Angle","")]
    math_single_modes = [("Length","Length",""),("Multiply","Multiply",""),("Divide","Divide",""),("Normalize","Normalize",""),("Invert","Invert","")]
        
    modes_enum = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Mode",
        update = updateNode
    )
        
    multi_enum = EnumProperty(
        name = "Choose Mode",
        items = math_multi_modes,
        description = "Mode",
        update = updateNode
    )
    
    single_enum = EnumProperty(
        name = "Choose Mode",
        items = math_single_modes,
        description = "Mode",
        update = updateNode
    )

    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self):
    
        #disconnect all inputs except Mesh
    
        #hide all inputs/outputs
        for input in self.inputs:
            input.enabled = False
            
        self.inputs[0].enabled = True
                

        self.outputs[0].enabled = True
        self.outputs[1].enabled = False
        
        if len(self.inputs) == 3 and len(self.outputs) == 2:
            #add new inputs/outputs, based on the selected mode
            if self.modes_enum == "Multi Vec3":
                self.inputs[1].enabled = True
                if self.multi_enum == "Dot":
                    self.outputs[1].enabled = True
                    self.outputs[0].enabled = False
                
                elif self.multi_enum == "Angle":
                    self.outputs[1].enabled = True
                    self.outputs[0].enabled = False
                
            
            else:
                if self.single_enum == "Multiply" or self.single_enum == "Divide":
                    self.inputs[2].enabled = True
            
                elif self.single_enum == "Length":
                    self.outputs[1].enabled = True
                    self.outputs[0].enabled = False
            
        
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_VEC3_F", "Vec3 1")
        socket = self.inputs.new("socket_VEC3_F", "Vec3 2")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT", "Value")
        socket.enabled = False
        socket = self.outputs.new("socket_VEC3_F", "Vec3")
        socket.enabled = False
        self.outputs.new("socket_FLOAT", "Value")
        
        
        self.use_custom_color = True
        self.color = (.5,.7,.55)
        
        
        self.update()
        
        


    ##\brief GUI.   
    def draw_buttons(self, context, layout):
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "modes_enum", "")
        if self.modes_enum == "Single Vec3":
            rowS = layout.row(align = True)
            rowS.prop(self, "single_enum", "")
        elif self.modes_enum == "Multi Vec3":
            rowS = layout.row(align = True)
            rowS.prop(self, "multi_enum", "")
        layout.separator()
        
        
        
    ##\brief Re-calculates the node's data.    
    def recalculate(self):
        self.corrupted = False
        vec1 = self.inputs[0].returnData()
        
        vectors = []
        values = []
            
        if self.modes_enum == "Single Vec3":
            if self.single_enum == "Length":
                for i in range (0, len(vec1)):
                    x = math.pow(vec1[i][0],2)
                    y = math.pow(vec1[i][1],2)
                    z = math.pow(vec1[i][2],2)
                    values.append(math.sqrt(x + y + z))
                    
                    
                
            elif self.single_enum == "Normalize":
                for i in range (0, len(vec1)):
                    vectors.append(utils_MATH.vec3_normalize(vec1[i]))
                    
                
            elif self.single_enum == "Multiply":
            
                val = self.inputs[2].returnData()
                
                lists = utils_GEN.adjustLists(val,vec1)
                
                val = lists[0]
                vec1 = lists[1]
            
                for i in range (0, len(vec1)):
                    self.vec = [vec1[i][0]*val[i], vec1[i][1]*val[i], vec1[i][2]*val[i]]
                    
                
            elif self.single_enum == "Divide":
                val = self.inputs[2].returnData()
                
                lists = utils_GEN.adjustLists(val,vec1)
                
                val = lists[0]
                vec1 = lists[1]
            
                for i in range (0, len(vec1)):
                    vectors.append([vec1[i][0]/val[i], vec1[i][1]/val[i], vec1[i][2]/val[i]])
                    
            elif self.single_enum == "Invert":
                for i in range (0, len(vec1)):
                    vectors.append([vec1[i][0]*(-1), vec1[i][1]*(-1), vec1[i][2]*(-1)])

            
            
            
        elif self.modes_enum == "Multi Vec3":
            #get second value list
            vec2 = self.inputs[1].returnData()
            
            lists = utils_GEN.adjustLists([vec1,vec2])
                
            vec1 = lists[0]
            vec2 = lists[1]
            
                
            if self.multi_enum == "Add":
                for i in range (0, len(vec1)):
                    vectors.append([vec1[i][0]+vec2[i][0],vec1[i][1]+vec2[i][1],vec1[i][2]+vec2[i][2]])
            
            elif self.multi_enum == "Subtract":
                for i in range (0, len(vec1)):
                    vectors.append([vec1[i][0]-vec2[i][0],vec1[i][1]-vec2[i][1],vec1[i][2]-vec2[i][2]])
            
            elif self.multi_enum == "Multiply":
                for i in range (0, len(vec1)):
                    vectors.append([vec1[i][0]*vec2[i][0],vec1[i][1]*vec2[i][1],vec1[i][2]*vec2[i][2]])
            
            elif self.multi_enum == "Divide":
                for i in range (0, len(vec1)):
                    vectors.append([vec1[i][0]/vec2[i][0],vec1[i][1]/vec2[i][1],vec1[i][2]/vec2[i][2]])
                    
            elif self.multi_enum == "Dot":
                for i in range (0, len(vec1)):
                    values.append(utils_MATH.vec3_dot(vec1[i],vec2[i]))
                
            elif self.multi_enum == "Cross":
                for i in range (0, len(vec1)):
                    vectors.append(utils_MATH.vec3_cross(vec1[i],vec2[i]))
                
            elif self.multi_enum == "Angle":
                for i in range (0, len(vec1)):
                    values.append(utils_MATH.getAngle(vec1[i],vec2[i]))
                    

        if self.outputs[1].enabled:
            self.outputs[1].setData(values)
            
        if self.outputs[0].enabled:
            self.outputs[0].setData(vectors)
        
        

##\package buildingGen.nodes.building_nodes_FLOW
# Flow Control nodes..

import bpy
import bmesh
import random
from bpy.types import NodeTree, Node, NodeSocket

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

from bpy.props import EnumProperty, StringProperty, BoolProperty, FloatProperty, FloatVectorProperty, PointerProperty

import custom_sockets


from . import building_NODETREE
from .building_NODETREE import *

from utils import utils_GEN, utils_MATH, utils_OBJ, utils_GEOM, utils_SEL,utils_GLO
import mathutils
import math
from random import randrange





        

        
##\brief Serves as a gate in nodetree calculations.
#\detail If the gate is closed, the tree part behind it won't be recalculated. Instead, the last known calculation will be used.        
class FLOW_GateNode(buildingNode):


    bl_idname = 'FLOW_GateNode'

    bl_label = 'Gate'

    bl_icon = 'NODETREE'
    
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
        
    corrupted = BoolProperty(default = True, update = updateEmpty)
    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self,context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True

        if outdated and self.open:
            self.callObsolete("")
            
            
            
            
    ##\brief Custom flooding function, depends on gate status.        
    def floodObsolete(self, context):
    
        if self.open:
            #mark as outdated:
            self.corrupted = True
            print_debug(self.name+" has been marked obsolete.")
            # propagate flood
            
            outputs = [] 
            
            for output in self.outputs:
                if len(output.links) != 0:
                    for link in output.links:
                        print_debug("   -> "+self.name+" is flooding "+link.to_node.name)
                        test = link.to_node.floodObsolete(context)
                        if not test == None:
                            if not test in outputs:
                                outputs.extend(test)

            return outputs
            
        return []
            
            
            
            
            
            
            
            
    

        
    ##\brief Closes the gate and handles the tree part's data.    
    def closeGate(self):
        self.open = False
        self.saveCurrentData()
    
    ##\brief Opens the gate and alerts the father nodes.
    def openGate(self):
        self.open = True
        self.callObsolete("")
    
    ##\brief Recalculates its tree part's data and alerts the father nodes.
    def refresh(self):
        self.saveCurrentData()
        self.callObsolete("")
        
        


    
	#NODE DATA
    datatype = StringProperty(default = "",update = updateEmpty)
    current_DATA = StringProperty(default = "",update = updateEmpty)
    
    


    
    open = BoolProperty(
        name = "Open/Close Gate",
        default = True,
        description = "Open/Close Gate",
        update = updateEmpty
    )
                
            
        
    ##\brief Initializes the node.
    def init(self, context):
        
        #Generic Sockets
        self.inputs.new("socket_UNIV", "Input")
        
        self.outputs.new("socket_UNIV", "Output")
        
        self.use_custom_color = True
        self.color = (.7,.7,.7)
        
        self.update()
        
        
    ##\brief GUI.    
    def draw_buttons(self, context, layout):
        
        layout.context_pointer_set("CALLER", self)

        row0 = layout.row()
        row1 = layout.row()
        
        if self.open:
            row1.label(text = "")
            row0.operator("gate.close", text="Close", emboss=True)
        else:
            row1.operator("gate.refresh", text="Refresh", emboss=True) 
            row0.operator("gate.open", text="Open", emboss=True)  
        
    
    ##\brief Re-calculates the node's data, if open.
    def recalculate(self):
        
        self.corrupted = False
        
        if self.open:
            self.saveCurrentData()

        
            
            
    ##\brief Saves its tree part's data as its own to return.        
    def saveCurrentData(self):

        self.corrupted = True
        
        if len(self.inputs[0].links) > 0:
        
        
            savedata = self.inputs[0].returnData()
                
                
            self.outputs[0].setData(savedata)

        return
                

                
                
                
                
                
        
        
        
        
        
        
        
        
        
         
        
        
        
        
        
        
        
##\brief Chooses between two inputs to forward.
#\detail Based on simple greater/smaller calculations, it forwards one of two inputs to its father nodes.
class FLOW_IfNode(buildingNode):

    '''A custom node'''

    bl_idname = 'FLOW_IfNode'

    bl_label = 'If-Statement'

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
        
        if self.mode_last != self.mode:
            self.mode_last = self.mode
            outdated = True
            

        
        
           
        
        if outdated:
            self.callObsolete(context)

        


    
	#NODE DATA
    
    
    
    #data checking
    mode_last = StringProperty(default = "",update = updateEmpty)
    corrupted = BoolProperty(default = True, update = updateEmpty) 
                 

     
    m = [("g","Greater Than",""),("ge","Greater/Equals",""),("e","Equals",""),("le","Less/Equals",""),("l","Less Than","")]

                    
    mode = EnumProperty(
        name = "Choose Mode",
        items = m,
        description = "If-Statement Mode",
        update = updateNode
    )
            
                
            
        
    ##\brief Initializes the node.
    def init(self, context):
        
        #Generic Sockets
        self.inputs.new("socket_FLOAT", "Value 1")
        self.inputs.new("socket_FLOAT", "Value 2")
        self.inputs.new("socket_UNIV", "Input 1")
        self.inputs.new("socket_UNIV", "Input 2")
        
        self.outputs.new("socket_UNIV", "Output")
        
        self.use_custom_color = True
        self.color = (.7,.7,.7)
        
        self.update()
        
        
    ##\brief GUI.    
    def draw_buttons(self, context, layout):
        
        layout.separator()
        layout.prop(self,"mode","")
        layout.separator()
        
        
       
        
    ##\brief Re-calculates the node's data.     
    def recalculate(self):
    
        self.corrupted = False
    
        vals1 = self.inputs[0].returnData()
        vals2 = self.inputs[1].returnData()
        
        obs1 = self.inputs[2].returnData()
        obs2 = self.inputs[3].returnData()
        
        dt1 = self.inputs[2].askForType()
        dt2 = self.inputs[3].askForType()
        
        if dt1 == dt2:
        
            lists = utils_GEN.adjustLists([vals1,vals2,obs1,obs2])
            
            vals1 = lists[0]
            vals2 = lists[1]
            obs1 = lists[2]
            obs2 = lists[3]
            
            oblist = []
            
            if self.mode == "g":
            
                for i in range(0,len(vals1)):
                    
                    if vals1[i] > vals2[i]:
                        oblist.append(obs1[i])
                    else:
                        oblist.append(obs2[i])
                        
            elif self.mode == "ge":
            
                for i in range(0,len(vals1)):
                    
                    if vals1[i] >= vals2[i]:
                        oblist.append(obs1[i])
                    else:
                        oblist.append(obs2[i])
                        
            elif self.mode == "e":
            
                for i in range(0,len(vals1)):
                    
                    if vals1[i] == vals2[i]:
                        oblist.append(obs1[i])
                    else:
                        oblist.append(obs2[i])
                        
            elif self.mode == "le":
            
                for i in range(0,len(vals1)):
                    
                    if vals1[i] <= vals2[i]:
                        oblist.append(obs1[i])
                    else:
                        oblist.append(obs2[i])
                        
            elif self.mode == "l":
            
                for i in range(0,len(vals1)):
                    
                    if vals1[i] < vals2[i]:
                        oblist.append(obs1[i])
                    else:
                        oblist.append(obs2[i])
                        
            if self.outputs[0].enabled:
                self.outputs[0].setData(oblist,dt1)
                    
        
            
            
        
            

        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

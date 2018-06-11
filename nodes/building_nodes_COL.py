import bpy
from bpy.types import NodeTree, Node, NodeSocket

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatProperty

import custom_sockets

from . import building_NODETREE
from .building_NODETREE import *
from utils import utils_GLO




        
        
class COL_MixNode(buildingNode, BuildingTree):

    '''Building Output'''
    bl_idname = 'COL_MixNode'
    bl_label = 'Color Math'
    bl_icon = 'NODETREE'
    
    def update(self):
        self.updateNode("")
    
    def updateNode(self, context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
                
        #Check internal modes
        
        if self.mix_mode_last != self.mix_mode:
            self.mix_mode_last = self.mix_mode
            outdated = True
        
        
        
        if outdated:
            self.floodObsolete(context)
        
        
        
           

     


    corrupted = True
    retcols = []

    mix_mode_last = StringProperty(default = "")
      
                    
                    
                    
                    
    modes = [("Add","Add",""),("Subtract","Subtract",""),("Multiply","Multiply",""),("Divide","Divide","")]
    
    
    
    
    
    mix_mode = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Extraction Modes",
        update = updateNode
    )
                    
    

                    
                    
                    
                    
    
    
    def init(self, context):
        self.inputs.new("socket_FLOAT", "Factor")
        self.inputs.new("socket_COL", "Color 1")
        self.inputs.new("socket_COL", "Color 2")
        self.outputs.new("socket_COL", "Color")
        
        
        
        
        self.use_custom_color = True
        self.color = (.3,.3,.3)
        


        
    def draw_buttons(self, context, layout):
        layout.separator()
        row1 = layout.row()
        row1.prop(self, "mix_mode", "")
        layout.separator()
        
    def returnData(self, output):

        self.recalculate(output)
        return self.retcols
    
    def recalculate(self, output):
    
        self.corrupted = False
        self.retcols = []
                
        col1 = self.inputs[1].returnData()
        col2 = self.inputs[2].returnData()
                
                
                
                

        
        
        
        
        
        

                
                
                
            
        
        
        
            

        
        













##\package buildingGen.utils.utils_OPERATOR
# Operators

import bpy
import math
from . import utils_OBJ, utils_MATH,utils_GLO
from bpy.props import EnumProperty, StringProperty, FloatVectorProperty, IntProperty, FloatProperty, BoolProperty



class GEN_MessageOperator(bpy.types.Operator):

    bl_idname = "popup.message"
    bl_label = "Message"
    
    type = StringProperty()
    message = StringProperty()

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self)

    def draw(self, context):
        if self.type == "Notify":
            self.layout.prop(self, "message")






##\brief Operator for updating a nodetree.
class OUT_UpdateOperator(bpy.types.Operator):
    
    ##\property bl_idname
    #\brief Name of the operator.
    bl_idname = "output.update"
    
    ##\property bl_label
    #\brief Label of the operator.
    bl_label = "Update"

    ##\fn execute
    #\brief Execute the Output's recalculate() function
    #\returns (String) 'FINISHED' if finished
    def execute(self, context):
        
        context.CALLER.update()
        context.CALLER.recalculate()
        
        
        return {'FINISHED'}
        
        
##\brief Operator for generating a building.        
class OUT_GenerateOperator(bpy.types.Operator):
    
    ##\property bl_idname
    #\brief Name of the operator.
    bl_idname = "output.generate"
    
    ##\property bl_label
    #\brief Label of the operator.
    bl_label = "Generate"

    ##\fn execute
    #\brief Execute the Output's generate() function
    #\returns (String) 'FINISHED' if finished
    def execute(self, context):
        
        context.CALLER.update()
        context.CALLER.generate()
        
        return {'FINISHED'}
        
        
        
 
 


##\brief Opens a gate node.
class FLOW_GateOpenOperator(bpy.types.Operator):
    
    ##\property bl_idname
    #\brief Name of the operator.
    bl_idname = "gate.open"
    
    ##\property bl_label
    #\brief Label of the operator.
    bl_label = "Open"

    
    ##\fn execute
    #\brief Execute the gate's openGate() function.
    #\returns (String) 'FINISHED' if finished
    def execute(self, context):
        
        context.CALLER.update()
        context.CALLER.openGate()
        
        return {'FINISHED'}

 
        
##\brief Closes a gate node.       
class FLOW_GateCloseOperator(bpy.types.Operator):
    
    ##\property bl_idname
    #\brief Name of the operator.
    bl_idname = "gate.close"
    
    ##\property bl_label
    #\brief Label of the operator.
    bl_label = "Open"

    
    ##\fn execute
    #\brief Execute the gate's closeGate() function.
    #\returns (String) 'FINISHED' if finished
    def execute(self, context):
        
        context.CALLER.update()
        context.CALLER.closeGate()
        
        return {'FINISHED'}   



##\brief Refreshes a gate node.
class FLOW_GateRefreshOperator(bpy.types.Operator):
    
    ##\property bl_idname
    #\brief Name of the operator.
    bl_idname = "gate.refresh"
    
    ##\property bl_label
    #\brief Label of the operator.
    bl_label = "Refresh"

    
    ##\fn execute
    #\brief Execute the gate's update() function.
    #\returns (String) 'FINISHED' if finished
    def execute(self, context):
        
        context.CALLER.update()
        context.CALLER.refresh()
        
        return {'FINISHED'} 
        
        
        
        
        
        
##\brief Randomizes a node.        
class RandomizeOperator(bpy.types.Operator):
    
    ##\property bl_idname
    #\brief Name of the operator.
    bl_idname = "nodetree.randomize"
    
    ##\property bl_label
    #\brief Label of the operator.
    bl_label = "Randomize"

    
    ##\fn execute
    #\brief Execute the node's recalculate() function.
    #\returns (String) 'FINISHED' if finished
    def execute(self, context):
        
        context.CALLER.randomize()
        
        return {'FINISHED'}
        
##\brief Freezes a node with random elements.  
class FreezeOperator(bpy.types.Operator):
    
    ##\property bl_idname
    #\brief Name of the operator.
    bl_idname = "nodetree.freeze"
    
    ##\property bl_label
    #\brief Label of the operator.
    bl_label = "Freeze Randomization"

    
    ##\fn execute
    #\brief Execute the node's freezeRandom() function.
    #\returns (String) 'FINISHED' if finished
    def execute(self, context):
        
        context.CALLER.freezeRandom()
        
        return {'FINISHED'}
        
##\brief Unfreezes a node with random elements.       
class UnfreezeOperator(bpy.types.Operator):
    
    ##\property bl_idname
    #\brief Name of the operator.
    bl_idname = "nodetree.unfreeze"
    
    ##\property bl_label
    #\brief Label of the operator.
    bl_label = "Unfreeze Randomization"

    
    ##\fn execute
    #\brief Execute the node's unfreezeRandom() function.
    #\returns (String) 'FINISHED' if finished
    def execute(self, context):
        
        context.CALLER.unfreezeRandom()
        
        return {'FINISHED'}
        
        
        
##\brief Refreshes an IN_GrabMeshNode's 3D object.        
class IN_MeshRefreshOperator(bpy.types.Operator):
    
    ##\property bl_idname
    #\brief Name of the operator.
    bl_idname = "in_mesh.refresh"
    
    ##\property bl_label
    #\brief Label of the operator.
    bl_label = "Refresh"

    
    ##\fn execute
    #\brief Execute the node's recalculate() function.
    #\returns (String) 'FINISHED' if finished
    def execute(self, context):
        
        context.CALLER.recalculate()
        context.CALLER.callObsolete(context)
        
        return {'FINISHED'}
        





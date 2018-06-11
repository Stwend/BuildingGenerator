##\package buildingGen.nodes.building_nodes_OUT
# Output nodes.


import bpy
from bpy.types import NodeTree, Node, NodeSocket

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatVectorProperty, IntProperty

import custom_sockets


from . import building_NODETREE
from .building_NODETREE import *

from utils import utils_OBJ, utils_GEN,utils_GLO
from utils.utils_GLO import print_debug


##\brief A tree's output.
#\detail Makes the building visible and puts it in a selected layer. Also maintains a preview object.
class OUT_OutputNode(buildingNode):

    bl_idname = 'OUT_OutputNode'
    bl_label = 'Building Output'
    bl_icon = 'NODETREE'
    
    bl_width_min = 180
    bl_width_default = 180
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    
    ##\brief Gets all active layers.
    def getObjectLayerList(self,layer):
        list1 = []
        for x in range (1,21):
            if x == int(layer):
                list1.extend([True])
            else:
                list1.extend([False])
        return list1

    ##\brief Starts the calculation of a tree.  
    def triggerData(self,context):
        if self.keep_updated:
            self.recalculate()
    
    
    ##\brief Custom flooding method, returns the node's pointer.
    def floodObsolete(self, context):
        return [self.as_pointer()]
    
    def layerNums(self, context):
        numList = []
        for i in range(1,21):
            numList.append((str(i),str(i),""))
        return numList
    
    #NODE DATA
    
    
    NodeInitialized = BoolProperty(default = False,update = updateEmpty)
    displayWarning = BoolProperty(default = True,update = updateEmpty)
    
    building_name = StringProperty(
        default = "Building",
        update = triggerData
    )
    
    
    create_in_layer = EnumProperty(
        items = layerNums,
        name = "Choose Layer",
        description = "Layer the preview is created in",
        update = triggerData
    )
    
    create_in_layer_g = EnumProperty(
        items = layerNums,
        name = "Choose Layer",
        description = "Layer the building is created in",
        update = triggerData
    )
    
    keep_updated = BoolProperty(
        default = False,
        update = updateEmpty
    )
    
    building_name = StringProperty(
        default = "Building",
        update = triggerData
    )
    
    edit_prev = BoolProperty(
        default = False,
        update = updateEmpty
    )
    
    edit_gen = BoolProperty(
        default = False,
        update = updateEmpty
    )
    
    edit_rand = BoolProperty(
        default = False,
        update = updateEmpty
    )
    
    
    
    
    ##\brief If an input has changed, tries to start a calculation.
    def checkInputs(self,context):
        
        request = False
    
        for input in self.inputs:
            if input.check_outdated():
                request = True
                
        if request:
            self.triggerData(context)
            
    ##\brief Custom update method. Also checks inputs.          
    def update(self):
        print_debug("UPDATING:",self.name)
        print_debug("   -> self:",self.name)
        
        
        
        self.checkInputs("")
    
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_MESH", "Mesh")
        
        self.use_custom_color = True
        self.color = (.6,.6,.6)
        
        


    ##\brief GUI.    
    def draw_buttons(self, context, layout):
            
            
        
    
        #Needed for the update operator - this node gives the operator a self-reference so that the operator can backtrack to its caller and call this node's "recalculate()" method
        layout.context_pointer_set("CALLER", self)
    
        layout.separator()
        box1 = layout.box()
        box2 = layout.box()
        

        
        
        row0 = box1.row()
        row0.label(text = "Preview")
        row0.prop(self,"edit_prev","",icon="TRIA_DOWN" if self.edit_prev else "TRIA_RIGHT",icon_only=True, emboss=False)
        
        if self.edit_prev:
        
            box1.prop(self, "create_in_layer", 'Layer')
            row1 = box1.row()
            row1.alignment = "RIGHT"
            row1.prop(self, "keep_updated", "Auto-Preview")

            rowb1 = box1.row()
            rowb1.scale_y = 1.4
            rowb1.operator("output.update", text="Preview", emboss=True)
        
        
        row0 = box2.row()
        row0.label(text = "Generate")
        row0.prop(self,"edit_gen","",icon="TRIA_DOWN" if self.edit_gen else "TRIA_RIGHT",icon_only=True, emboss=False)
        
        if self.edit_gen:
        
            box2.prop(self, "create_in_layer_g", 'Layer')
            box2.prop(self,"building_name", "Name")
            rowb2 = box2.row()
            rowb2.scale_y = 1.4
            rowb2.operator("output.generate", text="Generate", emboss=True)
        
        boxF = layout.box()
        rowL = boxF.row()
        rowL.label(text = "Randomize")
        rowL.prop(self,"edit_rand","",icon="TRIA_DOWN" if self.edit_rand else "TRIA_RIGHT",icon_only=True, emboss=False)
        
        if self.edit_rand:
        
            rowF = boxF.row()
            rowR = boxF.row()
            
            rowF.scale_y = 1.4
            rowR.scale_y = 1.4
            
            rowF.operator("nodetree.freeze", text = "Freeze", emboss = True)
            rowF.operator("nodetree.unfreeze", text = "Unfreeze", emboss = True)
            rowR.operator("nodetree.randomize", text = "Randomize", emboss = True)
        
        
        
        
        layout.separator()
        
        
        if self.displayWarning:

            layout.separator()
            row1 = layout.row()
            row1.alignment = "CENTER"
            row1.label(text = "WARNING", icon = "ERROR")

            layout.separator()
            
            row2 = layout.row()
            row3 = layout.row()
            row4 = layout.row()
            row_split = layout.row()
            row6 = layout.row()
            
            row2.alignment = "LEFT"
            row3.alignment = "LEFT"
            row4.alignment = "LEFT"
            row6.alignment = "LEFT"
            
            
            row_split.scale_y = 0.3
            row_split.label(text = "")

            
            row2.label(text = "If no stored data is found,")
            row3.label(text = "the entire tree will be re-")
            row4.label(text = "calculated by force.")
            row6.label(text = "This may take some time.")
            layout.separator()
            layout.separator()

        
        
        
    ##\brief Re-calculates the node's data.    
    def recalculate(self):
    
    
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
    
                override = bpy.context.copy()
                override['area'] = area               
                bpy.ops.view3d.snap_cursor_to_center(override)
                break
                
                
    
        print_debug("")
        print_debug("BEGIN CYCLE")
        print_debug("-------------------")
        #utils_GLO.dumpNodelist(self.id_data)
        
        utils_OBJ.clear_selection()
        
        
        curLayer = utils_OBJ.enableLayers()
        
        
        
    
        #change color to red to show this node is working on something
        self.color = (1,.3,.3)
    
        #delete old object

        lastOb = utils_OBJ.findFGOb(self.name + " (Preview)")
        if not lastOb == None:
            lastOb.name = "_$OBS$_"
            bpy.context.scene.objects.unlink(lastOb)

    
        #collect data from inputs
        if len(self.inputs[0].links) != 0:
        
            scene = bpy.context.scene
            obs = self.inputs[0].returnData()
            
            if obs == [] or obs == None:
                #garbage collection
                utils_OBJ.collectGarbage()
        
                #change color back to normal
                self.color = (.6,.6,.6)
                utils_OBJ.disableLayers(curLayer)
                print_debug("")
                print_debug("END CYCLE(no objects)")
                print_debug("-------------------")
                print_debug("")
                return True

            for ob in obs:
                scene.objects.link(ob)
            
            ctx = bpy.context.copy()

            # one of the objects to join
            obs[0].name = self.name + " (Preview)"
            obs[0].layers = self.getObjectLayerList(self.create_in_layer)
            ctx['active_object'] = obs[0]
            
            if len(obs) == 1:
            
                #garbage collection
                utils_OBJ.collectGarbage()
        
                #change color back to normal
                self.color = (.6,.6,.6)
                utils_OBJ.disableLayers(curLayer)
                print_debug("")
                print_debug("END CYCLE(1 object)")
                print_debug("-------------------")
                print_debug("")
                return True

            ctx['selected_objects'] = obs

            # we need the scene bases as well for joining
            ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]

            bpy.ops.object.join(ctx)
            
            
            


        #garbage collection
        utils_OBJ.collectGarbage()
        
        #change color back to normal
        self.color = (.6,.6,.6)
        
        utils_OBJ.disableLayers(curLayer)
        
        print_debug("")
        print_debug("END CYCLE")
        print_debug("-------------------")
        print_debug("")
        self.displayWarning = False
        
        
        
    ##\brief Generates a new building object.   
    def generate(self):
    
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
    
                override = bpy.context.copy()
                override['area'] = area               
                bpy.ops.view3d.snap_cursor_to_center(override)
                break
    
        print_debug("")
        print_debug("GENERATING")
        print_debug("-------------------")
        #utils_GLO.dumpNodelist(self.id_data)
        
        utils_OBJ.clear_selection()
        
        
        curLayer = utils_OBJ.enableLayers()
        
        
        
    
        #change color to red to show this node is working on something
        self.color = (1,.3,.3)

    
        #collect data from inputs
        if len(self.inputs[0].links) != 0:
        
            scene = bpy.context.scene
            obs = self.inputs[0].returnData()
            
            if obs == [] or obs == None:
                #garbage collection
                utils_OBJ.collectGarbage()
        
                #change color back to normal
                self.color = (.6,.6,.6)
                utils_OBJ.disableLayers(curLayer)
                print_debug("")
                print_debug("GENERATING DONE (no objects)")
                print_debug("-------------------")
                print_debug("")
                return True

            for ob in obs:
                scene.objects.link(ob)
            
            ctx = bpy.context.copy()

            # one of the objects to join
            obs[0].name = self.building_name
            obs[0].layers = self.getObjectLayerList(self.create_in_layer_g)
            ctx['active_object'] = obs[0]
            
            if len(obs) == 1:
            
                #garbage collection
                utils_OBJ.collectGarbage()
        
                #change color back to normal
                self.color = (.6,.6,.6)
                utils_OBJ.disableLayers(curLayer)
                print_debug("")
                print_debug("GENERATING DONE(1 object)")
                print_debug("-------------------")
                print_debug("")
                return True

            ctx['selected_objects'] = obs

            # we need the scene bases as well for joining
            ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]

            bpy.ops.object.join(ctx)
            
            
            


        #garbage collection
        utils_OBJ.collectGarbage()
        
        #change color back to normal
        self.color = (.6,.6,.6)
        
        utils_OBJ.disableLayers(curLayer)
        
        print_debug("")
        print_debug("GENERATING DONE")
        print_debug("-------------------")
        print_debug("")
        self.displayWarning = False
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

##\brief Serves as a debugger.
#\detail Can be used to check values, vectors, objects, and selections.        
class OUT_DebugNode(buildingNode, BuildingTree):

    '''Building Output'''
    bl_idname = 'OUT_DebugNode'
    bl_label = 'Debug'
    bl_icon = 'NODETREE'
    
    bl_width_min = 200
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    
    lastmode = StringProperty(default = "",update = updateEmpty)
    
    value = StringProperty(default = "",update = updateEmpty)
    
    stringX = StringProperty(default = "",update = updateEmpty)
    stringY = StringProperty(default = "",update = updateEmpty)
    stringZ = StringProperty(default = "",update = updateEmpty)
    
    ob_name = StringProperty(default = "",update = updateEmpty)
    mesh_name = StringProperty(default = "",update = updateEmpty)
    
    v_count = IntProperty(update = updateEmpty)
    e_count = IntProperty(update = updateEmpty)
    f_count = IntProperty(update = updateEmpty)
    
    ob_pos_X = StringProperty(default = "",update = updateEmpty)
    ob_pos_Y = StringProperty(default = "",update = updateEmpty)
    ob_pos_Z = StringProperty(default = "",update = updateEmpty)
    
    color = FloatVectorProperty(
        size = 3,
        update = updateEmpty
    )
    
    
    
    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
        if not self.lastmode == self.mode_list:
            self.lastmode = self.mode_list
            self.updateInputs(self.mode_list)
    
    modes = [("Value","Value",""),("Vec3","Vec3",""),("Mesh","Mesh",""),("Selection","Selection",""),("Color","Color","")]
    
    mode_list = EnumProperty(
        name = "Debug Mode",
        items = modes,
        update = updateNode
    )

    ##\brief Empty method, to avoid exceptions in the update process.   
    def triggerData(self,context):
        return
    
    ##\brief Custom flooding method, returns the node's pointer.
    def floodObsolete(self,context):
        return [self.as_pointer()]
    
    ##\brief Re-calculates the node's data.  
    def recalculate(self):
        
        if len(self.inputs) > 0:
            if len(self.inputs[0].links) != 0:
                if self.mode_list == "Value":

                    floats = self.inputs[0].returnData()
                    string = ""
                    for f in floats:
                        string = string + str(f)[:8] + ", "
                        
                    string = string[:len(string)-2]
                    
                    self.value = string
               
                
        if len(self.inputs) > 1:       
            if len(self.inputs[1].links) != 0:   
                if self.mode_list == "Vec3":

                    array = self.inputs[1].returnData()[0]

                    self.stringX = str(array[0])
                    self.stringY = str(array[1])
                    self.stringZ = str(array[2])
                
                
        if len(self.inputs) > 2:       
            if len(self.inputs[2].links) != 0:      
                if self.mode_list == "Mesh":

                    obs = self.inputs[2].returnData()[0]
                    self.ob_name = obs[0].name
                    self.mesh_name = obs[0].data.name
                
                
        if len(self.inputs) > 3:      
            if len(self.inputs[3].links) != 0:
                if self.mode_list == "Selection":
                    sel = self.inputs[3].returnData()[0]

                    self.v_count = len(sel[0])
                    self.e_count = len(sel[1])
                    self.f_count = len(sel[2])
                    
        
        if len(self.inputs) > 4:      
            if len(self.inputs[4].links) != 0:
                if self.mode_list == "Color":
                    self.color = self.inputs[4].returnData()[0]
                
                    
                
        
        else:
            self.ob_name = ""
            self.stringX = ""
            self.stringY = ""
            self.stringZ = ""
            self.value = ""
            self.v_count = ""
            self.e_count = ""
            self.f_count = ""
        
        
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_FLOAT", "Value")
        self.inputs.new("socket_VEC3_F", "Vec3")
        self.inputs.new("socket_MESH", "Mesh")
        self.inputs.new("socket_SELECTION", "Selection")
        self.inputs.new("socket_COL", "Color")
        
        self.use_custom_color = True
        self.color = (1,1,1)
        
        self.updateNode(context)

    ##\brief GUI.     
    def draw_buttons(self, context, layout):
    
        #Needed for the update operator - this node gives the operator a self-reference so that the operator can backtrack to its caller and call this node's "recalculate()" method
        layout.context_pointer_set("CALLER", self)
    
        layout.separator()
        row1 = layout.row(align = True)
        row1.prop(self, "mode_list", "")
        layout.separator()
        if self.mode_list == "Value":
            layout.label(text = self.value)
        elif self.mode_list == "Vec3":
            row = layout.row(align = True)
            col1 = row.column(align = True)
            col2 = row.column(align = True)
            rowC11 = col1.row(align = True)
            rowC12 = col1.row(align = True)
            rowC13 = col1.row(align = True)
        
            rowC21 = col2.row(align = True)
            rowC22 = col2.row(align = True)
            rowC23 = col2.row(align = True)
        
            rowC11.label(text = "X:")
            rowC12.label(text = "Y:")
            rowC13.label(text = "Z:")
        
            rowC21.label(text = self.stringX)
            rowC22.label(text = self.stringY)
            rowC23.label(text = self.stringZ)
        
        elif self.mode_list == "Mesh":
            rowNO = layout.row(align = False)
            rowNO.label(text = self.ob_name, icon = 'OBJECT_DATA')
            rowNM = layout.row(align = False)
            rowNM.label(text = self.mesh_name, icon = 'MESH_DATA')
        
        elif self.mode_list == "Color":
            row1 = layout.row()
            if len(self.inputs[4].links) > 0:
                row1.label(text = "RGB: " + str(round(self.color[0],2)) + ", " + str(round(self.color[1],2)) + ", " + str(round(self.color[2],2)))
            else:
                row1.label(text = "RGB: NO INPUT")
            
        else:
            rowVC = layout.row(align = True)
            rowEC = layout.row(align = True)
            rowFC = layout.row(align = True)

            VCcol1 = rowVC.column(align = True)
            VCcol2 = rowVC.column(align = True)
            ECcol1 = rowEC.column(align = True)
            ECcol2 = rowEC.column(align = True)
            FCcol1 = rowFC.column(align = True)
            FCcol2 = rowFC.column(align = True)


            
            VCcol1.label("Vertices:")
            ECcol1.label("Edges:")
            FCcol1.label("Faces:")

            
            VCcol2.label(str(self.v_count))
            ECcol2.label(str(self.e_count))
            FCcol2.label(str(self.f_count))

            
            
        layout.operator("output.update", text="Update", emboss=True)
            
            
        layout.separator()   
        
        
        
    ##\brief Makes inputs and outputs visible, based on the node's current settings.    
    def updateInputs(self, context):
    
    
        #hide all inputs
        for input in self.inputs:
            input.enabled = False

        #add new inputs, based on the selected mode
        if self.mode_list == "Value":
            self.inputs[0].enabled = True
        elif self.mode_list == "Vec3":
            self.inputs[1].enabled = True
        elif self.mode_list == "Mesh":
            self.inputs[2].enabled = True
        elif self.mode_list == "Selection":
            self.inputs[3].enabled = True
        elif self.mode_list == "Color":
            self.inputs[4].enabled = True
        else:
            return()
            

        
        













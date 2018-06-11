##\package buildingGen.nodes.building_nodes_LST
# List nodes.


import bpy
from bpy.types import NodeTree, Node, NodeSocket

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatProperty

import custom_sockets


from . import building_NODETREE
from .building_NODETREE import *

from utils import utils_OBJ,utils_GEN,utils_GLO

        
##\brief Extract parts of a list.       
class LST_ExtractNode(buildingNode, BuildingTree):

    bl_idname = 'LST_ExtractNode'
    bl_label = 'Extract from List'
    bl_icon = 'NODETREE'
    
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
                
        #Check internal modes
        
        if self.ext_mode_last != self.ext_mode:
            self.ext_mode_last = self.ext_mode
            outdated = True
        
        
        
        if outdated:
            self.updateInputs(context)
            self.callObsolete(context)
        
        
        
        
             

     


    corrupted = BoolProperty(default = True, update = updateEmpty) 

    ext_mode_last = StringProperty(default = "",update = updateEmpty)
      
                    
                    
                    
                    
    modes = [("Range","Range",""),("Index","Index",""),("Before","Before",""),("After","After","")]
    
    
    
    
    
    ext_mode = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Extraction Modes",
        update = updateNode
    )
                    
    


    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
        #hide all inputs
        for input in self.inputs:
            if input.name != "List":
                input.enabled = False

        if len(self.inputs) == 6 and len(self.outputs) == 1:
            
            if self.ext_mode == "Range":
                self.inputs[1].enabled = True
                self.inputs[2].enabled = True
            elif self.ext_mode == "Index":
                self.inputs[3].enabled = True
            elif self.ext_mode == "Before":
                self.inputs[4].enabled = True
            elif self.ext_mode == "After":
                self.inputs[5].enabled = True
                    
                    
                    
                    
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_UNIV", "List")
        self.outputs.new("socket_UNIV", "List")
        
        #Range Inputs
        self.inputs.new("socket_INT", "Start")
        self.inputs.new("socket_INT", "End")

        
        #Index Inputs
        socket = self.inputs.new("socket_INT", "Index")
        socket.enabled = False
        
        #Before Inputs
        socket = self.inputs.new("socket_INT", "End")
        socket.enabled = False
        
        #After Inputs
        socket = self.inputs.new("socket_INT", "Start")
        socket.enabled = False
        
        
        self.use_custom_color = True
        self.color = (.7,.7,.7)
        


    ##\brief GUI.    
    def draw_buttons(self, context, layout):
        layout.separator()
        row1 = layout.row()
        row1.prop(self, "ext_mode", "")
        layout.separator()
        
    ##\brief Re-calculates the node's data.
    def recalculate(self):
    
        self.corrupted = False
                
        list = self.inputs[0].returnData()
        retlist = []
        
        dt = self.inputs[0].askForType()
    
        if self.ext_mode == "Range":
            start = int(self.inputs[1].returnData()[0])
            end = int(self.inputs[2].returnData()[0])
            

            for ind in range(start, end):
                retlist.append(list[ind])
                    
                
        elif self.ext_mode == "Index":
            index = int(self.inputs[3].returnData()[0])
            retlist.append(list[index])
            
            
        elif self.ext_mode == "Before":
            end = int(self.inputs[4].returnData()[0])
            

            for ind in range(0, end):
                retlist.append(list[ind])
                    
                
        elif self.ext_mode == "After":
            start = int(self.inputs[5].returnData()[0])
            

            for ind in range(start, len(list)):
                retlist.append(utils_OBJ.copyobj(list[ind]))
                
        self.outputs[0].setData(retlist,dt)

                
                
                
                
                
                
##\brief Adjusts two lists (length-wise).                 
class LST_AdjustNode(buildingNode, BuildingTree):

    bl_idname = 'LST_AdjustNode'
    bl_label = 'Adjust List'
    bl_icon = 'NODETREE'
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
                
        #Check internal modes
        
        if self.adj_mode_last != self.adj_mode:
            self.adj_mode_last = self.adj_mode
            outdated = True
        
        if self.ext_mode_last != self.ext_mode:
            self.ext_mode_last = self.ext_mode
            outdated = True
        
        
        
        if outdated:
            self.updateInputs(context)
            self.callObsolete(context)
        
        
        
        
    
          

     


    corrupted = BoolProperty(default = True, update = updateEmpty)

    adj_mode_last = StringProperty(default = "", update = updateEmpty)
    ext_mode_last = StringProperty(default = "", update = updateEmpty)
      
                    
                    
                    
                    
    modes = [("Cut","Cut",""),("Extend","Extend","")]
    extend_m = [("Repeat Last","Repeat Last",""),("Repeat List","Repeat List",""),("Repeat Range","Repeat Range",""),("Repeat Index","Repeat Index","")]
    
    
    
    
    
    adj_mode = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Adjust Modes",
        update = updateNode
    )
    
    ext_mode = EnumProperty(
        name = "Choose Mode",
        items = extend_m,
        description = "Extension Modes",
        update = updateNode
    )
                    
    


    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
        #hide all inputs
        for input in self.inputs:
            if not input.name.startswith("List"):
                input.enabled = False

        if len(self.inputs) == 5 and len(self.outputs) == 2:
            if self.adj_mode == "Extend":
                if self.ext_mode == "Repeat Range":
                    self.inputs[2].enabled = True
                    self.inputs[3].enabled = True
                elif self.ext_mode == "Repeat Index":
                    self.inputs[4].enabled = True
                    
                    
                    
                    
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_UNIV", "List 1")
        self.inputs.new("socket_UNIV", "List 2")
        self.outputs.new("socket_UNIV", "Return List 1")
        self.outputs.new("socket_UNIV", "Return List 2")
        
        #Range Inputs
        socket = self.inputs.new("socket_INT", "Start")
        socket.enabled = False
        socket = self.inputs.new("socket_INT", "End")
        socket.enabled = False

        
        #Index Inputs
        socket = self.inputs.new("socket_INT", "Index")
        socket.enabled = False
        
        
        self.use_custom_color = True
        self.color = (.7,.7,.7)
        


    ##\brief GUI.     
    def draw_buttons(self, context, layout):
        layout.separator()
        row1 = layout.row()
        row1.prop(self, "adj_mode", "")
        
        if self.adj_mode == "Extend":
            row2 = layout.row()
            row2.prop(self, "ext_mode", "")
        
        layout.separator()
        

    ##\brief Re-calculates the node's data.
    def recalculate(self):
    
        self.corrupted = False
        
        retlist1 = []
        retlist2 = []
        
        list1 = self.inputs[0].returnData()
        list2 = self.inputs[1].returnData()
        
        dt1 = self.inputs[0].askForType()
        dt2 = self.inputs[1].askForType()
 
        
        if self.adj_mode == "Extend":
        
            if self.ext_mode == "Repeat Last":
                
                if len(list1) > len(list2):
                
                    length = len(list2)
                    
                    for i in range(0,len(list1)):
                        retlist1.append(list1[i])
                        
                        if i<length:
                            retlist2.append(list2[i])
                        else:
                            if dt2 == "socket_MESH":
                                retlist2.append(utils_OBJ.copyobj(list2[length-1]))
                            else:
                                retlist2.append(list2[length-1])
                                
                                
                elif len(list1) < len(list2):
                

                    length = len(list1)
                    
                    for i in range(0,len(list2)):
                        retlist2.append(list2[i])
                        
                        if i<length:
                            retlist1.append(list1[i])
                        else:
                            if dt1 == "socket_MESH":
                                retlist1.append(utils_OBJ.copyobj(list1[length-1]))
                            else:
                                retlist1.append(list1[length-1])
                                
            
            if self.ext_mode == "Repeat List":
                
                if len(list1) > len(list2):

                    length = len(list1)
                    length_short = len(list2)
                    
                    for i in range(0,len(list1)):
                        retlist1.append(list1[i])

                        if dt2 == "socket_MESH":
                            retlist2.append(utils_OBJ.copyobj(list2[i%length_short]))
                        else:
                            retlist2.append(list2[i%length_short])
                                
                
                elif len(list1) < len(list2):

                    length = len(list2)
                    length_short = len(list1)
                    
                    for i in range(0,len(list2)):
                        retlist2.append(list2[i])

                        if dt1 == "socket_MESH":
                            retlist1.append(utils_OBJ.copyobj(list1[i%length_short]))
                        else:
                            retlist1.append(list1[i%length_short])
                            
                            
            elif self.ext_mode == "Repeat Range":
            
                start = int(self.inputs[2].returnData()[0])
                end = int(self.inputs[3].returnData()[0])
                
                if start > end:
                    temp = start
                    start = end
                    end = temp
                
                dis = end-start
                
                if len(list1) > len(list2):

                    st = max(0,start)
                    en = min(len(list2),end)
                    
                    for i in range(0,len(list1)):
                        retlist1.append(list1[i])

                        if dt2 == "socket_MESH":
                            retlist2.append(utils_OBJ.copyobj(list2[(i%dis)+start]))
                        else:
                            retlist2.append(list2[(i%dis)+start])
                            
                elif len(list1) < len(list2):

                    st = max(0,start)
                    en = min(len(list1),end)
                    
                    for i in range(0,len(list2)):
                        retlist2.append(list2[i])

                        if dt1 == "socket_MESH":
                            retlist1.append(utils_OBJ.copyobj(list1[(i%dis)+start]))
                        else:
                            retlist1.append(list1[(i%dis)+start])
                            
                            
                            
                            
            
            elif self.ext_mode == "Repeat Index":
            
                index = self.inputs[4].returnData()[0]
                
                
                
                if len(list1) > len(list2):

                    id = max(0,min(len(list2)-1,index))

                    length = len(list2)
                    
                    for i in range(0,len(list1)):
                        retlist1.append(list1[i])
                        
                        if i<length:
                            retlist2.append(list2[i])
                        else:
                            if dt2 == "socket_MESH":
                                retlist2.append(utils_OBJ.copyobj(list2[id]))
                            else:
                                retlist2.append(list2[id])
                                
                                
                elif len(list1) < len(list2):

                    id = max(0,min(len(list1)-1,index))

                    length = len(list1)
                    
                    for i in range(0,len(list2)):
                        retlist2.append(list2[i])
                        
                        if i<length:
                            retlist1.append(list1[i])
                        else:
                            if dt1 == "socket_MESH":
                                retlist1.append(utils_OBJ.copyobj(list1[id]))
                            else:
                                retlist1.append(list1[id])
            
            
                
        elif self.adj_mode == "Cut":

            if len(list1) > len(list2):
            
                length = len(list2)
                
                retlist2 = list2
                retlist1 = list1[:length]
                
                if dt1 == "socket_MESH":
                    for i in range(length+1,len(list1)):
                        list1[i].name = "_$OBS$_"
                        
                
                            
            elif len(list1) < len(list2):
            
                length = len(list1)
                
                retlist1 = list1
                retlist2 = list2[:length]
                
                if dt2 == "socket_MESH":
                    for i in range(length+1,len(list2)):
                        list2[i].name = "_$OBS$_"
                            
            else:
                retlist1 = list1
                retlist2 = list2
                            

        self.outputs[0].setData(retlist1,dt1)
        self.outputs[1].setData(retlist2,dt2)
                        
                    
                    
                
                            
        
        
        
        
        
        
        
        
        
        
        
        
        
##\brief Extracts data from a list.
#\detail Currently only the length of a list.        
class LST_DataNode(buildingNode, BuildingTree):

    
    bl_idname = 'LST_DataNode'
    bl_label = 'List Data'
    bl_icon = 'NODETREE'
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
                
        #Check internal modes
        
        
        
        if outdated:
            self.callObsolete(context)
        
        
        
        
    
    corrupted = BoolProperty(default = True, update = updateEmpty)          
                    
                    
                    
                    
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_UNIV", "List")
        self.outputs.new("socket_INT", "Length")
        
        self.use_custom_color = True
        self.color = (.7,.7,.7)
        


    ##\brief GUI.    
    def draw_buttons(self, context, layout):
        layout.separator()
        
    ##\brief Re-calculates the node's data.
    def recalculate(self):
    
        self.corrupted = False

        list = self.inputs[0].returnData()
        
        l = len(list)
        
        self.outputs[0].setData([l])
        
            
        

        
        
        
##\brief Appends multiple lists.        
class LST_AppendNode(buildingNode, BuildingTree):

    
    bl_idname = 'LST_AppendNode'
    bl_label = 'Append Lists'
    bl_icon = 'NODETREE'
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
                
        #Check internal modes
        
        
        
        if outdated:
            self.callObsolete(context)
        
        
    
            

     


    corrupted = BoolProperty(default = True, update = updateEmpty) 
            

                    
                    
                    
                    
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_UNIV", "List 1")
        self.inputs.new("socket_UNIV", "List 2")
        self.inputs.new("socket_UNIV", "List 3")
        self.inputs.new("socket_UNIV", "List 4")
        self.inputs.new("socket_UNIV", "List 5")
        self.outputs.new("socket_UNIV", "List")
        
        self.use_custom_color = True
        self.color = (.7,.7,.7)
        


    ##\brief GUI.      
    def draw_buttons(self, context, layout):
        layout.separator()
        
    ##\brief Re-calculates the node's data.
    def recalculate(self):
    
        self.corrupted = False
        
        retlist = []
        
        dt = "socket_MESH"
        datatype = None
        
        for x in range (0, 5):
            if len(self.inputs[x].links) > 0:
            
                dt = self.inputs[0].askForType()
            
                data = self.inputs[x].returnData()
            
                if datatype == None:
                    datatype = type(data[0])
                elif type(data[0]) != datatype:
                    continue

                retlist.extend(data)
                
        self.outputs[0].setData(retlist,dt)
                    
                    
        
        
        
        
        
        

        
        
        
        
        
        
##\brief Extends a list.     
class LST_ExtendNode(buildingNode, BuildingTree):

    
    bl_idname = 'LST_ExtendNode'
    bl_label = 'Extend Lists'
    bl_icon = 'NODETREE'
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
                
        #Check internal modes
        
        if self.ext_mode_last != self.ext_mode:
            self.ext_mode_last = self.ext_mode
            outdated = True
        
        
        
        if outdated:
            self.updateInputs(context)
            self.floodObsolete(context)
        
        
        
        
    
           

     


    corrupted = BoolProperty(default = True, update = updateEmpty) 
    retlist = []

    ext_mode_last = StringProperty(default = "")
      
                    
                    
                    
                    
    modes = [("Repeat Last","Repeat Last",""),("Repeat List","Repeat List",""),("Repeat Range","Repeat Range",""),("Repeat Index","Repeat Index","")]
    
    
    
    
    
    ext_mode = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Extraction Modes",
        update = updateNode
    )
                    
    


    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
        #hide all inputs
        for input in self.inputs:
            if input.name != "List" and input.name != "Count":
                input.enabled = False

        if len(self.inputs) == 5 and len(self.outputs) == 1:
            
            if self.ext_mode == "Repeat Range":
                self.inputs[2].enabled = True
                self.inputs[3].enabled = True
            elif self.ext_mode == "Repeat Index":
                self.inputs[4].enabled = True

                    
                    
                    
                    
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_UNIV", "List")
        self.inputs.new("socket_INT", "Count")
        self.outputs.new("socket_UNIV", "List")
        
        #Range Inputs
        socket = self.inputs.new("socket_INT", "Start")
        socket.enabled = False
        socket = self.inputs.new("socket_INT", "End")
        socket.enabled = False
        
        #Index Inputs
        socket = self.inputs.new("socket_INT", "Index")
        socket.enabled = False
        

        
        
        self.use_custom_color = True
        self.color = (.7,.7,.7)
        


    ##\brief GUI.      
    def draw_buttons(self, context, layout):
        layout.separator()
        row1 = layout.row()
        row1.prop(self, "ext_mode", "")
        layout.separator()
       


    ##\brief Re-calculates the node's data.
    def recalculate(self):
    
        self.corrupted = False

        count = int(self.inputs[1].returnData()[0])
        retlist = self.inputs[0].returnData()
    
        if self.ext_mode == "Repeat Last":
            lastInd = len(retlist)-1

            for ind in range (0,count):
                retlist.append(retlist[lastInd])
                
        elif self.ext_mode == "Repeat List":

            for ind in range (0, count):
                retlist.append(retlist[ind])
                
        elif self.ext_mode == "Repeat Range":
            start = int(self.inputs[2].returnData()[0])
            modulo = int(self.inputs[3].returnData()[0]) - start

            for ind in range (0,count):
                retlist.append(retlist[start + count%modulo])
                
        elif self.ext_mode == "Repeat Index":
            index = int(self.inputs[4].returnData()[0]%len(retlist))

            for ind in range(0,count):
                retlist.append(retlist[index])
                
        self.outputs[0].setData(retlist)
                
                
                
                
                
                
                
                
                
                
                
                
#\brief Rearranges a list.               
class LST_MoveNode(buildingNode, BuildingTree):

    
    bl_idname = 'LST_MoveNode'
    bl_label = 'Rearrange List'
    bl_icon = 'NODETREE'
    
    ##\brief An empty function to silence some custom property updates.
    #\detail The superclass method cannot be used, Properties can't find it.
    def updateEmpty(self,context):
        return
    

    ##\brief Checks whether the node needs to be updated.
    def updateNode(self, context):
    
        self.updateInputs(context)
    
        outdated = False
        
        #Check connections
        
        for input in self.inputs:
            if input.check_outdated():
                outdated = True
                
        #Check internal modes
        
        if self.move_mode_last != self.move_mode:
            self.move_mode_last = self.move_mode
            outdated = True
        
        
        
        if outdated:
            self.updateInputs(context)
            self.floodObsolete(context)
        
        
        
        
    
          

     


    corrupted = BoolProperty(default = True, update = updateEmpty) 
    retlist = []

    move_mode_last = StringProperty(default = "")
      
                    
                    
                    
                    
    modes = [("Offset Range","Offset Range",""),("Offset Element","Offset Element",""),("Delete Range","Delete Range",""),("Delete Element","Delete Element",""),("Randomize Order","Randomize Order",""),("Invert Order","Invert Order",""),("Switch","Switch","")]
    switch_m = [("Element with Element","Element with Element",""),("Element with Range","Element with Range",""),("Range with Element","Range with Element",""),("Range with Range","Range with Range","")]
    
    
    
    
    
    move_mode = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Modes",
        update = updateNode
    )
    
    switch_mode = EnumProperty(
        name = "Choose Mode",
        items = switch_m,
        description = "Modes",
        update = updateNode
    )
                    
    


    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
        #hide all inputs
        for input in self.inputs:
            if input.name != "List":
                input.enabled = False

        if len(self.inputs) == 8 and len(self.outputs) == 1:
            if self.move_mode == "Offset Range":
                self.inputs[1].enabled = True
                self.inputs[2].enabled = True
                self.inputs[3].enabled = True
            elif self.move_mode == "Offset Element":
                self.inputs[4].enabled = True
                self.inputs[1].enabled = True
            elif self.move_mode == "Delete Range":
                self.inputs[2].enabled = True
                self.inputs[3].enabled = True
            elif self.move_mode == "Delete Element":
                self.inputs[4].enabled = True
            elif self.move_mode == "Randomize Order":
                self.inputs[2].enabled = True
                self.inputs[3].enabled = True
            elif self.move_mode == "Invert Order":
                self.inputs[2].enabled = True
                self.inputs[3].enabled = True
            elif self.move_mode == "Switch":
                if self.switch_mode == "Element with Element":
                    self.inputs[4].enabled = True
                    self.inputs[7].enabled = True
                elif self.switch_mode == "Element with Range" or self.switch_mode == "Range with Element":
                    self.inputs[4].enabled = True
                    self.inputs[2].enabled = True
                    self.inputs[3].enabled = True
                elif self.switch_mode == "Range with Range":
                    self.inputs[2].enabled = True
                    self.inputs[3].enabled = True
                    self.inputs[5].enabled = True
                    self.inputs[6].enabled = True
                
                    
                    
                    
                    
    
    ##\brief Initializes the node.
    def init(self, context):
        self.inputs.new("socket_UNIV", "List")
        self.outputs.new("socket_UNIV", "List")
        
        self.inputs.new("socket_INT", "Offset")
        self.inputs.new("socket_INT", "Start")
        self.inputs.new("socket_INT", "End")
        socket = self.inputs.new("socket_INT", "Index")
        socket.enabled = False
        
        socket = self.inputs.new("socket_INT", "Start 2")
        socket.enabled = False
        socket = self.inputs.new("socket_INT", "End 2")
        socket.enabled = False
        socket = self.inputs.new("socket_INT", "Index 2")
        socket.enabled = False
        
        

        
        
        self.use_custom_color = True
        self.color = (.7,.7,.7)
        
        self.updateInputs(context)


    ##\brief GUI.   
    def draw_buttons(self, context, layout):
        layout.separator()
        row1 = layout.row()
        row1.prop(self, "move_mode", "")
        if self.move_mode == "Switch":
            row2 = layout.row()
            row2.prop(self, "switch_mode", "")
        layout.separator()
        

    ##\brief Re-calculates the node's data.
    def recalculate(self, output):
    
        self.corrupted = False

        
        
        

        
                
                
            
        
        
        
            

        
        













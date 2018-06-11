##@package buildingGen.custom_sockets
# Node Sockets


import bpy
import mathutils
from nodes import building_NODETREE
from nodes.building_NODETREE import buildingSocket
from bpy.props import EnumProperty, StringProperty, BoolProperty, FloatProperty, FloatVectorProperty, CollectionProperty, IntProperty
import random

from utils import utils_OBJ,utils_GEN,utils_GLO
from utils.utils_GLO import print_debug





##@brief Mesh/Geometry Socket
class socket_MESH(buildingSocket):

    ##\property bl_idname
    #\brief Name of the socket.
    bl_idname = "socket_MESH"
    
    ##\property bl_label
    #\brief Label of the socket.
    bl_label = "Mesh"
    
    
    def updateEmpty(self,context):
        return
     
    def notify(self,context):
        self.node.callObsolete(context)

 
    ##\property conSocL
    #\brief Last connected socket.
    #\detail Pointer to the connected socket's internal Blender data.
    conSocL = StringProperty(default = ".",update = updateEmpty)

    
    
    ##\fn check_outdated
    #\brief Checks for outdated properties.
    #\returns (Boolean) Whether outdated or not.
    def check_outdated(self):
        if self.enabled and not self.is_output:
            outdated = False

            
            if len(self.links) > 0 and self.conSocL != str(self.links[0].from_socket.as_pointer()):
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
                
            elif len(self.links) > 0 and self.conSocL == ".":
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
            elif len(self.links) == 0 and self.conSocL != ".":
                self.conSocL = "."
                outdated = True
            

            return outdated

        return False
 

    def setStandard(mesh):
        return
 
    #DATA
    standard_data = None
 
 
    ##\fn draw
    #\brief GUI
    def draw(self, context, layout, node, x):
        layout.label(self.name)
                
            

        
    ##\fn draw_color
    #\brief socket color
    def draw_color(self, context, node):
        return (1,.5,0,1)

    

    
    

        
        

        
        

        
##@brief Vector Socket		
class socket_VEC3_F(buildingSocket):

    ##\property bl_idname
    #\brief Name of the socket.
    bl_idname = "socket_VEC3_F"
    
    ##\property bl_label
    #\brief Label of the socket.
    bl_label = "Vec3 Float"
    
    
    def updateEmpty(self,context):
        return
     
    def notify(self,context):
        self.node.callObsolete(context)
    

    

    #UPDATE DATA
    
    ##\property conSocL
    #\brief Last connected socket.
    #\detail Pointer to the connected socket's internal Blender data.
    conSocL = StringProperty(default = ".",update = updateEmpty)
    
    
    vec1_0_last = FloatProperty(default = 0,update = updateEmpty)
    vec1_1_last = FloatProperty(default = 0,update = updateEmpty)
    vec1_2_last = FloatProperty(default = 0,update = updateEmpty)
    
    
    
    ##\property vec1_0
    #\brief X-value of the vector (used for GUI).
    vec1_0 = FloatProperty(
        name = "X-VAL",
        default = 0.0,
        update = notify
    )
    
    ##\property vec1_1
    #\brief Y-value of the vector (used for GUI).
    vec1_1 = FloatProperty(
        name = "Y-VAL",
        default = 0.0,
        update = notify
    )
    
    
    ##\property vec1_2
    #\brief Z-value of the vector (used for GUI).
    vec1_2 = FloatProperty(
        name = "Z-VAL",
        default = 0.0,
        update = notify
    )
    
    
    ##\property edit_vec
    #\brief Show or hide the standard vector.
    edit_vec = BoolProperty(
        default = False,
        update = updateEmpty
    )
    
    
    
    
    
    
    
    
    
    ##\fn check_outdated
    #\brief Checks for outdated properties.
    #\returns (Boolean) Whether outdated or not.
    def check_outdated(self):
        if self.enabled and not self.is_output:
            outdated = False

            
            if len(self.links) > 0 and self.conSocL != str(self.links[0].from_socket.as_pointer()):
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
                
            elif len(self.links) > 0 and self.conSocL == ".":
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
            elif len(self.links) == 0 and self.conSocL != ".":
                self.conSocL = "."
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
                
                


            return outdated

        return False
        
        
        
    def setStandard(self, vector):
        return
        
        
    
    #DATA
    standard_data = mathutils.Vector([0,0,0])
    
    
    
    ##\fn draw
    #\brief GUI
    def draw(self, context, layout, node, x):
        if len(self.links) == 0 and not self.is_output:
            box1 = layout.box()
            row = box1.row()
            row.label(self.name)
            row.prop(self,"edit_vec","",icon="TRIA_DOWN" if self.edit_vec else "TRIA_RIGHT",icon_only=True, emboss=False)
            if self.edit_vec:
                row2 = box1.row(align = True)
                row2.prop(self,"vec1_0","")
                row2.prop(self,"vec1_1","")
                row2.prop(self,"vec1_2","")
                
        else:
            layout.label(self.name)
                
                
                
                
            
            
    ##\fn draw_color
    #\brief socket color
    def draw_color(self, context, node):
        return (.3,.8,.4,1)
        
        
    ##\fn returnData
    #\brief overriding buildingSocket's returnData().
    #\detail Vec3 sockets have the ability to return basic vectors if the socket is not connected. These vectors are stored in three separate properties. To be able to return that data, too, Vec3 sockets override buildingSocket's default method.
    #\returns list of whatever data its connected counterpart offers to it
    def returnData(self):
        if len(self.links) == 0:
        
            vec = mathutils.Vector([self.vec1_0,self.vec1_1,self.vec1_2])
            print_debug("Returning Data:",self.name,"/",vec)
            return [vec]
        else:
            node_output = self.links[0].from_socket
            return node_output.getData()
        
        
        
        
        
        

        

##@brief Selection Socket       
class socket_SELECTION(buildingSocket):

    ##\property bl_idname
    #\brief Name of the socket.
    bl_idname = "socket_SELECTION"
    
    ##\property bl_label
    #\brief Label of the socket.
    bl_label = "Selection"
    
    def updateEmpty(self,context):
        return
     
    def notify(self,context):
        self.node.callObsolete(context)
    

    m = [("fev","All",""),("f","Only Faces",""),("e","Only Edges",""),("v","Only vertices",""),("ev","No Faces",""),("fv","No Edges",""),("fe","No Vertices","")]
        
    ##\property sel_mode
    #\brief Selection Mode.
    #\detail In code, the selection modes are represented as a string. If the string includes "v", vertices are selected, same for "e" and "f". "Select All" is encoded as the combination "fev".
    sel_mode = EnumProperty(default = "fev", items = m, update = notify)
    
    ##\property sel_inv
    #\brief Whether to invert the selection.
    sel_inv = BoolProperty(default = False,update = notify)
    
    ##\property sel_vgroup
    #\brief The Vertex Group to select.
    sel_vgroup = StringProperty(default = "",update = notify)
    
    
    sel_mode_l = StringProperty(default = "",update = updateEmpty)
    sel_vgroup_l = StringProperty(default = "",update = updateEmpty)
    sel_inv_l = BoolProperty(default = False,update = updateEmpty)


    
    #UPDATE DATA
    
    ##\property conSocL
    #\brief Last connected socket.
    #\detail Pointer to the connected socket's internal Blender data.
    conSocL = StringProperty(default = ".",update = updateEmpty)
    
    
    
    ##\property edit_sel
    #\brief Show or hide the selection modes.
    edit_sel = BoolProperty(default = False,update = updateEmpty)
    
    
    ##\fn check_outdated
    #\brief Checks for outdated properties.
    #\returns (Boolean) Whether outdated or not.
    def check_outdated(self):
    
        outdated = False
            
    
        if self.enabled and not self.is_output:
            
            if len(self.links) > 0 and self.conSocL != str(self.links[0].from_socket.as_pointer()):
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
                
            elif len(self.links) > 0 and self.conSocL == ".":
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
            elif len(self.links) == 0 and self.conSocL != ".":
                self.conSocL = "."
                outdated = True
                
            if self.sel_mode_l != self.sel_mode:
                self.sel_mode_l = self.sel_mode
                outdated = True
                
            if self.sel_inv_l != self.sel_inv:
                self.sel_inv_l = self.sel_inv
                outdated = True
                
            if self.sel_vgroup_l != self.sel_vgroup:
                self.sel_vgroup_l = self.sel_vgroup
                outdated = True
            
        return outdated

    
    
    def setStandard(sel):
        return
 
    #DATA
    standard_data = StringProperty(default ="X", update = updateEmpty)
 
 
    ##\fn draw
    #\brief GUI
    def draw(self, context, layout, node, x):
        if self.is_output:
            layout.label(self.name)
        else:
            box1 = layout.box()
            row1 = box1.row()
            row1.label(self.name)
            row1.prop(self,"edit_sel","",icon="TRIA_DOWN" if self.edit_sel else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_sel:
            
                row2 = box1.row()
                row2.prop(self, "sel_mode", "")
                row2.prop(self, "sel_inv", "Invert")
                row3 = box1.row()
                row3.label("V-Group")
                row3.prop(self, "sel_vgroup","")
            
            
            
    ##\fn draw_color
    #\brief socket color
    def draw_color(self, context, node):
        return (.2,.7,1,1)

        
        


        
        
##@brief Float Socket       
class socket_FLOAT(buildingSocket):

    ##\property bl_idname
    #\brief Name of the socket.
    bl_idname = "socket_FLOAT"
    
    ##\property bl_label
    #\brief Label of the socket.
    bl_label = "Float"
    
    
    def updateEmpty(self,context):
        return
     
    def notify(self,context):
        self.node.callObsolete(context)
    
        
    
 
    #UPDATE DATA
    
    ##\property conSocL
    #\brief Last connected socket.
    #\detail Pointer to the connected socket's internal Blender data.
    conSocL = StringProperty(default = ".",update = updateEmpty)
    
    
    ##\fn check_outdated
    #\brief Checks for outdated properties.
    #\returns (Boolean) Whether outdated or not.
    def check_outdated(self):
        if self.enabled and not self.is_output:
            outdated = False

            
            if len(self.links) > 0 and self.conSocL != str(self.links[0].from_socket.as_pointer()):
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
                
            elif len(self.links) > 0 and self.conSocL == ".":
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
            elif len(self.links) == 0 and self.conSocL != ".":
                self.conSocL = "."
                outdated = True
                
            if self.standard_data_last != self.standard_data:
                self.standard_data_last = self.standard_data
                outdated = True
            

            return outdated

        return False
 
    
    def setStandard(self, val):
        self.standard_data = val
 
    #DATA
    
    ##\property standard_data
    #\brief Standard float.
    #\detail Gets returned if no sockets are connected.
    standard_data = FloatProperty(default = 0.0, update = notify)
    standard_data_last = FloatProperty(default = 0.0, update = updateEmpty)
    
    
    ##\property edit_float
    #\brief Show or hide the standard float.
    edit_float = BoolProperty(
        default = False,
        update = updateEmpty
    )
 

    ##\fn draw
    #\brief GUI
    def draw(self, context, layout, node, x):
        if not self.is_output and len(self.links) == 0:
            box1 = layout.box()
            row = box1.row()
            row.label(self.name)
            row.prop(self,"edit_float","",icon="TRIA_DOWN" if self.edit_float else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_float:
                row2 = box1.row()
                row2.prop(self,"standard_data","")
                
        else:
            layout.label(self.name)
       

       
    ##\fn draw_color
    #\brief socket color
    def draw_color(self, context, node):
        return (1,0,.25,1)

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

   
        
##@brief Integer Socket       
class socket_INT(buildingSocket):

    ##\property bl_idname
    #\brief Name of the socket.
    bl_idname = "socket_INT"
    
    ##\property bl_label
    #\brief Label of the socket.
    bl_label = "Integer"
    
    def updateEmpty(self,context):
        return
        
    def notify(self,context):
        self.node.callObsolete(context)
    
    
        
 
    #UPDATE DATA
    
    ##\property conSocL
    #\brief Last connected socket.
    #\detail Pointer to the connected socket's internal Blender data.
    conSocL = StringProperty(default = ".",update = updateEmpty)
    
    
    
    
    ##\fn check_outdated
    #\brief Checks for outdated properties.
    #\returns (Boolean) Whether outdated or not.
    def check_outdated(self):
        if self.enabled and not self.is_output:
            outdated = False

            
            if len(self.links) > 0 and self.conSocL != str(self.links[0].from_socket.as_pointer()):
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
                
            elif len(self.links) > 0 and self.conSocL == ".":
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
            elif len(self.links) == 0 and self.conSocL != ".":
                self.conSocL = "."
                outdated = True
            

            return outdated

        return False
 
 
 
 
    def setStandard(self, val):
        self.standard_data = int(val)
 
    #DATA
    
    ##\property standard_data
    #\brief Standard integer.
    #\detail Gets returned if no sockets are connected.
    standard_data = IntProperty(default = 0, update = notify)
    standard_data_last = IntProperty(default = 0, update = updateEmpty)
 
 
 
 
    ##\property edit_int
    #\brief Show or hide the standard integer.
    edit_int = BoolProperty(
        default = False,
        update = updateEmpty
    )
 

    ##\fn draw
    #\brief GUI
    def draw(self, context, layout, node, x):
        if not self.is_output and len(self.links) == 0:
            box1 = layout.box()
            row = box1.row()
            row.label(self.name)
            row.prop(self,"edit_int","",icon="TRIA_DOWN" if self.edit_int else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_int:
                row2 = box1.row()
                row2.prop(self,"standard_data","")
                
        else:
            layout.label(self.name)
 
 
    ##\fn draw_color
    #\brief socket color
    def draw_color(self, context, node):
        return (.8,.8,.8,1)












        

            
            
##@brief Universal Socket           
class socket_UNIV(buildingSocket):

    ##\property bl_idname
    #\brief Name of the socket.
    bl_idname = "socket_UNIV"
    
    ##\property bl_label
    #\brief Label of the socket.
    bl_label = "Universal"
    
    def updateEmpty(self,context):
        return
        
    
    
    
        
    
    
    #UPDATE DATA
    
    ##\property conSocL
    #\brief Last connected socket.
    #\detail Pointer to the connected socket's internal Blender data.
    conSocL = StringProperty(default = ".",update = updateEmpty)
    
    
    ##\fn check_outdated
    #\brief Checks for outdated properties.
    #\returns (Boolean) Whether outdated or not.
    def check_outdated(self):
        if self.enabled and not self.is_output:
            outdated = False

            
            if len(self.links) > 0 and self.conSocL != str(self.links[0].from_socket.as_pointer()):
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
                
            elif len(self.links) > 0 and self.conSocL == ".":
                self.conSocL = str(self.links[0].from_socket.as_pointer())
                outdated = True
            elif len(self.links) == 0 and self.conSocL != ".":
                self.conSocL = "."
                outdated = True
            

            return outdated

        return False
        
        
        
    def setStandard(self, data):
        self.standard_data = data
    
    #DATA
    standard_data = None

        
        
    
    
    ##\fn draw
    #\brief GUI
    def draw(self, context, layout, node, x):
        layout.label(self.name)
 
 
    ##\fn draw_color
    #\brief socket color
    def draw_color(self, context, node):
        return (.2,.2,.2,1)
        

            
            
            
            
            
            

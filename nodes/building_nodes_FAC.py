##\package buildingGen.nodes.building_nodes_FAC
# Facade nodes.



import bpy
import bmesh
import random
from bpy.types import NodeTree, Node, NodeSocket

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

from bpy.props import EnumProperty, StringProperty, BoolProperty, FloatProperty, FloatVectorProperty

import custom_sockets


from . import building_NODETREE
from .building_NODETREE import *

from utils import utils_GEN, utils_MATH, utils_OBJ, utils_GEOM, utils_SEL,utils_GLO
from utils.utils_GLO import print_debug
import mathutils
import math
from random import randrange





        

        
##\brief Replaces polygons with pre-made tiles.
#\detail Fits tile objects to polygons of a second object. In case you want a special cage, put the tile's cage in the tile object and assign it to a vertex group named "cage". Cages have to have rectangular shape and 4 vertices.      
class FAC_PolyNode(buildingNode):


    bl_idname = 'FAC_PolyNode'

    bl_label = 'Polygon'

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
            
      
        if self.mode_list_last != self.mode_list:
            self.mode_list_last = self.mode_list
            outdated = True
            
        if self.point_normal_last != self.point_normal:
            self.point_normal_last = self.point_normal
            outdated = True
            
        if self.dominant_last != self.dominant:
            self.dominant_last = self.dominant
            outdated = True
        
        if self.tileMode_last != self.tileMode:
            self.tileMode_last = self.tileMode
            outdated = True
    
        if self.fallback_last != self.fallback:
            self.fallback_last = self.fallback
            outdated = True
            
        if self.tileDom_last != self.tileDom:
            self.tileDom_last = self.tileDom
            outdated = True
            
        if self.tileSubdom_last != self.tileSubdom:
            self.tileSubdom_last = self.tileSubdom
            outdated = True
            
        if self.area_tiling_dom_last != self.area_tiling_dom:
            self.area_tiling_dom_last = self.area_tiling_dom
            outdated = True
            
        if self.area_tiling_subdom_last != self.area_tiling_subdom:
            self.area_tiling_subdom_last = self.area_tiling_subdom
            outdated = True
            
        if self.area_align_dom_last != self.area_align_dom:
            self.area_align_dom_last = self.area_align_dom
            outdated = True
            
        if self.area_align_subdom_last != self.area_align_subdom:
            self.area_align_subdom_last = self.area_align_subdom
            outdated = True

            
        if self.area_align_Z_last != self.area_align_Z:
            self.area_align_Z_last = self.area_align_Z
            outdated = True
            
 
        if self.quad_morph_last != self.quad_morph:
            self.quad_morph_last = self.quad_morph
            outdated = True
            
        if self.tri_morph_last != self.tri_morph:
            self.tri_morph_last = self.tri_morph
            outdated = True
            
        if self.quad_cut_last != self.quad_cut:
            self.quad_cut_last = self.quad_cut
            outdated = True
            
        if self.tri_cut_last != self.tri_cut:
            self.tri_cut_last = self.tri_cut
            outdated = True

            
        if self.ngon_cut_last != self.ngon_cut:
            self.ngon_cut_last = self.ngon_cut
            outdated = True
            
        if self.area_scale_Z_last != self.area_scale_Z:
            self.area_scale_Z_last = self.area_scale_Z
            outdated = True
            
        if self.point_cut_last != self.point_cut:
            self.point_cut_last = self.point_cut
            outdated = True
            
        if self.point_cut_nors_last != self.point_cut_nors:
            self.point_cut_nors_last = self.point_cut_nors
            outdated = True
        
            

        
        
           
        
        if outdated:
            self.updateInputs(context)
            self.callObsolete(context)


    
	#NODE DATA
    
    corrupted = BoolProperty(default = True, update = updateEmpty)
    
    
    #data checking
    mode_list_last = StringProperty(default = "",update = updateEmpty)
    point_normal_last = StringProperty(default = "",update = updateEmpty)
    dominant_last = StringProperty(default = "",update = updateEmpty)
    tileMode_last = StringProperty(default = "",update = updateEmpty)
    fallback_last = StringProperty(default = "",update = updateEmpty)
    tileDom_last = BoolProperty(default = True, update = updateEmpty)
    tileSubdom_last = BoolProperty(default = True, update = updateEmpty)
    area_tiling_dom_last = StringProperty(default = "",update = updateEmpty)
    area_tiling_subdom_last = StringProperty(default = "",update = updateEmpty)
    area_align_dom_last = StringProperty(default = "",update = updateEmpty)
    area_align_subdom_last = StringProperty(default = "",update = updateEmpty)
    area_align_Z_last = BoolProperty(default = True, update = updateEmpty)

    quad_morph_last = StringProperty(default = "",update = updateEmpty)
    quad_morph_d_last = StringProperty(default = "",update = updateEmpty)
    tri_morph_last = StringProperty(default = "",update = updateEmpty)
    quad_cut_last = StringProperty(default = "",update = updateEmpty)
    tri_cut_last = StringProperty(default = "",update = updateEmpty)
    ngon_cut_last = StringProperty(default = "",update = updateEmpty)
    point_cut_last = BoolProperty(default = True, update = updateEmpty)
    point_cut_nors_last = BoolProperty(default = True, update = updateEmpty)
    
    
    
    area_scale_Z_last = StringProperty(default = "",update = updateEmpty)
    
    
    
    
    

    
    modes = [("Area","Polygon Area",""),("Point","Place on Polygons","")]
    
    
    point_nors = [("Poly Normal","Poly Normal",""),("Vector","Vector","")]
    axes_strict = [("X","X",""),("Y","Y",""),("Z","Z",""),("-X","-X",""),("-Y","-Y",""),("-Z","-Z","")]
    
    point_tile_m = [("Single Random","Single Random",""),("Random","Random","")]
    tiling = [("s","Stretch",""),("t","Array","")]
    aligns = [("c","Center",""),("t","Top",""),("b","Bottom","")]
    
    cuts = [("ds","All",""),("d","Dominant",""),("s","Subdominant",""),("x","None","")]
    cuts_bin = [("c","All",""),("x","None","")]
    
    q_m = [("ds","Morph All",""),("d","Morph Dominant",""),("s","Morph Subdominant",""),("x","Cage","")]
    
    morph_t = [("m","Morph (Quad)",""),("p","Morph (Pinch)",""),("x","Cage","")]
    
    scaleZ = [("a","Average",""),("g","Greater",""),("s","Smaller",""),("x","Don't Scale","")]

    
    mode_list = EnumProperty(
        name = "Choose Mode",
        items = modes,
        default = "Point",
        description = "Poly Modes",
        update = updateNode
    )
    
    point_normal = EnumProperty(
        name = "Choose Mode",
        items = point_nors,
        description = "Point Normal Modes",
        update = updateNode
    )
    
    dominant = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        default = "Z",
        description = "Point Dominant Axis",
        update = updateNode
    )
    
    fallback = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        default = "X",
        description = "Fallback Dominant Axis",
        update = updateNode
    )
    
    
    tileMode = EnumProperty(
        name = "Choose Mode",
        items = point_tile_m,
        description = "Tile Mode",
        update = updateNode
    )
    
    tileDom = BoolProperty(
        name = "Choose Mode",
        default = False,
        description = "Randomize tiles (dominant axis)",
        update = updateNode
    )
    
    tileSubdom = BoolProperty(
        name = "Choose Mode",
        default = False,
        description = "Randomize tiles (subdominant axis)",
        update = updateNode
    )
 
    area_tiling_dom = EnumProperty(
        name = "Choose Mode",
        items = tiling,
        description = "Tile Mode",
        update = updateNode
    )
    
    area_tiling_subdom = EnumProperty(
        name = "Choose Mode",
        items = tiling,
        description = "Tile Mode",
        update = updateNode
    )
    
    area_align_dom = EnumProperty(
        name = "Choose Mode",
        items = aligns,
        description = "Tile Mode",
        update = updateNode
    )
    
    area_align_subdom = EnumProperty(
        name = "Choose Mode",
        items = aligns,
        description = "Tile Mode",
        update = updateNode
    )
    
    
    area_align_Z = BoolProperty(
        name = "Choose Mode",
        default = False,
        description = "Corrects seams of Z-offsetted tile vertices",
        update = updateNode
    )
    
    
    quad_morph = EnumProperty(
        name = "Choose Mode",
        items = q_m,
        description = "Quad Morph Mode",
        update = updateNode
    )
    
    tri_morph = EnumProperty(
        name = "Choose Mode",
        items = morph_t,
        description = "Tri Morph Mode",
        update = updateNode
    )
    

    quad_cut = EnumProperty(
        name = "Choose Mode",
        items = cuts,
        description = "Quad Cut Mode",
        update = updateNode
    )
    
    tri_cut = EnumProperty(
        name = "Choose Mode",
        items = cuts,
        description = "Tri Cut Mode",
        update = updateNode
    )
    
    ngon_cut = EnumProperty(
        name = "Choose Mode",
        items = cuts_bin,
        description = "NGon Cut Mode",
        update = updateNode
    )
    
    area_scale_Z = EnumProperty(
        name = "Choose Mode",
        items = scaleZ,
        description = "Z Scale Mode",
        update = updateNode
    )
    
    point_cut = BoolProperty(
        name = "Choose Mode",
        default = False,
        description = "Cut along polygon sides",
        update = updateNode
    )
    
    point_cut_nors = BoolProperty(
        name = "Choose Mode",
        default = False,
        description = "Cut along polygon sides",
        update = updateNode
    )
    
    
    
    
    edit_dominant = BoolProperty(
        default = False,
        update = updateEmpty
    )
    
    edit_tilemesh = BoolProperty(
        default = False,
        update = updateEmpty
    )
    
    edit_tilealign = BoolProperty(
        default = False,
        update = updateEmpty
    )
    
    edit_polymode = BoolProperty(
        default = False,
        update = updateEmpty
    )
    
    edit_normal = BoolProperty(
        default = False,
        update = updateEmpty
    )


    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
        #make all inputs visible
        for input in self.inputs:
            input.enabled = True
    
        #hide all but standard inputs + outputs
        for i in range(4,len(self.inputs)):
            self.inputs[i].enabled = False
                

        #make mode-specific inputs visible
        if len(self.inputs) == 7 and len(self.outputs) == 1:
       
            if self.mode_list == "Point":
                if self.point_normal == "Vector":
                    self.inputs[4].enabled = True
                    
            elif self.mode_list == "Area":
                self.inputs[5].enabled = True
                self.inputs[6].enabled = True
                    

            
                
            
        
    ##\brief Initializes the node.
    def init(self, context):
        #Generic Sockets
        self.inputs.new("socket_MESH", "Mesh")
        sock = self.inputs.new("socket_MESH", "Tile")
        sock.forced_full = True
        self.inputs.new("socket_SELECTION", "Selection")
        
        self.inputs.new("socket_VEC3_F","Offset")
        
        self.outputs.new("socket_MESH", "Mesh")
        
        socket = self.inputs.new("socket_VEC3_F","Vector")
        socket.enabled = False
        
        socket = self.inputs.new("socket_FLOAT","Scale Dom.")
        socket.enabled = False
        socket.setStandard(1.0)
        
        socket = self.inputs.new("socket_FLOAT","Scale Sub.")
        socket.enabled = False
        socket.setStandard(1.0)

        
        self.use_custom_color = True
        self.color = (1,.8,.5)
        
        self.update()
        
        
    ##\brief GUI.
    def draw_buttons(self, context, layout):
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "mode_list", "")
        
        if self.mode_list == "Point":
        
            
            box2 = layout.box()
            box3 = layout.box()
            box1 = layout.box()
            
            row = box1.row()
            
            
            row3 = box2.row()
            
            row.label(text = "Normal:")
            row.prop(self,"edit_normal","",icon="TRIA_DOWN" if self.edit_normal else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_normal:
                row2 = box1.row()
                row2.prop(self,"point_normal","")
                
            
            row3.label(text = "Dominant:")
            row3.prop(self,"edit_dominant","",icon="TRIA_DOWN" if self.edit_dominant else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_dominant:
                row4 = box2.row()
                row4.prop(self,"dominant","")
                rowF = box2.row()
                rowF.prop(self,"fallback","Fallback")
                
            row8 = box3.row()
            row8.label(text = "Tile Mesh:")
            row8.prop(self,"edit_tilemesh","",icon="TRIA_DOWN" if self.edit_tilemesh else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_tilemesh:
                row9 = box3.row()
                row10 = box3.row()
                row9.prop(self,"tileMode","")
                row10.prop(self,"point_cut","Cut Tile")
                if self.point_cut:
                    row11 = box3.row()
                    row11.prop(self,"point_cut_nors","Along Normals")
            
            
            
        elif self.mode_list == "Area":

            box1 = layout.box()
            
            row3 = box1.row()

            row3.label(text = "Dominant")
            row3.prop(self,"edit_dominant",icon="TRIA_DOWN" if self.edit_dominant else "TRIA_RIGHT",icon_only=True, emboss=False)
            if self.edit_dominant:
                row4 = box1.row()
                row4.prop(self,"dominant","")
                rowF = box1.row()
                rowF.prop(self,"fallback","Fallback")

            
            box3 = layout.box()
            
            rowL2 = box3.row()
            rowL2.label(text = "Tile Mesh")
            rowL2.prop(self,"edit_tilemesh",icon="TRIA_DOWN" if self.edit_tilemesh else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_tilemesh:
                row8 = box3.row()
                row8.prop(self,"tileMode","")
                row9 = box3.row()
                row10 = box3.row()
                row9.prop(self,"tileDom","Dominant")
                row10.prop(self,"tileSubdom","Subdominant")
            
            box4 = layout.box()
            
            row11 = box4.row()
            
            
            row11.label("Tile Alignment")
            row11.prop(self,"edit_tilealign","",icon="TRIA_DOWN" if self.edit_tilealign else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_tilealign:
                row12 = box4.row()
                row12.prop(self,"area_tiling_dom","Dom")
            
                if self.area_tiling_dom == "t":
                    row12_2 = box4.row()
                    row12_2.prop(self,"area_align_dom","")
                    
                row13 = box4.row()
                row13.prop(self,"area_tiling_subdom","Sub")
                if self.area_tiling_subdom == "t":
                    row13_2 = box4.row()
                    row13_2.prop(self,"area_align_subdom","")
                
            box5 = layout.box()
            
            
            rowPL = box5.row()
            rowPL.label("Polygons")
            rowPL.prop(self,"edit_polymode","",icon="TRIA_DOWN" if self.edit_polymode else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_polymode:
                rowTL = box5.row()
                
                rowTL.label(text = "Triangles:")
                
                rowTM = box5.row()
                rowTM.prop(self,"tri_morph","")
                
                if not self.tri_morph == "p":
                    rowTC = box5.row()
                    rowTC.prop(self,"tri_cut","Cut")
                
                
                box5.separator()
                
                rowQL = box5.row()
                
                
                
                rowQL.label(text = "Quads:")

                rowQM = box5.row()
                rowQM.prop(self,"quad_morph","")
                
                if not self.quad_morph == "ds":
                    rowQC = box5.row()
                    rowQC.prop(self,"quad_cut","Cut")
                
                
                box5.separator()
                
                rowNL = box5.row()
                rowNC = box5.row()
                
                rowNL.label(text = "NGons:")
                rowNC.prop(self,"ngon_cut","Cut")
            
            
            box8_1 = layout.box()
            
            row8S0 = box8_1.row()
            row8S0.label(text = "Normal:")
            row8S0.prop(self,"edit_normal","",icon="TRIA_DOWN" if self.edit_normal else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_normal:
            
                row8S = box8_1.row()
                row8S.prop(self,"area_scale_Z","Scale")
                
                row8S2 = box8_1.row()
                row8S2.prop(self,"area_align_Z","Align Bounds")

            
            

            
            
            

            
 
        
        layout.separator()
            
        
       
        
    ##\brief Re-calculates the node's data.   
    def recalculate(self):
        self.corrupted = False
        
        if len(self.inputs[0].links) > 0:
            
            copy_obs = self.inputs[0].returnData()
            
            
            current_OBJs = []
            for ob in copy_obs:
                ob.name = "_BG_"+self.name
            
            
            
            #Selections
            selections = self.inputs[2].returnData()
        

                
            if self.mode_list == "Point":
                
                tiles = self.inputs[1].returnData()
                
                offsets = self.inputs[3].returnData()
                
                ind = -1
                
                if self.tileMode == "Single Random":
                
                    ind = random.randrange(0,len(tiles))
                    
                
                
                if self.point_normal == "Vector":
                
                    vecs = self.inputs[4].returnData()

                    
                    
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,vecs,offsets])

                    copy_obs = lists[0]
                    selections = lists[1]
                    vecs = lists[2]
                    offsets = lists[3]
                    
                    utils_OBJ.prep_list(tiles)
                    
                    for i in range(0,len(copy_obs)):
                
                        copy_ob = copy_obs[i]
                        vec = vecs[i]
                        offset = offsets[i]

                        
                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv,True)
                            
                        utils_OBJ.prep(copy_ob,selection,"FACE")
                        
                        utils_GEOM.replace_poly_c(copy_ob,tiles,ind,"V",self.dominant,self.fallback,offset,vec,self.point_cut,self.point_cut_nors)
                       
                        utils_OBJ.deprep(copy_ob)
                        
                    utils_OBJ.deprep_list(tiles)
                        
                
                elif self.point_normal == "Poly Normal":
                    
                    
                        lists = utils_GEN.adjustLists([copy_obs,selections,offsets])
                        

                        copy_obs = lists[0]
                        selections = lists[1]
                        offsets = lists[2]
                        
                        
                        utils_OBJ.prep_list(tiles)

                    
                        for i in range(0,len(copy_obs)):
                
                            copy_ob = copy_obs[i]
                            offset = offsets[i]
                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv,True)
                            
                            utils_OBJ.prep(copy_ob,selection,"FACE")
                        
                            utils_GEOM.replace_poly_c(copy_ob,tiles,ind,"N",self.dominant,self.fallback,offset,None,self.point_cut,self.point_cut_nors)
                       
                            utils_OBJ.deprep(copy_ob)
                        
                        
                        
                        utils_OBJ.deprep_list(tiles)
                    
                
            elif self.mode_list == "Area":
            
                tiles = self.inputs[1].returnData()
                
                offsets = self.inputs[3].returnData()
                
                scales_d = self.inputs[5].returnData()
                scales_s = self.inputs[6].returnData()
                
                ind = -1
                
                if self.tileMode == "Single Random":
                
                    ind = random.randrange(0,len(tiles))
                
                lists = utils_GEN.adjustLists([copy_obs,selections,offsets,scales_d,scales_s])

                copy_obs = lists[0]
                selections = lists[1]
                offsets = lists[2]
                scales_d = lists[3]
                scales_s = lists[4]
                    
                utils_OBJ.prep_list(tiles)
                
                
                if not self.tri_morph == "p":
                    tri_cutM = self.tri_cut
                else:
                    tri_cutM = "x"
                
                
                    
                for i in range(0,len(copy_obs)):
                
                    copy_ob = copy_obs[i]
                    offset = offsets[i]
                    selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv,True)
                    
                    s_d = scales_d[i]
                    s_s = scales_s[i]

                    utils_OBJ.prep(copy_ob,selection,"FACE")
                        
                    utils_GEOM.replace_poly(copy_ob,tiles,ind,self.dominant,self.fallback,s_d,s_s,self.tileDom,self.tileSubdom,self.quad_morph,self.tri_morph,self.quad_cut,tri_cutM,self.ngon_cut,self.area_align_Z,offset,self.area_tiling_dom,self.area_tiling_subdom, self.area_align_dom,self.area_align_subdom)
                       
                    utils_OBJ.deprep(copy_ob)
                        
                        
                        
                utils_OBJ.deprep_list(tiles)
  
            #set current objects to new list
            self.outputs[0].setData(copy_obs)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
                
                
                
                
                
                
                
##\brief Replaces edges with pre-made tiles.
#\detail Fits tile objects to edges of a second object. In case you want a special cage, put the tile's cage in the tile object and assign it to a vertex group named "cage". Cages have to have rectangular shape and 4 vertices.               
class FAC_EdgeNode(buildingNode):

    '''A custom node'''

    bl_idname = 'FAC_EdgeNode'

    bl_label = 'Edge'

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
            
        if self.dominant_last != self.dominant:
            self.dominant_last = self.dominant
            outdated = True
    
        if self.fallback_last != self.fallback:
            self.fallback_last = self.fallback
            outdated = True
            
        if self.edge_mode_last != self.edge_mode:
            self.edge_mode_last = self.edge_mode
            outdated = True
            
        if self.point_normal_last != self.point_normal:
            self.point_normal_last = self.point_normal
            outdated = True
            
        if self.tileMode_last != self.tileMode:
            self.tileMode_last = self.tileMode
            outdated = True
            
        if self.tileDom_last != self.tileDom:
            self.tileDom_last = self.tileDom
            outdated = True
            
        if self.tileSubdom_last != self.tileSubdom:
            self.tileSubdom_last = self.tileSubdom
            outdated = True
            
        if self.area_tiling_dom_last != self.area_tiling_dom:
            self.area_tiling_dom_last = self.area_tiling_dom
            outdated = True
            
        if self.morph_m_last != self.morph_m:
            self.morph_m_last = self.morph_m
            outdated = True
            
        if self.morph_align_f_last != self.morph_align_f:
            self.morph_align_f_last = self.morph_align_f
            outdated = True
            
        if self.tile_align_last != self.tile_align:
            self.tile_align_last = self.tile_align
            outdated = True
            
        if self.along_cont_last != self.along_cont:
            self.along_cont_last = self.along_cont
            outdated = True
            

            

            

        
        
           
        
        if outdated:
            self.updateInputs(context)
            self.callObsolete(context)
    
    
    
    
    



    
	#NODE DATA
    
    corrupted = BoolProperty(default = True, update = updateEmpty)
    
    #data checking
    mode_list_last = StringProperty(default = "",update = updateEmpty)
    dominant_last = StringProperty(default = "",update = updateEmpty)
    fallback_last = StringProperty(default = "",update = updateEmpty)
    edge_mode_last = StringProperty(default = "",update = updateEmpty)
    point_normal_last = StringProperty(default = "",update = updateEmpty)
    tileMode_last = StringProperty(default = "",update = updateEmpty)
    tileDom_last = BoolProperty(default = True, update = updateEmpty)
    tileSubdom_last = BoolProperty(default = True, update = updateEmpty)
    area_tiling_dom_last = StringProperty(default = "",update = updateEmpty)
    morph_m_last = StringProperty(default = "",update = updateEmpty)
    morph_align_f_last = BoolProperty(default = True, update = updateEmpty)
    tile_align_last = StringProperty(default = "",update = updateEmpty)
    along_cont_last = BoolProperty(default = True, update = updateEmpty)
    
    

    
    modes = [("p","Place on Edges",""),("s","Along Edges","")]
    axes_strict = [("X","X",""),("Y","Y",""),("Z","Z",""),("-X","-X",""),("-Y","-Y",""),("-Z","-Z","")]
    point_nors = [("en","Edge Normal",""),("vn","Vector","")]
    point_tile_m = [("s","Single Random",""),("r","Random","")]
    point_edge_m = [("f","Adj. Faces",""),("e","Along Edge","")]
    tiling = [("s","Stretch",""),("t","Array","")]
    morphs = [("m","Morph",""),("c","Cut",""),("x","Neither","")]
    aligns = [("c","Center",""),("t","Top",""),("b","Bottom","")]

    
    mode_list = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Edge Modes",
        update = updateNode
    )
    
    point_normal = EnumProperty(
        name = "Choose Mode",
        items = point_nors,
        description = "Point Normal Modes",
        update = updateNode
    )
    
    dominant = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        default = "Z",
        description = "Point Dominant Axis",
        update = updateNode
    )
    
    fallback = EnumProperty(
        name = "Choose Mode",
        items = axes_strict,
        default = "X",
        description = "Fallback Dominant Axis",
        update = updateNode
    )
    
    
    tileMode = EnumProperty(
        name = "Choose Mode",
        items = point_tile_m,
        description = "Tile Mode",
        update = updateNode
    )
    
    edge_mode = EnumProperty(
        name = "Choose Mode",
        items = point_edge_m,
        description = "Tile Mode",
        update = updateNode
    )
    
    compensate_rot = BoolProperty(
        name = "Choose Mode",
        default = False,
        description = "Compensate for small rotation offsets",
        update = updateNode
    )
    
    tileDom = BoolProperty(
        name = "Choose Mode",
        default = False,
        description = "Randomize tiles (dominant axis)",
        update = updateNode
    )
    
    tileSubdom = BoolProperty(
        name = "Choose Mode",
        default = False,
        description = "Randomize tiles (subdominant axis)",
        update = updateNode
    )
    
    area_tiling_dom = EnumProperty(
        name = "Choose Mode",
        items = tiling,
        description = "Tile Mode",
        update = updateNode
    )
    
    morph_m = EnumProperty(
        name = "Choose Mode",
        items = morphs,
        description = "Tile Mode",
        update = updateNode
    )
    
    morph_align_f = BoolProperty(
        name = "Choose Mode",
        default = False,
        description = "Align bounds",
        update = updateNode
    )
    
    tile_align = EnumProperty(
        name = "Choose Mode",
        items = aligns,
        description = "Tile Mode",
        update = updateNode
    )
    
    along_cont = BoolProperty(
        name = "Choose Mode",
        default = False,
        description = "Align continuously along edgeloops",
        update = updateNode
    )
    
    
    
    edit_dominant = BoolProperty(default = False, update = updateEmpty)
    edit_tilemesh = BoolProperty(default = False, update = updateEmpty)
    edit_tilealign = BoolProperty(default = False, update = updateEmpty)
    edit_normal = BoolProperty(default = False, update = updateEmpty)
    edit_morph = BoolProperty(default = False, update = updateEmpty)
    
    
    

    ##\brief Makes inputs and outputs visible, based on the node's current settings.
    def updateInputs(self, context):
    
        #make all inputs visible
        for input in self.inputs:
            input.enabled = True
    
        #hide all but standard inputs + outputs
        for i in range(4,len(self.inputs)):
            self.inputs[i].enabled = False

        #make mode-specific inputs visible
        if len(self.inputs) == 7 and len(self.outputs) == 1:
            if self.mode_list == "p":
                if self.point_normal == "vn":
                    self.inputs[4].enabled = True
            elif self.mode_list == "s":
                self.inputs[5].enabled = True
                self.inputs[6].enabled = True

            
                
            
        
    ##\brief Initializes the node.
    def init(self, context):
        
        #Generic Sockets
        self.inputs.new("socket_MESH", "Mesh")
        sock = self.inputs.new("socket_MESH", "Tile")
        sock.forced_full = True
        self.inputs.new("socket_SELECTION", "Selection")
        
        self.inputs.new("socket_VEC3_F","Offset")
        socket = self.inputs.new("socket_VEC3_F","Vector")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT","Scale Dom.")
        socket.enabled = False
        socket = self.inputs.new("socket_FLOAT","Scale Sub.")
        socket.enabled = False
        
        self.outputs.new("socket_MESH", "Mesh")

        
        self.use_custom_color = True
        self.color = (1,.8,.5)
        
        self.update()
        
        
    ##\brief GUI.    
    def draw_buttons(self, context, layout):
        
        layout.separator()
        rowM = layout.row()
        rowM.prop(self,"mode_list","")
        
        if self.mode_list == "p":
            
            box2 = layout.box()
            box3 = layout.box()
            box1 = layout.box()
            
            row = box1.row()
            
            row3 = box2.row()
            
            row.label(text = "Normal:")
            row.prop(self,"edit_normal","",icon="TRIA_DOWN" if self.edit_normal else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_normal:
                row2 = box1.row()
                row2.prop(self,"point_normal","")
                if self.point_normal == "en":
                    row2_2 = box1.row()
                    row2_2.prop(self,"edge_mode","")
                    
                    if self.edge_mode == "f":
                        row3_c = box1.row()
                        row3_c.prop(self,"compensate_rot","Compensate")
            
            row3.label(text = "Dominant:")
            row3.prop(self,"edit_dominant","",icon="TRIA_DOWN" if self.edit_dominant else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_dominant:
                row4 = box2.row()
                row4.prop(self,"dominant","")
                rowF = box2.row()
                rowF.prop(self,"fallback","Fallback")
                
            row8 = box3.row()
            row8.label(text = "Tile Mesh:")
            row8.prop(self,"edit_tilemesh","",icon="TRIA_DOWN" if self.edit_tilemesh else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_tilemesh:
                row9 = box3.row()
                row9.prop(self,"tileMode","")
            
            
        elif self.mode_list == "s":
        
            box2 = layout.box()
            box3 = layout.box()

            row3 = box2.row()

            
            row3.label(text = "Dominant:")
            row3.prop(self,"edit_dominant","",icon="TRIA_DOWN" if self.edit_dominant else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_dominant:
                row4 = box2.row()
                row4.prop(self,"dominant","")
                rowF = box2.row()
                rowF.prop(self,"fallback","Fallback")
                
            row8 = box3.row()
            row8.label(text = "Tile Mesh:")
            row8.prop(self,"edit_tilemesh","",icon="TRIA_DOWN" if self.edit_tilemesh else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_tilemesh:
                row9 = box3.row()
                row9.prop(self,"tileMode","")
                row9 = box3.row()
                row10 = box3.row()
                row9.prop(self,"tileDom","Dominant")
                row10.prop(self,"tileSubdom","Subdominant")
            
            
            box4 = layout.box()
            
            row11 = box4.row()
            
            
            row11.label("Tile Alignment:")
            row11.prop(self,"edit_tilealign","",icon="TRIA_DOWN" if self.edit_tilealign else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_tilealign:
                row12 = box4.row()
                row12.prop(self,"area_tiling_dom","")
                if self.area_tiling_dom == "t":
                    row13 = box4.row()
                    row13.prop(self,"tile_align","Align")
                # row14 = box4.row()
                # row14.prop(self,"along_cont","Continuous")
            
            
            
            box5 = layout.box()
            
            row13 = box5.row()
            
            row13.label("Morphing:")
            row13.prop(self,"edit_morph","",icon="TRIA_DOWN" if self.edit_morph else "TRIA_RIGHT",icon_only=True, emboss=False)
            
            if self.edit_morph:
                row14 = box5.row()
                row16 = box5.row()
                row14.prop(self,"morph_m","")
                row16.prop(self,"morph_align_f","Align to Faces")
            
        
        
        
        
        
        
        
        
        layout.separator()
        
            
        
       
        
    ##\brief Re-calculates the node's data.   
    def recalculate(self):
        
        self.corrupted = False
        
        if len(self.inputs[0].links) > 0:
            
            copy_obs = self.inputs[0].returnData()
            
            
            #Selections
            selections = self.inputs[2].returnData()
        

                
            if self.mode_list == "p":
                
                tiles = self.inputs[1].returnData()
                
                offsets = self.inputs[3].returnData()
                
                ind = -1
                
                if self.tileMode == "s":
                
                    ind = random.randrange(0,len(tiles))
                    
                
                
                if self.point_normal == "vn":
                
                    vecs = self.inputs[4].returnData()

                    
                    
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,vecs,offsets])

                    copy_obs = lists[0]
                    selections = lists[1]
                    vecs = lists[2]
                    offsets = lists[3]
                    
                    utils_OBJ.prep_list(tiles)
                    
                    for i in range(0,len(copy_obs)):
                
                        copy_ob = copy_obs[i]
                        vec = vecs[i]
                        offset = offsets[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv,True)
                        
                        utils_OBJ.prep(copy_ob,selection,"VERT")
                        
                        utils_GEOM.replace_edge_c(copy_ob,tiles,ind,"V",self.dominant,self.fallback,offset,self.edge_mode,False,vec)
                       
                        utils_OBJ.deprep(copy_ob)
                        
                    utils_OBJ.deprep_list(tiles)
                    
                elif self.point_normal == "en":
                    
                    
                        lists = utils_GEN.adjustLists([copy_obs,selections,offsets])

                        copy_obs = lists[0]
                        selections = lists[1]
                        offsets = lists[2]
                        
                        utils_OBJ.prep_list(tiles)

                    
                        for i in range(0,len(copy_obs)):
                
                            copy_ob = copy_obs[i]
                            offset = offsets[i]
                            selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv,True)
                        
                            utils_OBJ.prep(copy_ob,selection,"VERT")
                        
                            utils_GEOM.replace_edge_c(copy_ob,tiles,ind,"N",self.dominant,self.fallback,offset,self.edge_mode,self.compensate_rot)
                       
                            utils_OBJ.deprep(copy_ob)
                        
                        
                        
                        utils_OBJ.deprep_list(tiles)
                        
                        
                        
                        
                        
                        
                        
            elif self.mode_list == "s":
                
                tiles = self.inputs[1].returnData()
                
                offsets = self.inputs[3].returnData()
                
                ind = -1
                
                if self.tileMode == "s":
                
                    ind = random.randrange(0,len(tiles))

                    reps = self.inputs[5].returnData()
                    subreps = self.inputs[6].returnData()
                    
                    lists = utils_GEN.adjustLists([copy_obs,selections,offsets,reps,subreps])

                    copy_obs = lists[0]
                    selections = lists[1]
                    offsets = lists[2]
                    reps = lists[3]
                    subreps = lists[4]
                    
                    utils_OBJ.prep_list(tiles)

                
                    for i in range(0,len(copy_obs)):
            
                        copy_ob = copy_obs[i]
                        offset = offsets[i]
                        selection = utils_SEL.mapSelection(selections[i], copy_obs[i],[self.inputs[2].sel_mode,self.inputs[2].sel_vgroup],self.inputs[2].sel_inv,True)
                        rep = reps[i]
                        subrep = subreps[i]
                    
                        utils_OBJ.prep(copy_ob,selection,"VERT")
                    
                        utils_GEOM.replace_edge_along(copy_ob,tiles,ind,self.dominant,self.fallback,offset,self.area_tiling_dom,rep,subrep,self.tileDom,self.tileSubdom,self.tile_align,self.morph_m,self.morph_align_f,self.along_cont)
                   
                        utils_OBJ.deprep(copy_ob)
                    
                    
                    
                    utils_OBJ.deprep_list(tiles)            
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
  
        #set current objects to new list
        self.outputs[0].setData(copy_obs)
            
            
                
                
                
                
                
                
                
                
                
                
                
                
                
class FAC_VertNode(buildingNode):

    bl_idname = 'FAC_VertNode'

    bl_label = 'Vertice'

    bl_icon = 'NODETREE'

    #UPDATE
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
    current_OBJs = []
    current_OBJs_secondary = []
    
    
    
    #data checking
    mode_list_last = StringProperty(default = "")


    
    modes = [("Tri","Tri",""),("Quad","Quad",""),("NGon","NGon","")]

    
    mode_list = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Flatten Modes",
        update = updateNode
    )
 

    
    def updateInputs(self, context):
    
        #make all inputs visible
        for input in self.inputs:
            input.enabled = True
    
        #hide all but standard inputs + outputs
        for input in self.inputs:
            if input.name != "Mesh" and input.name != "Selection":
                input.enabled = False
                

        #make mode-specific inputs visible
        if len(self.inputs) == 18 and len(self.outputs) == 3:
        
            if self.mode_list == "Tri":
                return
            elif self.mode_list == "Quad":
                return
            elif self.mode_list == "NGon":
                return
            
                
            
        
    
    def init(self, context):
        
        #Generic Outputs
        self.inputs.new("socket_MESH", "Mesh")
        self.inputs.new("socket_SELECTION", "Selection")
        
        self.outputs.new("socket_MESH", "Mesh")

        
        self.use_custom_color = True
        self.color = (1,.8,.5)
        
        
        self.update()
        
        
        
    def draw_buttons(self, context, layout):
        
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "mode_list", "")
        
        if self.mode_list == "Tri":
            return
        elif self.mode_list == "Quad":
            return
        elif self.mode_list == "NGon":
            return
            
 
        
        layout.separator()    
        
        
    def returnData(self, output):

        self.recalculate(output)
        
        if output.identifier == self.outputs[0].identifier:
            return current_OBJs
        elif output.identifier == self.outputs[1].identifier:
            return self.current_SELs
        elif output.identifier == self.outputs[2].identifier:
            return current_OBJs_secondary
            
        
       
        
        
    def recalculate(self, output):
        
        self.corrupted = False
        
        if len(self.inputs[0].links) > 0:
            
            selections = []
            source_obs = self.inputs[0].returnData()

            copy_obs = []
            
            for ob in source_obs:
                ob2 = utils_OBJ.copyobj(ob)
                copy_obs.append(ob2)
            
            
            for ob in bpy.data.objects:
                if self.name in ob.name:
                    ob.name = "_$OBS$_"
            
            
            current_OBJs = []
            for ob in copy_obs:
                ob.name = "_BG_"+self.name
            
            
            
            
            selections = self.inputs[1].returnData()

            if selections == [None]:
                selections = []
                for ob in copy_obs:
                    
                    sel_v = [v.index for v in ob.data.vertices]
                    sel_e = [e.index for e in ob.data.edges]
                    sel_f = [f.index for f in ob.data.polygons]
                    selection = [sel_v,sel_e,sel_f,ob]
                    selections.append(selection)
        

                
            if self.mode_list == "Tri":
                return
            elif self.mode_list == "Quad":
                return
            if self.mode_list == "NGon":
                return
                

                

                
                
                
                
                
class FAC_RegionNode(buildingNode):

    bl_idname = 'FAC_RegionNode'

    bl_label = 'Region'

    bl_icon = 'NODETREE'

    #UPDATE
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
    current_OBJs = []
    current_OBJs_secondary = []
    
    
    
    #data checking
    mode_list_last = StringProperty(default = "")


    
    modes = [("Tri","Tri",""),("Quad","Quad",""),("NGon","NGon","")]

    
    mode_list = EnumProperty(
        name = "Choose Mode",
        items = modes,
        description = "Flatten Modes",
        update = updateNode
    )
 

    
    def updateInputs(self, context):
    
        #make all inputs visible
        for input in self.inputs:
            input.enabled = True
    
        #hide all but standard inputs + outputs
        for input in self.inputs:
            if input.name != "Mesh" and input.name != "Selection":
                input.enabled = False
                

        #make mode-specific inputs visible
        if len(self.inputs) == 18 and len(self.outputs) == 3:
        
            if self.mode_list == "Tri":
                return
            elif self.mode_list == "Quad":
                return
            elif self.mode_list == "NGon":
                return
            
                
            
        
    
    def init(self, context):
        
        #Generic Outputs
        self.inputs.new("socket_MESH", "Mesh")
        self.inputs.new("socket_SELECTION", "Selection")
        
        self.outputs.new("socket_MESH", "Mesh")

        
        self.use_custom_color = True
        self.color = (1,.8,.5)
        
        
        self.update()
        
        
        
    def draw_buttons(self, context, layout):
        
        layout.separator()
        rowM = layout.row(align = True)
        rowM.prop(self, "mode_list", "")
        
        if self.mode_list == "Tri":
            return
        elif self.mode_list == "Quad":
            return
        elif self.mode_list == "NGon":
            return
            
 
        
        layout.separator()    
        
        
    def returnData(self, output):

        self.recalculate(output)
        
        if output.identifier == self.outputs[0].identifier:
            return current_OBJs
        elif output.identifier == self.outputs[1].identifier:
            return self.current_SELs
        elif output.identifier == self.outputs[2].identifier:
            return current_OBJs_secondary
            
        
       
        
        
    def recalculate(self, output):
        
        self.corrupted = False
        
        if len(self.inputs[0].links) > 0:
            
            selections = []
            source_obs = self.inputs[0].returnData()

            copy_obs = []
            
            for ob in source_obs:
                ob2 = utils_OBJ.copyobj(ob)
                copy_obs.append(ob2)
            
            
            for ob in bpy.data.objects:
                if self.name in ob.name:
                    ob.name = "_$OBS$_"
            
            
            current_OBJs = []
            for ob in copy_obs:
                ob.name = "_BG_"+self.name
            
            
            
            #Selections
            selections = self.inputs[1].returnData()

            if selections == [None]:
                selections = []
                for ob in copy_obs:
                    
                    sel_v = [v.index for v in ob.data.vertices]
                    sel_e = [e.index for e in ob.data.edges]
                    sel_f = [f.index for f in ob.data.polygons]
                    selection = [sel_v,sel_e,sel_f,ob]
                    selections.append(selection)
        

                
            if self.mode_list == "Tri":
                return
            elif self.mode_list == "Quad":
                return
            if self.mode_list == "NGon":
                return
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
            
            
                
import os, sys, inspect,faulthandler
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

# Info:
# cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
# __file__ fails if script is called in different ways on Windows
# __file__ fails if someone does os.chdir() before
# sys.argv[0] also fails because it doesn't not always contains the path

bl_info = {
    "name": "Building Generator",
    "description": "Generates buildings based on nodetrees and pre-made building tiles.",
    "author": "Stefan Wendling",
    "version": (0,1),
    "blender": (2, 71, 0),
    "location": "Node Editor",
    "warning": "Known Issue: Make sure to update the preview after loading a new file to avoid a crash.",
    "category": "Object",
}



if "bpy" in locals():
    import imp
    imp.reload(building_nodes_IN)
    imp.reload(building_nodes_OUT)
    imp.reload(building_nodes_MESH)
    imp.reload(building_nodes_SEL)
    imp.reload(building_nodes_MATH)
    imp.reload(building_nodes_LST)
    imp.reload(building_nodes_COL)
    imp.reload(building_nodes_FAC)
    imp.reload(building_nodes_FLOW)
    imp.reload(building_NODETREE)
    imp.reload(custom_sockets)
    imp.reload(utils_MATH)
    imp.reload(utils_GEN)
    imp.reload(utils_GEOM)
    imp.reload(utils_OBJ)
    imp.reload(utils_SEL)
    imp.reload(utils_OPERATOR)


else:
    
    import custom_sockets
    import nodes
    
    import utils
	

import bpy
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from utils.utils_GLO import DataHeap,BG_DataPackage

#Node Categories

class Building_GEN_Category(NodeCategory):
  @classmethod
  def poll(cls, context):
    return context.space_data.tree_type == "BuildingTree"
    

    

categories = [
  Building_GEN_Category("IN", "Input", items = [
    NodeItem("IN_GrabMeshNode"),
    NodeItem("IN_PrimitiveNode"),
    NodeItem("IN_VectorNode"),
    NodeItem("IN_ValueNode"),
    #NodeItem("IN_ColorNode"),
  ]),
  
  Building_GEN_Category("OUT", "Output", items = [
    NodeItem("OUT_OutputNode"),
    NodeItem("OUT_DebugNode"),
  ]),
  
  Building_GEN_Category("MESH", "Mesh", items = [
    NodeItem("MESH_FilterNode"),
    NodeItem("MESH_FilterCageNode"),
    NodeItem("MESH_OperatorNode"),
    NodeItem("MESH_ExtractNode"),
    NodeItem("MESH_ListNode"),
  ]),

  Building_GEN_Category("SEL", "Selection", items = [
    NodeItem("SEL_DataSelectionNode"),
    NodeItem("SEL_ShapeSelectionNode"),
    NodeItem("SEL_CombineSelectionNode"),
  ]),
  
  Building_GEN_Category("MATH", "Math", items = [
    NodeItem("MATH_ValueNode"),
    NodeItem("MATH_Vec3Node"),
    #NodeItem("COL_MixNode"),
  ]),
  
  Building_GEN_Category("FAC", "Facade", items = [
    NodeItem("FAC_PolyNode"),
    NodeItem("FAC_EdgeNode"),
    #NodeItem("FAC_VertNode"),
    #NodeItem("FAC_RegionNode"),
  ]),
  
  Building_GEN_Category("FLOW", "Flow Control", items = [
    NodeItem("FLOW_GateNode"),
    NodeItem("FLOW_IfNode"),
    NodeItem("LST_ExtractNode"),
    NodeItem("LST_ExtendNode"),
    NodeItem("LST_AdjustNode"),
    NodeItem("LST_AppendNode"),
    NodeItem("LST_MoveNode"),
    NodeItem("LST_DataNode"),
  ]),
  
  
]




#REGISTERING

def register():

    


	#node categories
    nodeitems_utils.register_node_categories("Building_GEN_Category",categories)


	#sockets
    
    bpy.utils.register_class(custom_sockets.socket_MESH)
    bpy.utils.register_class(custom_sockets.socket_VEC3_F)
    bpy.utils.register_class(custom_sockets.socket_SELECTION)
    bpy.utils.register_class(custom_sockets.socket_FLOAT)
    bpy.utils.register_class(custom_sockets.socket_INT)
    bpy.utils.register_class(custom_sockets.socket_UNIV)
    #bpy.utils.register_class(custom_sockets.socket_COL)
    
    
    

	
	
	#nodetrees
    bpy.utils.register_class(nodes.building_NODETREE.BuildingTree)

    
    #operators
    bpy.utils.register_class(utils.utils_OPERATOR.GEN_MessageOperator)
    bpy.utils.register_class(utils.utils_OPERATOR.OUT_UpdateOperator)
    bpy.utils.register_class(utils.utils_OPERATOR.OUT_GenerateOperator)
    bpy.utils.register_class(utils.utils_OPERATOR.FLOW_GateOpenOperator)
    bpy.utils.register_class(utils.utils_OPERATOR.FLOW_GateCloseOperator)
    bpy.utils.register_class(utils.utils_OPERATOR.FLOW_GateRefreshOperator)
    bpy.utils.register_class(utils.utils_OPERATOR.IN_MeshRefreshOperator)
    bpy.utils.register_class(utils.utils_OPERATOR.RandomizeOperator)
    bpy.utils.register_class(utils.utils_OPERATOR.FreezeOperator)
    bpy.utils.register_class(utils.utils_OPERATOR.UnfreezeOperator)
    
	
	#nodes  
    #IN
    bpy.utils.register_class(nodes.building_nodes_IN.IN_GrabMeshNode)
    bpy.utils.register_class(nodes.building_nodes_IN.IN_VectorNode)
    bpy.utils.register_class(nodes.building_nodes_IN.IN_ValueNode)
    bpy.utils.register_class(nodes.building_nodes_IN.IN_PrimitiveNode)
    bpy.utils.register_class(nodes.building_nodes_IN.IN_ColorNode)
    
    #OUT
    bpy.utils.register_class(nodes.building_nodes_OUT.OUT_OutputNode)
    bpy.utils.register_class(nodes.building_nodes_OUT.OUT_DebugNode)

    #MESH
    bpy.utils.register_class(nodes.building_nodes_MESH.MESH_FilterNode)
    bpy.utils.register_class(nodes.building_nodes_MESH.MESH_OperatorNode)
    bpy.utils.register_class(nodes.building_nodes_MESH.MESH_ExtractNode)
    bpy.utils.register_class(nodes.building_nodes_MESH.MESH_ListNode)
    bpy.utils.register_class(nodes.building_nodes_MESH.MESH_FilterCageNode)
    
    #SEL
    bpy.utils.register_class(nodes.building_nodes_SEL.SEL_CombineSelectionNode)
    bpy.utils.register_class(nodes.building_nodes_SEL.SEL_ShapeSelectionNode)
    bpy.utils.register_class(nodes.building_nodes_SEL.SEL_DataSelectionNode)
    
    #MATH
    bpy.utils.register_class(nodes.building_nodes_MATH.MATH_ValueNode)
    bpy.utils.register_class(nodes.building_nodes_MATH.MATH_Vec3Node)
    
    #LIST
    bpy.utils.register_class(nodes.building_nodes_LST.LST_ExtractNode)
    bpy.utils.register_class(nodes.building_nodes_LST.LST_ExtendNode)
    bpy.utils.register_class(nodes.building_nodes_LST.LST_AdjustNode)
    bpy.utils.register_class(nodes.building_nodes_LST.LST_AppendNode)
    bpy.utils.register_class(nodes.building_nodes_LST.LST_DataNode)
    bpy.utils.register_class(nodes.building_nodes_LST.LST_MoveNode)
    
    #COL
    bpy.utils.register_class(nodes.building_nodes_COL.COL_MixNode)
    
    #FAC
    bpy.utils.register_class(nodes.building_nodes_FAC.FAC_PolyNode)
    bpy.utils.register_class(nodes.building_nodes_FAC.FAC_EdgeNode)
    bpy.utils.register_class(nodes.building_nodes_FAC.FAC_VertNode)
    bpy.utils.register_class(nodes.building_nodes_FAC.FAC_RegionNode)
    
    #FLOW
    bpy.utils.register_class(nodes.building_nodes_FLOW.FLOW_GateNode)
    bpy.utils.register_class(nodes.building_nodes_FLOW.FLOW_IfNode)
    

def unregister():
    
    

    #nodes
    #IN
    bpy.utils.unregister_class(nodes.building_nodes_IN.IN_GrabMeshNode)
    bpy.utils.unregister_class(nodes.building_nodes_IN.IN_VectorNode)
    bpy.utils.unregister_class(nodes.building_nodes_IN.IN_ValueNode)
    bpy.utils.unregister_class(nodes.building_nodes_IN.IN_PrimitiveNode)
    bpy.utils.unregister_class(nodes.building_nodes_IN.IN_ColorNode)
    
    #OUT
    bpy.utils.unregister_class(nodes.building_nodes_OUT.OUT_OutputNode)
    bpy.utils.unregister_class(nodes.building_nodes_OUT.OUT_DebugNode)
    
    #MESH
    bpy.utils.unregister_class(nodes.building_nodes_MESH.MESH_FilterNode)
    bpy.utils.unregister_class(nodes.building_nodes_MESH.MESH_OperatorNode)
    bpy.utils.unregister_class(nodes.building_nodes_MESH.MESH_ExtractNode)
    bpy.utils.unregister_class(nodes.building_nodes_MESH.MESH_ListNode)
    bpy.utils.unregister_class(nodes.building_nodes_MESH.MESH_FilterCageNode)
    
    #SEL
    bpy.utils.unregister_class(nodes.building_nodes_SEL.SEL_CombineSelectionNode)
    bpy.utils.unregister_class(nodes.building_nodes_SEL.SEL_ShapeSelectionNode)
    bpy.utils.unregister_class(nodes.building_nodes_SEL.SEL_DataSelectionNode)
    
    #MATH
    bpy.utils.unregister_class(nodes.building_nodes_MATH.MATH_ValueNode)
    bpy.utils.unregister_class(nodes.building_nodes_MATH.MATH_Vec3Node)
    
    #LIST
    bpy.utils.unregister_class(nodes.building_nodes_LST.LST_ExtractNode)
    bpy.utils.unregister_class(nodes.building_nodes_LST.LST_ExtendNode)
    bpy.utils.unregister_class(nodes.building_nodes_LST.LST_AdjustNode)
    bpy.utils.unregister_class(nodes.building_nodes_LST.LST_AppendNode)
    bpy.utils.unregister_class(nodes.building_nodes_LST.LST_DataNode)
    bpy.utils.unregister_class(nodes.building_nodes_LST.LST_MoveNode)
    
    #COL
    bpy.utils.unregister_class(nodes.building_nodes_COL.COL_MixNode)
    
    #FAC
    bpy.utils.unregister_class(nodes.building_nodes_FAC.FAC_PolyNode)
    bpy.utils.unregister_class(nodes.building_nodes_FAC.FAC_EdgeNode)
    bpy.utils.unregister_class(nodes.building_nodes_FAC.FAC_VertNode)
    bpy.utils.unregister_class(nodes.building_nodes_FAC.FAC_RegionNode)
    
    #FLOW
    bpy.utils.unregister_class(nodes.building_nodes_FLOW.FLOW_GateNode)
    bpy.utils.unregister_class(nodes.building_nodes_FLOW.FLOW_IfNode)
    

    
	#node categories
    nodeitems_utils.unregister_node_categories("Building_GEN_Category")
	
	#nodetrees
    bpy.utils.unregister_class(nodes.building_NODETREE.BuildingTree)
	
	
	#sockets
    bpy.utils.unregister_class(custom_sockets.socket_MESH)
    bpy.utils.unregister_class(custom_sockets.socket_VEC3_F)
    bpy.utils.unregister_class(custom_sockets.socket_SELECTION)
    bpy.utils.unregister_class(custom_sockets.socket_FLOAT)
    bpy.utils.unregister_class(custom_sockets.socket_INT)
    bpy.utils.unregister_class(custom_sockets.socket_UNIV)
    #bpy.utils.unregister_class(custom_sockets.socket_COL)
    
    
    #operators
    bpy.utils.unregister_class(utils.utils_OPERATOR.GEN_MessageOperator)
    bpy.utils.unregister_class(utils.utils_OPERATOR.OUT_UpdateOperator)
    bpy.utils.unregister_class(utils.utils_OPERATOR.OUT_GenerateOperator)
    bpy.utils.unregister_class(utils.utils_OPERATOR.FLOW_GateOpenOperator)
    bpy.utils.unregister_class(utils.utils_OPERATOR.FLOW_GateCloseOperator)
    bpy.utils.unregister_class(utils.utils_OPERATOR.FLOW_GateRefreshOperator)
    bpy.utils.unregister_class(utils.utils_OPERATOR.IN_MeshRefreshOperator)
    bpy.utils.unregister_class(utils.utils_OPERATOR.RandomizeOperator)
    bpy.utils.unregister_class(utils.utils_OPERATOR.FreezeOperator)
    bpy.utils.unregister_class(utils.utils_OPERATOR.UnfreezeOperator)
    
    
    


if __name__ == "__main__":
    register()

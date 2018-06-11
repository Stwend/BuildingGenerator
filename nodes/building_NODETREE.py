##@package buildingGen.nodes.building_NODETREE
# Superclasses for nodes, trees, and sockets


from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import StringProperty,BoolProperty
from utils import utils_GEN,utils_GLO
from utils.utils_GLO import print_debug,DataHeap


##@brief Superclass for trees
class BuildingTree(NodeTree):
    
    ##\property bl_idname
    #@brief Name of the tree class.
    bl_idname = 'BuildingTree'

    ##\property bl_label
    #@brief Label of the tree.
    bl_label = 'Building'

    ##\property bl_icon
    #@brief Icon the BuildingGen trees are assigned in Blender's node editor.
    bl_icon = 'OBJECT_DATAMODE'
    
    ##\property init
    #@brief States whether the class has been initiated or not.
    init = False
    
    ##\fn update
    #\brief Called when a tree is updated.
    #\detail Check if the tree has been initialized. If not (this happens both on creation and on loading a saved .blend file), the tree is (re-)initialized.
    #\returns None
    def update(self):
        print_debug("UPDATING TREE:",self.name)
        if not self.init:
            print_debug("INITIALIZING TREE:",self.name)
            for node in self.nodes:
                node.corrupted = True
                node.update()
                node.displayWarning = True
            self.init = True
        
                

    
    
# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class BuildingTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'BuildingTree'

        

##\class buildingNode    
#\brief Superclass for nodes
#\par Responsible for:
#Calculating output data from input data, giving the user a GUI to work with.    
class buildingNode(Node):

    ##\fn free
    #\brief Called when a node is deleted.
    #\detail Upon deleting a node, it makes all of its outputs delete their data aswell.
    #\returns None
    def free(self):
        print_debug("Removing node: ", self.name)

        for output in self.outputs:
            output.clearData()
        
        
    ##\fn update
    #\brief Called when a node is updated.
    #\detail Puts a brief note into the debug log, then calls updateNode.
    #\returns None
    def update(self):
        print_debug("UPDATING:",self.name)
        print_debug("   -> self:",self.name)

        self.updateNode("")

    ##\property displayWarning
    #@brief Whether the node should be warning about long calculation times.
    displayWarning = BoolProperty(default = False)   
        
        
    ##\fn updateNode
    #\brief Checks for GUI and property changes.
    #\detail Empty implementation, every node has to have its own version.
    #\returns None    
    def updateNode(self,context):
        return

    ##\fn checkInputs
    #\brief Checks inputs for changes.
    #\detail Empty implementation, every node has to have its own version.
    #\returns None
    def checkInputs(self):
        return
     
    ##\fn updateEmpty
    #\brief Empty function.
    #\detail Empty function to silence unwanted property updates.
    #\returns None
    def updateEmpty(self,context):
        return
     
    primaryType = StringProperty(default = "",update = updateEmpty)
    
    
    ##\fn floodObsolete
    #\brief Marks itself and depending nodes as obsolete.
    #\detail In case a node is outdated, it recursively marks itself and nodes depending on its data as obsolete.
    #\returns a list of outputs connected to the node
    def floodObsolete(self, context):
    
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
        
        
    ##\fn callObsolete
    #\brief Calls in a marking wave, then updates the preview.
    #\detail Calls floodObsolete, then makes every connected output update its preview object.
    #\returns None    
    def callObsolete(self,context):
        print_debug("CALLING OBSOLETE:",self.name)
        pings = self.floodObsolete(context)
        
        print_debug(self.name,"is reaching out to outputs...")
        
        if not pings == []:
        
            pings = list(set(pings))
            
            print_debug(pings)
            
            for node in self.id_data.nodes:
                if node.as_pointer() in pings:
                    print_debug(node.name)
                    try:
                        node.triggerData(context)
                    except:
                        pass
                        
    
    ##\fn randomize
    #\brief Makes the node recalculate if it has random properties.
    #\detail Empty implementation, every node with random elements has to have its own version.
    #\returns None
    def randomize(self):
        return
    

    ##\fn freezeRandom
    #\brief Prevents unwanted randomizations.
    #\detail Part of the node/socket recursive freeze propagation through a tree. Calls propagateFreeze() in every input socket.
    #\returns None
    def freezeRandom(self):
        if len(self.inputs) > 0:
            for input in self.inputs:
                input.propagateFreeze()
    

    ##\fn unfreezeRandom
    #\brief Enables randomizations.
    #\detail Part of the node/socket recursive unfreeze propagation through a tree. Calls propagateUnfreeze() in every input socket.
    #\returns None
    def unfreezeRandom(self):
        if len(self.inputs) > 0:
            for input in self.inputs:
                input.propagateUnfreeze()
     


    ##\fn randomize
    #\brief Randomize node.
    #\detail Part of the node/socket recursive randomization propagation through a tree. Calls propagateRand() in every input socket.
    #\returns None
    def randomize(self):
        if len(self.inputs) > 0:
            for input in self.inputs:
                input.propagateRand()
                
    
    ##\fn askForType
    #\brief Finds the first socket's current datatype.
    #\detail Part of the node/socket recursive datatype finding process. Calls askForType() in the first input socket.
    #\returns None
    def askForType(self):
        if len(self.inputs) > 0:
            return self.inputs[0].askForType()
            
            
##\class buildingSocket     
#\brief Superclass for sockets
#\par Responsible for:
#Data transfers between nodes aswell as preparing data for usage inside nodes.
class buildingSocket(NodeSocket):

    ##\fn updateEmpty
    #\brief Empty function.
    #\detail Empty function to silence unwanted property updates.
    #\returns None
    def updateEmpty(self,context):
        return
        
    ##\fn notify
    #\brief Shortcut for notifyNode.
    #\detail Instead of making the node check itself, CallObsolete is called directly.
    #\returns None
    def notify(self,context):
        self.node.callObsolete(context)
            
            
    ##\fn askForType
    #\brief Finds the socket's current datatype.
    #\detail Together with buildingNode's askForType function, socket_UNIV sockets can recursively find out about their current datatype.
    #\returns the datatype
    def askForType(self):
        code = type(self).__name__
        if not code == "socket_UNIV":
            return code
            
        else:
            if self.is_output:
                return self.node.askForType()
            elif len(self.links) > 0:
                return self.links[0].from_socket.askForType()
    
    
    ##\fn returnData
    #\brief Returns data from other nodes.
    #\detail In case the socket is an input, it asks for data from its connected output.
    #\returns list of whatever data its connected counterpart offers to it
    def returnData(self):
        if len(self.links) == 0:
            print_debug("Returning data:",str(self.standard_data))
            return [self.standard_data]
        else:
            node_output = self.links[0].from_socket
            return node_output.getData()
    
    ##\fn propagateFreeze
    #\brief Freezes all randomized parts of nodes.
    #\detail Recursively calls freezeRandom() in all connected nodes. Intended for tree-wide use in nodes such as OUT_OutputNode.
    #\returns None
    def propagateFreeze(self):
        if len(self.links) > 0:
            for link in self.links:
                link.from_node.freezeRandom()
    

    ##\fn propagateUnfreeze
    #\brief Unfreezes all randomized parts of nodes.
    #\detail Recursively calls unfreezeRandom() in all connected nodes. Intended for tree-wide use in nodes such as OUT_OutputNode.
    #\returns None
    def propagateUnfreeze(self):
        if len(self.links) > 0:
            for link in self.links:
                link.from_node.unfreezeRandom()
    

    ##\fn propagateRand
    #\brief Randomizes all nodes with random parts.
    #\detail Recursively calls randomize() in all connected nodes. Intended for tree-wide use in nodes such as OUT_OutputNode.
    #\returns None
    def propagateRand(self):
        if len(self.links) > 0:
            for link in self.links:
                link.from_node.randomize()
                
    
    ##\fn notifyNode
    #\brief Updates a socket's node.
    #\detail In case the socket's properties have changed, its node is automatically outdated too, and needs to be updated.
    #\returns None
    def notifyNode(self):
        self.node.update()
        
        
        
    ##\fn getData
    #\brief Fetches data from DataHeap.
    #\detail In case of the socket being an output, it tries to get its data from DataHeap.
    #\returns list of whatever data was stored in the heap under the socket's ID
    def getData(self):
    
        if self.node.corrupted:
            self.node.recalculate()
        
        heap = DataHeap()
        
        data = heap.loadData(self.as_pointer())
        
        print_debug( "Data:",str(data))
        
        if data == None:
            print_debug("No data:",str(self),"/",self.as_pointer())
            self.node.corrupted = True
            return self.getData()
            
        return data
            
    ##\fn setData
    #\brief Stores calculated data in DataHeap.
    #\detail Once a node has finished recalculating, it makes all of its output sockets save their respective data in DataHeap.
    #\param data The data to be stored.
    #\returns None
    def setData(self,data):
    
        heap = DataHeap()
        heap.storeData(data,self.as_pointer())
        
    ##\fn clearData
    #\brief Deletes data from DataHeap.
    #\detail In case of a socket's data being outdated, it makes DataHeap delete it before saving new data into it.
    #\returns None    
    def clearData(self):
        heap = DataHeap()
        heap.clearData(self.as_pointer())
        

            
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        
        
        
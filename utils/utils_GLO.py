##\package buildingGen.utils.utils_GLO
# Global utilities.


import bpy
import math
import os

        
        
        
        

        
##\class DebugPrinter
#\brief Prints debug info to a file.
#\detail Implemented as singleton, creates and maintains a debug file.
class DebugPrinter(object):
    ##\class __DebugPrinter
    #\brief Internal class.
    class __DebugPrinter:
        
        ##\property file
        #\brief The output file.
        file = None

        
        def __init__(self):
        
            
            folder = os.path.dirname(os.path.dirname(__file__))
            rel_path = "BGen_debug.txt"
            filepath = os.path.join(folder, rel_path)
        
            self.file = open(filepath, "w")
            self.file.write("\n")
            self.file.write("Building Generator - Debug\n")
            self.file.write("__________________________\n")
            self.file.write("\n")
            self.file.write("\n")
            
        def __str__(self):
            return "Debug Printer/ <File: "+str(self.file)+">"
            
            
        ##\fn d_print
        #\brief Prints to the output file.
        def d_print(self,text):
            self.file.write(text+"\n")
            self.file.write("\n")
            self.file.flush()
            
    ##\property instance
    #\brief The current __DebugPrinter instance.    
    instance = None
    
    ##\fn __new__:
    #\brief Instantiates or returns a __DebugPrinter object.
    def __new__(cls):
        if not DebugPrinter.instance:
            DebugPrinter.instance = DebugPrinter.__DebugPrinter()
        return DebugPrinter.instance 
        
        
        
##\fn print_debug
#\brief Prepares multiple strings to be logged.   
#\detail Works just like Python's "print()" command, but writes to the debug file instead.
def print_debug(*args):

    text = ""
    
    for arg in args:
        text += str(arg) + " "
    
    printer = DebugPrinter()
    printer.d_print(text)
    
    
##\fn dumpNodelist
#\brief Prints all nodes and their info.   
def dumpNodelist(tree):
    
    print_debug("-------------------")
    print_debug("NODES:")
    
    for node in tree.nodes:
        print_debug("   -> Node:",node.name)
        print_debug("       -> Name:",node.name)
        print_debug("       -> Inputs:",len(node.inputs))
        for inp in node.inputs:
            print_debug("           -> Input:",inp.identifier)
            print_debug("               -> Hash:",inp.getHASH())
            print_debug("               -> Data:",inp.current_DATA)
            
        print_debug("       -> Outputs:",len(node.outputs))
        for inp in node.outputs:
            print_debug("           -> Output:",inp.identifier)
            print_debug("               -> Hash:",inp.getHASH())
            print_debug("               -> Data:",inp.current_DATA)
            
            
            
            
            
            
            
##\class DataHeap
#\brief Maintains all data passed between nodes.
#\detail Implemented as singleton, creates and maintains the generator's data heap.            
class DataHeap(object):
    
    ##\class __DataHeap
    #\brief Internal class.
    class __DataHeap:
    
        ##\property DATA
        #\brief List of BG_DataPackage objects
        DATA = None
    
        def __init__(self):
            
            self.DATA = []
            self.path = bpy.data.filepath
            
            
        def __str__(self):
            return "Data Heap"
            
        ##\fn storeData
        #\brief Stores data in DATA.
        #\detail Called by output sockets, creates a new BG_DataPackage object with the socket's pointer and data's pointer (if data is a 3D object), and stores it in DATA. Also checks if the loaded .blend file has changed and re-initializes itself if there's a new file (to avoid inter-file naming complications). 
        #\param data Data.
        #\param hash The socket's pointer.
        #\returns None
        def storeData(self,data,hash):
        
            
            testpath = bpy.data.filepath
            if not testpath == self.path:
                print_debug("INITIALIZING (STORE): File has changed. Re-initializing tree...")
                self.path = testpath
                self.cleanse()
        
        
            self.clearData(hash)

            print_debug("Storing data...","/",str(hash))
            
            if not data == []:
                if isinstance(data[0],bpy.types.Object):
                    for ob in data:
                        ob.name = "_BG_$STORED$_"
                        
                    tempData = BG_DataPackage()
                    datalist = [ob.as_pointer() for ob in data]
                    tempData.fill(datalist,hash,"obj")

                else:
                
                    tempData = BG_DataPackage()
                    tempData.fill(data,hash)
                    
            else:
                tempData = BG_DataPackage()
                tempData.fill(data,hash)
                    
                    

            print_debug("   -> stored:",str(tempData))
            self.DATA.append(tempData)
            
            
        ##\fn loadData
        #\brief Loads data from the heap.
        #\detail Checks all stores BG_DataPackage objects for the given pointer, then resolves the linked data and returns it.
        #\param hash The socket's pointer.
        #\returns The stored data or None when not found.
        def loadData(self,hash):
        
            testpath = bpy.data.filepath
            if not testpath == self.path:
                print_debug("INITIALIZING (LOAD): File has changed. Re-initializing tree...")
                self.path = testpath
                self.cleanse()
            
            print_debug("Loading data:",str(hash))
            
            retData = None
            
            for pack in self.DATA:
                if pack.sock == hash:
                    retData = pack
                    
            print_debug("   -> Data:", str(retData))
            
            if not retData == None:
                if retData.type == "obj":
                
                    obList = []
                    for sourceob_p in retData.data: 
                        for sourceob in bpy.data.objects:
                            if sourceob.as_pointer() == sourceob_p:
                
                                copyob = copyobj_GLO(sourceob)
                                obList.append(copyob)
                                break
                        
                    retData = obList
                    
                else:
                    retData = retData.data

            return retData
            
            
        ##\fn clearData
        #\brief Removes data from the heap.
        #\detail Removes the BG_DataPackage object linked to the socket from the heap.
        #\param hash The socket's pointer.
        #\returns None   
        def clearData(self,hash):
        
            print_debug("Clearing data:",str(hash))
            
            for pack in self.DATA:
                if pack.sock == hash:
                    if pack.type == "obj":
                    
                        for ob in bpy.data.objects:
                            if ob.as_pointer in pack.data:
                                ob.name = "_$OBS$_"
                        
                    self.DATA.remove(pack)
                    
        
        ##\fn cleanse
        #\brief Removes all data from the heap.
        #\detail Called when files have changed or anything else has happened that could possible endanger the heap's correctness.
        #\returns None
        def cleanse(self):
            
            for pack in self.DATA:
                if pack.type == "obj":
                
                    for ob in bpy.data.objects:
                        if ob.as_pointer in pack.data:
                            ob.name = "_$OBS$_"
                        
                self.DATA.remove(pack)
            
            
            
            
        
            
    ##\property instance
    #\brief The current __DataHeap instance.       
    instance = None
    
    
    ##\fn __new__:
    #\brief Instantiates or returns a __DataHeap object.
    def __new__(cls):
        if not DataHeap.instance:
            DataHeap.instance = DataHeap.__DataHeap()
        return DataHeap.instance   



        
##\class BG_DataPackage
#\brief Small class for stored data.
#\detail Made to store both the data and the socket linked to it in one place, for easy access. 
class BG_DataPackage(object):
    
    ##\property data
    #\brief Either a pointer to a 3D object or the data itself.
    data = None
    
    ##\property sock
    #\brief A pointer to the socket linked to data.
    sock = None
    
    ##\property type
    #\brief The datatype.
    type = None
        
        
    ##\fn fill
    #\brief Fills the object with data, socket pointer and type.
    #\param dat Data.
    #\param hash The socket's pointer.
    #\param typ Datatype(optional).
    #\returns None  
    def fill(self,dat,hash,typ = None):
        self.data = dat
        self.sock = hash
        self.type = typ
        
    def __str__(self):
        return("Data Package: "+str(self.data)+"  /  "+str(self.sock))
        
        
        
        
       
def copyobj_GLO(object):


    clear_selection_GLO()

    if isinstance(object,bpy.types.Object):
        print_debug("Copying(BG)(GLO):",object.name)

        name = object.name
        
        
        object.name = "_CPY"
        bpy.context.scene.objects.link(object)
        object.select = True
        bpy.context.scene.objects.active = object
        
        bpy.ops.object.duplicate()
        
        object.name = name
        
        for obj in bpy.context.scene.objects:
            if obj.name.startswith("_CPY"):
                copyob = obj
                break
        
        bpy.context.scene.objects.unlink(object)
        bpy.context.scene.objects.unlink(copyob)
        
        print_debug("   -> Copy:",copyob.name)
        
        copyob.name = "_$OBS$_"
        
        return copyob
        
        
        
def clear_selection_GLO():
    for ob in bpy.context.scene.objects:
        ob.select = False
        
        
        
        

            

            
            
            
        
    
    
    
    
    
    
    
    
    
    
    
    
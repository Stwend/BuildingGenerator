##\package buildingGen.utils.utils_GEN
# Generic utilities

import bpy
import math
import os

from . import utils_OBJ,utils_GLO

import random    




  
 

##\brief Adjusts lists of different lengths to the same size, extending shorter lists.
#\detail Goes through all lists, then adds the last element of each list to the list until all lists have the same length.
#\param lists List containing lists
#\return a list containing lists of the same length.     
def adjustLists(lists):
    length = 0
    for l in lists:
        if len(l) > length:
            length = len(l)
    
    for l in lists:
    
        if len(l) < length:
            index = len(l)-1
            togo = length - len(l)
            for i in range(0,togo):
                if isinstance(l[0], bpy.types.Object):
                    l.append(utils_OBJ.copyobj(l[index]))
                else:
                    l.append(l[index])
    
    return lists
 


##\brief Adjusts lists of different lengths to the same size, cutting longer lists.
#\detail Goes through all lists, then deletes the last elements of each list until their length equals the shortest list's length.
#\param lists List containing lists
#\return a list containing lists of the same length.   
def adjustListsCut(lists):
    for i in range(1,len(lists)):
        
        list = lists[i]
    
        if len(lists[i]) < len(lists[0]):
            lists[i] = adjustLists([lists[0],lists[i]])[1]
        elif len(lists[i]) > len(lists[0]):
            del list[-(len(list) - len(lists[0]))]
            
    return lists
    
    
    
    
def adjustLists2(lists):
    length = 0
    for l in lists:
        if len(l) > length:
            length = len(l)
    
    for l in lists:
    
        if len(l) < length:
            index = len(l)-1
            togo = length - len(l)
            for i in range(0,togo):
                l.append(l[index])
    
    return lists
    
    
    
    
    
    

    
    
    
    
    


        
    
    
    

    

        

            
            
        
    
    
            
        
        
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
##\package buildingGen.utils.utils_MATH
# Math utilities


import bpy
import math
import mathutils
from . import utils_GLO
 

##\brief Euler Distance.
#\returns (Float) The distance.
#\param point1 (mathutils.Vector) First point.
#\param point2 (mathutils.Vector) Second point.
def distanceEuler(point1, point2):
    result = math.sqrt(math.pow((point1[0] - point2[0]),2) + math.pow((point1[1]- point2[1]),2) + math.pow((point1[2]- point2[2]),2))
    return result


##\brief Euler Distance in 2D space.
#\returns (Float) The distance.
#\param point1 (mathutils.Vector) First point.
#\param point2 (mathutils.Vector) Second point.
def distanceEuler_2d(point1,point2):
    result = math.sqrt(math.pow((point1[0] - point2[0]),2) + math.pow((point1[1]- point2[1]),2))
    return result
    
    

##\brief Distance along an axis.
#\returns (Float) The distance.
#\param point1 (mathutils.Vector) First point.
#\param point2 (mathutils.Vector) Second point.
#\param axis (string in ["X","Y","Z"]) The axis.
def distanceAxis(point1, point2, axis):
    if axis == "X" or axis == "x":
        return math.fabs(point1[0] - point2[0])
        
    elif axis == "Y" or axis == "y":
        return math.fabs(point1[1] - point2[1])
        
    elif axis == "Z" or axis == "z":
        return math.fabs(point1[2] - point2[2])
        
        
        
        
        

##\brief Distance between a point and a line.
#\returns (mathutils.Vector) Shortest distance
#\param p (mathutils.Vector) A point.
#\param l1 (mathutils.Vector) First point on the line.
#\param l2 (mathutils.Vector) Second point on the line.
def distancePointLine(p,l1,l2):

    return vec3_length(vec3_cross(vec3_sub(p,l1),vec3_sub(p,l2)))/vec3_length(vec3_sub(l2,l1))
    
    
        
            
    
        
        

##\brief The middle coordinates of a list of points.
#\returns (mathutils.Vector) Middle coordinates.
#\param list (List of (mathutils.Vector)) List of points. 
def getMidCoords(list):
    length = len(list)
    
    if length == 0:
        return [0,0,0]
    
    x = 0
    y = 0
    z = 0
    
    for i in list:
        x = x + i[0]
        y = y + i[1]
        z = z + i[2]
    
    x = x/length
    y = y/length
    z = z/length
        
    return mathutils.Vector([x,y,z])
   


def vec3_length(vec):
    return math.sqrt(math.pow(vec[0],2) + math.pow(vec[1],2) + math.pow(vec[2],2))
    
    

##\brief Sets one axis to 0.
#\returns (mathutils.Vector) The new vector.
#\param vec (mathutils.Vector) A vector.
#\param axis (string in ["X","Y","Z"]) The axis.
def vec3_removeAxis(vec, axis):
    if axis != "All":
        if axis == "X":
            vec[0] = 0
        elif axis == "Y":
            vec[1] = 0
        elif axis == "Z":
            vec[2] = 0
    return vec
       
 

def vec3_add(vec3, vec3_2):
    x = vec3[0] + vec3_2[0]
    y = vec3[1] + vec3_2[1]
    z = vec3[2] + vec3_2[2]
    return [x,y,z]
 

def vec3_sub(vec3, vec3_2):
    x = vec3[0] - vec3_2[0]
    y = vec3[1] - vec3_2[1]
    z = vec3[2] - vec3_2[2]
    return [x,y,z]
  
       
def vec3_normalize(vec3):
    
    x = vec3[0]
    y = vec3[1]
    z = vec3[2]

    ratio = distanceEuler([0,0,0], vec3)
    
    if x != 0:
        x = x / ratio

    if y != 0:
        y = y / ratio
        
    if z != 0:
        z = z / ratio
    
    return [x,y,z]

    
def vec3_dot(vector1, vector2):
    dot = vector1[0]*vector2[0] + vector1[1]*vector2[1] + vector1[2]*vector2[2]
    return dot
 
 
def vec3_cross(vector1, vector2):

    x = vector1[1]*vector2[2] - vector1[2]*vector2[1]
    y = vector1[2]*vector2[0] - vector1[0]*vector2[2]
    z = vector1[0]*vector2[1] - vector1[1]*vector2[0]
    
    return [x,y,z]


    
def vec3_invert(vector):
    return [vector[0]*-1,vector[1]*-1,vector[2]*-1]

   
def vec3_fromPoints(point1, point2):
    x = point2[0] - point1[0]
    y = point2[1] - point1[1]
    z = point2[2] - point1[2]
    
    return vec3_normalize([x,y,z])
 

def vec3_fromPointsRaw(point1,point2):
    x = point2[0] - point1[0]
    y = point2[1] - point1[1]
    z = point2[2] - point1[2]
    
    return [x,y,z]
 
 
def vec3_scale(vec3,factor):

    x = vec3[0]*factor
    y = vec3[1]*factor
    z = vec3[2]*factor

    
    return [x,y,z]
    
    
    
    
    
    
    
    
    
    
    

##\brief Angle between two vectors in 3D space, unsigned.
#\returns (Float) The angle.
#\param vector1 (mathutils.Vector) Vector 1.
#\param vector2 (mathutils.Vector) Vector 2.
def getAngle(vector1, vector2):
    vector1 = vec3_normalize(vector1)
    vector2 = vec3_normalize(vector2)
    
    dot = vec3_dot(vector1, vector2)
    
    dot = math.acos(dot)
    
    dot = dot*180
    dot = dot/math.pi
    
    return dot
    


##\brief Angle between two vectors in 3D space, signed.
#\returns (Float) The angle.
#\param vector1 (mathutils.Vector) Vector 1.
#\param vector2 (mathutils.Vector) Vector 2.
#\param nor (mathutils.Vector) The normal vector relative to which the angle should be calculated.
def getAngleNor(vector1, vector2, nor):

    nvec = vec3_cross(nor, vector1);
    
    res = vec3_dot(nvec, vector2)

    vector1 = vec3_normalize(vector1)
    vector2 = vec3_normalize(vector2)
    
    dot = vec3_dot(vector1, vector2)
    
    dot = math.acos(dot)
    
    if dot > math.radians(180):
        dot = -(math.pi - dot)
    
    if res > 0:
        return dot
    else:
        return -dot
    
    
    
    
 
def toDegrees(radians):
    radians = radians*180
    return radians/math.pi
  
  
def toRadians(degree):
    degree = degree*math.pi
    return degree/180
    
    
    

##\brief Median element of a sortable list. 
#\returns (Float) The median.
#\param list (List) List of sortable elements. 
def getMedian(list):
    sorts = sorted(list)
    length = len(list)
    pos = int(length/2)
    
    return sorts[pos]


##\brief Interpolate between two values. 
#\returns (Float) The interpolated values.
#\param val1 (Float) Value 1   
#\param val2 (Float) Value 2
#\param ratio (Float) Ratio
#\param mode (String) Mode (currently only "Linear" is supported).     
def interpolate(val1, val2, ratio, mode = "Linear"):
    if mode == "Linear":
        return (val1*(1-ratio) + val2*ratio)
    elif mode == "Root":
        return()
    elif mode == "Sharp":
        return()
    elif mode == "Smooth":
        return()
 


def samePoint(point1,point2):
    if distanceEuler(point1,point2) < 0.05:
        return True
    else:
        return False
        
        
def fracMin(f1,f2):
    return min(f1,f2)/max(f1,f2)
  

  
def fracMax(f1,f2):
    return max(f1,f2)/min(f1,f2)
    
    



##\brief Checks if a point is inside a line segment.
#\detail Only call if you are sure that the point already is on the edge's line.
#\returns (Boolean) Whether the point is inside or not.
#\param p (mathutils.Vector) A point.
#\param e1 (mathutils.Vector) First edge point.
#\param e2 (mathutils.Vector) Second edge point.
def insideEdge(p,e1,e2):

    if distanceEuler(p,e1) < 0.001:
        return True
    if distanceEuler(p,e2) < 0.001:
        return True

    v1 = vec3_fromPointsRaw(e1,p)
    v2 = vec3_fromPointsRaw(p,e2)
    
    dot = vec3_dot(v1,v2)
    
    if dot > 0:
        return True
    else:
        return False
        


##\brief Checks if a point is inside a line segment (strictly).
#\detail Only call if you are sure that the point already is on the edge's line. Unlike insideEdge(), insideEdgeStrict() will return false if the point is located on one of the edge points.
#\returns (Boolean) Whether the point is inside or not.
#\param p (mathutils.Vector) A point.
#\param e1 (mathutils.Vector) First edge point.
#\param e2 (mathutils.Vector) Second edge point.        
def insideEdgeStrict(p,e1,e2):

    if distanceEuler(p,e1) < 0.001:
        return False
    if distanceEuler(p,e2) < 0.001:
        return False

    v1 = vec3_fromPointsRaw(e1,p)
    v2 = vec3_fromPointsRaw(p,e2)
    
    dot = vec3_dot(v1,v2)
    
    if dot > 0:
        return True
    else:
        return False
        

        
    
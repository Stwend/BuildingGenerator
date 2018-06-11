##\package buildingGen.utils.utils_GEOM
# Geometry utilities

import bpy
import math
import mathutils
import random

from . import utils_MATH, utils_OBJ,utils_GLO

##\brief Get mapped coords/edges of a polygon
#\returns (List of(List of (mathutils.Vector)),(List of (List of (Int))),(List of (mathutils.Vector))) Coords, mapped edge indices, and normals.
#\param ob (Object) The object holding the polygon
#\param polyID (Int) The index of the polygon in ob.data.polygons
def getMappedCoords(ob,polyID):

    coords = []
    coords_indexes = []
    edgemap = []
    
    nors = []

    poly = ob.data.polygons[polyID]
    
    for vID in poly.vertices:
        vert = ob.data.vertices[vID]
        coords.append(vert.co)
        coords_indexes.append(vert.index)
        nors.append(vert.normal)
        
    for edge in ob.data.edges:
        v1 = edge.vertices[0]
        v2 = edge.vertices[1]
        
        if v1 in coords_indexes and v2 in coords_indexes:
            
            ind1 = coords_indexes.index(v1)
            ind2 = coords_indexes.index(v2)
            
            mapped_edge = [ind1,ind2]
            
            edgemap.append(mapped_edge)

    
    return[coords,edgemap,nors]
    
    
    
    
    
    
    
   
        
    
    

##\brief Get the position of an edge.
#\returns (mathutils.Vector) The middle coordinates.
#\param object (Object) The object holding the edge.
#\param edgeID (Int) The index of the edge in ob.data.edges
def getEdgePos(object, edgeID):
    v1 = object.data.edges[edgeID].vertices[0]
    v2 = object.data.edges[edgeID].vertices[1]
    
    ed = [object.data.vertices[v1].co,object.data.vertices[v2].co]
    return utils_MATH.getMidCoords(ed)
 

##\brief Get the length of an edge.
#\returns (mathutils.Vector) The edge's length.
#\param object (Object) The object holding the edge.
#\param edgeID (Int) The index of the edge in ob.data.edges 
def getEdgeLength(object, edgeID):
    v1 = object.data.edges[edgeID].vertices[0]
    v2 = object.data.edges[edgeID].vertices[1]
    return utils_MATH.distanceEuler(object.data.vertices[v1].co,object.data.vertices[v2].co)
    

##\brief Get the normal vector of an edge.
#\returns (mathutils.Vector) The edge's normal.
#\param object (Object) The object holding the edge.
#\param edgeID (Int) The index of the edge in ob.data.edges     
def getEdgeNormal (object, edgeID):
    v1 = object.data.edges[edgeID].vertices[0]
    v2 = object.data.edges[edgeID].vertices[1]

    #check if there are any polygons containing both vertices (= the edge)
    
    normals_list = []
    
    for poly in object.data.polygons:
        if v1 in poly.vertices and v2 in poly.vertices:
            normals_list.append(poly.normal)
           
    edge_normal = mathutils.Vector([0.0,0.0,0.0])
    length = len(normals_list)
    if length > 0:
        for normal in normals_list:
            edge_normal += normal
    
    edge_normal.normalize()
    
    return edge_normal
    
 

##\brief Get the normal vector of an edge, depending on a given vector.
#\returns (mathutils.Vector) The edge's normal.
#\param object (Object) The object holding the edge.
#\param edgeID (Int) The index of the edge in ob.data.edges   
#\param vec (mathutils.Vector) The vector the edge's normal will be based on.
def getEdgeNormal_vec (object, edgeID, vec):
    
    
    v1 = object.data.vertices[object.data.edges[edgeID].vertices[0]]
    v2 = object.data.vertices[object.data.edges[edgeID].vertices[1]]
        
    edgevec = v1.co - v2.co
    
    edgevec2 = edgevec.cross(vec)
    
    edgevec3 = edgevec2.cross(edgevec)
    
    if edgevec3.dot(vec) < 0:
        edgevec3.negate()
        
    edgevec3.normalize()
    
    return edgevec3
    
    
    
##\brief Get the normal vector along an edge.
#\returns (mathutils.Vector) The edge's normal.
#\param object (Object) The object holding the edge.
#\param edgeID (Int) The index of the edge in ob.data.edges 
#\param axis (String in ["X","Y","Z","-X","-Y","-Z"]) The axis the edge's normal will be based on.
#\param fallback (String in ["X","Y","Z","-X","-Y","-Z"]) The axis the edge's normal will be based on in case axis is orthogonal to the edge's direction.
def getEdgeNormal_along(object,edgeID,axis = "Z",fallback = "X"):

    if not axis == fallback:
    
        v1 = object.data.vertices[object.data.edges[edgeID].vertices[0]]
        v2 = object.data.vertices[object.data.edges[edgeID].vertices[1]]
        
        vec = v1.co - v2.co
        vec.normalize()
        
        if "Z" in axis:
            axisvec = mathutils.Vector([0,0,1])
        elif "Y" in axis:
            axisvec = mathutils.Vector([0,1,0])
        elif "X" in axis:
            axisvec = mathutils.Vector([1,0,0])
            
        if "Z" in fallback:
            fallbackvec = mathutils.Vector([0,0,1])
        elif "Y" in fallback:
            fallbackvec = mathutils.Vector([0,1,0])
        elif "X" in fallback:
            fallbackvec = mathutils.Vector([1,0,0])
            
            
        if "-" in axis:
            axisvec.negate()
        if "-" in fallback:
            fallbackvec.negate()
            
            
            
            
            
        res = vec.dot(axisvec)
        if res < 0:
            vec = -vec
        if res == 0:
            res = vec.dot(fallbackvec)
            if res < 0:
                vec = -vec
                    
        return vec
        
    return mathutils.Vector([0,0,0])
    
    
    
##\brief Get the normal vectors of all faces adjactant to a given edge.
#\returns (mathutils.Vector) The face normals.
#\param object (Object) The object holding the edge.
#\param edge (Edge) The edge to be used.  
def getEdgeNeighborNormals(ob,edge):

    found = False
    
    for e in ob.data.edges:
        if not e.index == edge.index:
            if edge.vertices[0] == e.vertices[0]:
                
                v1 = ob.data.vertices[edge.vertices[1]].co
                v2 = ob.data.vertices[edge.vertices[0]].co
                v3 = ob.data.vertices[e.vertices[0]].co
                
                found = True
                
                edge_vec = v2-v1
                edge_norvec = v3-v2
                
            elif edge.vertices[0] == e.vertices[1]:
                
                v1 = ob.data.vertices[edge.vertices[1]].co
                v2 = ob.data.vertices[edge.vertices[0]].co
                v3 = ob.data.vertices[e.vertices[1]].co
                
                found = True
                
                edge_vec = v2-v1
                edge_norvec = v3-v2
                
                
    if not found:
        rot1 = mathutils.Matrix.Rotation(0, 4, "Z").to_3x3()
    else:
        rot1 = edge_vec.rotation_difference(edge_norvec).to_matrix().to_3x3()
        
        
        
    found = False
    
    for e in ob.data.edges:
        if not e.index == edge.index:
            if edge.vertices[1] == e.vertices[0]:
                
                v1 = ob.data.vertices[edge.vertices[0]].co
                v2 = ob.data.vertices[edge.vertices[1]].co
                v3 = ob.data.vertices[e.vertices[0]].co
                
                found = True
                
                edge_vec2 = v2-v1
                edge_norvec2 = v3-v2
                
            elif edge.vertices[1] == e.vertices[1]:
                
                v1 = ob.data.vertices[edge.vertices[0]].co
                v2 = ob.data.vertices[edge.vertices[1]].co
                v3 = ob.data.vertices[e.vertices[1]].co
                
                found = True
                
                edge_vec2 = v2-v1
                edge_norvec2 = v3-v2
                
                
    if not found:
        rot2 = mathutils.Matrix.Rotation(0, 4, "Z").to_3x3()
    else:
        rot2 = edge_vec2.rotation_difference(edge_norvec2).to_matrix().to_3x3()

  
  
    tvec = mathutils.Vector([0,1,0])
  
    nor1 = tvec * rot1
    nor2 = -tvec * rot2
        
    return[nor1,nor2]
    
    
##\brief Get the faces adjactant to a given edge.
#\returns (Face) The faces.
#\param object (Object) The object holding the edge.
#\param edge (Edge) The edge to be used.     
def getEdgeNeighborFaces(ob,edge):

    faces = []
    
    count = 0
    for face in ob.data.polygons:
        if count > 2:
            break
        if edge.vertices[0] in face.vertices and edge.vertices[1] in face.vertices:
            faces.append(face)
            count += 1
            
    return faces
        
    
                
                
                
    
    
    
    
    
    
    
    
    
    
    
 


#FILTERS
# Object needs to be in object mode, with selected geometry. All methods have object mode active again when finishing.


##\brief Flatten geometry to its average normal.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of(mathutils.Vector),(mathutils.Vector)) The flatten plane's anchor point, and its normal.
#\param ob (Object) The object holding the geometry.
def flatten_alongNormal(ob):

    points = []
    nors = []
    
    for vert in ob.data.vertices:
        if vert.select:
            points.append(vert.co)
            nors.append(vert.normal)
            
    plane_pt = mathutils.Vector(utils_MATH.getMidCoords(points))
    plane_no = mathutils.Vector(utils_MATH.getMidCoords(nors))
    
    
    for vert in ob.data.vertices:
        if vert.select:
    
            res = mathutils.geometry.intersect_line_plane(vert.co, vert.co + plane_no, plane_pt, plane_no)
            
            if not res == None:
                
                vert.co = res
                
    return [plane_pt,plane_no]
    
    
##\brief Flatten geometry to a vector.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of(mathutils.Vector),(mathutils.Vector)) The flatten plane's anchor point, and its normal.
#\param ob (Object) The object holding the geometry.
#\param vec (mathutils.Vector) The vector used as plane normal.   
def flatten_alongVector(ob,vec):

    points = []
    
    for vert in ob.data.vertices:
        if vert.select:
            points.append(vert.co)
            
    plane_pt = mathutils.Vector(utils_MATH.getMidCoords(points))
    plane_no = mathutils.Vector(vec)
    
    
    for vert in ob.data.vertices:
        if vert.select:
    
            res = mathutils.geometry.intersect_line_plane(vert.co, vert.co + plane_no, plane_pt, plane_no)
            
            if not res == None:
                
                vert.co = res
                
    return [plane_pt,plane_no]
    
    
##\brief Flatten geometry to a point using its average normal.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of(mathutils.Vector),(mathutils.Vector)) The flatten plane's anchor point, and its normal.
#\param ob (Object) The object holding the geometry.
#\param point (mathutils.Vector) The point used as the plane's anchor.    
def flatten_toPoint(ob,point):

    points = []
    nors = []
    
    for vert in ob.data.vertices:
        if vert.select:
            points.append(vert.co)
            nors.append(vert.normal)
            
    plane_pt = mathutils.Vector(point)
    plane_no = mathutils.Vector(utils_MATH.getMidCoords(nors))
    
    
    for vert in ob.data.vertices:
        if vert.select:
    
            res = mathutils.geometry.intersect_line_plane(vert.co, vert.co + plane_no, plane_pt, plane_no)
            
            if not res == None:
                
                vert.co = res
                
    return [plane_pt,plane_no]
    
    
##\brief Flatten geometry to a point using a given vector.
#\detail Intended to be used after the object has been prepared with utils_OBJ.prep() or any other prep function.
#\returns (List of(mathutils.Vector),(mathutils.Vector)) The flatten plane's anchor point, and its normal.
#\param ob (Object) The object holding the geometry.
#\param point (mathutils.Vector) The point used as the plane's anchor.
#\param vec (mathutils.Vector) The vector used as plane normal.          
def flatten_alongVectorToPoint(ob,point,vec):

            
    plane_pt = mathutils.Vector(point)
    plane_no = mathutils.Vector(vec)
    
    
    for vert in ob.data.vertices:
        if vert.select:
    
            res = mathutils.geometry.intersect_line_plane(vert.co, vert.co + plane_no, plane_pt, plane_no)
            
            
            if not res == None:
                
                vert.co = res
                
    return [plane_pt,plane_no]
    
    
##\brief Rotates an object so that it faces the same direction as a given vector.   
#\returns (None)
#\param ob (Object) The object holding the geometry.
#\param vec (mathutils.Vector) The direction vector.
def rotate_toVec(ob,vec):
    vec2 = mathutils.Vector(vec)
    vec1 = mathutils.Vector([0,0,1])
    
    rot = vec2.rotation_difference(vec1)
    
    rotmat = rot.to_matrix()
    
    for vert in ob.data.vertices:
        vert.co = vert.co * rotmat
        
##\brief Rotates a tile object to a given normal vector.
#\detail Also respects a dominant axis, and compensates for small angle offsets if wanted.
#\returns (None)
#\param ob (Object) The object holding the geometry.
#\param vec (mathutils.Vector) The normal vector.
#\param domAxis (String in ["X","Y","Z","-X","-Y","-Z"]) The dominant axis.
#\param offset (mathutils.Vector) The offset that will be applied to the tile before rotating.
#\param compensateNor(Boolean) Compensate for small angle offsets.
def tileToX(ob,vec,domAxis,offset,compensateNor = None):

    if "Z" in domAxis:
        prep = mathutils.Matrix.Rotation(0, 4, 'Z').to_3x3()
        check_nor = mathutils.Vector([0,0,1])
        check_axis_1 = "X"
        check_axis_2 = "Z"
        flatten = 2
        mult = 1
        check_nor2 = mathutils.Vector([0,1,0])
        check_nor3 = mathutils.Vector([0,-1,0])
        
        
    elif "X" in domAxis:
        prep = mathutils.Matrix.Rotation(math.radians(-90), 4, 'Y').to_3x3()
        check_nor = mathutils.Vector([1,0,0])
        check_axis_1 = "Z"
        check_axis_2 = "X"
        flatten = 0
        mult = -1
        check_nor2 = mathutils.Vector([0,1,0])
        check_nor3 = mathutils.Vector([0,-1,0])
        
        
    elif "Y" in domAxis:
        prep = mathutils.Matrix.Rotation(math.radians(180), 4, 'Z').to_3x3() * mathutils.Matrix.Rotation(math.radians(90), 4, 'X').to_3x3()
        check_nor = mathutils.Vector([0,1,0])
        check_axis_1 = "X"
        check_axis_2 = "Y"
        flatten = 1
        mult = -1
        check_nor2 = mathutils.Vector([0,0,1])
        check_nor3 = mathutils.Vector([0,0,-1])
    
    
    

    rot_inv = mathutils.Matrix.Rotation(math.radians(180), 4, 'Z').to_3x3()

    
    
    
    
    
    ang = vec.angle(check_nor)
    
    rot = mathutils.Matrix.Rotation(mult * ang, 4, check_axis_1).to_3x3()
    
    vec2 = vec.copy()
    
    vec2[flatten] = 0
    
    rot2 = utils_MATH.getAngleNor(vec2,check_nor3,check_nor) + math.radians(180)
    
    
    rot2 = mathutils.Matrix.Rotation(rot2, 4, check_axis_2).to_3x3()
        
    if compensateNor != None:
    
        rotadd_cor = mathutils.Matrix.Rotation(math.radians(-90), 4, "Z").to_3x3()
    
        testVec = check_nor3.copy()

        if not "-" in domAxis:
        
            if vec[flatten] >= 0:
        
                rotmat = rot * rot2
                
                testVec.rotate(rotmat.inverted())
                
                testVec2 = compensateNor.cross(vec)

                angle = utils_MATH.getAngleNor(testVec2,testVec,check_nor)
                    
                rotadd = mathutils.Matrix.Rotation(angle, 4, check_axis_2).to_3x3()
                
                rotmat = rotadd_cor * rot_inv * prep * rotadd * rot * rot2
                
            else:
            
                rotmat = rot * rot2
                
                testVec.rotate(rotmat.inverted())
                
                testVec2 = compensateNor.cross(vec)

                angle = utils_MATH.getAngleNor(testVec2,testVec,check_nor)
                    
                rotadd = mathutils.Matrix.Rotation(-angle, 4, check_axis_2).to_3x3()
                
                rotmat = rotadd_cor * prep * rotadd * rot * rot2
                
 
        else:
            
            if vec[flatten] <= 0:
        
                rotmat = rot * rot2
                
                testVec.rotate(rotmat.inverted())
                
                testVec2 = compensateNor.cross(vec)


                angle = utils_MATH.getAngleNor(testVec2,testVec,check_nor)
                    
                rotadd = mathutils.Matrix.Rotation(angle, 4, check_axis_2).to_3x3()
                
                rotmat = rotadd_cor * rot_inv * prep * rotadd * rot * rot2
                
            else:
            
                rotmat = rot * rot2
                
                testVec.rotate(rotmat.inverted())
                
                testVec2 = compensateNor.cross(vec)


                angle = utils_MATH.getAngleNor(testVec2,testVec,check_nor)
                    
                rotadd = mathutils.Matrix.Rotation(-angle, 4, check_axis_2).to_3x3()
                
                rotmat = rotadd_cor * prep * rotadd * rot * rot2
                
                
                
                
                
    else:
        
        if not "-" in domAxis:
            rotmat = rot_inv * prep *  rot * rot2
        else:
            rotmat = prep * rot * rot2
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        

    for vert in ob.data.vertices:

        vert.co = (vert.co * rotmat) + offset
            
            
##\brief Rotates a tile object to a given normal vector using a rotation matrix.
#\returns (None)
#\param ob (Object) The tile holding the geometry.
#\param rotmat (mathutils.Matrix) The rotation as a 3x3 matrix.
#\param offset (mathutils.Vector) The offset that will be applied to the tile before rotating.
def tileToX_rotmat(ob,rotmat,offset):

    inv = mathutils.Matrix.Rotation(math.radians(180), 4, 'Z').to_3x3()

    rotmat.invert()
    
    mat = inv*rotmat
    
    for vert in ob.data.vertices:
        vert.co = (vert.co * mat) + offset
    
            
            
        
            
            
            
        
##\brief Offsets a tile along a given offset vector.
#\returns (None)
#\param tile (Object) The tile holding the geometry.
#\param offset (mathutils.Vector) The offset. 
def offset_dom(tile,offset):

    for vert in tile.data.vertices:
        vert.co += mathutils.Vector(offset)
        
        
##\brief Rotates an edge or a polygon to tile requirements.
#\returns ([[mathutils.Vector],mathutils.Matrix,[mathutils.Vector]]) Rotated vertice coordinates, rotation matrix, rotated vertice normals.
#\param coords (List of (mathutils.Vector)) Coordinates of the polygon/edge vertices.
#\param center (mathutils.Vector) Center coordinates.
#\param vec (mathutils.Vector) Polygon/Edge normal vector.
#\param domAxis (String in ["X","Y","Z","-X","-Y","-Z"]) The dominant axis.
#\param nors (List of (mathutils.Vector)) Normals of the polygon/edge vertices (optional).    
def xToTile(coords,center,vec,domAxis,nors = None):

    c = center.copy()
    c.negate()

    
    retco = []
    retnors = []

    if domAxis == "Z":
    
        check_nor = mathutils.Vector([0,1,0])
        check_nor2 = mathutils.Vector([0,0,1])
        check_nor3 = mathutils.Vector([0,-1,0])
        up = check_nor2
    
        vec_c = vec.copy()

        vec_c[2] = 0

        
        ang = -utils_MATH.getAngleNor(vec_c,check_nor,up)
        
        rot1 = mathutils.Matrix.Rotation(ang, 4, 'Z').to_3x3()
        
        vec_rot = vec.copy()
        vec_rot.rotate(rot1)

        ang2 = -vec_rot.angle(up)
        
        rot2 = mathutils.Matrix.Rotation(ang2, 4, 'X').to_3x3()

        rotmat = rot1 * rot2
            
            
    elif domAxis == "-Z":
    
        check_nor = mathutils.Vector([0,1,0])
        check_nor2 = mathutils.Vector([0,0,1])
        check_nor3 = mathutils.Vector([0,-1,0])
        up = check_nor2

        vec_c = vec.copy()

        vec_c[2] = 0

        rotadd = mathutils.Matrix.Rotation(math.radians(180), 4, 'Z').to_3x3()
        
        ang = -utils_MATH.getAngleNor(vec_c,check_nor,up)
        
        rot1 = mathutils.Matrix.Rotation(ang, 4, 'Z').to_3x3()
        
        vec_rot = vec.copy()
        vec_rot.rotate(rot1)

        ang2 = -vec_rot.angle(up)
        
        rot2 = mathutils.Matrix.Rotation(ang2, 4, 'X').to_3x3()

        rotmat = rot1 * rot2 * rotadd


            
            
    
    
    elif domAxis == "X":
    
        if vec[1] <= 0:
            prep = mathutils.Matrix.Rotation(math.radians(-90), 4, 'Z').to_3x3()
        else:
            prep = mathutils.Matrix.Rotation(math.radians(90), 4, 'Z').to_3x3()
    
        check_nor = mathutils.Vector([0,1,0])
        check_nor2 = mathutils.Vector([0,0,1])
        check_nor3 = mathutils.Vector([0,-1,0])
        up = check_nor2
    
        vec_c = vec.copy()

        vec_c[2] = 0

        
        ang = -utils_MATH.getAngleNor(vec_c,check_nor,up)
        
        rot1 = mathutils.Matrix.Rotation(ang, 4, 'Z').to_3x3()
        
        vec_rot = vec.copy()
        vec_rot.rotate(rot1)

        ang2 = -vec_rot.angle(up)
        
        rot2 = mathutils.Matrix.Rotation(ang2, 4, 'X').to_3x3()

        rotmat = rot1 * rot2 * prep


            
            
    
    elif domAxis == "-X":
    
        if vec[1] >= 0:
            prep = mathutils.Matrix.Rotation(math.radians(-90), 4, 'Z').to_3x3()
        else:
            prep = mathutils.Matrix.Rotation(math.radians(90), 4, 'Z').to_3x3()
    
        check_nor = mathutils.Vector([0,1,0])
        check_nor2 = mathutils.Vector([0,0,1])
        check_nor3 = mathutils.Vector([0,-1,0])
        up = check_nor2
    
        vec_c = vec.copy()

        vec_c[2] = 0

        
        ang = -utils_MATH.getAngleNor(vec_c,check_nor,up)
        
        rot1 = mathutils.Matrix.Rotation(ang, 4, 'Z').to_3x3()
        
        vec_rot = vec.copy()
        vec_rot.rotate(rot1)

        ang2 = -vec_rot.angle(up)
        
        rot2 = mathutils.Matrix.Rotation(ang2, 4, 'X').to_3x3()

        rotmat = rot1 * rot2 * prep


            
            
            
            
            
            
    elif domAxis == "Y":
    
        if vec[0] >= 0:
            prep = mathutils.Matrix.Rotation(math.radians(-90), 4, 'Z').to_3x3()
        else:
            prep = mathutils.Matrix.Rotation(math.radians(90), 4, 'Z').to_3x3()
    
        check_nor = mathutils.Vector([0,1,0])
        check_nor2 = mathutils.Vector([0,0,1])
        check_nor3 = mathutils.Vector([0,-1,0])
        up = check_nor2
    
        vec_c = vec.copy()

        vec_c[2] = 0

        
        ang = -utils_MATH.getAngleNor(vec_c,check_nor,up)
        
        rot1 = mathutils.Matrix.Rotation(ang, 4, 'Z').to_3x3()
        
        vec_rot = vec.copy()
        vec_rot.rotate(rot1)

        ang2 = -vec_rot.angle(up)
        
        rot2 = mathutils.Matrix.Rotation(ang2, 4, 'X').to_3x3()

        rotmat = rot1 * rot2 * prep


            
            
            
    elif domAxis == "-Y":
    
        if vec[0] <= 0:
            prep = mathutils.Matrix.Rotation(math.radians(-90), 4, 'Z').to_3x3()
        else:
            prep = mathutils.Matrix.Rotation(math.radians(90), 4, 'Z').to_3x3()
    
        check_nor = mathutils.Vector([0,1,0])
        check_nor2 = mathutils.Vector([0,0,1])
        check_nor3 = mathutils.Vector([0,-1,0])
        up = check_nor2
    
        vec_c = vec.copy()

        vec_c[2] = 0

        
        ang = -utils_MATH.getAngleNor(vec_c,check_nor,up)
        
        rot1 = mathutils.Matrix.Rotation(ang, 4, 'Z').to_3x3()
        
        vec_rot = vec.copy()
        vec_rot.rotate(rot1)

        ang2 = -vec_rot.angle(up)
        
        rot2 = mathutils.Matrix.Rotation(ang2, 4, 'X').to_3x3()

        rotmat = rot1 * rot2 * prep

            
            
    for co in coords:
        retco.append((co+c) * rotmat)
            
    
    if not nors == None:
        for nor in nors:
            retnors.append(nor * rotmat)
            
            
            
            
            
                
    return [retco,rotmat,retnors]
    
    
    

    
##\brief Projects mesh along average normal axis onto another mesh.
#\returns (None)
#\param ob (Object) The object to be projected.
#\param tar (Object) The target <ob> gets projected onto.
#\param selV ([Int]) IDs of selected vertices
#\param neg (Boolean) Project to opposite direction.        
def project_nor(ob,tar,selV,neg):

    bpy.context.scene.objects.active = tar

    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if not neg:
    
        for vID in selV:
        
            vert = ob.data.vertices[vID]
            
            replace = vert.co
            
            dis = None
            
            for face in tar.data.polygons:
            
                v1 = tar.data.vertices[face.vertices[0]].co
                v2 = tar.data.vertices[face.vertices[1]].co
                v3 = tar.data.vertices[face.vertices[2]].co
                


                result =  mathutils.geometry.intersect_ray_tri(v1, v2, v3, vert.normal, vert.co,True)
                
                if not result == None:
                
                    tdis = utils_MATH.distanceEuler(vert.co,result)
                
                    if not dis == None:
                        if tdis < dis:
                            dis = tdis
                            replace = result
                    else:
                        dis = tdis
                        replace = result
                        
            vert.co = replace
                    
    else:
    
        for vID in selV:
        
            vert = ob.data.vertices[vID]
            
            replace = vert.co
            
            dis = None
            
            
            for face in tar.data.polygons:

            
                v1 = tar.data.vertices[face.vertices[0]].co
                v2 = tar.data.vertices[face.vertices[1]].co
                v3 = tar.data.vertices[face.vertices[2]].co
                


                result =  mathutils.geometry.intersect_ray_tri(v1, v2, v3, -vert.normal, vert.co,True)
                
                if not result == None:
                    tdis = utils_MATH.distanceEuler(vert.co,result)
                
                    if not dis == None:
                        if tdis < dis:
                            dis = tdis
                            replace = result
                    else:
                        dis = tdis
                        replace = result
                    
            vert.co = replace        
                    
                    
                    
##\brief Projects mesh along average normal axis onto another mesh, picks the shortest distance (between negative and positive normal direction).
#\returns (None)
#\param ob (Object) The object to be projected.
#\param tar (Object) The target <ob> gets projected onto.
#\param selV ([Int]) IDs of selected vertices                   
def project_nor_shortest(ob,tar,selV):

    
    bpy.context.scene.objects.active = tar

    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.object.mode_set(mode = 'OBJECT')

    
    for vID in selV:
    
        vert = ob.data.vertices[vID]
        
        replace = vert.co
        
        disMin = None
        
        for face in tar.data.polygons:

        
            v1 = tar.data.vertices[face.vertices[0]].co
            v2 = tar.data.vertices[face.vertices[1]].co
            v3 = tar.data.vertices[face.vertices[2]].co
            
            result =  mathutils.geometry.intersect_ray_tri(v1, v2, v3, vert.normal, vert.co,True)
            result2 =  mathutils.geometry.intersect_ray_tri(v1, v2, v3, -vert.normal, vert.co,True)
            
            if not result2 == None:
                dis = utils_MATH.distanceEuler(vert.co,result2)
                if not disMin == None:
                    if dis < disMin:
                        replace = result2
                        disMin = dis
                else:
                    replace = result2
                    disMin = dis
                        
                        

            if not result == None:
                dis = utils_MATH.distanceEuler(vert.co,result)
                if not disMin == None:
                    if dis < disMin:
                        replace = result
                        disMin = dis
                else:
                    replace = result
                    disMin = dis
                    
        vert.co = replace
        
        
##\brief Projects mesh along average normal axis onto another mesh, picks closest vertice/face surface.
#\returns (None)
#\param ob (Object) The object to be projected.
#\param tar (Object) The target <ob> gets projected onto.
#\param selV ([Int]) IDs of selected vertices
#\param mode (String in ["v","s"]) Projection mode (Vertices or Surface).     
def project_closest(ob,tar,selV,mode):


    if mode == "v":
        
        for vID in selV:
            vert = ob.data.vertices[vID]
            
            dis = None
            
            replace = vert.co
            
            for vert2 in tar.data.vertices:
            
                disV = utils_MATH.distanceEuler(vert.co,vert2.co)
                
                if not dis == None:
                    if disV < dis:
                        dis = disV
                        replace = vert2.co
                else:
                    dis = disV
                    replace = vert2.co        
            vert.co = replace
                    
    elif mode == "s":
    
        bpy.context.scene.objects.active = tar

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        for vID in selV:
            
            vert = ob.data.vertices[vID]
            
            disMin = None
            
            replace = vert.co
            
            for face in tar.data.polygons:
                
                result = mathutils.geometry.distance_point_to_plane(vert.co, face.center, face.normal)
                
                if not disMin == None:
                    
                    if math.fabs(result) < disMin:
                    
                        v1 = tar.data.vertices[face.vertices[0]].co
                        v2 = tar.data.vertices[face.vertices[1]].co
                        v3 = tar.data.vertices[face.vertices[2]].co


                        test = vert.co - result*face.normal

                            
                        res = mathutils.geometry.intersect_point_tri(test, v1,v2,v3)
                        
                        if not res == None:
                            replace = test
                            disMin = math.fabs(result)
                            
                else:
                
                    v1 = tar.data.vertices[face.vertices[0]].co
                    v2 = tar.data.vertices[face.vertices[1]].co
                    v3 = tar.data.vertices[face.vertices[2]].co
                

                
                    test = vert.co - result*face.normal


                    res = mathutils.geometry.intersect_point_tri(test, v1,v2,v3)
                    
                    if not res == None:
                        replace = test
                        disMin = math.fabs(result)
                    
                            
                            
            vert.co = replace
                        
                        
            
    
    

    
    
    
    
    
##\brief Projects mesh along a given vector onto another mesh.
#\returns (None)
#\param ob (Object) The object to be projected.
#\param tar (Object) The target <ob> gets projected onto.
#\param selV ([Int]) IDs of selected vertices
#\param vec (mathutils.Vector) Projection vector.
#\param neg (Boolean) Project to opposite direction.    
def project_vec(ob,tar,selV,vec,neg):

    bpy.context.scene.objects.active = tar

    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if not neg:
    
        for vID in selV:
        
            vert = ob.data.vertices[vID]
            
            replace = vert.co
            
            dis = None
            
            for face in tar.data.polygons:
            
                v1 = tar.data.vertices[face.vertices[0]].co
                v2 = tar.data.vertices[face.vertices[1]].co
                v3 = tar.data.vertices[face.vertices[2]].co
                


                result =  mathutils.geometry.intersect_ray_tri(v1, v2, v3, vec, vert.co,True)
                
                if not result == None:
                
                    tdis = utils_MATH.distanceEuler(vert.co,result)
                
                    if not dis == None:
                        if tdis < dis:
                            dis = tdis
                            replace = result
                    else:
                        dis = tdis
                        replace = result
                        
            vert.co = replace
                    
    else:
    
        for vID in selV:
        
            vert = ob.data.vertices[vID]
            
            replace = vert.co
            
            dis = None
            
            
            for face in tar.data.polygons:

            
                v1 = tar.data.vertices[face.vertices[0]].co
                v2 = tar.data.vertices[face.vertices[1]].co
                v3 = tar.data.vertices[face.vertices[2]].co
                


                result =  mathutils.geometry.intersect_ray_tri(v1, v2, v3, -vec, vert.co,True)
                
                if not result == None:
                    tdis = utils_MATH.distanceEuler(vert.co,result)
                
                    if not dis == None:
                        if tdis < dis:
                            dis = tdis
                            replace = result
                    else:
                        dis = tdis
                        replace = result
                    
            vert.co = replace        
                    
    
    

##\brief Projects mesh along a given vector onto another mesh, picks the shortest distance (between negative and positive normal direction).
#\returns (None)
#\param ob (Object) The object to be projected.
#\param tar (Object) The target <ob> gets projected onto.
#\param selV ([Int]) IDs of selected vertices  
#\param vec (mathutils.Vector) Projection vector.
def project_vec_shortest(ob,tar,selV,vec):

    
    bpy.context.scene.objects.active = tar

    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.object.mode_set(mode = 'OBJECT')

    
    for vID in selV:
    
        vert = ob.data.vertices[vID]
        
        replace = vert.co
        
        disMin = None
        
        for face in tar.data.polygons:

        
            v1 = tar.data.vertices[face.vertices[0]].co
            v2 = tar.data.vertices[face.vertices[1]].co
            v3 = tar.data.vertices[face.vertices[2]].co
            
            result =  mathutils.geometry.intersect_ray_tri(v1, v2, v3, vec, vert.co,True)
            result2 =  mathutils.geometry.intersect_ray_tri(v1, v2, v3, -vec, vert.co,True)
            
            if not result2 == None:
                dis = utils_MATH.distanceEuler(vert.co,result2)
                if not disMin == None:
                    if dis < disMin:
                        replace = result2
                        disMin = dis
                else:
                    replace = result2
                    disMin = dis
                        
                        

            if not result == None:
                dis = utils_MATH.distanceEuler(vert.co,result)
                if not disMin == None:
                    if dis < disMin:
                        replace = result
                        disMin = dis
                else:
                    replace = result
                    disMin = dis
                    
        vert.co = replace    
        
    
    
            




 
    
   

# OPERATORS
    

##\brief Deletes selected geometry.
#\returns (None)
#\param mode (String in ["VERT","EDGE","FACE","ONLY_FACE","EDGE_FACE"]) The delete mode.    
def delete(mode):
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type=mode)
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
##\brief Extrudes selected geometry (vertices).
#\returns (None)  
def extrudeV():
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.extrude_verts_indiv()
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')

##\brief Extrudes selected geometry (edges).
#\returns (None)  
def extrudeE():
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.extrude_edges_indiv()
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
##\brief Extrudes selected geometry (regions).
#\returns (None)  
def extrudeF():
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.extrude_region()
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')

##\brief Extrudes selected geometry (faces).
#\returns (None)     
def extrudeF_indiv():
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.inset(use_boundary = True, use_even_offset = True, use_relative_offset = False, use_edge_rail = True, thickness = 0, depth = 0, use_outset = False, use_select_inset = False, use_individual = True, use_interpolate = True)
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
##\brief Merges selected geometry.
#\returns (None)   
#\param collapse (Boolean) Whether to use collapsing edges or not. 
def merge(collapse):
    bpy.ops.object.mode_set(mode = 'EDIT')
    if not collapse:
        bpy.ops.mesh.merge(type='CENTER', uvs=False)
    else:
        bpy.ops.mesh.edge_collapse()
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
##\brief Merges selected geometry (only double vertices).
#\returns (None)   
#\param thr (Float) Merging threshold.
#\param unsel (Boolean) Include previously unselected geometry.     
def merge_doubles(thr,unsel):
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.remove_doubles(threshold = thr, use_unselected = unsel)
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
##\brief Triangulates selected geometry.
#\returns (None)   
#\param qm (String in ["BEAUTY","FIXED","FIXED_ALTERNATE","SHORTEST_DIAGONAL"]) Quad triangulation method.
#\param pm (String in ["BEAUTY","CLIP"]) NGon triangulation method.    
def triangulate(qm, pm):
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method=qm, ngon_method=pm)
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
##\brief Converts selected geometry to quads if possible.
#\returns (None)   
#\param UV (Boolean) Respect UVs.
#\param VCol (Boolean) Respect vertex colors.
#\param Sharp (Boolean) Respect sharpness.
#\param Material (Boolean) Respect materials.  
def make_quads(UV,VCol,Sharp,Material):
    bpy.ops.object.mode_set(mode = 'EDIT')
                    
                    
    angle = 10
                    
    for count in range (0,9):
        bpy.ops.mesh.tris_convert_to_quads(limit=utils_MATH.toRadians(angle), uvs=UV, vcols=VCol, sharp=Sharp, materials=Material)
        angle += 10
                        
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    


##\brief Bevels selected geometry.
#\returns (None)   
#\param offset_t (String in ["OFFSET","WIDTH","DEPTH","PERCENT"]) Offset method.
#\param amount (Float) Bevel amount.
#\param seg (Int) Number of segments.
#\param pr (Float) Profile shape.
#\param verts (Boolean) If true, vertices only.
def bevel(offset_t,amount,seg,pr,verts):
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.bevel(offset_type = offset_t, offset = amount, segments = seg, profile = pr, vertex_only = verts)
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
##\brief Fills holes in selected geometry.
#\returns (None)   
def fill():
    bpy.ops.object.mode_set(mode = 'EDIT')
    try:
        bpy.ops.mesh.edge_face_add()
    except:
        pass
    bpy.ops.mesh.select_mode(type="VERT")    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
##\brief Insets selected geometry.
#\returns (None)   
#\param bound (Boolean) If true, inset from open borders. 
#\param rel (Boolean) If true, use relative amount.
#\param amount (Float) Inset amount.
#\param out (Boolean) If true, outset instead of inset.
#\param indiv (Boolean) If true, inset individual faces.
#\param merge (Boolean) If true, merge at center.
def inset(bound,rel,amount,out,indiv,merge):

    ob = bpy.context.scene.objects.active
            
    length = len(ob.data.polygons)

    if not merge and length > 0:
        bpy.ops.object.mode_set(mode = 'EDIT')
        try:
            bpy.ops.mesh.inset(use_boundary = bound, use_even_offset = True, use_relative_offset = rel, use_edge_rail = True, thickness = amount, depth = 0, use_outset = out, use_select_inset = False, use_individual = indiv, use_interpolate = True)
        except:
            pass
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
    elif not indiv:
 
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        #delete all but selection border
        try:
            inset_mergeAtCenter()
        except:
            pass
        
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
    else:
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        try:
            bpy.ops.mesh.inset(use_boundary = bound, use_even_offset = True, use_relative_offset = rel, use_edge_rail = True, thickness = 0, depth = 0, use_outset = out, use_select_inset = False, use_individual = True, use_interpolate = True)

            bpy.ops.mesh.edge_collapse()
        except:
            pass
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.object.mode_set(mode = 'OBJECT')
 

 
##\brief Insets selected geometry to a straight skeleton.
#\returns (None)   
def inset_skeleton():

    #Iterative intersection detection, similar to the way a polygon's straight skeleton is built:
    
    #In each iteration, the remaining part of the roof is inset to the point where either two or more vertices are in the same position or an edge and a vert overlap.
    #All of these double vertices are merged and then marked in a vertex group as a "line".
    #The remaining faces are inset again, and so on and so on, until there are no more faces to inset.
    #Then, all edges that are not part of a line or the border are deleted to get rid of the unnecessary inset borders between the line and the mesh border.
    #The line parts are then merged together.
    #After the inset center lines have been merged into one line, all end points are selected.
    #Each end point will go outwards and search for a "real" edge (a corner, not just a part of a straight line), then form a triangle with that edge.
    #After that, for each pait of line ends, an algorithm will select the border part that is the most fitting (searching from one of the end triangles, the most fitting border is the one that directly connects to the other end's triangle)
    #Then, Blender's internal filling method will take care of filling the spaces.
    #Before returning, the center line is selected to ease selection in the node editor
    
    
    #Optional: Straightening of almost-straight edge loops by removing verts in the final skeleton. (NEEDED: Threshold input)
    
    
    
    #CAUTION: This algorithm WILL create unevenly shaped roofs if the roof's base is unevenly shaped (even as much as differing widths in different building extrusions)!
    
    
    
    #STEP 1: Gather data, object preparation
    
    #Hide all geometry that doesnt take part
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.hide(unselected=True)
    
    #get object reference
    ob = bpy.context.scene.objects.active
    bpy.ops.mesh.dissolve_limited(angle_limit=0.0001, use_dissolve_boundaries=False,delimit=set(["MATERIAL"]))
    bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, use_relative_offset=False, use_edge_rail=False, thickness=0.01, depth=0.0, use_outset=False, use_select_inset=False, use_individual=False, use_interpolate=False)
    
    #Save border in vertex group
    bpy.ops.mesh.select_all(action='INVERT')
    bordergroup = ob.vertex_groups.new("$BG$_BORDER")
    bpy.ops.object.vertex_group_set_active(group = bordergroup.name)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action='INVERT')

    shortest_distance = inset_findShortestDistance(ob)
    shortest_dis = shortest_distance
    
    #Perform Inset on the rest, select insides
    #This will ensure that the inverses of the vectors we need are the only edge of the border vertices that is currently not selected
    
    bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, use_relative_offset=False, use_edge_rail=False, thickness=shortest_distance, depth=0.0, use_outset=False, use_select_inset=False, use_individual=False, use_interpolate=False)

    
    
    linegroup = ob.vertex_groups.new("$BG$_LINE")
    
    
    result = inset_merge(ob,linegroup)
    
    
    
    
    
    
    #STEP 2: Inset until you hit the center everywhere
    
    
    while result:
    
        bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, use_relative_offset=False, use_edge_rail=False, thickness=0.005, depth=0.0, use_outset=False, use_select_inset=False, use_individual=False, use_interpolate=False)

        bpy.ops.object.vertex_group_set_active(group = linegroup.name)
        bpy.ops.object.vertex_group_remove_from(use_all_groups=True, use_all_verts=False)

        shortest_distance = inset_findShortestDistance(ob)
        
        bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, use_relative_offset=False, use_edge_rail=False, thickness=shortest_distance, depth=0.0, use_outset=False, use_select_inset=False, use_individual=False, use_interpolate=False)
        
        bpy.ops.object.vertex_group_set_active(group = linegroup.name)
        bpy.ops.object.vertex_group_remove_from(use_all_groups=False, use_all_verts=False)
        
        result = inset_merge(ob,linegroup)
        
        
    #insetting is done, we now have all line parts inside the "$BG$_LINE" vertex group.
    
    #STEP 3: Line processing
    #Prone to errors, needs refining!
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT') 
    bpy.ops.object.vertex_group_set_active(group = linegroup.name)
    bpy.ops.object.vertex_group_select()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
       
    line_ends = []
    
        
    for vert in ob.data.vertices:
        if vert.select and not vert.hide:
            count = 0
            nb = getNeighborVerts(ob,vert.index)
            for n in nb:
                if ob.data.vertices[n].select:
                    count += 1
            if count < 2:
                #vert is end of line
                line_ends.append(vert.index)
          
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT') 
    bpy.ops.object.mode_set(mode = 'OBJECT')

    
                    
    for vID1 in line_ends:
        
        for vID2 in line_ends:
                
            if not vID1 == vID2:
                
                ob.data.vertices[vID1].select = True
                ob.data.vertices[vID2].select = True
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.shortest_path_select(use_length=True)
                bpy.ops.object.mode_set(mode = 'OBJECT')
                    
                if straightLine_sel(ob):
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    #Connect separated line parts by searching for straight lines connecting the ends of line parts (that happened automatically due to insetting)
                    bpy.ops.object.vertex_group_assign()
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_all(action='DESELECT') 
                bpy.ops.object.mode_set(mode = 'OBJECT')
   
    
        
    
    #Delete everything but the border and the line
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.object.vertex_group_set_active(group = bordergroup.name)
    bpy.ops.object.vertex_group_select()
    
    bpy.ops.object.vertex_group_set_active(group = linegroup.name)
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.delete(type='VERT')
    
    bpy.ops.mesh.select_all(action='DESELECT')
    
    bpy.ops.mesh.select_mode(type="EDGE")
    
    bpy.ops.object.vertex_group_set_active(group = linegroup.name)
    bpy.ops.object.vertex_group_select()
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    

        
    #Dissolve verts on straight lines
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='SELECT') 
    bpy.ops.mesh.dissolve_limited(angle_limit=0.001, use_dissolve_boundaries=False, delimit=set(["MATERIAL"]))
    bpy.ops.mesh.select_all(action='DESELECT') 
    
    
    
    
    bpy.ops.object.vertex_group_select()
    
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.mesh.select_mode(type="EDGE")
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    eIDs = []
    
    for face in ob.data.polygons:
        if face.select and len(face.vertices) == 3:
            
            v1 = ob.data.vertices[face.vertices[0]]
            v2 = ob.data.vertices[face.vertices[1]]
            v3 = ob.data.vertices[face.vertices[2]]
            
            l1 = utils_MATH.distanceEuler(v1.co,v2.co)
            l2 = utils_MATH.distanceEuler(v3.co,v2.co)
            l3 = utils_MATH.distanceEuler(v1.co,v3.co)
            
            m = max([l1,l2,l3])
            
            if m == l1:
                for edge in ob.data.edges:
                    if v1.index in edge.vertices and v2.index in edge.vertices:
                        eIDs.append(edge.index)
                        break
                        
                        
            if m == l2:
                for edge in ob.data.edges:
                    if v3.index in edge.vertices and v2.index in edge.vertices:
                        eIDs.append(edge.index)
                        break
                        
            if m == l3:
                for edge in ob.data.edges:
                    if v1.index in edge.vertices and v3.index in edge.vertices:
                        eIDs.append(edge.index)
                        break
                        
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT') 
    bpy.ops.object.mode_set(mode = 'OBJECT') 
    
    for id in eIDs:
        ob.data.edges[id].select = True
        
                        
            
            
            
    bpy.ops.object.mode_set(mode = 'EDIT')       
    bpy.ops.mesh.delete(type='EDGE')
    bpy.ops.object.vertex_group_set_active(group = linegroup.name)
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')



    #Dissolve verts on straight lines
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT') 
    bpy.ops.mesh.dissolve_limited(angle_limit=0.001, use_dissolve_boundaries=False, delimit=set(["MATERIAL"]))
    bpy.ops.mesh.select_all(action='DESELECT') 
    bpy.ops.object.vertex_group_select()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    

    
    
    

    
    
    #STEP 4: Find end triangle constellations and save them in ID-lists
        #Remove edges in end triangle constellations
        
        
    tris = []
    del_e = []
    endpoints = []
    endpoints_v = []
    
    for vert in ob.data.vertices:
        if vert.select and not vert.hide:
        
            nbs = getNeighborVerts(ob,vert.index)
            
            if len(nbs) == 1:
                endpoints.append(vert.index)
                
                vec = mathutils.Vector(utils_MATH.vec3_fromPoints(ob.data.vertices[nbs[0]].co, vert.co))
                endpoints_v.append(vec)
     



    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT') 
    
     
    bpy.ops.object.vertex_group_set_active(group = bordergroup.name)
    bpy.ops.object.vertex_group_select()
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    
    for i in range(0,len(endpoints)):
    
        dis = 10000
        edgeID = None
    
        v = ob.data.vertices[endpoints[i]]
        v_nor = endpoints_v[i]
        
        for edge in ob.data.edges:
            
            if edge.select and not edge.hide:
                
                res = mathutils.geometry.intersect_line_line(v.co, v.co+v_nor, ob.data.vertices[edge.vertices[0]].co, ob.data.vertices[edge.vertices[1]].co)
                
                if not res == None:
                
                    if utils_MATH.insideEdgeStrict(res[0],ob.data.vertices[edge.vertices[0]].co, ob.data.vertices[edge.vertices[1]].co):
                    
                
                        tempdis = mathutils.geometry.distance_point_to_plane(res[0], v.co, v_nor)
                    
                        if tempdis < dis and tempdis > 0:
                            dis = tempdis
                            edgeID = edge.index
                        
        tri = [v.index]
        tri.append(ob.data.edges[edgeID].vertices[0])
        tri.append(ob.data.edges[edgeID].vertices[1])
        tris.append(tri)
        del_e.append(edgeID)
        
        
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type="EDGE")
    bpy.ops.object.mode_set(mode = 'OBJECT')
        
    for eID in del_e:
        ob.data.edges[eID].select = True
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='EDGE')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
        

    #STEP 5: Select border part
    
    #select one end, find tri constellation linked to it (vert at index 0 in the tri list is always a line end)
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    bpy.ops.object.vertex_group_set_active(group = bordergroup.name)
    
    border_ends = []
    
    for tri in tris:
        border_ends.append(tri[1])
        border_ends.append(tri[2])
        
        
      
    border_ends = inset_fillBorder(ob,border_ends, tris)
    
    while len(border_ends) > 0:
        border_ends = inset_fillBorder(ob,border_ends, tris)
            
    
        
    #STEP 6: Fill tris
    
    tris = inset_fillTris(ob,tris)
    
    while len(tris) > 0:
        tris = inset_fillTris(ob,tris)
        
        
    #STEP 7: Cleanup and selections
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    bpy.ops.object.vertex_group_set_active(group = linegroup.name)
    bpy.ops.object.vertex_group_select()
    
    
    
    for vgroup in ob.vertex_groups:
    
        if "$BG$" in vgroup.name:
            bpy.ops.object.vertex_group_set_active(group = vgroup.name)
            bpy.ops.object.vertex_group_remove(all=False)
    
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
        
        

    return
    
    
    
    
    
##\brief Insets selected geometry to the center (until the first verts collide).
#\returns (None)    
def inset_mergeAtCenter():

    #STEP 1: Gather data, object preparation
    
    #Hide all geometry that doesnt take part
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.hide(unselected=True)
    
    #get object reference
    ob = bpy.context.scene.objects.active
    bpy.ops.mesh.dissolve_limited(angle_limit=0.0001, use_dissolve_boundaries=False, delimit=set(["MATERIAL"]))
    bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, use_relative_offset=False, use_edge_rail=False, thickness=0.01, depth=0.0, use_outset=False, use_select_inset=False, use_individual=False, use_interpolate=False)
    
    #Save border in vertex group
    bpy.ops.mesh.select_all(action='INVERT')
    bordergroup = ob.vertex_groups.new("$BG$_BORDER")
    bpy.ops.object.vertex_group_set_active(group = bordergroup.name)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action='INVERT')

    shortest_distance = inset_findShortestDistance(ob)
    
    #Perform Inset on the rest, select insides
    #This will ensure that the inverses of the vectors we need are the only edge of the border vertices that is currently not selected
    
    bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, use_relative_offset=False, use_edge_rail=False, thickness=shortest_distance, depth=0.0, use_outset=False, use_select_inset=False, use_individual=False, use_interpolate=False)

    
    
    linegroup = ob.vertex_groups.new("$BG$_LINE")
    
    
    inset_merge(ob,linegroup)
    bpy.ops.object.vertex_group_set_active(group = linegroup.name)
    bpy.ops.object.vertex_group_select()
    bpy.ops.object.vertex_group_set_active(group = bordergroup.name)
    bpy.ops.object.vertex_group_select()
    
    bpy.ops.mesh.select_all(action='INVERT')
    
    bpy.ops.mesh.delete_edgeloop(use_face_split=True)
    
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.object.vertex_group_set_active(group = bordergroup.name)
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.select_all(action='INVERT')
    
    
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    
    
    
##\brief Finds shortest distance of an inset.
#\detail NEEDED: One small inset operation beforehand, center area selected.
#\returns (None) 
#\param ob (Object) Object the inset is performed on.
def inset_findShortestDistance(ob):

    bpy.ops.object.mode_set(mode = 'OBJECT')
    

    
    for face in ob.data.polygons:
        if face.select:
            if face.area == 0:
                return 0
    
    

    #select region's loop
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.region_to_loop()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    edges = []
    for edge in ob.data.edges:
        if edge.select and not edge.hide:
            edges.append(edge.index)
            
   
            
    #not we have a list of the border edge IDs
    #reselect region
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.loop_to_region()
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    v_indexmap = []
    v_vecs = []
    
    #we also need the inset vectors for each vert
    for vert in ob.data.vertices:
        if vert.select and not vert.hide:
            nb = getNeighborVerts(ob,vert.index)
            for n in nb:  
                testv = ob.data.vertices[n]
                if not testv.select and not testv.hide:
                    vec = mathutils.Vector(utils_MATH.vec3_fromPoints(testv.co, vert.co))
                    v_indexmap.append(vert.index)
                    v_vecs.append(vec)
                    break
        
    
        
        
            
    
    
            
            
    shortestDis = 1000000

            
    
    
    #check vert-edge collisions (excluding combinations where the vert is part of the edge)
    
    for i in range(0,len(v_indexmap)):
        
        vID = v_indexmap[i]
        
        vert = ob.data.vertices[vID]
        vert_nor = v_vecs[i]
        
        
        vIDs =  getNeighborVerts(ob, vID)
                        
        vert_1 = ob.data.vertices[vIDs[0]]
        vert_2 = ob.data.vertices[vIDs[1]]
        

        for eID in edges:
        
            #get edge coords
            
            edge = ob.data.edges[eID]
                
            if not vID in edge.vertices:
            
                v1 = ob.data.vertices[edge.vertices[0]]
                v2 = ob.data.vertices[edge.vertices[1]]
                    
                eind1 = v_indexmap.index(edge.vertices[0])
                eind2 = v_indexmap.index(edge.vertices[1])
                            
                enor1 = v_vecs[eind1]
                enor2 = v_vecs[eind2]
                    
                
                edge_nor = inset_getEdgeNormal(v1.co, v2.co, mathutils.Vector(enor1))
                    
                testdot = utils_MATH.vec3_dot(edge_nor,vert_nor)
                
                if testdot < 0:
                    
            
                    vert_p2 = vert.co+vert_nor
            
                    result = mathutils.geometry.intersect_line_line(vert.co, vert_p2 , v1.co, v2.co)
            
                    #validify result
                    if not result == None:
                    
                    
                        #hit point in front of vert?
                        
                        testdis =  mathutils.geometry.distance_point_to_plane(result[0], vert.co, vert_nor)
 
                        #further validify result
                        if testdis > 0:
                                
                            res_v = mathutils.geometry.intersect_point_line(vert.co + vert_nor, vert_1.co, vert.co)[0]
                            
                            dis= utils_MATH.distanceEuler(res_v,vert.co+vert_nor)


                            fac_v = 1/dis
                            
                            directHit = mathutils.geometry.intersect_point_line(vert.co, v1.co, v2.co)[0]
                            
                            directHit_length = utils_MATH.distanceEuler(directHit,vert.co)
 
                            hyp = utils_MATH.distanceEuler(vert.co,result[0])
                            factor = fac_v + hyp/directHit_length
                        
                            distance = hyp/factor
                            
                            
                            #Check if distance is plausible! Can the edge even reach the vert within the distance?
                            #check if the vert.co + normal*distance is on the "grown" edge (edge after inset)

                            
                            #construct grown edge
                            
                            #vert 1
                            
                            res_e1 = mathutils.geometry.intersect_point_line(v1.co + enor1, v1.co, v2.co)[0]
                            
                            dis = utils_MATH.distanceEuler(res_e1,v1.co+enor1)
                            

                            fac = 1/dis
                            
                            eg1 = mathutils.Vector(v1.co + enor1*(distance*fac))
                            
                            
                            #vert 2
                            
                            res_e2 = mathutils.geometry.intersect_point_line(v2.co + enor2, v1.co, v2.co)[0]
                            
                            dis = utils_MATH.distanceEuler(res_e2,v2.co+enor2)
                            
                            fac = 1/dis
                            
                            eg2 = mathutils.Vector(v2.co + enor2*(distance*fac))
                            
                            
                            
                            #grow first vert
                            
                            vg = mathutils.Vector(vert_nor*(distance*fac_v))
                            
                            
                            
                            #intersect
                            
                            fin_res = mathutils.geometry.intersect_line_line(vert.co, vert_nor, eg1, eg2)
                            
                            if not fin_res == None:

                                if utils_MATH.insideEdge(fin_res[0],eg1,eg2):
                            
                                
                            
                                    if distance < shortestDis:
                                    
                                        shortestDis = distance
                                                
                                                
      

    #check collapsing edges(collisions of neighbor verts)

    for eID in edges:
    
        edge = ob.data.edges[eID]
        
        v1 = ob.data.vertices[edge.vertices[0]]
        v2 = ob.data.vertices[edge.vertices[1]]
        
        ind1 = v_indexmap.index(v1.index)
        ind2 = v_indexmap.index(v2.index)
        
        v1_nor = v_vecs[ind1]
        v2_nor = v_vecs[ind2]
        
        res1 = mathutils.geometry.intersect_line_line(v1.co, v1.co + v1_nor , v2.co, v2.co + v2_nor)
        
        #if vert normals aren't parallel
        if not res1 == None:
            
            #test if collision is happening in front of both vertices
            
            col1 = mathutils.geometry.distance_point_to_plane(res1[0], v1.co, v1_nor)
            col2 = mathutils.geometry.distance_point_to_plane(res1[0], v2.co, v2_nor)
            
            if col1 > 0 and col2 > 0:
                
                #calculate distance
                
                res2 = mathutils.geometry.intersect_point_line(res1[0], v1.co, v2.co)

                basevert = res2[0]
                
                distance = utils_MATH.distanceEuler(basevert,res1[0])
                
                if distance < shortestDis:
                                    
                    shortestDis = distance
            
    
    
                        
            
     

            
    
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    
    return shortestDis
        
       

##\brief Checks for connecting edge between two vertices.
#\returns (Boolean) True if edge exists, false otherwise. 
#\param ob (Object) Object the check is performed on.
#\param vID1 (Int) Index of first vertice.
#\param vID2 (Int) Index of second vertice.
#\param edgelist ([Int]) List of edge IDs.
def conEdge(ob, vID1, vID2, edgelist):

    if vID1 == vID2:
        return True

    for eID in edgelist:
        edge = ob.data.edges[eID]
        if vID1 in edge.vertices and vID2 in edge.vertices:
            return True
    
    return False
  

##\brief Finds the neighbor verts of a vertice.
#\returns ([Int]) Indices of neighbor verts.
#\param ob (Object) Object the check is performed on.
#\param vID (Int) Index of vertice. 
def getNeighborVerts(ob,vID):
    vlist = []
    for edge in ob.data.edges:
        if not edge.hide:
            if vID == edge.vertices[0]:
                vlist.append(edge.vertices[1])
            elif vID == edge.vertices[1]:
                vlist.append(edge.vertices[0])
            
    return vlist
    
    
    
#broken
def inset_getEdgeNormal(v1co,v2co,v1nor):

    edgevec = utils_MATH.vec3_fromPointsRaw(v1co,v2co)
    angle = math.fabs(utils_MATH.getAngle(edgevec,v1nor))
    
    if angle == 90:
        return v1nor
   
    res1 = mathutils.geometry.intersect_point_line(v1co+v1nor, v1co, v2co)
    
    if res1[1] < 1 and res1[1] > 0:
        return utils_MATH.vec3_fromPoints(res1[0],v1co+v1nor)
        
        
        
    res1 = mathutils.geometry.intersect_point_line(v2co+v1nor, v1co, v2co)
    

    return utils_MATH.vec3_fromPoints(res1[0],v2co+v1nor)
        
    
        
    
    
##\brief Checks for colliding vertices and edges after an inset.
#\returns (Boolean) True if collision has been found, false otherwise.
#\param ob (Object) Object the check is performed on.
#\param linegroup (Vertex Group) Vertex group the collision check is performed on.
def inset_merge(ob,linegroup):

    bpy.ops.object.mode_set(mode = 'OBJECT')
    prevSel = ob.vertex_groups.new("$BG$_prevSel")
    bpy.ops.object.mode_set(mode = 'EDIT')

    bpy.ops.object.vertex_group_set_active(group = linegroup.name)
    bpy.ops.object.vertex_group_remove_from(use_all_groups=False, use_all_verts=False)


    bpy.ops.object.vertex_group_set_active(group = prevSel.name)
    bpy.ops.object.vertex_group_assign()
    

    res = inset_mergeVertEdge(ob)
    
    while res:
        res = inset_mergeVertEdge(ob)   
                        
                        
    #merge doubles
    bpy.ops.mesh.select_all(action='DESELECT') 
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for v1 in ob.data.vertices:
        if not v1.hide:
            for v2 in ob.data.vertices:
                if not v2.hide and not v1.index == v2.index:
                    if utils_MATH.distanceEuler(v1.co,v2.co) < 0.001:
                        v1.select = True
                        v2.select = True
        
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.object.vertex_group_set_active(group = linegroup.name)
    bpy.ops.object.vertex_group_assign()
    
    bpy.ops.mesh.select_all(action='SELECT') 
    
    bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=False)

    
    bpy.ops.mesh.select_all(action='DESELECT')  

    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT')
        
    
     
    #remove line verts from prevSel
    bpy.ops.object.vertex_group_set_active(group = prevSel.name)
    bpy.ops.object.vertex_group_select()
    
    bpy.ops.object.vertex_group_remove_from(use_all_groups=False, use_all_verts=True)
    
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.mesh.select_mode(type="VERT")
    
    bpy.ops.object.vertex_group_assign()
    
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    found = False    
    
    for vert in ob.data.vertices:
        if vert.select:
            found = True
    
    
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT') 
    bpy.ops.object.vertex_group_select()
    
    return found
    
    

##\brief Merges colliding geometry after an inset.
#\detail Helper function for the inset_skeleton() method.
#\returns (Boolean) True if collision has been found, false otherwise. 
#\param ob (Object) Object the merge is performed on.
def inset_mergeVertEdge(ob):

    bpy.ops.mesh.select_all(action='DESELECT') 


    bpy.ops.object.mode_set(mode = 'OBJECT')

    cutvert = None
    cutedge = None
    
    found = False
    
    for vert in ob.data.vertices:
        
        if found:
            break;
    
        if not vert.hide:
            for edge in ob.data.edges:
            
                if found:
                    break;
            
                if not edge.hide and not vert.index in edge.vertices:
                
                    v1 = ob.data.vertices[edge.vertices[0]]
                    v2 = ob.data.vertices[edge.vertices[1]]
                    
                    if not utils_MATH.distanceEuler(v1.co,v2.co) < 0.001:
                    
                        res = mathutils.geometry.intersect_point_line(vert.co, v1.co, v2.co)[0]
                    
                        if utils_MATH.distanceEuler(res,vert.co) < 0.001:
                        
                            if utils_MATH.insideEdgeStrict(vert.co,v1.co,v2.co):
                            
                                found = True
                                cutvert = vert
                                cutedge = edge
                                break;
                            
    
    if found:
        
        loc = list(cutvert.co)

        cutedge.select = True
        
        bpy.ops.object.mode_set(mode = 'EDIT')

        bpy.ops.mesh.subdivide(number_cuts=1, smoothness=0.0, quadtri=False, quadcorner='STRAIGHT_CUT', fractal=0.0, fractal_along_normal=0.0, seed=0)
        bpy.ops.mesh.select_less()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        for vert in ob.data.vertices:
            if vert.select:
                vert.co = loc
        
        
    
        
        
    bpy.ops.object.mode_set(mode = 'EDIT')
                        
    
    return found
                    

##\brief Checks if selected edges run along a straight line.
#\returns (Boolean) True if there's a straight line, false otherwise.
#\param ob (Object) Object the check is performed on.                   
def straightLine_sel(ob):

    vecs = []
    
    for edge in ob.data.edges:
        if edge.select:
            v1 = ob.data.vertices[edge.vertices[0]]
            v2 = ob.data.vertices[edge.vertices[1]]
            
            vec = utils_MATH.vec3_fromPoints(v1.co, v2.co)
            
            vecs.append(vec)
            
    for i in range(0,len(vecs)):
    
        res = math.fabs(utils_MATH.vec3_dot(vecs[0],vecs[i]))
        
        if res < 0.999:
            return False

            
    return True

                



##\brief Fills the space between the border and the straight skeleton.
#\detail Helper function for the inset_skeleton() method.
#\returns ([Int]) The remaining, unconnected skeleton ends, as vertice IDs.
#\param ob (Object) Object the check is performed on.      
#\param border_ends ([Int]) The ends of the skeleton.
#\param tris ([[Int,Int,Int]]) Lists of one skeleton end and two linked border vertices, as vertice IDs.                   
def inset_fillBorder(ob,border_ends, tris):

    ob.data.vertices[border_ends[0]].select = True
    
    b2 = None
    
    tri1 = None
    tri2 = None
    
    for t in tris:
        if border_ends[0] in t:
            tri1 = t
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_linked(limit=False)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    tempsel = [v.index for v in ob.data.vertices if v.select]
    
    for i in range(1,len(border_ends)):
        if not tri2 == None:
            break
        if ob.data.vertices[border_ends[i]].select:
            b2 = border_ends[i]
            for t in tris:
                if border_ends[i] in t:
                    tri2 = t
                    break
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')

    
    ob.data.vertices[tri1[0]].select = True
    ob.data.vertices[tri2[0]].select = True
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.shortest_path_select(use_length=True)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for vID in tempsel:
        ob.data.vertices[vID].select = True
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.bridge_edge_loops(type='SINGLE', use_merge=False, merge_factor=0.5, twist_offset=0, number_cuts=0, interpolation='PATH', smoothness=1.0, profile_shape_factor=0.0, profile_shape='SMOOTH')
    
    bpy.ops.object.vertex_group_remove_from(use_all_groups=False, use_all_verts=False)
    
    bpy.ops.mesh.select_all(action='DESELECT')
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    border_ends.remove(border_ends[0])
    border_ends.remove(b2)
    
    return border_ends
    
    
    
##\brief Fills the given triangles.
#\detail Helper function for the inset_skeleton() method.
#\returns ([[Int,Int,Int]]) Lists of one skeleton end and two linked border vertices, as vertice IDs.
#\param ob (Object) Object the fill is performed on.      
#\param tris ([[Int,Int,Int]]) Lists of one skeleton end and two linked border vertices, as vertice IDs.     
def inset_fillTris(ob, tris):
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for vID in tris[0]:
        ob.data.vertices[vID].select = True
        
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.edge_face_add()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    del tris[0]
    
    return tris
    
    
    
    

 
 
        
##\brief Subdivides the selected geometry.
#\returns (None)    
#\param cut (Int) Number of cuts.
#\param smooth (Float) Smoothness.
#\param subQ (Boolean) Quad/Tri Mode.
#\param qc (String in ["INNERVERT","PATH","STRAIGHT_CUT","FAN"]) Subdivide method.
def subdiv(cut,smooth,subQ,qc):
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.subdivide(number_cuts = cut, smoothness = smooth, quadtri = subQ, quadcorner = qc)
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    


##\brief Performs a boolean operation on two objects.
#\returns (None)    
#\param ob (Object) Source object.
#\param tar_ob (Object) Target object.
#\param mode (String in ["Intersect","Union","Difference"]) Boolean Mode.
def bool(ob, tar_ob, mode):

    bpy.ops.object.mode_set(mode = 'OBJECT')                
                
    boolean = ob.modifiers.new('Bool', 'BOOLEAN')
    boolean.object = tar_ob
                
    if mode == "Intersect":
        boolean.operation = 'INTERSECT'
    elif mode == "Union":
        boolean.operation = 'UNION'
    elif mode == "Difference":
        boolean.operation = 'DIFFERENCE'
    
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bool")

                        
                        
                        
                        
                        
    tar_ob.name = "_$OBS$_"
    
    
    
##\brief Splits an object into selected/unselected.
#\returns (Object) if separate objects is enabled, (None) otherwise.  
#\param ob (Object) Object the split is performed on.
#\param newOb (Boolean) Split into separate objects.    
def split(ob,newOb):

    if not newOb:
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.split()
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.object.mode_set(mode = 'OBJECT')
        return
        
    else:
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.split()
        #split object
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        splitob = utils_OBJ.copyobj_vis(ob)
        
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.delete(type="VERT")
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        bpy.context.scene.objects.active = splitob
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.delete(type="VERT")
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        
        
        
        return splitob
        
##\brief Turns a region into an NGon, if possible.
#\returns (None) 
#\param ob (Object) Object the operation is performed on.        
def ngonize(ob):

    bpy.ops.object.mode_set(mode = 'EDIT')
    
    try:
        bpy.ops.mesh.dissolve_faces(use_verts=False)
    except:
        pass
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    

##\brief Turns a region into an NGon, if possible, respects angles.
#\returns (None) 
#\param ob (Object) Object the operation is performed on.
#\param val (Float) Threshold angle.    
def ngonize_angle(ob,val):

    bpy.ops.object.mode_set(mode = 'EDIT')

    bpy.ops.mesh.hide(unselected=True)
    
    bpy.ops.mesh.region_to_loop()
    
    bpy.ops.mesh.select_all(action='INVERT')
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    

    edges = []
    
    for edge in ob.data.edges:
    
        if edge.select:
    
            count = 0
    
            adj_faces = []
    
            v1 = edge.vertices[0]
            v2 = edge.vertices[1]
        
            for face in ob.data.polygons:
                if v1 in face.vertices and v2 in face.vertices:
                    adj_faces.append(face.index)
                    count += 1
                
                if count == 2:
                    break
                
            nor1 = ob.data.polygons[adj_faces[0]].normal
            nor2 = ob.data.polygons[adj_faces[1]].normal
        
            angle = utils_MATH.getAngle(nor1,nor2)
        
            if angle <= val:
                edges.append(edge.index)
                
    bpy.ops.object.mode_set(mode = 'EDIT')            
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
                
                
                
    for eID in edges:
        ob.data.edges[eID].select = True
        
    bpy.ops.object.mode_set(mode = 'EDIT')  
    try:
        bpy.ops.mesh.dissolve_edges(use_verts=False, use_face_split=False)
    except:
        pass
        
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    
##\brief Solidifies the selected geometry.
#\returns (None) 
#\param ob (Object) Object the solidify operation is performed on.   
#\param amount (Float) Solidify thickness.
def solidify(ob,amount):

    bpy.ops.object.mode_set(mode = 'EDIT')
    
    try:
        bpy.ops.mesh.solidify(thickness=amount)
    except:
        pass
    
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    
    
##\brief Bisects an object.
#\returns (None) 
#\param ob (Object) Object the operation is performed on. 
#\param pos (mathutils.Vector) Cut plane anchor point.
#\param nor (mathutils.Vector) Cut plane normal.
#\param fill (Boolean) If true, fill the cut.
#\param inner (Boolean) If true, delete geometry behind the cut plane.
#\param outer (Boolean) If true, delete geometry in front of the cut plane.    
def bisect(ob,pos,nor,fill,inner,outer):

    bpy.ops.object.mode_set(mode = 'EDIT')
    
    try:
        bpy.ops.mesh.bisect(plane_co=mathutils.Vector(pos), plane_no=mathutils.Vector(nor), use_fill=fill, clear_inner=inner, clear_outer=outer, threshold=0.0001)
    except:
        pass
    
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
 

##\brief Turns selected edges into a diamong-shaped wireframe.
#\returns (None) 
#\param ob (Object) Object the wireframe operation is performed on.   
#\param th (Float) Wireframe thickness. 
def wireframe_diamond(ob,th):
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    try:
        bpy.ops.mesh.wireframe(use_boundary=True, use_even_offset=True, use_relative_offset=False, use_replace=True, thickness=th, offset=0, use_crease=False, crease_weight=0)
    except:
        pass   
         

    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
##\brief Turns selected edges into a square-shaped wireframe.
#\returns (None) 
#\param ob (Object) Object the wireframe operation is performed on.   
#\param th (Float) Wireframe thickness.     
def wireframe_square(ob,th):
    
    
    
    try:
    
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, use_relative_offset=False, use_edge_rail=False, thickness=0.001, depth=0.0, use_outset=False, use_select_inset=False, use_individual=False, use_interpolate=False)
        bpy.ops.mesh.bevel(offset_type='OFFSET', offset=th, segments=1, profile=1, vertex_only=False, clamp_overlap=False, material=-1)
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.delete(type="FACE")

        solidify = ob.modifiers.new('Sol', 'SOLIDIFY')
        
        solidify.offset = 0
        solidify.thickness = th*2
        solidify.use_even_offset = True
        solidify.use_quality_normals = True
        solidify.use_rim = True
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Sol")
        
 
        
    except:
        pass   
         

    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
##\brief Performs a 2D boolean operation on two objects.
#\returns (None) 
#\param ob (Object) Source object. 
#\param ob2 (Object) Target object.   
#\param mode (String in ["INTERSECT","UNION","DIFFERENCE"]) Boolean mode to use.
#\param planeMode (String in ["N","X","Y","Z","V"]) Projection axis.
#\param v (mathutils.Vector) Vector to project along(optional). Cannot be (None) if planeMode is "V". 
def bool_2D(ob,ob2,mode,planeMode,v = None):

    vector = None
    point = None

    #flatten the faces of both objects to one plane
    
    if planeMode == "N":
    
        list = flatten_alongNormal(ob)
    
        flatten_alongVectorToPoint(ob2,list[0],list[1])
        
        vector = list[1]
        point = list[0]
        
    elif planeMode == "X":
    
        vec = mathutils.Vector([1,0,0])
    
        list = flatten_alongVector(ob,vec)
    
        flatten_alongVectorToPoint(ob2,list[0],vec)
        
        vector = vec
        point = list[0]
        
    elif planeMode == "Y":
    
        vec = mathutils.Vector([0,1,0])
    
        list = flatten_alongVector(ob,vec)
    
        flatten_alongVectorToPoint(ob2,list[0],vec)
        
        vector = vec
        point = list[0]
        
    elif planeMode == "Z":
    
        vec = mathutils.Vector([0,0,1])
    
        list = flatten_alongVector(ob,vec)
    
        flatten_alongVectorToPoint(ob2,list[0],vec)
        
        vector = vec
        point = list[0]
        
    elif planeMode == "V" and not v == None:
    
        list = flatten_alongVector(ob,v)
    
        flatten_alongVectorToPoint(ob2,list[0],v)
        
        vector = v
        point = list[0]
        
        
    #extrude along vector
    
    vector = mathutils.Vector(utils_MATH.vec3_normalize(vector))
    
    bpy.context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = "SELECT")
    bpy.ops.mesh.extrude_region(mirror=False)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for vert in ob.data.vertices:
        if vert.select:
            vert.co = vert.co + vector
            
            
            
    bpy.context.scene.objects.active = ob2
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = "SELECT")
    bpy.ops.mesh.extrude_region(mirror=False)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for vert in ob2.data.vertices:
        if vert.select:
            vert.co = vert.co + vector
            
            
            
    #regular boolean
            
            
    bpy.context.scene.objects.active = ob
    
    boolean = ob.modifiers.new('Bool', 'BOOLEAN')
    
    boolean.object = ob2
    boolean.operation = mode
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bool")
    

    #cut away excess geometry
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = "DESELECT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    for vert in ob.data.vertices:
        if not math.fabs(mathutils.geometry.distance_point_to_plane(vert.co, point, vector)) < 0.0001:
            vert.select = True
            
            
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.mesh.select_all(action = "SELECT")
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
##\brief Replaces a polygon with a tile anchored to its center.
#\returns (None) 
#\param ob (Object) Source object. 
#\param tiles ([Object]) Tiles to choose from.
#\param ind (Int) Index of the chosen tile (-1 for random).
#\param norMode (String in ["N","V"]) Normal mode, either the polygon's normal ("N") or a vector ("V").
#\param axis (String in ["N","X","Y","Z","V"]) Dominant axis.
#\param fallback (String in ["N","X","Y","Z","V"]) Fallback axis.
#\param offset (mathutils.Vector) Tile offset.
#\param vec (mathutils.Vector) if norMode is "V", (None) otherwise.
#\param cutTile (Boolean) Whether to cut the tile to the polygon's bounds.
#\param cutNors (Boolean) Respect polygon normals when cutting.
def replace_poly_c(ob,tiles,ind,norMode,axis,fallback,offset,vec,cutTile,cutNors):

    if axis in ["X","-X"]:
        
        if axis == "X":
            checkVec = mathutils.Vector([1,0,0])
        else:
            checkVec = mathutils.Vector([-1,0,0])
        
        if norMode == "X":
            return
        if fallback in ["X","-X"]:
            return
            
    elif axis in ["Y","-Y"]:
    
        if axis == "Y":
            checkVec = mathutils.Vector([0,1,0])
        else:
            checkVec = mathutils.Vector([0,-1,0])
    
        if norMode == "Y":
            return
        if fallback in ["Y","-Y"]:
            return
            
    elif axis in ["Z","-Z"]:
    
        if axis == "Z":
            checkVec = mathutils.Vector([0,0,1])
        else:
            checkVec = mathutils.Vector([0,0,-1])
    
        if norMode == "Z":
            return
        if fallback in ["Z","-Z"]:
            return
            
    
            
            
            
            

    obs = [ob]

    if norMode == "N":
    
        if ind == -1:
    
            for face in ob.data.polygons:
                if face.select and not face.hide:
                    ind = random.randrange(0,len(tiles))
                    ob2 = utils_OBJ.copyobj_vis(tiles[ind])
                    offset_dom(ob2,offset)
                    
                    if face.normal == checkVec:
                        tileToX(ob2,face.normal,fallback,face.center)
                    else:
                        tileToX(ob2,face.normal,axis,face.center)
                        
                    if cutTile:
                        poly_c_cut(ob,face,ob2,cutNors)
                            
                    obs.append(ob2)
                    
        else:
            
            for face in ob.data.polygons:
                if face.select and not face.hide:
                    ob2 = utils_OBJ.copyobj_vis(tiles[ind])
                    offset_dom(ob2,offset)
                    
                    if face.normal == checkVec:
                        tileToX(ob2,face.normal,fallback,face.center)
                    else:
                        tileToX(ob2,face.normal,axis,face.center)
                        
                    if cutTile:
                        poly_c_cut(ob,face,ob2,cutNors)

                    obs.append(ob2)
                    
                    
    elif norMode == "V" and not vec == None:
    
        if vec == checkVec:
            axis = fallback
    
        if ind == -1:
    
            for face in ob.data.polygons:
                if face.select and not face.hide:
                    ind = random.randrange(0,len(tiles))
                    ob2 = utils_OBJ.copyobj_vis(tiles[ind])
                    offset_dom(ob2,offset)
                    tileToX(ob2,vec,axis,face.center) 
                    if cutTile:
                        poly_c_cut(ob,face,ob2,cutNors)
                    obs.append(ob2)
                    
        else:
            
            for face in ob.data.polygons:
                if face.select and not face.hide:
                    ob2 = utils_OBJ.copyobj_vis(tiles[ind])
                    offset_dom(ob2,offset)
                    tileToX(ob2,vec,axis,face.center) 
                    if cutTile:
                        poly_c_cut(ob,face,ob2,cutNors)
                    obs.append(ob2)
              
                
    if len(obs) > 1:
        scene = bpy.context.scene
        ctx = bpy.context.copy()
        
        bpy.context.scene.objects.active = ob
        
        ctx['active_object'] = obs[0]
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = "SELECT")
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        ctx['selected_objects'] = obs
        
        ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]

        bpy.ops.object.join(ctx)
                
            

            
            
            
            
##\brief Cuts an object to a polygon's boundary edges.
#\detail Intended to be used in functions like replace_poly_c(), not standalone.
#\returns (None) 
#\param ob (Object) Source object.
#\param face (Polygon) The polygon the bounds are taken from. 
#\param tile (Object) Tile to be cut.
#\param nors (Boolean) Respect normals when cutting(optional, default = False).       
def poly_c_cut(ob,face,tile,nors = False):
    
    bpy.context.scene.objects.active = tile

    bpy.ops.object.mode_set(mode = 'EDIT')
    

    up = face.normal
    center = face.center
    
    
    edgemap = []
    
    for edge in ob.data.edges:
        v0 = edge.vertices[0]
        v1 = edge.vertices[1]
        
        if v0 in face.vertices and v1 in face.vertices:
            
            edgemap.append([v0,v1])
            
            
    if not nors:
        for edge in edgemap:
        
            bpy.ops.mesh.select_all(action = "SELECT")
            
            vector = ob.data.vertices[edge[1]].co - ob.data.vertices[edge[0]].co
            
            normal = vector.cross(up)
            
            if normal.dot(-ob.data.vertices[edge[0]].co) < 0:
                normal.negate()
            
            bpy.ops.mesh.bisect(plane_co=ob.data.vertices[edge[0]].co, plane_no=normal, use_fill=False, clear_inner=True, clear_outer=False, threshold=0.001)
            
    else:
        for edge in edgemap:
        
            bpy.ops.mesh.select_all(action = "SELECT")
            
            vector = ob.data.vertices[edge[1]].co - ob.data.vertices[edge[0]].co
            nor = utils_MATH.getMidCoords([ob.data.vertices[edge[1]].normal,ob.data.vertices[edge[0]].normal])
            
            normal = vector.cross(nor)
            
            if normal.dot(-ob.data.vertices[edge[0]].co) < 0:
                normal.negate()
            
            bpy.ops.mesh.bisect(plane_co=ob.data.vertices[edge[0]].co, plane_no=normal, use_fill=False, clear_inner=True, clear_outer=False, threshold=0.001)
            
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
            
            
            
            
            
            
            
            
            
            
            
            


##\brief Replaces a polygon with a tile.
#\returns (None) 
#\param ob (Object) Source object. 
#\param tiles ([Object]) Tiles to choose from.
#\param ind (Int) Index of the chosen tile (-1 for random).
#\param dominant (String in ["N","X","Y","Z","V"]) Dominant axis.
#\param fallback (String in ["N","X","Y","Z","V"]) Fallback axis.
#\param dom_size (Float) Factor by which to multiply the tile's length (dominant axis).
#\param subdom_size (Float) Factor by which to multiply the tile's length (subdominant axis).
#\param dom_random (Boolean) If true, will take random tiles along the dominant axis.
#\param subdom_random (Boolean) If true, will take random tiles along the subdominant axis.
#\param quad_morph (String in ["ds","d","s","x"]) Morph type in case the polygon is a quad. "x" in case of no morphing, "ds" for morph all, "s" and "d" for only morph one axis.
#\param tri_morph (String in ["m","p","x"]) Morph type in case the polygon is a triangle. "m" for quad morphing, "p" for pinching, "x" for no morphing.
#\param quad_cut (String in ["ds","d","s","x"]) Cut type in case the polygon is a quad. "x" in case of no cutting, "ds" for cut all, "s" and "d" for only cut along one axis.
#\param tri_cut (String in ["ds","d","s","x"]) Cut type in case the polygon is a triangle. "x" in case of no cutting, "ds" for cut all, "s" and "d" for only cut along one axis.
#\param ngon_cut (String in ["c","x"]) Cut type in case the polygon is an ngon. "c" for cut all, "x" for no cuts.
#\param bounds_align (Boolean) Respect polygon normals when cutting and morphing.
#\param offset (mathutils.Vector) Tile offset.
#\param dom_tiling (String in ["s","t"]) Tiling mode along the dominant axis. "s" for stretching, "t" for arraying.
#\param subdom_tiling (String in ["s","t"]) Tiling mode along the subdominant axis. "s" for stretching, "t" for arraying.
#\param dom_align (String in ["b","c","t"]) Where to anchor the tiles (bottom, center, top) on the dominant axis. Has no effect if dom_tiling is "s".
#\param subdom_align (String in ["b","c","t"]) Where to anchor the tiles (bottom, center, top) on the subdominant. Has no effect if dom_tiling is "s".
def replace_poly(ob, tiles, ind, dominant, fallback, dom_size, subdom_size, dom_random, subdom_random, quad_morph,tri_morph,quad_cut,tri_cut,ngon_cut, bounds_align, offset, dom_tiling, subdom_tiling, dom_align, subdom_align):
    
    

    if dominant in ["X","-X"]:
        
        if dominant == "X":
            checkVec = mathutils.Vector([1,0,0])
        else:
            checkVec = mathutils.Vector([-1,0,0])

        if fallback in ["X","-X"]:
            return
            
    elif dominant in ["Y","-Y"]:
    
        if dominant == "Y":
            checkVec = mathutils.Vector([0,1,0])
        else:
            checkVec = mathutils.Vector([0,-1,0])

        if fallback in ["Y","-Y"]:
            return
            
    elif dominant in ["Z","-Z"]:
    
        if dominant == "Z":
            checkVec = mathutils.Vector([0,0,1])
        else:
            checkVec = mathutils.Vector([0,0,-1])

        if fallback in ["Z","-Z"]:
            return
            
    
    obs = [ob]
            
            
    if ind == -1:

    
        for face in ob.data.polygons:
            if face.select and not face.hide:


            
                #separate tile and tile cage
                
                ind = random.randrange(0,len(tiles))
                
                t = utils_OBJ.copyobj_vis(tiles[ind])
                
                t_list = tile_separate(t)

            
                tile = t_list[0]
                cage = t_list[1]
            
                #rotate poly to match standard tile orientation
                
                c_list = getMappedCoords(ob,face.index)
                
                coords = c_list[0]
                edgemap = c_list[1]
                nors = c_list[2]
                    
                
                poly = xToTile(coords,face.center,face.normal,dominant)
                
                rotationMatrix = poly[1]
                nors = poly[2]
                poly = poly[0]
                    
                    
                rotmat2 = mathutils.Matrix.Rotation(math.radians(180), 4, 'Z').to_3x3()  
                    
                    
                p2 = []
                for co in poly:
                    p2.append(co * rotmat2)
                poly = p2
                
                
                #Polygon is now rotated to match the tile's initial rotation, plus adjustment.
                #We can now build the cage and deform the tile.

                #morph/array cages, apply
                
                if len(face.vertices) == 4:
                    
                    if not quad_morph == "x":
                        polybox = fillTile(poly, tile, cage, dom_random, subdom_random, tiles, dom_size, subdom_size, "s", "s", dom_align, subdom_align)
                        if bounds_align:
                            morphTile_quad(tile,poly,polybox,edgemap,quad_morph,nors)
                        else:
                            morphTile_quad(tile,poly,polybox,edgemap,quad_morph)
                        domEdges = findDomEdges_quad(poly,edgemap)
                        
                    else:
                        polybox = fillTile(poly, tile, cage, dom_random, subdom_random, tiles, dom_size, subdom_size, dom_tiling, subdom_tiling, dom_align, subdom_align)
                        domEdges = findDomEdges_quad(poly,edgemap)
                        
                    if not quad_morph == "ds":
                    
                        if quad_cut == "ds":
                            cutTile(tile,poly,edgemap)
                        elif quad_cut == "d":
                            cutTile_dom(tile,poly,domEdges)
                        elif quad_cut == "s":
                            cutTile_subdom(tile,poly,edgemap,domEdges)
                        
                
                elif len(face.vertices) == 3:
                    
                    if not tri_morph == "x":
                        polybox = fillTile(poly, tile, cage, dom_random, subdom_random, tiles, dom_size, subdom_size, "s", "s", dom_align, subdom_align)
                        domEdges = findDomEdges_tri(poly,edgemap)
                        if bounds_align:
                            morphTile_tri(tile,poly,polybox,edgemap,tri_morph,nors)
                        else:
                            morphTile_tri(tile,poly,polybox,edgemap,tri_morph)
                        
                        if bounds_align:
                            if tri_cut == "ds":
                                cutTile(tile,poly,edgemap,nors_cut)
                            elif tri_cut == "d":
                                cutTile_dom(tile,poly,domEdges,nors_cut)
                            elif tri_cut == "s":
                                cutTile_subdom(tile,poly,edgemap,domEdges,nors_cut)
                            
                            
                        else:
                            if tri_cut == "ds":
                                cutTile(tile,poly,edgemap)
                            elif tri_cut == "d":
                                cutTile_dom(tile,poly,domEdges)
                            elif tri_cut == "s":
                                cutTile_subdom(tile,poly,edgemap,domEdges)

                    else:
                        polybox = fillTile(poly, tile, cage, dom_random, subdom_random, tiles, dom_size, subdom_size, dom_tiling, subdom_tiling, dom_align, subdom_align)
                        domEdges = findDomEdges_tri(poly,edgemap)
                        
                        if tri_cut == "ds":
                            cutTile(tile,poly,edgemap)
                        elif tri_cut == "d":
                            cutTile_dom(tile,poly,domEdges)
                        elif tri_cut == "s":
                            cutTile_subdom(tile,poly,edgemap,domEdges)
                    

                    
                    
                
                
                else:
                    polybox = fillTile(poly, tile, cage, dom_random, subdom_random, tiles, dom_size, subdom_size, dom_tiling, subdom_tiling, dom_align, subdom_align)
                    if ngon_cut == "c":
                        cutTile(tile,poly,edgemap)
                    
                
                offsetTile(tile,offset)

                #clean up

                obs.append(tile)
                
                #move morphed tile back to face location/rotation
                
                tileToX_rotmat(tile,rotationMatrix,face.center)
                
    
    else:
        
        copytile = tiles[ind]
        
        for face in ob.data.polygons:
            if face.select and not face.hide:
            
                #separate tile and tile cage
                
                t = utils_OBJ.copyobj_vis(copytile)
                
                t_list = tile_separate(t)

            
                tile = t_list[0]
                cage = t_list[1]
            
                #rotate poly to match standard tile orientation
                
                c_list = getMappedCoords(ob,face.index)
                
                coords = c_list[0]
                edgemap = c_list[1]
                nors = c_list[2]
                    
                
                poly = xToTile(coords,face.center,face.normal,dominant,nors)
                
                rotationMatrix = poly[1]
                nors = poly[2]
                poly = poly[0]
                    
                    
                rotmat2 = mathutils.Matrix.Rotation(math.radians(180), 4, 'Z').to_3x3()  
                    
                    
                p2 = []
                n2 = []
                for i in range(0,len(poly)):
                    p2.append(poly[i] * rotmat2)
                    n2.append(nors[i] * rotmat2)
                    
                poly = p2
                nors = n2
                
                nors_cut = []
                for n in nors:
                    nors_cut.append(n.copy())
                
                
                #Polygon is now rotated to match the tile's initial rotation, plus adjustment.
                #We can now build the cage and deform the tile.

                #morph/array cages, apply
                
                
                
                if len(face.vertices) == 4:
                    
                    if not quad_morph == "x":
                        polybox = fillTile(poly, tile, cage, dom_random, subdom_random, tiles, dom_size, subdom_size, "s", "s", dom_align, subdom_align)
                        if bounds_align:
                            morphTile_quad(tile,poly,polybox,edgemap,quad_morph,nors)
                        else:
                            morphTile_quad(tile,poly,polybox,edgemap,quad_morph)
                        domEdges = findDomEdges_quad(poly,edgemap)
                        
                    else:
                        polybox = fillTile(poly, tile, cage, dom_random, subdom_random, tiles, dom_size, subdom_size, dom_tiling, subdom_tiling, dom_align, subdom_align)
                        domEdges = findDomEdges_quad(poly,edgemap)
                        
                    if not quad_morph == "ds":
                    
                        if quad_cut == "ds":
                            cutTile(tile,poly,edgemap)
                        elif quad_cut == "d":
                            cutTile_dom(tile,poly,domEdges)
                        elif quad_cut == "s":
                            cutTile_subdom(tile,poly,edgemap,domEdges)
                        
                
                elif len(face.vertices) == 3:
                    
                    if not tri_morph == "x":
                        polybox = fillTile(poly, tile, cage, dom_random, subdom_random, tiles, dom_size, subdom_size, "s", "s", dom_align, subdom_align)
                        domEdges = findDomEdges_tri(poly,edgemap)
                        if bounds_align:
                            morphTile_tri(tile,poly,polybox,edgemap,tri_morph,nors)
                        else:
                            morphTile_tri(tile,poly,polybox,edgemap,tri_morph)
                        
                        print(tri_cut)
                        
                        if bounds_align:
                            if tri_cut == "ds":
                                cutTile(tile,poly,edgemap,nors_cut)
                            elif tri_cut == "d":
                                cutTile_dom(tile,poly,domEdges,nors_cut)
                            elif tri_cut == "s":
                                cutTile_subdom(tile,poly,edgemap,domEdges,nors_cut)
                            
                            
                        else:
                            if tri_cut == "ds":
                                cutTile(tile,poly,edgemap)
                            elif tri_cut == "d":
                                cutTile_dom(tile,poly,domEdges)
                            elif tri_cut == "s":
                                cutTile_subdom(tile,poly,edgemap,domEdges)

                    else:
                        polybox = fillTile(poly, tile, cage, dom_random, subdom_random, tiles, dom_size, subdom_size, dom_tiling, subdom_tiling, dom_align, subdom_align)
                        domEdges = findDomEdges_tri(poly,edgemap)
                        
                        if tri_cut == "ds":
                            cutTile(tile,poly,edgemap)
                        elif tri_cut == "d":
                            cutTile_dom(tile,poly,domEdges)
                        elif tri_cut == "s":
                            cutTile_subdom(tile,poly,edgemap,domEdges)
                    

                    
                    
                
                
                else:
                    polybox = fillTile(poly, tile, cage, dom_random, subdom_random, tiles, dom_size, subdom_size, dom_tiling, subdom_tiling, dom_align, subdom_align)
                    if ngon_cut == "c":
                        cutTile(tile,poly,edgemap)

                    
                
                offsetTile(tile,offset)

                #clean up

                obs.append(tile)
                
                #move morphed tile back to face location/rotation
                
                tileToX_rotmat(tile,rotationMatrix,face.center)

    
                
                
                
                
    
    utils_OBJ.empty(obs[0])
    utils_OBJ.join(obs)
                
              
                
                
##\brief Aligns a polygon's coordinates to the tile-conform axes.
#\returns ([[mathutils.Vector],mathutils.Matrix]) The rotated coordinates and the rotation matrix.
#\param verts ([mathutils.Vector]) The polygon's vertices coordinates.
#\param edgemap ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge.
def adjustToTile(verts,edgemap):

    coords = verts
    
    retco = []

    x = mathutils.Vector([1,0,0])
    y = mathutils.Vector([0,1,0])
    check = mathutils.Vector([0,0,1])
    
    angle = math.radians(90)
    angle_abs = angle
    vec = None
    

    for edge in edgemap:
    
        co1 = coords[edge[0]]
        co2 = coords[edge[1]]

        vector = coords[edge[0]] - coords[edge[1]]
        
        ang1 = -utils_MATH.getAngleNor(vector,x,check)
        ang2 = -utils_MATH.getAngleNor(vector,y,check)
            

        
        if math.fabs(ang1) < angle_abs:
            angle = ang1
            angle_abs = math.fabs(ang1)
            vec = vector
            
        if math.fabs(ang2) < angle_abs:
            angle = ang2
            angle_abs = math.fabs(ang2)
            vec = vector
     
    rotmat = mathutils.Matrix.Rotation(angle, 4, 'Z').to_3x3()
    
    for co in coords:
        retco.append(co * rotmat)
        
 
    return [retco,rotmat]
    

##\brief Rotates a tile back to the original polygon's aligns (reverts adjustToTile()'s effect).
#\returns (None)
#\param tile (Object) The tile to be rotated.
#\param rotmat (mathutils.Matrix) The rotation matrix from adjustToTile().
def adjustTile(tile,rotmat):
    
    rotmat.invert()
    
    
    
    for vert in tile.data.vertices:
        vert.co = vert.co * rotmat
    
            
    
    
    
                
                
                
                
##\brief Gets a 2D bounding box (X and Y) of a polygon.
#\returns ([mathutils.Vector,mathutils.Vector,mathutils.Vector,mathutils.Vector]) minX, maxX, minY and maxY of the box.
#\param coords ([mathutils.Vector]) The coordinates to form a box around.             
def getPolyBox(coords):

    
    x = []
    y = []
    
    for co in coords:
        x.append(co[0])
        y.append(co[1])
        

        
    minX = min(x)
    maxX = max(x)
    minY = min(y)
    maxY = max(y)
    
    
    return [minX,maxX,minY,maxY]
    



##\brief Fills a polygon's 2D bounding box with tiles.
#\returns ([mathutils.Vector,mathutils.Vector,mathutils.Vector,mathutils.Vector]) minX, maxX, minY and maxY of the polygon's box.
#\param poly (Polygon) The polygon to be filled. 
#\param tile (Object) The first tile (must get chosen beforehand).
#\param cage ([mathutils.Vector]) The polygon's cage's coordinates.
#\param domRandom (Boolean) If true, will take random tiles along the dominant axis.
#\param subdomRandom (Boolean) If true, will take random tiles along the subdominant axis.
#\param tiles ([Object]) Tiles to choose from in case randomized is set.
#\param domSize (Float) Factor by which to multiply the tile's length (dominant axis).
#\param subdomSize (Float) Factor by which to multiply the tile's length (subdominant axis).
#\param domTiling (String in ["s","t"]) Tiling mode along the dominant axis. "s" for stretching, "t" for arraying.
#\param subdomTiling (String in ["s","t"]) Tiling mode along the subdominant axis. "s" for stretching, "t" for arraying.
#\param domAlign (String in ["b","c","t"]) Where to anchor the tiles (bottom, center, top) on the dominant axis. Has no effect if dom_tiling is "s".
#\param subdomAlign (String in ["b","c","t"]) Where to anchor the tiles (bottom, center, top) on the subdominant. Has no effect if dom_tiling is "s".    
def fillTile(poly, tile, cage, domRandom, subdomRandom, tiles, domSize, subdomSize, domTiling, subdomTiling, domAlign, subdomAlign):
    
    p_ex = getPolyBox(poly)
    c_ex = getPolyBox(cage)
    
    
    retCAGE = c_ex[:]
    
    
    bottom = p_ex[2]
    top = p_ex[3]
    left = p_ex[0]
    right = p_ex[1]
    
    c_bottom = c_ex[2]
    c_top = c_ex[3]
    c_left = c_ex[0]
    c_right = c_ex[1]
    
    
    pDomLen = top-bottom
    domLen = c_top-c_bottom
    
    pSubdomLen = right-left
    subdomLen = c_right-c_left

    
    domOff = mathutils.Vector([0,domLen,0])
    subdomOff = mathutils.Vector([subdomLen,0,0])
    
    
    
    #add more tiles
    #assuming all tiles have the same cage
     
     
    if domTiling == "s":

        rep = max(int(domSize),1)
        
        joins = [tile]
        
        if not domRandom:
            for i in range(1,rep):
                tile2 = utils_OBJ.copyobj_vis(tile)
                tile2.location += domOff*i
                joins.append(tile2)
        
        else:
            for i in range(1,rep):
                ind = random.randrange(0,len(tiles))
                tile2 = utils_OBJ.copyobj_vis(tiles[ind])
                tile2 = tile_separate(tile2)[0]
                tile2.location += domOff*i
                joins.append(tile2)
            
        utils_OBJ.join(joins)
            
         
        factor = pDomLen/((rep)*domLen)

            
        domOffset = bottom - c_bottom * factor
            
        for vert in tile.data.vertices:
            vert.co[1] = (vert.co[1] * factor) + domOffset
                
    elif domTiling == "t":
    
        joins = [tile]
        
        maxSize = pDomLen
        curSize = domLen
        
        if not domRandom:
        
            while not curSize >= maxSize*(1/domSize):
                tile2 = utils_OBJ.copyobj_vis(tile)
                tile2.location[1] += curSize
                curSize += domLen
                joins.append(tile2)
                
        else:
        
            while not curSize >= maxSize*(1/domSize):
                ind = random.randrange(0,len(tiles))
                tile2 = utils_OBJ.copyobj_vis(tiles[ind])
                tile_sep = tile_separate(tile2)
                tile2 = tile_sep[0]
                tile2.location[1] += curSize
                
                ex = getPolyBox(tile_sep[1])
                curSize += ex[3] - ex[2]
                joins.append(tile2)
                
        utils_OBJ.join(joins)
        
        
        if domAlign == "b":      
            domOffset = bottom - c_bottom * domSize
            
        elif domAlign == "c":
            domOffset = -((curSize-domLen)*domSize)/2
            
        elif domAlign == "t":
            domOffset = (top - c_top*domSize) - (curSize - domLen)*domSize
            
            
            
        for vert in tile.data.vertices:
            vert.co[1] = (vert.co[1] * domSize) + domOffset

                
            
        

    if subdomTiling == "s":
        if subdomSize >= 1:
            rep = int(subdomSize)
        
            joins = [tile]
        
            if not subdomRandom:
                for i in range(1,rep):
                    tile2 = utils_OBJ.copyobj_vis(tile)
                    tile2.location += subdomOff*i
                    joins.append(tile2)
        
            else:
                for i in range(1,rep):
                    ind = random.randrange(0,len(tiles))
                    tile2 = utils_OBJ.copyobj_vis(tiles[ind])
                    tile2 = tile_separate(tile2)[0]
                    tile2.location += subdomOff*i
                    joins.append(tile2)
                    
            utils_OBJ.join(joins) 

            factor = pSubdomLen/((rep)*subdomLen)
            
            subdomOffset = left - c_left * factor
            
            for vert in tile.data.vertices:
                vert.co[0] = (vert.co[0] * factor) + subdomOffset
                
    elif subdomTiling == "t":
        joins = [tile]
        
        maxSize = pSubdomLen*(1/subdomSize)
        curSize = subdomLen
        
        if not subdomRandom:
        
            while not curSize >= maxSize:
                tile2 = utils_OBJ.copyobj_vis(tile)
                tile2.location[0] += curSize
                curSize += subdomLen
                joins.append(tile2)
                
        else:
        
            while not curSize >= maxSize:
                ind = random.randrange(0,len(tiles))
                tile2 = utils_OBJ.copyobj_vis(tiles[ind])
                tile_sep = tile_separate(tile2)
                tile2 = tile_sep[0]
                tile2.location[0] += curSize
                
                ex = getPolyBox(tile_sep[1])
                curSize += ex[3] - ex[2]
                joins.append(tile2)
                
        utils_OBJ.join(joins)
        

        
        if subdomAlign == "b":       
            subdomOffset = left - c_left * subdomSize
            
        elif subdomAlign == "c":
            subdomOffset = -((curSize-subdomLen)*subdomSize)/2
            
        elif subdomAlign == "t":
            subdomOffset = (right - c_right*subdomSize) - (curSize - subdomLen)*subdomSize

            
        for vert in tile.data.vertices:
            vert.co[0] = (vert.co[0] * subdomSize) + subdomOffset
            
            
            
            
    return p_ex
        
    
    



    
##\brief Offsets a tile.
#\returns (None)
#\param tile (Object) The tile to be moved.   
#\param offset (mathutils.Vector) The offset.         
def offsetTile(tile,offset):
    
    for vert in tile.data.vertices:
        vert.co += offset


        
        
##\brief Separates a tile's cage and the "real" tile.
#\returns ([Object,[mathutils.Vector,mathutils.Vector,mathutils.Vector,mathutils.Vector]]) The tile and its cage (as coordinates).
#\param tile (Object) The tile to be prepared.   
def tile_separate(tile):

    bpy.context.scene.objects.active = tile
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action = "DESELECT")
    bpy.ops.object.mode_set(mode = 'OBJECT')

    cage_ids = []
    tile_ids = []
    cage = []
    
    passCage = False
    
    try:
        index = tile.vertex_groups["cage"].index
    except:
        passCage = True
    
    if not passCage:
        for vert in tile.data.vertices:
            if index in [v.group for v in vert.groups]:
                cage_ids.append(vert.index)

    if len(cage_ids) == 4:
        for vID in cage_ids:
            tile.data.vertices[vID].select = True
            cage.append(tile.data.vertices[vID].co.copy())
    else:
        cage = findCage_poly(tile)
        
        
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    return [tile,cage]
    
    

    
##\brief Finds a cage for a given tile.
#\detail Called in case a user-made tile has no cage.
#\returns ([mathutils.Vector,mathutils.Vector,mathutils.Vector,mathutils.Vector]) The cage (as coordinates).
#\param tile (Object) The tile to be used as the cage's source.
def findCage_poly(tile):

    min_dom = 1000000
    max_dom = -1000000
    
    min_subdom = 1000000
    max_subdom = -1000000
    
    for vert in tile.data.vertices:
        
        coords = vert.co
        
        if coords[1] > max_dom:
            max_dom = coords[1]
            
        if coords[1] < min_dom:
            min_dom = coords[1]
            
            
        if coords[0] > max_subdom:
            max_subdom = coords[0]
            
        if coords[0] < min_subdom:
            min_subdom = coords[0]
            
    v1 = mathutils.Vector([min_subdom,max_dom,0])
    v2 = mathutils.Vector([max_subdom,max_dom,0])
    v3 = mathutils.Vector([max_subdom,min_dom,0])
    v4 = mathutils.Vector([min_subdom,min_dom,0])
            
    return [v1,v2,v3,v4]
    
    
    
    
    

            
##\brief Cuts a tile to a polygon's boundary edges.
#\detail Intended to be used in functions like replace_poly(), not standalone.
#\returns (None) 
#\param tile (Object) Tile to be cut.
#\param poly (Polygon) The polygon the bounds are taken from. 
#\param edgemap ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge.
#\param nors (Boolean) Respect normals when cutting(optional, default = False).             
def cutTile(tile,poly,edgemap,nors = None):


    bpy.context.scene.objects.active = tile

    bpy.ops.object.mode_set(mode = 'EDIT')
    

    up = mathutils.Vector([0,0,1])
    center = mathutils.Vector([0,0,0])
    
    
    if nors == None:
        for edge in edgemap:
        
            bpy.ops.mesh.select_all(action = "SELECT")
            
            vector = poly[edge[1]] - poly[edge[0]]
            
            normal = vector.cross(up)
            
            if normal.dot(-poly[edge[0]]) < 0:
                normal.negate()
            
            bpy.ops.mesh.bisect(plane_co=poly[edge[0]], plane_no=normal, use_fill=False, clear_inner=True, clear_outer=False, threshold=0.001)
            
    else:
        for edge in edgemap:
        
            bpy.ops.mesh.select_all(action = "SELECT")
            
            vector = poly[edge[1]] - poly[edge[0]]
            nor = utils_MATH.getMidCoords([nors[edge[1]],nors[edge[0]]])
            
            normal = vector.cross(nor)
            
            if normal.dot(-poly[edge[0]]) < 0:
                normal.negate()
            
            bpy.ops.mesh.bisect(plane_co=poly[edge[0]], plane_no=normal, use_fill=False, clear_inner=True, clear_outer=False, threshold=0.001)
            
    bpy.ops.object.mode_set(mode = 'OBJECT')
   



   
    
##\brief Morphs a tile-filled polygon cage back to the original shape.
#\detail Intended to be used in functions like replace_poly(), not standalone.
#\returns (None) 
#\param tile (Object) Tile to be morphed.
#\param poly (Polygon) The polygon the bounds are taken from. 
#\param polybox ([mathutils.Vector,mathutils.Vector,mathutils.Vector,mathutils.Vector]) The polygon's bounding box, as calculated in getPolyBox().
#\param edgemap ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge.
#\param morph (String in ["s","d","ds"]) Morph mode. If it contains "d", the dominant axis is morphed, if it contains "s", the subdominant axis is morphed. 
#\param nors (Boolean) Respect normals when cutting(optional, default = False). 
def morphTile_quad(tile,poly,polybox,edgemap,morph,nors = None):
    
    up = mathutils.Vector([0,1,0])
    right = mathutils.Vector([1,0,0])

    smallest_ang_edge = 0
    ang = 400
    
    if morph == "s":
    
        
        if not nors == None:
            nors = flattenNors(nors)
    
    
    
        dominants = findDomEdges_quad(poly,edgemap)
        
        subdominants = []
        
        for edge in edgemap:
            if not edge in dominants:
                subdominants.append(edge)
    
        testedge = subdominants[0]
        testedge2 = subdominants[1]
            
            
        center1 = utils_MATH.getMidCoords([poly[testedge[0]],poly[testedge[1]]])
        center2 = utils_MATH.getMidCoords([poly[testedge2[0]],poly[testedge2[1]]])
            
        if center1[0] > center2[0]:
            rightE = testedge
            leftE = testedge2
                
        else:
            rightE = testedge2
            leftE = testedge
            
        
            
   
   
        anchor1 = poly[rightE[0]]
        anchor2 = poly[leftE[0]]
        
        
        testvec1 = poly[rightE[0]] - poly[rightE[1]]
        testvec1.normalize()
        testvec1.negate()
           
        rat1 = 1/testvec1[1]
        distance_r = testvec1[0] * rat1

  
        testvec2 = poly[leftE[0]] - poly[leftE[1]]
        testvec2.normalize()
        testvec2.negate()
            
        rat2 = 1/testvec2[1]
        distance_l = testvec2[0] * rat2
                
                
        maxdis = polybox[1] - polybox[0]
        
        if nors == None:       
            for vert in tile.data.vertices:     
        
                disp1 = anchor1[1] - vert.co[1]
                disp2 = anchor2[1] - vert.co[1]
                
                pot1 = anchor1[0] - disp1*distance_r
                pot2 = anchor2[0] - disp2*distance_l
                
                fac = (polybox[1] - vert.co[0])/maxdis
         
                vert.co[0] = pot2*fac + pot1*(1-fac)
                
        else:
                
            for nor in nors:
                nor[1] = 0

            testvec1 = poly[rightE[0]]+nors[rightE[0]] - poly[rightE[1]] - nors[rightE[1]]
            testvec1.normalize()
            testvec1.negate()
               
            rat1_2 = 1/testvec1[1]
            distance_r_n = testvec1[0] * rat1_2

      
            testvec2 = poly[leftE[0]]+nors[leftE[0]] - poly[leftE[1]] - nors[leftE[1]]
            testvec2.normalize()
            testvec2.negate()
                
            rat2_2 = 1/testvec2[1]
            distance_l_n = testvec2[0] * rat2_2
                
                
            diff1 = distance_r - distance_r_n
            diff2 = distance_l - distance_l_n
                
            
            for vert in tile.data.vertices:     
        
                disp1 = anchor1[1] - vert.co[1]
                disp2 = anchor2[1] - vert.co[1]
                
                pot1 = anchor1[0] - disp1*distance_r + vert.co[2]*rat1 *( disp1 * diff1 + rat1_2*nors[rightE[0]][0])
                pot2 = anchor2[0] - disp2*distance_l + vert.co[2]*rat2 *( disp2 * diff2 + rat2_2*nors[leftE[0]][0])

                
                fac = (polybox[1] - vert.co[0])/maxdis
         
                vert.co[0] = pot2*fac + pot1*(1-fac)
                
                
            
            
            
           
       
                

                    
                
                
                
    
    elif morph == "d":
    
        if not nors == None:
            nors = flattenNors(nors)
    
        dominants = findDomEdges_quad(poly,edgemap)
        
        testedge = dominants[0]
        testedge2 = dominants[1]
            
            
        center1 = utils_MATH.getMidCoords([poly[testedge[0]],poly[testedge[1]]])
        center2 = utils_MATH.getMidCoords([poly[testedge2[0]],poly[testedge2[1]]])
            
        if center1[1] > center2[1]:
            rightE = testedge
            leftE = testedge2
                
        else:
            rightE = testedge2
            leftE = testedge
   
   
        
        
        anchor1 = poly[rightE[0]]
        anchor2 = poly[leftE[0]]
        
        
        testvec1 = - poly[rightE[0]] + poly[rightE[1]]
        testvec1.normalize()
           
        rat1 = 1/testvec1[0]
        distance_r = testvec1[1] * rat1

  
        testvec2 = - poly[leftE[0]] + poly[leftE[1]]
        testvec2.normalize()
            
        rat2 = 1/testvec2[0]
        distance_l = testvec2[1] * rat2
                
                
        maxdis = polybox[3] - polybox[2]
        
        if nors == None:       
            for vert in tile.data.vertices:     
        
                disp1 = anchor1[0] - vert.co[0]
                disp2 = anchor2[0] - vert.co[0]
                
                pot1 = anchor1[1] - disp1*distance_r
                pot2 = anchor2[1] - disp2*distance_l
                
                fac = (polybox[3] - vert.co[1])/maxdis
         
                vert.co[1] = pot2*fac + pot1*(1-fac)
                
        else:

            testvec1 =  - poly[rightE[0]] - nors[rightE[0]] + poly[rightE[1]] + nors[rightE[1]]
            testvec1.normalize()
               
            rat1_2 = 1/testvec1[0]
            distance_r_n = testvec1[1] * rat1_2

      
            testvec2 = - poly[leftE[0]] - nors[leftE[0]] + poly[leftE[1]] + nors[leftE[1]]
            testvec2.normalize()
                
            rat2_2 = 1/testvec2[0]
            distance_l_n = testvec2[1] * rat2_2
                
                
            diff1 = distance_r - distance_r_n
            diff2 = distance_l - distance_l_n
                
            
            for vert in tile.data.vertices:     
        
                disp1 = anchor1[0] - vert.co[0]
                disp2 = anchor2[0] - vert.co[0]
                
                pot1 = anchor1[1] - disp1*distance_r + vert.co[2]*rat1 *( disp1 * diff1 + rat1_2*nors[rightE[0]][1])
                pot2 = anchor2[1] - disp2*distance_l + vert.co[2]*rat2 *( disp2 * diff2 + rat2_2*nors[leftE[0]][1])

                
                fac = (polybox[3] - vert.co[1])/maxdis
         
                vert.co[1] = pot2*fac + pot1*(1-fac)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
            
    elif morph == "ds":
    
        if not nors == None:
            nors = flattenNors(nors)
    
        dominants = findDomEdges_quad(poly,edgemap)
        
        testedge = dominants[0]
        testedge2 = dominants[1]
        
        center1 = utils_MATH.getMidCoords([poly[testedge[0]],poly[testedge[1]]])
        center2 = utils_MATH.getMidCoords([poly[testedge2[0]],poly[testedge2[1]]])
            
        if center1[1] > center2[1]:
            topE = testedge
            botE = testedge2
                
        else:
            topE = testedge2
            botE = testedge
            
            
            
        targetBL = poly[botE[0]]
        targetBR = poly[botE[1]]
        if not nors == None:
            norBL = nors[botE[0]]
            norBR = nors[botE[1]]
        else:
            norBL = mathutils.Vector([0,0,1])
            norBR = mathutils.Vector([0,0,1])
        
        if targetBL[0] > targetBR[0]:
            targetBL = poly[botE[1]]
            targetBR = poly[botE[0]]
            
            if not nors == None:
                norBL = nors[botE[1]]
                norBR = nors[botE[0]]
            
            
        targetTL = poly[topE[0]]
        targetTR = poly[topE[1]]
        if not nors == None:
            norTL = nors[topE[0]]
            norTR = nors[topE[1]]
        else:
            norTL = mathutils.Vector([0,0,1])
            norTR = mathutils.Vector([0,0,1])
        
        
        if targetTL[0] > targetTR[0]:
            targetTL = poly[topE[1]]
            targetTR = poly[topE[0]]
            if not nors == None:
                norTL = nors[topE[1]]
                norTR = nors[topE[0]]
            
            
        cornerBL = mathutils.Vector([polybox[0],polybox[2],0])
        cornerBR = mathutils.Vector([polybox[1],polybox[2],0])
        
        cornerTL = mathutils.Vector([polybox[0],polybox[3],0])
        cornerTR = mathutils.Vector([polybox[1],polybox[3],0])
        
        
        vectorBL = targetBL - cornerBL
        vectorBR = targetBR - cornerBR
        vectorTL = targetTL - cornerTL
        vectorTR = targetTR - cornerTR
        
        spanD = polybox[3] - polybox[2]
        spanSD = polybox[1] - polybox[0]
            

        for vert in tile.data.vertices:
            
            facD = (polybox[3] - vert.co[1])/spanD
            facSD = (polybox[1] - vert.co[0])/spanSD
            
            vecR = (vectorBR + vert.co[2] * norBR)*facD + (vectorTR + vert.co[2] * norTR)*(1-facD)
            vecL = (vectorBL + vert.co[2] * norBL)*facD + (vectorTL + vert.co[2] * norTL)*(1-facD)

            vector = vecL*facSD + vecR*(1-facSD)
            
            vert.co += vector
            
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
##\brief Flattens normal vectors to tile-conform dimensions (no Z-axis).
#\returns ([mathutils.Vector]) The flattened normals. 
#\param nors ([mathutils.Vector]) The normals to be flattened.  
def flattenNors(nors):
    for nor in nors:
        ratio = 1/nor[2]
        nor[2] = 0
        nor[0] *= ratio
        nor[1] *= ratio
       
    return nors
        
                
            
            
    
            
    
    
    
    
                    
                    
            
            
                
 

##\brief Morphs triangles.
#\returns (None)
#\param tile (Object) Tile to be morphed.
#\param poly (Polygon) The polygon the bounds are taken from. 
#\param polybox ([mathutils.Vector,mathutils.Vector,mathutils.Vector,mathutils.Vector]) The polygon's bounding box, as calculated in getPolyBox().
#\param edgemap ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge.
#\param morph (String in ["s","d","ds"]) Morph mode. If it contains "d", the dominant axis is morphed, if it contains "s", the subdominant axis is morphed. 
#\param nors (Boolean) Respect normals when cutting(optional, default = False).
def morphTile_tri(tile,poly,polybox,edgemap,morph,nors = None):
    
    if morph == "m":
        morphTile_tri_cage(tile,poly,polybox,edgemap,nors)
    elif morph == "p":
        morphTile_tri_pinch(tile,poly,polybox,edgemap,nors)
 
    
##\brief Morphing subfunction. Takes the same arguments as morphTile_tri().
def morphTile_tri_cage(tile,poly,polybox,edgemap,nors = None):

    right = mathutils.Vector([1,0,0])
    up = mathutils.Vector([0,1,0])

    smallest_ang_edge = 0
    ang = 400
    ax = 0
    
    for i in range(0,len(edgemap)):
    
        edge = edgemap[i]
    
        co1 = poly[edge[0]]
        co2 = poly[edge[1]]

        vector = co1 - co2
        
        angle = utils_MATH.getAngle(vector,right)
        angle2 = utils_MATH.getAngle(vector,up)
        
        if angle > 90:
            angle = math.fabs(180-angle)
        
        if angle < ang:
            ang = angle
            smallest_ang_edge = i  
            ax = 0

        if angle2 < ang:
            ang = angle2
            smallest_ang_edge = i
            ax = 1
                
    if ax == 0 and not ang > 370:
    
        testedge = edgemap[smallest_ang_edge]
            
        v1 = poly[testedge[0]]
        v2 = poly[testedge[1]]
        
        if not nors == None:
            v1_n = nors[testedge[0]]
            v2_n = nors[testedge[1]]
        
        if v1[0] < v2[0]:
            v1 = poly[testedge[1]]
            v2 = poly[testedge[0]]
            if not nors == None:
                v1_n = nors[testedge[1]]
                v2_n = nors[testedge[0]]
        
        v3 = None
        v3_n = None
        
        for i in range(0,len(poly)):
            if not i in testedge:
                v3 = poly[i]
                if not nors == None:
                    v3_n = nors[i]
                
        #v1 is always the upper one of both testedge vertices
        
        mid = utils_MATH.getMidCoords([v1,v2])
        
        vec = v3-mid
        
        
        v1_con = v1 + vec
        v2_con = v2 + vec

            
            
            
            
            
    elif ax == 1 and not ang > 370:
    
        testedge = edgemap[smallest_ang_edge]
            
        v1 = poly[testedge[0]]
        v2 = poly[testedge[1]]
        
        if not nors == None:
            v1_n = nors[testedge[0]]
            v2_n = nors[testedge[1]]
        
        if v1[1] < v2[1]:
            v1 = poly[testedge[1]]
            v2 = poly[testedge[0]]
            if not nors == None:
                v1_n = nors[testedge[1]]
                v2_n = nors[testedge[0]]
        
        v3 = None
        v3_n = None
        
        for i in range(0,len(poly)):
            if not i in testedge:
                v3 = poly[i]
                if not nors == None:
                    v3_n = nors[i]
                
        #v1 is always the upper one of both testedge vertices
        
        mid = utils_MATH.getMidCoords([v1,v2])
        
        vec = v3-mid

        
        v1_con = v1 + vec
        v2_con = v2 + vec
        
        
        
    new_poly = [v1,v2,v1_con,v2_con]
    new_edges = [[0,1],[0,2],[1,3],[2,3]]
    if not nors == None:
        new_nors = [v1_n,v2_n,v3_n,v3_n.copy()]
        morphTile_quad(tile,new_poly,polybox,new_edges,"ds",new_nors)
    else:
        morphTile_quad(tile,new_poly,polybox,new_edges,"ds")
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
##\brief Morphing subfunction. Takes the same arguments as morphTile_tri().
def morphTile_tri_pinch(tile,poly,polybox,edgemap,nors = None):
    
    
    right = mathutils.Vector([1,0,0])
    up = mathutils.Vector([0,1,0])
    
    z = mathutils.Vector([0,0,1])

    smallest_ang_edge = 0
    ang = 400
    ax = 0
    
    for i in range(0,len(edgemap)):
    
        edge = edgemap[i]
    
        co1 = poly[edge[0]]
        co2 = poly[edge[1]]

        vector = co1 - co2
        
        angle = utils_MATH.getAngle(vector,right)
        angle2 = utils_MATH.getAngle(vector,up)
        
        if angle > 90:
            angle = math.fabs(180-angle)
        
        if angle < ang:
            ang = angle
            smallest_ang_edge = i  
            ax = 0

        if angle2 < ang:
            ang = angle2
            smallest_ang_edge = i
            ax = 1
                
    if ax == 0 and not ang > 370:
    
        testedge = edgemap[smallest_ang_edge]
            
        v1 = poly[testedge[0]]
        v2 = poly[testedge[1]]
        
        if not nors == None:
            v1_n = nors[testedge[0]]
            v2_n = nors[testedge[1]]
        
        if v1[0] < v2[0]:
            v1 = poly[testedge[1]]
            v2 = poly[testedge[0]]
            if not nors == None:
                v1_n = nors[testedge[1]]
                v2_n = nors[testedge[0]]
        
        v3 = None
        v3_n = None
        
        for i in range(0,len(poly)):
            if not i in testedge:
                v3 = poly[i]
                if not nors == None:
                    v3_n = nors[i]
                

            
            
            
            
            
    elif ax == 1 and not ang > 370:
    
        testedge = edgemap[smallest_ang_edge]
            
        v1 = poly[testedge[0]]
        v2 = poly[testedge[1]]
        
        if not nors == None:
            v1_n = nors[testedge[0]]
            v2_n = nors[testedge[1]]
        
        if v1[1] < v2[1]:
            v1 = poly[testedge[1]]
            v2 = poly[testedge[0]]
            if not nors == None:
                v1_n = nors[testedge[1]]
                v2_n = nors[testedge[0]]
        
        v3 = None
        v3_n = None
        
        for i in range(0,len(poly)):
            if not i in testedge:
                v3 = poly[i]
                if not nors == None:
                    v3_n = nors[i]
        

    
    
    new_poly = [v1,v2,v3,v3]
    new_edges = [[0,1],[0,2],[1,3],[2,3]]
    
    
    if not nors == None:
        new_nors = [v1_n,v2_n,v3_n,v3_n.copy()]
        morphTile_quad(tile,new_poly,polybox,new_edges,"ds",new_nors)
    else:
        morphTile_quad(tile,new_poly,polybox,new_edges,"ds")
            
 

    
##\brief Cuts a tile to a polygon's boundary edges (dominant axis only).
#\detail Intended to be used in functions like replace_poly(), not standalone.
#\returns (None) 
#\param tile (Object) Tile to be cut.
#\param poly (Polygon) The polygon the bounds are taken from. 
#\param domEdges ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge along the X-axis.
#\param nors (Boolean) Respect normals when cutting(optional, default = False).     
def cutTile_dom(tile,poly,domEdges,nors = None):
    
    bpy.context.scene.objects.active = tile

    bpy.ops.object.mode_set(mode = 'EDIT')
    

    up = mathutils.Vector([0,0,1])
    center = mathutils.Vector([0,0,0])
    
    if nors == None:
        for edge in domEdges:
        
            bpy.ops.mesh.select_all(action = "SELECT")
            
            vector = poly[edge[1]] - poly[edge[0]]
            
            normal = vector.cross(up)
            
            if normal.dot(-poly[edge[0]]) < 0:
                normal.negate()
            
            bpy.ops.mesh.bisect(plane_co=poly[edge[0]], plane_no=normal, use_fill=False, clear_inner=True, clear_outer=False, threshold=0.001)
            
    else:
        for edge in domEdges:
        
            bpy.ops.mesh.select_all(action = "SELECT")
            
            vector = poly[edge[1]] - poly[edge[0]]
            nor = utils_MATH.getMidCoords([nors[edge[1]],nors[edge[0]]])
            
            normal = vector.cross(nor)
            
            if normal.dot(-poly[edge[0]]) < 0:
                normal.negate()
            
            bpy.ops.mesh.bisect(plane_co=poly[edge[0]], plane_no=normal, use_fill=False, clear_inner=True, clear_outer=False, threshold=0.001)
           
            
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    
    
    
    
    return
 



##\brief Cuts a tile to a polygon's boundary edges (subdominant axis only).
#\detail Intended to be used in functions like replace_poly(), not standalone.
#\returns (None) 
#\param tile (Object) Tile to be cut.
#\param poly (Polygon) The polygon the bounds are taken from. 
#\param edgemap ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge.
#\param domEdges ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge along the X-axis.
#\param nors (Boolean) Respect normals when cutting(optional, default = False).  
def cutTile_subdom(tile,poly,edgemap,domEdges,nors = None):
    
    bpy.context.scene.objects.active = tile

    bpy.ops.object.mode_set(mode = 'EDIT')
    

    up = mathutils.Vector([0,0,1])
    center = mathutils.Vector([0,0,0])
    
    
    
    if nors == None:
        for edge in edgemap:
        
            if not edge in domEdges:
        
                bpy.ops.mesh.select_all(action = "SELECT")
                
                vector = poly[edge[1]] - poly[edge[0]]
                
                normal = vector.cross(up)
                
                if normal.dot(-poly[edge[0]]) < 0:
                    normal.negate()
                
                bpy.ops.mesh.bisect(plane_co=poly[edge[0]], plane_no=normal, use_fill=False, clear_inner=True, clear_outer=False, threshold=0.001)
            
    else:
        for edge in edgemap:
        
            if not edge in domEdges:
        
                bpy.ops.mesh.select_all(action = "SELECT")
                
                vector = poly[edge[1]] - poly[edge[0]]
                nor = utils_MATH.getMidCoords([nors[edge[1]],nors[edge[0]]])
                
                normal = vector.cross(nor)
                
                if normal.dot(-poly[edge[0]]) < 0:
                    normal.negate()
                
                bpy.ops.mesh.bisect(plane_co=poly[edge[0]], plane_no=normal, use_fill=False, clear_inner=True, clear_outer=False, threshold=0.001)
           
            
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    
    return
                


##\brief Finds all edges running orthogonal to the dominant axis (Y-axis), for triangles.
#\detail Intended to be used in functions like replace_poly(), not standalone.
#\returns ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge along the X-axis. 
#\param poly (Polygon) The polygon the bounds are taken from. 
#\param edgemap ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge.             
def findDomEdges_tri(poly,edgemap):
    
    right = mathutils.Vector([1,0,0])
    up = mathutils.Vector([0,1,0])

    smallest_ang_edge = 0
    ang = 400
    ax = 0
    
    for i in range(0,len(edgemap)):
    
        edge = edgemap[i]
    
        co1 = poly[edge[0]]
        co2 = poly[edge[1]]

        vector = co1 - co2
        
        angle = utils_MATH.getAngle(vector,right)
        angle2 = utils_MATH.getAngle(vector,up)
        
        if angle > 90:
            angle = math.fabs(180-angle)
        
        if angle < ang:
            ang = angle
            smallest_ang_edge = i  
            ax = 0

        if angle2 < ang:
            ang = angle2
            smallest_ang_edge = i
            ax = 1
            
    
    if ax == 0 and not ang > 370:
        return [edgemap[smallest_ang_edge]]

    elif ax == 1 and not ang > 370:
        
        retmap = []
        for i in range(0,len(edgemap)):
            if not i == smallest_ang_edge:
                retmap.append(edgemap[i])
                
        return retmap
        

##\brief Finds all edges running orthogonal to the dominant axis (Y-axis), for quads.
#\detail Intended to be used in functions like replace_poly(), not standalone.
#\returns ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge along the X-axis. 
#\param poly (Polygon) The polygon the bounds are taken from. 
#\param edgemap ([[Int,Int]]) A list of 2-element lists containing the vertex indices that form an edge.          
def findDomEdges_quad(poly,edgemap):
                
    up = mathutils.Vector([0,1,0])
    right = mathutils.Vector([1,0,0])

    smallest_ang_edge = 0
    ang = 400
            
    for i in range(0,len(edgemap)):
    
        edge = edgemap[i]
    
        co1 = poly[edge[0]]
        co2 = poly[edge[1]]

        vector = co1 - co2
        
        angle = utils_MATH.getAngle(vector,right)
        
        if angle > 90:
            angle = math.fabs(180-angle)
        
        if angle < ang:
            ang = angle
            smallest_ang_edge = i
                
                
    if not ang > 370:
    

        testedge = edgemap[smallest_ang_edge]
    
            
            
        for edge in edgemap:
            if not testedge[0] in edge and not testedge[1] in edge:
                testedge2 = edge
            
        return[testedge,testedge2]
        
            
                    
def project_merge(ob, tar, type):   

    z_unit = mathutils.Vector([0,0,1])
    y_unit = mathutils.Vector([0,1,0])
        
    if type == "a":
        
        nor = []
        
        for face in ob.data.polygons:
            if face.select:
                nor.append(face.normal)
                
        nor = mathutils.Vector(utils_MATH.getMidCoords(nor))
        if nor.length == 0:
            nor = mathutils.Vector([1,1,1])
        else:
            nor = mathutils.Vector([1,1,1])
         

        nor_xy = mathutils.Vector([nor[0],nor[1],0])
            
        angXY = -utils_MATH.getAngleNor(nor_xy,y_unit,z_unit)
        
        angZ = nor.angle(z_unit)
        
        
        rotmat1 = mathutils.Matrix.Rotation(angXY,4,"Z")
        rotmat2 = mathutils.Matrix.Rotation(angZ,4,"X")
        
        rotmat = rotmat2*rotmat1
        
        quat = rotmat.to_quaternion()


        
        original_type = bpy.context.area.type
        bpy.context.area.type = "VIEW_3D"
        
        for space in bpy.context.area.spaces:
            if space.type == "VIEW_3D":

                region = space.region_3d
                        
                region.view_perspective = "ORTHO"
                        
                region.view_rotation.rotate(quat)
        
                            
                            

                            
        ob_proj = utils_OBJ.copyobj_vis(ob)
        
        bpy.context.scene.objects.active = ob_proj
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = "INVERT")
        bpy.ops.mesh.delete(type="FACE")
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.delete(type="FACE")
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        #We will now use ob_proj to projection cut into tar
        
        utils_OBJ.hide_all([tar,ob_proj])
        
        bpy.context.scene.objects.active = tar
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = "DESELECT")
        
        try:
            bpy.ops.mesh.knife_project(cut_through=False)
        except:
            pass
        
        connectgroup = tar.vertex_groups.new("$BG$_CONNECT")
        bpy.ops.object.vertex_group_set_active(group = connectgroup.name)
        bpy.ops.object.vertex_group_assign()

        bpy.ops.mesh.delete(type="FACE")
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        bpy.context.scene.objects.active = ob_proj
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = "SELECT")
        bpy.ops.mesh.dissolve_edges()
        bpy.ops.mesh.delete(type="ONLY_FACE")
        bpy.ops.mesh.select_all(action = "SELECT")
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        utils_OBJ.join([tar,ob_proj])
        
        bpy.context.scene.objects.active = tar
        bpy.ops.object.mode_set(mode = 'EDIT')
        try:
            bpy.ops.mesh.bridge_edge_loops(type='SINGLE', use_merge=False, merge_factor=0.5, twist_offset=0, number_cuts=0, interpolation='PATH', smoothness=1.0, profile_shape_factor=0.0, profile_shape='SMOOTH')
        except:
            pass
        bpy.ops.mesh.dissolve_limited(angle_limit=math.radians(1))
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        ob.hide = False
        
        utils_OBJ.join([ob,tar])
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=True)
        bpy.ops.object.mode_set(mode = 'OBJECT')
            
        bpy.context.area.type = original_type
        
        
        



##\brief Slices off the bottom of an object.
#\returns (None)
#\param ob (Object) The object to get sliced. 
#\param pos (mathutils.Vector) The anchor point of the knife plane.
#\param nor (mathutils.Vector) The normal vector of the knife plane.     
#\param fill (Boolean) Whether or not to fill the sliced area.   
def slice_bottom(ob,pos,nor,fill):

    bpy.context.scene.objects.active = ob
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.bisect(plane_co = pos, plane_no = nor, clear_outer = True, use_fill = fill)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
##\brief Cuts out a slice of an object.
#\returns (None)
#\param ob (Object) The object to get sliced. 
#\param pos1 (mathutils.Vector) The anchor point of the first knife's plane.
#\param pos2 (mathutils.Vector) The anchor point of the second knife's plane.
#\param nor1 (mathutils.Vector) The normal vector of the first knife's plane. 
#\param nor2 (mathutils.Vector) The normal vector of the second knife's plane.     
#\param fill (Boolean) Whether or not to fill the sliced area.     
def slice(ob,pos1,pos2,nor1,nor2,fill):

    bpy.context.scene.objects.active = ob

    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.bisect(plane_co = pos1, plane_no = nor1,clear_inner = True,clear_outer = False, use_fill = fill)
    bpy.ops.mesh.select_all(action = "SELECT")
    bpy.ops.mesh.bisect(plane_co = pos2, plane_no = nor2,clear_outer = True,clear_inner = False, use_fill = fill)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
 

##\brief Slices off the top of an object.
#\returns (None)
#\param ob (Object) The object to get sliced. 
#\param pos (mathutils.Vector) The anchor point of the knife plane.
#\param nor (mathutils.Vector) The normal vector of the knife plane.     
#\param fill (Boolean) Whether or not to fill the sliced area.   
def slice_top(ob,pos,nor,fill):
    
    bpy.context.scene.objects.active = ob
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.bisect(plane_co = pos, plane_no = nor, clear_inner = True, clear_outer = False, use_fill = fill)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
##\brief Replaces a polygon with a tile anchored to its center.
#\returns (None) 
#\param ob (Object) Source object. 
#\param tiles ([Object]) Tiles to choose from.
#\param ind (Int) Index of the chosen tile (-1 for random).
#\param norMode (String in ["N","V"]) Normal mode, either the polygon's normal ("N") or a vector ("V").
#\param axis (String in ["N","X","Y","Z","V"]) Dominant axis.
#\param fallback (String in ["N","X","Y","Z","V"]) Fallback axis.
#\param offset (mathutils.Vector) Tile offset.
#\param edgemode (String in ["e", "f"]). Whether to take the adjactant faces normals as edge normal ("f") or make the normal run along the edge ("e")
#\param compensate (Boolean) Whether to compensate for small angle offsets or not.
#\param vec (mathutils.Vector) Vector to replace edge normal (in case norMode is "V", and then it can't be (None)).  
def replace_edge_c(ob,tiles,ind,norMode,axis,fallback,offset,edgemode,compensate,vec=None):

    if axis in ["X","-X"]:
        
        if axis == "X":
            checkVec = mathutils.Vector([1,0,0])
        else:
            checkVec = mathutils.Vector([-1,0,0])

        if fallback in ["X","-X"]:
            return
            
    elif axis in ["Y","-Y"]:
    
        if axis == "Y":
            checkVec = mathutils.Vector([0,1,0])
        else:
            checkVec = mathutils.Vector([0,-1,0])

        if fallback in ["Y","-Y"]:
            return
            
    elif axis in ["Z","-Z"]:
    
        if axis == "Z":
            checkVec = mathutils.Vector([0,0,1])
        else:
            checkVec = mathutils.Vector([0,0,-1])

        if fallback in ["Z","-Z"]:
            return
            
    
    zero = mathutils.Vector([0,0,0])   

    obs = [ob]

    if norMode == "N":
    
        if ind == -1:
    
            for edge in ob.data.edges:
                if edge.select and not edge.hide:
                    ind = random.randrange(0,len(tiles))
                    ob2 = utils_OBJ.copyobj_vis(tiles[ind])
                    offset_dom(ob2,offset)
                    
                    e_pos = getEdgePos(ob,edge.index)
                    
                    if not compensate or edgemode == "e":
                    
                        e_nor = zero
                        if edgemode == "f":
                            e_nor = getEdgeNormal(ob,edge.index)   
                            
                        if edgemode == "e" or e_nor == zero:
                            e_nor = getEdgeNormal_along(ob,edge.index,axis,fallback)
                        
                        if e_nor == checkVec:
                            tileToX(ob2,e_nor,fallback,e_pos)
                        else:
                            tileToX(ob2,e_nor,axis,e_pos)

                        obs.append(ob2)
                        
                    else: 
                        e_nor = getEdgeNormal_along(ob,edge.index,axis,fallback)
                        
                        if e_nor == checkVec:
                            tileToX(ob2,e_nor,fallback,e_pos,compensate)
                        else:
                            tileToX(ob2,e_nor,axis,e_pos,compensate)

                        obs.append(ob2)
                        
                    
        else:
            
            for edge in ob.data.edges:
                if edge.select and not edge.hide:
                    ob2 = utils_OBJ.copyobj_vis(tiles[ind])
                    offset_dom(ob2,offset)
                    
                    e_pos = getEdgePos(ob,edge.index)
                    
                    if not compensate or edgemode == "e":
                    
                        e_nor = zero
                        if edgemode == "f":
                            e_nor = getEdgeNormal(ob,edge.index)
                        if edgemode == "e" or e_nor == zero:
                            e_nor = getEdgeNormal_along(ob,edge.index,axis,fallback)
                        
                        if e_nor == checkVec:
                            tileToX(ob2,e_nor,fallback,e_pos)
                        else:
                            tileToX(ob2,e_nor,axis,e_pos)

                        obs.append(ob2)
                        
                    else: 
                        e_nor = getEdgeNormal(ob,edge.index)
                        e_nor2 = getEdgeNormal_along(ob,edge.index,axis,fallback)
                        
                        if not e_nor == zero:
                        
                            if e_nor == checkVec:
                                tileToX(ob2,e_nor,fallback,e_pos,e_nor2)
                            else:
                                tileToX(ob2,e_nor,axis,e_pos,e_nor2)
                                
                        else:
                            
                            e_nor = getEdgeNormal_along(ob,edge.index,axis,fallback)
                            
                            if e_nor == checkVec:
                                tileToX(ob2,e_nor,fallback,e_pos,compensate)
                            else:
                                tileToX(ob2,e_nor,axis,e_pos,compensate)
                            

                        obs.append(ob2)
                        
                        
                    
                    
    elif norMode == "V" and not vec == None:
    
        if vec == checkVec:
            axis = fallback
    
        if ind == -1:
    
            for edge in ob.data.edges:
                if edge.select and not edge.hide:
                    ind = random.randrange(0,len(tiles))
                    ob2 = utils_OBJ.copyobj_vis(tiles[ind])
                    offset_dom(ob2,offset)
                    
                    e_pos = getEdgePos(ob,edge.index)

                    tileToX(ob2,vec,axis,e_pos)
                            
                    obs.append(ob2)
                    
            
                    
        else:
            
            for edge in ob.data.edges:
                if edge.select and not edge.hide:
                    ob2 = utils_OBJ.copyobj_vis(tiles[ind])
                    offset_dom(ob2,offset)
                    
                    e_pos = getEdgePos(ob,edge.index)
 
                    tileToX(ob2,vec,axis,e_pos)

                    obs.append(ob2)
                    
      
    
    
                
    if len(obs) > 1:
        scene = bpy.context.scene
        ctx = bpy.context.copy()
        
        bpy.context.scene.objects.active = ob
        
        ctx['active_object'] = obs[0]
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = "SELECT")
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        ctx['selected_objects'] = obs
        
        ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]

        bpy.ops.object.join(ctx)
        
        
        
        
        
     



     
        
 

##\brief Replaces an edge with a tile.
#\returns (None) 
#\param ob (Object) Source object. 
#\param tiles ([Object]) Tiles to choose from.
#\param ind (Int) Index of the chosen tile (-1 for random).
#\param axis (String in ["N","X","Y","Z","V"]) Dominant axis.
#\param fallback (String in ["N","X","Y","Z","V"]) Fallback axis.
#\param offset (mathutils.Vector) Tile offset.
#\param tileAlign (String in ["s","t"]) How to tile the edge. "s" means stretching <tileReps> tiles along the edge, "t" means scaling all tiles by the factor <tileReps>, using as many as necessary to fill the edge.
#\param tileReps (Float) How many tiles should be used for an edge (to be placed along the edge).
#\param tileSubReps (Float) How many rows of tiles should be going along the edge.
#\param tileRand (Boolean) Use random tiles  along the edge.
#\param tileSubRand (Boolean) Use random tiles for each row.
#\param tileAlignment (String in ["b","c","t"]) Where to anchor the tiles (bottom, center, top) on the dominant axis. Has no effect if tileAlign is "s".
#\param morph_mode (String in ["m","c","x"]) How to morph the tiles. "m" scales them to the edge's length (no effect if tileAlign is "s"), "c" cuts them off and "x" does nothing.
#\param morph_faces (Boolean) Glue tiles to adjactant faces instead of have them sitting on the edge.
#\param cont (Boolean) Not implemented. "cont" will enable a continuous offset in edge loops, making edge tiles flow seamlessly.
def replace_edge_along(ob,tiles,ind,axis,fallback,offset,tileAlign,tileReps,tileSubReps,tileRand,tileSubRand,tileAlignment,morph_mode,morph_faces,cont):

    if axis in ["X","-X"]:
        
        if axis == "X":
            checkVec = mathutils.Vector([1,0,0])
        else:
            checkVec = mathutils.Vector([-1,0,0])

        if fallback in ["X","-X"]:
            return
            
    elif axis in ["Y","-Y"]:
    
        if axis == "Y":
            checkVec = mathutils.Vector([0,1,0])
        else:
            checkVec = mathutils.Vector([0,-1,0])

        if fallback in ["Y","-Y"]:
            return
            
    elif axis in ["Z","-Z"]:
    
        if axis == "Z":
            checkVec = mathutils.Vector([0,0,1])
        else:
            checkVec = mathutils.Vector([0,0,-1])

        if fallback in ["Z","-Z"]:
            return
            
    
    zero = mathutils.Vector([0,0,0])   

    obs = [ob]
    
    if ind == -1:

        for edge in ob.data.edges:
            if edge.select and not edge.hide:
                ind = random.randrange(0,len(tiles))
                
                
                ob2 = utils_OBJ.copyobj_vis(tiles[ind])
                list = edgetile_separate(ob2)
                
                tile = list[0]
                cage = list[1]
                
                
                list2 = fillEdgeTile(ob,edge,tile,cage,tiles,tileAlign,tileReps,tileSubReps,tileRand,tileSubRand,tileAlignment,morph_mode)
                
                tile_len = list2[0]
                tile_ex = list2[1]
                
                if morph_mode == "m" and tileAlign == "t":
                    morphEdgeTile(ob,edge,tile,tile_len)
                        
                elif morph_mode == "c":
                    cutEdgeTile(tile,tile_ex[0],tile_ex[1])
                    
                
                
                offset_dom(ob2,offset)
                
                e_pos = getEdgePos(ob,edge.index)

                e_nor = zero
                e_nor = getEdgeNormal(ob,edge.index)
                e_nor2 = getEdgeNormal_along(ob,edge.index,axis,fallback)                
                    
                if e_nor == zero:
                    e_nor = getEdgeNormal_vec(ob,edge.index,checkVec)
                    
                    
                if morph_faces:
                    morphEdgeFaces(ob,edge,tile,e_nor,e_nor2)
                    
                
                if e_nor == checkVec:
                    tileToX(ob2,e_nor,fallback,e_pos,e_nor2)
                else:
                    tileToX(ob2,e_nor,axis,e_pos,e_nor2)

                obs.append(ob2)

                    
                
    else:
        
        for edge in ob.data.edges:
            if edge.select and not edge.hide:
                ob2 = utils_OBJ.copyobj_vis(tiles[ind])
                list = edgetile_separate(ob2)
                
                tile = list[0]
                cage = list[1]
                
                
                list2 = fillEdgeTile(ob,edge,tile,cage,tiles,tileAlign,tileReps,tileSubReps,tileRand,tileSubRand,tileAlignment,morph_mode)
                
                tile_len = list2[0]
                tile_ex = list2[1]
                
                if morph_mode == "m" and tileAlign == "t":
                    morphEdgeTile(ob,edge,tile,tile_len)
                        
                elif morph_mode == "c":
                    cutEdgeTile(tile,tile_ex[0],tile_ex[1])
                    
                
                
                offset_dom(ob2,offset)
                
                e_pos = getEdgePos(ob,edge.index)

                e_nor = zero
                e_nor = getEdgeNormal(ob,edge.index)
                e_nor2 = getEdgeNormal_along(ob,edge.index,axis,fallback)                
                    
                if e_nor == zero:
                    e_nor = getEdgeNormal_vec(ob,edge.index,checkVec)
                    
                    
                if morph_faces:
                    morphEdgeFaces(ob,edge,tile,e_nor,e_nor2)
                    
                
                if e_nor == checkVec:
                    tileToX(ob2,e_nor,fallback,e_pos,e_nor2)
                else:
                    tileToX(ob2,e_nor,axis,e_pos,e_nor2)

                obs.append(ob2)

    
    
                
    if len(obs) > 1:
        scene = bpy.context.scene
        ctx = bpy.context.copy()
        
        bpy.context.scene.objects.active = ob
        
        ctx['active_object'] = obs[0]
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = "SELECT")
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        utils_OBJ.join(obs)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
##\brief Separates an edge tile's cage and the "real" tile.
#\detail To be scrapped, does basically the same as tile_separate().
#\returns ([Object,[mathutils.Vector,mathutils.Vector,mathutils.Vector,mathutils.Vector]]) The tile and its cage (as coordinates).
#\param tile (Object) The tile to be prepared.          
def edgetile_separate(tile):

    bpy.context.scene.objects.active = tile
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action = "DESELECT")
    bpy.ops.object.mode_set(mode = 'OBJECT')


    cage_ids = []
    tile_ids = []
    cage = []
    
    passCage = False
    
    try:
        index = tile.vertex_groups["cage"].index
    except:
        passCage = True
    
    if not passCage:
        for vert in tile.data.vertices:
            if index in [v.group for v in vert.groups]:
                cage_ids.append(vert.index)

    
    
    min_dom = 1000000
    max_dom = -1000000
    
    min_subdom = 1000000
    max_subdom = -1000000
    
    for vID in cage_ids:
        tile.data.vertices[vID].select = True
        
        coords = tile.data.vertices[vID].co
        
        if coords[1] > max_dom:
            max_dom = coords[1]
            
        if coords[1] < min_dom:
            min_dom = coords[1]
            
            
        if coords[0] > max_subdom:
            max_subdom = coords[0]
            
        if coords[0] < min_subdom:
            min_subdom = coords[0]
        
        
        
        
        
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if len(cage_ids) == 4:
        ret2 = [max_dom,min_dom,max_subdom,min_subdom]
    else:
        ret2 = findCage_edge(tile)
    
    return [tile,[max_dom,min_dom,max_subdom,min_subdom]]
    
    
##\brief Finds a cage for a given tile.
#\detail To be scrapped, does basically the same as findCage_poly().
#\returns ([Float,Float,Float,Float]) The cage (as minX, maxX, minY, maxY).
#\param tile (Object) A tile.   
def findCage_edge(tile):
    
    min_dom = 1000000
    max_dom = -1000000
    
    min_subdom = 1000000
    max_subdom = -1000000
    
    for vert in tile.data.vertices:
        
        coords = vert.co
        
        if coords[1] > max_dom:
            max_dom = coords[1]
            
        if coords[1] < min_dom:
            min_dom = coords[1]
            
            
        if coords[0] > max_subdom:
            max_subdom = coords[0]
            
        if coords[0] < min_subdom:
            min_subdom = coords[0]
            
            
    return [max_dom,min_dom,max_subdom,min_subdom]

    
    
 



##\brief Fills an edge's 2D bounding box with tiles.
#\returns ([mathutils.Vector,mathutils.Vector,mathutils.Vector,mathutils.Vector]) minX, maxX, minY and maxY of the polygon's box.
#\param ob (Object) The object holding the edge.
#\param edge (Edge) The edge to be filled. 
#\param tile (Object) The first tile (must get chosen beforehand).
#\param cage ([mathutils.Vector]) The polygon's cage's coordinates.
#\param tiles ([Object]) Tiles to choose from in case randomized is set.
#\param tileAlign (String in ["s","t"]) How to tile the edge. "s" means stretching <tileReps> tiles along the edge, "t" means scaling all tiles by the factor <tileReps>, using as many as necessary to fill the edge.
#\param tileReps (Float) How many tiles should be used for an edge (to be placed along the edge).
#\param tileSubReps (Float) How many rows of tiles should be going along the edge.
#\param tileRand (Boolean) Use random tiles  along the edge.
#\param tileSubRand (Boolean) Use random tiles for each row.
#\param alignment (String in ["b","c","t"]) Where to anchor the tiles (bottom, center, top) on the dominant axis. Has no effect if tileAlign is "s".
#\param morphing (String in ["m","c","x"]) How to morph the tiles. "m" scales them to the edge's length (no effect if tileAlign is "s"), "c" cuts them off and "x" does nothing.
#\param morph_faces (Boolean) Glue tiles to adjactant faces instead of have them sitting on the edge.
#\param lastInd (Int) Not implemented. "lastInd" will be the index of the last tile that's been added.
#\param contOffs (Boolean) Not implemented. "cont" will enable a continuous offset in edge loops, making edge tiles flow seamlessly.

def fillEdgeTile(ob,edge,tile,cage,tiles,tileAlign,tileReps,tileSubReps,tileRand,tileSubRand,alignment,morphing,lastInd = None,contOffs = None):
    
    if tileAlign == "s":
    
        tileReps = int(max(1,tileReps))
        tileSubReps = int(max(1,tileSubReps))
        
        v1 = ob.data.vertices[edge.vertices[0]].co
        v2 = ob.data.vertices[edge.vertices[1]].co
        
        distance = (v1-v2).length
        
        tileTarDis = distance/tileReps
        
        cagev1 = cage[0]
        cagev2 = cage[1]
        
        cagedis = cagev1-cagev2
        
        cagev1 = cage[2]
        cagev2 = cage[3]
        
        cageSubDis = cagev1-cagev2
        
        
        fac = tileTarDis/cagedis
        
        obs = [tile]
        
        if not tileRand:
            for i in range(1,tileReps):
                tile2 = utils_OBJ.copyobj_vis(tile)
                obs.append(tile2)
                tile2.location[1] = i*cagedis
                
                
        else:
            for i in range(1,tileReps):
                tile2 = utils_OBJ.copyobj_vis(tile)
                tile2 = edgetile_separate(tile2)[0]
                obs.append(tile2)
                tile2.location[1] = i*cagedis
                
                
        if tileSubReps > 1:
            
            subobs = []
            
            if not tileSubRand:
                
                for j in range(1,tileSubReps):
                    for ob in obs:
                        tile2 = utils_OBJ.copyobj_vis(ob)
                        subobs.append(tile2)
                        tile2.location[0] = j*cageSubDis
                        
            else:
                for j in range(1,tileSubReps):
                    for x in range(1,tileReps):
                        tile2 = utils_OBJ.copyobj_vis(ob)
                        subobs.append(tile2)
                        tile2.location[0] = j*cageSubDis
                        tile2.location[1] = x*cagedis
                
            obs.extend(subobs)   
    
        utils_OBJ.join(obs)
        
        
        

        offs_dom = ((tileReps-1) * cagedis)/2
        offs_subdom = ((tileSubReps-1) * cageSubDis)/2
        
        for vert in tile.data.vertices:
            vert.co[1] -= offs_dom
            vert.co[0] -= offs_subdom
            
            vert.co[1] *= fac
            
        return[tileReps*cagedis,None]
            
            
            
            
            
    else:
    
        if tileReps == 0:
            tileReps = 1
        
        tileSubReps = int(max(1,tileSubReps))
        
        v1 = ob.data.vertices[edge.vertices[0]].co
        v2 = ob.data.vertices[edge.vertices[1]].co
        
        distance = (v1-v2).length/tileReps

        
        cagev1 = cage[0]
        cagev2 = cage[1]
        
        cagedis = cagev1-cagev2
        
        cagev1 = cage[2]
        cagev2 = cage[3]
        
        cageSubDis = cagev1-cagev2
        
        obs = [tile]
        
        
        reps = int(math.ceil(distance*tileReps/cagedis))
        
        
        if not tileRand:
            for i in range(1,reps):
                tile2 = utils_OBJ.copyobj_vis(tile)
                obs.append(tile2)
                tile2.location[1] = i*cagedis
                
                
        else:
            for i in range(1,reps):
                tile2 = utils_OBJ.copyobj_vis(tile)
                tile2 = edgetile_separate(tile2)[0]
                obs.append(tile2)
                tile2.location[1] = i*cagedis
                
                
        if tileSubReps > 1:
            
            subobs = []
            
            if not tileSubRand:
                
                for j in range(1,tileSubReps):
                    for ob in obs:
                        tile2 = utils_OBJ.copyobj_vis(ob)
                        subobs.append(tile2)
                        tile2.location[0] = j*cageSubDis
                        
            else:
                for j in range(1,tileSubReps):
                    for x in range(1,reps):
                        tile2 = utils_OBJ.copyobj_vis(ob)
                        subobs.append(tile2)
                        tile2.location[0] = j*cageSubDis
                        tile2.location[1] = x*cagedis
                
            obs.extend(subobs)   
    
        utils_OBJ.join(obs)
        
        
        
        if morphing == "m" or alignment == "c":
            offs_dom = ((reps-1)*cagedis*tileReps)/2
            min_y = -offs_dom
            max_y = offs_dom
            
        elif alignment == "t":
            offs_dom = ((reps)*cagedis*tileReps)/2
            max_y = - offs_dom - (cagedis*tileReps)/2
            min_y = offs_dom + (cagedis*tileReps)/2
        
        elif alignment == "b":
            offs_dom = ((reps-2)*cagedis*tileReps)/2
            max_y = offs_dom + (cagedis*tileReps)/2
            min_y = - offs_dom - (cagedis*tileReps)/2
            
            
            
        offs_subdom = ((tileSubReps-1) * cageSubDis)/2
        
        for vert in tile.data.vertices:
            vert.co[1] -= offs_dom
            vert.co[0] -= offs_subdom
            
            vert.co[1] *= tileReps
            
        return ([reps*cagedis*tileReps,[min_y,max_y]])
            
            
            
            
            
 




##\brief Scales a row of tiles to the length of an edge.
#\returns (None)
#\param ob (Object) The object holding the edge.
#\param edge (Edge) The edge to be filled. 
#\param tile (Object) A tile.
#\param tile_len (Float) The length of one tile.
def morphEdgeTile(ob,edge,tile,tile_len):
        
    v1 = ob.data.vertices[edge.vertices[0]].co
    v2 = ob.data.vertices[edge.vertices[1]].co
    
    distance = (v1-v2).length
    
    fac = distance/tile_len
    
    
    for vert in tile.data.vertices:
        vert.co[1] *= fac
        





##\brief Cuts off tile parts that are longer than the edge.
#\returns (None)
#\param tile (Object) A tile.
#\param minPos (Float) One end of the edge (the lower X value).
#\param maxPos (Float) The other end of the edge (the higher X value).       
def cutEdgeTile(tile,minPos,maxPos):

    anchor1 = mathutils.Vector([0,minPos,0])
    anchor2 = mathutils.Vector([0,maxPos,0])
    
    dir = mathutils.Vector([0,1,0])

    bpy.context.scene.objects.active = tile

    bpy.ops.object.mode_set(mode = 'EDIT')
    
    bpy.ops.mesh.select_all(action = "SELECT")
    bpy.ops.mesh.bisect(plane_co = anchor1, plane_no = dir,clear_outer = False,clear_inner = True, use_fill = False)
    
    bpy.ops.mesh.select_all(action = "SELECT")
    bpy.ops.mesh.bisect(plane_co = anchor2, plane_no = dir,clear_outer = True,clear_inner = False, use_fill = False)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
            
        
            
        
        
        
        
        
##\brief Glues a row of tiles to adjactant faces.
#\returns (None)
#\param ob (Object) The object holding the edge.
#\param edge (Edge) The edge to be filled. 
#\param tile (Object) A tile.
#\param e_nor (mathutils.Vector) The edge's normal.
#\param along (mathutils.Vector) The vector along the edge.     
def morphEdgeFaces(ob,edge,tile,e_nor,along):

    nor1 = None
    found = False
    
    for face in ob.data.polygons:
        if edge.vertices[0] in face.vertices and edge.vertices[1] in face.vertices:
            if nor1 == None:
                nor1 = face.normal
                found = True
                break
                
    if not found:
        return
                

    ang = utils_MATH.getAngleNor(e_nor,nor1,along)
    
    if ang > math.radians(180):
        ang -= math.pi*2
        
        
    rotmat = mathutils.Matrix.Rotation(ang, 4, "Y").to_3x3()
    rotmatNEG = mathutils.Matrix.Rotation(-ang, 4, "Y").to_3x3()
    
    for vert in tile.data.vertices:
        
        if vert.co[0] < 0:
            vert.co = vert.co * rotmat
        elif vert.co[0] > 0:
            vert.co = vert.co * rotmatNEG
            
            
            
            
##\brief Joins two objects.
#\returns (None)
#\param ob (Object) The first object.
#\param ob2 (Object) The second object.
def join(ob,ob2):
    obs = [ob,ob2]
    utils_OBJ.join(obs)
        
        



##\brief Determines the object's center, based on the average position of all mesh vertices.
#\returns (mathutils.Vector) The average position.
#\param ob (Object) The object the mesh is taken from.
def meshCenter(ob):
    
    verts = []
    for v in ob.data.vertices:
        verts.append(v.co)
        
    return utils_MATH.getMidCoords(verts)
        
    
        
                
    
##\brief Proportionally translates an object, based on a cage.
#\detail For more info on which window, screen, area and region is the right one, check out the start of MESH_FilterCageNode's recalculate() function.
#\returns (None)
#\param ob (Object) The object that is translated (partially).    
#\param cage (Object) The object that acts as "hook" for ob.
#\param falloff (Float) The proportional editing falloff.
#\param vec (mathutils.Vector) The direction to move in.
#\param radius (Float) The influence radius.
#\param window (Window) The 3D View window.
#\param screen (Screen) The screen.
#\param area (Area) The area.
#\param region (Region) The region.
def prop_translate(ob,cage,falloff,vec,radius,window,screen,area,region):


    
    
    override = {'window': window, 'screen': screen, 'area': area,'region': region, 'edit_object': ob}
    
    




    bpy.context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.hide(unselected=True)
    bpy.ops.mesh.select_all(action = "DESELECT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    bpy.context.scene.objects.active = cage
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    
    cagegroup = cage.vertex_groups.new("$BG$_PROP_TRANS_CAGE")
    cagegroup_s = cage.vertex_groups.new("$BG$_PROP_TRANS_CAGESEL")
    bpy.ops.object.vertex_group_set_active(group = cagegroup_s.name)
    bpy.ops.object.vertex_group_assign()
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = "SELECT")
    
    bpy.ops.object.vertex_group_set_active(group = cagegroup.name)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action = "DESELECT")
    
    bpy.ops.object.vertex_group_set_active(group = cagegroup_s.name)
    
    bpy.ops.object.vertex_group_select()
    
    bpy.ops.mesh.hide(unselected=True)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    utils_OBJ.join([ob,cage])
    
    bpy.context.scene.objects.active = ob
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.transform.translate(override,value=vec, constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff=falloff, proportional_size=radius)
    
    bpy.ops.mesh.reveal()
    
    bpy.ops.mesh.select_all(action = "DESELECT")
    
    bpy.ops.object.vertex_group_set_active(group = cagegroup.name)
    
    bpy.ops.object.vertex_group_select()

    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.mesh.delete(type='VERT')
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    

    
    
    
    
    
    
    
    

    
##\brief Proportionally rotates an object, based on a cage.
#\detail For more info on which window, screen, area and region is the right one, check out the start of MESH_FilterCageNode's recalculate() function.
#\returns (None)
#\param ob (Object) The object that is translated (partially).    
#\param cage (Object) The object that acts as "hook" for ob.
#\param falloff (Float) The proportional editing falloff.
#\param ang (Float) The angle.
#\param axisvec (mathutils.Vector) The vector to rotate around.
#\param piv (mathutils.Vector) The rotation's pivot point.
#\param radius (Float) The influence radius.
#\param window (Window) The 3D View window.
#\param screen (Screen) The screen.
#\param area (Area) The area.
#\param region (Region) The region.   
def prop_rotate(ob,cage,falloff,ang,axisvec,piv,radius,window,screen,area,region):

    override2 = bpy.context.copy()
    override2[area] = area
    area.spaces[0].pivot_point = "CURSOR"
    area.spaces[0].cursor_location = piv
    
    override = {'window': window, 'screen': screen, 'area': area,'region': region, 'edit_object': ob}




    bpy.context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.hide(unselected=True)
    bpy.ops.mesh.select_all(action = "DESELECT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    bpy.context.scene.objects.active = cage
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    
    cagegroup = cage.vertex_groups.new("$BG$_PROP_TRANS_CAGE")
    cagegroup_s = cage.vertex_groups.new("$BG$_PROP_TRANS_CAGESEL")
    bpy.ops.object.vertex_group_set_active(group = cagegroup_s.name)
    bpy.ops.object.vertex_group_assign()
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = "SELECT")
    
    bpy.ops.object.vertex_group_set_active(group = cagegroup.name)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action = "DESELECT")
    
    bpy.ops.object.vertex_group_set_active(group = cagegroup_s.name)
    
    bpy.ops.object.vertex_group_select()
    
    bpy.ops.mesh.hide(unselected=True)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    utils_OBJ.join([ob,cage])
    
    bpy.context.scene.objects.active = ob
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.transform.rotate(override,value=math.radians(ang), axis=axisvec, constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff=falloff, proportional_size=radius)
    
    bpy.ops.mesh.reveal()
    
    bpy.ops.mesh.select_all(action = "DESELECT")
    
    bpy.ops.object.vertex_group_set_active(group = cagegroup.name)
    
    bpy.ops.object.vertex_group_select()

    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.mesh.delete(type='VERT')
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    area.spaces[0].cursor_location = mathutils.Vector([0,0,0])
    
    
    
    
    
    
    
    
    

    
    
##\brief Proportionally scales an object, based on a cage.
#\detail For more info on which window, screen, area and region is the right one, check out the start of MESH_FilterCageNode's recalculate() function.
#\returns (None)
#\param ob (Object) The object that is translated (partially).    
#\param cage (Object) The object that acts as "hook" for ob.
#\param falloff (Float) The proportional editing falloff.
#\param scalevec (mathutils.Vector) The vector to scale with. scalevec[0] is the X axis scale factor, and so on.
#\param piv (mathutils.Vector) The rotation's pivot point.
#\param radius (Float) The influence radius.
#\param window (Window) The 3D View window.
#\param screen (Screen) The screen.
#\param area (Area) The area.
#\param region (Region) The region.    
def prop_scale(ob,cage,falloff,scalevec,piv,radius,window,screen,area,region):

    override2 = bpy.context.copy()
    override2[area] = area
    area.spaces[0].pivot_point = "CURSOR"
    area.spaces[0].cursor_location = piv
    
    override = {'window': window, 'screen': screen, 'area': area,'region': region, 'edit_object': ob}




    bpy.context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.hide(unselected=True)
    bpy.ops.mesh.select_all(action = "DESELECT")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    bpy.context.scene.objects.active = cage
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    
    cagegroup = cage.vertex_groups.new("$BG$_PROP_TRANS_CAGE")
    cagegroup_s = cage.vertex_groups.new("$BG$_PROP_TRANS_CAGESEL")
    bpy.ops.object.vertex_group_set_active(group = cagegroup_s.name)
    bpy.ops.object.vertex_group_assign()
    
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = "SELECT")
    
    bpy.ops.object.vertex_group_set_active(group = cagegroup.name)
    bpy.ops.object.vertex_group_assign()
    bpy.ops.mesh.select_all(action = "DESELECT")
    
    bpy.ops.object.vertex_group_set_active(group = cagegroup_s.name)
    
    bpy.ops.object.vertex_group_select()
    
    bpy.ops.mesh.hide(unselected=True)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    utils_OBJ.join([ob,cage])
    
    bpy.context.scene.objects.active = ob
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.transform.resize(override,value=scalevec, constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff=falloff, proportional_size=radius)
    
    bpy.ops.mesh.reveal()
    
    bpy.ops.mesh.select_all(action = "DESELECT")
    
    bpy.ops.object.vertex_group_set_active(group = cagegroup.name)
    
    bpy.ops.object.vertex_group_select()

    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.mesh.delete(type='VERT')
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    area.spaces[0].cursor_location = mathutils.Vector([0,0,0])
    
            
        
        
        
                            
        
            
            
        
            
            
            
    
            
    
            
            
    
            
    
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
        
    
    

    
    
        


    
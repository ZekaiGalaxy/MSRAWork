

# Python Code:
# A,B,C,D are 3d objs, +, -, &, | are operations for NewBodyFeatureOperation, JoinFeatureOperation, CutFeatureOperation, IntersectFeatureOperation
obj = (A + B - C) & D
A.rotation = # 3d rotation matrix
A.extrude = # extrude (low, high)
A.origin = # 3d origin point
A.vertices = [
    # vertices range from 1 to 128 in (x,y)
    (0,63), (8,63), (8,45), (0,45)
]
A.faces[0] = PolyLine(0,1,2,3,4) + Arc(5,6,7,8) + PolyLine(10,11,12,13,14) - Circle(15,16)
# PolyLine means line that connects all the vertices in order, multiple points
# Arc means arc that connects all the vertices in order, 4 points
# Circle means circle that connects all the vertices in order, 2 points
# + means outer face, - means inner face, one face can have > 1 outer face and 0 or 1 inner face
A.faces[1] = Circle(11,12) 

# B,C,D also define in similar ways

return obj


def construct_3d():
    # A,B,C,D are 3d objs, +, -, &, | are operations for 
    # NewBodyFeatureOperation, JoinFeatureOperation, CutFeatureOperation, IntersectFeatureOperation
    obj = (A + B - C) & D
    A.init(
        rotation = # 3d rotation matrix
        extrude = # extrude (low, high)
        origin = # 3d origin point
    )
    A.vertices = [
        # vertices range from 1 to 128 in (x,y)
        (0,63), (8,63), (8,45), (0,45)
    ]
    A.faces[0] = PolyLine(0,1,2,3,4) + Arc(5,6,7,8) + PolyLine(10,11,12,13,14) - Circle(15,16)
    # PolyLine means line that connects all the vertices in order, multiple points
    # Arc means arc that connects all the vertices in order, 4 points
    # Circle means circle that connects all the vertices in order, 2 points
    # + means outer face, - means inner face, one face can have > 1 outer face and 0 or 1 inner face
    A.faces[1] = Circle(11,12)
    # B,C,D also define in similar ways

    return obj
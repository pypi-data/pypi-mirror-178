# Import packages
import joblib
import numpy as np

def vectorField(location, isNode = False, nodeNumber = -1):
    shapes = joblib.load("Data/geometry.sav")
    mesh = joblib.load("Data/mesh.sav")
    solver = joblib.load("Data/solver.sav")
    x = mesh.x
    y = mesh.y
    tri = mesh.conmat
    u = solver.u.copy()
    if isinstance(location, int):
        if shapes[location].shape == 'point':
            nodeNumber = shapes[location].boundaryList[0]
            return(vectorField(np.array(shapes[location].position), True, nodeNumber))
        elif shapes[location-1].shape == 'line' and shapes[location].shape == 'line' and shapes[location+1].shape == 'line':
            l1 = shapes[location-1].boundaryList
            l2 = shapes[location].boundaryList
            l3 = shapes[location+1].boundaryList
            field = []
            for i in range(1,len(l2)-1):
                Exp = (u[l2[i]]-u[l2[i+1]])/(np.sqrt((x[l2[i]] - x[l2[i+1]])**2+(y[l2[i]] - y[l2[i+1]])**2))
                Exn = (u[l2[i-1]]-u[l2[i]])/(np.sqrt((x[l2[i-1]] - x[l2[i]])**2+(y[l2[i-1]] - y[l2[i]])**2))
                Ex = (Exp+Exn)/2
                Eyp = (u[l2[i]]-u[l1[i]])/(np.sqrt((x[l2[i]] - x[l1[i]])**2+(y[l2[i]] - y[l1[i]])**2))
                Eyn = (u[l3[i]]-u[l2[i]])/(np.sqrt((x[l3[i]] - x[l2[i]])**2+(y[l3[i]] - y[l2[i]])**2))
                Ey = (Eyp+Eyn)/2
                field.append([Ex, Ey])

            if solver.name == "magnetostatic":
                thr = 90
                R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
                [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
                for i in range(len(field)):
                    field[i] = np.dot(R,field[i])

            return field
        else:
            raise Exception("Field along the line cannot be obtained for the selected shape", location)
    elif isinstance(location, np.ndarray):
        if isNode:
            field = [0, 0]
            neiElements = mesh.neiElements[nodeNumber]
            elementfields = []
            for element in neiElements:
                A = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                for k in range(3):
                    A[k] = [1, x[tri[element][k]], y[tri[element][k]]]
                b = [[u[tri[element][0]][0]], [u[tri[element][1]][0]], [u[tri[element][2]][0]]]
                X = np.linalg.lstsq(A, b)[0]
                elementfield = [-X[1][0], -X[2][0]]
                elementfields.append(elementfield)
            elementfields = np.array(elementfields)
            field = sum(elementfields)/len(elementfields)
        else:
            field = []
            noOfRows = location.shape[0]
            for i in range(noOfRows):
                field.append([0, 0])

            for j in range(noOfRows):
                isInsideGlobalBoundary = False
                for i in range(len(tri)):
                    if isInside(x[tri[i][0]], y[tri[i][0]], x[tri[i][1]], y[tri[i][1]], x[tri[i][2]], y[tri[i][2]], location[j][0], location[j][1]):
                        theElement = i
                        isInsideGlobalBoundary = True
                        break

                if isInsideGlobalBoundary:
                    A = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                    for k in range(3):
                        A[k] = [1, x[tri[theElement][k]], y[tri[theElement][k]]]
                    b = [[u[tri[theElement][0]][0]], [u[tri[theElement][1]][0]], [u[tri[theElement][2]][0]]]
                    X = np.linalg.lstsq(A, b)[0]
                    field[j] = [-X[1][0], -X[2][0]]
                else:
                    field[j] = [[0, 0]]
                    raise Exception("Position", location[j], "is out of Global Boundary")

        if solver.name == "magnetostatic":
            thr = 90
            R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
            [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
            field = np.dot(R,field)

        return field

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)+ x3 * (y1 - y2))/ 2.0)

def isInside(x1, y1, x2, y2, x3, y3, x, y):
    A = area(x1, y1, x2, y2, x3, y3)
    A1 = area(x, y, x2, y2, x3, y3)
    A2 = area(x1, y1, x, y, x3, y3)
    A3 = area(x1, y1, x2, y2, x, y)
    AT = A1 + A2 + A3
    if(AT < A*1.00001): # To avoid floating point error
        return True
    else:
        return False

def force(shapeNumber):
    shapes = joblib.load("Data/geometry.sav")
    mesh = joblib.load("Data/mesh.sav")
    solver = joblib.load("Data/solver.sav")
    x = mesh.x
    y = mesh.y
    nodeSource = mesh.nodeSource
    inducedNodeSource = solver.bi

    nodes = np.concatenate((shapes[shapeNumber].boundaryList, shapes[shapeNumber].freeList)).astype(int)
    nodeForce = []
    for node in nodes:
        nodeVectorField = vectorField(np.array([x[node], y[node]]), True, node)
        if solver.name == "electrostatic":
            if shapes[shapeNumber].material == 1:
                nodeForce.append(nodeVectorField*nodeSource[node])
            else:
                nodeForce.append(nodeVectorField*inducedNodeSource[node]*solver.physicalConstant)
        elif solver.name == "magnetostatic":
            thr = 90
            R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
            [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
            if shapes[shapeNumber].material == 1:
                nodeForce.append(np.dot(R,nodeVectorField)*nodeSource[node])
            else:
                nodeForce.append(np.dot(R,nodeVectorField)*inducedNodeSource[node]/solver.physicalConstant)

    Force = sum(nodeForce)
    return Force
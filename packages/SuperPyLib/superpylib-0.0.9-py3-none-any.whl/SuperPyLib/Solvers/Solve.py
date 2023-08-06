import numpy as np

def getMatrices(shapes, mesh, solver, solutionName):
    if solver.name == "structural":
        if (solutionName == "stress"):
            solver.getStressMatrices(mesh, shapes)
    else:
        if (solutionName == "approximate"):
            solver.getApproximateMatrices(mesh, shapes)
        elif (solutionName == "numerical"):
            solver.getNumericalMatrix(mesh)
            solver.getLinNumericalMatrix(mesh)
        elif (solutionName == "numericalApproxBound"):
            solver.getApproximateBoundaryMatrices(mesh, shapes)
            solver.getNumericalMatrix(mesh)
            solver.getLinNumericalMatrix(mesh)
        elif (solutionName == "numericalIterBound"):
            solver.getNumericalMatrix(mesh)
            solver.getLinNumericalMatrix(mesh)

def solve(shapes, mesh, solver, solutionName, solverMethod):

    if (solutionName == "approximate"):
        A = solver.Aa.copy()
        b = solver.ba.copy()
        solver.bi = b*0
        if (solverMethod == "Scipy"):
            solver.solveApproximateMatricesScipy(A, b)
        elif (solverMethod == "Numpy"):
            solver.solveApproximateMatricesNumpy(A, b)
        elif (solverMethod == "Sadiku"):
            ui = b.copy()+1
            target = 0.001
            solver.solveApproximateMatricesSadiku(A, ui, b, target)
        
    elif (solutionName == "numerical"):
        ep0 = solver.physicalConstant

        if solver.name == "electrostatic":
            b = mesh.nodeSource.copy()/ep0
        elif solver.name == "magnetostatic":
            b = mesh.nodeSource.copy()*ep0
        elif solver.name == "thermoostatic":
            b = mesh.nodeSource.copy()*ep0

        A = solver.An.copy()

        # Dirichelet Boundary conditions
        for i in range(len(shapes)):
            if len(shapes[i].parent) == 0:
                gs = i
                break

        lbn = shapes[gs].boundaryList
        lbn = lbn.astype(int)
        for i in lbn:
            A[i] = 0*A[i].copy()
            A[i, i] = 1
            b[i] = 0

        if (solverMethod == "Scipy"):
            solver.solveNumericalMatricesScipy(A, b)
        elif (solverMethod == "Numpy"):
            solver.solveNumericalMatricesNumpy(A, b)
        elif (solverMethod == "Sadiku"):
            ui = b.copy()+1
            target = 0.001
            solver.solveNumericalMatricesSadiku(A, ui, b, target)

        bind = np.matmul(solver.AnLin.copy(),solver.un.copy())
        # Get list of material nodes
        matNodes = np.array([])
        for shape in shapes:
            if shape.material != 1:
                matNodes = np.append([matNodes], [shape.boundaryList])
                matNodes = np.append([matNodes], [shape.freeList])

        bi = bind.copy()*0
        matNodes = matNodes.astype(int)
        for node in matNodes:
            bi[node] = bind[node].copy()

        solver.bi = bi.copy()

    elif (solutionName == "numericalApproxBound"):
        Ab = solver.Aab.copy()
        bb = solver.bab.copy()
        solver.solveApproximateBoundaryMatricesScipy(Ab, bb)
        uab = solver.uab.copy()
        ep0 = solver.physicalConstant

        if solver.name == "electrostatic":
            b = mesh.nodeSource.copy()/ep0
        elif solver.name == "magnetostatic":
            b = mesh.nodeSource.copy()*ep0
        A = solver.An.copy()

        # Dirichelet Boundary conditions
        for i in range(len(shapes)):
            if len(shapes[i].parent) == 0:
                gs = i
                break

        lbn = shapes[gs].boundaryList

        for i in lbn:
            A[i] = 0*A[i].copy()
            A[i, i] = 1
            b[i] = uab[i].copy()

        if (solverMethod == "Scipy"):
            solver.solveNumericalMatricesApproxBoundScipy(A, b)
        elif (solverMethod == "Numpy"):
            solver.solveNumericalMatricesApproxBoundNumpy(A, b)
        elif (solverMethod == "Sadiku"):
            ui = b.copy()+1
            target = 0.001
            solver.solveNumericalMatricesApproxBoundSadiku(A, ui, b, target)

        bind = np.matmul(solver.AnLin.copy(),solver.unab.copy())
        # Get list of material nodes
        matNodes = np.array([])
        for shape in shapes:
            if shape.material != 1:
                matNodes = np.append([matNodes], [shape.boundaryList])
                matNodes = np.append([matNodes], [shape.freeList])

        bi = bind.copy()*0
        matNodes = matNodes.astype(int)
        for node in matNodes:
            bi[node] = bind[node].copy()

        solver.bi = bi.copy()

    elif (solutionName == "numericalIterBound"):
        ep0 = solver.physicalConstant

        if solver.name == "electrostatic":
            ba = mesh.nodeSource.copy()/ep0
        elif solver.name == "magnetostatic":
            ba = mesh.nodeSource.copy()*ep0

        A = solver.An.copy()
        bi = ba.copy()*0

        # Get list of material nodes
        matNodes = np.array([])
        for shape in shapes:
            if shape.material != 1:
                matNodes = np.append([matNodes], [shape.boundaryList])
                matNodes = np.append([matNodes], [shape.freeList])

        matNodes = matNodes.astype(int)
        maxIt = 10

        for it in range(maxIt):
            bt = ba + bi
            # Boundary potential due to total sources
            solver.getIterBoundaryMatrices(mesh, shapes, bt)
            Ab = solver.Aib.copy()
            bb = solver.bib.copy()
            solver.solveIterBoundaryMatricesScipy(Ab, bb)
            uib = solver.uib.copy()

            # Dirichelet Boundary conditions
            for i in range(len(shapes)):
                if len(shapes[i].parent) == 0:
                    gs = i
                    break

            lbn = shapes[gs].boundaryList
            
            for i in lbn:
                A[i] = 0*A[i].copy()
                A[i, i] = 1
                ba[i] = uib[i].copy()

            if (solverMethod == "Scipy"):
                solver.solveNumericalMatricesApproxIterBoundScipy(A, ba)
            elif (solverMethod == "Numpy"):
                solver.solveNumericalMatricesApproxIterBoundNumpy(A, ba)
            elif (solverMethod == "Sadiku"):
                ui = b.copy()+1
                target = 0.001
                solver.solveNumericalMatricesApproxIterBoundSadiku(A, ui, ba, target)

            bind = np.matmul(solver.AnLin.copy(),solver.unib.copy())

            for node in matNodes:
                bi[node] = bind[node].copy()

        solver.bi = bi.copy()
        
    solver.findVectorFields(mesh, solver)

def getDistributedSources(shapes, mesh, solver, tn):

    tri = mesh.tri
    x = mesh.rx
    y = mesh.ry
    ep0 = solver.physicalConstant
    # pc = solver.proportionalityConstant
    if solver.name == "electrostatic":
        b = mesh.nodeSource.copy()/ep0
    elif solver.name == "magnetostatic":
        b = mesh.nodeSource.copy()*ep0
    # List of all truncated nodes
    bcopy = b.copy()
    tNodes = np.array([])

    nodeAttNames = mesh.nodeAttNames.copy()
    eleAttNames = mesh.eleAttNames.copy()
    # farnodeAttNames = mesh.farnodeAttNames.copy()

    neiNodesTn = getattr(mesh, nodeAttNames[tn])
    neiElementsTn = getattr(mesh, eleAttNames[tn])
    # farneiNodesTn = getattr(mesh, farnodeAttNames[tn-1])

    for domain in shapes:
        if domain.source != 0:

            if domain.shape == "point":
                domainNode = domain.boundaryList[0]
                tNodes = np.append(tNodes, neiNodesTn[domainNode])

            else:
                domainNodes = domain.boundaryList
                domainNodes = np.append(domainNodes, domain.freeList)
                domainNodes = domainNodes.astype(int)
                for node in domainNodes:
                    tNodes = np.append(tNodes, neiNodesTn[node])

    tNodes = np.unique(tNodes)
    tNodes = tNodes.astype(int)

    # count = 0
    for node in tNodes:

        miniNodes = neiNodesTn[node]
        miniElements = neiElementsTn[node]
        miniTri = tri[miniElements]

        miniNodes = np.sort(miniNodes)

        for j in range(len(miniNodes)):
            if miniNodes[j] == node:
                miniMeshCentreNode = j
                break

        for j in range(len(miniElements)):
            for k in range(3):
                globalNode = miniTri[j,k]

                for l in range(len(miniNodes)):
                    if globalNode == miniNodes[l]:
                        miniTri[j,k] = l
                        break

        minix = x[miniNodes].copy()
        miniy = y[miniNodes].copy()

        mne = len(miniElements)
        mnn = len(minix)

        miniA = np.zeros([mnn, mnn])
        minib = np.zeros([mnn,1])

        for i in range(mne):

            # 0-1 edge
            k = 0
            l = 1
            Ex = 0
            Ey = 0

            for mnode in range(len(miniNodes)):
                px = minix[mnode].copy()
                py = miniy[mnode].copy()
                Rx = (minix[miniTri[i,k]] + minix[miniTri[i,l]])/2 - px
                Ry = (miniy[miniTri[i,k]] + miniy[miniTri[i,l]])/2 - py
                Ex = Ex + b[miniNodes[mnode]]/(2*np.pi)*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                Ey = Ey + b[miniNodes[mnode]]/(2*np.pi)*Ry/(np.sqrt(Rx**2 + Ry**2))**2

            rx = minix[miniTri[i,l]] - minix[miniTri[i,k]]
            ry = miniy[miniTri[i,l]] - miniy[miniTri[i,k]]
            Er = np.dot([Ex[0], Ey[0]], [rx, ry]/np.sqrt(rx**2+ry**2))
            miniA[miniTri[i,k], miniTri[i,k]] = miniA[miniTri[i,k], miniTri[i,k]] +1
            miniA[miniTri[i,k], miniTri[i,l]] = -1
            minib[miniTri[i,k]]           = minib[miniTri[i,k]] + Er*np.sqrt(rx**2+ry**2)

            # 1-2 edge
            k = 1
            l = 2
            Ex = 0
            Ey = 0

            for mnode in range(len(miniNodes)):
                px = minix[mnode].copy()
                py = miniy[mnode].copy()
                Rx = (minix[miniTri[i,k]] + minix[miniTri[i,l]])/2 - px
                Ry = (miniy[miniTri[i,k]] + miniy[miniTri[i,l]])/2 - py
                Ex = Ex + b[miniNodes[mnode]]/(2*np.pi)*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                Ey = Ey + b[miniNodes[mnode]]/(2*np.pi)*Ry/(np.sqrt(Rx**2 + Ry**2))**2

            rx = minix[miniTri[i,l]] - minix[miniTri[i,k]]
            ry = miniy[miniTri[i,l]] - miniy[miniTri[i,k]]
            Er = np.dot([Ex[0], Ey[0]], [rx, ry]/np.sqrt(rx**2+ry**2))
            miniA[miniTri[i,k], miniTri[i,k]] = miniA[miniTri[i,k], miniTri[i,k]] +1
            miniA[miniTri[i,k], miniTri[i,l]] = -1
            minib[miniTri[i,k]]           = minib[miniTri[i,k]] + Er*np.sqrt(rx**2+ry**2)

            # 2-0 edge
            k = 2
            l = 0
            Ex = 0
            Ey = 0

            for mnode in range(len(miniNodes)):
                px = minix[mnode].copy()
                py = miniy[mnode].copy()
                Rx = (minix[miniTri[i,k]] + minix[miniTri[i,l]])/2 - px
                Ry = (miniy[miniTri[i,k]] + miniy[miniTri[i,l]])/2 - py
                Ex = Ex + b[miniNodes[mnode]]/(2*np.pi)*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                Ey = Ey + b[miniNodes[mnode]]/(2*np.pi)*Ry/(np.sqrt(Rx**2 + Ry**2))**2

            rx = minix[miniTri[i,l]] - minix[miniTri[i,k]]
            ry = miniy[miniTri[i,l]] - miniy[miniTri[i,k]]
            Er = np.dot([Ex[0], Ey[0]], [rx, ry]/np.sqrt(rx**2+ry**2))
            miniA[miniTri[i,k], miniTri[i,k]] = miniA[miniTri[i,k], miniTri[i,k]] +1
            miniA[miniTri[i,k], miniTri[i,l]] = -1
            minib[miniTri[i,k]]           = minib[miniTri[i,k]] + Er*np.sqrt(rx**2+ry**2)

        solver.solveminiNumpy(miniA, minib)

        miniu = solver.miniu
        solver.getMiniLinNumericalMatrix(minix, miniy, miniTri)
        miniAn = solver.miniAn

        minibnshould = np.matmul(miniAn, miniu)
        bcopy[node] = minibnshould[miniMeshCentreNode]

    solver.bn = b.copy()
    solver.bdss = bcopy.copy()
    mesh.nodeSourceDss = bcopy.copy()*ep0

def solveDSS(shapes, mesh, solver, solutionName, solverMethod):

    if (solutionName == "approximate"):
        raise Exception("DSS does not support approximate solution")

    elif (solutionName == "numerical"):
        #ep0 = solver.physicalConstant

        b = solver.bdss.copy()
        A = solver.An.copy()

        # Dirichelet Boundary conditions
        lbn = shapes[0].boundaryList

        for i in lbn:
            A[i] = 0*A[i].copy()
            A[i, i] = 1
            b[i] = 1

        if (solverMethod == "Scipy"):
            solver.solveNumericalMatricesScipy(A, b)
        elif (solverMethod == "Numpy"):
            solver.solveNumericalMatricesNumpy(A, b)
        elif (solverMethod == "Sadiku"):
            ui = b.copy()+1
            target = 0.001
            solver.solveNumericalMatricesSadiku(A, ui, b, target)

    elif (solutionName == "numericalApproxBound"):
        Ab = solver.Aab.copy()
        bb = solver.bab.copy()
        solver.solveApproximateBoundaryMatricesScipy(Ab, bb)
        uab = solver.uab.copy()

        # ep0 = solver.physicalConstant

        b = solver.bdss
        A = solver.An.copy()

        # Dirichelet Boundary conditions
        lbn = shapes[0].boundaryList

        for i in lbn:
            A[i] = 0*A[i].copy()
            A[i, i] = 1
            b[i] = uab[i].copy()

        if (solverMethod == "Scipy"):
            solver.solveNumericalMatricesApproxBoundScipy(A, b)
        elif (solverMethod == "Numpy"):
            solver.solveNumericalMatricesApproxBoundNumpy(A, b)
        elif (solverMethod == "Sadiku"):
            ui = b.copy()+1
            target = 0.001
            solver.solveNumericalMatricesApproxBoundSadiku(A, ui, b, target)

    elif (solutionName == "numericalIterBound"):
        ep0 = solver.physicalConstant

        if solver.name == "electrostatic":
            ba = mesh.nodeSource.copy()/ep0
        elif solver.name == "magnetostatic":
            ba = mesh.nodeSource.copy()*ep0

        bdss = solver.bdss.copy()

        A = solver.An.copy()
        bi = ba.copy()*0

        # Get list of material nodes
        matNodes = np.array([])
        for domain in shapes:
            if domain.material != 1:
                matNodes = np.append([matNodes], [domain.boundaryList])
                matNodes = np.append([matNodes], [domain.freeList])

        matNodes = matNodes.astype(int)

        maxIt = 10

        for it in range(maxIt):
            bt = ba + bi

            # Boundary potential due to total sources
            solver.getIterBoundaryMatrices(mesh, shapes, bt)
            Ab = solver.Aib.copy()
            bb = solver.bib.copy()
            solver.solveIterBoundaryMatricesScipy(Ab, bb)
            uib = solver.uib.copy()

            # Dirichelet Boundary conditions
            lbn = shapes[0].boundaryList

            for i in lbn:
                A[i] = 0*A[i].copy()
                A[i, i] = 1
                bdss[i] = uib[i].copy()

            if (solverMethod == "Scipy"):
                solver.solveNumericalMatricesApproxIterBoundScipy(A, bdss)
            elif (solverMethod == "Numpy"):
                solver.solveNumericalMatricesApproxIterBoundNumpy(A, bdss)
            elif (solverMethod == "Sadiku"):
                ui = b.copy()+1
                target = 0.001
                solver.solveNumericalMatricesApproxIterBoundSadiku(A, ui, bdss, target)

            bind = np.matmul(solver.AnLin.copy(),solver.unib.copy())

            for node in matNodes:
                bi[node] = bind[node].copy()
            
        solver.bi = bi.copy()

    solver.findVectorFields(mesh, solver)

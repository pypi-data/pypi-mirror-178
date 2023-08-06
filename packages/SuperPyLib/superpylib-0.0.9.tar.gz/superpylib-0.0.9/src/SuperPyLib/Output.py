# Import packages
import joblib
from . import PlotUtils
from . import Mesh
from .Solvers import Solve

def mesh(par, meshingMethod = "triangle", maxAngle = "", maxArea = "", crse = 1, dpi = 300):
    if par == []:
        geometry = joblib.load("Data/geometry.sav")
    else:
        stri = f'Data/geometry_{par}.sav'
        geometry = joblib.load(stri)

    Mesh.prepareGeometryForMeshing(geometry)
    Mesh.generateNodes(geometry, meshingMethod, maxAngle, maxArea, crse)
    mesh = Mesh.createMesh(geometry)

    if dpi < 300:
        dpi = 300

    if par == []:
        joblib.dump(geometry, "Data/geometry.sav")
        joblib.dump(mesh, "Data/mesh.sav")
        PlotUtils.plotMesh(geometry, mesh, "Figures/2_Mesh.png", dpi)
    else: 
        stri = f'Data/geometry_{par}.sav'
        joblib.dump(geometry, stri)
        stri = f'Data/mesh_{par}.sav'
        joblib.dump(mesh, stri)
        stri = f'Figures/2_Mesh_{par}.png'
        PlotUtils.plotMesh(geometry, mesh, stri, dpi)


def assigedSources(par, dpi):
    if par == []:
        shapes = joblib.load("Data/geometry.sav")
        mesh = joblib.load("Data/mesh.sav")
        solver = joblib.load("Data/solver.sav")
    else:
        stri = f'Data/geometry_{par}.sav'
        shapes = joblib.load(stri)
        stri = f'Data/mesh_{par}.sav'
        mesh = joblib.load(stri)
        stri = f'Data/solver_{par}.sav'
        solver = joblib.load(stri)

    Mesh.assignSources(shapes, mesh)

    if par == []:
        joblib.dump(mesh, "Data/mesh.sav")
        PlotUtils.plotSources(mesh, solver, "Figures/3_Sources.png", dpi)
    else:
        stri = f'Data/mesh_{par}.sav'
        joblib.dump(mesh, stri)
        stri = f'Figures/3_Sources_{par}.png'
        PlotUtils.plotSources(mesh, solver, stri, dpi)
    

def assigedMaterials(par, dpi):
    if par == []:
        shapes = joblib.load("Data/geometry.sav")
        mesh = joblib.load("Data/mesh.sav")
        solver = joblib.load("Data/solver.sav")
    else:
        stri = f'Data/geometry_{par}.sav'
        shapes = joblib.load(stri)
        stri = f'Data/mesh_{par}.sav'
        mesh = joblib.load(stri)
        stri = f'Data/solver_{par}.sav'
        solver = joblib.load(stri)

    Mesh.assignMaterials(shapes, mesh)
    
    if par == []:
        joblib.dump(mesh, "Data/mesh.sav")
        PlotUtils.plotMaterials(mesh, solver, "Figures/4_Materials.png", dpi)
    else:
        stri = f'Data/mesh_{par}.sav'
        joblib.dump(mesh, stri)
        stri = f'Figures/4_Materials_{par}.png'
        PlotUtils.plotMaterials(mesh, solver, stri, dpi)


def solution(par, solutionName = "numerical", solverMethod = "Scipy", withDifference = False, withField = False, dpi = 300):
    if par == []:
        shapes = joblib.load("Data/geometry.sav")
        mesh = joblib.load("Data/mesh.sav")
        solver = joblib.load("Data/solver.sav")
    else:
        stri = f'Data/geometry_{par}.sav'
        shapes = joblib.load(stri)
        stri = f'Data/mesh_{par}.sav'
        mesh = joblib.load(stri)
        stri = f'Data/solver_{par}.sav'
        solver = joblib.load(stri)

    Solve.getMatrices(shapes, mesh, solver, solutionName)
    Solve.solve(shapes, mesh, solver, solutionName, solverMethod)
    if dpi < 300:
        dpi = 300
        
    showSolution(par, mesh, solver, solutionName, withField, dpi)
    if withDifference:
        showDifference(par, mesh, solver, solutionName, dpi)

    if par == []:
        joblib.dump(mesh, "Data/mesh.sav")
        joblib.dump(solver, "Data/solver.sav")
    else:
        stri = f'Data/mesh_{par}.sav'
        joblib.dump(mesh, stri)
        stri = f'Data/solver_{par}.sav'
        joblib.dump(solver, stri)


def showSolution(par, mesh, solver, solutionName, withField, dpi):
    if (solutionName == "approximate"):
        solution = solver.ua
        PlotUtils.plotSolution(par, mesh, solver, solution, solutionName, withField, dpi)
    elif (solutionName == "numerical"):
        solution = solver.un
        PlotUtils.plotSolution(par, mesh, solver, solution, solutionName, withField, dpi)
    elif (solutionName == "numericalApproxBound"):
        solution = solver.unab
        PlotUtils.plotSolution(par, mesh, solver, solution, solutionName, withField, dpi)
    elif (solutionName == "numericalIterBound"):
        solution = solver.unib
        PlotUtils.plotSolution(par, mesh, solver, solution, solutionName, withField, dpi)

def showDifference(par, mesh, solver, solutionName, dpi):
    pass

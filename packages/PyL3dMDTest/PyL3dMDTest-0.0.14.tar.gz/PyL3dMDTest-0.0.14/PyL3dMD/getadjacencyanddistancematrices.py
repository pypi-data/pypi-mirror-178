# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 09:15:31 2022

@author: pawan
"""
from math import inf
import numpy as np

"""
It removes bonds of hydrogen atoms from a molecule using mass of atom
"""
def removehydrogen(masses, bonds):
    # Idenstify hydrogen atoms to deleted
    idxdeletexyz = [i for i, masses in enumerate(masses) if masses < 1.2]
    if len(idxdeletexyz)>=1:
        # Update bonds table accordingly - Numpy check if elements of array belong to another array
        check = np.isin(bonds, np.array(idxdeletexyz)+1)
        idxkeepbond = [i for i in range(len(check)) if np.all(check[i,:] == [False, False])]
        bondheavy = bonds[idxkeepbond,:] # Bonds between only heavy atoms
        
    else:
        bondheavy = bonds
    return bondheavy


"""
Modified matrix-matrix multiplication of sqaure matrices
"""
# Assume M and N are both square (size x size) matrices 
# Ref - https://imada.sdu.dk/~rolf/Edu/DM534/E16/IntroCS2016-final.pdf
def multModSquareMatrices(M,N):
    size = len(M)
    result = [[inf for x in range(size)] for y in range(size)]

    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] = min(result[i][j], M[i][k] + N[k][j])
                
    return result


"""
Calculate adjacency matrix from bonds
"""
def caladjacencymatrix(bonds):      
    edge = bonds-1
    edge_u = edge[:,0]
    edge_v = edge[:,1]

    # Number of nodes
    n = np.max(edge)+1

    # create empty adjacency lists - one for each node
    # adjList = [[] for k in range(n)]

    # adjacency matrix - initialize with 0
    adjMatrix = np.zeros((n,n))

    # scan the arrays edge_u and edge_v
    for i in range(len(edge_u)):
        u = edge_u[i]
        v = edge_v[i]
        # adjList[u].append(v)
        # adjList[v].append(u)
        adjMatrix[u][v] = 1
        adjMatrix[v][u] = 1
    return adjMatrix

         
"""
Calculate edge or 2D distance matrix from adjacency matrix
"""
def caldistancematrix(adjMatrix):    
    # Create Edge Wight Matrix with weightage of 1 for all edge
    W = np.zeros((len(adjMatrix),len(adjMatrix)))
    for i in range(len(adjMatrix)):
        for j in range(len(adjMatrix)):
            if i==j:
                W[i,j] = 0
            else:
                if adjMatrix[i,j] != 1:
                    W[i,j] = inf
                else:
                    W[i,j] = 1
                    
    # Compute the distance matrix iteratively by computation of W^2, W^3, ..., W^5
    R = W
    for i in range(2,len(adjMatrix)):
        R = multModSquareMatrices(R,W)
    disMatrix = np.array(R)
    return disMatrix


"""
Get adjacency and distnace matrices from rdkit
"""
def getadjANDdismatrices(eachMolsMass, eachMolsBonds):
    eachMolsAdjMat = {}
    eachMolsDisMat = {}
    numMols = len(eachMolsBonds)
    for i in range(numMols):
        bonds = eachMolsBonds[i]
        masses = eachMolsMass[i]
        bondheavy = removehydrogen(masses, bonds)
        eachMolsAdjMat[i] = caladjacencymatrix(bondheavy)        # Get 2D adjaceny matrix
        eachMolsDisMat[i] = caldistancematrix(eachMolsAdjMat[i])    # Get 2D distance matrix
    return (eachMolsAdjMat, eachMolsDisMat)
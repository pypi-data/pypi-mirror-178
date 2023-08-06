# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 08:19:43 2022

@author: pawan
"""
"""
GETAWAY Descriptors - Geometry, topology, and atom-weights assembly (GETAWAY) descriptors
"""

from math import inf
import numpy as np

"""
count the number of occurrences
"""
def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count


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


def calgeometricdistancematrix(M):
    """
    Calculate Euclidean Distance of atoms in a molecule - (numAtoms x numAtoms)
        G = Geometric Distance Matrix
        Ginv = Inverse Geometric Distance Matrix
        Gx = Euclidean distance of atoms in a molecule in x-direction
        Gy = Euclidean distance of atoms in a molecule in y-direction
        Gz = Euclidean distance of atoms in a molecule in z-direction
    """
    onesMat = np.ones([len(M),len(M)])
    Gx = onesMat*M[:,0]-np.transpose(onesMat*M[:,0])
    Gy = onesMat*M[:,1]-np.transpose(onesMat*M[:,1])
    Gz = onesMat*M[:,2]-np.transpose(onesMat*M[:,2])
    G = np.sqrt(Gx**2 + Gy**2 + Gz**2)
    return G


def calmolecularinfluencematrix(M):
    """
    calculate the molecular influence matrix (H) using the 3D cartesian coordinates of a molecule.
       H = M*pinv(M'*M)*M' - (numAtoms x numAtoms)
       leverage = diag(H)  - (numAtoms x 1)     
    """
    H = np.matmul(np.matmul(M,np.linalg.pinv(np.matmul(np.transpose(M),M))),np.transpose(M))
    return H


def calleverage(H):
    """
    calculate leverage using the the molecular influence matrix (H) of a molecule.
       leverage = diag(H)  - (numAtoms x 1)     
    """
    leverage = np.diagonal(H)
    return leverage


def calinfluencedistancematrix(G, leverage):
    """
    Calculation of the Influence Distance Matrix (R) - (numAtoms x numAtoms)
    """
    nA = len(leverage)
    R = np.zeros((nA,nA))
    for i in range(nA):
        for j in range(nA):
            if i != j:
                R[i,j] = np.sqrt(leverage[i]*leverage[j])/G[i,j]
    return R


def calinversegeometricdistancematrix(G):
    """
    Calculate Euclidean Distance of atoms in a molecule - (numAtoms x numAtoms)
        G = Geometric Distance Matrix (numAtoms x numAtoms)
        Ginv = Inverse Geometric Distance Matrix (numAtoms x numAtoms)
        Ginv2 = Squared inverse Geometric Distance Matrix (numAtoms x numAtoms)
    """
    Ginv = np.zeros(np.shape(G))
    Ginv2 = np.zeros(np.shape(G))
    for i in range(len(G)):
        for j in range(len(G)):
            if i == j:
                Ginv[i,j] = 0
                Ginv2[i,j] = 0
            else:
                Ginv[i,j] = 1/G[i,j]
                Ginv2[i,j] = 1/(G[i,j]**2)
    return (Ginv, Ginv2)


##################################################################################################################################
# ############### GETAWAY descriptors based on autocorrelation functions ######################
"""
Calculate GETAWAY HATS indexes
"""
def calgetawayhatsindexes(disMat, leverage, propertyValue, propertyName):
    n = 20
    step = int(1) # step size [Å]
    lag = np.array([i for i in range(1,n+1)]).astype(int)*step
    nA = len(leverage)

    getawayHATS = {}
    getawayHATS['getawayHATS'+propertyName+str(0)] = np.sum((propertyValue*leverage)**2)
    for kkk in lag:
        temp = 0.0
        for i in range(0,nA-1):
            for j in range(i+1,nA):  
                if disMat[i,j] == kkk:
                    temp = temp + (propertyValue[i]*leverage[i])*(propertyValue[j]*leverage[j])
                else:
                    temp= temp + 0.0     
        getawayHATS['getawayHATS'+propertyName+str(kkk)] = temp
        
    # HATS total index
    temp = np.array(list(getawayHATS.values()))
    temp2 = 0.0
    for i in range(0,int(np.max(disMat))):
        temp2 = temp2+temp[i+1]
    getawayHATS['getawayHATST'+propertyName] = temp[0] + 2*temp2 
    return getawayHATS


"""
Calculate GETAWAY H indexes
"""
def calgetawayhindexes(disMat, H, leverage, propertyValue, propertyName):
    n = 20
    step = int(1) # step size [Å]
    lag = np.array([i for i in range(1,n+1)]).astype(int)*step
    nA = len(leverage)

    getawayH = {}
    getawayH['getawayH'+propertyName+str(0)] = np.sum(leverage*propertyValue**2)
    for kkk in lag:
        temp = 0.0
        for i in range(0,nA-1):
            for j in range(i+1,nA):  
                if disMat[i,j] == kkk and H[i,j]>0:
                    temp = temp + propertyValue[i]*propertyValue[j]*H[i,j]
                else:
                    temp= temp + 0.0     
        getawayH['getawayH'+propertyName+str(kkk)] = temp
        
    # H total index
    temp = np.array(list(getawayH.values()))
    temp2 = 0.0
    for i in range(0,int(np.max(disMat))):
        temp2 = temp2+temp[i+1]
    getawayH['getawayHT'+propertyName] = temp[0] + 2*temp2 
    return getawayH


"""
Calculate GETAWAY R indexes
"""
def calgetawayrindexes(disMat, R, propertyValue, propertyName):
    n = 20
    step = int(1) # step size [Å]
    lag = np.array([i for i in range(1,n+1)]).astype(int)*step
    nA = len(disMat)
    
    junk = []
    Rkmax = []
    getawayR = {}
    for kkk in lag:
        temp = 0.0
        Rk = []
        for i in range(0,nA-1):
            for j in range(i+1,nA):  
                if disMat[i,j] == kkk: 
                    temp = temp + R[i,j]*(propertyValue[i]*propertyValue[j])
                    Rk.append(R[i,j]*(propertyValue[i]*propertyValue[j]))
                else:
                    temp= temp + 0.0
        getawayR['getawayR'+propertyName+str(kkk)] = temp
        junk.append(temp)    
        # Maximal R indexes
        if len(Rk) == 0:
            Rkmax.append(0)
            getawayR['getawayRmax'+propertyName+str(kkk)] = 0
        else:
            Rkmax.append(np.max(Rk))
            getawayR['getawayRmax'+propertyName+str(kkk)] = np.max(Rk)
    
    # Maximal R total index
    getawayR['getawayRTmax'+propertyName] = np.max(Rkmax)
    
    # R total index
    temp = np.array(junk)
    temp2 = 0.0
    for i in range(0,int(np.max(disMat))):
        temp2 = temp2+temp[i]
    getawayR['getawayRT'+propertyName] = 2*temp2   
    return getawayR



##################################################################################################################################

"""
Get 3D GETAWAY descriptors for all atomic weights/properties
"""
def getgetawayhatsindexes(*args):
    """ INPUTS
    0 ; Geometric or 3D distnace matrix (G)
    1 : atomic charge (c)
    2 : atomic mass (m)
    3 : van der Waals vloume (V)
    4 : Sanderson electronegativity (En)
    5 : atomic polarizability in 10e-24 cm3 (P)
    6 : ionization potential in eV (IP)
    7 : electron affinity in eV (EA)
    """
     
    propertyNames = ['c','m','V','En','P','IP','EA']
    GETAWAY = {}
    
    xyz = args[0]
    masses = args[1]
    bonds = args[2]
    
    
    bondheavy = removehydrogen(masses, bonds)
    adjMat = caladjacencymatrix(bonds)          # Get 2D adjaceny matrix
    disMat = caldistancematrix(adjMat)          # Get 2D distance matrix
    G = calgeometricdistancematrix(xyz)
    Ginv, Ginv2 = calinversegeometricdistancematrix(G)
    H = calmolecularinfluencematrix(xyz)
    leverage = calleverage(H)
    R = calinfluencedistancematrix(G, leverage)



    # Geometric mean of the leverage magnitude
    multiply = 1
    for i in leverage:
        multiply = (multiply)*(i)
        
    HGM = ((multiply)**(1/len(leverage)))*100

    # Row sum of influence distnace matrix
    VSi = np.sum(R, axis=1)
    nA = len(R)

    # # Total information content on the leverage equality
    # A0 = len(massheavy) # number of non-hydrogen atoms
    # Ng = # number of atoms with the same leverage value
    A0 = len(bondheavy)
    uniqueleverage = np.unique(leverage[0:A0])
    Ng = []
    for i in uniqueleverage:
        Ng.append(countX(leverage, i))
        
    temp = A0*np.log2(A0) - np.sum(np.array(Ng)*np.log2(Ng))
    ITH = temp


    # Standardized information content on the leverage equality
    ISH = ITH/A0*np.log2(A0)


    # Mean information content on the leverage magnitude
    HIC1 = -1*np.sum((leverage/1.0)*(np.log2(leverage/1.0))) # For linear molecule
    HIC2 = -1*np.sum((leverage/2.0)*(np.log2(leverage/2.0))) # For Planar molecule
    HIC3 = -1*np.sum((leverage/3.0)*(np.log2(leverage/3.0))) # For Non-Planar molecule

    # Average row sum of the influence/distance matrix
    RARS = np.sum(R)/nA

    # R-connectivity index
    temp = 0.0
    for i in range(nA):
        for j in range(nA):
            temp = temp + adjMat[i,j]*np.sqrt(VSi[i]*VSi[j])
    RCON = temp

    # R-matrix leading eigenvalue
    REIG = np.max(np.linalg.eig(R)[0])

    GETAWAY['getawayHGM'] = HGM
    GETAWAY['getawayITH'] = ITH
    GETAWAY['getawayISH'] = ISH
    GETAWAY['getawayHIC1'] = HIC1
    GETAWAY['getawayHIC2'] = HIC2
    GETAWAY['getawayHIC3'] = HIC3
    GETAWAY['getawayRARS'] = RARS
    GETAWAY['getawayRCON'] = RCON
    GETAWAY['getawayREIG'] = REIG
    
    
    for i in range(len(propertyNames)):
        GETAWAY.update(calgetawayhatsindexes(disMat, leverage, args[i+3], propertyNames[i]))
        
    for i in range(len(propertyNames)):
        GETAWAY.update(calgetawayhindexes(disMat, H, leverage, args[i+3], propertyNames[i]))
        
    for i in range(len(propertyNames)):
        GETAWAY.update(calgetawayrindexes(disMat, R, args[i+3], propertyNames[i]))
        
    return GETAWAY









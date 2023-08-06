# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:13:03 2022

@author: pawan
"""
import numpy as np
import pandas as pd
import time
import multiprocessing as mp

from . import getatomicproperties
from . import getinfofromlammpsdatafile
from . import getadjacencyanddistancematrices
from . import getinfofromlammpstrajfile
from . import rdf
from . import morse
from . import moreaubroto
from . import geary
from . import moran
from . import whim
from . import getaway
from . import cpsa
from . import geometricdescriptors
from . import topologyconnectivity3Ddescriptors

# from getinfofromlammpsdatafile import getalldatafileinfo
# from getinfofromlammpsdatafile import arragebymolecule

# from getadjacencyanddistancematrices import getadjANDdismatrices

# from getinfofromlammpstrajfile import getcolumns
# from getinfofromlammpstrajfile import readlammpsdumpfile
# from getinfofromlammpstrajfile import getboxboundariesANDlengths

# from rdf import getrdfdescriptors
# from morse import getmorsedescriptors
# from moreaubroto import getmoreaubrotodescriptors
# from geary import getgearyindices
# from moran import getmorandescriptors
# from whim import getwhimdescriptors
# from getaway import getgetawayhatsindexes
# from cpsa import getcpsadescriptors
# from geometricdescriptors import calgeometricdescriptors
# from topologyconnectivity3Ddescriptors import caltopologyconnectivitydescriptors

"""
############################################ ADDITIONAL FUNCTIONS ###########################################
"""
def caldensity(massBox, volBox):
    """
    simulation calculated density of the fluid [g/cc]
    """
    NA = 6.0221408e+23              # Avogadro's number [1/mol]
    volBoxcc = volBox*1.0E-24       # volume of the simulation box [cc]
    
    # Simulation-calculated density [g/cc]
    rho = (massBox/volBoxcc)*(1.0/NA) 
    return rho

def calgeometricdistancematrix(xyz):
    """
    Calculate Euclidean Distance of atoms in a molecule - (numAtoms x numAtoms)
    """
    onesMat = np.ones([len(xyz),len(xyz)])
    Gx = onesMat*xyz[:,0]-np.transpose(onesMat*xyz[:,0])
    Gy = onesMat*xyz[:,1]-np.transpose(onesMat*xyz[:,1])
    Gz = onesMat*xyz[:,2]-np.transpose(onesMat*xyz[:,2])
    
    # Geometric Distance Matrix
    G = np.sqrt(Gx**2 + Gy**2 + Gz**2)
    return G


def Descriptors(datafilename, dumpfilename, fromWhichFrame, toWhichFrame, FrameInterval):
    global caldescriptors
    # # Check if number of workers are provided bt user or not
    # if len(args)>1:
    #     poolCount = int(args[1])
    # else:
    #     poolCount = 1
    
    # Get the number of processors available in system
    poolCount = mp.cpu_count()
    
    # Write the number of workers to output
    print ("Started pool with "+str(poolCount)+" workers.")
    
    t1 = time.perf_counter() 
    
    
    
    
    """
    ############################################ DEFINE/PROVIDE REQUIRED INFORMATION ###########################################
    """
    # locationDataFile = './'
    # locationDumpFile = './'
    # datafilename = locationDataFile + 'methylpentaneAA.txt'
    # dumpfilename = locationDumpFile + 'NPT_w_methylpentaneAA_T100CP1atm.lammpstrj'
    # fromWhichFrame = 0
    # toWhichFrame = 1
    # FrameInterval = 1
    # numCores = 4
    
    
    
    """
    ######################################## GET ALL INFORMATIONS FROM LAMMPS DATA FILE ###########################################
    """
    idAtoms, idMols, atomTypes, atomCharges, atomMasses, atomSection, bondSection =  getinfofromlammpsdatafile.getalldatafileinfo(datafilename)
    eachMolsNumIdx,eachMolsIdx,eachMolsMass,eachMolsCharge,eachMolsBonds,eachMolsAngles,eachMolsDihedrals = getinfofromlammpsdatafile.arragebymolecule(idAtoms, idMols, atomMasses, atomCharges, bondSection)
    numAtoms = len(idAtoms) # num of atoms in the simulation box        
    numMols = max(idMols)   # num of molecules in the simulation box
    
    
    
    """
    ######################################## GET ALL ATOMIC PROPERTIES #############################################################
    """
    _,_,_,_,eachMolsRc,eachMolsm,eachMolsV,eachMolsEn,eachMolsalapha,eachMolsIP,eachMolsEA = getatomicproperties.getatomicproperties(atomMasses,eachMolsIdx)
    
    
    
    """
    ######################################## Get adjacency and distnace matrices from rdkit ########################################
    """
    eachMolsAdjMat, eachMolsDisMat = getadjacencyanddistancematrices.getadjANDdismatrices(eachMolsMass, eachMolsBonds)
    
    
    
    """
    ######################################## GET ALL INFORMATIONS FROM LAMMPS DUMP FILE ############################################
    """
    dataXdim, dataYdim, dataZdim, boxlengths = getinfofromlammpstrajfile.getboxboundariesANDlengths(dumpfilename)
    colid, colmol, coltype, colx, coly, colz, needToUnwrap = getinfofromlammpstrajfile.getcolumns(dumpfilename)
    datadump, datadumpdict, nframes = getinfofromlammpstrajfile.readlammpsdumpfile(dumpfilename, numAtoms, colid, colmol, coltype, colx, coly, colz, needToUnwrap, boxlengths)
    
    
    
    """
    ######################################## DENSITY OF THE SIMULATION BOX AT EACH TIME FRAMES ########################################
    """
    rho = []
    massBox = np.sum(atomMasses) # Sum of mass of all atoms in the simulation box 
    # for i in range(nframes):
    for i in range(fromWhichFrame,toWhichFrame,FrameInterval):
        # Length of the simulation box at a time frame
        lx = boxlengths[i,0]
        ly = boxlengths[i,1]
        lz = boxlengths[i,2]
        
        # Volume of the simulation box at a time frame
        volBox = lx*ly*lz                          # [ÅxÅxÅ]
    
        # Density at a time frame
        rho.append(caldensity(massBox, volBox))    # [g/cc]
        
        
    
    """
    ######################################## CALCULATE DESCRIPTORS OF ALL MOLECULES AT ALL TIME FRAMES ########################################
    """
    def caldescriptors(i,j):
        mass = eachMolsMass[i]
        charge = eachMolsCharge[i]
        bond = eachMolsBonds[i]
        angle = eachMolsAngles[i]
        dihedral = eachMolsDihedrals[i]
        disMat = eachMolsDisMat[i]
        adjMat = eachMolsAdjMat[i]
        xyz = datadumpdict[j][i][:,3:6]
        density = rho[j]
        
        # Atomic properties
        apRc = eachMolsRc[i]
        apm = eachMolsm[i]
        apV = eachMolsV[i]
        apEn = eachMolsEn[i]
        apalapha = eachMolsalapha[i]
        apIP = eachMolsIP[i]
        apEA = eachMolsEA[i]
        
        
        # calculate Geometric matrix
        G = calgeometricdistancematrix(xyz)  
        
        # Calculate all descriptors
        RDF = rdf.getrdfdescriptors(G, charge, apm, apV, apEn, apalapha, apIP, apEA)            # 30*8 = 240
        MoRSE = morse.getmorsedescriptors(G, charge, apm, apV, apEn, apalapha, apIP, apEA)        # 30*8 = 240
        ATS = moreaubroto.getmoreaubrotodescriptors(G, charge, apm, apV, apEn, apalapha, apIP, apEA)    # 30*7 = 210
        GATS = geary.getgearyindices(G, charge, apm, apV, apEn, apalapha, apIP, apEA)             # 30*7 = 210
        MATS = moran.getmorandescriptors(G, charge, apm, apV, apEn, apalapha, apIP, apEA)         # 30*7 = 210
        WHIM = whim.getwhimdescriptors(xyz, charge, apm, apV, apEn, apalapha, apIP, apEA)        # 14*8 = 112
        GETAWAY = getaway.getgetawayhatsindexes(xyz, mass, bond, charge, apm, apV, apEn, apalapha, apIP, apEA)        # 14*8 = 112
        #CPSA = getcpsadescriptors(xyz, charge, apRc) # 30
        
        GMdes, DDMdes = geometricdescriptors.calgeometricdescriptors(xyz, mass, charge, bond, angle, dihedral, density, disMat) # GMdes = 85, DDMdes = 10
        TCdes = topologyconnectivity3Ddescriptors.caltopologyconnectivitydescriptors(xyz, mass, bond, angle, dihedral, adjMat, disMat) # TCdes = 27
        
        others = {}
        others['molecule'] = i+1
        others['Timeframe'] = j
        others['rho'] = density
        
        # Combine all dictionaries into a single dictionary to return/store
        res = {**others, **GMdes, **DDMdes, **TCdes, **RDF, **MoRSE, **ATS, **GATS, **MATS, **WHIM, **GETAWAY} # , **CPSA
        return res
    
     
    # entry point for the program
    if __name__ == '__main__':
        
        # create the process pool
        with mp.Pool(processes = poolCount) as pool:
            
            # prepare arguments
            items = []
            for i in range(numMols):
                # for j in range(nframes):
                for j in range(fromWhichFrame,toWhichFrame,FrameInterval):
                    items.append((i,j)) 
            
            ans = []
            # call the same function with different data in parallel
            for result in pool.starmap(caldescriptors, items):
               
                # report the value to show progress
                ans.append(result)
        
        # Convert to dataframe
        df = pd.DataFrame.from_dict(ans)
        
        # split dataframe using gropuby
        splits = list(df.groupby("molecule"))
        for i in range(numMols):
            # Dump descriptors of a molecule for all time frames
            splits[0][1].to_csv('Molecule_'+str(i+1)+'.csv')
            
        
        t2 = time.perf_counter()
        print(f'Finished in {t2-t1} seconds')
            
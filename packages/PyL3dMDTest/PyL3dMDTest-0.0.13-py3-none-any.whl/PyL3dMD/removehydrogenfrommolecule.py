# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 11:33:43 2022

@author: pawan
"""
import numpy as np

def removehydrogen(xyz, mass, bond, angle, dihedral):
    """
    It removes coordinates, mass, bonds, angles, and dihedrals of hydrogen atoms from a molecule
        M = molecular matrix consist of x, y, z coordinates of heavy atoms of a molecule
        massheavy = masses of heady atoms in a molecule
        bondheavy = atom ids of heavy atoms connected by bonds in a molecule
        angleheavy = atom ids of heavy atoms that are in angle interaction in a molecule
        dihedralheavy = atom ids of heavy atoms that are in dihedral or torsional interaction in a molecule
    """
    # Idenstify hydrogen atoms to deleted
    idxdeletexyz = [i for i, mass in enumerate(mass) if mass < 1.2]
    if len(idxdeletexyz)>=1:
        # Mass
        massheavy = np.delete(mass, idxdeletexyz, 0) # Coordinates of only heavy atoms
        
        # Molecular matrix consist of x, y, z cartesian coordinates of the molecule
        M = np.delete(xyz, idxdeletexyz, 0) # Coordinates of only heavy atoms
        
        # Update bond table accordingly - Numpy check if elements of array belong to another array
        check = np.isin(bond, np.array(idxdeletexyz)+1)
        idxkeepbond = [i for i in range(len(check)) if np.all(check[i,:] == [False, False])]
        bondheavy = bond[idxkeepbond,:] # Bonds between only heavy atoms
        
        # Update angle table accordingly - Numpy check if elements of array belong to another array
        check = np.isin(angle, np.array(idxdeletexyz)+1)
        idxkeepangle = [i for i in range(len(check)) if np.all(check[i,:] == [False, False, False])]
        angleheavy = angle[idxkeepangle,:] # Angles between only heavy atoms
        
        # Update dihedral table accordingly - Numpy check if elements of array belong to another array
        check = np.isin(dihedral, np.array(idxdeletexyz)+1)
        idxkeepdihedral = [i for i in range(len(check)) if np.all(check[i,:] == [False, False, False, False])]
        dihedralheavy = dihedral[idxkeepdihedral,:] # Dihedralheavy = between only heavy atoms
    else:
        # If no heavy atoms then keep as it is
        massheavy = mass
        M = xyz
        bondheavy = bond
        angleheavy = angle
        dihedralheavy = dihedral
    return (massheavy, M, bondheavy, angleheavy, dihedralheavy)
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 16:24:36 2022

@author: pawan
"""

"""
Routines to calculate the Accessible Surface Area of a set of atoms.
The algorithm/code is directly adapted from the Dr. Cao's chemopy package:

Cao, D. S., Xu, Q. S., Hu, Q. N., & Liang, Y. Z. (2013). ChemoPy: freely
available python package for computational biology and chemoinformatics. 
Bioinformatics, 29(8), 1092-1094.


This algorithm uses the dot density technique found in:

Shrake, A., and J. A. Rupley. "Environment and Exposure to Solvent
of Protein Atoms. Lysozyme and Insulin." JMB (1973) 79:351-371.
"""

import math
import numpy as np

"""
3D coordinates of n points on a sphere using the Golden Section Spiral algorithm
"""
def generate_sphere_points(n):
    inc = math.pi * (3 - math.sqrt(5))
    offset = 2.0/n

    i = np.array([i for i in range(int(n))]).astype(float)

    phi = i * inc
    y = i * offset - 1.0 + (offset/2.0)
    x = np.cos(phi)*np.sqrt(1 - y*y)
    z = np.sin(phi)*np.sqrt(1 - y*y)
    points = np.array([x,y,z]).T
    return points

"""
Indices of atoms within probe distance to atom k
"""
def find_neighbor_indices(xyz, Rc, probe, k):
    dist = np.sqrt(np.sum((xyz-xyz[k,:])**2,axis=1))
    temp = Rc[k] + Rc + 2*probe
    indices = np.append(range(k), range(k+1, len(xyz))).astype(int)
    neighbor_indices = [i for i in indices if dist[i] < temp[i]]
    return neighbor_indices

"""
Partial accessible surface areas of the atoms, using the probe and atom radius 
which were used todefine the surface
"""
def calculate_asa(xyz, Rc, probe, n_sphere_point = 960):
    
    sphere_points = generate_sphere_points(n_sphere_point)
    constant = 4.0 * math.pi / len(sphere_points)

    radius = probe + Rc
    areas = []
    for i in range(len(xyz)):
        neighbor_indices = find_neighbor_indices(xyz, Rc, probe, i)
        n_neighbor = len(neighbor_indices)
        
        
        j_closest_neighbor = 0
        n_accessible_point = 0
        
        for point in sphere_points:
            is_accessible = True
            
            testpoint = point*radius[i] + xyz[i,:]
            indices = np.append(range(j_closest_neighbor), range(j_closest_neighbor, n_neighbor)).astype(int)
            
            
            for j in indices:
                r = Rc[neighbor_indices[j]] + probe
                dist = np.sqrt(np.sum((xyz[neighbor_indices[j]] - testpoint)**2))
                if dist < r:
                    j_closest_neighbor = j
                    is_accessible = False
                    break
            if is_accessible:
                n_accessible_point += 1

        area = constant * (radius[i]**2) * n_accessible_point 
        areas.append(area)
    return areas

"""
Get 3D CPSA descriptors
    ASA = solvent-accessible surface area
    MSA = molecular surface area
    PNSA1 = partial negative area
    PNSA2 = total charge wighted negative surface area
    PNSA3 = atom charge weighted negative surface area
    PPSA1 = partial positive area
    PPSA2 = total charge wighted positive surface area
    PPSA3 = atom charge weighted positive surface area
    DPSA1 = difference in charged partial surface area
    DPSA2 = total charge wighted difference in charged partial surface area
    DPSA3 = atom charge weighted difference in charged partial surface area
    FNSA1 = fractional charged partial negative surface area
    FNSA2 = total charge wighted fractional charged partial negative surface area
    FNSA3 = atom charge weighted fractional charged partial negative surface area
    FPSA1 = fractional charged partial positive surface area
    FPSA2 = total charge wighted fractional charged partial positive surface area
    FPSA3 = atom charge weighted fractional charged partial positive surface area
    WNSA1 = surface weighted charged partial negative surface area 1
    WNSA2 = surface weighted charged partial negative surface area 2
    WNSA3 = surface weighted charged partial negative surface area 3
    WPSA1 = surface weighted charged partial positive surface area 1
    WPSA2 = surface weighted charged partial positive surface area 2
    WPSA3 = surface weighted charged partial positive surface area 3
    TASA = total hydrophobic surface area
    TPSA = total polar surface area
    FrTATP = TASA/TPSA
    RASA = relative hydrophobic surface area
    RPSA = relative polar surface area
    RNCS = relative negative charge surface area
    RPCS = relative positive charge surface area
"""
def getcpsadescriptors(xyz, charge, apRc):
    Rc = apRc*1.75
    CPSA = {}

    # molecular surface areas (MSA)
    RadiusProbe = 0.0
    n_sphere_point = 500
    SA = np.array(calculate_asa(xyz, Rc, RadiusProbe, n_sphere_point))   
    CPSA['MSA'] = np.sum(SA)

    # solvent-accessible surface areas (ASA)
    RadiusProbe = 1.5
    n_sphere_point = 1500
    SA = np.array(calculate_asa(xyz, Rc, RadiusProbe, n_sphere_point))
    CPSA['ASA'] = np.sum(SA)

    # Find indexes of the atoms with negative charge 
    idxNeg = [int(i) for i, x in enumerate(charge) if x < 0]

    # Find indexes of the atoms with positive charge 
    idxPos = [int(i) for i, x in enumerate(charge) if x > 0]

    # Find indexes of the atoms with absolute charge < 0.5 and >= 0.2
    idx1 = [int(i) for i, x in enumerate(charge) if abs(x) < 0.2]
    idx2 = [int(i) for i, x in enumerate(charge) if abs(x) >= 0.2]


       
    CPSA['PNSA1'] = np.sum(SA[idxNeg])
    CPSA['PPSA1'] = np.sum(SA[idxPos])

    CPSA['PNSA2'] = np.sum(charge[idxNeg]) * np.sum(SA[idxNeg])
    CPSA['PPSA2'] = np.sum(charge[idxPos]) * np.sum(SA[idxPos])

    CPSA['PNSA3'] = np.sum(charge[idxNeg]*SA[idxNeg])
    CPSA['PPSA3'] = np.sum(charge[idxPos]*SA[idxPos])

    # difference in charged partial surface areas
    CPSA['DPSA1'] = CPSA['PPSA1'] - CPSA['PNSA1']
    CPSA['DPSA2'] = CPSA['PPSA2'] - CPSA['PNSA2']
    CPSA['DPSA3'] = CPSA['PPSA3'] - CPSA['PNSA3']

    # fractional charged partial surface areas
    temp = np.sum(SA)    
    CPSA['FNSA1'] = CPSA['PNSA1']/temp    
    CPSA['FNSA2'] = CPSA['PNSA2']/temp
    CPSA['FNSA3'] = CPSA['PNSA3']/temp
    CPSA['FPSA1'] = CPSA['PPSA1']/temp    
    CPSA['FPSA2'] = CPSA['PPSA2']/temp
    CPSA['FPSA3'] = CPSA['PPSA3']/temp
     
    # surface weighted charged partial surface areas
    CPSA['WNSA1'] = CPSA['PNSA1']*temp/1000  
    CPSA['WNSA2'] = CPSA['PNSA2']*temp/1000 
    CPSA['WNSA3'] = CPSA['PNSA3']*temp/1000 
    CPSA['WPSA1'] = CPSA['PPSA1']*temp/1000
    CPSA['WPSA2'] = CPSA['PPSA2']*temp/1000 
    CPSA['WPSA3'] = CPSA['PPSA3']*temp/1000 
    
    # total hydrophobic (TASA) and polar surface areas (TPSA)
    CPSA['TASA'] = np.sum(SA[idx1])
    CPSA['TPSA'] = np.sum(SA[idx2])

    # fraction between TASA and TPSA
    if CPSA['TPSA'] == 0:
        CPSA['FrTATP'] = 0.0
    else:
        CPSA['FrTATP'] = CPSA['TASA']/CPSA['TPSA']
        
    # relative hydrophobic surface and polar surface areas
    CPSA['RASA'] = CPSA['TASA']/temp
    CPSA['RPSA'] = CPSA['TPSA']/temp
        
    # relative negative and positive charge surface areas
    idxmincharge = [int(i) for i, x in enumerate(charge) if x < np.min(charge)]
    RNCG = np.min(charge) / np.sum(charge[idxNeg])
    RPCG = np.max(charge) / np.sum(charge[idxPos])
    CPSA['RNCS'] =  SA[idxmincharge]/RNCG
    CPSA['RPCS'] = SA[idxmincharge]/RPCG
    
    return CPSA



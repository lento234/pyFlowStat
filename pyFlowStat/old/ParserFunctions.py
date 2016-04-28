'''
ParserFunctions.py

Collection of parser for pyFlowStat.

Import of pyFlowStat classes is not allowed in the file!
'''

import numpy as np
import re


def parseFoamFile_sampledSurface(foamFile):
    '''
    Parse a foamFile generated by the OpenFOAM sample tool or sampling library.
    The foamFile is basically a list of N scalar, N vector, N symmtensor or
    N tensor. It looks like this:
        * for a list of scalar s:    
          N
          (
              s1
              s2
              .
              .
              sN
          )
        * for a list of vector v:    
          N
          (
              (vx vy vz)1
              (vx vy vz)2
              .
              .
              (vx vy vz)N
          )
          
    If the N componants of the list are the same, then the foamfile looks like
    this:
        * for a list of constant scalar s:
            N{s}
        * for a list of constant vector v:
            N{(vx vy vz)}
    
    Note:
        * It's a primitiv parser, do not add header in your foamFile!
        * Inline comment are allowed only from line start. c++ comment style.
        * It's REALLY a primitive parser!!!
        
    Arguments:
        *foamFile*: python string
         Path of the foamFile.

    Returns:
        *output*: numpy array
         Data store in foamFile.
    '''
    output = []
    catchFirstNb = False
    istream = open(foamFile, 'r')
    for line in istream: 
        # This regex finds all numbers in a given string.
        # It can find floats and integers writen in normal mode (10000) or
        # with power of 10 (10e3).
        match = re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)
        if (line.startswith('//')):
            pass
        # chatch the firt number and it is alone: non constant field (normal case)
        if (catchFirstNb==False and len(match)==1):
            catchFirstNb = True
        # chatch the firt number and it is NOT alone: the field is constant and only one line is write in the file (OF standard)
        elif (catchFirstNb==False and len(match)>1):   
            catchFirstNb = True
            matchfloat = [float(nb) for nb in match]
            output = [matchfloat[1:]  for i in range(int(matchfloat[0])) ]
        # catch the remainding numbers
        elif (catchFirstNb==True and len(match)>0):
            matchfloat = [float(nb) for nb in match]
            if len(matchfloat)==1:
                output.append(matchfloat[0])
            else:
                output.append(matchfloat)
        else:
            pass
    istream.close()
    return np.array(output)
   
   
def parseVTK_ugly_sampledSurface(vtkfile):
    '''
    Parse a VTK file generate by the surface sampling tool of OpenFOAM. The
    surface has N grid points and M triangles. The data stored at each grid
    points has a dimension D.
    
    Warnings: This is a VERY primitive and ugly parser!! the python-to-vtk
    binding should be used instead of the following shitty code! 
    Nevertheless, this shit works :-)!!
    
    Arguments:
        *vtkfile*: python string
         Path to the vtk file
         
    Returns:
        *points*: numpy array of shape (N,3)
         List of points composing the grid.
         
        *polygon*: numpy array of shape (M,3)
         List of triangles. Technically, this parser can return a List of any
         type of ploygon, e.g: triangle, square, pentagon...
 
        *pointData* numpy array of shape (N,D)
         List of data associate with each point of the grid.
    '''
    pointsOut = []
    polyOut = []
    pointDataOut = []
    
    istream = open(vtkfile, 'r')
    line = istream.readline()

    # catch the begin of the list of points
    # -------------------------------------
    catchLine = False
    while catchLine==False:
        if (line.startswith('DATASET POLYDATA')):
            catchLine = True
        line = istream.readline()
        
    # catch the number of points
    nbpoints = int(re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)[0])
    pti = 0
    line = istream.readline()
    
    #store the points in pointsOut
    while (pti<nbpoints):
        match = re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)
        pointsOut.append(match)
        line = istream.readline()
        pti = pti+1
    pointsOut = np.asarray(pointsOut,dtype=float)
    
    # catch the begin of the list of polygons and the number of polygon
    # -----------------------------------------------------------------
    catchLine = False
    nbpoly = 0
    while catchLine==False:
        if (line.startswith('POLYGONS')):
            catchLine = True
            nbpoly = int(re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)[0])
        line = istream.readline()
    polyi = 0
    
    #store the polygons in polyOut
    while polyi<nbpoly:
        match = re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)
        polyOut.append(match[1:])
        line = istream.readline()
        polyi = polyi+1
    polyOut = np.asarray(polyOut,dtype=float)
    
    # catch the begin of the list of point data
    # -----------------------------------------
    catchLine = False
    nbptdata = 0
    while catchLine==False:
        if (line.startswith('POINT_DATA')):
            catchLine = True
            nbptdata = int(re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)[0])
        line = istream.readline()
    ptdatai = 0
    
    # jump the line starting with "FIELD attributes"
    line = istream.readline()
    
    # catch the dimension of point data and the number of point data
    match = re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)
    dimptdata = int(match[0])
    line = istream.readline()
    
    #store the point data in pointDataOut
    if dimptdata==1:
        pointDataOut = re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)
    else: 
        while ptdatai<nbptdata:
            match = re.findall('[-+]?\d*\.?\d+e*[-+]?\d*', line)
            pointDataOut.append(match)
            line = istream.readline()
            ptdatai = ptdatai+1
    pointDataOut = np.asarray(pointDataOut,dtype=float)
    
    istream.close()
    
    return pointsOut, polyOut, pointDataOut
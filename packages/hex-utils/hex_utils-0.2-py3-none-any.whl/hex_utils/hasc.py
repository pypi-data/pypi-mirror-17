#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Class for HASC grid - an ASCII encoded cartographic hexagonal grid [0]. 
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 31-03-2016 
#
# [0] https://github.com/ldesousa/HexAsciiBNF

import math
from hex_utils.grid import Grid

class HASC (Grid):
    
    _key_ncols  = "ncols"
    _key_nrows  = "nrows"
    _key_xll    = "xll"
    _key_yll    = "yll"
    _key_side   = "side"
    _key_nodata = "no_data"
    _key_angle  = "angle"
     
    _side    = 0
    _angle   = None  
    _hexPerp = 0
    
    @property
    def side(self):
        return self._side
    
    @property
    def angle(self):
        return self._angle
    
    @property
    def hexPerp(self):
        return self._hexPerp

    
    def _set_side(self, side):
                
        if (side <= 0):
            raise ValueError('Invalid cell side')
        self._side = side

   
    def init(self, ncols, nrows, xll, yll, side, nodata = "", angle = None):
        
        Grid.init(self, ncols, nrows, xll, yll, nodata)  
        self._set_side( side)
        self._angle   = angle 
        self._hexPerp = math.sqrt(3) * self._side / 2
    
        
    def _loadHeader(self):
    
        # Mandatory header
        self._set_ncols(self._loadHeaderLine(self._file.readline(), self._key_ncols,  type(1)))
        self._set_nrows(self._loadHeaderLine(self._file.readline(), self._key_nrows,  type(1)))
        self._xll     = self._loadHeaderLine(self._file.readline(), self._key_xll,    type(1.0))
        self._yll     = self._loadHeaderLine(self._file.readline(), self._key_yll,    type(1.0))
        self._set_side( self._loadHeaderLine(self._file.readline(), self._key_side,   type(1.0)))
        # Optional headers
        self._nextLine = self._file.readline()
        self._nodata = self._loadHeaderLine(self._nextLine, self._key_nodata, type("a"), True)
        if self._nodata != "" :
            self._nextLine = self._file.readline()
        self._angle  = self._loadHeaderLine(self._nextLine, self._key_angle, type(1.0),  True)
        if self._angle != None :
            self._nextLine =  self._file.readline()
    
    
    def _saveHeader(self, f):
           
        f.write(self._key_ncols + "\t" + str(self._ncols) + "\n")
        f.write(self._key_nrows + "\t" + str(self._nrows) + "\n")
        f.write(self._key_xll + "\t" + str(self._xll) + "\n")
        f.write(self._key_yll + "\t" + str(self._yll) + "\n")
        f.write(self._key_side + "\t" + str(self._side) + "\n")
        if self._nodata != "" :
            f.write(self._key_nodata + "\t" + str(self._nodata) + "\n") 
        if self._angle != None :
            f.write(self._key_angle + "\t" + str(self._angle) + "\n") 
            
            
    def getCellCentroidCoords(self, i, j):
        
        x = self._xll + i * 3 * self._side / 2
        y = self._yll + (self._nrows - 1 - j) * 2 * self._hexPerp + (i % 2) * self._hexPerp
        
        return (x, y)
            
    
    def saveAsGML(self, outputFilePath):
        
        try:
            from osgeo import ogr
        except ImportError:
            raise ImportError(""" ERROR: Could not find the GDAL/OGR Python library. 
                       On Debian based systems you can install it with this command:
                       apt install python-gdal""") 
        
        driver = ogr.GetDriverByName("GML")
        outSource = driver.CreateDataSource(
            outputFilePath, 
            ["XSISCHEMAURI=http://schemas.opengis.net/gml/2.1.2/feature.xsd"])
        outLayer = outSource.CreateLayer("output", None, ogr.wkbUnknown)
    
        newField = ogr.FieldDefn("value", ogr.OFTReal)
        outLayer.GetLayerDefn().AddFieldDefn(newField)
    
        # The perpendicular distance from cell center to cell edge
        perp = math.sqrt(3) * self._side / 2
        
        # Edge coordinates of an hexagon centered in (x,y) and a side of d:
        #
        #           [x-d/2, y+sqrt(3)*d/2]   [x+d/2, y+sqrt(3)*d/2] 
        #
        #  [x-d, y]                                                 [x+d, y]
        #
        #           [x-d/2, y-sqrt(3)*d/2]   [x+d/2, y-sqrt(3)*d/2]
    
        for j in range(self._nrows):
            for i in range(self._ncols):
                x = self._xll + i * 3 * self._side / 2
                y = self._yll + j * 2 * perp
                if (i % 2) != 0:
                    y += perp
                    
                polygon = ogr.CreateGeometryFromWkt("POLYGON ((" +
                    str(x - self._side)     + " " +  str(y)        + ", " +
                    str(x - self._side / 2) + " " +  str(y - perp) + ", " +
                    str(x + self._side / 2) + " " +  str(y - perp) + ", " +
                    str(x + self._side)     + " " +  str(y)        + ", " +
                    str(x + self._side / 2) + " " +  str(y + perp) + ", " +
                    str(x - self._side / 2) + " " +  str(y + perp) + ", " +
                    str(x - self._side)     + " " +  str(y)       + "))")
                
                outFeature = ogr.Feature(feature_def=outLayer.GetLayerDefn())
                outFeature.SetGeometryDirectly(polygon)
                outFeature.SetField("value", self._grid[i][self._nrows - j - 1])
                outLayer.CreateFeature(outFeature)
    
    
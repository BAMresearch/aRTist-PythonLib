# -*- coding: utf-8 -*-
"""
Created on Tue May 31 11:04:16 2022

@author: dschumac

The aRTist.py library needs to be present!
This is an example scipt which shows how to use a spreadsheet to simulate a bunch of images. The corresponding spreadsheet for this script is as a tab-separeted text-file ("ListOfSimulations.txt").
Each row in the spreadsheet corresponds to a single aRTist simulation. The colums represent the individual simulation parameters.
The given comlumns need to be adapted according to the simulation task, as the script needs to be!

"""

import pandas as pd
import os
import sys
sys.path.insert(1, '[Your python library directory]/aRTist-PythonLib')
import aRTist
import math




######################## Options ###############################
''' aRTist connection '''
HOST = "127.0.0.1"              # localhost
PORT = 3658                     # port @HOST
buffer = 1024                   # package size
timeout = 10                    # TimeOut in sec



''' Path '''
#Cone Beam
path_script = "[Your directory]/ListOfSimulations.txt"
path_save_images = "[Your directory]/Images_UB_ConeBeam/"




##############################################################################
''' Read Script file'''

data = pd.read_csv(path_script, sep="\t", encoding='mbcs')  #Read data
data.dropna(axis=0, how='all', inplace=True)                #Delete empty rows
data["Filename"].fillna('NA', inplace = True)               #Replace empty file names with "NA"
data_sort = data.sort_values(by=['ETA', 'ID'])        #sort by ID and spot size


###############################################################################                
''' Connect to aRTist '''
Con = aRTist.Connection(HOST, PORT, buffer, timeout)

###############################################################################
aRTist.Connection.send(Con, aRTist.SETUP_Preview(1))         

"""Source Setup"""
SourceZ = 10            #Random SZ pos, outside of object
SourcekV = data_sort['Source U'].iloc[0]
SourcemA = data_sort['Source I'].iloc[0]
SourceType = data_sort['Source Type'].iloc[0]
SourceFilterMat = data_sort['Source Filter Material'].iloc[0]
SourceFilterTh = data_sort['Source Filter Thickness'].iloc[0]
sampling = data_sort['Sampling'].iloc[0]

aRTist.Connection.send(Con, aRTist.SETUP_source(SourceZ, SourcekV, SourcemA, SourceType, SourceFilterMat, SourceFilterTh))
aRTist.Connection.send(Con, aRTist.SETUP_SourceSampling(sampling))


eta_out = -1                        # for checking if ETA has changed
FS_out = -1                         # for checking if FS has changed

for index, row in data_sort.iterrows():
    
    Fname = data_sort.loc[index, 'Filename']
    Fname = os.path.splitext(Fname)[0]              #extract name without extension
    
    """Detector position and pixel size"""
    PixelSize = data_sort.loc[index, 'Detector pixel size']
    
    
    """Spot Setup"""
    FS = data_sort.loc[index, 'Spot size']
    eta = data_sort.loc[index, 'ETA']
    SpotRes = data_sort.loc[index, 'Spot resolution']
    
    """Scene Setup"""
    LG = data_sort.loc[index, 'LG']
    name = 'LG{:.0f}'.format(LG)                                        # create object name similar to list in aRTist
    Obj = aRTist.Connection.send(Con, aRTist.get_ObjID(name)).split()   # Query Object ID from name
    OID = Obj[1]                                                        # isolate Object ID
    aRTist.Connection.send(Con, aRTist.set_vis_AllParts("off"))         # set visibility of all objects off
    aRTist.Connection.send(Con, aRTist.set_vis(OID, 'on'))              # activate object with <name> only
    
    """Calc magnification, source and detector Z pos"""
    cba = data_sort.loc[index, 'Cone beam angle']                       # Read cone beam angle
    CBA = cba*math.pi/180                                               # Degree to radian
    
    GW = LG*9                                                           # group width for 5 lines and 4 gaps in um!!
    N = data_sort.loc[index, 'N']                                       # No. of pixels representing unsharpness
    Mag = N*PixelSize/FS+1                                              # Magnification
    SZ = (GW/1000) / (2 * math.sin(CBA))                                # Source Z position (SOD)
    DetZ = -SZ * (Mag-1)                                                # Detector Z position (SOD)
    aRTist.Connection.send(Con, aRTist.set_position('S', 0, 0, SZ))
    
    '''Set object thickness (and other dimensions)'''
    sizeX = GW*10/3000
    sizeY = GW/1000
    sizeZ = data_sort.loc[index, 'LG Thickness']/1000 
    aRTist.Connection.send(Con, aRTist.resize(OID, sizeX, sizeY, sizeZ))
        
    
    """Calc Detector Size"""
    ePS = PixelSize*1000 / Mag      # effective pixel size
    DetSizeX = int(GW / ePS * 1.5)       # Detector length 1.5x group width to limit calc and analysis time
    DetSizeY = int(GW / ePS * 2.5)       # Detector widht 2.5x group width to allow for background fitting
    aRTist.Connection.send(Con, aRTist.SETUP_detector(DetZ, 0, DetSizeX, DetSizeY, PixelSize, 'max', 50000))
    
    
    if eta != eta_out or FS != FS_out:                    # Only calc new source when ETA or FS have changed
        aRTist.Connection.send(Con, aRTist.SETUP_CalcFocalspot(FS, FS, eta, SpotRes))
        
    
    aRTist.Connection.send(Con, aRTist.Clear_FF())
    aRTist.Connection.send(Con, aRTist.AutoAcq_FF(1))
    eta_out = eta
    FS_out = FS
    
    aRTist.Connection.send(Con, aRTist.RenderPreview())
    
    
    #Print name to update user
    # print('ID={}, ETA={:.1f}; LG={:.0f} um; Spot={:.1f} um; Sampling={:.0f};  N={:.1f}; {}'.format(index, eta, LG, FS*1000, sampling, N, Fname))
    print('ID={}, CB={:.2f}°; ETA={:.1f}; LG={:.0f} um; Thickness {:.0f} um; Spot={:.1f} um; Sampling={};  N={:.1f}; {}'.format(index, cba, eta, LG, sizeZ*1000, FS*1000, sampling, N, Fname))
    ResFname = '{}_CB{:.2f}_ETA{:.1f}_LG{:.0f}_Th{:.0f}_FS{:.1f}um_Sampling{}_N{:.1f}.tif'.format(Fname, cba, eta, LG, sizeZ*1000, FS*1000, sampling, N)
    ResPath = path_save_images + ResFname
    
    
    aRTist.Connection.send(Con, aRTist.make_image())
    aRTist.Connection.send(Con, aRTist.save_image(ResPath))    



###############################################################################
''' Close Connection to aRTist'''
Con.S.close()

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 19:30:16 2019
Creates and transates particles/pores
ONLY for 0 to 1 pore, faster and less expensive than creating new objects each time.
@authors: Alexander Funk, David Schumacher
"""

import socket
import random
import numpy as np
import math
from time import sleep

############################### Options #######################################
''' Connection '''
HOST = "127.0.0.1"              # localhost
PORT = 3658                     # port @HOST
BUFFER_SIZE = 1024              # package size
timeout = 10                    # TimeOut in sec

''' aRTist Module '''
SolidModNo = 17                 # Number of module "Solid" in aRTist (Modules/XX. Solid)

''' Particles/Pores '''
D_max = 100                      # max particle diameter in micrometer
D_min = 90                      # min particle diameter in micrometer
P_max = 45                      # max pore diameter in micrometer
P_min = 10                      # min pore diameter in micrometer
N_Par = 10                      # No. of particles to be created
pores_max = 5                   # max. no. of pores per particle
pores_min = 1                   # min. no. of pores per particle
space = 5 / 1000                # space to particle boundary

''' X-Ray Setup '''
MAG = 200                       # magnification
SDD = 400                       # source-detector distance in mm
pitch = 0.1                     # native pixel size (pitch) of the detector in mm
DBorder = 1.5                   # detector border (1/2), Factor (particle size)

kV = 15                         # Voltage of X-ray source
mA = 100                        # Current of X-ray source

''' Paths '''
path_aRTist_scene = "I:/Simulations/TMP/Pores/Single_Pore_Scene.aRTist"
path_save_images = "I:/Simulations/TMP/Pores/img_"


error = 0

############### aRTist functions (to be replaced by library!) #################
''' Communication with aRTist '''
def aRTist_connect():
    S = socket.socket()             # Create socket (for TCP)
    S.connect((HOST, PORT))         # Connect to aRTist
    S.settimeout(timeout)
    return S

def aRTist_sent(x):
    total = ""
    for i in range(len(x)):
       # print(i+1, "of", len(x), " commands send")  
       # print(x[i])
        S.send(x[i].encode())
        total = total + aRTist_listen(1)
    return total

def aRTist_listen(command_no):
    total = ""
    stop = False
    if (command_no == 0):
        S.settimeout(0.2)
    while (not stop):# and ("SUCCESS" not in total) and ("ERROR" not in total):     # as long as server doesn't respond and doesn't contain "SUCCESS"
        try:
            msg = S.recv(BUFFER_SIZE).decode()                                     # 
        except socket.timeout as e:
            err = e.args[0]
            if err == "timed out":
                print("Timeout\n")
                stop = True
                continue
        else:
            if ("SUCCESS" in msg):
                total = total + msg
               # print(msg)
                stop = True
                continue
            elif ("ERROR" in msg):
                total = total + msg
               # print(msg)
                stop = True
                global error
                error = error + 1 
                continue
            else:
               # print(msg)
                if (command_no == 0):
                    print(msg)
                total = total + msg
    S.settimeout(timeout)
    return total

''' aRTist specific commands '''
def aRTist_setup(Path):
    STR = ["""FileIO::OpenAny """+ Path +""";
"""]
    return STR

def aRTist_SETUP_detector(x, y, px):
    STR = ["""set ::Xdetector(Type) {flat panel};
""","""set ::Xsetup_private(DGauto) {Size};
""","""set ::Xsetup(DetectorPixelX) """+ str((int(x))) +""";
""","""set ::Xsetup(DetectorPixelY) """+ str((int(y))) +""";
""","""set ::Xsetup_private(DGdx) """+ str(px) +""";
""","""set ::Xsetup_private(DGdy) """+ str(px) +""";
""","""set ::Xdetector(AutoD) {max};
""","""set ::Xdetector(RefGV) 50000;
""","""::XDetector::UpdateGeometry 1;
"""]
    return STR

def aRTist_SETUP_source(pos, kV, mA):
    STR = ["""set ::Xsetup(SourceSampling) {point};
""","""set ::Xsource(Exposure) """+ str(mA) +""";
""","""set ::Xsource(Tube) {Mono};
""","""set ::Xsource(Voltage) """+ str(kV) +""";
""","""::PartList::Invoke S SetPosition 0 0 """+ str(pos) +""";
""","""::PartList::Invoke S SetRefPos 0 0 """+ str(pos) +""";
""","""set ::Xdetector(FFCorrRun) 0;
""","""XDetector::FFCorrClearCmd;
""","""::XSource::spectrumOK;
"""]  # set ::Engine::RenderPreview 0;
    return STR

def aRTist_SETUP_FFcorr():
    STR = ["""::XDetector::FFCorrGenCmd;
"""]
    return STR

def aRTist_create_sphere(R):
    R = 2 * R
    STR = ["""::Modules::Run Solid;
""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(Type) {ellipsoid};
""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(Equilateral) 1;
""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(X) """+ str(R) +""";
""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(PhiResolution) 80;
""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(ThetaResolution) 80;
""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(GridEllipsoid) 1;
""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(VolumeCorrect) 1;
""","""::Modules::Module""" +str(SolidModNo)+"""::GenerateCmd;
"""]
    return STR

def aRTist_set_material(ID, mat):
    STR = ["""::PartList::Set """+ str(ID) +""" Material """+ mat +""";
"""]
    return STR

def aRTist_translate(ID, x, y, z):
    STR = ["""::PartList::Invoke """+ str(ID) +""" SetPosition """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
""","""::PartList::Invoke """+ str(ID) +""" SetRefPos """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
"""]
    return STR

def aRTist_vis_off():
    STR = ["""::PartList::Set 1 Visible off;
""","""::PartList::Set 2 Visible off;
"""]
    return STR

def aRTist_vis_on(ID):
    STR = ["""::PartList::Set """+str(ID)+""" Visible on;
"""]
    return STR

def aRTist_resize(ID, size):
    STR = ["""::PartList::Invoke """+str(ID)+""" SetSize """+str(size)+""" """+str(size)+""" """+str(size)+""";
"""]
    return STR

def aRTist_make_image():
    STR = ["""::Engine::StartStopCmd;
"""]
    return STR

def aRTist_save_image(Path):
    STR = ["""::Modules::Execute ImageViewer Save16bit """+ Path +""" 1;
"""]
    return STR


# def aRTist_fire():
    # STR = ["""::Modules::Module""" +str(SolidModNo)+"""::GenerateCmd;
# """]
# ::Modules::Module""" +str(SolidModNo)+"""::Close;"
    # return STR            

########################## Conversions ################################
''' Particle/Pore '''
R_max = D_max / 2 / 1000        # max. particle radius in mm
R_min = D_min / 2 / 1000        # min. particle radius in mm
r_max = P_max / 2 / 1000        # max. pore radius in mm
r_min = P_min / 2 / 1000        # min. pore radius in mm

''' Detector/Source '''
OZ  = SDD / MAG                 # position of object (in Z-direction)
OZ = SDD - OZ
VX   = pitch / MAG               # voxel size , i.e. eff. pixel size
DETxy = (DBorder * D_max) / (VX * 1000) # detector size (square) in pixel

P_xy = (DETxy / 2) * VX * 0.9    # origin of particle range[x][y] with 10% border

###############################################################################
''' Generation of random variables and calculate objects (paricles+pores) '''
P_ID, P_RAD, P_XYZ, p_ANZ, p_RAD, p_XYZ = [],[],[],[],[],[]         # List of all particles/pores
R = np.array(range(N_Par), dtype=np.float)
for i in range(N_Par):
    R[i] = round(random.uniform(R_min, R_max),3)                    # particle radius in mm
    X = round(random.uniform(-(P_xy-R[i]), (P_xy-R[i])),3)          # particle position x 
    Y = round(random.uniform(-(P_xy-R[i]), (P_xy-R[i])),3)          # particle position y
    print('Particle',i ,'         RADIUS =',R[i] ,'mm')
    P_ID.append(i)
    P_RAD.append(R[i])
    P_XYZ.append([X, Y, OZ])
    pores = random.randint(pores_min, pores_max)                    # random no. of pores
    r = [] #np.array(range(pores), dtype=np.float)
    p_xyz = []
    for ii in range(pores):
        r.append(round(random.uniform(r_min, r_max),3))             # random pore radius in mm
        print('Particle',i ,' Pore',ii ,' RADIUS =', r[ii],'mm')
        
        ''' Generate coordinates for pore '''
        R2 = round(R[i] - space - r[ii],3)                          # max. sphere radius with R2+pore in sphere R
     #   print(R2)
        R3 = round(random.uniform(0, R2),3)                         # sphere with random radius in R2
        theta = random.uniform(0, math.pi)
        phi = random.uniform(0, 2*math.pi)
       # print(theta, phi)
        p_x = round((X + R3 * math.sin(theta) * math.cos(phi)),3)
        p_y = round((Y + R3 * math.sin(theta) * math.sin(phi)),3)
        p_z = round((OZ + R3 * math.cos(theta)),3)
        p_xyz.append([p_x, p_y, p_z])
    p_ANZ.append(pores)
    p_RAD.append(r)
    p_XYZ.append(p_xyz)
    
print(P_RAD)   
print(P_XYZ)  
print(p_RAD) 
print(p_XYZ)
print(p_ANZ)

###################### Save coordinates in CSV ###########################
with open(path_save_images +"data.csv", "w+") as file:
    STR = "Particle_ID, P_RADIUS, P_x, P_y, P_z, No. of pores, Pore_ID, p_RADIUS, p_x, p_y, p_z"
    file.write(STR + "\n")
    for i in range(N_Par):
        STR = ""+str(P_ID[i])+", "+str(P_RAD[i])+", "+str(P_XYZ[i][0])+", "+str(P_XYZ[i][1])+", "+str(P_XYZ[i][2])
        if p_ANZ[i] == 0:
            STR = STR + ", 0, , , , , "
            file.write(STR + "\n")
        elif p_ANZ[i] > 0: 
            STR = STR + ", " +str(p_ANZ[i])
            for ii in range(p_ANZ[i]):
                STR2 = STR +", "+str(ii)+", "+str(p_RAD[i][ii])+", "+str(p_XYZ[i][ii][0])+", "+str(p_XYZ[i][ii][1])+", "+str(p_XYZ[i][ii][2])
                file.write(STR2 + "\n")
                
###############################################################################                
''' Connect to aRTist '''
S = aRTist_connect()

aRTist_listen(0)

###############################################################################
''' SETUP aRTist scene '''
print("SETUP aRTist scene")
aRTist_sent(aRTist_setup(path_aRTist_scene))
print("SETUP Detector aRTist-Scene") 
aRTist_sent(aRTist_SETUP_detector(DETxy, DETxy, pitch))
print("SETUP Source aRTist-Scene") 
aRTist_sent(aRTist_SETUP_source(SDD, kV, mA))
print("SETUP FFcorr aRTist-Scene") 
aRTist_sent(aRTist_SETUP_FFcorr())
aRTist_sent(["""set ::Xdetector(FFCorrRun) 1;
"""])
print("SETUP FINISH aRTist-Scene") 

###############################################################################
''' Create particles and pores in aRTist, save image '''
# Create two dummy spheres
aRTist_sent(aRTist_create_sphere(R_max))
aRTist_sent(aRTist_create_sphere(r_max))
aRTist_sent(aRTist_set_material(1, "{Ti}"))
aRTist_sent(aRTist_set_material(2, "{void}"))
#aRTist_sent(["""::Modules::Module""" +str(SolidModNo)+"""::Close;
#"""])

# translate spheres
for i in range(N_Par):
   # particle
    print("Create Particle ", i , "of", N_Par)
    aRTist_sent(aRTist_vis_off())
    aRTist_sent(aRTist_vis_on(1))
    aRTist_sent(aRTist_resize(1, (2*P_RAD[i])))
    aRTist_sent(aRTist_translate(1, P_XYZ[i][0], P_XYZ[i][1], P_XYZ[i][2]))
    
   # pores
    if p_ANZ[i] > 0:
        aRTist_sent(aRTist_vis_on(2))
        aRTist_sent(aRTist_resize(2, (2*p_RAD[i][0])))
        aRTist_sent(aRTist_translate(2, p_XYZ[i][0][0], p_XYZ[i][0][1], p_XYZ[i][0][2]))
       # for ii in range(p_ANZ[i]):
    # acquire image
    aRTist_sent(aRTist_make_image())
    # save image
    aRTist_sent(aRTist_save_image((path_save_images + str(i).zfill(5) +".tif")))



###############################################################################
''' Timer for Debug '''
for i in range(5):
    print("wait ",i ," s")
    sleep(1)
print("FINISH!", error, "aRTist Errors")    
###############################################################################
''' Close Connection to aRTist'''
S.close()

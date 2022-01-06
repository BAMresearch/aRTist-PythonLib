# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:20:50 2020

@author: David Schumacher
"""
import socket
import numpy as np
import csv

########################### Options ####################################
''' aRTist connection '''
HOST = "127.0.0.1"              # localhost
PORT = 3658                     # port @HOST
BUFFER_SIZE = 1024              # package size
timeout = 10                    # TimeOut in sec

''' aRTist setup '''
SolidModNo = 16                 # Number of module "Solid" in aRTist (Modules/XX. Solid)

''' Particles/Pores '''
D_max = 100                     # max particle diameter in micrometer
P_max = 30                      # max pore diameter in micrometer
P_min = 5                       # min pore diameter in micrometer

N_ParX = 2                      # No. of particles in X-direction
N_ParY = 2                      # No. of particles in X-direction

Mat_par = "{Fe}"                # Material of Particle
Mat_pore = "{VOID}"             # Material of Pore


MAG = 50                        # magnification
SDD = 400                       # source-detector distance in mm
pitch = 0.1                     # ative pixel size (pitch) of the detector in mm
DBorder = 1.5                   # detector border (1/2), Factor (particle size)

DetX = 500                      # Detector resolution X
DetY = 500                      # Detector resolution Y

kV = 150                        # Voltage of X-ray source
mA = 100                        # Current of X-ray source

''' Paths '''
path_aRTist_scene = "I:/Simulations/TMP/Pores/Pore_Matrix_Scene.aRTist"
path_save = "I:/Simulations/TMP/Pores/Coordinates_"



error = 0

########################### aRTist functions (to be replaced by library!) #################################
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

def aRTist_set_position(ID, x, y, z):
    STR = ["""::PartList::Invoke """+ str(ID) +""" SetPosition """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
""","""::PartList::Invoke """+ str(ID) +""" SetRefPos """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
"""]
    return STR

def aRTist_translate(ID, x, y, z):
    STR = ["""::PartList::Invoke """+ str(ID) +""" Translate world """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
"""]
    return STR


def aRTist_vis_off():
    STR = ["""::PartList::Set parts Visible off;
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

       

########################## Conversions ################################
''' Particle/Pore '''

R_max = D_max / 2 / 1000        # max. particle radius in mm
r_max = P_max / 2 / 1000        # max. pore radius in mm
r_min = P_min / 2 / 1000        # min. pore radius in mm

''' Detector/Source '''
OZ  = SDD / MAG                         # position of object (in Z-direction)
OZ  = SDD - OZ
VX   = pitch / MAG                      # voxel size , i.e. eff. pixel size
DETxy = (DBorder * D_max) / VX / 1000   # detector size (square) in pixel

P_xy = (DETxy / 2) * VX * 0.9           # origin of particle range[x][y] with 10% border

###############################################################################

P_count = N_ParX*N_ParY              #No. of Particles/Pores


###############################################################################                
''' Connect to aRTist '''
S = aRTist_connect()

aRTist_listen(0)

###############################################################################
''' SETUP aRTist scene '''
print("SETUP aRTist scene")
aRTist_sent(aRTist_setup(path_aRTist_scene))
print("SETUP Detector aRTist-Scene") 
aRTist_sent(aRTist_SETUP_detector(DetX, DetY, pitch))
print("SETUP Source aRTist-Scene") 
aRTist_sent(aRTist_SETUP_source(SDD, kV, mA))
print("SETUP FFcorr aRTist-Scene") 
aRTist_sent(aRTist_SETUP_FFcorr())
aRTist_sent(["""set ::Xdetector(FFCorrRun) 1;        
"""])                                          #to check!!
print("SETUP FINISH aRTist-Scene") 

###############################################################################
'''Calc Particle/Pore positions:'''
P_ID, P_RAD, P_XYZ, p_RAD, p_ID = [],[],[],[],[]    # List of all particles/pores

n = 0                                               #loop count
for i in range(N_ParY):
    for ii in range(N_ParX):        
        n += 1                                      #increment n by 1
        if (i % 2):                                 #ii is odd
            X = 2*R_max*ii + R_max
        else:                                       #ii is even (incl. 0)
            X = 2*R_max*ii                          # particle position x 

        Y = np.sqrt(3*R_max**2)*i                   # particle position x 
        
        P_XYZ.append([X, Y, OZ])
        P_ID.append(2*n-1)                          # Particle-ID
        p_ID.append(2*n)                            # Pore-ID
        P_RAD.append(R_max)
 
print(P_ID) 
print(p_ID)   
print(P_XYZ)

##############################################################################
'''Calc Pore distribution:'''
p_RAD = list(np.linspace(r_min, r_max, num=P_count))      #list of pore radii

##############################################################################
''' Create particles and pores in aRTist '''
n = -1                                                      #loop count
for i in range(N_ParY):
    for ii in range(N_ParX):
        n += 1                                              #increment n by 1
        # Particle
        print("Create Particle ", n+1 , "of", P_count)
        aRTist_sent(aRTist_create_sphere(R_max))
        aRTist_sent(aRTist_set_material(P_ID[n], Mat_par))
        aRTist_sent(aRTist_set_position(P_ID[n], P_XYZ[n][0], P_XYZ[n][1], P_XYZ[n][2]))
        
        
        # Pore
        aRTist_sent(aRTist_create_sphere(p_RAD[n]))
        aRTist_sent(aRTist_set_material(p_ID[n], Mat_pore))
        aRTist_sent(aRTist_set_position(p_ID[n], P_XYZ[n][0], P_XYZ[n][1], P_XYZ[n][2]))
        
    if (i == range(N_ParY)[-1]):
        aRTist_sent(["""::Modules::Module""" +str(SolidModNo)+"""::Close;
        """])

##############################################################################
'Center middle particle at [0,0,z]'

Shift = []
for i in range(len(P_XYZ[0])):   
    diff = (P_XYZ[0][i] - P_XYZ[-1][i]) / 2       
    Shift.append(diff)

aRTist_sent(aRTist_translate('Parts', Shift[0], Shift[1] , Shift[2]))



####################### Save coordinates in CSV ####################################
header = ["Particle ID", "Particle Diameter", "Pore ID", "Pore Diameter", "X", "Y", "Z"]

with open(path_save +"data.csv", "w", newline ='') as file:
    write = csv.writer(file) 
    write.writerow(header) 
   
    for i in range(P_count):
        row = [str(P_ID[i]), str(2*P_RAD[i]), str(p_ID[i]), str(2*p_RAD[i]), str(P_XYZ[i][0]), str(P_XYZ[i][1]), str(P_XYZ[i][2])]
        write.writerow(row)


###############################################################################
''' Close Connection to aRTist'''
S.close()
        
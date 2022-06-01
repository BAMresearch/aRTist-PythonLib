# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:23:40 2020by afunkt1 based on MATLAB-scripts by dschumac
Updated on Mon May 30 17:36:00 2022 by dschumac

@authors: dschumac. afunk1
"""
import socket


   
class Connection:
    def __init__(self, Host, Port, buffer_size, timeout):
        self.Host = Host
        self.Port = Port
        self.buffer_size = buffer_size
        self.timeout = timeout
        self.connect()
    
    def connect(self):
        self.S = socket.socket()                        # Create socket (for TCP)
        self.S.connect((self.Host, self.Port))          # Connect to aRTist
        self.S.settimeout(self.timeout)
        self.listen(0)
        return self.S
    
    def send(self, x):
        total = ""
        for i in range(len(x)):
           # print(i+1, "of", len(x), " commands send")  
           # print(x[i])
            self.S.send(x[i].encode())
            total = total + self.listen(1)
        return total
    
    def listen(self, command_no):
        total = ""
        stop = False
        if (command_no == 0):
            self.S.settimeout(0.2)
        while (not stop):# and ("SUCCESS" not in total) and ("ERROR" not in total):     # Solange server antwortet und nicht "SUCCESS" enthält
            try:
                msg = self.S.recv(self.buffer_size).decode()                                     # 
            except BaseException as e:
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
        self.S.settimeout(self.timeout)
        return total

''' Scene '''
def open_scene(Path):
    STR = ["""FileIO::OpenAny """+ Path +""";
"""]
    return STR

def SETUP_Preview(state):
    #state (0, 1)
    STR = ["""set ::Engine::RenderPreview """+str(state)+""";
           """]
    return STR

def SETUP_detector(posZ, angleZ, x, y, px, RefPoint, GV): #Order of commands important!! -> Invoke should be reomved!
    #RefPoint ('off', 'min', 'max', 'center')
    STR = ["""::PartList::Invoke D SetPosition 0 0 """+ str(posZ) +""";
           ""","""::PartList::Invoke D SetRefPos 0 0 """+ str(posZ) +""";
           ""","""::PartList::Invoke D SetOrientation 0 0 """+ str(angleZ) +""";
           ""","""set ::Xdetector(AutoD) """+ RefPoint +""";
           ""","""set ::Xdetector(RefGV) """+ str(GV) +""";
           ""","""set ::Xsetup(DetectorPixelX) """+ str((int(x))) +""";
           ""","""set ::Xsetup(DetectorPixelY) """+ str((int(y))) +""";
           ""","""set ::Xsetup_private(DGauto) Size;
           ""","""set ::Xsetup_private(DGdx) """+ str(px) +""";
           ""","""set ::Xsetup_private(DGdy) """+ str(px) +""";
           ""","""::XDetector::ExposureModeChange;
           ""","""::XDetector::UpdateGeometry 1;
           """]
    return STR

def SETUP_source(posZ, kV, mA, Type, FMat, FThick):
    #Type (Mono, General)
    STR = ["""set ::Xsource(Exposure) """+ str(mA) +""";
           ""","""set ::Xsource(Voltage) """+ str(kV) +""";
           ""","""set ::Xsource(Tube) """+ str(Type) +""";
           ""","""set ::Xsource(FilterMaterial) """+ str(FMat) +""";
           ""","""set ::Xsource(FilterThickness) """+ str(FThick) +""";
           ""","""::PartList::Invoke S SetPosition 0 0 """+ str(posZ) +""";
           ""","""::PartList::Invoke S SetRefPos 0 0 """+ str(posZ) +""";
           ""","""::XSource::ComputeSpectrum;
           """]
    return STR

def SETUP_SourceSampling(sampling):
    #Type (Mono, General)
    STR = ["""set ::Xsetup(SourceSampling) """+ str(sampling) +""";
           """]
    return STR

def SETUP_CalcFocalspot(width, height, fract, res):
    STR = ["""set ::Xsource_private(SpotWidth) """+ str(width) +""";       
			""","""set ::Xsource_private(SpotHeight) """+ str(height) +""";
			""","""set ::Xsource_private(SpotHeight) """+ str(height) +""";
			""","""set ::Xsource_private(SpotLorentz) """+ str(fract) +""";
			""","""set ::Xsource_private(SpotRes) """+ str(res) +""";
			""","""::XSource::SetSpotProfile;
			"""]
    return STR

def LOAD_spectrum(SpecPath):
    #Type (Mono, General)
    STR = ["""::XSource::LoadSpectrum """+ SpecPath +""";
           """]
    return STR

def Acq_FF():
    STR = ["""::XDetector::FFCorrGenCmd;
"""]
    return STR

def AutoAcq_FF(state):
    #state (0, 1)
    STR = ["""set ::Xdetector(FFCorrRun) """+str(state)+""";
"""]
    return STR

def Clear_FF():
    STR = ["""XDetector::FFCorrClearCmd;
"""]
    return STR

def count_parts():
    STR = ["""::PartList::Count;
"""]
    return STR

def set_material(ID, mat):
    STR = ["""::PartList::Set """+ str(ID) +""" Material """+ mat +""";
"""]
    return STR

def set_position(ID, x, y, z):
    STR = ["""::PartList::Invoke """+ str(ID) +""" SetPosition """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
""","""::PartList::Invoke """+ str(ID) +""" SetRefPos """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
"""]
    return STR

def translate(ID, x, y, z):
    STR = ["""::PartList::Invoke """+ str(ID) +""" Translate world """+ str(x) +""" """+ str(y) +""" """+ str(z) +""";
"""]
    return STR

def set_vis_AllParts(state): #state = "on"/"off"
    STR = ["""::PartList::SetVisibility """+state+""";
           """]
    return STR

def set_vis(ID, state):
    STR = ["""::PartList::Set """+str(ID)+""" Visible """+state+""";
           """]
    return STR

def resize(ID, size):
    STR = ["""::PartList::Invoke """+str(ID)+""" SetSize """+str(size)+""" """+str(size)+""" """+str(size)+""";
"""]
    return STR

def make_image():
    STR = ["""::Engine::StartStopCmd;
"""]
    return STR

def save_image(Path):
    STR = ["""::Modules::Execute ImageViewer Save16bit """+ Path +""" 1;
"""]
    return STR

def SETUP_CT(CTModNo, angle, steps, OutDir, OutName, OutFormat, PType, RunFDK, OnlySelObj, Direction, Scat, ScatInt):
    #OutFormat ({BAM CT}, TIFFs)
    #PType (16bit, float)
    #Direction (clockwise, counterclockwise)
    #Scat (off, McRay)
    STR = ["""::Modules::Run CtScan;
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Angle) """+ str(angle) +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Steps) """+ str(steps) +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Directory) """+ OutDir +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(File) """+ OutName +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Output) """+ str(OutFormat) +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(PixelType) """+ str(PType) +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Feldkamp) """+ str(RunFDK) +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Selected) """+ str(OnlySelObj) +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Direction) """+ str(Direction) +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(ScatterMode) """+ Scat +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(ScatterInterval) """+ str(ScatInt) +""";
           """]
    return STR

def SETUP_FDK(CTModNo, VType, Interp, OutFormat):
    #VType (8bit, 16bit, 32bit, float)
    #OutFormat ({BAM CT}, VTK, RAW)
    STR = ["""::Modules::Run CtScan;
        ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(VoxelType) """+ str(VType) +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(Interpolate) """+ str(Interp) +""";
           ""","""set ::Modules::Module""" +str(CTModNo)+"""::CtScan(FileType) """+ str(OutFormat) +""";
           """]
    return STR

def Run_CT(CTModNo):
    STR = ["""::Modules::Run CtScan;
        ""","""::Modules::Module""" +str(CTModNo)+"""::Execute; 
           """]
    return STR

def create_Object(SolidModNo, OType, Eq, x, y, z, PhiRes, ThetaRes, Grid, VC):
    STR = ["""::Modules::Run Solid;
           ""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(Type) """+ str(OType) +""";
           ""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(Equilateral) """+ str(Eq) +""";
           ""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(X) """+ str(x) +""";
           ""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(Y) """+ str(y) +""";
           ""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(Z) """+ str(z) +""";
           ""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(PhiResolution) """+ str(PhiRes) +""";
           ""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(ThetaResolution) """+ str(ThetaRes) +""";
           ""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(GridEllipsoid) """+ str(Grid) +""";
           ""","""set ::Modules::Module""" +str(SolidModNo)+"""::Solid(VolumeCorrect) """+ str(VC) +""";
           ""","""::Modules::Module""" +str(SolidModNo)+"""::GenerateCmd;
           """]
    return STR

def get_Obj_IDs():
    STR = ["""PartList::Query {ID};
           """]
    return STR

def get_ObjID(name):
    STR = ['PartList::Query {ID Name} -where {Name=="' +str(name)+ '"};\r\n']
    return STR #PartList::Query {ID Name Material} -where {Material=="Al"}

def get_Obj_ID_by_Pos(pos):
    #pos (e.g. 'end')
    STR = ["""PartList::GetIDFromPos """+ str(pos) +""";
           """]
    return STR

def select_last_Obj():
    STR = ["""PartList::Select [PartList::GetIDFromPos end];
           """]
    return STR

def delete_all_Obj():
    STR = ["""PartList::Clear;
           """]
    return STR



################# Extract results from aRTist answer string ###################
def Extract_resultStr(aRTist_string):
    startI = aRTist_string.find('RESULT ') + 7
    endI = aRTist_string.find('\r\nSUCCESS', startI)
    result = aRTist_string[startI:endI]
    return result



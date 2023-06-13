## utilis functinons for S-aRTist
# Load, move, rotate and change material of .stl
# !!! DO NOT CHANGE THE FIRST 15 LINES !!!

namespace eval SaRTist {
    variable ns [namespace current]

    proc GetPythonPath {} {
        return C:\\Data\\GIT\\SaRTist_small\\venv\\Scripts\\python.exe 
    }

    # YOU CAN START CHANGES HERE: (!!!!!!!!!!!!!!!!!!!)

    proc SendToPython { DATA } {
        # Sends DATA to the TCP Python listing connection
        if { [catch {set SEND_DATA [eval $DATA]}] != 0} {
            set SEND_DATA "Error"
        }
        puts "Data for Python: $SEND_DATA"

        # socket config
        set host "127.0.0.1"
        set port 1234
        set my_sock [socket -async $host $port]
        fconfigure $my_sock -buffering none

        # Send data
        puts $my_sock $SEND_DATA
        flush $my_sock
        ::RemoteControl::CloseConnection $my_sock 127.0.0.1 1234
	}

	proc SendImageToPython { Image } {
        variable TransferImage

	    # socket config
        set host "127.0.0.6"
        set port 1234
        set my_sock [socket $host $port]

        fconfigure $my_sock -buffering none

        if { ![info exists TransferImage] } { set TransferImage [TempFile::mktmp .raw] }
		if { [$Image GetClassName] == [Image::aRTistImage GetClassName] } { set Image [$Image GetImage] }

		lassign [$Image GetDimensions] NX NY NZ
		set NC [$Image GetNumberOfScalarComponents]
		set NB [$Image GetScalarSize]
		set ES [Image::GetEndianString]

		set Writer [vtkImageWriter New]
		try {
			Utils::SetFileName $Writer $TransferImage
			$Writer SetFileDimensionality 3
			$Writer SetInput $Image
			$Writer Write
			set Status [$Writer GetErrorCode]
			if { $Status != 0 } { error "Error writing '$TransferImage': VTK error code $Status" }
		} finally { $Writer Delete }

		lassign [RemoteControl::EncodeFile $TransferImage] Type Data
		puts $Type

		Send $my_sock IMAGE

		Send $my_sock $NZ
		Send $my_sock $NY
		Send $my_sock $NX
		Send $my_sock $NB
		Send $my_sock $ES

		Send $my_sock $Type
		puts $my_sock $Data

		Send $my_sock {IMAGE {}}

	}

	proc Send { Channel Data } {
        set Type BASE64
		try {

			if { [eof $Channel] } { return }

			if { $Data == {} } {
				
			} else {
				foreach Line [split $Data \n] {
					puts $Channel $Line
				}
			}

		} on error { errmsg } {
			# do not use ::puts in any way here, as that might lead to an endless loop
			aRTist::WriteLog "Error sending remote control message via '$Channel': '$errmsg'" "ERR: "
		}

	}

    proc Move { ID X Y Z } {
        # Move obj with $ID to position ($X, $Y, $Z) in world coordinate system
        set obj [::PartList::Get $ID Obj]
        $obj SetPosition $X $Y $Z
        return obj
    }

    proc Scale { ID SX SY SZ } {
        # Scale obj with $ID to size ($SX, $SY, $SZ)
        set obj [::PartList::Get $ID Obj]
        $obj SetScale $SX $SY $SZ
        return obj
    }

    proc Delete { ID } {
        # Delete obj with $ID
        ::PartList::Delete $ID
        puts "DELETED"
    }

    proc SetMaterial { ID  MAT } {
        # Set material of obj. The material must be in the material list.
        ::PartList::SetMaterial $MAT $ID
    }

    proc Rotate { ID ALP BET GAM } {
        # Rotate obj with $ID with euler angles ($ALP, $BET, $GAMA) in world coordinate system
        set obj [::PartList::Get $ID Obj]
        $obj SetOrientation $ALP $BET $GAM
        return obj
    }

    proc CheckSaRTist {} {
        set text "aRTist is now SaRTist !!!"
        puts $text
        return $text
    }

    proc LoadSTL {Path Name} {
        # Loads stl from path
        set obj [::PartList::LoadPart $Path Fe $Name]
        return obj
    }

    proc LoadPart {Path Name Material} {
        # Loads stl from path
        set obj [::PartList::LoadPart $Path $Material $Name]
        return $obj
    }

    proc LoadSpectrum {Path} {
        # Loads spectrum from path
        ::XSource::LoadSpectrum $Path
    }

    proc LoadDetector {Path} {
        # Loads detector from path
        ::XDetector::OpenDetector $Path
    }

    proc MakeSnapshot_TIFF {OutputName} {
        # Saves an X-Ray scan to the desired path
        set ImagePointerFull [Engine::ComputeRadiography [Engine::Compute]]
		set ImagePointer [lindex $ImagePointerFull 0]
        Image::SaveTIFF $ImagePointer $OutputName 1
		foreach img $ImagePointerFull { Utils::nohup { $img Delete } }
        return 0
    }

    proc GetImageName {} {
        return Engine::Compute
    }

    proc SetSpectrum {MaxVoltage Tube computed Transmission Voltage TargetThickness WindowThickness ReferenceActivity Resolution ActivityUnit AngleIn
                      WindowMaterial MaxCurrent ExposureDate Name FilterThickness MaxPower Exposure HalfLife ReferenceDate FilterMaterial TargetAngle
                      TargetMaterial} {
        global Xsource

        set Xsource(MaxVoltage) $MaxVoltage
        set Xsource(Tube) $Tube
        set Xsource(computed) $computed
        set Xsource(Transmission) $Transmission
        set Xsource(Voltage) $Voltage
        set Xsource(TargetThickness) $TargetThickness
        set Xsource(WindowMaterial) $WindowMaterial
        set Xsource(ReferenceActivity) $ReferenceActivity
        set Xsource(Resolution) $Resolution
        set Xsource(ActivityUnit) $ActivityUnit
        set Xsource(AngleIn) $AngleIn
        set Xsource(WindowMaterial) $WindowMaterial
        set Xsource(MaxCurrent) $MaxCurrent
        set Xsource(ExposureDate) $ExposureDate
        set Xsource(Name) $Name
        set Xsource(FilterThickness) $FilterThickness
        set Xsource(MaxPower) $MaxPower
        set Xsource(Exposure) $Exposure
        set Xsource(HalfLife) $HalfLife
        set Xsource(ReferenceDate) $ReferenceDate
        set Xsource(FilterMaterial) $FilterMaterial
        set Xsource(TargetAngle) $TargetAngle
        set Xsource(TargetMaterial) $TargetMaterial

        ::XSource::spectrumOK
        return 0
    }

    proc GetSpectrum {} {
        global Xsource

        set source_list [array get Xsource]
        set source_string [join $source_list " !?"]
        return $source_string
    }


    proc SetDetector {LRUnsharpness Scale AutoDPosY AutoDPosX Type NoiseFactorOn ScanMode Unsharpness FFCorrAutoScale FFCorrRun
                      UnsharpnessOn FFCorrScale RefGV NrOfFrames LRRatio AutoD NoiseFactor} {
        global Xdetector

        set Xdetector(LRUnsharpness)  $LRUnsharpness
        set Xdetector(Scale) $Scale
        set Xdetector(AutoDPosY) $AutoDPosY
        set Xdetector(AutoDPosX) $AutoDPosX
        set Xdetector(Type) $Type
        set Xdetector(NoiseFactorOn) $NoiseFactorOn
        set Xdetector(ScanMode) $ScanMode
        set Xdetector(Unsharpness) $Unsharpness
        set Xdetector(FFCorrAutoScale) $FFCorrAutoScale
        set Xdetector(FFCorrRun) $FFCorrRun
        set Xdetector(UnsharpnessOn) $UnsharpnessOn
        set Xdetector(FFCorrScale) $FFCorrScale
        set Xdetector(RefGV) $RefGV
        set Xdetector(NrOfFrames) $NrOfFrames
        set Xdetector(LRRatio) $LRRatio
        set Xdetector(AutoD) $AutoD
        set Xdetector(NoiseFactor) $NoiseFactor

        return 0
    }

    proc GetDetector {} {
        global Xdetector

        set detector [array get Xdetector]

        set detector_string [join $detector " !?"]

        return $detector_string
    }

    proc SetSpot {DetectorSamplingTypes SourceSampling SGSx SGSy DGdx DGdy
                  SourceSamplingTypes DGdmin DGdmax DGauto ViewPickPos DGSx DGSy} {
        global Xsource_private

        set Xsource_private(SpotWidth) $SpotWidth
        set Xsource_private(SpotHeight) $SpotHeight
        set Xsource_private(SpotLorentz) $SpotLorentz
        set Xsource_private(SpotRes) $SpotRes

        ::XSource::SetSpotProfile

        return 0
    }

    proc GetSpot {} {
        global Xsetup_private]

        set spot [array get Xsetup_private]]

        set spot_string [join $spot " !?"]

        return $spot_string
    }
}

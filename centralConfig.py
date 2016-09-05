### total on Z predictions
class zPredictions:
	class default:
		class SF:
			class central:
				val = 62.0
				err = 8.2
			class forward:
				val = 24.1
				err = 3.1
	class geOneBTags:
		class SF:
			class central:
				val = 15.6
				err = 2.2
			class forward:
				val = 6.0
				err = 1.3
	class noBTags:
		class SF:
			class central:
				val = 46.4
				err = 7.9
			class forward:
				val = 18.1
				err = 2.8

### On Z background from processes with real neutrinos (WZ, ZZ, ttZ, etc)
### taken from MC
class OtherPredictions:
	class default:
		class SF:
			class central:
				val = 16.7
				err = 8.0
			class forward:
				val = 5.8
				err = 8.0
	class geOneBTags:
		class SF:
			class central:
				val = 3.0
				err = 8.0
			class forward:
				val = 0.9
				err = 8.2
	class noBTags:
		class SF:
			class central:
				val = 13.7
				err = 8.0
			class forward:
				val = 4.9
				err = 8.0

### On Z background predictions from Z boson decays, estimated using photon+jets data
class OnlyZPredictions:
	class default:
		class SF:
			class central:
				val = 45.3
				err = 8.0
			class forward:
				val = 18.3
				err = 8.0
	class geOneBTags:
		class SF:
			class central:
				val = 12.6
				err = 8.0
			class forward:
				val = 5.1
				err = 8.2
	class noBTags:
		class SF:
			class central:
				val = 32.7
				err = 8.0
			class forward:
				val = 13.2
				err = 8.0

### default systematics for the different background estimation tools
class systematics:
	class rMuE:
		class central:
			val = 0.1
		class forward:
			val = 0.2	
	class trigger:
		class central:
			val = 0.05
		class forward:
			val = 0.05
	class rOutIn:
		class central:
			val = 0.25
		class forward:
			val = 0.25		

### dilepton mass bins for the signal bins and for the direct measurement of R_SF/OF			
class mllBins:
	class lowMass:
		low = 20
		high = 70
	class onZ:
		low = 81
		high = 101
	class highMass:
		low = 120
		high = 1000		
	class belowZ:
		low = 70
		high = 81
	class aboveZ:
		low = 101
		high = 120
		
	class highMassRSFOF:
		low = 110
		high = 1000

### default regions (defined in defs.py) to be used by certain background prediction tools
### or for the determination of signal events		
class regionsToUse:
	class triggerEfficiencies:
		class central: 
			name = "HighHTExclusiveCentral"
		class forward: 
			name = "HighHTExclusiveForward"
		class inclusive: 
			name = "HighHTExclusive"
	class rMuE:
		class central: 
			name = "ZPeakControlCentral"
		class forward: 
			name = "ZPeakControlForward"
		class inclusive: 
			name = "ZPeakControl"
	class rOutIn:
		class central: 
			name = "DrellYanControlCentral"
		class forward: 
			name = "DrellYanControlForward"
		class inclusive: 
			name = "DrellYanControl"
	class rSFOF:
		class central: 
			name = "ControlCentral"
		class forward: 
			name = "ControlForward"
		class inclusive: 
			name = "Control"
	class signal:
		class central: 
			name = "SignalCentral"
		class forward: 
			name = "SignalForward"
		class inclusive: 
			name = "SignalInclusive"

### default run range
class runRanges:
	name = "Run2015_25ns"

### default MC backgrounds to use (have to be define in defs.py).
### Some tools/studies only use some of them
class backgroundLists:
	default = ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
	#~ default = ["TT_Powheg","DrellYan"]
	trigger = ["TT_Powheg","DrellYan"]
	rSFOF = ["TT_Powheg","DrellYan"]
	rareStudies = ["WW","WZ","ZZ","RareNonZ","RareZ"]

### default plots for certain tools (have to be define in defs.py).
### More control plots for different uncertainty tools can/should be added
class plotLists:
	default = ["mllPlot"]
	trigger = ["leadingPtPlotTrigger","trailingPtPlotTrigger","mllPlotTrigger"]
	rSFOF = ["mllPlot"]
	signal = ["mllPlot"]
	rMuE = ["nJetsPlotRMuE","nBJetsPlotRMuE","leadingPtPlotRMuE","trailingPtPlotRMuE","mllPlotRMuE","htPlotRMuE","metPlotRMuE","tralingEtaPlotRMuE"]
	rOutIn =  ["metPlotROutIn","nJetsPlotROutIn"]
	
### List of additional cut regions to look at in the signal region
### Can be extended for additional studies
class cutNCountXChecks:
	cutList = {"bTags":["noBTags","OneBTags","TwoBTags","geOneBTags"]}


### cut version and MasterList file used at the moment
class versions:
	cuts = "cutsV31"
	masterListForMC = "../frameWorkBase/MasterList.ini"

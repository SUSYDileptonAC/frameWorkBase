

class zPredictions:

	class SF:
		class central:
			val = 17
			err = 17
		class forward:
			val = 11
			err = 11
	class EE:
		class central:
			val = 5
			err = 5
		class forward:
			val = 4
			err = 4
	class MM:
		class central:
			val = 12
			err = 12
		class forward:
			val = 7
			err = 7


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

class runRanges:
	name = "Run2015_25ns"

class backgroundLists:
	#~ default = ["Rare","SingleTop","TTJets_SpinCorrelations","Diboson","DrellYanTauTau","DrellYan"]
	default = ["TT_Powheg","DrellYan"]
	#~ trigger = ["TTJets_SpinCorrelations"]
	trigger = ["TT_Powheg"]
	iso = ["TT_Powheg","DrellYan"]
	rSFOF = ["TT_Powheg","DrellYan"]
	nonPrompt = ["TT_Powheg","DrellYan"]
	Loose = ["TT_Powheg","DrellYan"]
	#~ Loose = ["DrellYan"]
	rareStudies = ["WW","WZ","ZZ","RareNonZ","RareZ"]
	
class plotLists:
	default = ["mllPlot","metPlot","htPlot","tralingEtaPlot","trailingPtPlot","nJetsPlot","leadingJetPtPlot","nBJetsPlot"]
	#~ default = ["tralingEtaPlot","trailingPtPlot","nJetsPlot","leadingJetPtPlot","nBJetsPlot"]
	#~ default = ["leadingPtPlot"]
	#~ trigger = ["nJetsPlotTrigger","leadingPtPlotTriggerTrailing10","leadingPtPlotTrigger","leadingPtPlotTrigger2515","leadingPtPlotTrigger2520","leadingPtPlotTrigger2525","trailigPtPlotTrigger","trailigPtPlotTrigger2515","trailigPtPlotTrigger2520","trailigPtPlotTrigger2525","trailigPtPlotTriggerLeading30","mllPlotTrigger","mllPlotTrigger2515","mllPlotTrigger2520","mllPlotTrigger2525","htPlotTrigger","metPlotTrigger","nVtxPlotTrigger","tralingEtaPlotTrigger"]
	trigger = ["nBJetsPlotTrigger","nJetsPlotTrigger","leadingPtPlotTrigger","trailingPtPlotTrigger","mllPlotTrigger","htPlotTrigger","metPlotTrigger","nVtxPlotTrigger","tralingEtaPlotTrigger"]
	#~ trigger = ["htPlotTrigger"]
	iso = ["leadingPtPlotTrigger","trailingPtPlotTrigger","mllPlotTrigger","nVtxPlotTrigger"]
	rSFOF = ["mllPlot"]
	signal = ["mllPlot"]
	#~ rMuE = ["nJetsPlotRMuE","nBJetsPlotRMuE","leadingPtPlotRMuE","trailingPtPlotRMuE","trailingPtPlotRMuELeading30","mllPlotRMuE","htPlotRMuE","metPlotRMuE","nVtxPlotRMuE","tralingEtaPlotRMuE","deltaRPlotRMuE"]
	rMuE = ["nJetsPlotRMuE","nBJetsPlotRMuE","leadingPtPlotRMuE","trailingPtPlotRMuE","mllPlotRMuE","htPlotRMuE","metPlotRMuE","nVtxPlotRMuE","tralingEtaPlotRMuE","deltaRPlotRMuE"]
	#~ rMuE = ["leadingPtPlotRMuE","trailingPtPlotRMuE","mllPlotRMuE","nVtxPlotRMuE"]
	rOutIn =  ["metPlotROutIn","nJetsPlotROutIn"]
	fake =  ["trailingPtPlot100","tralingEtaPlot","metPlot","htPlot",]

class baselineTrigger: 
	name = "PFHT"

class cutNCountXChecks:
	cutList = {"leptonPt":["pt2010","pt3020","pt3010","pt3030"],"pileUpCuts":["lowPU","midPU","highPU"],"isoCuts":["TightIso"],"bTags":["noBTags","OneBTags","TwoBTags","geOneBTags","geTwoBTags"],"htCuts":["ht100to300","ht300"]}



class versions:
	cmssw = "sw7412"
	cuts = "cutsV27"
	masterListForMC = "Master74X_25nsMC.ini"

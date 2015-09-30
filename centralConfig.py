

class zPredictions:

	class SF:
		class central:
			val = 116*1.03
			err = (21**2 + (116*0.03)**2)**0.5
		class forward:
			val = 42*1.03
			err = (9**2 + (42*0.03)**2)**0.5
	class EE:
		class central:
			val = 60.7*1.03
			err = (11.2**2 + (60.7*0.03)**2)**0.5
		class forward:
			val = 21*1.03
			err = (5**2 + (21*0.03)**2)**0.5
	class MM:
		class central:
			val = 56.8*1.03
			err = (10.7**2 + (56.8*0.03)**2)**0.5
		class forward:
			val = 25*1.03
			err = (6**2 + (25*0.03)**2)**0.5


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
	name = "EarlyData2015"

class backgroundLists:
	#~ default = ["Rare","SingleTop","TTJets_SpinCorrelations","Diboson","DrellYanTauTau","DrellYan"]
	default = ["TTJets","DrellYan"]
	#~ trigger = ["TTJets_SpinCorrelations"]
	trigger = ["TTJets","DrellYan"]
	iso = ["TTJets","DrellYan"]
	rSFOF = ["TTJets","DrellYan"]
	nonPrompt = ["TTJets","DrellYan"]
	Loose = ["TTJets","DrellYan"]
	#~ Loose = ["DrellYan"]
	rareStudies = ["WW","WZ","ZZ","RareNonZ","RareZ"]
	
class plotLists:
	default = ["mllPlot","metPlot","htPlot","tralingEtaPlot","trailingPtPlot","nJetsPlot","leadingJetPtPlot","nBJetsPlot"]
	#~ default = ["leadingPtPlot"]
	#~ trigger = ["nJetsPlotTrigger","leadingPtPlotTriggerTrailing10","leadingPtPlotTrigger","leadingPtPlotTrigger2515","leadingPtPlotTrigger2520","leadingPtPlotTrigger2525","trailigPtPlotTrigger","trailigPtPlotTrigger2515","trailigPtPlotTrigger2520","trailigPtPlotTrigger2525","trailigPtPlotTriggerLeading30","mllPlotTrigger","mllPlotTrigger2515","mllPlotTrigger2520","mllPlotTrigger2525","htPlotTrigger","metPlotTrigger","nVtxPlotTrigger","tralingEtaPlotTrigger"]
	trigger = ["nJetsPlotTrigger","leadingPtPlotTrigger","trailingPtPlotTrigger","mllPlotTrigger","htPlotTrigger","metPlotTrigger","nVtxPlotTrigger","tralingEtaPlotTrigger"]
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
	name = "HT"

class cutNCountXChecks:
	cutList = {"leptonPt":["pt2010","pt3020","pt3010","pt3030"],"pileUpCuts":["lowPU","midPU","highPU"],"isoCuts":["TightIso"],"bTags":["noBTags","OneBTags","TwoBTags","geOneBTags","geTwoBTags"],"htCuts":["ht100to300","ht300"]}

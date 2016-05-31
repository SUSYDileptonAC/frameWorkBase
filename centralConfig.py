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

class zPredictions:
	class default:
		class SF:
			class central:
				val = 62.0
				err = 8.2
			class forward:
				val = 24.1
				err = 3.1
		class EE:
			class central:
				val = 5
				err = 5
			class forward:
				val = 2
				err = 2
		class MM:
			class central:
				val = 5
				err = 5
			class forward:
				val = 2
				err = 2
	class geOneBTags:
		class SF:
			class central:
				val = 15.6
				err = 2.2
			class forward:
				val = 6.0
				err = 1.3
		class EE:
			class central:
				val = 2
				err = 2
			class forward:
				val = 1
				err = 1
		class MM:
			class central:
				val = 2
				err = 2
			class forward:
				val = 1
				err = 1
	class noBTags:
		class SF:
			class central:
				val = 46.4
				err = 7.9
			class forward:
				val = 18.1
				err = 2.8
		class EE:
			class central:
				val = 2
				err = 2
			class forward:
				val = 1
				err = 1
		class MM:
			class central:
				val = 2
				err = 2
			class forward:
				val = 1
				err = 1
	class geTwoBTags:
		class SF:
			class central:
				val = 2.3
				err = 1.8
			class forward:
				val = 0.8
				err = 0.8
		class EE:
			class central:
				val = 1
				err = 1
			class forward:
				val = 1
				err = 1
		class MM:
			class central:
				val = 1
				err = 1
			class forward:
				val = 1
				err = 1
	class eleLeading:
		class SF:
			class central:
				val = 1.7
				err = 0.51
			class forward:
				val = 0.7
				err = 0.31
		class EE:
			class central:
				val = 1
				err = 1
			class forward:
				val = 1
				err = 1
		class MM:
			class central:
				val = 1
				err = 1
			class forward:
				val = 1
				err = 1
	class muLeading:
		class SF:
			class central:
				val = 1.7
				err = 0.51
			class forward:
				val = 0.7
				err = 0.31
		class EE:
			class central:
				val = 1
				err = 1
			class forward:
				val = 1
				err = 1
		class MM:
			class central:
				val = 1
				err = 1
			class forward:
				val = 1
				err = 1


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
	class belowZ:
		low = 70
		high = 81
	class aboveZ:
		low = 101
		high = 120
		
	class highMassRSFOF:
		low = 110
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
	trigger = ["TT_Powheg"]
	rSFOF = ["TT_Powheg","DrellYan"]
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


class cutNCountXChecks:
	cutList = {"leptonPt":["pt2010","pt3020","pt3010","pt3030"],"pileUpCuts":["lowPU","midPU","highPU"],"bTags":["noBTags","OneBTags","TwoBTags","geOneBTags","geTwoBTags"],"htCuts":["ht100to300","ht300"]}



class versions:
	cmssw = "sw7414"
	cuts = "cutsV31"
	masterListForMC = "../frameWorkBase/MasterList.ini"

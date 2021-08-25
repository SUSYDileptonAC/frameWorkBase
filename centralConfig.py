from baseClasses import maplike

class OtherPredictions:
        class MT2:
                class SF:
                        class inclusive:
                                val = 84.0
                                err = 84.0*0.25
                        class lowNLL:
                                val = 31.5
                                err = 31.5*0.25
                        class highNLL:
                                val = 52.5
                                err = 52.5*0.25
                

class OnlyZPredictions:
        class MT2:
                class SF:
                        class zeroB:  
                                class inclusive:
                                        val = 148.1#144.8
                                        err = 54.9
                                class lowNLL:
                                        val = 148.1*0.72
                                        err = 54.9*0.72
                                class highNLL:
                                        val = 148.1*0.28
                                        err = 54.9*0.28
                        class oneB:
                                class inclusive:
                                        val = 93.3#85.0
                                        err = 36.2
                                class lowNLL:
                                        val = 93.3*0.72
                                        err = 36.2*0.72
                                class highNLL:
                                        val = 93.3*0.28
                                        err = 36.2*0.28
                                
                                
                

class zPredictions:
        # only used when dicing toys. Update this from fit pkls before doing toy studies
        class Fit:
                class SF:
                        class inclusive:
                                val = 448 # for data
                                #val = 414 # for MC
                                err = 0

                        


class systematics:
        class rSFOF(maplike):
                class for2016:
                        class inclusive:
                                val = 0.04    
                class for2017:
                        class inclusive:
                                val = 0.04
                class for2018:
                        class inclusive:
                                val = 0.04
  
        class rMuE(maplike):
                class for2016:
                        class flat:
                                val = 0.05
                        class ptdep:
                                val = 0.05
                        class etadep:
                                val = 0.05
                        class inclusive:
                                val = 0.1
                        class central:
                                val = 0.1
                        class forward:
                                val = 0.1       
                class for2017:
                        class flat:
                                val = 0.05
                        class ptdep:
                                val = 0.05
                        class etadep:
                                val = 0.05
                        class inclusive:
                                val = 0.1
                        class central:
                                val = 0.1
                        class forward:
                                val = 0.1       
                class for2018:
                        class flat:
                                val = 0.05
                        class ptdep:
                                val = 0.05
                        class etadep:
                                val = 0.05
                        class inclusive:
                                val = 0.1
                        class central:
                                val = 0.1
                        class forward:
                                val = 0.1       
        class trigger(maplike):
                class for2016:
                        class inclusive:
                                val = 0.03
                class for2017:
                        class inclusive:
                                val = 0.03
                class for2018:
                        class inclusive:
                                val = 0.03
        class rOutIn(maplike):
                class for2016:
                        class old:
                                val = 0.25
                        class massBelow150:
                                val = 0.5               
                        class massAbove150:
                                val = 1.                
                class for2017:
                        class old:
                                val = 0.25
                        class massBelow150:
                                val = 0.5               
                        class massAbove150:
                                val = 1.                
                class for2017:
                        class old:
                                val = 0.25
                        class massBelow150:
                                val = 0.5               
                        class massAbove150:
                                val = 1.                
                class for2018:
                        class old:
                                val = 0.25
                        class massBelow150:
                                val = 0.5               
                        class massAbove150:
                                val = 1.                
                class combined:
                        class mass20To60:
                                val = 0.5              
                        class massBelow150:
                                val = 0.5               
                        class massAbove150:
                                val = 1.                
                                
class mllBins:
        
        class mass20To60:
                low = 20
                high = 60
        class mass60To86:
                low = 60
                high = 86
        class onZ:
                low = 86
                high = 96
        class mass96To150:
                low = 96
                high = 150
        class mass150To200:
                low = 150
                high = 200
        class mass200To300:
                low = 200
                high = 300
        class mass300To400:
                low = 300
                high = 400
        class mass400:
                low = 400
                high = 2000
                
        
        class edgeMass:
                low = 20
                high = 70
        class lowMassOld:
                low = 20
                high = 81
        class lowMass:
                low = 20
                high = 86
        class highMassOld:
                low = 101
                high = 5000     
        class highMass:
                low = 96
                high = 5000     
        class highMassRSFOF:
                low = 110
                high = 2000
                
class mllBinsOld:
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
        class triggerEfficiencies: # deprecated
                class central: 
                        name = "HighHTExclusiveCentral"
                class forward: 
                        name = "HighHTExclusiveForward"
                class inclusive: 
                        name = "HighMETExclusive"
                class met:
                        name = "HighMETExclusive"
                class metForward:
                        name = "HighMETExclusiveForward"
                class metCentral:
                        name = "HighMETExclusiveCentral"
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
                class legacy: 
                        name = "SignalCentralOld"
                class ICHEP: 
                        name = "SignalHighNLL"
                class inclusive: 
                        name = "SignalInclusive"
                class Moriond: 
                        name = "SignalHighMT2DeltaPhiJetMet"
                class MoriondLowNLL: 
                        name = "SignalLowNLLHighMT2DeltaPhiJetMet"
                class MoriondHighNLL: 
                        name = "SignalHighNLLHighMT2DeltaPhiJetMet"

class triggerRegionNamesLists(maplike):
        class for2016(maplike):
                class inclusive:
                        name = "HighMETExclusive"
                class forward:
                        name = "HighMETExclusive"
                class central:
                        name = "HighMETExclusive"
        class for2017(maplike):
                class inclusive:
                        name = "HighMETExclusive"
                class forward:
                        name = "HighMETExclusive"
                class central:
                        name = "HighMETExclusive"
        class for2018(maplike):
                class inclusive:
                        name = "HighMETExclusive"
                class forward:
                        name = "HighMETExclusive"
                class central:
                        name = "HighMETExclusive"

# era to runRange
class runRanges(maplike):
        class for2016(maplike):
                name = "Run2016_36fb"
        class for2017(maplike):
                name = "Run2017_42fb"
        class for2018(maplike):
                name = "Run2018_60fb"
#runRanges.name = runRanges["2016"].name
runRanges.allNames = [runRanges["2016"]["name"], runRanges["2017"]["name"], runRanges["2018"]["name"]]



class backgroundLists:
        default = ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
        #~ default = ["OtherSM","SingleTop","DrellYanTauTau","RareOnZ","TT_Powheg","ZJets","DrellYanNonResonant"]
        #~ default = ["TT_Powheg","DrellYan"]
        #trigger = ["TT_Powheg","DrellYan"]
        trigger = ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
        iso = ["TT_Powheg","DrellYan"]
        #~ rSFOF = ["TT_Powheg"]
        rSFOF = ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
        nonPrompt = ["TT_Powheg","DrellYan"]
        Loose = ["TT_Powheg","DrellYan"]
        rareStudies = ["WW","WZ","ZZ","RareNonZ","RareZ"]
        
class plotLists:
        #~ default = ["mllPlot","metPlot","htPlot","tralingEtaPlot","trailingPtPlot","nJetsPlot","nBJetsPlot","nVtxPlot","deltaPhiPlot","ptllPlot","sumMlbPlot","leadingPtPlot","mt2Plot"]
        #~ default = ["mllPlot","metPlot","nJetsPlot","mt2Plot"]
        default = ["mllPlot"]
        trigger = ["nBJetsPlotTrigger","nJetsPlotTrigger","leadingPtPlotTrigger","leadingEtaPlotTrigger","trailingPtPlotTrigger","mllPlotTrigger","htPlotTrigger","metPlotTrigger","nVtxPlotTrigger","tralingEtaPlotTrigger","ptllPlotTrigger","deltaPhiPlotTrigger","sumMlbPlotTrigger","mt2PlotTrigger"]
        #trigger = ["mllPlotTrigger",]
        #trigger = ["trailingPtPlotTrigger","leadingPtPlotTrigger"]
        iso = ["leadingPtPlotTrigger","trailingPtPlotTrigger","mllPlotTrigger","nVtxPlotTrigger"]
        #~ rSFOF = ["mllPlotRSFOF","metPlotRSFOF","nJetsPlotRSFOF","nBJetsPlotRSFOF","htPlotRSFOF","trailingPtPlotRSFOF","leadingPtPlotRSFOF","mt2PlotRSFOF","ptllPlotRSFOF","deltaPhiPlotRSFOF","sumMlbPlotRSFOF","nLLPlotRSFOF","nVtxPlotRSFOF"]
        rSFOF = ["mllPlotRSFOF","metPlotRSFOF","nJetsPlotRSFOF","nBJetsPlotRSFOF","htPlotRSFOF","trailingPtPlotRSFOF","leadingPtPlotRSFOF","mt2PlotRSFOF","ptllPlotRSFOF","deltaPhiPlotRSFOF","sumMlbPlotRSFOF","nVtxPlotRSFOF"]
        #rSFOF = ["trailingPtPlotRSFOF","leadingPtPlotRSFOF"]
        signal = ["mllPlotROutIn"]
        rMuE = ["negativePtPlotRMuE", "positivePtPlotRMuE", "positiveEtaPlotRMuE", "negativeEtaPlotRMuE", "mllPlotRMuE","leadingPtPlotRMuE","nJetsPlotRMuE","mt2PlotRMuE","metPlotRMuE","nVtxPlotRMuE","nBJetsPlotRMuE","leadingEtaPlotRMuE","trailingPtPlotRMuE","htPlotRMuE","tralingEtaPlotRMuE","deltaRPlotRMuE","ptllPlotRMuE","deltaPhiPlotRMuE","sumMlbPlotRMuE"]
        #rMuE = ["leadingPtPlotRMuE","negativePtPlotRMuE", "positivePtPlotRMuE", "positiveEtaPlotRMuE", "negativeEtaPlotRMuE",]
        #rMuE = ["leadingPtPlotRMuE",]
        #rMuE = ["negativePtPlotRMuE", "positivePtPlotRMuE", "positiveEtaPlotRMuE", "negativeEtaPlotRMuE",]
        #rMuE = ["nVtxPlotRMuE",]
        #rMuE = ["leadingPtPlotRMuE","trailingPtPlotRMuE"]
        #~ rMuE = ["trailingPtPlotRMuE"]
        rOutIn =  ["metPlotROutIn","nJetsPlotROutIn","mt2PlotROutIn"]
        fake =  ["trailingPtPlot100","tralingEtaPlot","metPlot","htPlot",]

class baselineTrigger: 
        name = "PFHT"

class cutNCountXChecks:
        cutList = {"NLL":["inclusive","lowNLL","highNLL"],"Legacy":["legacy"]}



class versions:
        cmssw = "sw8026" # Shouldnt be used anymore, remove where possible
        cuts = "cutsV34" # Shouldnt be used anymore, remove where possible
        masterListForMC = [ "Master94X_2016_MC.ini", "Master94X_2017_MC.ini", "Master102X_2018_MC.ini"] # "Master80X_MC_Summer16.ini",
        signalCrossSections = {"T6bbllslepton":"sbottom_xsecs.ini", "T6qqllslepton":"squarks_xsecs.ini"}

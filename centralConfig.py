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
                                
        class ICHEP:
                class SF:
                        class inclusive:
                                val = 45.3
                                err = 8.0
                        class lowNLL:
                                val = 45.3
                                err = 8.0
                        class highNLL:
                                val = 45.3
                                err = 8.0
                
        class legacy:
                class SF:
                        class central:
                                val = 45.3
                                err = 8.0
                

class OnlyZPredictions:
        class MT2:
                class SF:
                        class inclusive:
                                val = 19.4
                                err = 11.7
                        class lowNLL:
                                val = 19.4 * 0.36
                                err = 11.7 * 0.36
                        class highNLL:
                                val = 19.4 * 0.64
                                err = 11.7 * 0.64
                                
        class ICHEP:
                class SF:
                        class inclusive:
                                val = 45.3
                                err = 8.0
                        class lowNLL:
                                val = 45.3
                                err = 8.0
                        class highNLL:
                                val = 45.3
                                err = 8.0
                
        class legacy:
                class SF:
                        class central:
                                val = 45.3
                                err = 8.0
                

class zPredictions:
        class MT2:
                class SF:
                        class inclusive:
                                val = 100.4
                                err = 28.5
                        class lowNLL:
                                val = 100.4 * 0.36
                                err = 28.5 * 0.36
                        class highNLL:
                                val = 100.4 * 0.64
                                err = 28.5 * 0.64
        class ICHEP:
                class SF:
                        class inclusive:
                                val = 188.8
                                err = 44.2
                        class lowNLL:
                                val = 188.8 * 0.65
                                err = 44.2 * 0.65
                        class highNLL:
                                val = 188.8 * 0.35
                                err = 44.2 * 0.35
                                
        class legacy:
                class SF:
                        class central:
                                val = 391.5
                                err = 38.5
                        


class systematics:
        class rSFOF:
                class inclusive:
                        val = 0.04
                class central:
                        val = 0.04
                class forward:
                        val = 0.06      
        class rMuE:
                class inclusive:
                        val = 0.1
                class central:
                        val = 0.1
                class forward:
                        val = 0.1       
        class trigger:
                class inclusive:
                        val = 0.03
                class central:
                        val = 0.03
                class forward:
                        val = 0.03
        class rOutIn:
                class old:
                        val = 0.25
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

class runRanges:
        name = "Run2016_36fb"

class backgroundLists:
        default = ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
        #~ default = ["OtherSM","SingleTop","DrellYanTauTau","RareOnZ","TT_Powheg","ZJets","DrellYanNonResonant"]
        #~ default = ["TT_Powheg","DrellYan"]
        trigger = ["TT_Powheg","DrellYan"]
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
        #~ trigger = ["nBJetsPlotTrigger","nJetsPlotTrigger","leadingPtPlotTrigger","leadingEtaPlotTrigger","trailingPtPlotTrigger","mllPlotTrigger","htPlotTrigger","metPlotTrigger","nVtxPlotTrigger","tralingEtaPlotTrigger","ptllPlotTrigger","deltaPhiPlotTrigger","sumMlbPlotTrigger","mt2PlotTrigger"]
        trigger = ["trailingPtPlotTrigger","leadingPtPlotTrigger"]
        iso = ["leadingPtPlotTrigger","trailingPtPlotTrigger","mllPlotTrigger","nVtxPlotTrigger"]
        #~ rSFOF = ["mllPlotRSFOF","metPlotRSFOF","nJetsPlotRSFOF","nBJetsPlotRSFOF","htPlotRSFOF","trailingPtPlotRSFOF","leadingPtPlotRSFOF","mt2PlotRSFOF","ptllPlotRSFOF","deltaPhiPlotRSFOF","sumMlbPlotRSFOF","nLLPlotRSFOF","nVtxPlotRSFOF"]
        #~ rSFOF = ["mllPlotRSFOF","metPlotRSFOF","nJetsPlotRSFOF","nBJetsPlotRSFOF","htPlotRSFOF","trailingPtPlotRSFOF","leadingPtPlotRSFOF","mt2PlotRSFOF","ptllPlotRSFOF","deltaPhiPlotRSFOF","sumMlbPlotRSFOF","nVtxPlotRSFOF"]
        rSFOF = ["trailingPtPlotRSFOF","leadingPtPlotRSFOF"]
        signal = ["mllPlotROutIn"]
        #~ rMuE = ["mllPlotRMuE","leadingPtPlotRMuE","nJetsPlotRMuE","mt2PlotRMuE","metPlotRMuE","nVtxPlotRMuE","nBJetsPlotRMuE","leadingEtaPlotRMuE","trailingPtPlotRMuE","htPlotRMuE","tralingEtaPlotRMuE","deltaRPlotRMuE","ptllPlotRMuE","deltaPhiPlotRMuE","sumMlbPlotRMuE"]
        #~ rMuE = ["mllPlotRMuE"]
        rMuE = ["leadingPtPlotRMuE","trailingPtPlotRMuE"]
        #~ rMuE = ["trailingPtPlotRMuE"]
        rOutIn =  ["metPlotROutIn","nJetsPlotROutIn","mt2PlotROutIn"]
        fake =  ["trailingPtPlot100","tralingEtaPlot","metPlot","htPlot",]

class baselineTrigger: 
        name = "PFHT"

class cutNCountXChecks:
        cutList = {"NLL":["inclusive","lowNLL","highNLL"],"Legacy":["legacy"]}



class versions:
        cmssw = "sw8026"
        cuts = "cutsV34"
        masterListForMC = ["Master80X_MC_Summer16.ini", "Master94X_MC.ini"]

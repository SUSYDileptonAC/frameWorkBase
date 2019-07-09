from math import sqrt
import ROOT
from ROOT import TMath
import sys
import copy
from corrections import triggerEffs
from baseClasses import maplike

class runRanges:
        class Run2012:
                lumi = 19518
                printval = "19.5"
                lumiErr = 0.026*19518
                runCut = "&& runNr < 99999999"
                label = "Full2012"
                era = "2012"
                weight = None
                
        class Run2011:
                lumi = 4980
                printval = "5.0"
                lumiErr = 0.045*4980
                runCut = "&& runNr < 99999999"
                label = "2011"
                era = "2011"
                weight = None
                
        class Run2015_25ns:
                lumi = 2260
                printval = "2.3"
                lumiErr = 0.045*2260
                runCut = "&& deltaR > 0.3 && miniIsoEffArea1 < 0.1 && miniIsoEffArea2 < 0.1 && runNr < 99999999 "
                label = "Run2015_25ns"
                era = "2015"
                weight = None
                
        class Run2016_36fb:
                lumi = 35867.
                printval = "35.9"
                lumiErr = 0.025*35867.
                runCut = "&& ( (runNr >= 271036 && runNr <= 284044) || runNr ==1)"
                label = "Run2016_36fb"
                era = "2016"
                weight = None #"prefireWeight"
                
        class Run2016_140fb:
                lumi = 140000.
                printval = "140"
                lumiErr = 0.025*140000.
                runCut = "&& ( (runNr >= 271036 && runNr <= 284044) || runNr ==1)"
                label = "Run2016_140fb"
                era = "2016"
                weight = "prefireWeight"
                
        class Run2016G_4_4fb:
                lumi = 4400.
                printval = "4.4"
                lumiErr = 0.045*4400.
                runCut = "&& ( (runNr >= 278820 && runNr <= 279931) || runNr ==1)"
                label = "Run2016G_4_4fb"
                era = "2016"
                weight = "prefireWeight"

        class Run2016_12_9fb:
                lumi = 12900.
                printval = "12.9"
                lumiErr = 0.045*12900.
                runCut = "&& ( (runNr >= 271036 && runNr <= 276811) || runNr ==1)"
                label = "Run2016_12_9fb"
                era = "2016"
                weight = "prefireWeight"
                                
        class Run2016_17fb_Unblinded:
                lumi = 17300.
                printval = "17.3"
                lumiErr = 0.045*17300.
                runCut = "&& ( (runNr >= 271036 && runNr <= 276811) || (runNr >= 278820 && runNr <= 279931) || runNr ==1)"
                label = "Run2016_17fb_Unblinded"
                era = "2016"
                weight = "prefireWeight"

        class Run2017_42fb:
                lumi = 41529.
                printval = "41.5"
                lumiErr = 0.023*41529.
                runCut = "&& ( (runNr >= 297050 && runNr <= 306460) || runNr ==1)"
                label = "Run2017_42fb"
                era = "2017"
                weight = "prefireWeight"
                
        class Run2018_60fb:
                lumi = 59740.
                printval = "59.7"
                lumiErr = 0.025*59740.
                runCut = "&& ( (runNr >= 315257 && runNr <= 325172) || runNr ==1)" # 
                label = "Run2018_60fb"
                era = "2018"
                weight = None
        
                
class Region:
        ### normal trees ## && metFilterSummary > 0 
        #cut = "met / caloMet < 5 && nBadMuonJets == 0 && p4.Pt() > 25 && chargeProduct < 0 && ((pt1 > 25 && pt2 > 20) || (pt1 > 20 && pt2 > 25))  && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && p4.M() > 20 && deltaR > 0.1" # && deltaPhiJetMET > 0.4
        ### trees with likelihood &&   met / caloMet < 5 && nBadMuonJets == 0 &&
        
        # && triggerSummary > 0 && metFilterSummary > 0 
        #cut = "triggerSummary > 0 && metFilterSummary > 0  && pt > 25 && chargeProduct < 0 && (pt1 > 25 || pt2 > 25) && mll > 20 && deltaR > 0.1"
        cut = "pt > 25 && chargeProduct < 0 && (pt1 > 25 || pt2 > 25) && mll > 20 && deltaR > 0.1"
        #cut = "p4.Pt() > 25 && chargeProduct < 0 && (pt1 > 25 || pt2 > 25) && mll > 20 && deltaR > 0.1"
        cutNLL = "met / caloMet < 5 && nBadMuonJets == 0 && pt > 25 && chargeProduct < 0 && ((pt1 > 25 && pt2 > 20) || (pt1 > 20 && pt2 > 25))  && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && mll > 20 && deltaR > 0.1"
        cutToUse = "genWeight*weight*(chargeProduct < 0 && ((pt1 > 25 && pt2 > 20) || (pt1 > 20 && pt2 > 25)) && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.1)"
        #~ cutToUse = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*genWeight*weight*(chargeProduct < 0 && ((pt1 > 25 && pt2 > 20) || (pt1 > 20 && pt2 > 25)) && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.1)"
        #~ cutToUse = "genWeight*weight*(chargeProduct < 0 && ((pt1 > 25 && pt2 > 20) || (pt1 > 20 && pt2 > 25)) && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.1)"
        title = "Inclusive dilepton selection"
        latex = "Inclusive dilepton selection"
        labelRegion = "p_{T}^{l} > 20 GeV |#eta^{l}| < 2.4"
        name = "Inclusive"
        labelSubRegion = ""
        dyPrediction = {}
        logY = True
        trigEffs = triggerEffs.inclusive
        
class allCuts:
        class genMatchCuts:
                class leptonMinusMatch:
                        cut = "leptonMinusMatch == 1"
                        label = "l matched"
                        name = "leptonMinusMatch"   
                class leptonPlusMatch:
                        cut = "leptonPlusMatch == 1"
                        label = "#bar{l} matched"
                        name = "leptonPlusMatch"   
                class bJetMatch:
                        cut = "bJetMatch == 1"
                        label = "b matched"
                        name = "bJetMatch"   
                class bbarJetMatch:
                        cut = "bbarJetMatch == 1"
                        label = "#bar{b} matched"
                        name = "bbarJetMatch"   
                class genBJetMatch:
                        cut = "genBJetMatch == 1"
                        label = "gen b matched"
                        name = "genBJetMatch"   
                class genBbarJetMatch:
                        cut = "genBbarJetMatch == 1"
                        label = "gen #bar{b} matched"
                        name = "genBbarJetMatch"   
                class promptNuMatch:
                        cut = "genNPromptN == 2"
                        label = "two prompt neutrinos"
                        name = "promptNuMatch"  
        class nuSolCuts:
                class hasNuSols:
                        cut = "nNuSols > 0"
                        label = "N_{#nu sols} > 0"
                        name = "hasNuSols"        
        class massCuts:
                class default:
                        cut = "p4.M() > 20"
                        label = "m_{ll} = 20 GeV"
                        name = "fullMassRange"
                class edgeMass:
                        cut = "p4.M()> 20 && p4.M() < 70"
                        label = "20 GeV < m_{ll} < 70 GeV"
                        name = "edgeMass"
                class lowMassOld:
                        cut = "p4.M()> 20 && p4.M() < 81"
                        label = "20 GeV < m_{ll} < 81 GeV"
                        name = "lowMassOld"
                class lowMass:
                        cut = "p4.M()> 20 && p4.M() < 86"
                        label = "20 GeV < m_{ll} < 86 GeV"
                        name = "lowMass"
                class zMass:
                        cut = "p4.M()> 86 && p4.M() < 96"
                        label = "86 GeV < m_{ll} < 96 GeV"
                        name = "zMass"
                class looseZ:
                        cut = "p4.M()> 70 && p4.M() < 110"
                        label = "70 GeV < m_{ll} < 110 GeV"
                        name = "looseZ"
                class highMass:
                        cut = "p4.M() > 96"
                        label = "m_{ll} > 96 GeV"
                        name = "highMass"
                class highMassOld:
                        cut = "p4.M() > 101"
                        label = "m_{ll} > 101 GeV"
                        name = "highMassOld"
                class lowAndZMass:
                        cut = "p4.M()> 20 && p4.M() < 101"
                        label = "20 GeV < m_{ll} < 101 GeV"
                        name = "lowAndZMass"
                class mass100To200:
                        cut = "p4.M()> 101 && p4.M() < 200"
                        label = "101 GeV < m_{ll} < 200 GeV"
                        name = "mass100To200"
                class mass20To60:
                        cut = "p4.M()> 20 && p4.M() < 60"
                        label = "20 GeV < m_{ll} < 60 GeV"
                        name = "mass20To60"
                class mass60To86:
                        cut = "p4.M()> 60 && p4.M() < 86"
                        label = "60 GeV < m_{ll} < 86 GeV"
                        name = "mass60To86"
                class mass60To81:
                        cut = "p4.M()> 60 && p4.M() < 81"
                        label = "60 GeV < m_{ll} < 81 GeV"
                        name = "mass60To81"
                class mass81To101:
                        cut = "p4.M()> 81 && p4.M() < 101"
                        label = "81 GeV < m_{ll} < 101 GeV"
                        name = "mass81To101"
                class mass86To96:
                        cut = "p4.M()> 86 && p4.M() < 96"
                        label = "86 GeV < m_{ll} < 96 GeV"
                        name = "mass86To96"
                class mass96To150:
                        cut = "p4.M()> 96 && p4.M() < 150"
                        label = "96 GeV < m_{ll} < 150 GeV"
                        name = "mass96To150"
                class mass101To150:
                        cut = "p4.M()> 101 && p4.M() < 150"
                        label = "101 GeV < m_{ll} < 150 GeV"
                        name = "mass101To150"
                class mass150To200:
                        cut = "p4.M()> 150 && p4.M() < 200"
                        label = "150 GeV < m_{ll} < 200 GeV"
                        name = "mass150To200"
                class mass200To300:
                        cut = "p4.M()> 200 && p4.M() < 300"
                        label = "200 GeV < m_{ll} < 300 GeV"
                        name = "mass200To300"
                class mass300To400:
                        cut = "p4.M()> 300 && p4.M() < 400"
                        label = "300 GeV < m_{ll} < 400 GeV"
                        name = "mass300To400"
                class mass400:
                        cut = "p4.M()> 400"
                        label = "400 GeV < m_{ll}"
                        name = "massAbove400"
                        
        class ptCuts:
                class pt2010:
                        cut = "((pt1 > 20 && pt2 > 10)||(pt1 > 10 && pt2 > 20))"
                        label = "p_{T} > 20(10) GeV"
                        name = "pt2010"
                class eleLeading:
                        cut = "(pt1 > pt2)"
                        label = "electron leading"
                        name = "eleLeading"
                class muLeading:
                        cut = "(pt2 > pt1)"
                        label = "muon leading"
                        name = "muLeading"
                class pt2020:
                        cut = "pt1 > 20 && pt2 > 20"
                        label = "p_{T} > 20 GeV"
                        name = "pt2020"
                class pt2515:
                        cut = "((pt1 > 25 && pt2 > 15)||(pt1 > 15 && pt2 > 25))"
                        label = "p_{T} > 25(15) GeV"
                        name = "pt2515"
                class pt2520:
                        cut = "((pt1 > 25 && pt2 > 20)||(pt1 > 20 && pt2 > 25))"
                        label = "p_{T} > 25(20) GeV"
                        name = "pt2520"
                class pt2525:
                        cut = "pt1 > 25 && pt2 > 25"
                        label = "p_{T} > 25 GeV"
                        name = "pt2525"
                class pt3010:
                        cut = "((pt1 > 30 && pt2 > 10)||(pt1 > 10 && pt2 > 30))"
                        label = "p_{T} > 30(10) GeV"
                        name = "pt3010"
                class pt3015:
                        cut = "((pt1 > 30 && pt2 > 15)||(pt1 > 15 && pt2 > 30))"
                        label = "p_{T} > 30(15) GeV"
                        name = "pt3015"
                class pt3020:
                        cut = "((pt1 > 30 && pt2 > 20)||(pt1 > 20 && pt2 > 30))"
                        label = "p_{T} > 30(20) GeV"
                        name = "pt3020"
                class pt3030:
                        cut = "pt1 > 30 && pt2 > 30"
                        label = "p_{T} > 30 GeV"
                        name = "pt3030"
                class leadingPt30:
                        cut = "((pt1 > pt2)*(pt1 > 30)|| (pt2 > pt1)*(pt2 > 30))"
                        label = "leading p_{T} > 30 GeV"
                        name = "leadingPt30"
                class leadingPt40:
                        cut = "((pt1 > pt2)*(pt1 > 40)|| (pt2 > pt1)*(pt2 > 40))"
                        label = "leading p_{T} > 40 GeV"
                        name = "leadingPt40"

        class nJetsCuts:
                class noCut:
                        cut = "nJets >= 0"
                        label = ""
                        name = ""
                class geOneJetCut:
                        cut = "nJets >= 1"
                        label = "nJets #geq 1"
                        name = "ge1Jets"
                class geTwoJetCut:
                        cut = "nJets >= 2"
                        label = "nJets #geq 2"
                        name = "ge2Jets"
                class geThreeJetCut:
                        cut = "nJets >= 3"
                        label = "nJets #geq 3"
                        name = "ge3Jets"
                class noJet:
                        cut = "nJets == 0"
                        label = "nJets = 0"
                        name = "0Jets"
                class OneJet:
                        cut = "nJets == 1"
                        label = "nJets = 1"
                        name = "1Jets"
                class TwoJet:
                        cut = "nJets == 2"
                        label = "nJets = 2"
                        name = "2Jets"
                class ThreeJet:
                        cut = "nJets == 3"
                        label = "nJets = 3"
                        name = "3Jets"
                class FourJet:
                        cut = "nJets == 4"
                        label = "nJets = 4"
                        name = "4Jets"
        class metCuts:
                class noCut:
                        cut = "met >= 0"
                        label = ""
                        name = ""
                class met50:
                        cut = "met > 50"
                        label = "E_{T}^{miss} > 50 GeV"
                        name = "MET50"
                class met100:
                        cut = "met > 100"
                        label = "E_{T}^{miss} > 100 GeV"
                        name = "MET100"
                class met150:
                        cut = "met > 150"
                        label = "E_{T}^{miss} > 150 GeV"
                        name = "MET150"
                        
        class dRCuts:
                class lowDR:
                        cut = "deltaR < 1.5"
                        label = "#Delta R(ll) < 1.5"
                        name = "LowDR"
                class midDR:
                        cut = "deltaR > 1.5 && deltaR < 2.5"
                        label = "1.5 #Delta R(ll) < 2.5"
                        name = "MidDR"
                class highDR:
                        cut = "deltaR > 2.5"
                        label = "#Delta R(ll) > 2.5"
                        name = "HighDR"
                        
        class dPhiCuts:
                class lowDPhi:
                        cut = "abs(deltaPhi) < 1.0"
                        label = "#Delta #phi (ll) < 1.0"
                        name = "LowDPhi"
                class midDPhi:
                        cut = "abs(deltaPhi) > 1.0 && (deltaPhi) < 2.0"
                        label = "1.0 < #Delta #phi (ll) < 2.0"
                        name = "MidDPhi"
                class highDPhi:
                        cut = "abs(deltaPhi) > 2.0"
                        label = "#Delta #phi (ll) > 2.0"
                        name = "HighDPhi"

        class dEtaCuts:
                class lowDEta:
                        cut = "sqrt(deltaR^2 - deltaPhi^2) < 1.0"
                        label = "#Delta #eta (ll) < 1.0 "
                        name = "LowDEta"
                class midDEta:
                        cut = "sqrt(deltaR^2 - deltaPhi^2) > 1.0 && sqrt(deltaR^2 - deltaPhi^2) < 2.0"
                        label = "1.0 #Delta #eta (ll) < 2.0 "
                        name = "midDEta"
                class highDEta:
                        cut = "sqrt(deltaR^2 - deltaPhi^2) > 2.0 "
                        label = "#Delta #eta (ll) > 2.0 "
                        name = "highDEta"

        class etaCuts:
                class inclusive:
                        cut = "abs(eta1) < 2.4 && abs(eta2) < 2.4"
                        label = "|#eta| < 2.4"
                        name = "FullEta"
                class Barrel:
                        cut = "abs(eta1) < 1.4 && abs(eta2) < 1.4"
                        label = "|#eta| < 1.4"
                        name = "Barrel"
                class Endcap:
                        cut = "1.4 <= TMath::Max(abs(eta1),abs(eta2))"
                        label = "at least one |#eta| > 1.4"
                        name = "Endcap"
                class BothEndcap:
                        cut = "abs(eta1) > 1.4 && abs(eta2) > 1.4"
                        label = "|#eta| > 1.4"
                        name = "BothEndcap"
                class CentralBarrel:
                        cut = "abs(eta1) < 0.8 && abs(eta2) < 0.8"
                        label = "|#eta| < 0.8"
                        name = "CentralBarrel"
                class OuterBarrel:
                        cut = "abs(eta1) > 0.8 && abs(eta2) > 0.8 && abs(eta1) < 1.4 && abs(eta2) < 1.4"
                        label = "0.8 < |#eta| < 1.4"
                        name = "CentralBarrel"

        class isoCuts:
                class TightIso:
                        cut = "miniIsoEffArea1 < 0.05 && miniIsoEffArea2 < 0.05"
                        label = "rel. iso. < 0.05"
                        name = "TightIso"

        class bTags:
                class noBTags:
                        cut = "nBJets == 0"
                        label = "nBJets = 0"
                        name = "noBJets"
                class OneBTags:
                        cut = "nBJets == 1"
                        label = "nBJets = 1"
                        name = "OneBJets"
                class TwoBTags:
                        cut = "nBJets == 2"
                        label = "nBJets = 2"
                        name = "TwoBJets"
                class ThreeBTags:
                        cut = "nBJets == 3"
                        label = "nBJets = 3"
                        name = "ThreeBJets"
                class geOneBTags:
                        cut = "nBJets >= 1"
                        label = "nBJets #geq 1"
                        name  = "geOneBTags"
                class geTwoBTags:
                        cut = "nBJets >= 2"
                        label = "nBJets #geq 2"
                        name  = "geTwoBTags"
                class geThreeBTags:
                        cut = "nBJets >= 3"
                        label = "nBJets #geq 3"
                        name  = "geThreeBTags"
                        
        class htCuts:
                class ht100:
                        cut = "ht > 100"
                        label = "H_{T} > 100 GeV"
                        name = "HT100"
                class ht300:
                        cut = "ht > 300"
                        label = "H_{T} > 300 GeV"
                        name = "HT300"
                class ht400:
                        cut = "ht > 400"
                        label = "H_{T} > 400 GeV"
                        name = "HT400"
                class ht700:
                        cut = "ht > 700"
                        label = "H_{T} > 700 GeV"
                        name = "HT700"
                class ht100to300:
                        cut = "ht > 100 && ht < 300"
                        label = "100 GeV < H_{T} < 100 GeV"
                        name = "HT100to300"
                class lowHT:
                        cut = "ht < 400"
                        label = "H_{T} < 400 GeV"
                        name = "LowHT"
                class mediumHT:
                        cut = "ht > 400 && ht < 800"
                        label = "400 GeV < H_{T} < 800 GeV"
                        name = "MediumHT"
                class highHT:
                        cut = "ht > 800"
                        label = "800 GeV < H_{T}"
                        name = "HighHT"

        class pileUpCuts:
                class lowPU:
                        cut = "nVertices < 13"
                        label = "N_{Vtx} < 13"
                        name = "LowPU"
                class midPU:
                        cut = "nVertices >= 13 && nVertices < 17"
                        label = "13 #leq N_{Vtx} < 17"
                        name = "MidPU"
                class highPU:
                        cut = "nVertices >= 17"
                        label = "N_{Vtx} #geq 17"
                        name = "HighPU"

        class nLLCuts:
                #class lowNLL:
                        #cut = "nLL < 21"
                        #label = "NLL < 21"
                        #name = "LowNLL"
                #class highNLL:
                        #cut = "nLL >= 21"
                        #label = "NLL #geq 21"
                        #name = "HighNLL"
                class lowNLL:
                        cut = "nLL < 21"
                        label = "NLL < 30"
                        name = "LowNLL"
                class highNLL:
                        cut = "nLL >= 21"
                        label = "NLL #geq 27"
                        name = "HighNLL"

        class mt2Cuts:
                class lowMT2:
                        cut = "MT2 < 80"
                        label = "MT2 < 80"
                        name = "LowMT2"
                class highMT2:
                        cut = "MT2 > 80 && nBJets >= 1"
                        label = "MT2 > 80"
                        name = "HighMT2"     

class theCuts2016:
        class triggerCuts:
                class EE:
                        cut = "(HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v > 0 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v > 0 || HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v > 0 || HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_MW_v > 0)"
                        label = "ee trigger"
                        name = "EETrigger"
                class EM:
                        #~ cut = "(HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ_v > 0 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v > 0 || HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v > 0 || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v > 0 || HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v > 0 || HLT_Mu33_Ele33_CaloIdL_GsfTrkIdVL_v > 0)"
                        cut = "(HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ_v > 0 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v > 0 || HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v > 0 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v > 0 || HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v > 0 || HLT_Mu33_Ele33_CaloIdL_GsfTrkIdVL_v > 0)"
                        label = "e#mu trigger"
                        name = "EMTrigger"
                class MM:
                        #~ cut = "(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v > 0 || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v > 0 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v > 0 || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v > 0 || HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v > 0 || HLT_Mu27_TkMu8_v > 0 || HLT_Mu30_TkMu11_v > 0)"
                        cut = "(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v > 0 || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v > 0 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v > 0 || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v > 0 || HLT_Mu27_TkMu8_v > 0 || HLT_Mu30_TkMu11_v > 0)"
                        label = "#mu#mu trigger"
                        name = "MMTrigger"
                class HT:
                        cut = ""
                        label = "HT trigger"
                        name = "HTTrigger"
                class baseline:
                        cut = "(triggerSummaryHT > 0)"
                        label = "HT trigger"
                        name = "HTTrigger"
                
                
class theCuts2017:
        class triggerCuts:
                class EE:
                        cut = "(triggerSummary > 0)"
                        label = "ee trigger"
                        name = "EETrigger"
                class EM:
                        cut = "(triggerSummary > 0)"
                        label = "e#mu trigger"
                        name = "EMTrigger"
                class MM:
                        cut = "(triggerSummary > 0)"
                        label = "#mu#mu trigger"
                        name = "MMTrigger"
                class HT:
                        cut = "(triggerSummaryHT > 0)"
                        label = "HT trigger"
                        name = "HTTrigger"
                class baseline:
                        cut = "(triggerSummaryMET > 0)"
                        label = "HT trigger"
                        name = "HTTrigger"
         
class theCuts2018:
        class triggerCuts:
                class EE:
                        cut = "(triggerSummary > 0)"
                        label = "ee trigger"
                        name = "EETrigger"
                class EM:
                        cut = "(triggerSummary > 0)"
                        label = "e#mu trigger"
                        name = "EMTrigger"
                class MM:
                        cut = "(triggerSummary > 0)"
                        label = "#mu#mu trigger"
                        name = "MMTrigger"
                class HT:
                        cut = "(triggerSummaryHT > 0)"
                        label = "HT trigger"
                        name = "HTTrigger"
                class baseline:
                        cut = "(triggerSummaryMET > 0)"
                        label = "HT trigger"
                        name = "HTTrigger"
         
class theCuts(maplike):
        pass
                                
for key, val in allCuts.__dict__.iteritems():
        if not "__" in key:
                setattr(theCuts, key, val)
theCuts["2016"] = theCuts2016
theCuts["2017"] = theCuts2017
theCuts["2018"] = theCuts2018



class theVariables:
        class Eta1:
                variable = "eta1"
                name = "Eta1"
                xMin = -2.4
                xMax = 2.4
                nBins = 10
                labelX = "#eta_{1}"
                labelY = "Events / 0.48"        
        class Eta2:
                variable = "eta2"
                name = "Eta2"
                xMin = -2.4
                xMax = 2.4
                nBins = 10
                labelX = "#eta_{2}"
                labelY = "Eventdes / 0.48"        
        class TrailingEta:
                variable = "(pt2>pt1)*eta1+(pt1>pt2)*eta2"
                name = "TrailingEta"
                xMin = -2.4
                xMax = 2.4
                nBins = 10
                labelX = "trailing #eta"
                labelY = "Events / 0.48"        
        class TrailingIso:
                variable = "(pt2>pt1)*id1+(pt1>pt2)*id2"
                name = "TrailingIso"
                xMin = 0
                xMax = 3
                nBins = 60
                labelX = "trailing relative isolation"
                labelY = "Events / 0.05"        
        class AbsTrailingEta:
                variable = "abs((pt2>pt1)*eta1+(pt1>pt2)*eta2)"
                name = "TrailingEta"
                xMin = 0
                xMax = 2.4
                nBins = 5
                labelX = "trailing #eta"
                labelY = "Events / 0.48"        
        class LeadingEta:
                variable = "(pt2<pt1)*eta1+(pt1<pt2)*eta2"
                name = "LeadingEta"
                xMin = -2.4
                xMax = 2.4
                nBins = 10
                labelX = "leading #eta"
                labelY = "Events / 0.48"        
        class AbsLeadingEta:
                variable = "abs((pt2<pt1)*eta1+(pt1<pt2)*eta2)"
                name = "LeadingEta"
                xMin = 0
                xMax = 2.4
                nBins = 5
                labelX = "leading #eta"
                labelY = "Events / 0.48"        
        class PtEle:
                variable = "pt1"
                name = "Pt1"
                xMin = 0
                xMax = 400
                nBins = 40
                labelX = "p_{T}^{ele} [GeV]"
                labelY = "Events / 10 GeV"      
        class PtMu:
                variable = "pt2"
                name = "Pt2"
                xMin = 0
                xMax = 400
                nBins = 40
                labelX = "p_{T}^{#mu} [GeV]"
                labelY = "Events / 10 GeV"      
        class LeadingPt:
                variable = "(pt1>pt2)*pt1+(pt2>pt1)*pt2"
                name = "LeadingPt"
                xMin = 0
                xMax = 200
                nBins = 40
                labelX = "p_{T}^{leading} [GeV]"
                labelY = "Events / 5 GeV"      
        class TrailingPt:
                variable = "(pt1>pt2)*pt2+(pt2>pt1)*pt1"
                name = "TrailingPt"
                xMin = 0
                xMax = 150
                nBins = 30
                labelX = "p_{T}^{trailing} [GeV]"
                labelY = "Events / 5 GeV"      
        class Met:
                variable = "met"
                name = "MET"
                xMin = 0
                xMax = 400
                nBins = 40
                labelX = "p_{T}^{miss} [GeV]"
                labelY = "Events / 10 GeV"      
        class GenMet:
                variable = "genMetPromptNeutrinos"
                name = "GenMET"
                xMin = 150
                xMax = 400
                nBins = 25
                labelX = "p_{T}^{miss,gen} [GeV]"
                labelY = "Events / 10 GeV"      
        class RawMet:
                variable = "uncorrectedMet"
                name = "RawMET"
                xMin = 0
                xMax = 400
                nBins = 40
                labelX = "uncorr. E_{T}^{miss} [GeV]"
                labelY = "Events / 10 GeV"      
        class Type1Met:
                variable = "type1Met"
                name = "Type1MET"
                xMin = 0
                xMax = 400
                nBins = 40
                labelX = "typeI corr. E_{T}^{miss} [GeV]"
                labelY = "Events / 10 GeV"      
        class TcMet:
                variable = "tcMet"
                name = "TCMET"
                xMin = 0
                xMax = 400
                nBins = 40
                labelX = "track corr. E_{T}^{miss} [GeV]"
                labelY = "Events / 10 GeV"      
        class CaloMet:
                variable = "caloMet"
                name = "CaloMET"
                xMin = 0
                xMax = 400
                nBins = 40
                labelX = "calo E_{T}^{miss} [GeV]"
                labelY = "Events / 10 GeV"      
        class MHT:
                variable = "mht"
                name = "MHT"
                xMin = 0
                xMax = 400
                nBins = 40
                labelX = "H_{T}^{miss} [GeV]"
                labelY = "Events / 10 GeV"      
        class HT:
                variable = "ht"
                name = "HT"
                xMin = 0
                xMax = 1000
                nBins = 25
                labelX = "H_{T} [GeV]"
                labelY = "Events / 40 GeV"          
                #~ labelY = "Fraction"  
        class GenHT:
                variable = "genHT"
                name = "GenHT"
                xMin = 0
                xMax = 1000
                nBins = 25
                labelX = "H_{T,gen} [GeV]"
                labelY = "Events / 40 GeV"        
        class DiffGenHT:
                variable = "ht - genHT"
                name = "DiffGenHT"
                xMin = -200
                xMax = 200
                nBins = 40
                labelX = "H_{T} - H_{T,gen} [GeV]"
                labelY = "Events / 10 GeV"     
        class ST:
                variable = "ht+lepton1.Pt()+lepton2.Pt()"
                name = "ST"
                xMin = 0
                xMax = 1000
                nBins = 20
                labelX = "S_{T} [GeV]"
                labelY = "Events / 50 GeV" 
        class Mll:
                #variable = "p4.M()"
                variable = "mll" # In case of trees with likelihood
                name = "Mll"
                xMin = 20
                xMax = 500
                nBins = 96
                labelX = "m_{ll} [GeV]" 
                labelY = "Events / 5 GeV"       
                #~ labelY = "Events / GeV"      # For plots normalized to bin width
                #~ labelY = "Events / Bin"      
                #~ labelY = "Fraction"       
        class GenMll:
                variable = "p4Gen.M()"
                name = "GenMll"
                xMin = 20
                xMax = 500
                nBins = 96
                labelX = "m_{ll,gen} [GeV]"
                labelY = "Events / 5 GeV"      
        class nLL:
                variable = "nLL"
                name = "ttbar likelihood"
                xMin = 11.5
                xMax = 34.5
                nBins = 46
                labelX = "nLL"
                labelY = "Fraction"     
        class Ptll:
                variable = "p4.Pt()"
                name = "Ptll"
                xMin = 20
                xMax = 600
                nBins = 58
                labelX = "p_{T}^{ll} [GeV]"
                labelY = "Events / 10 GeV"       
        class sumMlb:
                variable = "sumMlb"
                name = "sumMlb"
                xMin = 0
                xMax = 1000
                nBins = 50
                labelX = "#sum mlb [GeV]"
                labelY = "Events / 20 GeV"      
        class nJets:
                variable = "nJets"
                name = "NJets"
                xMin = -0.5
                xMax = 8.5
                nBins = 9
                labelX = "n_{jets}"
                labelY = "Events"       
        class nBJets:
                variable = "nBJets"
                name = "NBJets"
                xMin = -0.5
                xMax = 10.5
                nBins = 11
                labelX = "n_{b-tagged jets}"
                labelY = "Events"       
        class nLightLeptons:
                variable = "nLightLeptons"
                name = "NLightLeptons"
                xMin = -0.5
                xMax = 6.5
                nBins = 7
                labelX = "n_{light leptons}"
                labelY = "Events"       
        class deltaR:
                variable = "deltaR"
                name = "DeltaR"
                xMin = 0
                xMax = 4
                nBins = 20
                labelX = "#Delta R_{ll}"
                labelY = "Events / 0.2" 
        class deltaPhiLep1Met:
                variable = "abs((lepton1.Phi()-vMet.Phi()) - ((lepton1.Phi()-vMet.Phi()) > TMath::Pi())*2*TMath::Pi() + ((lepton1.Phi()-vMet.Phi()) < -TMath::Pi())*2*TMath::Pi())"
                name = "DeltaPhi"
                xMin = 0
                xMax = 3.2
                nBins = 32
                labelX = "#Delta #phi_{l_{1}, p_{T}^{miss}}"
                labelY = "Events / 0.1" 
        class deltaPhiLep2Met:
                variable = "abs((lepton2.Phi()-vMet.Phi()) - ((lepton2.Phi()-vMet.Phi()) > TMath::Pi())*2*TMath::Pi() + ((lepton2.Phi()-vMet.Phi()) < -TMath::Pi())*2*TMath::Pi())"
                name = "DeltaPhi"
                xMin = 0
                xMax = 3.2
                nBins = 32
                labelX = "#Delta #phi_{l_{1}, p_{T}^{miss}}"
                labelY = "Events / 0.1" 
        class deltaPhi:
                variable = "abs(deltaPhi)"
                name = "DeltaPhi"
                xMin = 0
                xMax = 3.2
                nBins = 32
                labelX = "#Delta #phi_{ll}"
                labelY = "Events / 0.1" 
        class GenDeltaPhi:
                variable = "abs(genDeltaPhi)"
                name = "DeltaPhi"
                xMin = 0
                xMax = 3.2
                nBins = 32
                labelX = "gen #Delta #phi_{ll}"
                labelY = "Events / 0.1" 
        class nVtx:
                variable = "nVertices"
                name = "nVtx"
                xMin = 0
                xMax = 40
                nBins = 40
                labelX = "N_{Vertex}"
                labelY = "Events"       
        class leadingJetPt:
                variable = "jet1pt"
                name = "leadingJetPt"
                xMin = 0
                xMax = 400
                nBins = 40
                labelX = "leading p_{T}^{jet} [GeV]"
                labelY = "Events / 10 GeV"      
        class subleadingJetPt:
                variable = "jet2pt"
                name = "subleadingJetPt"
                xMin = 0
                xMax = 400
                nBins = 40
                labelX = "subleading p_{T}^{jet} [GeV]"
                labelY = "Events / 10 GeV"      
        class MT2:
                variable = "MT2"
                name = "MT2"
                #~ xMin = 10
                xMin = 0
                #~ xMax = 120
                #~ nBins = 12
                xMax = 200
                nBins = 20
                labelX = "MT2 [GeV]"
                #~ labelY = "Events / 10 GeV"   
                labelY = "Fraction"           
        
        
        
class Regions:
        class ExactlyTwoJetsHighMet(Region):
                cut = "(nJets == 2 && met > 150) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} = 2, MET > 150"
                titel = "SR"
                latex = "ThreeJetsHighMet"
                name = "ThreeJetsHighMet"
                logY = False
                
        class TwoJetsHighMet(Region):
                cut = "(nJets >= 2 && met > 150 ) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, MET > 150"
                titel = "SR"
                latex = "TwoJetsHighMet"
                name = "TwoJetsHighMet"
                logY = False
                
        class TwoJets(Region):
                cut = "(nJets >= 2) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2"
                titel = "SR"
                latex = "TwoJets"
                name = "TwoJets"
                logY = False
                
        class SignalATLAS(Region):
                cut = "(met > 225 && (ht + pt1 + pt2) > 600 && abs(deltaPhiJetMET) > 0.4 & abs(deltaPhiSecondJetMET) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "ATLAS Signal Region"
                titel = "ATLAS SR"
                latex = "ATLAS Signal Region"
                name = "SignalATLAS"
                logY = False
                
        class SignalInclusive(Region):
                cut = "(nJets >= 2 && met > 150) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 150 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusive"
                logY = False
                
        class SignalInclusiveHighMT2(Region):
                cut = "(nJets >= 2 && met > 150 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 150 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2"
                logY = False
                
        class SignalInclusiveHighMT2MetLimited(Region):
                cut = "(nJets >= 2 && met > 150 && met < 200 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 150 GeV, p_{T}^{miss} < 200 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2MetLimited"
                logY = False
                
        class SignalInclusiveHighMT2OneB(Region):
                cut = "(nJets >= 2 && nBJets >= 1 && met > 150 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, N_{b-Jets} #geq 1, p_{T}^{miss} > 150 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2OneB"
                logY = False
                
                
        class SignalInclusiveHighMT2_MT2_80_MET_300(Region):
                cut = "(nJets >= 2 && met > 300 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 300 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2_MT2_80_MET_300"
                logY = False
                
        class SignalInclusiveHighMT2_MT2_80_MET_230(Region):
                cut = "(nJets >= 2 && met > 230 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 230 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2_MT2_80_MET_230"
                logY = False
                
        class SignalInclusiveHighMT2_MT2_80_MET_250(Region):
                cut = "(nJets >= 2 && met > 250 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 250 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2_MT2_80_MET_250"
                logY = False
                
        class SignalInclusiveHighMT2_85OneB(Region):
                cut = "(nJets >= 2 && met > 150 && MT2 > 85 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4 && nBJets >= 1) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 150 GeV, M_{T2} > 85 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2_85OneB"
                logY = False
                
        class SignalInclusiveHighMT2_85_Met200(Region):
                cut = "(nJets >= 2 && met > 200 && MT2 > 85 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 200 GeV, M_{T2} > 85 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2_85_Met200"
                logY = False
                
        class SignalInclusiveHighMT2_90_Met200(Region):
                cut = "(nJets >= 2 && met > 200 && MT2 > 90 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 200 GeV, M_{T2} > 90 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2_90_Met200"
                logY = False
                
        class SignalInclusiveHighMT2_90(Region):
                cut = "(nJets >= 2 && met > 150 && MT2 > 90 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 150 GeV, M_{T2} > 90 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2_90"
                logY = False
                
        class SignalInclusiveHighMT2_100(Region):
                cut = "(nJets >= 2 && met > 150 && MT2 > 100 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 150 GeV, M_{T2} > 100 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2_100"
                logY = False
                
        class SignalInclusiveHighMT2Met200(Region):
                cut = "(nJets >= 2 && met > 200 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 200 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2Met200"
                logY = False
                
        class SignalInclusiveHighMT2Met220(Region):
                cut = "(nJets >= 2 && met > 220 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 220 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2Met220"
                logY = False
                
        class SignalInclusiveHighMT2Met230(Region):
                cut = "(nJets >= 2 && met > 230 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 250 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2Met250"
                logY = False
         
        class SignalInclusiveHighMT2Met240(Region):
                cut = "(nJets >= 2 && met > 240 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 240 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2Met240"
                logY = False
         
                
        class SignalInclusiveHighMT2Met250(Region):
                cut = "(nJets >= 2 && met > 230 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{Jets} #geq 2, p_{T}^{miss} > 230 GeV, M_{T2} > 80 GeV"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalInclusiveHighMT2Met230"
                logY = False
         
        class SignalDeltaPhi(Region):
                cut = "(nJets >= 2 && met > 150 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{jets} #geq 2, MET > 150 GeV, #Delta#phi_{jet_{1,2},MET} > 0.4"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalDeltaPhi"
                #~ logY = False
                logY = True
                
        class SignalDeltaPhiLeptonVeto(Region):
                cut = "(nJets >= 2 && met > 150 && abs(deltaPhiJetMet1) > 0.4  && abs(deltaPhiJetMet1) < 2*TMath::Pi() - 0.4   && abs(deltaPhiJetMet2) > 0.4 && abs(deltaPhiJetMet2) < 2*TMath::Pi() - 0.4  && nLooseLeptons == 2) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "3rd lepton veto, #Delta#phi_{jet_{1,2},MET} Signal Region"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalDeltaPhiLeptonVeto"
                logY = False
        class SignalHighNLLHighHT(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && ht > 800) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Non-ttbar like, high HT Signal Region"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalHighNLLHighHT"
                logY = False
                
        class SignalHighNLLHighMT2DeltaPhiJetMetForward(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 && (mll < 86 || mll > 96)) && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                #~ cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Non-ttbar like Signal Region forward"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalHighNLLHighMT2DeltaPhiJetMetForward"
                logY = False
        
        class SignalHighNLLHighMT2DeltaPhiJetMetCentral(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 && (mll < 86 || mll > 96)) && abs(eta1) < 1.6 && abs(eta2) < 1.6 && (%s)"%Region.cut
                #~ cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Non-ttbar like Signal Region central"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalHighNLLHighMT2DeltaPhiJetMetCentral"
                logY = False
        
        class SignalHighNLLHighMT2DeltaPhiJetMetCentralJets(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 && (mll < 86 || mll > 96)) &&  abs(jet1eta) < 1.6 && abs(jet2eta) < 1.6 && (%s)"%Region.cut
                #~ cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Non-ttbar like Signal Region central jets"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalHighNLLHighMT2DeltaPhiJetMetCentralJets"
                logY = False
        
        class SignalHighNLLHighMT2DeltaPhiJetMetForwardJets(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 && (mll < 86 || mll > 96)) && 1.6 <= TMath::Max(abs(jet1eta),abs(jet2eta)) && (%s)"%Region.cut
                #~ cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Non-ttbar like Signal Region forward jets"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalHighNLLHighMT2DeltaPhiJetMetForwardJets"
                logY = False
        
        class SignalHighNLLHighMT2DeltaPhiJetMetForwardAll(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 && (mll < 86 || mll > 96)) && 1.6 <= TMath::Max(abs(jet1eta),abs(jet2eta)) && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                #~ cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Non-ttbar like Signal Region forward all"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalHighNLLHighMT2DeltaPhiJetMetForwardAll"
                logY = False
                
        class SignalHighNLLHighMT2DeltaPhiJetMetCentralAll(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 && (mll < 86 || mll > 96)) &&  abs(jet1eta) < 1.6 && abs(jet2eta) < 1.6 && abs(eta1) < 1.6 && abs(eta2) < 1.6 && (%s)"%Region.cut
                #~ cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Non-ttbar like Signal Region central all"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalHighNLLHighMT2DeltaPhiJetMetCentralAll"
                logY = False
        
        class SignalLowNLLHighMT2DeltaPhiJetMet(Region):
                cut = "(nJets >= 2 && met > 150 && nLL < 21 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 && (mll < 86 || mll > 96)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "ttbar like Signal Region"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalLowNLLHighMT2DeltaPhiJetMet"
                logY = False
                
        class SignalHighNLLHighMT2DeltaPhiJetMetLeptonVeto(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet1) < 2*TMath::Pi() - 0.4 && abs(deltaPhiJetMet2) > 0.4 && abs(deltaPhiJetMet2) < 2*TMath::Pi() - 0.4  && nLooseLeptons == 2) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "3rd lepton veto, #Delta#phi_{jet_{1,2},MET}, Non-ttbar like, high MT2 Signal Region"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalHighNLLHighMT2DeltaPhiJetMetLeptonVeto"
                logY = False
                
        class SignalHighNLLHighMT2(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && MT2 < 1000) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "Non-ttbar like, high MT2 Signal Region"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLLHighMT2"
                logY = False        
                
        class SignalHighNLLHighMT2OneB(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && MT2 < 1000 && nBJets >= 1) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "Non-ttbar like, high MT2 Signal Region, N_{b} #geq 1"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLLHighMT2OneB"
                logY = False
                
        class SignalHighNLL22HighMT2(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 22 && MT2 > 80 && MT2 < 1000) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 22, high MT2 Signal Region"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLL22HighMT2"
                logY = False
                
        class SignalHighNLL23HighMT2(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 23 && MT2 > 80 && MT2 < 1000) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 23, high MT2 Signal Region"
                titel = "SR"
                latex = "Signal Region nLL > 23"
                name = "HighNLL23HighMT2"
                logY = False
                
        class SignalHighNLL24HighMT2(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 24 && MT2 > 80 && MT2 < 1000) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 24, high MT2 Signal Region"
                titel = "SR"
                latex = "Signal Region nLL > 24"
                name = "HighNLL24HighMT2"
                logY = False
                
        class SignalHighNLL25HighMT2(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 25 && MT2 > 80 && MT2 < 1000) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 25, high MT2 Signal Region"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLL25HighMT2"
                logY = False
                
        class SignalHighNLL22HighMT2OneB(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 22 && MT2 > 80 && MT2 < 1000 && nBJets >= 1) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 22, high MT2 Signal Region, N_{b} #geq 1"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLL22HighMT2OneB"
                logY = False
        class SignalHighNLL23HighMT2OneB(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 23 && MT2 > 80 && MT2 < 1000 && nBJets >= 1) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 23, high MT2 Signal Region, N_{b} #geq 1"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLL23HighMT2OneB"
                logY = False
        class SignalHighNLL24HighMT2OneB(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 24 && MT2 > 80 && MT2 < 1000 && nBJets >= 1) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 24, high MT2 Signal Region, N_{b} #geq 1"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLL24HighMT2OneB"
                logY = False
        class SignalHighNLL24HighMT2ZeroB(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 24 && MT2 > 80 && MT2 < 1000 && nBJets == 0) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 24, high MT2 Signal Region, N_{b} = 0"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLL24HighMT2ZeroB"
                logY = False
        class SignalHighNLL25HighMT2OneB(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 25 && MT2 > 80 && MT2 < 1000 && nBJets >= 1) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 25, high MT2 Signal Region, N_{b} #geq 1"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLL25HighMT2OneB"
                logY = False
        class SignalHighNLL26HighMT2ZeroB(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 26 && MT2 > 80 && MT2 < 1000 && nBJets == 0) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 26, high MT2 Signal Region, N_{b} = 0"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLL26HighMT2ZeroB"
                logY = False
        class SignalHighNLL26HighMT2OneB(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 26 && MT2 > 80 && MT2 < 1000 && nBJets >= 1) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL > 26, high MT2 Signal Region, N_{b} #geq 1"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLL26HighMT2OneB"
                logY = False
                
        class SignalLowNLL26HighMT2ZeroB(Region):
                cut = "(nJets >= 2 && met > 150 && nLL < 26 && MT2 > 80 && MT2 < 1000 && nBJets == 0) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL < 26, high MT2 Signal Region, N_{b} = 0"
                titel = "SR"
                latex = "Signal Region"
                name = "LowNLL26HighMT2ZeroB"
                logY = False
                
        class SignalLowNLL26HighMT2OneB(Region):
                cut = "(nJets >= 2 && met > 150 && nLL < 26 && MT2 > 80 && MT2 < 1000 && nBJets >= 1) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "nLL < 26, high MT2 Signal Region, N_{b} #geq 1"
                titel = "SR"
                latex = "Signal Region"
                name = "LowNLL26HighMT2OneB"
                logY = False
                
        class SignalHighNLLHighMT2OneBVetoSols(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && MT2 > 80 && MT2 < 1000 && nBJets >= 1 && nNuSols > 0) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "Non-ttbar like, high MT2 Signal Region, N_{b} #geq 1"
                titel = "SR"
                latex = "Signal Region"
                name = "HighNLLHighMT2OneBVetoNu"
                logY = False
                
        class SignalLowNLLHighMT2(Region):
                cut = "(nJets >= 2 && met > 150 && nLL < 21 && MT2 > 80 && MT2 < 1000) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "ttbar like, high MT2 Signal Region"
                titel = "SR"
                latex = "Signal Region"
                name = "SignalLowNLLHighMT2"
                logY = False
                
        class SignalInclusiveOld(Region):
                cut = "((nJets >= 2 && met > 150) || (nJets >=3 && met > 100)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Inclusive Signal Region"
                titel = "Inclusive SR"
                latex = "Inclusive Signal Region"
                name = "SignalInclusive"
                logY = False

        class SignalForward(Region):
                cut = "(nJets >= 2 && met > 150) &&  1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Forward Signal Region"
                titel = "Forward SR"
                latex = "Forward Signal Region"
                name = "SignalForward"
                logY = False
                trigEffs = triggerEffs.forward  
                        
        class SignalForwardOld(Region):
                cut = "((nJets >= 2 && met > 150) || (nJets>=3 && met > 100)) &&  1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Forward Signal Region"
                titel = "Forward SR"
                latex = "Forward Signal Region"
                name = "SignalForward"
                logY = False
                trigEffs = triggerEffs.forward          

                        
        class SignalOneForward(Region):
                cut = "((nJets >= 2 && met > 150) || (nJets>=3 && met > 100)) &&  1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (abs(eta1) < 1.6 || abs(eta2) < 1.6) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Signal Region One Forward"
                titel = "One Forward SR"
                latex = "One Forward Signal Region"
                name = "SignalOneForward"
                logY = False
                trigEffs = triggerEffs.forward

        class SignalCentral(Region):
                cut = "(nJets >= 2 && met > 150) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelSubRegion = "Central Signal Region"
                labelRegion = Region.labelRegion.replace("< 2.4","< 1.4")
                titel = "Central SR"
                latex = "Central Signal Region"
                name = "SignalCentral"
                trigEffs = triggerEffs.central
                logY = False

        class SignalCentralOld(Region):
                cut = "((nJets >= 2 && met > 150) || (nJets >= 3 && met > 100)) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelSubRegion = "Central Signal Region"
                labelRegion = Region.labelRegion.replace("< 2.4","< 1.4")
                titel = "Central SR"
                latex = "Central Signal Region"
                name = "SignalCentral"
                trigEffs = triggerEffs.central
                logY = False
        
        class SignalHighMT2(Region):
                cut = "(nJets >= 2 && met > 150 && MT2 > 80 && MT2 < 1000) && (%s)"%Region.cutNLL
                labelRegion = Region.labelRegion
                labelSubRegion = "High MT2 Signal Region"
                titel = "SR"
                latex = "High MT2 Signal Region"
                name = "SignalHighMT2"
                logY = False
        
        class SignalHighMT2DeltaPhiJetMet(Region):
                #~ cut = "( deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 && nJets >= 2 && met > 150 && MT2 > 80 &&  (mll < 86 || mll > 96) ) && (%s)"%Region.cut
                cut = "(nJets >= 2 && met > 150 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 ) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Baseline Signal Region"
                titel = "SR"
                latex = "Baseline Signal Region"
                name = "SignalHighMT2DeltaPhiJetMet"
                logY = False
                
        class SignalHighMT2DeltaPhiJetMetOneB(Region):
                #~ cut = "( deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 && nJets >= 2 && met > 150 && MT2 > 80 &&  (mll < 86 || mll > 96) ) && (%s)"%Region.cut
                cut = "(nJets >= 2 && nBJets >= 1 && met > 150 && MT2 > 80 && deltaPhiJetMet1 > 0.4 && deltaPhiJetMet2 > 0.4 ) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Baseline Signal Region"
                titel = "SR"
                latex = "Baseline Signal Region"
                name = "SignalHighMT2DeltaPhiJetMetOneB"
                logY = False

        class SignalHighNLL(Region):
                cut = "(nJets >= 2 && met > 150 && nLL > 21 && mll > 101) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "non-ttbar like ICHEP Signal Region"
                titel = "SR"
                latex = "non-ttbar like Signal Region"
                name = "SignalHighNLL"
                logY = False

        class Signal3Jets(Region):
                cut = "(nJets >= 3 && met > 150 ) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "#geq 3 jet Signal Region"
                titel = "SR"
                latex = "#geq 3 jet Signal Region"
                name = "Signal3Jets"
                logY = False

        class SignalOnZ(Region):
                cut = "(nLooseLeptons == 2 && abs(deltaPhiJetMet1) > 0.4  && abs(deltaPhiJetMet2) > 0.4) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "#geq 3 jet Signal Region"
                titel = "SR"
                latex = "#geq 3 jet Signal Region"
                name = "Signal3Jets"
                logY = False
        
        class Control(Region):
                #~ cut = "nJets == 2  && 100 < met && met < 150 && (%s)"%Region.cut
                cut = "chargeProduct < 0 && nJets == 2  && 100 < met && met < 150 && (mll < 70 || mll > 110) && (%s)"%Region.cut
                #~ cut = "nJets == 2  && 100 < met && met < 150 && (p4.M() < 70 || p4.M() > 110) && (%s)"%Region.cut
                labelRegion = Region.labelRegion        
                labelSubRegion = "N_{jets} = 2, 100 < MET < 150 GeV"            
                titel = "CR"
                latex = "Control Region"
                name = "Control"
                logY = True
        class ControlForward(Region):
                cut = "nJets == 2  && 100 < met && met < 150 && (mll < 70 || mll > 110) && 1.4 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Control Region Forward"               
                titel = "CR"
                latex = "Control Region Forward"
                name = "ControlForward"
                logY = True
                trigEffs = triggerEffs.forward
        class ControlCentral(Region):
                cut = "nJets == 2  && 100 < met && met < 150 && (mll < 70 || mll > 110) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Control Region Central"               
                titel = "CR"
                latex = "Control Region Central"
                name = "ControlCentral"
                logY = True
                trigEffs = triggerEffs.central      

        class ControlLowMT2(Region):
                cut = "nJets == 2  && 100 < met && met < 150 && (mll < 70 || mll > 110) && MT2 < 80 && (%s)"%Region.cut
                labelSubRegion = "Control Region, MT2 < 80 GeV"         
                titel = "CR"
                latex = "Control Region, MT2 < 80 GeV"
                name = "ControlLowMT2"
                logY = True
        
        class ControlHighMT2DeltaPhiJetMet(Region):
                cut = "(nJets == 2 && met > 100 && met > 150 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet1) < 2*TMath::Pi() - 0.4 && abs(deltaPhiJetMet2) > 0.4 && abs(deltaPhiJetMet2) < 2*TMath::Pi() - 0.4  ) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "High MT2 Control Region"
                titel = "SR"
                #~ latex = "#Delta#phi_{jet_{1,2},MET} > 0.4, High MT2 Control Region"
                latex = "High MT2 Control Region"
                name = "ControlHighMT2DeltaPhiJetMet"
                logY = False            
        
        class ControlOld(Region):
                cut = "nJets == 2  && 100 < met && met < 150 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Control Region"               
                titel = "CR"
                latex = "Control Region"
                name = "Control"
                logY = True
        class ControlForwardOld(Region):
                cut = "nJets == 2  && 100 < met && met < 150 && 1.4 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Control Region Forward"               
                titel = "CR"
                latex = "Control Region Forward"
                name = "ControlForward"
                logY = True
                trigEffs = triggerEffs.forward
        class ControlCentralOld(Region):
                cut = "nJets == 2  && 100 < met && met < 150 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Control Region Central"               
                titel = "CR"
                latex = "Control Region Central"
                name = "ControlCentral"
                logY = True
                trigEffs = triggerEffs.central              
                        
        class bTagControl(Region):
                #~ cut = "nJets >=2 && met > 50 && nBJets >=1 && (%s)"%Region.cut
                cut = "nJets >=2 && met > 50 && nBJets >=1 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{jets} #geq 2 N_{bJets} #geq 1 E_{T}^{miss} > 50 GeV"                       
                titel = "High E_{T}^{miss} CR"
                latex = "High \MET\ Control Region"
                name = "bTagControl"
                logY = True
                        
        class InclusiveJets(Region):
                cut = "nJets >= 2   && (%s)"%Region.cut
                #~ cut = "nJets >= 0   && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{jets} #geq 2 "                     
                #~ labelSubRegion = ""                  
                titel = "Inclusive Jets"
                latex = "Inclusive Jets"
                name = "InclusiveJets"
                logY = True
        class InclusiveJetsBlinded(Region):
                #~ cut = "nJets >= 2   && (%s)"%Region.cut
                cut = "!((nJets >= 2 && met > 150) || (nJets >= 3 && met > 100)) && nJets >= 2   && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "N_{jets} #geq 2 blinded "                     
                titel = "Inclusive Jets Blinded"
                latex = "Inclusive Jets Blinded"
                name = "InclusiveJetsBlinded"
                logY = True

        class Inclusive(Region):
                cut = "(%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = ""                     
                titel = "Inclusive"
                latex = "Inclusive"
                name = "Inclusive"
                logY = True
                
        class InclusiveBlinded(Region):
                #~ cut = "!((nJets >= 2 && met > 150) || (nJets >= 3 && met > 100)) && (%s)"%Region.cut
                cut = "(!(nJets >= 2 && met > 150) && (%s))"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = ""                     
                titel = "InclusiveBlinded"
                latex = "InclusiveBlinded"
                name = "InclusiveBlinded"
                logY = True


        class Central(Region):
                cut = "abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = ""                     
                titel = "Central"
                latex = "Central"
                name = "Central"
                logY = True

        class Forward(Region):
                cut = " 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = ""                     
                titel = "Forward"
                latex = "Forward"
                name = "Forward"
                logY = True

                                
        class ZPeak(Region):
                cut = "p4.M() > 60 && p4.M() < 120 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "60 < m_{ll} < 120 GeV"                        
                titel = "Drell-Yan Enhanced"
                latex = "Drell-Yan Enhanced"
                name = "ZPeak"
                logY = True
        
        class ZPeakHighMetControl(Region):
                cut = "p4.M() > 60 && p4.M() < 120 && met < 150 && met > 100 && nJets >= 2 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "#splitline{60 < m_{ll} < 120 GeV}{N_{jets} #geq 2, 100 < E_{T}^{miss} < 150 GeV}"                     
                titel = "Drell-Yan Enhanced"
                latex = "Drell-Yan Enhanced"
                name = "ZPeakHighMetControl"
                logY = True
        
        class ZPeakMediumMetControl(Region):
                cut = "p4.M() > 60 && p4.M() < 120 && met < 100 && met > 50 && nJets >= 2 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "#splitline{60 < m_{ll} < 120 GeV}{N_{jets} #geq 2, 50 < E_{T}^{miss} < 100 GeV}"                      
                titel = "Drell-Yan Enhanced"
                latex = "Drell-Yan Enhanced"
                name = "ZPeakMediumMetControl"
                logY = True
        
        class ZPeakControl(Region):
                #~ cut = "p4.M() > 60 && p4.M() < 120 && met < 50 && nJets >= 2 && (%s)"%Region.cut
                cut = "mll > 60 && met < 50 && mll < 120 && nJets >= 2 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "#splitline{60 < m_{ll} < 120 GeV}{N_{jets} #geq 2, E_{T}^{miss} < 50 GeV}"                    
                titel = "Drell-Yan Enhanced"
                latex = "Drell-Yan Enhanced"
                name = "ZPeakControl"
                logY = True
        class ZPeakControlCentral(Region):
                cut = "mll > 60 && mll < 120 && met < 50 && nJets >= 2 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "#splitline{60 < m_{ll} < 120 GeV}{N_{jets} #geq 2, E_{T}^{miss} < 50 GeV}"                    
                titel = "Drell-Yan Enhanced Central"
                latex = "Drell-Yan Enhanced Central"
                name = "ZPeakControlCentral"
                logY = True
        class ZPeakControlForward(Region):
                cut = "mll > 60 && mll < 120 && met < 50 && nJets >= 2 && 1.4 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "#splitline{60 GeV < m_{ll} < 120 GeV}{N_{jets} #geq 2 E_T^{miss} < 50 GeV}"                   
                titel = "Drell-Yan Enhanced Forward"
                latex = "Drell-Yan Enhanced Forward"
                name = "ZPeakControlForward"
                logY = True
        
        class DrellYanControl(Region):
                cut = "nJets >= 2 && met < 50 &&(%s)"%Region.cut
                #~ cut = "nJets >= 2 && met < 50 && MT2 > 80 &&(%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Drell-Yan control region"                     
                titel = "Drell-Yan control region"
                latex = "Drell-Yan control region"
                name = "DrellYanControl"
                logY = True
        class DrellYanControlCentral(Region):
                cut = "nJets >= 2 && met < 50 && abs(eta1) < 1.4 && abs(eta2) < 1.4  && MT2 > 80 &&(%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Drell-Yan control region"                     
                titel = "Drell-Yan control region central"
                latex = "Drell-Yan control region central"
                name = "DrellYanControlCentral"
                logY = True
        class DrellYanControlForward(Region):
                cut = "nJets >= 2 && met < 50 && 1.4 <= TMath::Max(abs(eta1),abs(eta2))  && MT2 > 80 &&(%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "Drell-Yan control region"                     
                titel = "Drell-Yan control region forward"
                latex = "Drell-Yan control region forward"
                name = "DrellYanControlForward"
                logY = True     
### for trigger efficiency measurements:                

        class HighHT(Region):
                cut = "ht > 200 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "H_{T} > 200 GeV"
                titel = "High HT region"
                latex = "High H_{T} region"
                name = "HighHT"
                logY = False
                
        class HighMET(Region):
                cut = "met > 130 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "p_{T}^{miss} > 130 GeV"
                titel = "High MET region"
                latex = "High p_{T}^{miss} region"
                name = "HighMET"
                logY = False
        
        class HighMETForward(Region):
                cut = "met > 100 && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "p_{T}^{miss} > 100 GeV, forward"
                titel = "High MET region forward"
                latex = "High p_{T}^{miss} region forward"
                name = "HighMETForward"
                logY = False
                
        class HighMETCentral(Region):
                cut = "met > 100 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "p_{T}^{miss} > 100 GeV, central"
                titel = "High MET region central"
                latex = "High p_{T}^{miss} region central"
                name = "HighMETCentral"
                logY = False
        
        class HighHTExclusive(Region):
                cut = "ht > 200 && !(nJets >= 2 && met > 100) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "H_{T} > 200 GeV"
                titel = "High HT region exclusive"
                latex = "High H_{T} region exclusive"
                name = "HighHTExclusive"
                logY = False
        class HighHTExclusiveForward(Region):
                cut = "ht > 200 && !(nJets >= 2 && met > 100) &&  1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "H_{T} > 200 GeV"
                titel = "High HT region exclusive forward"
                latex = "High H_{T} region exclusive forward"
                name = "HighHTExclusiveForward"
                logY = False
        class HighHTExclusiveCentral(Region):
                cut = "ht > 200 && !(nJets >= 2 && met > 100) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "H_{T} > 200 GeV central"
                titel = "High HT region exclusive central"
                latex = "High H_{T} region exclusive central"
                name = "HighHTExclusiveCentral"
                logY = False
                
        class HighMETExclusive(Region):
                cut = "met > 130 && !(nJets >= 2 && met > 150 && MT2 > 80) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "E_{T}^{miss} > 130 GeV"
                titel = "High MET region exclusive"
                latex = "High E_{T}^{miss} region exclusive"
                name = "HighMETExclusive"
                logY = False
        class HighMETExclusiveForward(Region):
                cut = "met > 130 && !(nJets >= 2 && met > 150 && MT2 > 80) && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "E_{T}^{miss} > 200 GeV"
                titel = "High MET region exclusive forward"
                latex = "High E_{T}^{miss} region exclusive forward"
                name = "HighMETExclusiveForward"
                logY = False
        class HighMETExclusiveCentral(Region):
                cut = "met > 130 && !(nJets >= 2 && met > 150 && MT2 > 80) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "E_{T}^{miss} > 200 GeV central"
                titel = "High MET region exclusive central"
                latex = "High E_{T}^{miss} region exclusive central"
                name = "HighMETExclusiveCentral"
                logY = False

        class HighMETForward(Region):
                cut = "met > 200 &&  1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "E_{T}^{miss} > 200 GeV"
                titel = "High MET region forward"
                latex = "High E_{T}^{miss} region forward"
                name = "HighMETForward"
                logY = False
        class HighMETCentral(Region):
                cut = "met > 200 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "E_{T}^{miss} > 200 GeV central"
                titel = "High MET region central"
                latex = "High E_{T}^{miss} region central"
                name = "HighMETCentral"
                logY = False

        class Exclusive(Region):
                cut = "!(nJets >= 2 && met > 100) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "signal region excluded"
                titel = "exclusive"
                latex = "exclusive"
                name = "Exclusive"
                logY = False
        class ExclusiveForward(Region):
                cut = "!(nJets >= 2 && met > 100) &&  1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "signal region excluded"
                titel = "exclusive forward"
                latex = "exclusive forward"
                name = "ExclusiveForward"
                logY = False
        class ExclusiveCentral(Region):
                cut = "!(nJets >= 2 && met > 100) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
                labelRegion = Region.labelRegion
                labelSubRegion = "signal region excluded"
                titel = "exclusive central"
                latex = "exclusive central"
                name = "ExclusiveCentral"
                logY = False

def getRegion(name):
        if not name in dir(Regions) and not name == "Region":
                print "unknown region '%s, exiting'"%name
                sys.exit()
        elif name == "Region":
                return Region
        else:
                return copy.copy(getattr(Regions, name))
                
def getMassSelection(name):
        if not name in dir(theCuts.massCuts):
                print "unknown selection '%s, using existing selection'"%name
                return None
        else:
                return copy.copy(getattr(theCuts.massCuts, name))
                
def getPlot(name):
        if not name in dir(thePlots):
                print "unknown plot '%s, exiting'"%name
                sys.exit()
        else:
                return copy.copy(getattr(thePlots, name))
                
def getRunRange(name):
        if not name in dir(runRanges):
                print "unknown run range '%s, exiting'"%name
                sys.exit()
        else:
                return copy.copy(getattr(runRanges, name))
        
        
                
class Plot:
        variable= "none"
        variablePlotName = "none"
        additionalName = "none"
        cuts    = "none"
        xaxis   = "none"
        yaxis   = "none"
        tree1   = "none"
        tree2   = "none"
        nBins   = 0
        firstBin = 0
        lastBin = 0
        binning = []
        yMin    = 0
        yMax    = 0 
        label = "none"
        label2 = "none"
        label3 = "none"
        filename = "none.pdf"
        log = False
        tree1 = "None"
        tree2 = "None"
        
        def __init__(self,variable,additionalCuts,binning = None, yRange = None,additionalName=None,DoCleanCuts = True):
                self.variable=variable.variable
                self.cuts="genWeight*weight*leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*(%s)" # 
                self.xaxis=variable.labelX
                self.yaxis=variable.labelY
                self.nBins=variable.nBins
                self.firstBin=variable.xMin
                self.lastBin=variable.xMax
                self.variablePlotName = variable.name
                self.yMin = 0.1
                self.yMax = 0
                self.label3="%s"
                self.filename=variable.name+"_%s"
                self.doCleanCuts = True
                self.additionalName = additionalName
                
                if not DoCleanCuts:
                        self.doCleanCuts = False

                if len(additionalCuts) >0:
                        for additionalCut in additionalCuts:
                                self.cuts=self.cuts%(additionalCut.cut+"&& %s")
                                self.label3 = self.label3%(additionalCut.label+" %s")
                                self.filename = self.filename%(additionalCut.name+"_%s")
                if binning != None:
                        self.nBins = binning[0]
                        self.firstBin = binning[1]
                        self.lastBin = binning [2]
                        self.yaxis = binning [3]
                        self.binning = binning[4]
                if yRange != None:
                        self.yMin = yRange[0]
                        self.yMax = yRange[0]
                if additionalName != None:
                        self.filename = self.filename%(additionalName+"_%s")
                self.filename = self.filename.replace("_%s","%s.pdf") 
                self.label3 = self.label3.replace("%s","")
        
        
        def clone(self,selection):
                tempPlot = Plot(theVariables.Met,[])
                if getMassSelection(selection) != None:
                        tempPlot.cuts = "genWeight*weight*(%s)"%(getMassSelection(selection).cut+"&& %s")
                        tempPlot.overlayLabel = getMassSelection(selection).name
                else:
                        tempPlot.cuts=self.cuts
                        tempPlot.overlayLabel = "None"                  
                tempPlot.variable=self.variable
                tempPlot.xaxis=self.xaxis
                tempPlot.yaxis=self.yaxis
                tempPlot.nBins=self.nBins
                tempPlot.firstBin=self.firstBin
                tempPlot.lastBin=self.lastBin
                tempPlot.yMin = 0.1
                tempPlot.yMax = 0
                tempPlot.label3="%s"
                tempPlot.filename=self.filename 
                return tempPlot 
        
        def addRunRange(self, runRange):
                self.cuts = self.cuts % runRange.runCut
                if runRange.weight != None:
                        self.cuts = "%s*%s"%(runRange.weight, self.cuts)
        
        def addRegion(self,region):
                self.cuts = self.cuts%(region.cut+" %s")
                self.filename = region.name+"_"+self.filename
                self.label = region.labelRegion
                self.label2 = region.labelSubRegion
                self.regionName = region.name
                self.log = region.logY
        def addDilepton(self,dilepton):
                if dilepton == "SF":
                        self.tree1 = "EE"
                        self.tree2 = "MuMu"
                elif dilepton == "OF":
                        self.tree1 = "EMu"
                        self.tree2 = "None"
                else:           
                        self.tree1 = dilepton
                        self.tree2 = "None"             
        def cleanCuts(self):
                if self.doCleanCuts:
                        if self.variable == "met" or self.variable == "type1Met" or self.variable == "tcMet" or self.variable == "caloMet" or self.variable == "mht":
                                cuts = self.cuts.split("&&")
                                metCutUp = []
                                metCutDown = [] 
                                for cut in cuts:
                                        if "met >" in cut:
                                                metCutUp.append(cut)
                                        elif "met <" in cut:
                                                metCutDown.append(cut)
                                        elif "< met" in cut:
                                                metCutDown.append(cut)
                                for cut in metCutUp:
                                        self.cuts = self.cuts.replace(cut.split(")")[0],"")
                                for cut in metCutDown:
                                        self.cuts = self.cuts.replace(cut,"")
                                self.cuts = self.cuts.replace("&&)",")")
                                self.cuts = self.cuts.replace("&& &&","&&")
                                self.cuts = self.cuts.replace("&&&&&&","&&")                            
                                self.cuts = self.cuts.replace("&&&&","&&")

                        if self.variable == "ht":
                                cuts = self.cuts.split("&&")
                                htCutUp = "" 
                                htCutDown = "" 
                                for cut in cuts:
                                        if "ht >" in cut:
                                                htCupUp = cut
                                        elif "ht <" in cut:
                                                htCutDown = cut
                                self.cuts = self.cuts.replace(htCutUp,"")
                                self.cuts = self.cuts.replace(htCutDown,"")
                                self.cuts = self.cuts.replace("&& &&","&&")
                                self.cuts = self.cuts.replace("&&&&","&&")                      
                        if self.variable == "p4.M()":
                                cuts = self.cuts.split("&&")
                                mllCutUp = "" 
                                mllCutDown = "" 
                                for cut in cuts:
                                        if "p4.M() > 60" in cut:
                                                subcuts = cut.split("*(")
                                                mllCutUp = subcuts[1]
                                        elif "p4.M() < 120" in cut:
                                                mllCutDown = cut
                                self.cuts = self.cuts.replace(mllCutUp,"")
                                self.cuts = self.cuts.replace(mllCutDown,"")
                                self.cuts = self.cuts.replace("&& &&","&&")
                                self.cuts = self.cuts.replace("&&&&","&&")      
                                self.cuts = self.cuts.replace("(&&","(")        
                                
                        if self.variable == "mll":
                                cuts = self.cuts.split("&&")
                                mllCutUp = "" 
                                mllCutDown = "" 
                                for cut in cuts:
                                        if "mll > 60" in cut:
                                                subcuts = cut.split("*(")
                                                mllCutUp = subcuts[1]
                                        elif "mll < 120" in cut:
                                                mllCutDown = cut
                                self.cuts = self.cuts.replace(mllCutUp,"")
                                self.cuts = self.cuts.replace(mllCutDown,"")
                                self.cuts = self.cuts.replace("&& &&","&&")
                                self.cuts = self.cuts.replace("&&&&","&&")      
                                self.cuts = self.cuts.replace("(&&","(")        
                                
                        if self.variable == "nJets":
                                cuts = self.cuts.split("&&")
                                nJetsCutUp = [] 
                                nJetsCutDown = [] 
                                nJetsCutEqual = []
                                for cut in cuts:
                                        if "nJets >" in cut:
                                                nJetsCutUp.append(cut)
                                        elif "nJets <" in cut:
                                                nJetsCutDown.append(cut)
                                        elif "nJets ==" in cut:
                                                nJetsCutEqual.append(cut)
                                for cut in nJetsCutUp:
                                        if "weight" and "(((" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*(((")
                                        elif "weight" and "((!(" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*((!(")
                                        elif "weight" and "((" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*((")
                                        elif "weight" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*(")
                                        elif "(" in cut:
                                                self.cuts = self.cuts.replace(cut.split("(")[1],"")
                                        else:
                                                self.cuts = self.cuts.replace(cut,"")
                                for cut in nJetsCutDown:
                                        if "weight" and "(((" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*(((")
                                        elif "weight" and "((!(" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*((!(")
                                        elif "weight" and "((" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*((")
                                        elif "weight" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*(")
                                        elif "(" in cut:
                                                self.cuts = self.cuts.replace(cut.split("(")[1],"")
                                        else:
                                                self.cuts = self.cuts.replace(cut,"")
                                for cut in nJetsCutEqual:
                                        if "weight" and "(((" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*(((")
                                        elif "weight" and "((!(" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*((!(")
                                        elif "weight" and "((" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*((")
                                        elif "weight" in cut:
                                                self.cuts = self.cuts.replace(cut,"genWeight*weight*(")
                                        elif "(" in cut:
                                                self.cuts = self.cuts.replace(cut.split("(")[1],"")
                                        else:
                                                self.cuts = self.cuts.replace(cut,"")
                                                
                                self.cuts = self.cuts.replace("&& &&","&&")
                                self.cuts = self.cuts.replace("&&&&","&&")                      
                                self.cuts = self.cuts.replace("( &&","(")                       
                                self.cuts = self.cuts.replace("(&&","(")        
                        if (self.additionalName == "trailingPt10" or self.additionalName == "leadingPt30Single") and "pt" in self.variable:
                                self.cuts = self.cuts.replace("&& pt1 > 20 && pt2 > 20  &&", "&&")              
                else:
                        print "Cut cleaning deactivated for this plot!"
                
class thePlots:                   
        mllPlotThreeBins = Plot(theVariables.Mll,[], binning=[96,20,500,"Events / Bin", [20,81,101,300,500]])
        mllPlot10GeV = Plot(theVariables.Mll,[], binning=[28,20,300,"Events / 10 GeV", []])
        mllPlot10GeVShifted = Plot(theVariables.Mll,[], binning=[28,25,305,"Events / 10 GeV", []])
        mllPlotFine = Plot(theVariables.Mll,[], binning=[50,20,120,"fraction / 2 GeV", []])
        mllPlot5GeV = Plot(theVariables.Mll,[], binning=[56,20,300,"Events / 5 GeV", []])
        
        
        deltaPhiLep1MetPlotC = Plot(theVariables.deltaPhiLep1Met,[])
        deltaPhiLep2MetPlotC = Plot(theVariables.deltaPhiLep2Met,[])
        metPlotC = Plot(theVariables.Met,[], binning=[15,150,900,"Events / 50 GeV",[]])
        nJetsPlotC = Plot(theVariables.nJets,[], binning=[6,3,8,"Events",[]])
        htPlotC = Plot(theVariables.HT,[], binning=[15,100,1600,"Events / 100 GeV",[]])
        stPlotC = Plot(theVariables.ST,[], binning=[16,400,2000,"Events / 100 GeV",[]])
        ptllPlotC = Plot(theVariables.Ptll,[])
        mt2PlotC = Plot(theVariables.MT2,[], binning=[10,0,200,"Events / Bin",[80,100,120,160,180,200,220]])
        mllPlotC = Plot(theVariables.Mll,[], binning=[96,20,500,"Events / Bin", []])
        mllWidePlotC = Plot(theVariables.Mll,[], binning=[96,20,500,"Events / Bin", [20,50,86,96,150,200,300,400,500]])
        deltaPhiPlotC = Plot(theVariables.deltaPhi,[])
        

        metPlot = Plot(theVariables.Met,[])
        rawMetPlot = Plot(theVariables.RawMet,[])
        metPlotEdgeMass = Plot(theVariables.Met,[theCuts.massCuts.edgeMass])
        metPlotLowMass = Plot(theVariables.Met,[theCuts.massCuts.lowMass])
        metPlotZMass = Plot(theVariables.Met,[theCuts.massCuts.zMass])
        metPlotHighMass = Plot(theVariables.Met,[theCuts.massCuts.highMass])
        metPlotLowPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.lowPU])
        metPlotMidPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.midPU])
        metPlotHighPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.highPU])
        metPlot0Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.noJet])
        metPlot1Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.OneJet])
        metPlot2Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.TwoJet])
        metPlot3Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.ThreeJet])
        metPlotnoBTags = Plot(theVariables.Met,[theCuts.bTags.noBTags])
        metPlotwithBTags = Plot(theVariables.Met,[theCuts.bTags.geOneBTags])
        metPlotCentralBarrel = Plot(theVariables.Met,[theCuts.etaCuts.CentralBarrel])
        metPlotOuterBarrel = Plot(theVariables.Met,[theCuts.etaCuts.OuterBarrel])
        metPlotEndcap = Plot(theVariables.Met,[theCuts.etaCuts.Endcap])
        metPlotlowDR = Plot(theVariables.Met,[theCuts.dRCuts.lowDR])
        metPlotmidDR = Plot(theVariables.Met,[theCuts.dRCuts.midDR])
        metPlothighDR = Plot(theVariables.Met,[theCuts.dRCuts.highDR])
        metPlotType1 = Plot(theVariables.Type1Met,[])
        metPlotCalo = Plot(theVariables.CaloMet,[])
        metPlotTc = Plot(theVariables.TcMet,[])
        metPlotUncertaintyHighMET = Plot(theVariables.Met,[theCuts.htCuts.ht100,theCuts.nJetsCuts.geTwoJetCut])
        metPlotUncertaintyLowMET = Plot(theVariables.Met,[theCuts.nJetsCuts.geThreeJetCut])
        metPlot100 = Plot(theVariables.Met,[],binning = [30,100,400,"Events / 10 Gev",[]],additionalName = "MET100")
        metPlot100 = Plot(theVariables.Met,[],binning = [30,100,400,"Events / 10 Gev",[]],additionalName = "MET100")
        metPlot100NoClean = Plot(theVariables.Met,[],binning = [30,100,400,"Events / 10 Gev",[]],additionalName = "MET100Cuts",DoCleanCuts=False)
        

        
        metPlotNoClean = Plot(theVariables.Met,[],binning = [15,0,150,"Events / 10 Gev",[]],additionalName = "NoClean",DoCleanCuts=False)
        
        
        htPlot = Plot(theVariables.HT,[])               
        htPlotEdgeMass = Plot(theVariables.HT,[theCuts.massCuts.edgeMass])              
        htPlotLowMass = Plot(theVariables.HT,[theCuts.massCuts.lowMass])                
        htPlotHighMass = Plot(theVariables.HT,[theCuts.massCuts.highMass])      
        htPlotUntertaintyHighMET = Plot(theVariables.HT,[theCuts.metCuts.met150])       
        htPlotUntertaintyLowMET = Plot(theVariables.HT,[theCuts.metCuts.met100])

        mhtPlot = Plot(theVariables.MHT,[])
        
        mt2Plot = Plot(theVariables.MT2,[])
        mt2PlotHighMass = Plot(theVariables.MT2,[theCuts.massCuts.highMass])

        eta1Plot = Plot(theVariables.Eta1,[])           
        trailingEtaPlot = Plot(theVariables.TrailingEta,[])              
        LeadingEtaPlot = Plot(theVariables.LeadingEta,[])               
        leadingEtaPlot = Plot(theVariables.LeadingEta,[])               
        eta2Plot = Plot(theVariables.Eta2,[])

        ptElePlot = Plot(theVariables.PtEle,[])         
        ptMuPlot = Plot(theVariables.PtMu,[])
        trailingPtPlot = Plot(theVariables.TrailingPt,[])
        trailingPtPlot100 = Plot(theVariables.TrailingPt,[],binning = [16,20,100,"Events / 5 Gev",[]],additionalName = "range100")
        leadingPtPlot = Plot(theVariables.LeadingPt,[])
        trailingPtPlotEdgeMass = Plot(theVariables.TrailingPt,[theCuts.massCuts.edgeMass])
        trailingPtPlotLowMass = Plot(theVariables.TrailingPt,[theCuts.massCuts.lowMass])
        leadingPtPlotEdgeMass = Plot(theVariables.LeadingPt,[theCuts.massCuts.edgeMass])
        leadingPtPlotLowMass = Plot(theVariables.LeadingPt,[theCuts.massCuts.lowMass])
        trailingPtPlotHighMass = Plot(theVariables.TrailingPt,[theCuts.massCuts.highMass])
        leadingPtPlotHighMass = Plot(theVariables.LeadingPt,[theCuts.massCuts.highMass])

        trailingIsoPlot = Plot(theVariables.TrailingIso,[])
        
        nLLPlot   = Plot(theVariables.nLL,  [])
        nLLPlotLowMll = Plot(theVariables.nLL,[theCuts.massCuts.lowMass])
        nLLPlotHighMll = Plot(theVariables.nLL,[theCuts.massCuts.highMassOld])



        mllPlot = Plot(theVariables.Mll,[])
        mllPlotEleLeading = Plot(theVariables.Mll,[theCuts.ptCuts.eleLeading])
        mllPlotMuLeading = Plot(theVariables.Mll,[theCuts.ptCuts.muLeading])
        mllPlotGeOneBTags = Plot(theVariables.Mll,[theCuts.bTags.geOneBTags])
        mllPlotNoBTags = Plot(theVariables.Mll,[theCuts.bTags.noBTags])
        mllPlotGeTwoBTags = Plot(theVariables.Mll,[theCuts.bTags.geTwoBTags])
        mllPlotEdgeMass = Plot(theVariables.Mll,[theCuts.massCuts.edgeMass])
        mllPlotLowMass = Plot(theVariables.Mll,[theCuts.massCuts.lowMass])
        mllPlotHighMass = Plot(theVariables.Mll,[theCuts.massCuts.highMassOld])
        mllPlotOnZ = Plot(theVariables.Mll,[theCuts.massCuts.zMass])
        mllPlotZpeak = Plot(theVariables.Mll,[],binning = [30,60,120,"Events / 2 Gev",[]],additionalName = "ZPeak")
        mllPlotLowNLL = Plot(theVariables.Mll,[theCuts.nLLCuts.lowNLL])
        mllPlotHighNLL = Plot(theVariables.Mll,[theCuts.nLLCuts.highNLL])
        
        mllPlotHighMT2 = Plot(theVariables.Mll,[theCuts.mt2Cuts.highMT2])
        mllPlotHighMllHighMT2 = Plot(theVariables.Mll,[theCuts.massCuts.highMass,theCuts.mt2Cuts.highMT2])

        nJetsPlot = Plot(theVariables.nJets,[])
        leadingJetPtPlot = Plot(theVariables.leadingJetPt,[])
        subleadingJetPtPlot = Plot(theVariables.subleadingJetPt,[])
        nJetsPlotEdgeMass = Plot(theVariables.nJets,[theCuts.massCuts.edgeMass])
        nJetsPlotLowMass = Plot(theVariables.nJets,[theCuts.massCuts.lowMass])
        nJetsPlotHighMass = Plot(theVariables.nJets,[theCuts.massCuts.highMass])

        nBJetsPlot = Plot(theVariables.nBJets,[])
        nBJetsPlotEdgeMass = Plot(theVariables.nBJets,[theCuts.massCuts.edgeMass])
        nBJetsPlotLowMass = Plot(theVariables.nBJets,[theCuts.massCuts.lowMass])
        nBJetsPlotHighMass = Plot(theVariables.nBJets,[theCuts.massCuts.highMass])
        
        nLightLeptonsPlot = Plot(theVariables.nLightLeptons,[])

        deltaRPlot = Plot(theVariables.deltaR,[])
        deltaRPlotEdgeMass = Plot(theVariables.deltaR,[theCuts.massCuts.edgeMass])
        deltaRPlotLowMass = Plot(theVariables.deltaR,[theCuts.massCuts.lowMass])
        deltaRPlotHighMass = Plot(theVariables.deltaR,[theCuts.massCuts.highMass])

        ptllPlot = Plot(theVariables.Ptll,[])
        ptllPlotEdgeMass = Plot(theVariables.Ptll,[theCuts.massCuts.edgeMass])
        ptllPlotLowMass = Plot(theVariables.Ptll,[theCuts.massCuts.lowMass])
        ptllPlotHighMass = Plot(theVariables.Ptll,[theCuts.massCuts.highMass])
        
        sumMlbPlot = Plot(theVariables.sumMlb,[])
        
        deltaPhiPlot = Plot(theVariables.deltaPhi,[])

        nVtxPlot = Plot(theVariables.nVtx,[],binning=[40,0,40,"Events",[]])                               

                        
        ### plots for trigger efficiency measurements
        nJetsPlotTriggerMC = Plot(theVariables.nJets,[],binning=[9,1.5,10.5,"Events",[]])
        nBJetsPlotTriggerMC = Plot(theVariables.nBJets,[],binning=[6,-0.5,5.5,"Events",[]])
        leadingPtPlotTriggerTrailing10MC= Plot(theVariables.LeadingPt,[],binning=[9,20,90,"Events / 10 GeV",[]],additionalName = "trailingPt10")
        leadingPtPlotTriggerMC= Plot(theVariables.LeadingPt,[],binning=[38,10,200,"Events / 5 GeV",[]])
        trailingPtPlotTriggerMC= Plot(theVariables.TrailingPt,[],binning=[38,10,200,"Events / 5 GeV",[]])
        #~ leadingPtPlotTriggerMC= Plot(theVariables.LeadingPt,[],binning=[30,20,320,"Events / 10 GeV",[]])
        #~ trailingPtPlotTriggerMC= Plot(theVariables.TrailingPt,[],binning=[18,20,200,"Events / 10 GeV",[]])
        trailingPtPlotTriggerLeading30MC = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[9,20,90,"Events / 10 GeV",[]],additionalName = "leadingPt30")
        trailingPtPlotTriggerLeading30SingleMC = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[10,10,110,"Events / 10 GeV",[]],additionalName = "leadingPt30Single")
        mllPlotTriggerMC = Plot(theVariables.Mll,[],binning=[30,20,520,"Events / 17 GeV",[]])                                                   
        #~ htPlotTriggerMC = Plot(theVariables.HT,[],binning=[20,200,1000,"Events / 40 GeV",[]])                                
        htPlotTriggerMC = Plot(theVariables.HT,[],binning=[20,200,1200,"Events / 50 GeV",[]])                           
        metPlotTriggerMC = Plot(theVariables.Met,[],binning=[15,0,200,"Events / 20 GeV",[]])                            
        nVtxPlotTriggerMC = Plot(theVariables.nVtx,[],binning=[15,0,60,"Events / 2",[]])                                
        tralingEtaPlotTriggerMC = Plot(theVariables.AbsTrailingEta,[],binning=[24,0,2.4,"Events / 0.1",[]])
        leadingEtaPlotTriggerMC = Plot(theVariables.AbsLeadingEta,[],binning=[24,0,2.4,"Events / 0.1",[]])
        deltaRPlotTriggerMC = Plot(theVariables.deltaR,[],binning=[35,0,3.5,"Events / 0.1",[]])
        mt2PlotTriggerMC = Plot(theVariables.MT2,[],binning=[18,0,120,"Events / 10 GeV",[]])
        deltaPhiPlotTriggerMC = Plot(theVariables.deltaPhi,[],binning=[30,0,3.2,"Events / 0.4",[]])                             
        ptllPlotTriggerMC = Plot(theVariables.Ptll,[],binning=[20,0,400,"Events / 20 GeV",[]])                  
        sumMlbPlotTriggerMC = Plot(theVariables.sumMlb,[],binning=[25,0,500,"Events / 20 GeV",[]])
        
                                        
        #~ ptllPlotTriggerMC = Plot(theVariables.Ptll,[],binning=[40,0,1000,"Events / 25 GeV",[]])                                      

        #~ nJetsPlotTrigger = Plot(theVariables.nJets,[],binning=[6,-0.5,11.5,"Events",[]])
        nJetsPlotTrigger = Plot(theVariables.nJets,[],binning=[6,1.5,7.5,"Events",[]])
        nBJetsPlotTrigger = Plot(theVariables.nBJets,[],binning=[5,-0.5,4.5,"Events",[]])
        #~ leadingPtPlotTriggerTrailing10= Plot(theVariables.LeadingPt,[],binning=[9,20,90,"Events / 10 GeV",[]],additionalName = "trailingPt10")
        #~ leadingPtPlotTrigger= Plot(theVariables.LeadingPt,[],binning=[10,20,320,"Events / 30 GeV",[]])
        leadingPtPlotTrigger= Plot(theVariables.LeadingPt,[],binning=[24,0,120,"Events / 5 GeV",[]])
        #~ leadingPtPlotTrigger= Plot(theVariables.LeadingPt,[],binning=[26,20,150,"Events / 5 GeV",[]])
        #~ trailingPtPlotTrigger= Plot(theVariables.TrailingPt,[],binning=[9,20,200,"Events / 20 GeV",[]])
        #~ trailingPtPlotTrigger= Plot(theVariables.TrailingPt,[],binning=[9,20,200,"Events / 20 GeV",[]])
        trailingPtPlotTrigger= Plot(theVariables.TrailingPt,[],binning=[24,0,120,"Events / 5 GeV",[]])
        trailingPtPlotTriggerLeading30 = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[40,0,100,"Events / 2.5 GeV",[]],additionalName = "leadingPt30")
        trailingPtPlotTriggerLeading30Single = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[40,0,100,"Events / 2.5 GeV",[]],additionalName = "leadingPt30Single")
        trailingPtPlotTriggerLeading30SingleOnZ = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30,theCuts.massCuts.looseZ],binning=[40,0,100,"Events / 2.5 GeV",[]],additionalName = "leadingPt30SingleOnZ")
        trailingPtPlotTriggerLeading40Single = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt40],binning=[40,0,100,"Events / 2.5 GeV",[]],additionalName = "leadingPt40Single")
        #~ mllPlotTrigger = Plot(theVariables.Mll,[],binning=[4,20,300,"Events / 40 GeV",[]])                                                   
        mllPlotTrigger = Plot(theVariables.Mll,[],binning=[10,20,520,"Events / 50 GeV",[]])                                                     
        mllPlotTriggerLeading30Single = Plot(theVariables.Mll,[theCuts.ptCuts.leadingPt30],binning=[7,20,300,"Events / 40 GeV",[]],additionalName = "leadingPt30Single")                                                        
        htPlotTrigger = Plot(theVariables.HT,[],binning=[10,200,1200,"Events / 100 GeV",[]])                            
        #~ htPlotTrigger = Plot(theVariables.HT,[],binning=[20,0,1000,"Events / 50 GeV",[]])                            
        metPlotTrigger = Plot(theVariables.Met,[],binning=[5,0,200,"Events / 40 GeV",[]])                       
        #~ metPlotTrigger = Plot(theVariables.Met,[],binning=[30,0,300,"Events / 10 GeV",[]])                           
        nVtxPlotTrigger = Plot(theVariables.nVtx,[],binning=[15,0,60,"Events / 4",[]])                           
        tralingEtaPlotTrigger = Plot(theVariables.AbsTrailingEta,[],binning=[12,0,2.4,"Events / 0.3",[]])
        leadingEtaPlotTrigger = Plot(theVariables.AbsLeadingEta,[],binning=[12,0,2.4,"Events / 0.3",[]])
        #~ tralingEtaPlotTrigger = Plot(theVariables.TrailingEta,[],binning=[12,-2.4,2.4,"Events / 0.3",[]])
        #~ leadingEtaPlotTrigger = Plot(theVariables.LeadingEta,[],binning=[12,-2.4,2.4,"Events / 0.3",[]])
        
        deltaRPlotTrigger = Plot(theVariables.deltaR,[],binning=[35,0,3.5,"Events / 0.1",[]])
        mt2PlotTrigger = Plot(theVariables.MT2,[],binning=[6,0,120,"Events / 20 GeV",[]])
        
        deltaPhiPlotTrigger = Plot(theVariables.deltaPhi,[],binning=[10,0,3.2,"Events / 0.4",[]])                               
        #~ deltaPhiPlotTrigger = Plot(theVariables.deltaPhi,[],binning=[32,0,3.2,"Events / 0.1",[]])                            
        ptllPlotTrigger = Plot(theVariables.Ptll,[],binning=[10,0,400,"Events / 40 GeV",[]])                    
        sumMlbPlotTrigger = Plot(theVariables.sumMlb,[],binning=[10,0,500,"Events / 50 GeV",[]])        

                        
        ### plots for isolation efficiency measurements
        leadingPtPlotIso= Plot(theVariables.LeadingPt,[],binning=[24,0,120,"Events / 5 GeV",[]])
        trailingPtPlotIso= Plot(theVariables.TrailingPt,[],binning=[24,0,120,"Events / 5 GeV",[]])
        mllPlotIso = Plot(theVariables.Mll,[],binning=[28,20,300,"Events / 10 GeV",[]])                                                 
                                        
                        
        ### plots for rmue measurements
        nJetsPlotRMuE = Plot(theVariables.nJets,[],binning=[9,-0.5,8.5,"Events",[]])
        nBJetsPlotRMuE = Plot(theVariables.nBJets,[],binning=[7,-0.5,6.5,"Events",[]])
        leadingPtPlotRMuE= Plot(theVariables.LeadingPt,[],binning=[46,20,250,"Events / 5 GeV",[]])
        #~ trailingPtPlotRMuE= Plot(theVariables.TrailingPt,[],binning=[38,10,200,"Events / 5 GeV",[]])
        trailingPtPlotRMuE= Plot(theVariables.TrailingPt,[],binning=[-1,10,200,"Events / 5 GeV",range(20,100,5)+range(100,160,10)+range(160,220,20)])
        #~ leadingPtPlotRMuE= Plot(theVariables.LeadingPt,[],binning=[16,20,100,"Events / 5 GeV",[]],additionalName = "PU4BX50")
        #~ trailingPtPlotRMuE= Plot(theVariables.TrailingPt,[],binning=[18,10,100,"Events / 5 GeV",[]],additionalName = "PU4BX50")
        trailingPtPlotRMuELeading30 = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[16,20,100,"Events / 5 GeV",[]],additionalName = "leadingPt30")
        mllPlotRMuE = Plot(theVariables.Mll,[],binning=[-1,20,500,"Events / 10 GeV",range(20,60,10)+range(60,120,10)+range(120,300,25)+range(300,550,50)])                                                      
        #~ mllPlotRMuE = Plot(theVariables.Mll,[],binning=[-1,20,200,"Events / 10 GeV",range(20,60,10)+range(60,120,10)+range(120,250,25)],additionalName = "PU4BX50")                                                  
        htPlotRMuE = Plot(theVariables.HT,[],binning=[-1,0,400,"Events / 40 GeV",range(0,300,50)+range(300,800,100)])                           
        metPlotRMuE = Plot(theVariables.Met,[],binning=[-1,0,450,"Events / 20 GeV",range(0,100,10)+range(100,150,25)+range(150,500,50)])                                
        nVtxPlotRMuE = Plot(theVariables.nVtx,[],binning=[65,0,65,"Events / 1",[]])                             
        tralingEtaPlotRMuE = Plot(theVariables.AbsTrailingEta,[],binning=[-1,0,2.55,"Events / 0.3",[i*0.14 for i in range(0,10)]+[i*0.2+1.4 for i in range(0,6)]])                              
        leadingEtaPlotRMuE = Plot(theVariables.AbsLeadingEta,[],binning=[-1,0,2.55,"Events / 0.3",[i*0.14 for i in range(0,10)]+[i*0.2+1.4 for i in range(0,6)]])                               
        #~ tralingEtaPlotRMuE = Plot(theVariables.TrailingEta,[],binning=[-1,-2.55,2.55,"Events / 0.3",[i*0.2-2.5 for i in range(0,6)]+[i*0.14-1.4 for i in range(0,20)]+[i*0.2+1.4 for i in range(0,6)]])                              
        #~ leadingEtaPlotRMuE = Plot(theVariables.LeadingEta,[],binning=[-1,-2.55,2.55,"Events / 0.3",[i*0.2-2.5 for i in range(0,6)]+[i*0.14-1.4 for i in range(0,20)]+[i*0.2+1.4 for i in range(0,6)]])                               
        deltaRPlotRMuE = Plot(theVariables.deltaR,[],binning=[-1,0,5.5,"Events / 0.3",[0.2*i for i in range(10)]+[2+0.5*i for i in range(7)]])                          
        #~ deltaPhiPlotRMuE = Plot(theVariables.deltaPhi,[],binning=[-1,0,3.2,"Events / 0.2",[0.2*i for i in range(10)]+[2+0.3*i for i in range(4)]])                           
        deltaPhiPlotRMuE = Plot(theVariables.deltaPhi,[],binning=[16,0,3.2,"Events / 0.2",[]])                          
        ptllPlotRMuE = Plot(theVariables.Ptll,[],binning=[-1,0,300,"Events / 20 GeV",range(0,100,10)+range(100,200,25)+range(200,350,50)])                      
        sumMlbPlotRMuE = Plot(theVariables.sumMlb,[],binning=[-1,0,500,"Events / 20 GeV",range(0,300,25)+range(300,550,50)])                    
                        
                                                                
        mllPlotRMuESignal = Plot(theVariables.Mll,[],binning=[28,20,300,"Events / 10 GeV",[]])
        #~ mllPlotRMuESignal = Plot(theVariables.Mll,[],binning=[5,20,300,"Events / 10 GeV",[20,70,81,101,120,300]])
        
        mt2PlotRMuE = Plot(theVariables.MT2,[],binning=[-1,0,150,"Events / 10 GeV",range(0,80,10)+range(80,100,20)+range(100,200,50)])
        
        ### plots for rSFOF measurements
        #~ nJetsPlotRSFOF = Plot(theVariables.nJets,[],binning=[8,-0.5,7.5,"Events",[]])
        nJetsPlotRSFOF = Plot(theVariables.nJets,[],binning=[5,1.5,6.5,"Events",[]])
        nBJetsPlotRSFOF = Plot(theVariables.nBJets,[],binning=[5,-0.5,4.5,"Events",[]])
        #~ leadingPtPlotRSFOF= Plot(theVariables.LeadingPt,[],binning=[-1,25,250,"Events / 10 GeV",range(25,45,10)+range(45,75,15)+range(75,200,25)+range(200,300,50)])
        #~ trailingPtPlotRSFOF= Plot(theVariables.TrailingPt,[],binning=[-1,20,150,"Events / 10 GeV",range(20,70,10)+range(70,110,20)+range(110,190,40)])
        leadingPtPlotRSFOF= Plot(theVariables.LeadingPt,[],binning=[30,0,150,"Events / 5 GeV",[]])
        trailingPtPlotRSFOF= Plot(theVariables.TrailingPt,[],binning=[30,0,150,"Events / 5 GeV",[]])
        #~ mllPlotRSFOF = Plot(theVariables.Mll,[],binning=[-1,20,500,"Events / 10 GeV",range(20,70,25)+range(70,110,20)+range(110,150,20)+range(150,200,25)+range(200,300,50)+range(300,600,100)])                                                                             
        mllPlotRSFOF = Plot(theVariables.Mll,[],binning=[-1,20,500,"Events / 10 GeV",range(20,70,25)+range(70,110,40)+range(110,150,40)+range(150,300,50)+range(300,600,100)])                                                                          
        htPlotRSFOF = Plot(theVariables.HT,[],binning=[-1,0,500,"Events / 40 GeV",range(0,400,40)+range(400,600,100)])                          
        metPlotRSFOF = Plot(theVariables.Met,[],binning=[-1,100,450,"Events / 20 GeV",range(0,100,10)+range(100,150,25)+range(150,250,50)+range(250,550,100)])                          
        #~ metPlotRSFOF = Plot(theVariables.Met,[],binning=[-1,100,300,"Events / 20 GeV",range(0,100,10)+range(100,150,25)+range(150,200,50)+range(200,500,100)])                               
        #~ metPlotRSFOF = Plot(theVariables.Met,[],binning=[-1,100,400,"Events / 20 GeV",range(0,100,10)+range(100,150,25)+range(150,450,50)])                          
        nVtxPlotRSFOF = Plot(theVariables.nVtx,[],binning=[10,0,40,"Events / 1",[]])                            
        tralingEtaPlotRSFOF = Plot(theVariables.AbsTrailingEta,[],binning=[-1,0,2.55,"Events / 0.3",[i*0.14 for i in range(0,10)]+[i*0.2+1.4 for i in range(0,6)]])                             
        leadingEtaPlotRSFOF = Plot(theVariables.AbsLeadingEta,[],binning=[-1,0,2.55,"Events / 0.3",[i*0.14 for i in range(0,10)]+[i*0.2+1.4 for i in range(0,6)]])                                                              
        deltaRPlotRSFOF = Plot(theVariables.deltaR,[],binning=[-1,0,5.5,"Events / 0.3",[0.2*i for i in range(10)]+[2+0.5*i for i in range(7)]])                                         
        deltaPhiPlotRSFOF = Plot(theVariables.deltaPhi,[],binning=[10,0,3.2,"Events / 0.32",[]])                                
        ptllPlotRSFOF = Plot(theVariables.Ptll,[],binning=[-1,0,300,"Events / 20 GeV",range(0,100,20)+range(100,150,25)+range(150,350,50)])                     
        sumMlbPlotRSFOF = Plot(theVariables.sumMlb,[],binning=[-1,0,600,"Events / 20 GeV",range(0,300,50)+range(300,700,100)])                  
                        
                                                                
        mllPlotRSFOFSignal = Plot(theVariables.Mll,[],binning=[28,20,300,"Events / 10 GeV",[]])
        
        #~ mt2PlotRSFOF = Plot(theVariables.MT2,[],binning=[-1,0,120,"Events / 10 GeV",range(0,80,10)+range(80,140,20)])
        mt2PlotRSFOF = Plot(theVariables.MT2,[],binning=[-1,-5,120,"Events / 10 GeV",range(-5,5,10)+range(5,20,15)+range(20,140,20)])
        nLLPlotRSFOF = Plot(theVariables.nLL,[],binning=[-1,12,31,"Events / 10 GeV",range(12,21,1)+range(21,23,2)+range(23,26,3)+range(26,36,5)])
        
                                        
                                
        mllPlotROutIn = Plot(theVariables.Mll,[],binning=[2000,0,2000,"Events / 5 GeV",[]])                             
        metPlotROutIn = Plot(theVariables.Met,[],binning=[-1,0,100,"Events / 1 GeV",[0,10,20,30,40,50,60,80,100]])                              
        nJetsPlotROutIn = Plot(theVariables.nJets,[],binning=[7,-0.5,6.5,"Events / 1 GeV",[]])
        mt2PlotROutIn = Plot(theVariables.MT2,[],binning=[-1,0,120,"Events / 1 GeV",[0,10,20,30,40,50,60,70,80,100,120]])                               

        nVtxPlotWeights = Plot(theVariables.nVtx,[],binning=[60,0,60,"Events / 1",[]])          
        
        #~ mllResultPlot = Plot(theVariables.Mll,[],binning=[-1,20,500,"Events / 10 GeV",range(20,60,40)+range(60,86,26)+range(86,96,10)+range(96,150,54)+range(150,200,50)+range(200,600,100)])                
        mllResultPlot = Plot(theVariables.Mll,[],binning=[-1,20,500,"Events / 10 GeV",[20,60,86,96,150,200,300,400,500,10000]])         
        mllResultPlot2 = Plot(theVariables.Mll,[],binning=[-1,20,500,"Events / 10 GeV",range(20,60,40)+range(60,86,26)+range(86,96,10)+range(96,150,54)+range(150,200,50)+range(200,600,100)])  
                
        #~ metPlotSignal = Plot(theVariables.Met,[],binning=[45,150,600,"Events / 10 GeV",[]])          
        metPlotSignal = Plot(theVariables.Met,[],binning=[9,150,600,"Events / 50 GeV",[]])              
        
        mt2PlotSignal = Plot(theVariables.MT2,[],binning=[8,80,240,"Events / 20 GeV",[]])
        
        mllPlotRSFOFCentralVal = Plot(theVariables.Mll,[],binning=[1000,20,500,"Events / GeV",[]])                         

        
class Signals:  
        class T6bbllslepton_msbottom_550_mneutralino_175:
                subprocesses = ["T6bbllslepton_msbottom_550_mneutralino_175"]
                label            = "m_{#tilde{b}} = 550 GeV m_{#tilde{#chi}_{0}^{2}} = 175 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed-7
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None      
        
        class T6bbllslepton_msbottom_600_mneutralino_250:
                subprocesses = ["T6bbllslepton_msbottom_600_mneutralino_250"]
                label            = "m_{#tilde{b}} = 600 GeV m_{#tilde{#chi}_{0}^{2}} = 250 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed-5
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
        
        class T6bbllslepton_msbottom_600_mneutralino_175:
                subprocesses = ["T6bbllslepton_msbottom_600_mneutralino_175"]
                label            = "m_{#tilde{b}} = 600 GeV m_{#tilde{#chi}_{0}^{2}} = 175 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kBlack
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
        
        class T6bbllslepton_msbottom_600_mneutralino_400:
                subprocesses = ["T6bbllslepton_msbottom_600_mneutralino_400"]
                label            = "m_{#tilde{b}} = 600 GeV m_{#tilde{#chi}_{0}^{2}} = 400 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kBlue
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        class T6bbllslepton_msbottom_600_mneutralino_575:
                subprocesses = ["T6bbllslepton_msbottom_600_mneutralino_575"]
                label            = "m_{#tilde{b}} = 600 GeV m_{#tilde{#chi}_{0}^{2}} = 575 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        
        class T6bbllslepton_msbottom_700_mneutralino_250:
                subprocesses = ["T6bbllslepton_msbottom_700_mneutralino_250"]
                label            = "m_{#tilde{b}} = 700 GeV m_{#tilde{#chi}_{0}^{2}} = 250 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed-5
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
        
        class T6bbllslepton_msbottom_700_mneutralino_150:
                subprocesses = ["T6bbllslepton_msbottom_700_mneutralino_150"]
                label            = "m_{#tilde{b}} = 700 GeV m_{#tilde{#chi}_{0}^{2}} = 150 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kBlack
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
        
        class T6bbllslepton_msbottom_700_mneutralino_175:
                subprocesses = ["T6bbllslepton_msbottom_700_mneutralino_175"]
                label            = "m_{#tilde{b}} = 700 GeV m_{#tilde{#chi}_{0}^{2}} = 175 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kBlack
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
        
        class T6bbllslepton_msbottom_700_mneutralino_400:
                subprocesses = ["T6bbllslepton_msbottom_700_mneutralino_400"]
                label            = "m_{#tilde{b}} = 700 GeV m_{#tilde{#chi}_{0}^{2}} = 400 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kBlue
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        class T6bbllslepton_msbottom_700_mneutralino_575:
                subprocesses = ["T6bbllslepton_msbottom_700_mneutralino_575"]
                label            = "m_{#tilde{b}} = 700 GeV m_{#tilde{#chi}_{0}^{2}} = 575 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        class T6bbllslepton_msbottom_750_mneutralino_175:
                subprocesses = ["T6bbllslepton_msbottom_750_mneutralino_175"]
                #~ label                 = "m_{#tilde{b}} = 750 GeV m_{#tilde{#chi}_{0}^{2}} = 175 GeV"
                label            = "m(#tilde{b}) = 750 GeV, m(#tilde{#chi}_{0}^{2}) = 175 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kBlack
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        class T6bbllslepton_msbottom_750_mneutralino_250:
                subprocesses = ["T6bbllslepton_msbottom_750_mneutralino_250"]
                #~ label                 = "m_{#tilde{b}} = 750 GeV m_{#tilde{#chi}_{0}^{2}} = 250 GeV"
                label            = "m(#tilde{b}) = 750 GeV, m(#tilde{#chi}_{0}^{2}) = 250 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        class T6bbllslepton_msbottom_750_mneutralino_400:
                subprocesses = ["T6bbllslepton_msbottom_750_mneutralino_400"]
                #~ label                 = "m_{#tilde{b}} = 750 GeV m_{#tilde{#chi}_{0}^{2}} = 400 GeV"
                label            = "m(#tilde{b}) = 750 GeV, m(#tilde{#chi}_{0}^{2}) = 400 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kBlue
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        class T6bbllslepton_msbottom_900_mneutralino_200:
                subprocesses = ["T6bbllslepton_msbottom_900_mneutralino_200"]
                label            = "m_{#tilde{b}} = 900 GeV m_{#tilde{#chi}_{0}^{2}} = 200 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kGreen+2
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        class T6bbllslepton_msbottom_900_mneutralino_750:
                subprocesses = ["T6bbllslepton_msbottom_900_mneutralino_750"]
                label            = "m_{#tilde{b}} = 900 GeV m_{#tilde{#chi}_{0}^{2}} = 750 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kOrange+8
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        class T6bbllslepton_msbottom_1000_mneutralino_150:
                subprocesses = ["T6bbllslepton_msbottom_1000_mneutralino_150"]
                label            = "m_{#tilde{b}} = 1000 GeV m_{#tilde{#chi}_{0}^{2}} = 150 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kBlack
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        class T6bbllslepton_msbottom_1000_mneutralino_250:
                subprocesses = ["T6bbllslepton_msbottom_1000_mneutralino_250"]
                label            = "m_{#tilde{b}} = 1000 GeV m_{#tilde{#chi}_{0}^{2}} = 250 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None
                
        class T6bbllslepton_msbottom_1000_mneutralino_400:
                subprocesses = ["T6bbllslepton_msbottom_1000_mneutralino_400"]
                label            = "m_{#tilde{b}} = 1000 GeV m_{#tilde{#chi}_{0}^{2}} = 400 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kBlue
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None      
                        
                
class Backgrounds2016:
        
        class T6bbllslepton:
                subprocesses = ["T6bbllslepton_msbottom_550_mneutralino_250"]
                label            = "m_{#tilde{b}} = 550 GeV m_{#tilde{#chi}_{0}^{2}} = 175 GeV"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed-7
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None 
        
        class T6bbllslepton_msbottom_1200_mneutralino_150:
                subprocesses = ["T6bbllslepton_msbottom_1200_mneutralino_150"]
                label            = "T6bbllslepton_msbottom_1200_mneutralino_150"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed-7
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None 
                
        class T6bbllslepton_msbottom_1200_mneutralino_850:
                subprocesses = ["T6bbllslepton_msbottom_1200_mneutralino_850"]
                label            = "T6bbllslepton_msbottom_1200_mneutralino_850"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed-7
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None 
        class T6bbllslepton_msbottom_1200_mneutralino_1100:
                subprocesses = ["T6bbllslepton_msbottom_1200_mneutralino_1100"]
                label            = "T6bbllslepton_msbottom_1200_mneutralino_1100"
                fillcolor    = ROOT.kWhite
                linecolor    = ROOT.kRed-7
                uncertainty      = 0.
                scaleFac     = 1.
                additionalSelection = None 
        
        class TTJets_Madgraph:
                subprocesses = ["TTJets_Dilepton_Madgraph_MLM_Summer16_25ns"]
                label = "t#bar{t} Madgraph"
                fillcolor = ROOT.kRed
                #fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None
        class TT_aMCatNLO:
                subprocesses = ["TT_Dilepton_aMCatNLO_FXFX_Summer16_25ns"]
                label = "aMC@NLO t#bar{t}"
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None
        class TT_Powheg:
                #~ subprocesses = ["TT_Semileptonic_Powheg_Summer16_25ns"]
                #subprocesses = ["TT_Dilepton_Powheg_Summer16_25ns"]
                subprocesses = ["TT_Dilepton_Powheg_Summer16_25ns","TT_Semileptonic_Powheg_Summer16_25ns"]
                label = "t#bar{t} Powheg"
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None
                
        class TT_incl_Powheg:
                subprocesses = ["TT_Powheg_Summer16_25ns"]
                label = "Powheg t#bar{t}, incl"
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None

        class TT_semiLept_Powheg:
                subprocesses = ["TT_Semileptonic_Powheg_Summer16_25ns"]
                label = "Powheg t#bar{t}, semi lept."
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None

        class DrellYan:
                #~ subprocesses = ["ZJets_Madgraph_Summer16_25ns","AStar_aMCatNLO_Summer16_25ns"]
                subprocesses = ["ZJets_Madgraph_Summer16_25ns","AStar_Madgraph_Summer16_25ns"]
                label = "DY+jets"
                fillcolor = 401
                linecolor = ROOT.kBlack 
                uncertainty = 0.2
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
                #~ additionalSelection = None
                
        class ZJetsOnly:
                subprocesses = ["ZJets_Madgraph_Summer16_25ns"]
                label = "DY+jets"
                fillcolor = 401
                linecolor = ROOT.kBlack 
                uncertainty = 0.2
                scaleFac     = 1.       
                #~ additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
                additionalSelection = None
        class DrellYanLO:
                subprocesses = ["ZJets_Madgraph_Summer16_25ns","AStar_Madgraph_Summer16_25ns"]
                label = "DY+jets"
                fillcolor = 401
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
                #~ additionalSelection = None
        class WJets:
                subprocesses = ["WJetsToLNu_aMCatNLO_Summer16_25ns"]
                label = "W+jets"
                fillcolor = 401
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = None
        class DrellYanTauTau:
                #~ subprocesses = ["ZJets_Madgraph_Summer16_25ns","AStar_aMCatNLO_Summer16_25ns"]
                subprocesses = ["ZJets_Madgraph_Summer16_25ns","AStar_Madgraph_Summer16_25ns"]
                label = "DY+jets (#tau#tau)"
                fillcolor = ROOT.kOrange
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 15 && abs(motherPdgId2) == 15)"
        class SingleTop:
                #"ST_sChannel_4f_aMCatNLO_Summer16_25ns",
                subprocesses = ["ST_top_tChannel_4f_Powheg_Summer16_25ns","ST_antitop_tChannel_4f_Powheg_Summer16_25ns","ST_antitop_tWChannel_5f_Powheg_NoFullyHadronicDecays_Summer16_25ns","ST_top_tWChannel_5f_Powheg_NoFullyHadronicDecays_Summer16_25ns"]
                label = "Single t"
                fillcolor = 854
                linecolor = ROOT.kBlack
                uncertainty = 0.06
                scaleFac     = 1.
                additionalSelection = None
                
        class Rare:
                subprocesses = ["ST_top_tWllChannel_5f_MadGraph_Summer16_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Summer16_25ns","TTZToQQ_aMCatNLO_FXFX_Summer16_25ns","TTWToLNu_aMCatNLO_FXFX_Summer16_25ns","TTWToQQ_aMCatNLO_FXFX_Summer16_25ns","TTG_aMCatNLO_FXFX_Summer16_25ns","4T_aMCatNLO_FXFX_Summer16_25ns","WZZ_aMCatNLO_FXFX_Summer16_25ns","WWZ_aMCatNLO_FXFX_Summer16_25ns","ZZZ_aMCatNLO_FXFX_Summer16_25ns","TTHToNonbb_Powheg_Summer16_25ns","TTHTobb_Powheg_Summer16_25ns","VH_ToNonbb_aMCatNLO_Summer16_25ns"]
                #~ subprocesses = ["TTZToLLNuNu_aMCatNLO_FXFX_Summer16_25ns","TTZToQQ_aMCatNLO_FXFX_Summer16_25ns","TTWToLNu_aMCatNLO_FXFX_Summer16_25ns","TTWToQQ_aMCatNLO_FXFX_Summer16_25ns","TTG_aMCatNLO_FXFX_Summer16_25ns","4T_aMCatNLO_FXFX_Summer16_25ns","WZZ_aMCatNLO_FXFX_Summer16_25ns","WWZ_aMCatNLO_FXFX_Summer16_25ns","ZZZ_aMCatNLO_FXFX_Summer16_25ns","TTHToNonbb_Powheg_Summer16_25ns","TTHTobb_Powheg_Summer16_25ns","VH_ToNonbb_aMCatNLO_Summer16_25ns"]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = None                      
                
        class TTZNonFS:
                subprocesses = ["TTZToLLNuNu_aMCatNLO_FXFX_Summer16_25ns"]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"                    
                
        class RareNonFS:
                subprocesses = ["ST_top_tWllChannel_5f_MadGraph_Summer16_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Summer16_25ns","TTZToQQ_aMCatNLO_FXFX_Summer16_25ns","TTWToLNu_aMCatNLO_FXFX_Summer16_25ns","TTWToQQ_aMCatNLO_FXFX_Summer16_25ns","TTG_aMCatNLO_FXFX_Summer16_25ns","4T_aMCatNLO_FXFX_Summer16_25ns","WZZ_aMCatNLO_FXFX_Summer16_25ns","WWZ_aMCatNLO_FXFX_Summer16_25ns","ZZZ_aMCatNLO_FXFX_Summer16_25ns","TTHToNonbb_Powheg_Summer16_25ns","TTHTobb_Powheg_Summer16_25ns","VH_ToNonbb_aMCatNLO_Summer16_25ns"]
                #~ subprocesses = ["TZQ_LL_aMCatNLO_Summer16_25ns","WZZ_aMCatNLO_FXFX_Summer16_25ns","WWZ_aMCatNLO_FXFX_Summer16_25ns","ZZZ_aMCatNLO_FXFX_Summer16_25ns",]
                label = "Other SM"
                fillcolor = ROOT.kRed-7
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23) || (abs(motherPdgId1) == 22 && abs(motherPdgId2) == 22)"                    
                
        class RareFS:
                subprocesses = ["ST_top_tWllChannel_5f_MadGraph_Summer16_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Summer16_25ns","TTZToQQ_aMCatNLO_FXFX_Summer16_25ns","TTWToLNu_aMCatNLO_FXFX_Summer16_25ns","TTWToQQ_aMCatNLO_FXFX_Summer16_25ns","TTG_aMCatNLO_FXFX_Summer16_25ns","4T_aMCatNLO_FXFX_Summer16_25ns","WZZ_aMCatNLO_FXFX_Summer16_25ns","WWZ_aMCatNLO_FXFX_Summer16_25ns","ZZZ_aMCatNLO_FXFX_Summer16_25ns","TTHToNonbb_Powheg_Summer16_25ns","TTHTobb_Powheg_Summer16_25ns","VH_ToNonbb_aMCatNLO_Summer16_25ns"]
                label = "Other FS SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "!(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"                   

        class Diboson:
                # "ZZTo2L2Q_aMCatNLO_Summer16_25ns",
                subprocesses = ["WWTo2L2Nu_Powheg_Summer16_25ns","WWTo1L1Nu2Q_aMCatNLO_Summer16_25ns","WZTo1L1Nu2Q_aMCatNLO_Summer16_25ns","WZTo1L3Nu_aMCatNLO_Summer16_25ns","WZTo2L2Q_aMCatNLO_Summer16_25ns","WZTo3LNu_aMCatNLO_Summer16_25ns","ZZTo4Q_aMCatNLO_Summer16_25ns","ZZTo4L_Powheg_Summer16_25ns","ZZTo2Q2Nu_aMCatNLO_Summer16_25ns","ZZTo2L2Nu_Powheg_Summer16_25ns"]
                label = "WW,WZ,ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = None      
                                
                        
        class DibosonNonFS:
                subprocesses = ["WZTo2L2Q_aMCatNLO_Summer16_25ns","WZTo3LNu_Powheg_Summer16_25ns","ZZTo4L_Powheg_Summer16_25ns","ZZTo2L2Q_aMCatNLO_Summer16_25ns","ZZTo2L2Nu_Powheg_Summer16_25ns"]
                label = "WZ,ZZ (not FS)"
                fillcolor = ROOT.kGray
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"    
                        
        class ZZNonFS:
                subprocesses = ["ZZTo4L_Powheg_Summer16_25ns","ZZTo2L2Q_aMCatNLO_Summer16_25ns","ZZTo2L2Nu_Powheg_Summer16_25ns"]
                label = "ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"    
                        
        class WZNonFS:
                subprocesses = ["WZTo3LNu_Powheg_Summer16_25ns"]
                label = "WZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"    
                        
        class DibosonFS:
                subprocesses = ["WWTo2L2Nu_Powheg_Summer16_25ns","WWTo1L1Nu2Q_aMCatNLO_Summer16_25ns","WZTo1L1Nu2Q_aMCatNLO_Summer16_25ns","WZTo1L3Nu_aMCatNLO_Summer16_25ns","WZTo3LNu_aMCatNLO_Summer16_25ns","ZZTo4Q_aMCatNLO_Summer16_25ns","ZZTo4L_Powheg_Summer16_25ns","ZZTo2Q2Nu_aMCatNLO_Summer16_25ns","ZZTo2L2Q_aMCatNLO_Summer16_25ns","ZZTo2L2Nu_Powheg_Summer16_25ns"]
                label = "WW,WZ (FS)"
                fillcolor = ROOT.kGray+2
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "!(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"   
                
                        
        class RareWZOnZ:
                subprocesses = ["WZTo3LNu_Powheg_Summer16_25ns"]
                label = "WZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
        class RareZZOnZ:
                subprocesses = ["ZZTo2L2Nu_Powheg_Summer16_25ns"]
                label = "ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
        class RareTTZOnZ:
                subprocesses = ["TTZToLLNuNu_aMCatNLO_FXFX_Summer16_25ns"]
                label = "TTZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
        class RareRestOnZ:
                subprocesses = ["ST_top_tWllChannel_5f_MadGraph_Summer16_25ns","TZQ_LL_aMCatNLO_Summer16_25ns","WZZ_aMCatNLO_FXFX_Summer16_25ns","WWZ_aMCatNLO_FXFX_Summer16_25ns","ZZZ_aMCatNLO_FXFX_Summer16_25ns"]
                label = "Rare"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                #~ additionalSelection = "( (abs(motherPdgId1) == 23 || (abs(grandMotherPdgId1) == 23 && abs(motherPdgId1) != 15)) && (abs(motherPdgId2) == 23 || (abs(grandMotherPdgId2) == 23 && abs(motherPdgId2) != 15)) && genMet > 20)"
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
                        
        class RareOnZ:
                subprocesses = ["WZTo3LNu_Powheg_Summer16_25ns","ZZTo2L2Nu_Powheg_Summer16_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Summer16_25ns","ST_top_tWllChannel_5f_MadGraph_Summer16_25ns","TZQ_LL_aMCatNLO_Summer16_25ns","WZZ_aMCatNLO_FXFX_Summer16_25ns","WWZ_aMCatNLO_FXFX_Summer16_25ns","ZZZ_aMCatNLO_FXFX_Summer16_25ns","TTHToNonbb_Powheg_Summer16_25ns","VH_ToNonbb_aMCatNLO_Summer16_25ns"]
                label = "Rares"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "( ((abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23) || (abs(motherPdgId1) == 22 && abs(motherPdgId2) == 22)) && genMet > 20)"
                
        class ZJets:
                subprocesses = ["ZJets_Madgraph_Summer16_25ns","AStar_Madgraph_Summer16_25ns","WZTo2L2Q_aMCatNLO_Summer16_25ns","ZZTo4L_Powheg_Summer16_25ns","ZZTo2L2Q_aMCatNLO_Summer16_25ns","ST_top_tWllChannel_5f_MadGraph_Summer16_25ns","TZQ_LL_aMCatNLO_Summer16_25ns","WZZ_aMCatNLO_FXFX_Summer16_25ns","WWZ_aMCatNLO_FXFX_Summer16_25ns","ZZZ_aMCatNLO_FXFX_Summer16_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Summer16_25ns","TTHToNonbb_Powheg_Summer16_25ns","VH_ToNonbb_aMCatNLO_Summer16_25ns"]
                label = "Z + jets"
                fillcolor = 401
                linecolor = 401 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "( ((abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23) || (abs(motherPdgId1) == 22 && abs(motherPdgId2) == 22)) && genMet < 20)"
                
        class DrellYanNonResonant:
                subprocesses = ["ZJets_Madgraph_Summer16_25ns","AStar_Madgraph_Summer16_25ns"]
                label = "DY+jets non resonant"
                fillcolor = 401
                linecolor = ROOT.kBlack
                uncertainty = 0.2
                scaleFac     = 1.       
                additionalSelection = "!(abs(motherPdgId1) == 15 && abs(motherPdgId2) == 15) && !(abs(motherPdgId1) == 22 && abs(motherPdgId2) != 22) && !(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"
                
        class OtherSM:
                subprocesses = ["WWTo2L2Nu_Powheg_Summer16_25ns","WWTo1L1Nu2Q_aMCatNLO_Summer16_25ns","WZTo3LNu_Powheg_Summer16_25ns","WZTo1L1Nu2Q_aMCatNLO_Summer16_25ns","WZTo1L3Nu_aMCatNLO_Summer16_25ns","ZZTo2Q2Nu_aMCatNLO_Summer16_25ns","ZZTo4Q_aMCatNLO_Summer16_25ns","WWZ_aMCatNLO_FXFX_Summer16_25ns","WZZ_aMCatNLO_FXFX_Summer16_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Summer16_25ns","TTZToQQ_aMCatNLO_FXFX_Summer16_25ns","TZQ_LL_aMCatNLO_Summer16_25ns","TTWToLNu_aMCatNLO_FXFX_Summer16_25ns","TTWToQQ_aMCatNLO_FXFX_Summer16_25ns","TTG_aMCatNLO_FXFX_Summer16_25ns","4T_aMCatNLO_FXFX_Summer16_25ns","TTHToNonbb_Powheg_Summer16_25ns","TTHTobb_Powheg_Summer16_25ns","VH_ToNonbb_aMCatNLO_Summer16_25ns"]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) != 23 || abs(motherPdgId2) != 23)"    
                
class Backgrounds2017:        
        class TTJets_Madgraph:
                subprocesses = ["TTJets_Dilepton_Madgraph_MLM_Fall17_25ns"]
                label = "Madgraph t#bar{t} + jets"
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None
        class TT_aMCatNLO:
                subprocesses = ["TT_Dilepton_aMCatNLO_FXFX_Fall17_25ns"]
                label = "aMC@NLO t#bar{t}"
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None
        class TT_Powheg:
                #~ subprocesses = []
                subprocesses = ["TT_Dilepton_Powheg_Fall17_25ns", "TT_Semileptonic_Powheg_Fall17_25ns"]
                label = "t#bar{t}"
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None
                
        class TT_incl_Powheg:
                subprocesses = ["TT_Powheg_Fall17_25ns"]
                label = "Powheg t#bar{t}, incl"
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None

        class TT_semiLept_Powheg:
                subprocesses = ["TT_Semileptonic_Powheg_Fall17_25ns"]
                label = "Powheg t#bar{t}, semi lept."
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None

        class DrellYan:
                #subprocesses = ["ZJets_Madgraph_Fall17_25ns","AStar_Madgraph_Fall17_25ns"]
                subprocesses = ["ZJets_aMCatNLO_FXFX_Fall17_25ns","AStar_MadGraph_Fall17_25ns"]
                label = "DY+jets"
                fillcolor = 401
                linecolor = ROOT.kBlack 
                uncertainty = 0.2
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
                #~ additionalSelection = None
                
        class ZJetsOnly:
                subprocesses = ["ZJets_Madgraph_Fall17_25ns"]
                label = "DY+jets"
                fillcolor = 401
                linecolor = ROOT.kBlack 
                uncertainty = 0.2
                scaleFac     = 1.       
                #~ additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
                additionalSelection = None
        class WJets:
                subprocesses = ["WJetsToLNu_aMCatNLO_Fall17_25ns"]
                label = "W+jets"
                fillcolor = 401
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = None
        class DrellYanTauTau:
                #subprocesses = ["ZJets_Madgraph_Fall17_25ns","AStar_Madgraph_Fall17_25ns"]
                subprocesses = ["ZJets_aMCatNLO_FXFX_Fall17_25ns","AStar_MadGraph_Fall17_25ns"]
                label = "DY+jets (#tau#tau)"
                fillcolor = ROOT.kOrange
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 15 && abs(motherPdgId2) == 15)"
        class SingleTop:
                #
                subprocesses = ["ST_sChannel_4f_aMCatNLO_Fall17_25ns","ST_top_tChannel_4f_Powheg_Fall17_25ns","ST_antitop_tChannel_4f_Powheg_Fall17_25ns","ST_antitop_tWChannel_5f_Powheg_NoFullyHadronicDecays_Fall17_25ns","ST_top_tWChannel_5f_Powheg_NoFullyHadronicDecays_Fall17_25ns"]
                label = "Single t"
                fillcolor = 854
                linecolor = ROOT.kBlack
                uncertainty = 0.06
                scaleFac     = 1.
                additionalSelection = None
                
        class Rare:
                # "ST_top_tWllChannel_5f_MadGraph_Fall17_25ns" ,"TTG_aMCatNLO_FXFX_Fall17_25ns", 
                subprocesses = ["WZZ_aMCatNLO_Fall17_25ns", "WWZ_aMCatNLO_Fall17_25ns","ZZZ_aMCatNLO_Fall17_25ns","TTZToLLNuNu_aMCatNLO_Fall17_25ns","TTZToQQ_aMCatNLO_Fall17_25ns","TTWToLNu_aMCatNLO_FXFX_Fall17_25ns","TTWToQQ_aMCatNLO_FXFX_Fall17_25ns","4T_aMCatNLO_Fall17_25ns","TTHToNonbb_Powheg_Fall17_25ns","TTHTobb_Powheg_Fall17_25ns","VH_ToNonbb_aMCatNLO_Fall17_25ns"]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = None                      
                
        class TTZNonFS:
                subprocesses = ["TTZToLLNuNu_aMCatNLO_FXFX_Fall17_25ns"]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"                    
                
        class RareNonFS:
                subprocesses = ["ST_top_tWllChannel_5f_MadGraph_Fall17_25ns","TZQ_LL_aMCatNLO_Fall17_25ns","WZZ_aMCatNLO_FXFX_Fall17_25ns","WWZ_aMCatNLO_FXFX_Fall17_25ns","ZZZ_aMCatNLO_FXFX_Fall17_25ns",]
                #~ subprocesses = ["TZQ_LL_aMCatNLO_Fall17_25ns","WZZ_aMCatNLO_FXFX_Fall17_25ns","WWZ_aMCatNLO_FXFX_Fall17_25ns","ZZZ_aMCatNLO_FXFX_Fall17_25ns",]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"                    
                
        class RareFS:
                # "ST_top_tWllChannel_5f_MadGraph_Fall17_25ns"
                subprocesses = ["WZZ_aMCatNLO_Fall17_25ns", "WWZ_aMCatNLO_Fall17_25ns","ZZZ_aMCatNLO_Fall17_25ns","TTZToLLNuNu_aMCatNLO_Fall17_25ns","TTZToQQ_aMCatNLO_Fall17_25ns","TTWToLNu_aMCatNLO_FXFX_Fall17_25ns","TTWToQQ_aMCatNLO_FXFX_Fall17_25ns","4T_aMCatNLO_Fall17_25ns","TTHToNonbb_Powheg_Fall17_25ns","TTHTobb_Powheg_Fall17_25ns","VH_ToNonbb_aMCatNLO_Fall17_25ns"]
                label = "Other FS SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "!(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"                   

        class Diboson:
                #  "ZZTo4Q_aMCatNLO_Fall17_25ns",
                subprocesses = ["ZZTo4L_Powheg_Fall17_25ns","ZZTo2Q2Nu_aMCatNLO_FXFX_Fall17_25ns","ZZTo2L2Q_aMCatNLO_FXFX_Fall17_25ns","ZZTo2L2Nu_Powheg_Fall17_25ns","WZTo3LNu_aMCatNLO_FXFX_Fall17_25ns","WZTo2L2Q_aMCatNLO_FXFX_Fall17_25ns","WWTo2L2Nu_Powheg_Fall17_25ns","WWTo1L1Nu2Q_aMCatNLO_FXFX_Fall17_25ns","WZTo1L1Nu2Q_aMCatNLO_FXFX_Fall17_25ns","WZTo1L3Nu_aMCatNLO_FXFX_Fall17_25ns"]
                label = "WW,WZ,ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = None      
                                
                        
        class DibosonNonFS:
                subprocesses = ["WZTo2L2Q_aMCatNLO_Fall17_25ns","WZTo3LNu_Powheg_Fall17_25ns","ZZTo4L_Powheg_Fall17_25ns","ZZTo2L2Q_aMCatNLO_Fall17_25ns","ZZTo2L2Nu_Powheg_Fall17_25ns"]
                label = "WW,WZ,ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"    
                        
        class ZZNonFS:
                subprocesses = ["ZZTo4L_Powheg_Fall17_25ns","ZZTo2L2Q_aMCatNLO_Fall17_25ns","ZZTo2L2Nu_Powheg_Fall17_25ns"]
                label = "ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"    
                        
        class WZNonFS:
                subprocesses = ["WZTo3LNu_Powheg_Fall17_25ns"]
                label = "WZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"    

        class DibosonFS:
                subprocesses = ["WWTo2L2Nu_Powheg_Fall17_25ns","WWTo1L1Nu2Q_aMCatNLO_FXFX_Fall17_25ns","WZTo1L1Nu2Q_aMCatNLO_FXFX_Fall17_25ns","WZTo3LNu_aMCatNLO_FXFX_Fall17_25ns","ZZTo4L_Powheg_Fall17_25ns","ZZTo2Q2Nu_aMCatNLO_FXFX_Fall17_25ns","ZZTo2L2Q_aMCatNLO_FXFX_Fall17_25ns","ZZTo2L2Nu_Powheg_Fall17_25ns", "WZTo1L3Nu_aMCatNLO_FXFX_Fall17_25ns"]
                label = "WW,WZ (FS part)"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "!(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"   
                
                        
        class RareWZOnZ:
                subprocesses = ["WZTo3LNu_Powheg_Fall17_25ns"]
                label = "WZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
        class RareZZOnZ:
                subprocesses = ["ZZTo2L2Nu_Powheg_Fall17_25ns"]
                label = "ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
        class RareTTZOnZ:
                subprocesses = ["TTZToLLNuNu_aMCatNLO_FXFX_Fall17_25ns"]
                label = "TTZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
        class RareRestOnZ:
                subprocesses = ["ST_top_tWllChannel_5f_MadGraph_Fall17_25ns","TZQ_LL_aMCatNLO_Fall17_25ns","WZZ_aMCatNLO_FXFX_Fall17_25ns","WWZ_aMCatNLO_FXFX_Fall17_25ns","ZZZ_aMCatNLO_FXFX_Fall17_25ns"]
                label = "Rare"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                #~ additionalSelection = "( (abs(motherPdgId1) == 23 || (abs(grandMotherPdgId1) == 23 && abs(motherPdgId1) != 15)) && (abs(motherPdgId2) == 23 || (abs(grandMotherPdgId2) == 23 && abs(motherPdgId2) != 15)) && genMet > 20)"
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
                        
        class RareOnZ:
                subprocesses = ["WZTo3LNu_Powheg_Fall17_25ns","ZZTo2L2Nu_Powheg_Fall17_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Fall17_25ns","ST_top_tWllChannel_5f_MadGraph_Fall17_25ns","TZQ_LL_aMCatNLO_Fall17_25ns","WZZ_aMCatNLO_FXFX_Fall17_25ns","WWZ_aMCatNLO_FXFX_Fall17_25ns","ZZZ_aMCatNLO_FXFX_Fall17_25ns","TTHToNonbb_Powheg_Fall17_25ns","VH_ToNonbb_aMCatNLO_Fall17_25ns"]
                label = "Rares"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "( ((abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23) || (abs(motherPdgId1) == 22 && abs(motherPdgId2) == 22)) && genMet > 20)"
                
        class ZJets:
                subprocesses = ["ZJets_Madgraph_Fall17_25ns","AStar_Madgraph_Fall17_25ns","WZTo2L2Q_aMCatNLO_Fall17_25ns","ZZTo4L_Powheg_Fall17_25ns","ZZTo2L2Q_aMCatNLO_Fall17_25ns","ST_top_tWllChannel_5f_MadGraph_Fall17_25ns","TZQ_LL_aMCatNLO_Fall17_25ns","WZZ_aMCatNLO_FXFX_Fall17_25ns","WWZ_aMCatNLO_FXFX_Fall17_25ns","ZZZ_aMCatNLO_FXFX_Fall17_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Fall17_25ns","TTHToNonbb_Powheg_Fall17_25ns","VH_ToNonbb_aMCatNLO_Fall17_25ns"]
                label = "Z + jets"
                fillcolor = 401
                linecolor = 401 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "( ((abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23) || (abs(motherPdgId1) == 22 && abs(motherPdgId2) == 22)) && genMet < 20)"
                
        class DrellYanNonResonant:
                subprocesses = ["ZJets_Madgraph_Fall17_25ns","AStar_Madgraph_Fall17_25ns"]
                label = "DY+jets non resonant"
                fillcolor = 401
                linecolor = ROOT.kBlack
                uncertainty = 0.2
                scaleFac     = 1.       
                additionalSelection = "!(abs(motherPdgId1) == 15 && abs(motherPdgId2) == 15) && !(abs(motherPdgId1) == 22 && abs(motherPdgId2) != 22) && !(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"
                
        class OtherSM:
                subprocesses = ["WWTo2L2Nu_Powheg_Fall17_25ns","WWTo1L1Nu2Q_aMCatNLO_Fall17_25ns","WZTo3LNu_Powheg_Fall17_25ns","WZTo1L1Nu2Q_aMCatNLO_Fall17_25ns","WZTo1L3Nu_aMCatNLO_Fall17_25ns","ZZTo2Q2Nu_aMCatNLO_Fall17_25ns","ZZTo4Q_aMCatNLO_Fall17_25ns","WWZ_aMCatNLO_FXFX_Fall17_25ns","WZZ_aMCatNLO_FXFX_Fall17_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Fall17_25ns","TTZToQQ_aMCatNLO_FXFX_Fall17_25ns","TZQ_LL_aMCatNLO_Fall17_25ns","TTWToLNu_aMCatNLO_FXFX_Fall17_25ns","TTWToQQ_aMCatNLO_FXFX_Fall17_25ns","TTG_aMCatNLO_FXFX_Fall17_25ns","4T_aMCatNLO_FXFX_Fall17_25ns","TTHToNonbb_Powheg_Fall17_25ns","TTHTobb_Powheg_Fall17_25ns","VH_ToNonbb_aMCatNLO_Fall17_25ns"]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) != 23 || abs(motherPdgId2) != 23)"    

class Backgrounds2018:        
        class TTJets_Madgraph:
                subprocesses = ["TTJets_Dilepton_Madgraph_MLM_Autumn18_25ns"]
                label = "Madgraph t#bar{t} + jets"
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None
        #class TT_aMCatNLO:
                #subprocesses = ["TT_Dilepton_aMCatNLO_FXFX_Fall17_25ns"]
                #label = "aMC@NLO t#bar{t}"
                #fillcolor = 855
                #linecolor = ROOT.kBlack
                #uncertainty = 0.07
                #scaleFac     = 1.0
                #additionalSelection = None
        class TT_Powheg:
                #~ subprocesses = []
                subprocesses = ["TT_Dilepton_Powheg_Autumn18_25ns", "TT_Semileptonic_Powheg_Autumn18_25ns"]
                label = "t#bar{t}"
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None
                
        #class TT_incl_Powheg:
                #subprocesses = ["TT_Powheg_Fall17_25ns"]
                #label = "Powheg t#bar{t}, incl"
                #fillcolor = 855
                #linecolor = ROOT.kBlack
                #uncertainty = 0.07
                #scaleFac     = 1.0
                #additionalSelection = None

        class TT_semiLept_Powheg:
                subprocesses = ["TT_Semileptonic_Powheg_Autumn18_25ns"]
                label = "Powheg t#bar{t}, semi lept."
                fillcolor = 855
                linecolor = ROOT.kBlack
                uncertainty = 0.07
                scaleFac     = 1.0
                additionalSelection = None

        class DrellYan:
                #subprocesses = ["ZJets_Madgraph_Fall17_25ns","AStar_Madgraph_Fall17_25ns"]
                subprocesses = ["ZJets_MadGraph_Autumn18_25ns","AStar_MadGraph_Autumn18_25ns"]
                label = "DY+jets"
                fillcolor = 401
                linecolor = ROOT.kBlack 
                uncertainty = 0.2
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
                #~ additionalSelection = None
                
        class ZJetsOnly:
                subprocesses = ["ZJets_MadGraph_Autumn18_25ns"]
                label = "DY+jets"
                fillcolor = 401
                linecolor = ROOT.kBlack 
                uncertainty = 0.2
                scaleFac     = 1.       
                #~ additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
                additionalSelection = None
        class WJets:
                subprocesses = ["WJetsToLNu_aMCatNLO_Autumn18_25ns"]
                label = "W+jets"
                fillcolor = 401
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = None
        class DrellYanTauTau:
                #subprocesses = ["ZJets_Madgraph_Fall17_25ns","AStar_Madgraph_Fall17_25ns"]
                subprocesses = ["ZJets_MadGraph_Autumn18_25ns","AStar_MadGraph_Autumn18_25ns"]
                label = "DY+jets (#tau#tau)"
                fillcolor = ROOT.kOrange
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 15 && abs(motherPdgId2) == 15)"
        class SingleTop:
                #
                subprocesses = ["ST_sChannel_4f_aMCatNLO_Autumn18_25ns","ST_top_tChannel_4f_Powheg_Autumn18_25ns","ST_antitop_tChannel_4f_Powheg_Autumn18_25ns","ST_antitop_tWChannel_5f_Powheg_NoFullyHadronicDecays_Autumn18_25ns","ST_top_tWChannel_5f_Powheg_NoFullyHadronicDecays_Autumn18_25ns"]
                label = "Single t"
                fillcolor = 854
                linecolor = ROOT.kBlack
                uncertainty = 0.06
                scaleFac     = 1.
                additionalSelection = None
                
        class Rare:
                # "ST_top_tWllChannel_5f_MadGraph_Autumn18_25ns", "TTZToQQ_aMCatNLO_Autumn18_25ns",
                subprocesses = ["TTG_aMCatNLO_FXFX_Autumn18_25ns", "WZZ_aMCatNLO_Autumn18_25ns", "WWZ_aMCatNLO_Autumn18_25ns","ZZZ_aMCatNLO_Autumn18_25ns","TTZToLLNuNu_aMCatNLO_Autumn18_25ns","TTWToLNu_aMCatNLO_FXFX_Autumn18_25ns","TTWToQQ_aMCatNLO_FXFX_Autumn18_25ns","4T_aMCatNLO_Autumn18_25ns","TTHToNonbb_Powheg_Autumn18_25ns","TTHTobb_Powheg_Autumn18_25ns","VH_ToNonbb_aMCatNLO_Autumn18_25ns"]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = None                      
                
        class TTZNonFS:
                subprocesses = ["TTZToLLNuNu_aMCatNLO_FXFX_Autumn18_25ns"]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"                    
                
        class RareNonFS: 
                # "ST_top_tWllChannel_5f_MadGraph_Autumn18_25ns",
                subprocesses = ["TZQ_LL_aMCatNLO_Autumn18_25ns","WZZ_aMCatNLO_FXFX_Autumn18_25ns","WWZ_aMCatNLO_FXFX_Autumn18_25ns","ZZZ_aMCatNLO_FXFX_Autumn18_25ns",]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"                    
                
        class RareFS:
                # "ST_top_tWllChannel_5f_MadGraph_Autumn18_25ns", 
                subprocesses = ["TTZToLLNuNu_aMCatNLO_FXFX_Autumn18_25ns","TTZToQQ_aMCatNLO_FXFX_Autumn18_25ns","TTWToLNu_aMCatNLO_FXFX_Autumn18_25ns","TTWToQQ_aMCatNLO_FXFX_Autumn18_25ns","TTG_aMCatNLO_FXFX_Autumn18_25ns","4T_aMCatNLO_FXFX_Autumn18_25ns","WZZ_aMCatNLO_FXFX_Autumn18_25ns","WWZ_aMCatNLO_FXFX_Autumn18_25ns","ZZZ_aMCatNLO_FXFX_Autumn18_25ns","TTHToNonbb_Powheg_Autumn18_25ns","TTHTobb_Powheg_Autumn18_25ns","VH_ToNonbb_aMCatNLO_Autumn18_25ns"]
                label = "Other FS SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "!(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"                   

        class Diboson:
                #  "ZZTo4Q_aMCatNLO_Fall17_25ns", "ZZTo4L_Powheg_Autumn18_25ns", "ZZTo2Q2Nu_aMCatNLO_FXFX_Autumn18_25ns", "ZZTo2L2Nu_Powheg_Autumn18_25ns", "WZTo3LNu_aMCatNLO_FXFX_Autumn18_25ns", "WZTo2L2Q_aMCatNLO_FXFX_Autumn18_25ns", "WWTo2L2Nu_Powheg_Autumn18_25ns", "WWTo1L1Nu2Q_aMCatNLO_FXFX_Autumn18_25ns", "WZTo1L1Nu2Q_aMCatNLO_FXFX_Autumn18_25ns", "WZTo1L3Nu_aMCatNLO_FXFX_Autumn18_25ns"
                subprocesses = ["ZZTo2L2Q_aMCatNLO_FXFX_Autumn18_25ns",]
                label = "WW,WZ,ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = None      
                                
                        
        class DibosonNonFS:
                #"ZZTo4L_Powheg_Autumn18_25ns", ,"ZZTo2L2Nu_Powheg_Autumn18_25ns"
                subprocesses = ["WZTo2L2Q_aMCatNLO_Autumn18_25ns","WZTo3LNu_Powheg_Autumn18_25ns","ZZTo2L2Q_aMCatNLO_Autumn18_25ns"]
                label = "WW,WZ,ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"    
                        
        class ZZNonFS:
                # "ZZTo4L_Powheg_Autumn18_25ns", ,"ZZTo2L2Nu_Powheg_Autumn18_25ns"
                subprocesses = ["ZZTo2L2Q_aMCatNLO_Autumn18_25ns"]
                label = "ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"    
                        
        class WZNonFS:
                subprocesses = ["WZTo3LNu_Powheg_Autumn18_25ns"]
                label = "WZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"    
                        
        class DibosonFS: # "ZZTo4L_Powheg_Autumn18_25ns",,"ZZTo2L2Nu_Powheg_Autumn18_25ns"
                subprocesses = ["WWTo2L2Nu_Powheg_Autumn18_25ns","WWTo1L1Nu2Q_aMCatNLO_Autumn18_25ns","WZTo1L1Nu2Q_aMCatNLO_Autumn18_25ns","WZTo1L3Nu_aMCatNLO_Autumn18_25ns","WZTo3LNu_aMCatNLO_Autumn18_25ns","ZZTo4Q_aMCatNLO_Autumn18_25ns","ZZTo2Q2Nu_aMCatNLO_Autumn18_25ns","ZZTo2L2Q_aMCatNLO_Autumn18_25ns"]
                label = "WW,WZ (FS part)"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "!(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"   
                
                        
        class RareWZOnZ:
                subprocesses = ["WZTo3LNu_Powheg_Autumn18_25ns"]
                label = "WZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
        class RareZZOnZ:
                subprocesses = ["ZZTo2L2Nu_Powheg_Autumn18_25ns"]
                label = "ZZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
        class RareTTZOnZ:
                subprocesses = ["TTZToLLNuNu_aMCatNLO_FXFX_Autumn18_25ns"]
                label = "TTZ"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.3
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
        class RareRestOnZ:
                subprocesses = ["ST_top_tWllChannel_5f_MadGraph_Autumn18_25ns","TZQ_LL_aMCatNLO_Autumn18_25ns","WZZ_aMCatNLO_FXFX_Autumn18_25ns","WWZ_aMCatNLO_FXFX_Autumn18_25ns","ZZZ_aMCatNLO_FXFX_Autumn18_25ns"]
                label = "Rare"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                #~ additionalSelection = "( (abs(motherPdgId1) == 23 || (abs(grandMotherPdgId1) == 23 && abs(motherPdgId1) != 15)) && (abs(motherPdgId2) == 23 || (abs(grandMotherPdgId2) == 23 && abs(motherPdgId2) != 15)) && genMet > 20)"
                additionalSelection = "(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23 && genMet > 20)"
                        
                        
        class RareOnZ:
                subprocesses = ["WZTo3LNu_Powheg_Autumn18_25ns","ZZTo2L2Nu_Powheg_Autumn18_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Autumn18_25ns","ST_top_tWllChannel_5f_MadGraph_Autumn18_25ns","TZQ_LL_aMCatNLO_Autumn18_25ns","WZZ_aMCatNLO_FXFX_Autumn18_25ns","WWZ_aMCatNLO_FXFX_Autumn18_25ns","ZZZ_aMCatNLO_FXFX_Autumn18_25ns","TTHToNonbb_Powheg_Autumn18_25ns","VH_ToNonbb_aMCatNLO_Autumn18_25ns"]
                label = "Rares"
                fillcolor = 920
                linecolor = ROOT.kBlack 
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "( ((abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23) || (abs(motherPdgId1) == 22 && abs(motherPdgId2) == 22)) && genMet > 20)"
                
        class ZJets:
                #"ZZTo4L_Powheg_Autumn18_25ns",
                subprocesses = ["ZJets_Madgraph_Autumn18_25ns","AStar_Madgraph_Autumn18_25ns","WZTo2L2Q_aMCatNLO_Autumn18_25ns","ZZTo2L2Q_aMCatNLO_Autumn18_25ns","ST_top_tWllChannel_5f_MadGraph_Autumn18_25ns","TZQ_LL_aMCatNLO_Autumn18_25ns","WZZ_aMCatNLO_FXFX_Autumn18_25ns","WWZ_aMCatNLO_FXFX_Autumn18_25ns","ZZZ_aMCatNLO_FXFX_Autumn18_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Autumn18_25ns","TTHToNonbb_Powheg_Autumn18_25ns","VH_ToNonbb_aMCatNLO_Autumn18_25ns"]
                label = "Z + jets"
                fillcolor = 401
                linecolor = 401 
                uncertainty = 0.04
                scaleFac     = 1.       
                additionalSelection = "( ((abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23) || (abs(motherPdgId1) == 22 && abs(motherPdgId2) == 22)) && genMet < 20)"
                
        class DrellYanNonResonant:
                subprocesses = ["ZJets_Madgraph_Autumn18_25ns","AStar_Madgraph_Autumn18_25ns"]
                label = "DY+jets non resonant"
                fillcolor = 401
                linecolor = ROOT.kBlack
                uncertainty = 0.2
                scaleFac     = 1.       
                additionalSelection = "!(abs(motherPdgId1) == 15 && abs(motherPdgId2) == 15) && !(abs(motherPdgId1) == 22 && abs(motherPdgId2) != 22) && !(abs(motherPdgId1) == 23 && abs(motherPdgId2) == 23)"
                
        class OtherSM:
                subprocesses = ["WWTo2L2Nu_Powheg_Autumn18_25ns","WWTo1L1Nu2Q_aMCatNLO_Autumn18_25ns","WZTo3LNu_Powheg_Autumn18_25ns","WZTo1L1Nu2Q_aMCatNLO_Autumn18_25ns","WZTo1L3Nu_aMCatNLO_Autumn18_25ns","ZZTo2Q2Nu_aMCatNLO_Autumn18_25ns","ZZTo4Q_aMCatNLO_Autumn18_25ns","WWZ_aMCatNLO_FXFX_Autumn18_25ns","WZZ_aMCatNLO_FXFX_Autumn18_25ns","TTZToLLNuNu_aMCatNLO_FXFX_Autumn18_25ns","TTZToQQ_aMCatNLO_FXFX_Autumn18_25ns","TZQ_LL_aMCatNLO_Autumn18_25ns","TTWToLNu_aMCatNLO_FXFX_Autumn18_25ns","TTWToQQ_aMCatNLO_FXFX_Autumn18_25ns","TTG_aMCatNLO_FXFX_Autumn18_25ns","4T_aMCatNLO_FXFX_Autumn18_25ns","TTHToNonbb_Powheg_Autumn18_25ns","TTHTobb_Powheg_Autumn18_25ns","VH_ToNonbb_aMCatNLO_Autumn18_25ns"]
                label = "Other SM"
                fillcolor = 630
                linecolor = ROOT.kBlack
                uncertainty = 0.5
                scaleFac     = 1.       
                additionalSelection = "(abs(motherPdgId1) != 23 || abs(motherPdgId2) != 23)"    

      
class Backgrounds(maplike):
        pass
        
Backgrounds["for2016"] =  Backgrounds2016
Backgrounds["for2017"] =  Backgrounds2017 
Backgrounds["for2018"] =  Backgrounds2018

# temporary ########################################
for key,entry in Backgrounds2016.__dict__.iteritems():
        if not "__" in key:
                setattr(Backgrounds, key, entry)
####################################################



# Color definition
#==================
defineMyColors = {
        'Black' : (0, 0, 0),
        'White' : (255, 255, 255),
        'Red' : (255, 0, 0),
        'DarkRed' : (128, 0, 0),
        'Green' : (0, 255, 0),
        'Blue' : (0, 0, 255),
        'Yellow' : (255, 255, 0),
        'Orange' : (255, 128, 0),
        'DarkOrange' : (255, 64, 0),
        'Magenta' : (255, 0, 255),
        'KDEBlue' : (64, 137, 210),
        'Grey' : (128, 128, 128),
        'DarkGreen' : (0, 128, 0),
        'DarkSlateBlue' : (72, 61, 139),
        'Brown' : (70, 35, 10),

        'MyBlue' : (36, 72, 206),
        'MyBlueOverview' : (150, 150, 255),
        'MyDarkBlue' : (18, 36, 103),
        'MyGreen' : (70, 164, 60),
        'AnnBlueTitle' : (29, 47, 126),
        'AnnBlue' : (55, 100, 255),
#        'W11AnnBlue' : (0, 68, 204),
#        'W11AnnBlue' : (63, 122, 240),
    }


myColors = {
            'W11ttbar':  855,
            'W11singlet':  854,
            'W11ZLightJets':  401,
            'W11ZbJets':  400,
            'W11WJets':  842,
            'W11Diboson':  920,
            'W11AnnBlue': 856,
            'W11Rare':  630,
            }

class sbottom_masses:
        class m_b_200:
                cross_section8TeV = 18.52
                cross_section13TeV = 64.51
        class m_b_210:
                cross_section8TeV = 14.7
        class m_b_220:
                cross_section8TeV = 11.5
        class m_b_225:
                cross_section8TeV = 9.91
                cross_section13TeV = 36.38
        class m_b_230:
                cross_section8TeV = 9.02 
        class m_b_240:
                cross_section8TeV = 7.16 
        class m_b_250:
                cross_section8TeV = 5.576
                cross_section13TeV = 21.59
        class m_b_260:
                cross_section8TeV = 4.61
        class m_b_270:
                cross_section8TeV = 3.74 
        class m_b_275:
                cross_section8TeV = 3.278
                cross_section13TeV = 13.32
        class m_b_280:
                cross_section8TeV = 3.04 
        class m_b_290:
                cross_section8TeV = 2.49 
        class m_b_300:
                cross_section8TeV = 1.996
                cross_section13TeV = 8.516
        class m_b_310:
                cross_section8TeV = 1.70
        class m_b_320:
                cross_section8TeV = 1.41
        class m_b_325:
                cross_section8TeV = 1.253
                cross_section13TeV = 5.605
        class m_b_330:
                cross_section8TeV = 1.18 
        class m_b_340:
                cross_section8TeV = 0.988
        class m_b_350:
                cross_section = 0.8073
                cross_section13TeV = 3.787
        class m_b_360:
                cross_section8TeV = 0.702
        class m_b_370:
                cross_section8TeV = 0.595
        class m_b_375:
                cross_section8TeV = 0.5314
                cross_section13TeV = 2.808
        class m_b_380:
                cross_section8TeV = 0.507
        class m_b_390:
                cross_section8TeV = 0.432
        class m_b_400:
                cross_section8TeV = 0.3568
                cross_section13TeV = 1.83537
        class m_b_410:
                cross_section8TeV = 0.317
        class m_b_420:
                cross_section8TeV = 0.273
        class m_b_425:
                cross_section8TeV = 0.2438
                cross_section13TeV = 1.312
        class m_b_430:
                cross_section8TeV = 0.235
        class m_b_440:
                cross_section8TeV = 0.203
        class m_b_450:
                cross_section8TeV = 0.1697 
                cross_section13TeV = 0.9483
        class m_b_460:
                cross_section8TeV = 0.153 
        class m_b_470:
                cross_section8TeV = 0.133  
        class m_b_475:
                cross_section8TeV = 0.1193 
                cross_section13TeV = 0.6971
        class m_b_480:
                cross_section8TeV = 0.116  
        class m_b_490:
                cross_section8TeV = 0.101 
        class m_b_500: 
                cross_section8TeV = 0.08558 
                cross_section13TeV = 0.5185
                cross_sectionUncertainty = 0.134
        class m_b_510:
                cross_section8TeV = 0.0774 
        class m_b_520:
                cross_section8TeV = 0.0679
        class m_b_525:
                cross_section8TeV = 0.06186
                cross_section13TeV = 0.3903
                cross_sectionUncertainty = 0.133
        class m_b_530:
                cross_section8TeV = 0.0597
        class m_b_540:
                cross_section8TeV = 0.0525
        class m_b_550:
                cross_section8TeV = 0.04521
                cross_section13TeV = 0.2961
                cross_sectionUncertainty = 0.133
        class m_b_560:
                cross_section8TeV = 0.0410
        class m_b_570:
                cross_section8TeV = 0.0366
        class m_b_575:
                cross_section8TeV = 0.03340
                cross_section13TeV = 0.2261
                cross_sectionUncertainty = 0.133
        class m_b_580:
                cross_section8TeV = 0.0320
        class m_b_590:
                cross_section8TeV = 0.0285
        class m_b_600:  
                cross_section8TeV = 0.02480     
                cross_section13TeV = 0.1746
                cross_sectionUncertainty = 0.132        
        class m_b_610:
                cross_section8TeV = 0.0226              
        class m_b_620:
                cross_section8TeV = 0.0200              
        class m_b_625:  
                cross_section8TeV = 0.01853     
                cross_section13TeV = 0.1364
                cross_sectionUncertainty = 0.128        
        class m_b_630:
                cross_section8TeV = 0.0178              
        class m_b_640:
                cross_section8TeV = 0.0160              
        class m_b_650:  
                cross_section8TeV = 0.01396     
                cross_section13TeV = 0.1070
                cross_sectionUncertainty = 0.129        
        class m_b_660:
                cross_section8TeV = 0.0127              
        class m_b_670:
                cross_section8TeV = 0.0113              
        class m_b_675:  
                cross_section8TeV = 0.01061     
                cross_section13TeV = 0.08449
                cross_sectionUncertainty = 0.131
        class m_b_680:
                cross_section8TeV = 0.0101              
        class m_b_690:
                cross_section8TeV = 0.00907             
        class m_b_700:  
                cross_section8TeV = 0.008114    
                cross_section13TeV = 0.06705
                cross_sectionUncertainty = 0.133
        class m_b_725:          
                cross_section13TeV = 0.0536438
                cross_sectionUncertainty = 0.136
        class m_b_750:          
                cross_section13TeV = 0.0431418
                cross_sectionUncertainty = 0.137
        class m_b_775:          
                cross_section13TeV = 0.0348796
                cross_sectionUncertainty = 0.140
        class m_b_800:          
                cross_section13TeV = 0.0283338
                cross_sectionUncertainty = 0.142
        class m_b_825:          
                cross_section13TeV = 0.0230866
                cross_sectionUncertainty = 0.144
        class m_b_850:          
                cross_section13TeV = 0.0189612
                cross_sectionUncertainty = 0.147
        class m_b_875:          
                cross_section13TeV =    0.015625
                cross_sectionUncertainty = 0.150
        class m_b_900:          
                cross_section13TeV = 0.0128895
                cross_sectionUncertainty = 0.152
        class m_b_950:          
                cross_section13TeV = 0.00883465
                cross_sectionUncertainty = 0.157
        class m_b_1000:         
                cross_section13TeV = 0.00615134
                cross_sectionUncertainty = 0.163
        class m_b_1050:         
                cross_section13TeV = 0.00432256
                cross_sectionUncertainty = 0.168
        class m_b_1100:         
                cross_section13TeV = 0.00307413
                cross_sectionUncertainty = 0.173
        class m_b_1150:         
                cross_section13TeV = 0.00221047
                cross_sectionUncertainty = 0.179
        class m_b_1200:         
                cross_section13TeV = 0.00159844
                cross_sectionUncertainty = 0.185
        class m_b_1250:         
                cross_section13TeV = 0.0011583
                cross_sectionUncertainty = 0.193
        class m_b_1300:         
                cross_section13TeV = 0.000850345
                cross_sectionUncertainty = 0.202
        class m_b_1350:         
                cross_section13TeV = 0.000625155
                cross_sectionUncertainty = 0.213
        class m_b_1400:         
                cross_section13TeV = 0.000461944
                cross_sectionUncertainty = 0.223
        class m_b_1450:         
                cross_section13TeV = 0.000343923
                cross_sectionUncertainty = 0.235
        class m_b_1500:         
                cross_section13TeV = 0.000256248
                cross_sectionUncertainty = 0.244
        class m_b_1550:         
                cross_section13TeV = 0.000190474
                cross_sectionUncertainty = 0.255
        class m_b_1600:         
                cross_section13TeV = 0.000141382
                cross_sectionUncertainty = 0.265
        

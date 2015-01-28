from math import sqrt
import ROOT
from ROOT import TMath
import sys
import copy
from corrections import triggerEffs

class runRanges:
	class RunAB:
		lumi = 5230
		printval = "5.23"
		lumiErr = 0.045*5230
		runCut = "&& runNr <= 196531"
		label = "RunAB"
	class RunC:
		lumi = 6770
		printval = "6.77"
		lumiErr = 0.045*6770
		runCut = "&& (runNr > 196531 || runNr ==1)"
		label = "RunC"
	class Run92:
		lumi = 9200
		printval = "9.2"
		lumiErr = 0.045*9200
		runCut = "&& runNr < 201678 && !(runNr >= 198049 && runNr <= 198522)"
		label = "Run92"
	class Full2012:
		lumi = 19700
		printval = "19.7"
		lumiErr = 0.026*19700
		runCut = "&& runNr < 99999999"
		label = "Full2012"
	class BlockA:
		lumi = 9200
		printval = "9.2"
		lumiErr = 0.045*9200
		runCut = "&& runNr < 99999999"
		label = "BlockA"
	class BlockB:
		lumi = 10200
		printval = "10.2"
		lumiErr = 0.045*9200
		runCut = "&& runNr < 99999999"
		label = "BlockB"
	class All:
		lumi = 12000
		printval = "12.0"
		lumiErr = 0.045*12000
		runCut = "&& runNr < 99999999"
		label = "Full"
	class Run2011:
		lumi = 4980
		printval = "5.0"
		lumiErr = 0.045*4980
		runCut = "&& runNr < 99999999"
		label = "2011"

		
class Region:
	cut = " chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && p4.M() > 20 && deltaR > 0.3 && !(runNr == 195649 && lumiSec == 49 && eventNr == 75858433) && !(runNr == 195749 && lumiSec == 108 && eventNr == 216906941)"
	cutToUse = "weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && !(runNr == 195649 && lumiSec == 49 && eventNr == 75858433) && !(runNr == 195749 && lumiSec == 108 && eventNr == 216906941) )"
	title = "everything"
	latex = "everything"
	labelRegion = "p_{T}^{l} > 20 GeV |#eta^{l}| < 2.4"
	name = "Inclusive"
	labelSubRegion = ""
	dyPrediction = {}
	logY = True
	trigEffs = triggerEffs.inclusive
	
class theCuts:
	class massCuts:
		class default:
			cut = "p4.M() > 20"
			label = "m_{ll} = 20 GeV"
			name = "fullMassRange"
		class edgeMass:
			cut = "p4.M()> 20 && p4.M() < 70"
			label = "20 GeV < m_{ll} < 70 GeV"
			name = "edgeMass"
		class zMass:
			cut = "p4.M()> 81 && p4.M() < 101"
			label = "81 GeV < m_{ll} < 101 GeV"
			name = "zMass"
		class highMass:
			cut = "p4.M() > 120"
			label = "m_{ll} > 120 GeV"
			name = "highMass"
			
	class ptCuts:
		class pt2010:
			cut = "((pt1 > 20 && pt2 > 10)||(pt1 > 10 && pt2 > 20))"
			label = "p_{T} > 20(10) GeV"
			name = "pt2010"
		class pt2020:
			cut = "pt1 > 20 && pt2 > 20"
			label = "p_{T} > 20 GeV"
			name = "pt2020"
		class pt3010:
			cut = "((pt1 > 30 && pt2 > 10)||(pt1 > 10 && pt2 > 30))"
			label = "p_{T} > 30(10) GeV"
			name = "pt3010"
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
			cut = "id1 < 0.05 && id2 < 0.05"
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
		class ht100to300:
			cut = "ht > 100 && ht < 300"
			label = "100 GeV < H_{T} < 100 GeV"
			name = "HT100to300"
			
	class pileUpCuts:
		class lowPU:
			cut = "nVertices < 11"
			label = "N_{Vtx} < 11"
			name = "LowPU"
		class midPU:
			cut = "nVertices >= 11 && nVertices < 16"
			label = "11 #leq N_{Vtx} < 16"
			name = "MidPU"
		class highPU:
			cut = "nVertices >= 16"
			label = "N_{Vtx} #geq 16"
			name = "HighPU"


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
		labelY = "Events / 0.48"	
	class TrailingEta:
		variable = "(pt2>pt1)*eta1+(pt1>pt2)*eta2"
		name = "TrailingEta"
		xMin = -2.4
		xMax = 2.4
		nBins = 10
		labelX = "trailing #eta"
		labelY = "Events / 0.48"	
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
		xMax = 400
		nBins = 40
		labelX = "p_{T}^{leading} [GeV]"
		labelY = "Events / 10 GeV"	
	class TrailingPt:
		variable = "(pt1>pt2)*pt2+(pt2>pt1)*pt1"
		name = "TrailingPt"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "p_{T}^{trailing} [GeV]"
		labelY = "Events / 10 GeV"	
	class Met:
		variable = "met"
		name = "MET"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "E_{T}^{miss} [GeV]"
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
		xMax = 800
		nBins = 20
		labelX = "H_{T} [GeV]"
		labelY = "Events / 40 GeV"	
	class Mll:
		variable = "p4.M()"
		name = "Mll"
		xMin = 20
		xMax = 305
		nBins = 57
		labelX = "m_{ll} [GeV]"
		labelY = "Events / 5 GeV"	
	class Ptll:
		variable = "p4.Pt()"
		name = "Ptll"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "p_{T}^{ll} [GeV]"
		labelY = "Events / 10 GeV"	
	class nJets:
		variable = "nJets"
		name = "NJets"
		xMin = -0.5
		xMax = 10.5
		nBins = 11
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
	class deltaR:
		variable = "deltaR"
		name = "DeltaR"
		xMin = 0
		xMax = 4
		nBins = 20
		labelX = "#Delta R_{ll}"
		labelY = "Events / 0.2"	
	class nVtx:
		variable = "nVertices"
		name = "nVtx"
		xMin = 0
		xMax = 40
		nBins = 40
		labelX = "N_{Vertex}"
		labelY = "Events"	

		

	
	
class Regions:
	class SignalInclusive(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets>=3 && met > 100)) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "Inclusive Signal Region"
		titel = "Inclusive SR"
		latex = "Inclusive Signal Region"
		name = "SignalInclusive"
		logY = False


	class SignalForward(Region):
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

	class SignalBarrel(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets >= 3 && met > 100)) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		labelSubRegion = "Central Signal Region"
		labelRegion = Region.labelRegion.replace("< 2.4","< 1.4")
		titel = "Central SR"
		latex = "Central Signal Region"
		name = "SignalCentral"
		trigEffs = triggerEffs.central
		logY = False

		
	class Control(Region):
		cut = "nJets == 2  && 100 <  met && met < 150 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} = 2 100 GeV < E_{T}^{miss} < 150 GeV"		
		titel = "CR"
		latex = "Control Region"
		name = "Control"
		logY = True
	class ControlForward(Region):
		cut = "nJets == 2  && 100 <  met && met < 150 && 1.4 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} = 2 100 GeV < E_{T}^{miss} < 150 GeV"		
		titel = "CR"
		latex = "Control Region Forward"
		name = "ControlForward"
		logY = True
		trigEffs = triggerEffs.forward
	class ControlCentral(Region):
		cut = "nJets == 2  && 100 <  met && met < 150 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} = 2 100 GeV < E_{T}^{miss} < 150 GeV |#eta| < 1.4"		
		titel = "CR"
		latex = "Control Region Central"
		name = "ControlCentral"
		logY = True
		trigEffs = triggerEffs.central		
			
	class bTagControl(Region):
		cut = "nJets >=2 && met > 50 && nBJets >=1 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} #geq 2 N_{bJets} #geq 1 E_{T}^{miss} > 50 GeV"			
		titel = "High E_{T}^{miss} CR"
		latex = "High \MET\ Control Region"
		name = "bTagControl"
		logY = True
			
	class ttBarDileptonSF(Region):
		cut = "nJets >=2 && met > 40 && (p4.M()<76 || p4.M() > 106) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} #geq 2 E_{T}^{miss} > 40 GeV |m_{ll} - m_{Z}| > 25 GeV"			
		titel = "High E_{T}^{miss} CR"
		latex = "High \MET\ Control Region"
		name = "ttBarDileptonSF"
		logY = True
	class ttBarDileptonOF(Region):
		cut = "nJets >=2 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} #geq 2"			
		titel = "High E_{T}^{miss} CR"
		latex = "High \MET\ Control Region"
		name = "ttBarDileptonOF"
		logY = True


	class InclusiveJets(Region):
		cut = "nJets >= 2   && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} >= 2 "			
		titel = "Inclusive Jets"
		latex = "Inclusive Jets"
		name = "InclusiveJets"
		logY = True
				
	class Zpeak(Region):
		cut = "p4.M() > 60 && p4.M() < 120 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "60 GeV < m_{ll} < 120 GeV"			
		titel = "Drell-Yan Enhanced"
		latex = "Drell-Yan Enhanced"
		name = "ZPeak"
		logY = True
	
	class ZPeakControl(Region):
		cut = "p4.M() > 60 && p4.M() < 120 && met < 50 && nJets >= 2 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "#splitline{60 GeV < m_{ll} < 120 GeV}{N_{jets} >= 2 E_T^{miss} < 50 GeV}"			
		titel = "Drell-Yan Enhanced"
		latex = "Drell-Yan Enhanced"
		name = "ZPeakControl"
		logY = True
	class ZPeakControlCentral(Region):
		cut = "p4.M() > 60 && p4.M() < 120 && met < 50 && nJets >= 2 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "#splitline{60 GeV < m_{ll} < 120 GeV}{N_{jets} >= 2 E_T^{miss} < 50 GeV}"			
		titel = "Drell-Yan Enhanced Central"
		latex = "Drell-Yan Enhanced Central"
		name = "ZPeakControlCentral"
		logY = True
	class ZPeakControlForward(Region):
		cut = "p4.M() > 60 && p4.M() < 120 && met < 50 && nJets >= 2 && 1.4 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "#splitline{60 GeV < m_{ll} < 120 GeV}{N_{jets} >= 2 E_T^{miss} < 50 GeV}"			
		titel = "Drell-Yan Enhanced Forward"
		latex = "Drell-Yan Enhanced Forward"
		name = "ZPeakControlForward"
		logY = True
	
	class DrellYanControl(Region):
		cut = "met < 50 && nJets >= 2 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} >= 2 E_T^{miss} < 50 GeV"			
		titel = "Drell-Yan control region"
		latex = "Drell-Yan control region"
		name = "DrellYanControl"
		logY = True
	class DrellYanControlCentral(Region):
		cut = "met < 50 && nJets >= 2 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} >= 2 E_T^{miss} < 50 GeV"			
		titel = "Drell-Yan control region central"
		latex = "Drell-Yan control region central"
		name = "DrellYanControlCentral"
		logY = True
	class DrellYanControlForward(Region):
		cut = "met < 50 && nJets >= 2 && 1.4 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} >= 2 E_T^{miss} < 50 GeV"			
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


	

def getRegion(name):
	if not name in dir(Regions):
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
	cuts	= "none"
	xaxis   = "none"
	yaxis	= "none"
	tree1 	= "none"
	tree2	= "none"
	nBins	= 0
	firstBin = 0
	lastBin = 0
	binning = []
	yMin 	= 0
	yMax	= 0 
	label = "none"
	label2 = "none"
	label3 = "none"
	filename = "none.pdf"
	log = False
	tree1 = "None"
	tree2 = "None"
	
	def __init__(self,variable,additionalCuts,binning = None, yRange = None,additionalName=None,DoCleanCuts = True):
		self.variable=variable.variable
		self.cuts="weight*(%s)"
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
			self.labelY = binning [3]
			self.binning = binning[4]
		if yRange != None:
			self.yMin = yRange[0]
			self.yMax = yRange[0]
		if additionalName != None:
			self.filename = self.filename%(additionalName+"_%s")
		self.filename = self.filename.replace("_%s","%s.pdf") 
		self.label3 = self.label3.replace("%s","")
	
	
	def clone(self,selection):
		print self.cuts
		tempPlot = Plot(theVariables.Met,[])
		if getMassSelection(selection) != None:
			tempPlot.cuts = "weight*(%s)"%(getMassSelection(selection).cut+"&& %s")
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
	
	def addRegion(self,region):
		self.cuts = self.cuts%(region.cut+" %s")
		self.filename = region.name+"_"+self.filename
		self.label = region.labelRegion
		self.label2 = region.labelSubRegion
		self.regionName = region.name
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
				for cut in metCutUp:
					self.cuts = self.cuts.replace(cut.split(")")[0],"")
				for cut in metCutDown:
					self.cuts = self.cuts.replace(cut,"")
				self.cuts = self.cuts.replace("&&)",")")
				self.cuts = self.cuts.replace("&& &&","&&")
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
						self.cuts = self.cuts.replace(cut,"weight*(((")
					elif "weight" in cut:
						self.cuts = self.cuts.replace(cut,"weight*(")
					elif "(" in cut:
						self.cuts = self.cuts.replace(cut.split("(")[1],"")
					else:
						self.cuts = self.cuts.replace(cut,"")
				for cut in nJetsCutDown:
					if "weight" and "(((" in cut:
						self.cuts = self.cuts.replace(cut,"weight*(((")
					elif "weight" in cut:
						self.cuts = self.cuts.replace(cut,"weight*(")
					elif "(" in cut:
						self.cuts = self.cuts.replace(cut.split("(")[1],"")
					else:
						self.cuts = self.cuts.replace(cut,"")
				for cut in nJetsCutEqual:
					if "weight" and "(((" in cut:
						self.cuts = self.cuts.replace(cut,"weight*(((")
					elif "weight" in cut:
						self.cuts = self.cuts.replace(cut,"weight*(")
					elif "(" in cut:
						self.cuts = self.cuts.replace(cut.split("(")[1],"")
					else:
						self.cuts = self.cuts.replace(cut,"")
						
				self.cuts = self.cuts.replace("&& &&","&&")
				self.cuts = self.cuts.replace("&&&&","&&")			
				self.cuts = self.cuts.replace("( &&","(")			
				self.cuts = self.cuts.replace("(&&","(")	
				
			if self.additionalName == "trailingPt10" or self.additionalName == "leadingPt30Single":
				self.cuts = self.cuts.replace("&& pt1 > 20 && pt2 > 20 &&", "&&") 		
		else:
			print "Cut cleaning deactivated for this plot!"
		
class thePlots:

	metPlot = Plot(theVariables.Met,[])
	metPlotLowMass = Plot(theVariables.Met,[theCuts.massCuts.edgeMass])
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
	metPlot100NoClean = Plot(theVariables.Met,[],binning = [30,100,400,"Events / 10 Gev",[]],additionalName = "MET100Cuts",DoCleanCuts=False)
	
	metPlotLowMass = Plot(theVariables.Met,[theCuts.massCuts.edgeMass])
	metPlotLowPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.lowPU,theCuts.massCuts.edgeMass])
	metPlotMidPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.midPU,theCuts.massCuts.edgeMass])
	metPlotHighPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.highPU,theCuts.massCuts.edgeMass])
	metPlot0Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.noJet,theCuts.massCuts.edgeMass])
	metPlot1Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.OneJet,theCuts.massCuts.edgeMass])
	metPlot2Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.TwoJet,theCuts.massCuts.edgeMass])
	metPlot3Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.ThreeJet,theCuts.massCuts.edgeMass])
	metPlotnoBTags = Plot(theVariables.Met,[theCuts.bTags.noBTags,theCuts.massCuts.edgeMass])
	metPlotwithBTags = Plot(theVariables.Met,[theCuts.bTags.geOneBTags,theCuts.massCuts.edgeMass])
	metPlotCentralBarrel = Plot(theVariables.Met,[theCuts.etaCuts.CentralBarrel,theCuts.massCuts.edgeMass])
	metPlotOuterBarrel = Plot(theVariables.Met,[theCuts.etaCuts.OuterBarrel,theCuts.massCuts.edgeMass])
	metPlotEndcap = Plot(theVariables.Met,[theCuts.etaCuts.Endcap,theCuts.massCuts.edgeMass])
	metPlotlowDR = Plot(theVariables.Met,[theCuts.dRCuts.lowDR,theCuts.massCuts.edgeMass])
	metPlotmidDR = Plot(theVariables.Met,[theCuts.dRCuts.midDR,theCuts.massCuts.edgeMass])
	metPlothighDR = Plot(theVariables.Met,[theCuts.dRCuts.highDR,theCuts.massCuts.edgeMass])
	metPlotType1 = Plot(theVariables.Type1Met,[theCuts.massCuts.edgeMass])
	metPlotCalo = Plot(theVariables.CaloMet,[theCuts.massCuts.edgeMass])
	metPlotTc = Plot(theVariables.TcMet,[theCuts.massCuts.edgeMass])
	mhtPlotLowMass = Plot(theVariables.MHT,[theCuts.massCuts.edgeMass])		
	
	htPlot = Plot(theVariables.HT,[])		
	htPlotLowMass = Plot(theVariables.HT,[theCuts.massCuts.edgeMass])		
	htPlotHighMass = Plot(theVariables.HT,[theCuts.massCuts.highMass])	
	htPlotUntertaintyHighMET = Plot(theVariables.HT,[theCuts.metCuts.met150])	
	htPlotUntertaintyLowMET = Plot(theVariables.HT,[theCuts.metCuts.met100])

	mhtPlot = Plot(theVariables.MHT,[])

	eta1Plot = Plot(theVariables.Eta1,[])		
	tralingEtaPlot = Plot(theVariables.TrailingEta,[])		
	LeadingEtaPlot = Plot(theVariables.LeadingEta,[])		
	eta2Plot = Plot(theVariables.Eta2,[])

	ptElePlot = Plot(theVariables.PtEle,[])		
	ptMuPlot = Plot(theVariables.PtMu,[])
	trailingPtPlot = Plot(theVariables.TrailingPt,[])
	leadingPtPlot = Plot(theVariables.LeadingPt,[])
	trailingPtPlotLowMass = Plot(theVariables.TrailingPt,[theCuts.massCuts.edgeMass])
	leadingPtPlotLowMass = Plot(theVariables.LeadingPt,[theCuts.massCuts.edgeMass])
	trailingPtPlotHighMass = Plot(theVariables.TrailingPt,[theCuts.massCuts.highMass])
	leadingPtPlotHighMass = Plot(theVariables.LeadingPt,[theCuts.massCuts.highMass])

	mllPlot = Plot(theVariables.Mll,[])
	mllPlotLowMass = Plot(theVariables.Mll,[theCuts.massCuts.edgeMass])
	mllPlotHighMass = Plot(theVariables.Mll,[theCuts.massCuts.highMass])
	mllPlotZpeak = Plot(theVariables.Mll,[],binning = [30,60,120,"Events / 2 Gev",[]],additionalName = "ZPeak")

	nJetsPlot = Plot(theVariables.nJets,[])
	nJetsPlotLowMass = Plot(theVariables.nJets,[theCuts.massCuts.edgeMass])
	nJetsPlotHighMass = Plot(theVariables.nJets,[theCuts.massCuts.highMass])

	nBJetsPlot = Plot(theVariables.nBJets,[])
	nBJetsPlotLowMass = Plot(theVariables.nBJets,[theCuts.massCuts.edgeMass])
	nBJetsPlotHighMass = Plot(theVariables.nBJets,[theCuts.massCuts.highMass])

	deltaRPlot = Plot(theVariables.deltaR,[])
	deltaRPlotLowMass = Plot(theVariables.deltaR,[theCuts.massCuts.edgeMass])
	deltaRPlotHighMass = Plot(theVariables.deltaR,[theCuts.massCuts.highMass])

	ptllPlot = Plot(theVariables.Ptll,[])
	ptllPlotLowMass = Plot(theVariables.Ptll,[theCuts.massCuts.edgeMass])
	ptllPlotHighMass = Plot(theVariables.Ptll,[theCuts.massCuts.highMass])

			
	### plots for trigger efficiency measurements
	nJetsPlotTrigger = Plot(theVariables.nJets,[],binning=[11,-0.5,10.5,"Events",[]])
	leadingPtPlotTriggerTrailing10= Plot(theVariables.LeadingPt,[theCuts.ptCuts.pt2010],binning=[9,20,90,"Events / 10 GeV",[]],additionalName = "trailingPt10")
	leadingPtPlotTrigger= Plot(theVariables.LeadingPt,[],binning=[9,20,90,"Events / 10 GeV",[]],additionalName = "trailingPt20")
	trailigPtPlotTrigger= Plot(theVariables.TrailingPt,[],binning=[9,20,90,"Events / 10 GeV",[]],additionalName = "leadingPt20")
	trailigPtPlotTriggerLeading30 = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[9,20,90,"Events / 10 GeV",[]],additionalName = "leadingPt30")
	trailigPtPlotTriggerLeading30Single = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[10,10,110,"Events / 10 GeV",[]],additionalName = "leadingPt30Single")
	mllPlotTrigger = Plot(theVariables.Mll,[],binning=[9,20,290,"Events / 30 GeV",[]])				
	htPlotTrigger = Plot(theVariables.HT,[],binning=[10,0,400,"Events / 40 GeV",[]])				
	metPlotTrigger = Plot(theVariables.Met,[],binning=[10,0,200,"Events / 20 GeV",[]])				
	nVtxPlotTrigger = Plot(theVariables.nVtx,[],binning=[15,0,30,"Events / 2",[]])				
	tralingEtaPlotTrigger = Plot(theVariables.AbsTrailingEta,[],binning=[8,0,2.4,"Events / 0.3",[]])				
			
	### plots for rmue measurements
	nJetsPlotRMuE = Plot(theVariables.nJets,[],binning=[9,-0.5,8.5,"Events",[]])
	nBJetsPlotRMuE = Plot(theVariables.nBJets,[],binning=[7,-0.5,6.5,"Events",[]])
	leadingPtPlotRMuE= Plot(theVariables.LeadingPt,[],binning=[16,20,100,"Events / 5 GeV",[]],additionalName = "trailingPt20")
	trailigPtPlotRMuE= Plot(theVariables.TrailingPt,[],binning=[16,20,100,"Events / 5 GeV",[]],additionalName = "leadingPt20")
	trailigPtPlotRMuELeading30 = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[16,20,100,"Events / 5 GeV",[]],additionalName = "leadingPt30")
	mllPlotRMuE = Plot(theVariables.Mll,[],binning=[-1,20,200,"Events / 10 GeV",range(20,60,10)+range(60,120,10)+range(120,250,25)])				
	htPlotRMuE = Plot(theVariables.HT,[],binning=[-1,0,400,"Events / 40 GeV",range(0,300,50)+range(300,800,100)])				
	metPlotRMuE = Plot(theVariables.Met,[],binning=[-1,0,250,"Events / 20 GeV",range(0,100,10)+range(100,150,25)+range(150,250,50)])				
	nVtxPlotRMuE = Plot(theVariables.nVtx,[],binning=[40,0,40,"Events / 1",[]])				
	tralingEtaPlotRMuE = Plot(theVariables.AbsTrailingEta,[],binning=[-1,0,2.55,"Events / 0.3",[i*0.14 for i in range(0,10)]+[i*0.2+1.4 for i in range(0,6)]])				
	deltaRPlotRMuE = Plot(theVariables.deltaR,[],binning=[-1,0,5.5,"Events / 0.3",[0.2*i for i in range(10)]+[2+0.5*i for i in range(7)]])				
			
								
	mllPlotRMuESignal = Plot(theVariables.Mll,[],binning=[28,20,300,"Events / 10 GeV",[]])
	
					
	mllPlotROutIn = Plot(theVariables.Mll,[],binning=[1000,0,1000,"Events / 1 GeV",[]])				
	metPlotROutIn = Plot(theVariables.Met,[],binning=[-1,0,100,"Events / 1 GeV",[0,10,20,30,40,50,65,80,100]])				
	nJetsPlotROutIn = Plot(theVariables.nJets,[],binning=[6,-0.5,5.5,"Events / 1 GeV",[]])				

	
class Signals:
	
	class SimplifiedModel_mB_225_mn2_150_mn1_80:
		subprocesses = ["SUSY_Simplified_Model_Madgraph_FastSim_T6bblledge_225_150_80_8TeV"]
		label 		 = "m_{#tilde{b}} = 225 GeV m_{#tilde{#chi_{0}^{2}}} = 150 GeV"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed-7
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None 	
	class SimplifiedModel_mB_350_mn2_275_mn1_205:
		subprocesses = ["SUSY_Simplified_Model_Madgraph_FastSim_T6bblledge_350_275_205_8TeV"]
		label 		 = "m_{#tilde{b}} = 350 GeV m_{#tilde{#chi_{0}^{2}}} = 275 GeV"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None 
	class SimplifiedModel_mB_400_mn2_150_mn1_80:
		subprocesses = ["SUSY_Simplified_Model_Madgraph_FastSim_T6bblledge_400_150_80_8TeV"]
		label 		 = "m_{#tilde{b}} = 400 GeV m_{#tilde{#chi_{0}^{2}}} = 150 GeV"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+2
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None 			
			
	class SimplifiedModel_mB_350_mn2_250_mn1_200:
		subprocesses = ["SUSY_SimplifiedModel_BR10_mb_350_mn2_250_mn1_200_Summer12_FullSim"]
		label 		 = "Signal"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None 
	class SimplifiedModel_mB_500_mn2_400_mn1_200:
		subprocesses = ["SUSY_SimplifiedModel_BR10_mb_500_mn2_400_mn1_200_Summer12_FullSim"]
		label 		 = "Signal"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None
	class SimplifiedModel_mB_400_mn2_400_mn1_160:
		subprocesses = ["SUSY_SimplifiedModel_BR50_mb_400_mn2_160_mn1_90_Summer12_FastSim"]
		label 		 = "Signal"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None				
	class SUSY2:
		subprocesses = ["SUSY_CMSSM_4500_188_Summer12"]
		label 		 = "CMSSM 4500/188"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+1
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None
	class SUSY3:
		subprocesses = ["SUSY_CMSSM_4580_202_Summer12"]
		label 		 = "CMSSM 4580/202"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+2
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None
	class SUSY4:
		subprocesses = ["SUSY_CMSSM_4640_202_Summer12"]
		label 		 = "CMSSM 4640/202"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+3
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None
	class SUSY5:
		subprocesses = ["SUSY_CMSSM_4700_216_Summer12"]
		label 		 = "CMSSM 4700/216"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+4
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None
		
class Backgrounds:
	
	class TTJets:
		subprocesses = ["TTJets_madgraph_Summer12"]
		label = "Madgraph t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class TTJets_SpinCorrelations:
		subprocesses = ["TTJets_MGDecays_madgraph_Summer12","TTJets_MGDecays_SemiLept_madgraph_Summer12","TTJets_MGDecays_FullHad_madgraph_Summer12"]
		label = "Madgraph t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class TT:
		subprocesses = ["TT_Powheg_Summer12_v2"] 
		label = "t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
		#~ scaleFac     = 0.71
	class TT_Dileptonic:
		subprocesses = ["TT_Dileptonic_Powheg_Summer12_v1"] 
		label = "Powheg t#bar{t} Dileptonic"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.07
		scaleFac     = 1.0
		#~ scaleFac     = 0.71
		additionalSelection = None
	class TT_MCatNLO:
		subprocesses = ["TT_MCatNLO_Summer12_v1"] 
		label = "MCatNLO t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
		#~ scaleFac     = 0.71
	class Diboson:
		subprocesses = ["ZZJetsTo2L2Q_madgraph_Summer12","ZZJetsTo2L2Nu_madgraph_Summer12","ZZJetsTo4L_madgraph_Summer12","WZJetsTo3LNu_madgraph_Summer12","WZJetsTo2L2Q_madgraph_Summer12","WWJetsTo2L2Nu_madgraph_Summer12"]
		label = "WW,WZ,ZZ"
		fillcolor = 920
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class Rare:
		subprocesses = ["WWWJets_madgraph_Summer12","WWGJets_madgraph_Summer12","WWZNoGstarJets_madgraph_Summer12","TTGJets_madgraph_Summer12","WZZNoGstar_madgraph_Summer12","TTWJets_madgraph_Summer12","TTZJets_madgraph_Summer12","TTWWJets_madgraph_Summer12"]
		label = "Other SM"
		fillcolor = 630
		linecolor = ROOT.kBlack
		uncertainty = 0.5
		scaleFac     = 1.	
		additionalSelection = None	
	class DrellYan:
		subprocesses = ["AStar_madgraph_Summer12","ZJets_madgraph_Summer12"]
		label = "DY+jets (e^{+}e^{-},#mu^{+}#mu^{-})"
		fillcolor = 401
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
	class DrellYanTauTau:
		subprocesses = ["AStar_madgraph_Summer12","ZJets_madgraph_Summer12"]
		label = "DY+jets (#tau#tau)"
		fillcolor = ROOT.kOrange
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = "(abs(motherPdgId1) == 15 && abs(motherPdgId2) == 15)"
	class SingleTop:
		subprocesses = ["TBar_tWChannel_Powheg_Summer12","TBar_tChannel_Powheg_Summer12","TBar_sChannel_Powheg_Summer12","T_tWChannel_Powheg_Summer12","T_tChannel_Powheg_Summer12","T_sChannel_Powheg_Summer12"]
		label = "Single t"
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None
class Backgrounds2011:
	
	class TTJets:
		subprocesses = ["TTJets_madgraph60M_Fall11"]
		label = "Madgraph t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.15
		scaleFac     = 1.0
		additionalSelection = None
	class Diboson:
		subprocesses = ["WWJets_madgraph_Fall11","WZJets_madgraph_Fall11","ZZJets_madgraph_Fall11"]
		label = "WW,WZ,ZZ"
		fillcolor = 920
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class DrellYan:
		subprocesses = ["AstarJets_madgraph_Summer11","ZJets_madgraph_Fall11"]
		label = "Z+jets"
		fillcolor = 401
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class SingleTop:
		subprocesses = ["Tbar_s_powheg_Fall11","Tbar_t_powheg_Fall11","Tbar_tWDR_powheg_Fall11","T_t_powheg_Fall11","T_s_powheg_Fall11","T_tWDR_powheg_Fall11"]
		label = "t/#bar{t}+jets"
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None

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


	

	

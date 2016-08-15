from math import sqrt
import ROOT
from ROOT import TMath
import sys
import copy
from corrections import triggerEffs

class runRanges:
	class Full2012:
		lumi = 19518
		printval = "19.5"
		lumiErr = 0.026*19518
		runCut = "&& runNr < 99999999"
		label = "Full2012"
		
	class RunIITest:
		lumi = 10000
		printval = "x"
		lumiErr = 0.045*10000
		runCut = "&& runNr < 99999999"
		label = "RunIITest"
	class Run2015_25ns:
		lumi = 2260
		printval = "2.3"
		lumiErr = 0.045*2260
		runCut = "&& ( (runNr > 254230 && runNr < 254833) || runNr > 254852 || runNr ==1)"
		#~ runCut = "&& runNr < 99999999"
		label = "Run2015_25ns"
	class Run2015_50ns:
		lumi = 71.52
		printval = "0.07"
		lumiErr = 0.045*71.52
		runCut = "&& (  runNr < 251884 || runNr == 254833 || runNr ==1) "
		label = "Run2015_50ns"

		
class Region:
	cut = " chargeProduct < 0 && pt1 > 20 && pt2 > 20  && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && deltaR > 0.3 && p4.M() > 20"
	title = "Inclusive dilepton selection"
	latex = "Inclusive dilepton selection"
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
		class looseZ:
			cut = "p4.M()> 70 && p4.M() < 110"
			label = "70 GeV < m_{ll} < 110 GeV"
			name = "looseZ"
		class highMass:
			cut = "p4.M() > 120"
			label = "m_{ll} > 120 GeV"
			name = "highMass"
		class belowZ:
			cut = "p4.M() > 70 && p4.M() < 81"
			label = "70 GeV < m_{ll} < 81 GeV"
			name = "belowZ"
		class aboveZ:
			cut = "p4.M() > 101 && p4.M() < 120"
			label = "101 GeV < m_{ll} < 120 GeV"
			name = "aboveZ"
			
	class ptCuts:
		class pt2010:
			cut = "((pt1 > 20 && pt2 > 10)||(pt1 > 10 && pt2 > 20))"
			label = "p_{T} > 20(10) GeV"
			name = "pt2010"
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
	class GenMet:
		variable = "genMet"
		name = "GenMET"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "gen E_{T}^{miss} [GeV]"
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
		xMax = 300
		nBins = 28
		labelX = "m_{ll} [GeV]"
		labelY = "Events / 10 GeV"		
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
	class leadingJetPt:
		variable = "jet1.Pt()"
		name = "leadingJetPt"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "leading p_{T}^{jet} [GeV]"
		labelY = "Events / 10 GeV"	
	class subleadingJetPt:
		variable = "jet2.Pt()"
		name = "subleadingJetPt"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "subleading p_{T}^{jet} [GeV]"
		labelY = "Events / 10 GeV"	

		

	
	
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

	class SignalCentral(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets >= 3 && met > 100)) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		labelSubRegion = "Central Signal Region"
		labelRegion = Region.labelRegion.replace("< 2.4","< 1.4")
		titel = "Central SR"
		latex = "Central Signal Region"
		name = "SignalCentral"
		trigEffs = triggerEffs.central
		logY = False

		
	class Control(Region):
		cut = "nJets == 2  && 100 < met && met < 150 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "Control Region"		
		titel = "CR"
		latex = "Control Region"
		name = "Control"
		logY = True
	class ControlForward(Region):
		cut = "nJets == 2  && 100 < met && met < 150 && 1.4 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "Control Region Forward"		
		titel = "CR"
		latex = "Control Region Forward"
		name = "ControlForward"
		logY = True
		trigEffs = triggerEffs.forward
	class ControlCentral(Region):
		cut = "nJets == 2  && 100 < met && met < 150 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "Control Region Central"		
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


	class Inclusive(Region):
		cut = "(%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = ""			
		titel = "Inclusive"
		latex = "Inclusive"
		name = "Inclusive"
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
		cut = "nJets >= 2 && met < 50 &&(%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "Drell-Yan control region"			
		titel = "Drell-Yan control region"
		latex = "Drell-Yan control region"
		name = "DrellYanControl"
		logY = True
	class DrellYanControlCentral(Region):
		cut = "nJets >= 2 && met < 50 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "Drell-Yan control region"			
		titel = "Drell-Yan control region central"
		latex = "Drell-Yan control region central"
		name = "DrellYanControlCentral"
		logY = True
	class DrellYanControlForward(Region):
		cut = "nJets >= 2 && met < 50 && 1.4 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
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
		self.cuts="genWeight*weight*(%s)"
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
			if self.variable == "met" or self.variable == "genMet" or self.variable == "mht":
				cuts = self.cuts.split("&&")
				metCutUp = []
				metCutDown = [] 
				for cut in cuts:
					if "%s >"%self.variable in cut:
						metCutUp.append(cut)
					elif "%s <"%self.variable in cut:
						metCutDown.append(cut)
					elif "< %s"%self.variable in cut:
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
			if (self.additionalName == "trailingPt10" or self.additionalName == "leadingPt30Single") and "pt" in self.variable:
				self.cuts = self.cuts.replace("&& pt1 > 20 && pt2 > 20  &&", "&&") 		
		else:
			print "Cut cleaning deactivated for this plot!"
		
class thePlots:

	metPlot = Plot(theVariables.Met,[])
	genMetPlot = Plot(theVariables.GenMet,[])
	metPlotLowMass = Plot(theVariables.Met,[theCuts.massCuts.edgeMass])
	metPlotZMass = Plot(theVariables.Met,[theCuts.massCuts.zMass])
	metPlotHighMass = Plot(theVariables.Met,[theCuts.massCuts.highMass])
	metPlotnoBTags = Plot(theVariables.Met,[theCuts.bTags.noBTags])
	metPlotwithBTags = Plot(theVariables.Met,[theCuts.bTags.geOneBTags])
	metPlot100 = Plot(theVariables.Met,[],binning = [30,100,400,"Events / 10 Gev",[]],additionalName = "MET100")
	metPlot100 = Plot(theVariables.Met,[],binning = [30,100,400,"Events / 10 Gev",[]],additionalName = "MET100")
	metPlot100NoClean = Plot(theVariables.Met,[],binning = [30,100,400,"Events / 10 Gev",[]],additionalName = "MET100Cuts",DoCleanCuts=False)
	
	
	metPlotNoClean = Plot(theVariables.Met,[],binning = [15,0,150,"Events / 10 Gev",[]],additionalName = "NoClean",DoCleanCuts=False)
	
	metPlotLowMass = Plot(theVariables.Met,[theCuts.massCuts.edgeMass])
	metPlotOnZ = Plot(theVariables.Met,[theCuts.massCuts.zMass])
	metPlotnoBTags = Plot(theVariables.Met,[theCuts.bTags.noBTags,theCuts.massCuts.edgeMass])
	metPlotwithBTags = Plot(theVariables.Met,[theCuts.bTags.geOneBTags,theCuts.massCuts.edgeMass])
	
	htPlot = Plot(theVariables.HT,[])		
	htPlotLowMass = Plot(theVariables.HT,[theCuts.massCuts.edgeMass])		
	htPlotHighMass = Plot(theVariables.HT,[theCuts.massCuts.highMass])	

	mhtPlot = Plot(theVariables.MHT,[])
	
	tralingEtaPlot = Plot(theVariables.TrailingEta,[])		
	LeadingEtaPlot = Plot(theVariables.LeadingEta,[])

	trailingPtPlot = Plot(theVariables.TrailingPt,[])
	trailingPtPlot100 = Plot(theVariables.TrailingPt,[],binning = [16,20,100,"Events / 5 Gev",[]],additionalName = "range100")
	leadingPtPlot = Plot(theVariables.LeadingPt,[])
	trailingPtPlotLowMass = Plot(theVariables.TrailingPt,[theCuts.massCuts.edgeMass])
	leadingPtPlotLowMass = Plot(theVariables.LeadingPt,[theCuts.massCuts.edgeMass])
	trailingPtPlotHighMass = Plot(theVariables.TrailingPt,[theCuts.massCuts.highMass])
	leadingPtPlotHighMass = Plot(theVariables.LeadingPt,[theCuts.massCuts.highMass])

	mllPlot = Plot(theVariables.Mll,[])
	mllPlotGeOneBTags = Plot(theVariables.Mll,[theCuts.bTags.geOneBTags])
	mllPlotNoBTags = Plot(theVariables.Mll,[theCuts.bTags.noBTags])
	mllPlotGeTwoBTags = Plot(theVariables.Mll,[theCuts.bTags.geTwoBTags])
	mllPlotLowMass = Plot(theVariables.Mll,[theCuts.massCuts.edgeMass])
	mllPlotHighMass = Plot(theVariables.Mll,[theCuts.massCuts.highMass])
	mllPlotOnZ = Plot(theVariables.Mll,[theCuts.massCuts.zMass])
	mllPlotZpeak = Plot(theVariables.Mll,[],binning = [30,60,120,"Events / 2 Gev",[]],additionalName = "ZPeak")

	nJetsPlot = Plot(theVariables.nJets,[])
	leadingJetPtPlot = Plot(theVariables.leadingJetPt,[])
	subleadingJetPtPlot = Plot(theVariables.subleadingJetPt,[])
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

	nVtxPlot = Plot(theVariables.nVtx,[],binning=[40,0,40,"Events",[]])				

			
	### plots for trigger efficiency measurements
	nJetsPlotTriggerMC = Plot(theVariables.nJets,[],binning=[11,-0.5,10.5,"Events",[]])
	nBJetsPlotTriggerMC = Plot(theVariables.nBJets,[],binning=[6,-0.5,5.5,"Events",[]])
	leadingPtPlotTriggerTrailing10MC= Plot(theVariables.LeadingPt,[],binning=[9,20,90,"Events / 10 GeV",[]],additionalName = "trailingPt10")
	leadingPtPlotTriggerMC= Plot(theVariables.LeadingPt,[],binning=[24,0,120,"Events / 5 GeV",[]])
	trailingPtPlotTriggerMC= Plot(theVariables.TrailingPt,[],binning=[24,0,120,"Events / 5 GeV",[]])
	trailingPtPlotTriggerLeading30MC = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[9,20,90,"Events / 10 GeV",[]],additionalName = "leadingPt30")
	trailingPtPlotTriggerLeading30SingleMC = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[10,10,110,"Events / 10 GeV",[]],additionalName = "leadingPt30Single")
	mllPlotTriggerMC = Plot(theVariables.Mll,[],binning=[28,20,300,"Events / 10 GeV",[]])							
	htPlotTriggerMC = Plot(theVariables.HT,[],binning=[20,200,1000,"Events / 40 GeV",[]])				
	metPlotTriggerMC = Plot(theVariables.Met,[],binning=[10,0,200,"Events / 20 GeV",[]])				
	nVtxPlotTriggerMC = Plot(theVariables.nVtx,[],binning=[15,0,30,"Events / 2",[]])				
	tralingEtaPlotTriggerMC = Plot(theVariables.AbsTrailingEta,[],binning=[8,0,2.4,"Events / 0.3",[]])				

	nJetsPlotTrigger = Plot(theVariables.nJets,[],binning=[6,-0.5,11.5,"Events",[]])
	nBJetsPlotTrigger = Plot(theVariables.nBJets,[],binning=[6,-0.5,5.5,"Events",[]])
	leadingPtPlotTriggerTrailing10= Plot(theVariables.LeadingPt,[],binning=[9,20,90,"Events / 10 GeV",[]],additionalName = "trailingPt10")
	leadingPtPlotTrigger= Plot(theVariables.LeadingPt,[],binning=[5,20,120,"Events / 5 GeV",[]])
	trailingPtPlotTrigger= Plot(theVariables.TrailingPt,[],binning=[5,20,120,"Events / 5 GeV",[]])
	trailingPtPlotTriggerLeading30 = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[40,0,100,"Events / 2.5 GeV",[]],additionalName = "leadingPt30")
	mllPlotTrigger = Plot(theVariables.Mll,[],binning=[4,20,300,"Events / 40 GeV",[]])							
	mllPlotTriggerLeading30Single = Plot(theVariables.Mll,[theCuts.ptCuts.leadingPt30],binning=[7,20,300,"Events / 40 GeV",[]],additionalName = "leadingPt30Single")							
	htPlotTrigger = Plot(theVariables.HT,[],binning=[10,200,1000,"Events / 40 GeV",[]])				
	metPlotTrigger = Plot(theVariables.Met,[],binning=[4,0,200,"Events / 20 GeV",[]])				
	nVtxPlotTrigger = Plot(theVariables.nVtx,[],binning=[8,0,32,"Events / 2",[]])				
	tralingEtaPlotTrigger = Plot(theVariables.AbsTrailingEta,[],binning=[6,0,2.4,"Events / 0.3",[]])

			
	### plots for isolation efficiency measurements
	leadingPtPlotIso= Plot(theVariables.LeadingPt,[],binning=[24,0,120,"Events / 5 GeV",[]])
	trailingPtPlotIso= Plot(theVariables.TrailingPt,[],binning=[24,0,120,"Events / 5 GeV",[]])
	mllPlotIso = Plot(theVariables.Mll,[],binning=[28,20,300,"Events / 10 GeV",[]])							
					
			
	### plots for rmue measurements
	nJetsPlotRMuE = Plot(theVariables.nJets,[],binning=[9,-0.5,8.5,"Events",[]])
	nBJetsPlotRMuE = Plot(theVariables.nBJets,[],binning=[7,-0.5,6.5,"Events",[]])
	leadingPtPlotRMuE= Plot(theVariables.LeadingPt,[],binning=[16,20,100,"Events / 5 GeV",[]])
	trailingPtPlotRMuE= Plot(theVariables.TrailingPt,[],binning=[18,10,100,"Events / 5 GeV",[]])
	trailingPtPlotRMuELeading30 = Plot(theVariables.TrailingPt,[theCuts.ptCuts.leadingPt30],binning=[16,20,100,"Events / 5 GeV",[]],additionalName = "leadingPt30")
	mllPlotRMuE = Plot(theVariables.Mll,[],binning=[-1,20,200,"Events / 10 GeV",range(20,60,10)+range(60,120,10)+range(120,250,25)])													
	htPlotRMuE = Plot(theVariables.HT,[],binning=[-1,0,400,"Events / 40 GeV",range(0,300,50)+range(300,800,100)])				
	metPlotRMuE = Plot(theVariables.Met,[],binning=[-1,0,250,"Events / 20 GeV",range(0,100,10)+range(100,150,25)+range(150,250,50)])				
	nVtxPlotRMuE = Plot(theVariables.nVtx,[],binning=[40,0,40,"Events / 1",[]])				
	tralingEtaPlotRMuE = Plot(theVariables.AbsTrailingEta,[],binning=[-1,0,2.55,"Events / 0.3",[i*0.14 for i in range(0,10)]+[i*0.2+1.4 for i in range(0,6)]])				
	deltaRPlotRMuE = Plot(theVariables.deltaR,[],binning=[-1,0,5.5,"Events / 0.3",[0.2*i for i in range(10)]+[2+0.5*i for i in range(7)]])				
			
								
	mllPlotRMuESignal = Plot(theVariables.Mll,[],binning=[28,20,300,"Events / 10 GeV",[]])
	
					
	mllPlotROutIn = Plot(theVariables.Mll,[],binning=[1000,0,1000,"Events / 1 GeV",[]])				
	metPlotROutIn = Plot(theVariables.Met,[],binning=[-1,0,100,"Events / 1 GeV",[0,10,20,30,40,50,65,80,100]])				
	nJetsPlotROutIn = Plot(theVariables.nJets,[],binning=[5,-0.5,4.5,"Events / 1 GeV",[]])				

	nVtxPlotWeights = Plot(theVariables.nVtx,[],binning=[60,0,60,"Events / 1",[]])				

class Signals:
	
	class T6bbllslepton_msbottom_550_mneutralino_175:
		subprocesses = ["T6bbllslepton_msbottom_550_mneutralino_175"]
		label 		 = "m_{#tilde{b}} = 550 GeV m_{#tilde{#chi_{0}^{2}}} = 175 GeV"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed-7
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None 	
	
	class T6bbllslepton_msbottom_600_mneutralino_250:
		subprocesses = ["T6bbllslepton_msbottom_600_mneutralino_250"]
		label 		 = "m_{#tilde{b}} = 600 GeV m_{#tilde{#chi_{0}^{2}}} = 250 GeV"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed-5
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None 	
	
		
class Backgrounds:
	
	class TTJets_Madgraph:
		subprocesses = ["TTJets_Dilepton_Madgraph_MLM_Spring15_25ns_v1"]
		label = "Madgraph t#bar{t} + jets"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class TT_aMCatNLO:
		subprocesses = ["TT_aMCatNLO_FXFX_Spring15_25ns"]
		label = "aMC@NLO t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class TTJets_aMCatNLO:
		subprocesses = ["TTJets_aMCatNLO_FXFX_Spring15_25ns"]
		label = "aMC@NLO t#bar{t} +jets"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class TT_Powheg:
		subprocesses = ["TT_Dilepton_Powheg_Spring15_25ns"]
		label = "Powheg t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None

	class DrellYan:
		subprocesses = ["ZJets_aMCatNLO_Spring15_25ns","AStar_aMCatNLO_Spring15_25ns"]
		label = "DY+jets"
		fillcolor = 401
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
	class DrellYanLO:
		subprocesses = ["ZJets_Madgraph_Spring15_25ns","AStar_Madgraph_Spring15_25ns"]
		label = "DY+jets"
		fillcolor = 401
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
	class WJets:
		subprocesses = ["WJetsToLNu_aMCatNLO_Spring15_25ns"]
		label = "W+jets"
		fillcolor = 401
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class DrellYanTauTau:
		subprocesses = ["ZJets_aMCatNLO_Spring15_25ns","AStar_aMCatNLO_Spring15_25ns"]
		label = "DY+jets (#tau#tau)"
		fillcolor = ROOT.kOrange
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = "(abs(motherPdgId1) == 15 && abs(motherPdgId2) == 15)"
	class SingleTop:
		subprocesses = ["ST_sChannel_4f_aMCatNLO_Spring15_25ns","ST_antitop_tChannel_4f_Powheg_Spring15_25ns","ST_top_tChannel_4f_Powheg_Spring15_25ns","ST_antitop_tWChannel_5f_Powheg_Spring15_25ns","ST_top_tWChannel_5f_Powheg_Spring15_25ns"]
		label = "Single t"
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None
		
	class Rare:
		subprocesses = ["TTZToLLNuNu_aMCatNLO_FXFX_Spring15_25ns","TTZToQQ_aMCatNLO_FXFX_Spring15_25ns","TTWToLNu_aMCatNLO_FXFX_Spring15_25ns","TTG_aMCatNLO_FXFX_Spring15_25ns","WZZ_aMCatNLO_FXFX_Spring15_25ns","WWZ_aMCatNLO_FXFX_Spring15_25ns","ZZZ_aMCatNLO_FXFX_Spring15_25ns"]
		label = "Other SM"
		fillcolor = 630
		linecolor = ROOT.kBlack
		uncertainty = 0.5
		scaleFac     = 1.	
		additionalSelection = None			

	class Diboson:
		subprocesses = ["WWTo2L2Nu_Powheg_Spring15_25ns","WWToLNuQQ_Powheg_Spring15_25ns","WZTo1L1Nu2Q_aMCatNLO_Spring15_25ns","WZTo1L3Nu_aMCatNLO_Spring15_25ns","WZTo3LNu_Powheg_Spring15_25ns","WZTo2L2Q_aMCatNLO_Spring15_25ns","ZZTo4Q_aMCatNLO_Spring15_25ns","ZZTo4L_Powheg_Spring15_25ns","ZZTo2Q2Nu_aMCatNLO_Spring15_25ns","ZZTo2L2Q_aMCatNLO_Spring15_25ns"]
		label = "WW,WZ,ZZ"
		fillcolor = 920
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
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
	class m_b_510:
		cross_section8TeV = 0.0774 
	class m_b_520:
		cross_section8TeV = 0.0679
	class m_b_525:
		cross_section8TeV = 0.06186
		cross_section13TeV = 0.3903
	class m_b_530:
		cross_section8TeV = 0.0597
	class m_b_540:
		cross_section8TeV = 0.0525
	class m_b_550:
		cross_section8TeV = 0.04521
		cross_section13TeV = 0.2961
	class m_b_560:
		cross_section8TeV = 0.0410
	class m_b_570:
		cross_section8TeV = 0.0366
	class m_b_575:
		cross_section8TeV = 0.03340
		cross_section13TeV = 0.2261
	class m_b_580:
		cross_section8TeV = 0.0320
	class m_b_590:
		cross_section8TeV = 0.0285
	class m_b_600:	
		cross_section8TeV = 0.02480	
		cross_section13TeV = 0.1746	
	class m_b_610:
		cross_section8TeV = 0.0226		
	class m_b_620:
		cross_section8TeV = 0.0200		
	class m_b_625:	
		cross_section8TeV = 0.01853	
		cross_section13TeV = 0.1364	
	class m_b_630:
		cross_section8TeV = 0.0178		
	class m_b_640:
		cross_section8TeV = 0.0160		
	class m_b_650:	
		cross_section8TeV = 0.01396	
		cross_section13TeV = 0.1070	
	class m_b_660:
		cross_section8TeV = 0.0127		
	class m_b_670:
		cross_section8TeV = 0.0113		
	class m_b_675:	
		cross_section8TeV = 0.01061	
		cross_section13TeV = 0.08449	
	class m_b_680:
		cross_section8TeV = 0.0101		
	class m_b_690:
		cross_section8TeV = 0.00907		
	class m_b_700:	
		cross_section8TeV = 0.008114	
		cross_section13TeV = 0.06705
	class m_b_725:		
		cross_section13TeV = 0.0536438
	class m_b_750:		
		cross_section13TeV = 0.0431418
	class m_b_775:		
		cross_section13TeV = 0.0348796
	class m_b_800:		
		cross_section13TeV = 0.0283338
	class m_b_825:		
		cross_section13TeV = 0.0230866
	class m_b_850:		
		cross_section13TeV = 0.0189612
	class m_b_875:		
		cross_section13TeV =  	0.015625
	class m_b_900:		
		cross_section13TeV = 0.0128895
	class m_b_950:		
		cross_section13TeV = 0.00883465
	

	

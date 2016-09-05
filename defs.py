from math import sqrt
import ROOT
from ROOT import TMath
import sys
import copy
from corrections import triggerEffs


### runRanges contains the data runs that can be used
### the tools get the lumi to normalize the MC and the runNr cut for data 
### and the corresponding labels from here
class runRanges:
	class Run2015_25ns:
		lumi = 2260
		printval = "2.3"
		lumiErr = 0.045*2260
		runCut = "&& ( (runNr > 254230 && runNr < 254833) || runNr > 254852 || runNr ==1)"
		label = "Run2015_25ns"
	class Run2015_50ns:
		lumi = 71.52
		printval = "0.07"
		lumiErr = 0.045*71.52
		runCut = "&& (  runNr < 251884 || runNr == 254833 || runNr ==1) "
		label = "Run2015_50ns"

### defaults for the regions to be plotted. In basically every case this is overwritten by a certain region in Regions		
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


### Cuts that can be used and combined	
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
		class pt2020:
			cut = "pt1 > 20 && pt2 > 20"
			label = "p_{T} > 20 GeV"
			name = "pt2020"
		class pt2520:
			cut = "((pt1 > 25 && pt2 > 20)||(pt1 > 20 && pt2 > 25))"
			label = "p_{T} > 25(20) GeV"
			name = "pt2520"

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
		class geOneBTags:
			cut = "nBJets >= 1"
			label = "nBJets #geq 1"
			name  = "geOneBTags"
		class geTwoBTags:
			cut = "nBJets >= 2"
			label = "nBJets #geq 2"
			name  = "geTwoBTags"
			
	class htCuts:
		class ht100:
			cut = "ht > 100"
			label = "H_{T} > 100 GeV"
			name = "HT100"
		class ht300:
			cut = "ht > 300"
			label = "H_{T} > 300 GeV"
			name = "HT300"


class theVariables:
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

	
### Signal and control region definitions that can be used via the option -s in most tools	
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

	class SignalCentral(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets >= 3 && met > 100)) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		labelSubRegion = "Central Signal Region"
		labelRegion = Region.labelRegion.replace("< 2.4","< 1.4")
		titel = "Central SR"
		latex = "Central Signal Region"
		name = "SignalCentral"
		trigEffs = triggerEffs.central
		logY = False

### for the direct measurement of R_SF/OF		
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

### Basic selections
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
		
### for r_Mu/E	
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

### for r_Out/In	
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


	
### Routine to fetch a signal/control region, has to be defined in Regions
def getRegion(name):
	if not name in dir(Regions) and not name == "Region":
		print "unknown region '%s, exiting'"%name
		sys.exit()
	elif name == "Region":
		return Region
	else:
		return copy.copy(getattr(Regions, name))

### Routine to fetch a dilepton mass selection, has to be defined in theCuts.massCuts	
def getMassSelection(name):
	if not name in dir(theCuts.massCuts):
		print "unknown selection '%s, using existing selection'"%name
		return None
	else:
		return copy.copy(getattr(theCuts.massCuts, name))

### Routine to fetch a certain plot, has to be defined in thePlots	
def getPlot(name):
	if not name in dir(thePlots):
		print "unknown plot '%s, exiting'"%name
		sys.exit()
	else:
		return copy.copy(getattr(thePlots, name))

### Routine to fetch a certain runRange, has to be defined in runRanges	
def getRunRange(name):
	if not name in dir(runRanges):
		print "unknown run range '%s, exiting'"%name
		sys.exit()
	else:
		return copy.copy(getattr(runRanges, name))
	
	
### Function that holds all relevant information to make a plot
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
		
		### If true: remove cuts on the variable that is to be plotted
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
			
	### Remove the cuts on the variable that is plotted from the cut string and clean the cut string of anything that might make it fail			
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


### Predefined plots that are used in the tools or can be used via option -p		
class thePlots:

	metPlot = Plot(theVariables.Met,[])
	metPlotLowMass = Plot(theVariables.Met,[theCuts.massCuts.edgeMass])
	metPlot100 = Plot(theVariables.Met,[],binning = [30,100,400,"Events / 10 Gev",[]],additionalName = "MET100")	
	metPlotNoClean = Plot(theVariables.Met,[],binning = [15,0,150,"Events / 10 Gev",[]],additionalName = "NoClean",DoCleanCuts=False)
	
	htPlot = Plot(theVariables.HT,[])	
	
	tralingEtaPlot = Plot(theVariables.TrailingEta,[])		
	LeadingEtaPlot = Plot(theVariables.LeadingEta,[])

	trailingPtPlot = Plot(theVariables.TrailingPt,[])
	leadingPtPlot = Plot(theVariables.LeadingPt,[])

	mllPlot = Plot(theVariables.Mll,[])
	mllPlotGeOneBTags = Plot(theVariables.Mll,[theCuts.bTags.geOneBTags])
	mllPlotNoBTags = Plot(theVariables.Mll,[theCuts.bTags.noBTags])

	nJetsPlot = Plot(theVariables.nJets,[])

	nBJetsPlot = Plot(theVariables.nBJets,[])

	ptllPlot = Plot(theVariables.Ptll,[])				

			
	### plots for trigger efficiency measurements
	### since the data statistics is limited we use a coarser binning on data than on MC
	nJetsPlotTriggerMC = Plot(theVariables.nJets,[],binning=[10,-0.5,9.5,"Events",[]])
	nBJetsPlotTriggerMC = Plot(theVariables.nBJets,[],binning=[6,-0.5,5.5,"Events",[]])
	leadingPtPlotTriggerMC= Plot(theVariables.LeadingPt,[],binning=[28,20,300,"Events / 10 GeV",[]])
	trailingPtPlotTriggerMC= Plot(theVariables.TrailingPt,[],binning=[23,20,250,"Events / 10 GeV",[]])
	mllPlotTriggerMC = Plot(theVariables.Mll,[],binning=[28,20,300,"Events / 10 GeV",[]])							
	htPlotTriggerMC = Plot(theVariables.HT,[],binning=[25,0,1000,"Events / 40 GeV",[]])				
	metPlotTriggerMC = Plot(theVariables.Met,[],binning=[10,0,200,"Events / 20 GeV",[]])					
	tralingEtaPlotTriggerMC = Plot(theVariables.TrailingEta,[],binning=[12,-2.4,2.4,"Events / 0.3",[]])
	leadingEtaPlotTriggerMC = Plot(theVariables.LeadingEta,[],binning=[12,-2.4,2.4,"Events / 0.3",[]])		

	nJetsPlotTrigger = Plot(theVariables.nJets,[],binning=[5,-0.5,9.5,"Events",[]])
	nBJetsPlotTrigger = Plot(theVariables.nBJets,[],binning=[6,-0.5,5.5,"Events",[]])
	leadingPtPlotTrigger= Plot(theVariables.LeadingPt,[],binning=[7,20,300,"Events / 40 GeV",[]])
	trailingPtPlotTrigger= Plot(theVariables.TrailingPt,[],binning=[7,20,300,"Events / 40 GeV",[]])
	mllPlotTrigger = Plot(theVariables.Mll,[],binning=[7,20,300,"Events / 40 GeV",[]])												
	htPlotTrigger = Plot(theVariables.HT,[],binning=[10,200,1000,"Events / 80 GeV",[]])			
	metPlotTrigger = Plot(theVariables.Met,[],binning=[5,0,200,"Events / 40 GeV",[]])			
	tralingEtaPlotTrigger = Plot(theVariables.TrailingEta,[],binning=[12,-2.4,2.4,"Events / 0.3",[]])
	leadingEtaPlotTrigger = Plot(theVariables.LeadingEta,[],binning=[12,-2.4,2.4,"Events / 0.3",[]])					
					
			
	### plots for rmue measurements
	nJetsPlotRMuE = Plot(theVariables.nJets,[],binning=[9,-0.5,8.5,"Events",[]])
	nBJetsPlotRMuE = Plot(theVariables.nBJets,[],binning=[7,-0.5,6.5,"Events",[]])
	leadingPtPlotRMuE= Plot(theVariables.LeadingPt,[],binning=[16,20,100,"Events / 5 GeV",[]])
	trailingPtPlotRMuE= Plot(theVariables.TrailingPt,[],binning=[18,10,100,"Events / 5 GeV",[]])
	mllPlotRMuE = Plot(theVariables.Mll,[],binning=[-1,20,200,"Events / 10 GeV",range(20,60,10)+range(60,120,10)+range(120,250,25)])													
	htPlotRMuE = Plot(theVariables.HT,[],binning=[-1,0,400,"Events / 40 GeV",range(0,300,50)+range(300,800,100)])				
	metPlotRMuE = Plot(theVariables.Met,[],binning=[-1,0,250,"Events / 20 GeV",range(0,100,10)+range(100,150,25)+range(150,250,50)])				
	tralingEtaPlotRMuE = Plot(theVariables.AbsTrailingEta,[],binning=[-1,0,2.55,"Events / 0.3",[i*0.14 for i in range(0,10)]+[i*0.2+1.4 for i in range(0,6)]])				
	leadingEtaPlotRMuE = Plot(theVariables.AbsLeadingEta,[],binning=[-1,0,2.55,"Events / 0.3",[i*0.14 for i in range(0,10)]+[i*0.2+1.4 for i in range(0,6)]])	
	
	### plots for rOutIn measurements				
	mllPlotROutIn = Plot(theVariables.Mll,[],binning=[1000,0,1000,"Events / 1 GeV",[]])				
	metPlotROutIn = Plot(theVariables.Met,[],binning=[-1,0,100,"Events / 1 GeV",[0,10,20,30,40,50,65,80,100]])				
	nJetsPlotROutIn = Plot(theVariables.nJets,[],binning=[5,-0.5,4.5,"Events / 1 GeV",[]])							


### Add signals that are to be plotted is DataMC comparisons here
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
	
### Background processes that can be used. Less important backgrounds are usually clustered
### and referred to as Diboson, Rare etc.
class Backgrounds:
	
	class TTJets_Madgraph:
		subprocesses = ["TTJets_Dilepton_Madgraph_MLM_Spring15_25ns_v1"]
		label = "Madgraph t#bar{t} + jets"
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
		subprocesses = ["ZJets_Madgraph_Spring15_25ns","AStar_aMCatNLO_Spring15_25ns"]
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
		subprocesses = ["WWTo2L2Nu_Powheg_Spring15_25ns","WWToLNuQQ_Powheg_Spring15_25ns","WZTo1L1Nu2Q_aMCatNLO_Spring15_25ns","WZTo1L3Nu_aMCatNLO_Spring15_25ns","WZTo3LNu_Powheg_Spring15_25ns","WZTo2L2Q_aMCatNLO_Spring15_25ns","ZZTo4L_Powheg_Spring15_25ns","ZZTo2Q2Nu_aMCatNLO_Spring15_25ns","ZZTo2L2Q_aMCatNLO_Spring15_25ns"]
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


### Sbottom cross-sections
### The routines in SignalScan use these instead of the MasterList
### since it was a seperate tool
class sbottom_masses:
	class m_b_400:
		cross_section13TeV = 1.83537
	class m_b_425:
		cross_section13TeV = 1.312
	class m_b_450:
		cross_section13TeV = 0.9483  
	class m_b_475:
		cross_section13TeV = 0.6971
	class m_b_500: 
		cross_section13TeV = 0.5185
	class m_b_525:
		cross_section13TeV = 0.3903
	class m_b_550:
		cross_section13TeV = 0.2961
	class m_b_575:
		cross_section13TeV = 0.2261
	class m_b_600:	
		cross_section13TeV = 0.1746		
	class m_b_625:	
		cross_section13TeV = 0.1364		
	class m_b_650:	
		cross_section13TeV = 0.1070		
	class m_b_675:	
		cross_section13TeV = 0.08449	
	class m_b_700:	
		cross_section13TeV = 0.06705
	class m_b_725:		
		cross_section13TeV = 0.0536438
	class m_b_750:		
		cross_section13TeV = 0.0431418
	

	

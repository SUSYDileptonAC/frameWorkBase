import ROOT
import gc
from array import array
from ROOT import TCanvas, TPad, TH1F, TH2F, TH1I, THStack, TLegend, TMath
from defs import defineMyColors
from defs import myColors
from ConfigParser import ConfigParser
from locations import locations
from math import sqrt
config_path = locations.masterListPath
config = ConfigParser()
config.read("%s/Master74X.ini"%config_path)


def loadPickles(path):
	from glob import glob
	import pickle
	result = {}
	for pklPath in glob(path):
		pklFile = open(pklPath, "r")
		result.update(pickle.load(pklFile))
	return result

def readTreeFromFile(path, dileptonCombination, modifier = ""):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""

	
	from ROOT import TChain
	result = TChain()
	if modifier == "":
		result.Add("%s/cutsV27DileptonMiniAODTriggerFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	else:
		if "Single" in modifier:
			result.Add("%s/cutsV27Dilepton%sFinalTriggerTrees/%sDileptonTree"%( path, modifier, dileptonCombination))
		elif "Fake" in modifier:
			result.Add("%s/cutsV27Dilepton%sTree/Trees/Iso"%( path, modifier))
		elif "baseTrees" in modifier:
			result.Add("%s/cutsV27DileptonBaseTrees/%sDileptonTree"%(path, dileptonCombination))
		else:
			result.Add("%s/cutsV27DileptonMiniAOD%sFinalTrees/%sDileptonTree"%( path, modifier, dileptonCombination))
	return result
	
def totalNumberOfGeneratedEvents(path,source="",modifier=""):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
	        (note these include events without EMu EMu EMu signature, too )
	"""
	from ROOT import TFile
	result = {}
	#~ print path

	if "baseTrees" in source:
		for sampleName, filePath in getFilePathsAndSampleNames(path,source).iteritems():
			rootFile = TFile(filePath, "read")
			result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)
		for sampleName, filePath in getFilePathsAndSampleNames(path,"baseTrees").iteritems():
			rootFile = TFile(filePath, "read")
			result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)
	else:				
		for sampleName, filePath in getFilePathsAndSampleNames(path,source,modifier).iteritems():
			rootFile = TFile(filePath, "read")
			result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)				
	return result
	
def readTrees(path, dileptonCombination,source = "", modifier = ""):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	
	for sampleName, filePath in getFilePathsAndSampleNames(path,source,modifier).iteritems():
		result[sampleName] = readTreeFromFile(filePath, dileptonCombination , modifier)
		
	return result

def getFilePathsAndSampleNames(path,source="",modifier = ""):
	"""
	helper function
	path: path to directory containing all sample files

	returns: dict of smaple names -> path of .root file (for all samples in path)
	"""
	result = []
	from glob import glob
	from re import match
	result = {}
	#This is stupid and deals with the mismatch between tasks and datasetnames. Take better care of this in Run II!
	if source == "AlphaT":
		source = "HTMHT_"
	if source == "PFHT":
		source = "HT_"

	#~ # This is even more stupid and tries to deal with uncleaned datasets. This has to improve otherwise it will drive you crazy at some point!
	for filePath in glob("%s/sw7412*.root"%path):
		if source == "":
			sampleName = match(".*sw7412.*\.processed.*\.(.*).root", filePath).groups()[0]		
		else:
			sampleName = ""
			if source == "Summer12" or source == "Fake":
				sample =  match(".*sw7412v.*\.cutsV27.*\.(.*).root", filePath)
			else:
				sourceInsert = source
				if source == "SingleMuon":
					sourceInsert = "SingleMu"
				sample =  match(".*sw7412v.*\.cutsV27.*\.(%s.*).root"%sourceInsert, filePath)
				
			if sample is not None:					
				sampleName = sample.groups()[0]
		#for the python enthusiats: yield sampleName, filePath is more efficient here :)
		if sampleName is not "":
			result[sampleName] = filePath
	return result


	
def createHistoFromTree(tree, variable, weight, nBins, firstBin, lastBin, nEvents = -1,smearDY=False,binning=None):
	"""
	tree: tree to create histo from)
	variable: variable to plot (must be a branch of the tree)
	weight: weights to apply (e.g. "var1*(var2 > 15)" will use weights from var1 and cut on var2 > 15
	nBins, firstBin, lastBin: number of bins, first bin and last bin (same as in TH1F constructor)
	nEvents: number of events to process (-1 = all)
	"""
	from ROOT import TH1F
	from random import randint
	from sys import maxint
	if nEvents < 0:
		nEvents = maxint
	#make a random name you could give something meaningfull here,
	#but that would make this less readable
	name = "%x"%(randint(0, maxint))
	
	if binning == []:
		result = TH1F(name, "", nBins, firstBin, lastBin)
	else:
		result = TH1F(name, "", len(binning)-1, array("f",binning))
		
	result.Sumw2()

	if smearDY and variable == "met":
		print weight
		r = ROOT.TRandom3()
		tempTree = tree.CopyTree(weight)
		print weight.split("*(")[0]
		for ev in tempTree:
			result.Fill(ev.met*r.Gaus(1.08,0.1),getattr(ev,weight.split("*(")[0]))
			
		tempTree.IsA().Destructor(tempTree)
		#myobject.IsA().Destructor(myobject)	
			#print getattr(ev,weight.split("*(")[0])
	else:
		tree.Draw("%s>>%s"%(variable, name), weight, "goff", nEvents)
	result.SetBinContent(nBins,result.GetBinContent(nBins)+result.GetBinContent(nBins+1))
	if result.GetBinContent(nBins) >= 0.:
		result.SetBinError(nBins,sqrt(result.GetBinContent(nBins)))
	else:
		result.SetBinError(nBins,0)
	gc.collect()
	return result
	
def create2DHistoFromTree(tree, variable, variable2, weight, nBins, firstBin, lastBin, nBins2=10, firstBin2=0, lastBin2=100, nEvents = -1,smearDY=False,binning=None,binning2=None):
	"""
	tree: tree to create histo from)
	variable: variable to plot (must be a branch of the tree)
	weight: weights to apply (e.g. "var1*(var2 > 15)" will use weights from var1 and cut on var2 > 15
	nBins, firstBin, lastBin: number of bins, first bin and last bin (same as in TH1F constructor)
	nEvents: number of events to process (-1 = all)
	"""
	from ROOT import TH2F
	from random import randint
	from sys import maxint
	if nEvents < 0:
		nEvents = maxint
	#make a random name you could give something meaningfull here,
	#but that would make this less readable
	name = "%x"%(randint(0, maxint))
	
	if binning == []:
		result = TH2F(name, "", nBins, firstBin, lastBin, nBins2, firstBin2, lastBin2)
	else:
		result = TH2F(name, "", len(binning)-1, array("f",binning), len(binning2)-1, array("f",binning2))
		
	result.Sumw2()

	tree.Draw("%s:%s>>%s"%(variable2,variable, name), weight, "goff", nEvents)
	
	#~ for ev in tree:
		#~ result.Fill(getattr(ev,variable),abs(getattr(ev,variable2)))
	return result


def createMyColors():
    iIndex = 2000

    containerMyColors = []
    for color in defineMyColors.keys():
        tempColor = ROOT.TColor(iIndex,
            float(defineMyColors[color][0]) / 255, float(defineMyColors[color][1]) / 255, float(defineMyColors[color][2]) / 255)
        containerMyColors.append(tempColor)

        myColors.update({ color: iIndex })
        iIndex += 1

    return containerMyColors
	
class Process:
	samples = []
	xsecs = []
	nEvents = []
	label = ""
	theColor = 0
	theLineColor = 0 
	histo = ROOT.TH1F()
	uncertainty = 0.
	scaleFac = 1.
	additionalSelection = None
	
	def __init__(self, process ,Counts={"none":-1}, normalized = True):
		self.samples = process.subprocesses
		self.xsecs = []
		self.negWeightFractions = []
		self.nEvents = []
		self.label = process.label
		self.theColor = process.fillcolor
		self.theLineColor = process.linecolor
		self.histo.SetLineColor(process.linecolor)
		self.histo.SetFillColor(process.fillcolor)
		self.uncertainty = process.uncertainty
		self.scaleFac = 1.
		self.additionalSelection = process.additionalSelection
		self.normalized = normalized
		for sample in self.samples:
			self.xsecs.append(eval(config.get(sample,"crosssection")))
			self.negWeightFractions.append(eval(config.get(sample,"negWeightFraction")))
			self.nEvents.append(Counts[sample])

		
	def createCombinedHistogram(self,lumi,plot,tree1,tree2 = "None",shift = 1.,scalefacTree1=1.,scalefacTree2=1.,TopWeightUp=False,TopWeightDown=False,signal=False,doTopReweighting=True):
		#~ doTopReweighting = False
		if len(plot.binning) == 0:
			self.histo = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		else:
			self.histo = TH1F("","",len(plot.binning)-1, array("f",plot.binning))
		
		nEvents = -1
		smearDY = False
		if self.additionalSelection != None:
			if self.additionalSelection == "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)":
				smearDY = False

			if "weightDown" in plot.cuts:
				cut = plot.cuts.replace("weightDown*(","weightDown*(%s &&"%self.additionalSelection)		
			elif "weightUp" in plot.cuts:
				cut = plot.cuts.replace("weightUp*(","weightUp*(%s &&"%self.additionalSelection)						
			else:
				cut = plot.cuts.replace("weight*(","weight*(%s &&"%self.additionalSelection)		
		else: 
			cut = plot.cuts

		weightNorm = 1./0.99
		
		if signal:



			MultiQuarkScaleFactor = "((nGenSUSYLeptons == 0 && nGenSUSYNeutrinos == 0) * 9 * 0.4887)"
			NeutrinoQuarkScaleFactor = "((nGenSUSYLeptons == 0 && nGenSUSYNeutrinos == 2) * 9./2. * 0.2796)"
			MultiNeutrinoScaleFactor = "((nGenSUSYLeptons == 0 && nGenSUSYNeutrinos == 4) * 9 * 0.04)"
			DileptonNeutrinoScaleFactor = "((nGenSUSYLeptons == 2 && nGenSUSYNeutrinos == 2) * 9./2. * 0.0404)"
			DileptonQuarkScaleFactor = "((nGenSUSYLeptons == 2 && nGenSUSYNeutrinos == 0) * 9./2. * 0.1411)"
			MultileptonScaleFactor = "((nGenSUSYLeptons == 4)*9*0.0102)"
			
			signalWeight = "(%s+%s+%s+%s+%s+%s)*sbottomWeight"%(MultiQuarkScaleFactor,NeutrinoQuarkScaleFactor,MultiNeutrinoScaleFactor,DileptonNeutrinoScaleFactor,DileptonQuarkScaleFactor,MultileptonScaleFactor)
			
			cut = cut+"*"+signalWeight
					
		for index, sample in enumerate(self.samples):
			for name, tree in tree1.iteritems(): 
				if name == sample:
					if doTopReweighting and "TT" in name:						
						if TopWeightUp:
							tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning)
						elif TopWeightDown:	
							tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning)
						else:	
							tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning)
					
					
					else:
						tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,smearDY,binning=plot.binning)
						
					if self.normalized:				
						tempHist.Scale((lumi*scalefacTree1*self.xsecs[index]/(self.nEvents[index]*(1-2*self.negWeightFractions[index])**2)))
					self.histo.Add(tempHist.Clone())

			if tree2 != "None":		
				for name, tree in tree2.iteritems(): 
					if name == sample:
						if doTopReweighting and "TT" in name:
							if TopWeightUp:
								tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning)
							elif TopWeightDown:	
								tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning)
							else:	
								tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning)
						else:
							tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,smearDY,binning=plot.binning)
						

						if self.normalized:
							tempHist.Scale((lumi*self.xsecs[index]*scalefacTree2/(self.nEvents[index]*(1-2*self.negWeightFractions[index])**2)))

						self.histo.Add(tempHist.Clone())
		self.histo.SetFillColor(self.theColor)
		self.histo.SetLineColor(self.theLineColor)
		self.histo.GetXaxis().SetTitle(plot.xaxis) 
		self.histo.GetYaxis().SetTitle(plot.yaxis)	
				
		return self.histo

	
class TheStack:
	from ROOT import THStack
	theStack = THStack()	
	theHistogram = ROOT.TH1F()	
	theHistogramXsecUp = ROOT.TH1F()
	theHistogramXsecDown = ROOT.TH1F()
	theHistogramTheoUp = ROOT.TH1F()
	theHistogramTheoDown = ROOT.TH1F()
	def  __init__(self,processes,lumi,plot,tree1,tree2,shift = 1.0,scalefacTree1=1.0,scalefacTree2=1.0,saveIntegrals=False,counts=None,JESUp=False,JESDown=False,TopWeightUp=False,TopWeightDown=False,PileUpUp=False,PileUpDown=False,doTopReweighting=True,theoUncert = 0.):
		self.theStack = THStack()
		self.theHistogram = ROOT.TH1F()
		self.theHistogram.Sumw2()
		self.theHistogramXsecDown = ROOT.TH1F()
		self.theHistogramXsecUp = ROOT.TH1F()
		self.theHistogramTheoDown = ROOT.TH1F()
		self.theHistogramTheoUp = ROOT.TH1F()
		if len(plot.binning) == 0:
			self.theHistogram = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			self.theHistogramXsecDown = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			self.theHistogramXsecUp = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			self.theHistogramTheoDown = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			self.theHistogramTheoUp = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		else:
			self.theHistogram = ROOT.TH1F("","",len(plot.binning)-1, array("f",plot.binning))
			self.theHistogramXsecDown = ROOT.TH1F("","",len(plot.binning)-1, array("f",plot.binning))
			self.theHistogramXsecUp = ROOT.TH1F("","",len(plot.binning)-1, array("f",plot.binning))
			self.theHistogramTheoDown = ROOT.TH1F("","",len(plot.binning)-1, array("f",plot.binning))
			self.theHistogramTheoUp = ROOT.TH1F("","",len(plot.binning)-1, array("f",plot.binning))


			

			
			
		for process in processes:
			if not "t#bar{t}" in process.label:
				localTheo = 0.
			else:
				localTheo = theoUncert
			temphist = TH1F()
			temphist.Sumw2()
			if TopWeightUp:
				temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2,TopWeightUp=True,doTopReweighting=True)
			elif TopWeightDown:	
				temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2,TopWeightDown=True,doTopReweighting=True)
			else:	
				temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2,doTopReweighting=doTopReweighting)
			if saveIntegrals:
				
				errIntMC = ROOT.Double()
				intMC = temphist.IntegralAndError(0,temphist.GetNbinsX()+1,errIntMC)				
				
				val = float(intMC)
				err = float(errIntMC)
				if JESUp:
					jesUp = abs(counts[process.label]["val"]-val)
					counts[process.label]["jesUp"]=jesUp
				elif TopWeightUp:
					topWeightUp = abs(counts[process.label]["val"]-val)
					counts[process.label]["topWeightUp"]=topWeightUp
				elif TopWeightDown:
					topWeightDown = abs(counts[process.label]["val"]-val)
					counts[process.label]["topWeightDown"]=topWeightDown
				elif PileUpUp:
					pileUpUp = abs(counts[process.label]["val"]-val)
					counts[process.label]["pileUpUp"]=pileUpUp
				elif PileUpDown:
					pileUpDown = abs(counts[process.label]["val"]-val)
					counts[process.label]["pileUpDown"]=pileUpDown
				elif JESDown:
					jesDown = abs(counts[process.label]["val"]-val)
					counts[process.label]["jesDown"]=jesDown
				else:
					xSecUncert = val*process.uncertainty
					theoUncertVal = val*localTheo
					counts[process.label] = {"val":val,"err":err,"xSec":xSecUncert,"theo":theoUncertVal}

					#~ counts[process.label]["val"]=val
					#~ counts[process.label]["err"]=err
					#~ counts[process.label]["xSec"]=xSecUncert
			self.theStack.Add(temphist.Clone())
			self.theHistogram.Add(temphist.Clone())
			temphist2 = temphist.Clone()
			temphist2.Scale(1-process.uncertainty)
			self.theHistogramXsecDown.Add(temphist2.Clone())
			temphist3 = temphist.Clone()
			temphist3.Scale(1+process.uncertainty)
			self.theHistogramXsecUp.Add(temphist3.Clone())
			temphist4 = temphist.Clone()
			temphist4.Scale(1-localTheo)
			self.theHistogramTheoDown.Add(temphist4.Clone())
			temphist5 = temphist.Clone()
			temphist5.Scale(1+localTheo)
			self.theHistogramTheoUp.Add(temphist5.Clone())

def getDataHist(plot,tree1,tree2="None",dataname = ""):
	histo = TH1F()
	histo2 = TH1F()
	if dataname == "":
		dataname = "MergedData"		
	for name, tree in tree1.iteritems():
		if name == dataname:
			histo = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin,binning=plot.binning)
	if tree2 != "None":		
		for name, tree in tree2.iteritems():
			if name == dataname:
				histo2 = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin,binning=plot.binning)
				histo.Add(histo2.Clone())
	return histo	
	
def getDataTrees(path):

	result = {}
	
	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
		

	dataname = "MergedData"	
	for name, tree in treesEE.iteritems():
		if name == dataname:
			result["EE"] = tree
	for name, tree in treesMM.iteritems():
		if name == dataname:
			result["MM"] = tree
	for name, tree in treesEM.iteritems():
		if name == dataname:
			result["EM"] = tree
			
	return result
				
def getTotalTopWeight(genPt1,genPt2):
	from math import exp,sqrt
	## 8 TeV Dilepton
	a = 0.148
	b = -0.00129 
	sf1 = exp(a*genPt1+b)
	sf2 = exp(a*genPt2+b)
	
	result = sqrt(sf1+sf2)
	
	return result

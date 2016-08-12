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

from centralConfig import versions

config.read("%s/%s"%(config_path,versions.masterListForMC))


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
		result.Add("%s/%sDileptonFinalTrees/%sDileptonTree"%(path,versions.cuts, dileptonCombination))
	else:
		result.Add("%s/%sDilepton%sFinalTrees/%sDileptonTree"%( path,versions.cuts, modifier, dileptonCombination))
	return result
	
def totalNumberOfGeneratedEvents(path):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
	        (note these include events without EMu EMu EMu signature, too )
	"""
	from ROOT import TFile
	result = {}
	#~ print path
			
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		rootFile = TFile(filePath, "read")
		result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)				
	return result
	
def readTrees(path, dileptonCombination, modifier = ""):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		result[sampleName] = readTreeFromFile(filePath, dileptonCombination , modifier)
		
	return result

def getFilePathsAndSampleNames(path):
	"""
	helper function
	path: path to directory containing all sample files

	returns: dict of smaple names -> path of .root file (for all samples in path)
	"""
	result = []
	from glob import glob
	from re import match
	result = {}


	for filePath in glob("%s/*.root"%(path)):		
		if "processed" in filePath:		
			sampleName = match(".*\.processed.*\.(.*).root", filePath).groups()[0]		
		else:		
			sampleName =  match(".*\.%s.*\.(.*).root"%(versions.cuts), filePath).groups()[0]		
		#for the python enthusiats: yield sampleName, filePath is more efficient here :)
		if sampleName is not "":
			result[sampleName] = filePath
	return result


	
def createHistoFromTree(tree, variable, weight, nBins, firstBin, lastBin, nEvents = -1,binning=None):
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
	tree.Draw("%s>>%s"%(variable, name), weight, "goff", nEvents)
	result.SetBinContent(nBins,result.GetBinContent(nBins)+result.GetBinContent(nBins+1))
	if result.GetBinContent(nBins) >= 0.:
		result.SetBinError(nBins,sqrt(result.GetBinContent(nBins)))
	else:
		result.SetBinError(nBins,0)
	gc.collect()
	return result
	
def create2DHistoFromTree(tree, variable, variable2, weight, nBins, firstBin, lastBin, nBins2=10, firstBin2=0, lastBin2=100, nEvents = -1,binning=None,binning2=None):
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

		
	def createCombinedHistogram(self,lumi,plot,tree1,tree2 = "None",shift = 1.,scalefacTree1=1.,scalefacTree2=1.,signal=False):
		if len(plot.binning) == 0:
			self.histo = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		else:
			self.histo = TH1F("","",len(plot.binning)-1, array("f",plot.binning))
		
		nEvents = -1
		if self.additionalSelection != None:
			cut = plot.cuts.replace("weight*(","weight*(%s &&"%self.additionalSelection)		
		else: 
			cut = plot.cuts

		weightNorm = 1./0.99
			

		for index, sample in enumerate(self.samples):
			for name, tree in tree1.iteritems(): 
				if name == sample:
					tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning)
						
					if self.normalized:		
						tempHist.Scale((lumi*scalefacTree1*self.xsecs[index]/(self.nEvents[index]*(1-2*self.negWeightFractions[index]))))
					self.histo.Add(tempHist.Clone())

			if tree2 != "None":		
				for name, tree in tree2.iteritems(): 
					if name == sample:
						tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning)
						

						if self.normalized:
							tempHist.Scale((lumi*self.xsecs[index]*scalefacTree2/(self.nEvents[index]*(1-2*self.negWeightFractions[index]))))

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
	def  __init__(self,processes,lumi,plot,tree1,tree2,shift = 1.0,scalefacTree1=1.0,scalefacTree2=1.0,saveIntegrals=False,counts=None):
		self.theStack = THStack()
		self.theHistogram = ROOT.TH1F()
		self.theHistogram.Sumw2()
		if len(plot.binning) == 0:
			self.theHistogram = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		else:
			self.theHistogram = ROOT.TH1F("","",len(plot.binning)-1, array("f",plot.binning))

			
			
		for process in processes:
			temphist = TH1F()
			temphist.Sumw2()	
			temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2)
			if saveIntegrals:
				
				errIntMC = ROOT.Double()
				intMC = temphist.IntegralAndError(0,temphist.GetNbinsX()+1,errIntMC)				
				
				val = float(intMC)
				err = float(errIntMC)
				
				xSecUncert = val*process.uncertainty
				counts[process.label] = {"val":val,"err":err,"xSec":xSecUncert}
				
			self.theStack.Add(temphist.Clone())
			self.theHistogram.Add(temphist.Clone())

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

	

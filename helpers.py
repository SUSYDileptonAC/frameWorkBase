import ROOT
import gc
from array import array
from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TMath
from defs import defineMyColors
from defs import myColors
from ConfigParser import ConfigParser
from locations import locations
config_path = locations.masterListPath
config = ConfigParser()
config.read("%s/Master53X.ini"%config_path)


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
		result.Add("%s/cutsV23DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	else:
		if "Single" in modifier:
			result.Add("%s/cutsV23Dilepton%sFinalTriggerTrees/%sDileptonTree"%( path, modifier, dileptonCombination))
		else:
			result.Add("%s/cutsV23Dilepton%sFinalTrees/%sDileptonTree"%( path, modifier, dileptonCombination))
	return result
	
def totalNumberOfGeneratedEvents(path,source=""):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
	        (note these include events without EMu EMu EMu signature, too )
	"""
	from ROOT import TFile
	result = {}
	#~ print path

	for sampleName, filePath in getFilePathsAndSampleNames(path,source).iteritems():
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


	for filePath in glob("%s/sw538*.root"%path):
		if source == "":
			sampleName = match(".*sw538v.*\.processed.*\.(.*).root", filePath).groups()[0]		
		else:
			sampleName = ""
			if source == "Summer12":
				sample =  match(".*sw538v.*\.cutsV23.*\.(.*).root", filePath)
			else:
				sourceInsert = source
				if source == "SingleMuon":
					sourceInsert = "SingleMu"
				sample =  match(".*sw538v.*\.cutsV23.*\.(%s.*).root"%sourceInsert, filePath)
				
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
	
	if len(binning) == 0:
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
	gc.collect()
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
	
	def __init__(self, process ,Counts={"none":-1}):
		self.samples = process.subprocesses
		self.xsecs = []
		self.nEvents = []
		self.label = process.label
		self.theColor = process.fillcolor
		self.theLineColor = process.linecolor
		self.histo.SetLineColor(process.linecolor)
		self.histo.SetFillColor(process.fillcolor)
		self.uncertainty = process.uncertainty
		self.scaleFac = 1.
		self.additionalSelection = process.additionalSelection
		for sample in self.samples:
			self.xsecs.append(eval(config.get(sample,"crosssection")))
			self.nEvents.append(Counts[sample])

		
	def createCombinedHistogram(self,lumi,plot,tree1,tree2 = "None",shift = 1.,scalefacTree1=1.,scalefacTree2=1.,TopWeightUp=False,TopWeightDown=False,signal=False,doTopReweighting=True):
		
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

					tempHist.Scale((lumi*scalefacTree1*self.xsecs[index]/self.nEvents[index]))
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
						

						tempHist.Scale((lumi*self.xsecs[index]*scalefacTree2/self.nEvents[index]))

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
	def  __init__(self,processes,lumi,plot,tree1,tree2,shift = 1.0,scalefacTree1=1.0,scalefacTree2=1.0,saveIntegrals=False,counts=None,JESUp=False,JESDown=False,TopWeightUp=False,TopWeightDown=False,PileUpUp=False,PileUpDown=False,doTopReweighting=True):
		self.theStack = THStack()
		self.theHistogram = ROOT.TH1F()
		self.theHistogram.Sumw2()
		self.theHistogramXsecDown = ROOT.TH1F()
		self.theHistogramXsecUp = ROOT.TH1F()
		if len(plot.binning) == 0:
			self.theHistogram = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			self.theHistogramXsecDown = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			self.theHistogramXsecUp = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		else:
			self.theHistogram = ROOT.TH1F("","",len(plot.binning)-1, array("f",plot.binning))
			self.theHistogramXsecDown = ROOT.TH1F("","",len(plot.binning)-1, array("f",plot.binning))
			self.theHistogramXsecUp = ROOT.TH1F("","",len(plot.binning)-1, array("f",plot.binning))


			

			
			
		for process in processes:
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
					counts[process.label] = {"val":val,"err":err,"xSec":xSecUncert}
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

def getDataHist(plot,tree1,tree2="None"):
	histo = TH1F()
	histo2 = TH1F()


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
				
def getTotalTopWeight(genPt1,genPt2):
	from math import exp,sqrt
	## 8 TeV Dilepton
	a = 0.148
	b = -0.00129 
	sf1 = exp(a*genPt1+b)
	sf2 = exp(a*genPt2+b)
	
	result = sqrt(sf1+sf2)
	
	return result

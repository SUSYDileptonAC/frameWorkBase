import ROOT
import gc
from array import array
from ROOT import TCanvas, TPad, TH1F, TH2F, TH1I, THStack, TLegend, TMath, TFile
from defs import defineMyColors, theCuts
from defs import myColors
from ConfigParser import ConfigParser
from locations import locations
from math import sqrt
config_path = locations.masterListPath
config = ConfigParser()

from centralConfig import versions

config.read("%s/%s"%(config_path,versions.masterListForMC))

def ensurePathExists(path):
        import os
        import errno
        try:
                os.makedirs(path)
        except OSError as exception:
                if exception.errno != errno.EEXIST:
                        raise



def loadPickles(path):
        from glob import glob
        import pickle
        result = {}
        for pklPath in glob(path):
                pklFile = open(pklPath, "r")
                result.update(pickle.load(pklFile))
        return result

def readTreeFromFile(path, dileptonCombination, modifier = "",versionNr="cutsV34"):
        """
        helper functionfrom argparse import ArgumentParser
        path: path to .root file containing simulated events
        dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

        returns: tree containing events for on sample and dileptonCombination
        """

        from ROOT import TChain
        result = TChain()
        #~ result.SetProof(True)
        if modifier == "":
                result.Add("%s/%sDileptonFinalTrees/%sDileptonTree"%(path, versionNr, dileptonCombination))
        else:
                #~ result.Add("%s/%sDilepton%sFinalTrees/%sDileptonTree"%( path, versions.cuts, modifier, dileptonCombination))
                result.Add("%s/%sDilepton%sFinalTrees/%sDileptonTree"%( path, versionNr, modifier, dileptonCombination))
        return result
        
def totalNumberOfGeneratedEvents(path,source="",modifier=""):
        """
        path: path to directory containing all sample files

        returns dict samples names -> number of simulated events in source sample
                (note these include events without EMu EMu EMu signature, too )
        """
        from ROOT import TFile
        result = {}
        
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
        #~ for filePath in glob("%s/%sv*.root"%(path,versions.cmssw)):
        for filePath in glob("%s/*.root"%(path)):
                if source == "":
                        #~ sampleName = match(".*%sv.*\.processed.*\.(.*).root"%versions.cmssw, filePath).groups()[0]           
                        sampleName = match(".*\.processed.*\.(.*).root", filePath).groups()[0]          
                else:
                        sampleName = ""
                        if source == "Summer12" or source == "Fake":
                                sample =  match(".*%sv.*\.%s.*\.(.*).root"%(versions.cmssw,versions.cuts), filePath)
                        else:
                                #~ print source 
                                #~ print versions.cuts
                                #~ print filePath
                                #~ print ".*%sv.*\.%s.*\.(%s.*).root"%(versions.cmssw,versions.cuts,source)
                                sourceInsert = source
                                sample =  match(".*%sv.*\.%s.*\.(%s.*).root"%(versions.cmssw,versions.cuts,sourceInsert), filePath)
                                
                        if sample is not None:                                  
                                sampleName = sample.groups()[0]
                #for the python enthusiats: yield sampleName, filePath is more efficient here :)
                if sampleName is not "":
                        result[sampleName] = filePath
        return result


        
def createHistoFromTree(tree, variable, weight, nBins, firstBin, lastBin, nEvents = -1,smearDY=False,binning=None,doPUWeights = False,normalizeToBinWidth = False):
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
        if binning == [] or binning == None:
                result = TH1F(name, "", nBins, firstBin, lastBin)
        else:
                result = TH1F(name, "", len(binning)-1, array("f",binning))
                nBins = len(binning)-1
                
                
        result.Sumw2()
        if smearDY and variable == "met":
                r = ROOT.TRandom3()
                tempTree = tree.CopyTree(weight)
                for ev in tempTree:
                        result.Fill(ev.met*r.Gaus(1.08,0.1),getattr(ev,weight.split("*(")[0]))
                        
                tempTree.IsA().Destructor(tempTree)
                #myobject.IsA().Destructor(myobject)    
                        #print getattr(ev,weight.split("*(")[0])
        elif doPUWeights:
                tempTree = tree.CopyTree(weight)
                
                for ev in tempTree:
                        if variable == "p4.M()":
                                result.Fill(ev.p4.M(),getattr(ev,"genWeight")*getVtxWeight(getattr(ev,"nVertices")))
                        elif variable == "(pt2>pt1)*eta1+(pt1>pt2)*eta2":
                                if ev.pt2 > ev.pt1: 
                                        result.Fill(ev.eta1,getattr(ev,"genWeight")*getVtxWeight(getattr(ev,"nVertices")))
                                elif ev.pt2 < ev.pt1: 
                                        result.Fill(ev.eta2,getattr(ev,"genWeight")*getVtxWeight(getattr(ev,"nVertices")))
                        elif variable == "(pt1>pt2)*pt2+(pt2>pt1)*pt1":
                                if ev.pt2 > ev.pt1: 
                                        result.Fill(ev.pt1,getattr(ev,"genWeight")*getVtxWeight(getattr(ev,"nVertices")))
                                elif ev.pt2 < ev.pt1: 
                                        result.Fill(ev.pt2,getattr(ev,"genWeight")*getVtxWeight(getattr(ev,"nVertices")))
                        else:   
                                result.Fill(getattr(ev,variable),getattr(ev,"genWeight")*getVtxWeight(getattr(ev,"nVertices")))
                        
                tempTree.IsA().Destructor(tempTree)
                #myobject.IsA().Destructor(myobject)    
                        #print getattr(ev,weight.split("*(")[0])
        else:
                tree.Draw("%s>>%s"%(variable, name), weight, "goff", nEvents)
                #~ tree.Draw("%s"%(variable), weight, "goff", nEvents)
        

        result.SetBinContent(nBins+1,0)
        
        #if binning == [] or binning == None:
        la,laErr = result.GetBinContent(nBins  ),result.GetBinError(nBins  )
        ov,ovErr = result.GetBinContent(nBins+1),result.GetBinError(nBins+1)
        result.SetBinContent(nBins,la+ov)
        result.SetBinError(nBins,sqrt(laErr**2+ovErr**2))
        #else:
                        #la,laErr = result.GetBinContent(nBins-2  ),result.GetBinError(nBins-2)
                        #ov,ovErr = result.GetBinContent(nBins-1),result.GetBinError(nBins)
                        #result.SetBinContent(nBins-2,la+ov)
                        #result.SetBinError(nBins-2,sqrt(laErr**2+ovErr**2))
       
        if normalizeToBinWidth:
                for i in range(0,nBins):
                        if i < nBins -1:
                                result.SetBinContent(i,result.GetBinContent(i)/result.GetBinWidth(i))
                                result.SetBinError(i,result.GetBinError(i)/result.GetBinWidth(i))
                        else:
                                result.SetBinContent(i,result.GetBinContent(i)/result.GetBinWidth(i-1))
                                result.SetBinError(i,result.GetBinError(i)/result.GetBinWidth(i-1)) 
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
        
        if binning == [] or binning == None:
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
                self.kFactors = []
                self.nEvents = []
                self.label = process.label
                self.theColor = process.fillcolor
                self.theLineColor = process.linecolor
                self.histo.SetLineColor(process.linecolor)
                self.histo.SetFillColor(process.fillcolor)
                self.uncertainty = process.uncertainty
                self.scaleFac = process.scaleFac
                self.additionalSelection = process.additionalSelection
                self.normalized = normalized
                for sample in self.samples:
                        self.xsecs.append(eval(config.get(sample,"crosssection")))
                        self.negWeightFractions.append(eval(config.get(sample,"negWeightFraction")))
                        self.kFactors.append(eval(config.get(sample,"kfactor")))
                        self.nEvents.append(Counts[sample])


        def createCombined2DHistogram(self,lumi,plot,plot2,tree1,tree2 = "None",shift = 1.,scalefacTree1=1.,scalefacTree2=1.,TopWeightUp=False,TopWeightDown=False,signal=False,doTopReweighting=True,doPUWeights=False):
                #~ doTopReweighting = False
                #if len(plot.binning) == 0:
                self.histo = TH2F("","",plot.nBins,plot.firstBin,plot.lastBin, plot2.nBins, plot2.firstBin,plot2.lastBin)
                #else:
                        #self.histo = TH2F("","",len(plot.binning)-1, array("f",plot.binning))
                
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
                                plot2.cuts = plot2.cuts.replace("weight*","")
                                plot2.cuts = plot2.cuts.replace("genWeight*","")
                                cut = cut+"*"+plot2.cuts
                else: 
                        plot2.cuts = plot2.cuts.replace("weight*","")
                        plot2.cuts = plot2.cuts.replace("genWeight*","")
                        cut = plot.cuts+"*"+plot2.cuts
                weightNorm = 1./0.99
                                      
                for index, sample in enumerate(self.samples):
                        for name, tree in tree1.iteritems(): 
                                if name == sample:
                                        if doTopReweighting and "TT" in name:                                
                                                if TopWeightUp:
                                                        tempHist = create2DHistoFromTree(tree, plot.variable, plot2.variable,  "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut, plot.nBins, plot.firstBin, plot.lastBin, plot2.nBins, plot2.firstBin, plot2.lastBin)
                                                elif TopWeightDown:     
                                                        tempHist = create2DHistoFromTree(tree, plot.variable, plot2.variable, cut , plot.nBins, plot.firstBin, plot.lastBin, plot2.nBins, plot2.firstBin, plot2.lastBin)
                                                else:   
                                                        tempHist = create2DHistoFromTree(tree, plot.variable, plot2.variable, "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut, plot.nBins, plot.firstBin, plot.lastBin, plot2.nBins, plot2.firstBin, plot2.lastBin)
                                        
                                        
                                        else:
                                                tempHist = create2DHistoFromTree(tree, plot.variable, plot2.variable, cut , plot.nBins, plot.firstBin, plot.lastBin, plot2.nBins, plot2.firstBin, plot2.lastBin)
                                                
                                        if self.normalized:     
                                                #~ print lumi
                                                #~ print scalefacTree1 
                                                #~ print self.xsecs[index]
                                                #~ print self.nEvents[index]
                                                #~ print self.negWeightFractions[index]         
                                                tempHist.Scale((self.scaleFac*lumi*scalefacTree1*self.xsecs[index]/(self.nEvents[index]*(1-2*self.negWeightFractions[index]))))
                                        self.histo.Add(tempHist.Clone(),1)

                        if tree2 != "None":             
                                for name, tree in tree2.iteritems(): 
                                        if name == sample:
                                                if doTopReweighting and "TT" in name:
                                                        if TopWeightUp:
                                                                tempHist = create2DHistoFromTree(tree, plot.variable, plot2.variable,  "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut, plot.nBins, plot.firstBin, plot.lastBin, plot2.nBins, plot2.firstBin, plot2.lastBin)
                                                        elif TopWeightDown:     
                                                                tempHist = create2DHistoFromTree(tree, plot.variable, plot2.variable, cut , plot.nBins, plot.firstBin, plot.lastBin, plot2.nBins, plot2.firstBin, plot2.lastBin)
                                                        else:   
                                                                tempHist = create2DHistoFromTree(tree, plot.variable, plot2.variable, "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut, plot.nBins, plot.firstBin, plot.lastBin, plot2.nBins, plot2.firstBin, plot2.lastBin)
                                                else:
                                                        tempHist = create2DHistoFromTree(tree, plot.variable, plot2.variable, cut , plot.nBins, plot.firstBin, plot.lastBin, plot2.nBins, plot2.firstBin, plot2.lastBin)
                                                

                                                if self.normalized:
                                                        tempHist.Scale((self.scaleFac*lumi*self.xsecs[index]*scalefacTree2/(self.nEvents[index]*(1-2*self.negWeightFractions[index]))))

                                                self.histo.Add(self.histo.Clone(),tempHist.Clone(),1,1)

                self.histo.GetXaxis().SetTitle(plot.xaxis) 
                self.histo.GetYaxis().SetTitle(plot2.xaxis)      
                                
                return self.histo
                

        def createCombinedHistogram(self,lumi,plot,tree1,tree2 = "None",shift = 1.,scalefacTree1=1.,scalefacTree2=1.,TopWeightUp=False,TopWeightDown=False,signal=False,doTopReweighting=True,doPUWeights=False,normalizeToBinWidth=False,useTriggerEmulation=False):
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
              
                
                cutsTrigger = cut.replace("chargeProduct < 0", "chargeProduct < 0 && triggerSummary > 0")
                
                if useTriggerEmulation:                                 
                                        cut = cutsTrigger
                else:                                   
                                        cut = cut.replace("triggerSummary > 0 &&","")
                                        
                
                #~ cut = cut.replace("triggerSummary > 0 &&","")
                
                
                for index, sample in enumerate(self.samples):
                        for name, tree in tree1.iteritems(): 
                                if name == sample:
                                                                        if doTopReweighting and "TT" in name:          
                                                                                        if TopWeightUp:
                                                                                                        #~ tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                                                                        tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.0615-0.0005*genPtTop1)*exp(0.0615-0.0005*genPtTop2))*sqrt(exp(0.0615-0.00005*genPtTop1)*exp(0.0615-0.00005*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                                                        elif TopWeightDown:     
                                                                                                        tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                                                        else:   
                                                                                                        #~ tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                                                                        tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.0615-0.0005*genPtTop1)*exp(0.0615-0.0005*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                                        
                                                                        
                                                                        else:
                                                                                        tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,smearDY,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                                                        
                                                                        if self.normalized:     
                                                                                        #~ print lumi
                                                                                        #~ print scalefacTree1 
                                                                                        #~ print self.xsecs[index]
                                                                                        #~ print self.nEvents[index]
                                                                                        #~ print self.negWeightFractions[index]         
                                                                                        #~ tempHist.Scale((self.scaleFac*lumi*scalefacTree1*self.xsecs[index]/(self.nEvents[index]*(1-2*self.negWeightFractions[index]))))
                                                                                        tempHist.Scale((self.scaleFac*lumi*scalefacTree1*self.xsecs[index]*self.kFactors[index]/(self.nEvents[index]*(1-2*self.negWeightFractions[index]))))
                                                                                        #~ tempHist.Scale((self.scaleFac*lumi*scalefacTree1*self.xsecs[index]/self.nEvents[index]))
                                                                        self.histo.Add(tempHist.Clone())

                        if tree2 != "None":             
                                for name, tree in tree2.iteritems(): 
                                        if name == sample:
                                                if doTopReweighting and "TT" in name:
                                                        if TopWeightUp:
                                                                #~ tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                                tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.0615-0.00005*genPtTop1)*exp(0.0615-0.00005*genPtTop2))*sqrt(exp(0.0615-0.00005*genPtTop1)*exp(0.0615-0.00005*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                        elif TopWeightDown:     
                                                                tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                        else:   
                                                                #~ tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                                tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.0615-0.00005*genPtTop1)*exp(0.0615-0.00005*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                else:
                                                        tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents,smearDY,binning=plot.binning,doPUWeights=doPUWeights,normalizeToBinWidth=normalizeToBinWidth)
                                                

                                                if self.normalized:
                                                        #~ tempHist.Scale((self.scaleFac*lumi*self.xsecs[index]*scalefacTree2/(self.nEvents[index]*(1-2*self.negWeightFractions[index]))))
                                                        tempHist.Scale((self.scaleFac*lumi*self.xsecs[index]*scalefacTree2*self.kFactors[index]/(self.nEvents[index]*(1-2*self.negWeightFractions[index]))))
                                                        #~ tempHist.Scale((self.scaleFac*lumi*self.xsecs[index]*scalefacTree2/self.nEvents[index]))

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
        def  __init__(self,processes,lumi,plot,tree1,tree2,shift = 1.0,scalefacTree1=1.0,scalefacTree2=1.0,saveIntegrals=False,counts=None,JESUp=False,JESDown=False,TopWeightUp=False,TopWeightDown=False,PileUpUp=False,PileUpDown=False,doTopReweighting=True,theoUncert = 0.,doPUWeights = False,normalizeToBinWidth = False, useTriggerEmulation= False):
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
                                temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2,TopWeightUp=True,doTopReweighting=True,doPUWeights = doPUWeights,normalizeToBinWidth = normalizeToBinWidth, useTriggerEmulation = useTriggerEmulation)
                        elif TopWeightDown:     
                                temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2,TopWeightDown=True,doTopReweighting=True,doPUWeights = doPUWeights,normalizeToBinWidth = normalizeToBinWidth, useTriggerEmulation = useTriggerEmulation)
                        else:   
                                temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2,doTopReweighting=doTopReweighting,doPUWeights = doPUWeights,normalizeToBinWidth = normalizeToBinWidth, useTriggerEmulation = useTriggerEmulation)
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

def getDataHist(plot,tree1,tree2="None",dataname = "",normalizeToBinWidth = False):
        histo = TH1F()
        histo2 = TH1F()
        if dataname == "":
                dataname = "MergedData"         
        for name, tree in tree1.iteritems():
                if name == dataname:
                        print dataname
                        histo = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin,binning=plot.binning,normalizeToBinWidth=normalizeToBinWidth)
        if tree2 != "None":             
                for name, tree in tree2.iteritems():
                        if name == dataname:
                                histo2 = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin,binning=plot.binning,normalizeToBinWidth=normalizeToBinWidth)
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
                                
def getVtxWeight(nVtx):
        #~ # based on 225/pb, Golden JSON from 02/10/2015
        #~ weights = [1, 1, 5.257347331038417, 3.6620287172043655, 3.2145438780779156, 2.9215830134107024, 2.7172733269793143, 2.499763816411226, 2.2358505010682275, 1.946608815936303, 1.66663585526661, 1.3917062061924035, 1.1239566743048217, 0.8838519279375375, 0.6762957802962626, 0.5277954493868846, 0.3953278839107886, 0.2916698725757984, 0.21232722799503542, 0.15516191067117857, 0.1187750029289671, 0.08675361880847646, 0.07089979610006057, 0.046231845546640206, 0.03480539409420972, 0.02463791911084164, 0.024537360650415386, 0.014415024309474854, 0.015096285304302518, 0.008316456648660545, 0.0, 0.010835052897837951, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, 1, 0.0, 0.0, 1, 1, 1, 0.0, 1, 1, 1, 1, 1, 1, 1]
        # based on ~600/pb, Golden JSON from 09/10/2015, produced by Vince
        
        weights = [0,0,3.06258,2.44413,2.36438,2.3998,2.37008,2.30127,2.14311,1.93811,1.70787,1.45249,1.19933,0.9531,0.740734,0.566524,0.425824,0.314512,0.229213,0.163893,0.123593,0.0896858,0.0608875,0.0481201,0.035267,0.0233243,0.01961,0.0132398,0.00812161,0.00758528,0.00949008,0.00438004,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
        if nVtx >= 49:
                return 0
        else:
                return weights[nVtx+1]
        

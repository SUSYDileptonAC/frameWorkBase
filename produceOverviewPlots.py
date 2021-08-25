import pickle
import os
import sys


from setTDRStyle import setTDRStyle

from corrections import corrections
#from corrections import rSFOF,rSFOFDirect,rSFOFTrig, rEEOF, rMMOF, rOutIn
from centralConfig import zPredictions, regionsToUse, runRanges, OtherPredictions, OnlyZPredictions,systematics
from helpers import createMyColors
from defs import myColors,thePlots,getPlot,theCuts,getRunRange

import ctypes
import ratios

from array import array

import ROOT
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphErrors, TF1, gStyle, TGraphAsymmErrors, TFile, TH2F
# ROOT.gROOT.SetBatch(True)

def readPickle(name,regionName,runName,MC=False):
        
        if MC:
                if os.path.isfile("shelves/%s_%s_%s_MC.pkl"%(name,regionName,runName)):
                        result = pickle.load(open("shelves/%s_%s_%s_MC.pkl"%(name,regionName,runName),"rb"))
                else:
                        print "shelves/%s_%s_%s.pkl not found, exiting"%(name,regionName,runName)               
                        sys.exit()              
        else:
                if os.path.isfile("shelves/%s_%s_%s.pkl"%(name,regionName,runName)):
                        result = pickle.load(open("shelves/%s_%s_%s.pkl"%(name,regionName,runName),"rb"))
                else:
                        print "shelves/%s_%s_%s.pkl not found, exiting"%(name,regionName,runName)               
                        sys.exit()

        return result   
        
### load pickles for the systematics
def loadPickles(path):
        from glob import glob
        result = {}
        for pklPath in glob(path):
                pklFile = open(pklPath, "r")
                result.update(pickle.load(pklFile))
        return result

def getWeightedAverage(val1,err1,val2,err2):
        
        weightedAverage = (val1/(err1**2) +val2/(err2**2))/(1./err1**2+1./err2**2)
        weightedAverageErr = 1./(1./err1**2+1./err2**2)**0.5
        
        return weightedAverage, weightedAverageErr

tableHeaders = {"default":"being inclusive in the number of b-tagged jets","geOneBTags":"requiring at least one b-tagged jet","geTwoBTags":"requiring at least two b-tagged jets"}
tableColumnHeaders = {"default":"no b-tag requirement","noBTags":"veto on b-tagged jets","geOneBTags":"$\geq$ 1 b-tagged jets","geTwoBTags":"$\geq$ 2 b-tagged jets"}

                        
def getResultsNLL(shelves, signalRegion):
       
        NLLRegions = ["lowNLL","highNLL",]
        massRegions = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]       
        nBJetsRegions = [ "zeroBJets","oneOrMoreBJets",]
        MT2Regions = ["highMT2"]
        result = {}
        
        region = "inclusive"
        
        result["onZPrediction_highNLL_highMT2_zeroBJets"] = OnlyZPredictions.MT2.SF.zeroB.highNLL.val
        result["onZPrediction_lowNLL_highMT2_zeroBJets"] = OnlyZPredictions.MT2.SF.zeroB.lowNLL.val
        result["onZPrediction_highNLL_highMT2_zeroBJets_Err"] = OnlyZPredictions.MT2.SF.zeroB.highNLL.err
        result["onZPrediction_lowNLL_highMT2_zeroBJets_Err"] = OnlyZPredictions.MT2.SF.zeroB.lowNLL.err
        
        result["onZPrediction_highNLL_highMT2_oneOrMoreBJets"] = OnlyZPredictions.MT2.SF.oneB.highNLL.val
        result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets"] = OnlyZPredictions.MT2.SF.oneB.lowNLL.val
        result["onZPrediction_highNLL_highMT2_oneOrMoreBJets_Err"] = OnlyZPredictions.MT2.SF.oneB.highNLL.err
        result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets_Err"] = OnlyZPredictions.MT2.SF.oneB.lowNLL.err
        
        runRanges = shelves.keys()
        
        
        for selection in NLLRegions:
                result[selection] = {}
                for MT2Region in MT2Regions:
                        for nBJetsRegion in nBJetsRegions:
                                for massRegion in massRegions: 
                                        
                                        
                                        currentBin = getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.nBJetsCuts,nBJetsRegion).name+"_"+getattr(theCuts.massCuts,massRegion).name
                                        resultsBinName = "%s_%s_%s"%(MT2Region,nBJetsRegion,massRegion)
                                        
                                        print resultsBinName
                                        print currentBin
                                        result[selection]["%s_EE"%(resultsBinName)] = 0.0
                                        result[selection]["%s_MM"%(resultsBinName)] = 0.0
                                        result[selection]["%s_SF"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OF"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaled"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)] = 0.0
                                        
                                        
                                        for runRangeName in runRanges:
                                                shelve = shelves[runRangeName]
                                                
                                                
                                                result[selection]["%s_EE"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EE"]
                                                result[selection]["%s_MM"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["MM"]
                                                result[selection]["%s_SF"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EE"] + shelve[signalRegion][selection][currentBin]["MM"]
                                                result[selection]["%s_OF"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EM"]
                                                result[selection]["%s_OFRMuEScaled"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EMRMuEScaled"]
                                                
                                                
                                                runRange = getRunRange(runRangeName)
                                                RT = corrections[runRange.era].rSFOFTrig.inclusive.val
                                                RTErr = corrections[runRange.era].rSFOFTrig.inclusive.err

                                                rmuepred = shelve[signalRegion][selection][currentBin]["EMRMuEScaled"]
                                                OFRMuEScaledErrRT = shelve[signalRegion][selection][currentBin]["EMRMuEScaled"]*RTErr/RT
                                                OFRMuEScaledErrFlat = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpFlat"]-rmuepred), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownFlat"]-rmuepred))
                                                OFRMuEScaledErrPt = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpPt"]-rmuepred), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownPt"]-rmuepred))
                                                OFRMuEScaledErrEta = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpEta"]-rmuepred), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownEta"]-rmuepred))
                                                
                                                result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)] + OFRMuEScaledErrRT**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)]**2 + OFRMuEScaledErrFlat**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)]**2 + OFRMuEScaledErrPt**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)]**2 + OFRMuEScaledErrEta**2)**0.5
                                        
                                        shelve=None # safety so it is not used outside the loop
                                        
                                        yield_up = ctypes.c_double(1.)
                                        yield_down = ctypes.c_double(1.)
                                
                                        
                                        ## calculate poisson error for FS prediction
                                        ROOT.RooHistError.instance().getPoissonInterval(int(result[selection]["%s_OF"%(resultsBinName)]),yield_down,yield_up,1.)
                                        
                                        ## calculate poisson error for observed data
                                        yieldSF_up = ctypes.c_double(1.)
                                        yieldSF_down = ctypes.c_double(1.)
                                        ROOT.RooHistError.instance().getPoissonInterval(int(result[selection]["%s_SF"%(resultsBinName)]),yieldSF_down,yieldSF_up,1.)
                                        
                                        
                                        result[selection]["%s_SFUp"%(resultsBinName)] = yieldSF_up.value - result[selection]["%s_SF"%(resultsBinName)]
                                        result[selection]["%s_SFDown"%(resultsBinName)] = result[selection]["%s_SF"%(resultsBinName)] - yieldSF_down.value
                                        
                                        # fs backgrounds
                                        result[selection]["%s_PredFactSF"%(resultsBinName)] = result[selection]["%s_OFRMuEScaled"%(resultsBinName)]
                                        if result[selection]["%s_OF"%(resultsBinName)] > 0:
                                                eff_rsfof = result[selection]["%s_PredFactSF"%(resultsBinName)]/result[selection]["%s_OF"%(resultsBinName)]
                                                
                                                result[selection]["%s_PredFactStatUpSF"%(resultsBinName)] = yield_up.value*eff_rsfof - result[selection]["%s_PredFactSF"%(resultsBinName)]
                                                result[selection]["%s_PredFactStatDownSF"%(resultsBinName)] = result[selection]["%s_PredFactSF"%(resultsBinName)] - yield_down.value*eff_rsfof
                                                systErrFact = (result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)]**2)**0.5
                                                result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] = systErrFact
                                        else:
                                                result[selection]["%s_PredFactStatUpSF"%(resultsBinName)] = 1.8
                                                result[selection]["%s_PredFactStatDownSF"%(resultsBinName)] = yield_down.value
                                                result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] = 0
                                        
                                        if result[selection]["%s_OF"%(resultsBinName)] > 0:
                                                result[selection]["%s_RSFOF_Fact"%(resultsBinName)] = result[selection]["%s_PredFactSF"%(resultsBinName)] / result[selection]["%s_OF"%(resultsBinName)]
                                                result[selection]["%s_RSFOF_Fact_Err"%(resultsBinName)] = result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] / result[selection]["%s_OF"%(resultsBinName)]
                                        else:
                                                result[selection]["%s_RSFOF_Fact"%(resultsBinName)] = 0.
                                                result[selection]["%s_RSFOF_Fact_Err"%(resultsBinName)] = 0.
                                        
                                        result[selection]["%s_PredSF"%(resultsBinName)] = result[selection]["%s_PredFactSF"%(resultsBinName)]
                                        if result[selection]["%s_PredSF"%(resultsBinName)] > 0:
                                                result[selection]["%s_PredStatUpSF"%(resultsBinName)] = result[selection]["%s_PredFactStatUpSF"%(resultsBinName)]
                                        else:
                                                result[selection]["%s_PredStatUpSF"%(resultsBinName)] = 1.8
                                                
                                        result[selection]["%s_PredStatDownSF"%(resultsBinName)] = result[selection]["%s_PredFactStatDownSF"%(resultsBinName)] 
                                        result[selection]["%s_PredSystErrSF"%(resultsBinName)] = result[selection]["%s_PredFactSystErrSF"%(resultsBinName)]
                                        
                                        result[selection]["%s_PredFSDownSF"%(resultsBinName)] =  (result[selection]["%s_PredFactStatDownSF"%(resultsBinName)]**2 + result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] **2)**0.5
                                        result[selection]["%s_PredFSUpSF"%(resultsBinName)] =  (result[selection]["%s_PredFactStatUpSF"%(resultsBinName)]**2 + result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] **2)**0.5
                                        
                                        # Drell-Yan
                                        rOutIn = corrections["Combined"].rOutIn
                                        onZPredName = "onZPrediction_%s_%s_%s"%(selection,MT2Region,nBJetsRegion)
                                        onZPredErrName = "onZPrediction_%s_%s_%s_Err"%(selection,MT2Region,nBJetsRegion)
                                        
                                        result[selection]["%s_ZPredSF"%(resultsBinName)] = result[onZPredName]*getattr(getattr(rOutIn,massRegion),region).val
                                        result[selection]["%s_ZPredErrSF"%(resultsBinName)] = ((result[onZPredName]*getattr(getattr(rOutIn,massRegion),region).err)**2 + (result[onZPredErrName] * getattr(getattr(rOutIn,massRegion),region).val)**2 )**0.5

                                        # ttz,wz,zz
                                        
                                        
                                        result[selection]["%s_RarePredSF"%(resultsBinName)] = 0.0
                                        result[selection]["%s_RarePredErrSF"%(resultsBinName)] = 0.0
                                        
                                        rarePredName ="%s_%s_%s_%s"%(massRegion,selection,MT2Region,nBJetsRegion)
                                        
                                        for runRangeName in runRanges:
                                                shelve = shelves[runRangeName]
                                        
                                                rarePred = shelve["Rares"]["%s_SF"%(rarePredName)] - shelve["Rares"]["%s_OF"%(rarePredName)]
                                                rareUp = shelve["Rares"]["%s_SF_Up"%(rarePredName)] - shelve["Rares"]["%s_OF_Up"%(rarePredName)]
                                                rareDown = shelve["Rares"]["%s_SF_Down"%(rarePredName)] - shelve["Rares"]["%s_OF_Down"%(rarePredName)]
                                                
                                                result[selection]["%s_RarePredSF"%(resultsBinName)] += rarePred
                                                
                                                errRare = max(abs(rareUp-rarePred), abs(rarePred-rareDown))
                                                statErrRare = shelve["Rares"]["%s_SF_Stat"%(rarePredName)]
                                                result[selection]["%s_RarePredErrSF"%(resultsBinName)] = (result[selection]["%s_RarePredErrSF"%(resultsBinName)]**2 + errRare**2 + statErrRare**2)**0.5
                                                
                        

                                        result[selection]["%s_TotalPredSF"%(resultsBinName)] = result[selection]["%s_PredSF"%(resultsBinName)] + result[selection]["%s_ZPredSF"%(resultsBinName)] + result[selection]["%s_RarePredSF"%(resultsBinName)]
                                        result[selection]["%s_TotalPredErrUpSF"%(resultsBinName)]   = ( result[selection]["%s_PredStatUpSF"%(resultsBinName)]**2   +  result[selection]["%s_PredSystErrSF"%(resultsBinName)]**2 + result[selection]["%s_ZPredErrSF"%(resultsBinName)]**2 + result[selection]["%s_RarePredErrSF"%(resultsBinName)]**2)**0.5
                                        result[selection]["%s_TotalPredErrDownSF"%(resultsBinName)] = ( result[selection]["%s_PredStatDownSF"%(resultsBinName)]**2 +  result[selection]["%s_PredSystErrSF"%(resultsBinName)]**2 + result[selection]["%s_ZPredErrSF"%(resultsBinName)]**2 + result[selection]["%s_RarePredErrSF"%(resultsBinName)]**2)**0.5

        return result
        

def makeOverviewMllPlot(shelves,region, nBJetsRegion,normalizeToBinWidth=False):


        colors = createMyColors()
        
        plot = getPlot("mllResultPlot")
        
        results = getResultsNLL(shelves,"NLL")
        
        
        histObs = ROOT.TH1F("histObs","histObs",len(plot.binning)-1, array("f",plot.binning))
        
        histObs.SetMarkerColor(ROOT.kBlack)
        histObs.SetLineColor(ROOT.kBlack)
        histObs.SetMarkerStyle(20)
        
        histPred = ROOT.TH1F("histPred","histPred",len(plot.binning)-1, array("f",plot.binning))
        histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",len(plot.binning)-1, array("f",plot.binning))
        histDY = ROOT.TH1F("histDY","histDY",len(plot.binning)-1, array("f",plot.binning))
        histRare = ROOT.TH1F("histRare","histRare",len(plot.binning)-1, array("f",plot.binning))
        histFullBG = ROOT.TH1F("histFullBG","histFullBG",len(plot.binning)-1, array("f",plot.binning))
        
                
        hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
        
        
        
        plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
        ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
        style = setTDRStyle()
        style.SetPadTopMargin(0.07)
        ROOT.gStyle.SetOptStat(0)
        plotPad.UseCurrentStyle()
        ratioPad.UseCurrentStyle()
        plotPad.Draw()  
        ratioPad.Draw() 
        plotPad.cd()
        
        
        
        
        graphObs = ROOT.TGraphAsymmErrors()     
        
        histObs.SetBinContent(1,results[region]["highMT2_"+nBJetsRegion+"_mass20To60_SF"])
        histObs.SetBinContent(2,results[region]["highMT2_"+nBJetsRegion+"_mass60To86_SF"])
        histObs.SetBinContent(3,0)
        histObs.SetBinContent(4,results[region]["highMT2_"+nBJetsRegion+"_mass96To150_SF"])
        histObs.SetBinContent(5,results[region]["highMT2_"+nBJetsRegion+"_mass150To200_SF"])
        histObs.SetBinContent(6,results[region]["highMT2_"+nBJetsRegion+"_mass200To300_SF"])
        histObs.SetBinContent(7,results[region]["highMT2_"+nBJetsRegion+"_mass300To400_SF"])
        histObs.SetBinContent(8,results[region]["highMT2_"+nBJetsRegion+"_mass400_SF"])  
        
        histFlavSym.SetBinContent(1,results[region]["highMT2_"+nBJetsRegion+"_mass20To60_PredSF"])
        histFlavSym.SetBinContent(2,results[region]["highMT2_"+nBJetsRegion+"_mass60To86_PredSF"])
        histFlavSym.SetBinContent(3,0)
        histFlavSym.SetBinContent(4,results[region]["highMT2_"+nBJetsRegion+"_mass96To150_PredSF"])
        histFlavSym.SetBinContent(5,results[region]["highMT2_"+nBJetsRegion+"_mass150To200_PredSF"])
        histFlavSym.SetBinContent(6,results[region]["highMT2_"+nBJetsRegion+"_mass200To300_PredSF"])
        histFlavSym.SetBinContent(7,results[region]["highMT2_"+nBJetsRegion+"_mass300To400_PredSF"])
        histFlavSym.SetBinContent(8,results[region]["highMT2_"+nBJetsRegion+"_mass400_PredSF"])

        histDY.SetBinContent(1,results[region]["highMT2_"+nBJetsRegion+"_mass20To60_ZPredSF"])
        histDY.SetBinContent(2,results[region]["highMT2_"+nBJetsRegion+"_mass60To86_ZPredSF"])
        histDY.SetBinContent(3,0)
        histDY.SetBinContent(4,results[region]["highMT2_"+nBJetsRegion+"_mass96To150_ZPredSF"])
        histDY.SetBinContent(5,results[region]["highMT2_"+nBJetsRegion+"_mass150To200_ZPredSF"])
        histDY.SetBinContent(6,results[region]["highMT2_"+nBJetsRegion+"_mass200To300_ZPredSF"])
        histDY.SetBinContent(7,results[region]["highMT2_"+nBJetsRegion+"_mass300To400_ZPredSF"])
        histDY.SetBinContent(8,results[region]["highMT2_"+nBJetsRegion+"_mass400_ZPredSF"])      
        
        histRare.SetBinContent(1,results[region]["highMT2_"+nBJetsRegion+"_mass20To60_RarePredSF"])
        histRare.SetBinContent(2,results[region]["highMT2_"+nBJetsRegion+"_mass60To86_RarePredSF"])
        histRare.SetBinContent(3,0)
        histRare.SetBinContent(4,results[region]["highMT2_"+nBJetsRegion+"_mass96To150_RarePredSF"])
        histRare.SetBinContent(5,results[region]["highMT2_"+nBJetsRegion+"_mass150To200_RarePredSF"])
        histRare.SetBinContent(6,results[region]["highMT2_"+nBJetsRegion+"_mass200To300_RarePredSF"])
        histRare.SetBinContent(7,results[region]["highMT2_"+nBJetsRegion+"_mass300To400_RarePredSF"])
        histRare.SetBinContent(8,results[region]["highMT2_"+nBJetsRegion+"_mass400_RarePredSF"]) 
        
        errGraph = ROOT.TGraphAsymmErrors()
        errGraphRatio = ROOT.TGraphAsymmErrors()
        
        for i in range(1,histFlavSym.GetNbinsX()+1):
                if i <= 3:
                        graphObs.SetPoint(i,histObs.GetBinCenter(i),histObs.GetBinContent(i))
                        errGraph.SetPoint(i,histFlavSym.GetBinCenter(i),histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
                        errGraphRatio.SetPoint(i,histFlavSym.GetBinCenter(i),1)
                else:
                        #~ if i == histFlavSym.GetNbinsX():
                                #~ graphObs.SetPoint(i-1,histObs.GetBinCenter(i-1)+histObs.GetBinWidth(i-1),histObs.GetBinContent(i))
                        #~ else:
                        graphObs.SetPoint(i-1,histObs.GetBinCenter(i),histObs.GetBinContent(i))
                        errGraph.SetPoint(i-1,histFlavSym.GetBinCenter(i),histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
                        errGraphRatio.SetPoint(i-1,histFlavSym.GetBinCenter(i),1)
                

        graphObs.SetPointError(1,0,0,results[region]["highMT2_"+nBJetsRegion+"_mass20To60_SFDown"],results[region]["highMT2_"+nBJetsRegion+"_mass20To60_SFUp"])
        graphObs.SetPointError(2,0,0,results[region]["highMT2_"+nBJetsRegion+"_mass60To86_SFDown"],results[region]["highMT2_"+nBJetsRegion+"_mass60To86_SFUp"])
        graphObs.SetPointError(3,0,0,results[region]["highMT2_"+nBJetsRegion+"_mass96To150_SFDown"],results[region]["highMT2_"+nBJetsRegion+"_mass96To150_SFUp"])
        graphObs.SetPointError(4,0,0,results[region]["highMT2_"+nBJetsRegion+"_mass150To200_SFDown"],results[region]["highMT2_"+nBJetsRegion+"_mass150To200_SFUp"])
        graphObs.SetPointError(5,0,0,results[region]["highMT2_"+nBJetsRegion+"_mass200To300_SFDown"],results[region]["highMT2_"+nBJetsRegion+"_mass200To300_SFUp"])
        graphObs.SetPointError(6,0,0,results[region]["highMT2_"+nBJetsRegion+"_mass300To400_SFDown"],results[region]["highMT2_"+nBJetsRegion+"_mass300To400_SFUp"])
        graphObs.SetPointError(7,0,0,results[region]["highMT2_"+nBJetsRegion+"_mass400_SFDown"],results[region]["highMT2_"+nBJetsRegion+"_mass400_SFUp"])

        errGraph.SetPointError(1,0.5*histFlavSym.GetBinWidth(1),0.5*histFlavSym.GetBinWidth(1),results[region]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrDownSF"],results[region]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrUpSF"])
        errGraph.SetPointError(2,0.5*histFlavSym.GetBinWidth(2),0.5*histFlavSym.GetBinWidth(2),results[region]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrDownSF"],results[region]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrUpSF"])
        errGraph.SetPointError(3,0.5*histFlavSym.GetBinWidth(4),0.5*histFlavSym.GetBinWidth(4),results[region]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrDownSF"],results[region]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrUpSF"])
        errGraph.SetPointError(4,0.5*histFlavSym.GetBinWidth(5),0.5*histFlavSym.GetBinWidth(5),results[region]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrDownSF"],results[region]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrUpSF"])
        errGraph.SetPointError(5,0.5*histFlavSym.GetBinWidth(6),0.5*histFlavSym.GetBinWidth(6),results[region]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrDownSF"],results[region]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrUpSF"])
        errGraph.SetPointError(6,0.5*histFlavSym.GetBinWidth(7),0.5*histFlavSym.GetBinWidth(7),results[region]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrDownSF"],results[region]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrUpSF"])
        errGraph.SetPointError(7,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),results[region]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrDownSF"],results[region]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrUpSF"])
        
        errGraphRatio.SetPointError(1,0.5*histFlavSym.GetBinWidth(1),0.5*histFlavSym.GetBinWidth(1),results[region]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrDownSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredSF"],results[region]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrUpSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredSF"])
        errGraphRatio.SetPointError(2,0.5*histFlavSym.GetBinWidth(2),0.5*histFlavSym.GetBinWidth(2),results[region]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrDownSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredSF"],results[region]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrUpSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredSF"])
        errGraphRatio.SetPointError(3,0.5*histFlavSym.GetBinWidth(4),0.5*histFlavSym.GetBinWidth(4),results[region]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrDownSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredSF"],results[region]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrUpSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredSF"])
        errGraphRatio.SetPointError(4,0.5*histFlavSym.GetBinWidth(5),0.5*histFlavSym.GetBinWidth(5),results[region]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrDownSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredSF"],results[region]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrUpSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredSF"])
        errGraphRatio.SetPointError(5,0.5*histFlavSym.GetBinWidth(6),0.5*histFlavSym.GetBinWidth(6),results[region]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrDownSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredSF"],results[region]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrUpSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredSF"])
        errGraphRatio.SetPointError(6,0.5*histFlavSym.GetBinWidth(7),0.5*histFlavSym.GetBinWidth(7),results[region]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrDownSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredSF"],results[region]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrUpSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredSF"])
        errGraphRatio.SetPointError(7,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),results[region]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrDownSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass400_TotalPredSF"],results[region]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrUpSF"]/results[region]["highMT2_"+nBJetsRegion+"_mass400_TotalPredSF"])
        
        errGraph.SetFillColor(ROOT.kGray+3)     
        errGraph.SetFillStyle(3644)     
        errGraphRatio.SetFillColor(ROOT.kGray+3)     
        errGraphRatio.SetFillStyle(3644)     
        #errGraph.SetLineStyle(3644)     
        histFlavSym.SetLineColor(ROOT.kBlack)
        histFlavSym.SetFillColor(17)    
        histDY.SetFillColor(ROOT.kGreen+2)  
        histRare.SetFillColor(38)
        histDY.SetLineColor(ROOT.kBlack)
        histRare.SetLineColor(ROOT.kBlack)

        
        if normalizeToBinWidth:
                print histFlavSym.GetNbinsX()
                for i in range(1,histFlavSym.GetNbinsX()+1):
                        if i < 3:
                                histObs.SetBinContent(i,histObs.GetBinContent(i)/histObs.GetBinWidth(i))
                                histFlavSym.SetBinContent(i,histFlavSym.GetBinContent(i)/histFlavSym.GetBinWidth(i))
                                histDY.SetBinContent(i,histDY.GetBinContent(i)/histDY.GetBinWidth(i))
                                histRare.SetBinContent(i,histRare.GetBinContent(i)/histRare.GetBinWidth(i))
                                graphObs.SetPoint(i,histObs.GetBinCenter(i),histObs.GetBinContent(i))
                                graphObs.SetPointError(i,0,0,graphObs.GetErrorYlow(i)/histObs.GetBinWidth(i),graphObs.GetErrorYhigh(i)/histObs.GetBinWidth(i))
                                errGraph.SetPoint(i,histFlavSym.GetBinCenter(i),histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
                                errGraph.SetPointError(i,0.5*histFlavSym.GetBinWidth(i),0.5*histFlavSym.GetBinWidth(i),errGraph.GetErrorYlow(i)/histFlavSym.GetBinWidth(i),errGraph.GetErrorYhigh(i)/histFlavSym.GetBinWidth(i))
                        elif i > 3:
                                histObs.SetBinContent(i,histObs.GetBinContent(i)/histObs.GetBinWidth(i))
                                histFlavSym.SetBinContent(i,histFlavSym.GetBinContent(i)/histFlavSym.GetBinWidth(i))
                                histDY.SetBinContent(i,histDY.GetBinContent(i)/histDY.GetBinWidth(i))
                                histRare.SetBinContent(i,histRare.GetBinContent(i)/histRare.GetBinWidth(i))
                                graphObs.SetPoint(i-1,histObs.GetBinCenter(i),histObs.GetBinContent(i))
                                graphObs.SetPointError(i-1,0,0,graphObs.GetErrorYlow(i-1)/histObs.GetBinWidth(i),graphObs.GetErrorYhigh(i-1)/histObs.GetBinWidth(i))
                                errGraph.SetPoint(i-1,histFlavSym.GetBinCenter(i),histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
                                errGraph.SetPointError(i-1,0.5*histFlavSym.GetBinWidth(i),0.5*histFlavSym.GetBinWidth(i),errGraph.GetErrorYlow(i-1)/histFlavSym.GetBinWidth(i),errGraph.GetErrorYhigh(i-1)/histFlavSym.GetBinWidth(i))
                        
        from ROOT import THStack
        
        stack = THStack()
        stack.Add(histDY)       
        stack.Add(histRare)     
        stack.Add(histFlavSym)
        
        histFullBG.Add(histDY)  
        histFullBG.Add(histRare)        
        histFullBG.Add(histFlavSym)
        
        
        ymax = histObs.GetBinContent(histObs.GetMaximumBin()) * 1.75
        ymin = 0
        
        if nBJetsRegion == "oneOrMoreBJets":
                bJetLabel = "N_{b-tags} #geq 1"
        else:
                bJetLabel = "N_{b-tags} = 0"
        if region == "highNLL":
                regionLabel = "#splitline{non.t#bar{t} like signal region}{%s}"%bJetLabel
        else:
                regionLabel = "#splitline{t#bar{t} like signal region}{%s}"%bJetLabel

        
        if normalizeToBinWidth:
                hCanvas.DrawFrame(20,ymin,500,ymax,"; m_{ll} [GeV] ; Events / GeV")
        else:
                hCanvas.DrawFrame(20,ymin,500,ymax,"; m_{ll} [GeV] ; Events / Bin")
        
        latex = ROOT.TLatex()
        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(0.04)
        latex.SetNDC(True)
        latexCMS = ROOT.TLatex()
        latexCMS.SetTextFont(61)
        #latexCMS.SetTextAlign(31)
        latexCMS.SetTextSize(0.06)
        latexCMS.SetNDC(True)
        latexCMSExtra = ROOT.TLatex()
        latexCMSExtra.SetTextFont(52)
        #latexCMSExtra.SetTextAlign(31)
        latexCMSExtra.SetTextSize(0.045)
        latexCMSExtra.SetNDC(True)              
        


        intlumi = ROOT.TLatex()
        intlumi.SetTextAlign(12)
        intlumi.SetTextSize(0.03)
        intlumi.SetNDC(True)            

        latex.DrawLatex(0.95, 0.95, "%s fb^{-1} (13 TeV)"%"35.9")
        
        #~ cmsExtra = "Preliminary"
        cmsExtra = ""
        latexCMS.DrawLatex(0.18,0.87,"CMS")
        if "Simulation" in cmsExtra:
                yLabelPos = 0.80        
        else:
                yLabelPos = 0.83        

        latexCMSExtra.DrawLatex(0.18,yLabelPos,"%s"%(cmsExtra))
        

        leg = ROOT.TLegend(0.55, 0.40, 0.95, 0.87,regionLabel,"brNDC")
        #leg.SetTitleSize(0.05)
        #~ leg.SetNColumns(2)
        leg.SetFillColor(10)
        leg.SetLineColor(10)
        leg.SetShadowColor(0)
        leg.SetBorderSize(1)
        
        bkgHistForLegend = histFlavSym.Clone("bkgHistForLegend")
        bkgHistForLegend.SetLineColor(ROOT.kBlack)
        bkgHistForLegend.SetFillColor(17)   
        #bkgHistForLegend.SetLineColor(ROOT.kBlue+3)
        #bkgHistForLegend.SetFillColor(ROOT.kWhite)
        bkgHistForLegend.SetLineWidth(2)
        
        #~ leg.AddEntry(histObs,"Data","pe")
        leg.AddEntry(graphObs,"Observed","pe")
        #~ leg.AddEntry(histFlavSym, "Total backgrounds","l")
        leg.AddEntry(bkgHistForLegend, "Flavor.symmetric","f")
        leg.AddEntry(errGraph,"Tot. unc.", "f") 
        leg.AddEntry(histDY,"DY+jets", "f")
        leg.AddEntry(histRare,"Z+#nu", "f")     

        
        stack.Draw("samehist")  
        errGraph.Draw("same02")
        #~ histObs.Draw("pesame")
        graphObs.Draw("pesame")
        
        leg.Draw("same")


        plotPad.RedrawAxis()    


        ratioPad.cd()
        
        
        xs = []
        ys = []
        yErrorsUp = []
        yErrorsDown = []
        widths = []
        
        for i in range(0,histObs.GetNbinsX()):
                if i <= 3:
                        xs.append(histObs.GetBinCenter(i))
                        widths.append(0.5*histObs.GetBinWidth(i))               
                        if histFullBG.GetBinContent(i) > 0:
                                ys.append(histObs.GetBinContent(i)/histFullBG.GetBinContent(i))
                                yErrorsUp.append(graphObs.GetErrorYhigh(i)/histFullBG.GetBinContent(i))                 
                                yErrorsDown.append(graphObs.GetErrorYlow(i)/histFullBG.GetBinContent(i))                                
                
                        else:
                                ys.append(10.)
                                yErrorsUp.append(0)                     
                                yErrorsDown.append(0)
                else:
                        xs.append(histObs.GetBinCenter(i))
                        widths.append(0.5*histObs.GetBinWidth(i))               
                        ys.append(histObs.GetBinContent(i)/histFullBG.GetBinContent(i))
                        yErrorsUp.append(graphObs.GetErrorYhigh(i-1)/histFullBG.GetBinContent(i))                       
                        yErrorsDown.append(graphObs.GetErrorYlow(i-1)/histFullBG.GetBinContent(i))                              
                
        
        
        ROOT.gPad.cd()

                # axis
        nBinsX = 20
        nBinsY = 10
        hAxis = ROOT.TH2F("hAxis", "", nBinsX, 20, 500, nBinsY, 0, 2)
        hAxis.Draw("AXIS")
                
        hAxis.GetYaxis().SetNdivisions(408)
        hAxis.SetTitleOffset(0.4, "Y")
        hAxis.SetTitleSize(0.15, "Y")
        hAxis.SetYTitle("#frac{Observed}{Prediction}  ")
        hAxis.GetXaxis().SetLabelSize(0.0)
        hAxis.GetYaxis().SetLabelSize(0.1)

        oneLine = ROOT.TLine(20, 1.0, 500, 1.0)
        #~ oneLine.SetLineStyle(2)
        oneLine.Draw()
        oneLine2 = ROOT.TLine(20, 0.5, 500, 0.5)
        oneLine2.SetLineStyle(2)
        oneLine2.Draw()
        oneLine3 = ROOT.TLine(20, 1.5, 500, 1.5)
        oneLine3.SetLineStyle(2)
        oneLine3.Draw()
        
        errGraphRatio.Draw("same02")
        
        ratioGraph = ROOT.TGraphAsymmErrors(len(xs), array("d", xs), array("d", ys), array("d", widths), array("d", widths), array("d", yErrorsDown), array("d", yErrorsUp))
                
        ratioGraph.Draw("same pe0")     


        
        ROOT.gPad.RedrawAxis()
        plotPad.RedrawAxis()
        ratioPad.RedrawAxis()
        
        hCanvas.Print("cutNCountResultMll_%s_%s.pdf"%(region, nBJetsRegion))
        

        
def makeOverviewPlot(shelves, nBJetsRegion, blind = False, ratio=True, signal=True):

        #from helpers import createMyColors
        from defs import myColors
        #colors = createMyColors()       

        ROOT.gROOT.SetBatch(True)
        resultsNLL = getResultsNLL(shelves,"NLL")
        
        hCanvas = TCanvas("hCanvas%s%s"%(ratio, nBJetsRegion), "Distribution", 1000,1000)
        
        if not ratio:
                plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
                style=setTDRStyle()
                style.SetPadBottomMargin(0.28)
                style.SetPadLeftMargin(0.13)
                style.SetTitleYOffset(0.9)
                plotPad.UseCurrentStyle()
                plotPad.Draw()  
                plotPad.cd()
                plotPad.SetLogy()       
        else:
                plotPad = ROOT.TPad("plotPad","plotPad",0,0.5,1,1)
                ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.5)
                style=setTDRStyle()
                style.SetPadBottomMargin(0.28)
                style.SetPadLeftMargin(0.13)
                style.SetTitleYOffset(0.9)
                plotPad.UseCurrentStyle()
                ratioPad.UseCurrentStyle()
                
                plotPad.SetTopMargin(0.069)
                plotPad.SetBottomMargin(0.0001)
                ratioPad.SetTopMargin(0)
                ratioPad.SetBottomMargin(0.5)
                
                plotPad.Draw()  
                ratioPad.Draw() 
                plotPad.cd() 
                plotPad.SetLogy()       
        
        
        
        histObs = ROOT.TH1F("histObs%s%s"%(ratio, nBJetsRegion),"histObs",14,0,14)
        
        # histObs.UseCurrentStyle()
        histObs.SetMarkerColor(ROOT.kBlack)
        histObs.SetLineColor(ROOT.kBlack)
        histObs.SetMarkerStyle(20)
        
        
        histPred = ROOT.TH1F("histPred%s%s"%(ratio, nBJetsRegion),"histPred",14,0,14)
        histFlavSym = ROOT.TH1F("histFlavSym%s%s"%(ratio, nBJetsRegion),"histFlavSym",14,0,14)
        histDY = ROOT.TH1F("histDY%s%s"%(ratio, nBJetsRegion),"histDY",14,0,14)
        histRare = ROOT.TH1F("histRare%s%s"%(ratio, nBJetsRegion),"histRare",14,0,14)
        histSignal = ROOT.TH1F("histSignal%s%s"%(ratio, nBJetsRegion),"histSignal",14,0,14)
        
        histRare.SetName("Znu")
        histDY.SetName("DY")
        histFlavSym.SetName("FS")
        histSignal.SetName("Signal")
        histObs.SetName("Data")
        
        if not blind:
                histObs.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_SF"%nBJetsRegion])
                histObs.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_SF"%nBJetsRegion])
                histObs.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_SF"%nBJetsRegion])
                histObs.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_SF"%nBJetsRegion])
                histObs.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_SF"%nBJetsRegion])
                histObs.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_SF"%nBJetsRegion])
                histObs.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_SF"%nBJetsRegion])     
                
                histObs.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_SF"%nBJetsRegion])
                histObs.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_SF"%nBJetsRegion])
                histObs.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_SF"%nBJetsRegion])
                histObs.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_SF"%nBJetsRegion])
                histObs.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_SF"%nBJetsRegion])
                histObs.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_SF"%nBJetsRegion])
                histObs.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_SF"%nBJetsRegion])   
        else:
                for i in range(1, 15):
                        histObs.SetBinContent(i,-100)
        
        
        names = ["\\mathrm{m}_{\\ell\\ell}\\mbox{: 20-60 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 60-86 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 96-150 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 150-200 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 200-300 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 300-400 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: > 400 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 20-60 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 60-86 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 96-150 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 150-200 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 200-300 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: 300-400 GeV}","\\mathrm{m}_{\\ell\\ell}\\mbox{: > 400 GeV}"]
        
        if not ratio:
                for index, name in enumerate(names):
                
                        histObs.GetXaxis().SetBinLabel(index+1,name)
                
        histFlavSym.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_PredSF"%nBJetsRegion])     
        
        histFlavSym.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_PredSF"%nBJetsRegion])   
        
        histDY.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_ZPredSF"%nBJetsRegion]) 
        
        histDY.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_ZPredSF"%nBJetsRegion])       

        histRare.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_RarePredSF"%nBJetsRegion])    
        
        histRare.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_RarePredSF"%nBJetsRegion])  

        errGraph = ROOT.TGraphAsymmErrors()
        errGraphRatio = ROOT.TGraphAsymmErrors()
        graphObs = ROOT.TGraphAsymmErrors()
        
        
        for i in range(1,histFlavSym.GetNbinsX()+1):
                graphObs.SetPoint(i,histObs.GetBinCenter(i),histObs.GetBinContent(i))
                errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
                if ratio:
                        errGraphRatio.SetPoint(i,histFlavSym.GetBinCenter(i),1)
                

        graphObs.SetPointError(1,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_SFDown"%nBJetsRegion],  resultsNLL["lowNLL"]["highMT2_%s_mass20To60_SFUp"%nBJetsRegion])
        graphObs.SetPointError(2,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_SFDown"%nBJetsRegion],  resultsNLL["lowNLL"]["highMT2_%s_mass60To86_SFUp"%nBJetsRegion])
        graphObs.SetPointError(3,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_SFDown"%nBJetsRegion], resultsNLL["lowNLL"]["highMT2_%s_mass96To150_SFUp"%nBJetsRegion])
        graphObs.SetPointError(4,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_SFDown"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass150To200_SFUp"%nBJetsRegion])
        graphObs.SetPointError(5,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_SFDown"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass200To300_SFUp"%nBJetsRegion])
        graphObs.SetPointError(6,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_SFDown"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass300To400_SFUp"%nBJetsRegion])
        graphObs.SetPointError(7,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass400_SFDown"%nBJetsRegion],     resultsNLL["lowNLL"]["highMT2_%s_mass400_SFUp"%nBJetsRegion])

        graphObs.SetPointError(8, 0.5,0.5,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_SFDown"%nBJetsRegion],   resultsNLL["highNLL"]["highMT2_%s_mass20To60_SFUp"%nBJetsRegion])
        graphObs.SetPointError(9, 0.5,0.5,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_SFDown"%nBJetsRegion],   resultsNLL["highNLL"]["highMT2_%s_mass60To86_SFUp"%nBJetsRegion])
        graphObs.SetPointError(10,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass96To150_SFDown"%nBJetsRegion],  resultsNLL["highNLL"]["highMT2_%s_mass96To150_SFUp"%nBJetsRegion])
        graphObs.SetPointError(11,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass150To200_SFDown"%nBJetsRegion], resultsNLL["highNLL"]["highMT2_%s_mass150To200_SFUp"%nBJetsRegion])
        graphObs.SetPointError(12,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass200To300_SFDown"%nBJetsRegion], resultsNLL["highNLL"]["highMT2_%s_mass200To300_SFUp"%nBJetsRegion])
        graphObs.SetPointError(13,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass300To400_SFDown"%nBJetsRegion], resultsNLL["highNLL"]["highMT2_%s_mass300To400_SFUp"%nBJetsRegion])
        graphObs.SetPointError(14,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass400_SFDown"%nBJetsRegion],      resultsNLL["highNLL"]["highMT2_%s_mass400_SFUp"%nBJetsRegion])


        errGraph.SetPointError(1,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass20To60_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(2,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass60To86_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(3,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass96To150_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(4,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass150To200_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(5,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass200To300_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(6,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass300To400_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(7,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass400_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass400_TotalPredErrUpSF"%nBJetsRegion])
        
        errGraph.SetPointError(8,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass20To60_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass20To60_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(9,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass60To86_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass60To86_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(10,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass96To150_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass96To150_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(11,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass150To200_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass150To200_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(12,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass200To300_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass200To300_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(13,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass300To400_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass300To400_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(14,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass400_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass400_TotalPredErrUpSF"%nBJetsRegion])

        if ratio:
                errGraphRatio.SetPointError(1,0.5*histFlavSym.GetBinWidth(1),0.5*histFlavSym.GetBinWidth(1),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredSF"])
                errGraphRatio.SetPointError(2,0.5*histFlavSym.GetBinWidth(2),0.5*histFlavSym.GetBinWidth(2),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredSF"])
                errGraphRatio.SetPointError(3,0.5*histFlavSym.GetBinWidth(4),0.5*histFlavSym.GetBinWidth(4),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredSF"])
                errGraphRatio.SetPointError(4,0.5*histFlavSym.GetBinWidth(5),0.5*histFlavSym.GetBinWidth(5),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredSF"])
                errGraphRatio.SetPointError(5,0.5*histFlavSym.GetBinWidth(6),0.5*histFlavSym.GetBinWidth(6),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredSF"])
                errGraphRatio.SetPointError(6,0.5*histFlavSym.GetBinWidth(7),0.5*histFlavSym.GetBinWidth(7),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredSF"])
                errGraphRatio.SetPointError(7,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredSF"])
                
                errGraphRatio.SetPointError(8,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredSF"])
                errGraphRatio.SetPointError(9,0.5*histFlavSym.GetBinWidth(9),0.5*histFlavSym.GetBinWidth(9),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredSF"])
                errGraphRatio.SetPointError(10,0.5*histFlavSym.GetBinWidth(10),0.5*histFlavSym.GetBinWidth(10),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredSF"])
                errGraphRatio.SetPointError(11,0.5*histFlavSym.GetBinWidth(11),0.5*histFlavSym.GetBinWidth(11),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredSF"])
                errGraphRatio.SetPointError(12,0.5*histFlavSym.GetBinWidth(12),0.5*histFlavSym.GetBinWidth(12),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredSF"])
                errGraphRatio.SetPointError(13,0.5*histFlavSym.GetBinWidth(13),0.5*histFlavSym.GetBinWidth(13),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredSF"])
                errGraphRatio.SetPointError(14,0.5*histFlavSym.GetBinWidth(14),0.5*histFlavSym.GetBinWidth(14),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredSF"])
        
        if nBJetsRegion == "zeroBJets":
                histSignal.SetBinContent(1,0.0639051627368)
                histSignal.SetBinContent(2,0.0640199345071)
                histSignal.SetBinContent(3,0.197323031709)
                histSignal.SetBinContent(4,0.222303471179)
                histSignal.SetBinContent(5,0.398917620711)
                histSignal.SetBinContent(6,0.0122580226162)
                histSignal.SetBinContent(7,0.00956270564348)
                
                histSignal.SetBinContent(8, 0.309321277309)
                histSignal.SetBinContent(9, 0.408749736613)
                histSignal.SetBinContent(10,1.18957425369)
                histSignal.SetBinContent(11,1.37581009429)
                histSignal.SetBinContent(12,2.75781275448)
                histSignal.SetBinContent(13,0.0)
                histSignal.SetBinContent(14,0.00395664619282)
        else:
                histSignal.SetBinContent(1,0.10120509511)
                histSignal.SetBinContent(2,0.138121711207)
                histSignal.SetBinContent(3,0.402074781392)
                histSignal.SetBinContent(4,0.382404221149)
                histSignal.SetBinContent(5,0.641636372602)
                histSignal.SetBinContent(6,0.0172456565779)
                histSignal.SetBinContent(7,0.00326249026693)
                
                histSignal.SetBinContent(8, 0.882021330472)
                histSignal.SetBinContent(9, 1.15418216883)
                histSignal.SetBinContent(10,3.48486203054)
                histSignal.SetBinContent(11,4.00152865014)
                histSignal.SetBinContent(12,8.46935899404)
                histSignal.SetBinContent(13,0.0469235587079)
                histSignal.SetBinContent(14,0.00361995585263)
        
        

        errGraph.SetFillColor(ROOT.kGray+3)     
        errGraph.SetFillStyle(3644)     
        errGraphRatio.SetFillColor(ROOT.kGray+3)     
        errGraphRatio.SetFillStyle(3644)   
        #errGraph.SetLineStyle(3644)     
        histFlavSym.SetLineColor(ROOT.kBlack)
        histFlavSym.SetFillColor(ROOT.kGray+1)    
        histDY.SetFillColor(ROOT.kGreen+2)  
        # histDY.SetFillColor(30)  
        histRare.SetFillColor(ROOT.kBlue-7)
        # histRare.SetFillColor(40)
        histDY.SetLineColor(ROOT.kBlack)
        histRare.SetLineColor(ROOT.kBlack)
        histSignal.SetLineColor(ROOT.kRed)
        histSignal.SetLineWidth(4)
        histSignal.SetLineStyle(2)
        from ROOT import THStack
        
        stack = THStack()
        stack.Add(histDY)       
        stack.Add(histRare)     
        stack.Add(histFlavSym)  
        
        histObs.GetYaxis().SetRangeUser(0.5,2000000)
        histObs.GetYaxis().SetTitle("Events")
        histObs.SetTitleOffset(0.7, "Y")
        
        histObs.GetYaxis().SetTitleSize(0.07)
        if ratio:
                histObs.GetXaxis().SetLabelSize(0)
                histObs.GetXaxis().SetTitleSize(0)
        #histObs.LabelsOption("v")
        
        
   
        histObs.Draw("pe")

        
        
        #~ hCanvas.DrawFrame(-0.5,0,30.5,65,"; %s ; %s" %("","Events"))
        
        latex = ROOT.TLatex()
        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(0.06)
        latex.SetNDC(True)
        latexCMS = ROOT.TLatex()
        latexCMS.SetTextFont(61)
        latexCMS.SetTextAlign(13)
        latexCMS.SetTextSize(0.105)
        latexCMS.SetNDC(True)
        latexCMSExtra = ROOT.TLatex()
        latexCMSExtra.SetTextFont(52)
        # latexCMSExtra.SetTextAlign(13)
        latexCMSExtra.SetTextSize(0.045)
        latexCMSExtra.SetNDC(True)              
        


        intlumi = ROOT.TLatex()
        intlumi.SetTextAlign(12)
        intlumi.SetTextSize(0.03)
        intlumi.SetNDC(True)            

        latex.DrawLatex(0.95, 0.945, "%s fb^{-1} (13 TeV)"%"137")
        
        # cmsExtra = "Preliminary"
        cmsExtra = ""
        latexCMS.DrawLatex(0.16,0.901,"CMS")
        if "Simulation" in cmsExtra:
                yLabelPos = 0.81        
        else:
                yLabelPos = 0.84        

        latexCMSExtra.DrawLatex(0.17,yLabelPos,"%s"%(cmsExtra))
        leg = ROOT.TLegend(0.31, 0.64, 0.91, 0.92,"","brNDC")
        leg.SetNColumns(3)
        leg.SetFillColor(10)
        leg.SetLineColor(10)
        leg.SetShadowColor(0)
        leg.SetBorderSize(1)
        leg.SetTextSize(0.06)
        
        bkgHistForLegend = histFlavSym.Clone("bkgHistForLegend")
        bkgHistForLegend.SetLineColor(ROOT.kBlack)
        bkgHistForLegend.SetFillColor(ROOT.kGray+1)
        bkgHistForLegend.SetLineWidth(1)
        
        obsGraph = ROOT.TGraphAsymmErrors()
        leg.AddEntry(obsGraph,"Observed","pe")
        leg.AddEntry(histDY,"DY+jets", "f")
        #~ leg.AddEntry(histFlavSym, "Total backgrounds","l")
        leg.AddEntry(bkgHistForLegend, "Flavor-symmetric","f")
        leg.AddEntry(errGraph,"Tot. unc.", "f") 
        leg.AddEntry(histRare,"Z+#nu", "f")
        if signal:
                leg.AddEntry(histSignal,"Signal (1250, 400)", "l")
        
        
        stack.Draw("samehist")  
        errGraph.Draw("same02")
        
        if signal:
                histSignal.Draw("histsame")
        
        graphObs.Draw("pesame")
        
        leg.Draw("same")

        
        
        line1 = ROOT.TLine(7,0,7,500)
        line1.SetLineColor(ROOT.kBlack)
        line1.SetLineWidth(2)
        line1.Draw("same")


        label = ROOT.TLatex()
        label.SetTextAlign(12)
        label.SetTextSize(0.06)
        label.SetTextColor(ROOT.kBlack) 
        label.SetTextAlign(22)  
        #~ label.SetTextAngle(-45)      
        
        label.DrawLatex(3.5,2000,"t#bar{t}-like")
        label.DrawLatex(10.5,2000,"non-t#bar{t}-like")
        label.SetTextSize(0.08)
        label.SetNDC(True)
        label.SetTextAlign(32) 
        if nBJetsRegion == "oneOrMoreBJets":
                label.DrawLatex(0.9,0.61,"\\mathrm{n}_{\\mathrm{b}} \\geq 1")
        else:
                label.DrawLatex(0.9,0.61,"\\mathrm{n}_{\\mathrm{b}} = 0")

        # plotPad.RedrawAxis()
        
        # ratios
        if ratio:
                ratioPad.cd()

                xs = []
                ys = []
                yErrorsUp = []
                yErrorsDown = []
                widths = []
                
                for i in range(0,histObs.GetNbinsX()+1):
                        xs.append(histObs.GetBinCenter(i))
                        widths.append(0.5*histObs.GetBinWidth(i)) 
                        predI = histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i)              
                        if predI > 0:
                                ys.append(histObs.GetBinContent(i)/predI)
                                yErrorsUp.append(graphObs.GetErrorYhigh(i)/predI)                 
                                yErrorsDown.append(graphObs.GetErrorYlow(i)/predI)                                
                        else:
                                ys.append(10.)
                                yErrorsUp.append(0)                     
                                yErrorsDown.append(0)
                
                ratioPad.cd()

                        # axis
                nBinsX = 14
                nBinsY = 10
                hAxis = ROOT.TH2F("hAxis", "", nBinsX, 0, 14, nBinsY, 0, 2.2)
                hAxis.Draw("AXIS")
                
                
                hAxis.GetXaxis().SetLabelSize(0.09)

                for index, name in enumerate(names):
                        hAxis.GetXaxis().SetBinLabel(index+1,name)   
                        hAxis.GetXaxis().ChangeLabel(index+1,270)   
                hAxis.GetXaxis().LabelsOption("v")
                
                hAxis.GetYaxis().CenterTitle()
                hAxis.GetYaxis().SetNdivisions(408)
                hAxis.SetTitleOffset(0.7, "Y")
                #hAxis.SetTitleSize(0.08, "Y")
                hAxis.GetYaxis().SetTitleSize(0.08)
                hAxis.GetYaxis().SetTitle("#frac{Observed}{Prediction}    ")
                hAxis.GetYaxis().SetLabelSize(0.06)

                oneLine = ROOT.TLine(0, 1.0, 14, 1.0)
                #~ oneLine.SetLineStyle(2)
                oneLine.Draw()
                oneLine2 = ROOT.TLine(0, 0.5, 14, 0.5)
                oneLine2.SetLineStyle(2)
                oneLine2.Draw()
                oneLine3 = ROOT.TLine(0, 1.5, 14, 1.5)
                oneLine3.SetLineStyle(2)
                oneLine3.Draw()
                
                errGraphRatio.Draw("same02")
                
                ratioGraph = ROOT.TGraphAsymmErrors(len(xs), array("d", xs), array("d", ys), array("d", widths), array("d", widths), array("d", yErrorsDown), array("d", yErrorsUp))
                        
                ratioGraph.Draw("same pe0")     
                
                line2 = ROOT.TLine(7,0,7,2.2)
                line2.SetLineColor(ROOT.kBlack)
                line2.SetLineWidth(2)
                line2.Draw("same")

        
                ROOT.gPad.RedrawAxis()
                plotPad.RedrawAxis()
                ratioPad.RedrawAxis()
        
        
        fn = "edgeOverview_%s.eps"%(nBJetsRegion)
        hCanvas.Print(fn)
        # hCanvas.Print("root/"+fn.replace("eps","root"))
        import os
        from locations import locations
        os.system("sed -i 's/STIX/STIXX/' %s"%(fn))
        os.system("%s %s"%(locations.epsToPdfPath, fn))
        os.remove(fn)
        
        # convert to useful root file 
        
        GraphObs = ROOT.TGraphAsymmErrors()
        GraphZNu = ROOT.TGraphAsymmErrors()
        GraphDY = ROOT.TGraphAsymmErrors()
        GraphFS = ROOT.TGraphAsymmErrors()
        GraphTot = errGraph.Clone()
        
        GraphObs.SetName("observed")
        GraphZNu.SetName("znu")
        GraphDY.SetName("dyjets")
        GraphFS.SetName("flavor symmetric")
        GraphTot.SetName("total prediction")

        for i in range(1, 15):
                GraphObs.SetPoint(i,  histObs.GetXaxis().GetBinCenter(i), histObs.GetBinContent(i))
                GraphZNu.SetPoint(i,  histObs.GetXaxis().GetBinCenter(i), histRare.GetBinContent(i))
                GraphDY.SetPoint(i,  histObs.GetXaxis().GetBinCenter(i), histDY.GetBinContent(i))
                GraphFS.SetPoint(i,  histObs.GetXaxis().GetBinCenter(i), histFlavSym.GetBinContent(i))
                binWidth = 0.5*histObs.GetBinWidth(i)
                GraphObs.SetPointError(i, binWidth, binWidth, 0,0)
        
        GraphFS.SetPointError(1,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_PredFSDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass20To60_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(2,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_PredFSDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass60To86_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(3,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_PredFSDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass96To150_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(4,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_PredFSDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass150To200_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(5,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_PredFSDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass200To300_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(6,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_PredFSDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass300To400_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(7,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass400_PredFSDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass400_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(8,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass20To60_PredFSDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass20To60_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(9,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass60To86_PredFSDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass60To86_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(10,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass96To150_PredFSDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass96To150_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(11,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass150To200_PredFSDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass150To200_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(12,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass200To300_PredFSDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass200To300_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(13,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass300To400_PredFSDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass300To400_PredFSUpSF"%nBJetsRegion])
        GraphFS.SetPointError(14,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass400_PredFSDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass400_PredFSUpSF"%nBJetsRegion])

        GraphDY.SetPointError(1,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_ZPredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass20To60_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(2,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_ZPredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass60To86_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(3,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_ZPredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass96To150_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(4,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_ZPredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass150To200_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(5,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_ZPredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass200To300_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(6,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_ZPredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass300To400_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(7,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass400_ZPredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass400_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(8,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass20To60_ZPredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass20To60_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(9,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass60To86_ZPredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass60To86_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(10,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass96To150_ZPredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass96To150_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(11,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass150To200_ZPredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass150To200_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(12,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass200To300_ZPredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass200To300_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(13,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass300To400_ZPredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass300To400_ZPredErrSF"%nBJetsRegion])
        GraphDY.SetPointError(14,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass400_ZPredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass400_ZPredErrSF"%nBJetsRegion])

        GraphZNu.SetPointError(1,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_RarePredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass20To60_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(2,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_RarePredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass60To86_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(3,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_RarePredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass96To150_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(4,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_RarePredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass150To200_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(5,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_RarePredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass200To300_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(6,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_RarePredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass300To400_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(7,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass400_RarePredErrSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass400_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(8,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass20To60_RarePredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass20To60_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(9,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass60To86_RarePredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass60To86_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(10,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass96To150_RarePredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass96To150_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(11,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass150To200_RarePredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass150To200_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(12,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass200To300_RarePredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass200To300_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(13,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass300To400_RarePredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass300To400_RarePredErrSF"%nBJetsRegion])
        GraphZNu.SetPointError(14,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass400_RarePredErrSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass400_RarePredErrSF"%nBJetsRegion])

        rootFile = ROOT.TFile("root/%s.root"%nBJetsRegion, "RECREATE")
        
        rootFile.mkdir(nBJetsRegion)
        rootFile.cd(nBJetsRegion)
        GraphObs.Write()
        GraphZNu.Write()
        GraphDY.Write()
        GraphFS.Write() 
        GraphTot.Write()
        rootFile.Close()

                
def makeOverviewPlotOnZ(region):

        #from helpers import createMyColors
        #from defs import myColors
        #colors = createMyColors()               
        ROOT.gROOT.SetBatch(True)
        binningSRA = [50,100,150,230,300,600]
        binningSRB = [50,100,150,250,600]
        binningSRC = [50,100,150,250,600]
        binningSRVZBoosted = [50,100,200,300,400,500,600]
        binningSRVZResolved =[50,100,150,250,350,600]
        binningSRHZ =[50,100,150,250,600]
        binningSlepton =[100,150,225,300,400]
        
        if "SRA" in region or "SRB" in region or "VRA" in region or "VRB" in region:
                binning = binningSRA
        elif "SRC" in region or "VRC" in region:
                binning = binningSRC
        elif "SRVZBoosted" in region or "VRWZBoosted" in region:
                binning = binningSRVZBoosted
        elif "SRVZResolved" in region or "VRWZResolved" in region:
                binning = binningSRVZResolved
        elif "SRHZ" in region or "VRHZ" in region:
                binning = binningSRHZ
        elif "Slepton" in region:
                binning = binningSlepton
        
        histObs = ROOT.TH1F("histObs","histObs",len(binning)-1, array("f", binning))
        histPred = ROOT.TH1F("histPred","histPred",len(binning)-1, array("f", binning))
        histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",len(binning)-1, array("f", binning))
        histDY = ROOT.TH1F("histDY","histDY",len(binning)-1, array("f", binning))
        histRare = ROOT.TH1F("histRare","histRare",len(binning)-1, array("f", binning))
        histSignal = ROOT.TH1F("histSignal","histSignal",len(binning)-1, array("f", binning))
        hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
        # hCanvas.SetGrayscale(True)

        histObs.SetMarkerColor(ROOT.kBlack)
        histObs.SetLineColor(ROOT.kBlack)
        histObs.SetMarkerStyle(20)
        
          
        plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
        ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
        
        style = setTDRStyle()
        style.SetPadLeftMargin(0.13)
        style.SetTitleYOffset(0.9)
        style.SetPadTopMargin(0.0675)
        ROOT.gStyle.SetOptStat(0)
        plotPad.UseCurrentStyle()
        ratioPad.UseCurrentStyle()
        plotPad.Draw()  
        ratioPad.Draw() 
        plotPad.cd()
        plotPad.SetLogy() 
        
        
        obs = {}
        obs["SRA"] = [1261, 186, 27, 5, 14]
        obs["SRAb"] = [616, 148, 42, 10, 4]
        obs["SRB"] = [700, 108, 18, 2, 3]
        obs["SRBb"] = [225, 69, 17, 3, 5]
        obs["SRC"] = [135, 19, 5, 1]
        obs["SRCb"] = [41, 14, 5, 1]
        
        obs["SRVZBoosted"] = [43, 5, 1, 0, 0, 0]
        obs["SRVZResolved"] = [3648, 461, 69, 7, 2]
        obs["SRHZ"] = [168, 14, 5, 0]
        
        obs["SRSleptonNoJetOffZ"] = [228, 99, 29, 17]
        obs["SRSleptonNoJetOnZ"] = [1059, 573, 116, 47]
        obs["SRSleptonOneJetOffZ"] = [283, 97, 19, 8]
        obs["SRSleptonOneJetOnZ"] = [674,241,72,30]
        
        obs["VRA"] = [5734, 1068, 236, 33.0, 19]
        obs["VRB"] = [1713, 414, 87, 12, 5]
        obs["VRC"] = [177, 48, 6, 2]
        
        obs["VRWZBoosted"]      = [16,7,0,0,0,0]
        obs["VRWZResolved"]     = [5021, 590, 68, 2, 1]
        obs["VRHZ"]             = [76, 7, 2, 0]
        
        for i in range(1, len(obs[region])+1):
                histObs.SetBinContent(i, obs[region][i-1])
        
        
        flavSym = {}
        flavSym["SRA"]          = [1.6,2.1,1.4,0.6,0.6]
        flavSym["SRAb"]         = [7.9,19.7,10.6,1.4,0.3]
        flavSym["SRB"]          = [1.2,2.4,1.0,0.6,0.1]
        flavSym["SRBb"]         = [4.5,9.3,5.3,1.0,0.1]
        flavSym["SRC"]          = [0.2,0.3,0.2,0.0]
        flavSym["SRCb"]         = [0.4,0.7,0.8,0.1]
        
        flavSym["SRVZBoosted"]  = [0.17,0.30,0.18,0.12,0.00,0.06] 
        flavSym["SRVZResolved"] = [10.7,15.4,5.1,0.5,0.3]
        flavSym["SRHZ"]         = [3.9,3.6,3.3,0.7]
        
        flavSym["SRSleptonNoJetOffZ"]   = [134.1, 82.5, 11.6, 4.2]
        flavSym["SRSleptonNoJetOnZ"]    = [97.9, 40.0, 2.0, 1.0]
        flavSym["SRSleptonOneJetOffZ"]  = [202.7, 94.8, 8.4, 5.2]
        flavSym["SRSleptonOneJetOnZ"]   = [85.4, 15.7, 1.1, 0.0]
        
        flavSym["VRA"]          = [13.1, 19.3, 11.0, 2.2, 1.0]
        flavSym["VRB"]          = [13.9, 15.7, 6.4, 1.0, 0.5]
        flavSym["VRC"]          = [0.4, 0.8, 0.7, 0.2]
        
        flavSym["VRWZBoosted"]  = [0.0, 0.0, 0.001, 0.001, 0.001, 0.001]
        flavSym["VRWZResolved"] = [6.3, 3.8, 0.6, 0.1, 0.1]
        flavSym["VRHZ"]         = [0.8, 0.4, 0.2, 0.0 ]
        
        for i in range(1, len(flavSym[region])+1):
                histFlavSym.SetBinContent(i, flavSym[region][i-1])
        
        
        dy = {}
        dy["SRA"]          = [1253.0,153.3,22.0,0.9,2.9]
        dy["SRAb"]         = [602.2,99.9,12.3,2.2,1.1]
        dy["SRB"]          = [696.2,103.6,11.2,0.6,1.0]
        dy["SRBb"]         = [214.5,48.0,10.7,1.9,0.4]
        dy["SRC"]          = [134.5,28.8,1.7,0.2]
        dy["SRCb"]         = [39.6,8.9,2.0,0.0]
        
        dy["SRVZBoosted"]  = [42.7,1.57,0.0,0.0,0.0,0.0]
        dy["SRVZResolved"] = [3613.3,393.6,20.5,1.7,1.8]
        dy["SRHZ"]         = [162.8,10.8,1.3,0.1]
        
        dy["SRSleptonNoJetOffZ"]   = [37.5, 11.2, 1.4, 0.0]
        dy["SRSleptonNoJetOnZ"]    = [457.8, 137.3, 17.5, 0.0]
        dy["SRSleptonOneJetOffZ"]  = [32.9, 5.4, 1.7, 0.0]
        dy["SRSleptonOneJetOnZ"]   = [402.1, 66.6, 21.1, 0.0]
        
        dy["VRA"]          = [5706.5, 1055.4, 200.6, 28.3, 15.2]
        dy["VRB"]          = [1690.8, 350.1, 68.2, 9.0, 4.3]
        dy["VRC"]          = [175.4, 51.5, 9.1, 1.5]
        dy["VRWZBoosted"]  = [15.99, 2.59, 0.0, 0.0, 0.0, 0.0]
        dy["VRWZResolved"] = [5000.4, 528.2, 43.2, 2.9, 0.2]
        dy["VRHZ"]         = [74.8, 8.1, 0.7, 0.1]
        
        for i in range(1, len(dy[region])+1):
                histDY.SetBinContent(i, dy[region][i-1])
        
        
        rare = {}
        rare["SRA"]          = [6.4,4.9,5.3,2.7,6.2]
        rare["SRAb"]         = [5.8,8.1,8.4,2.8,2.6]
        rare["SRB"]          = [2.6,2.3,3.5,0.9,1.9]
        rare["SRBb"]         = [6.0,7.9,6.6,2.4,1.6]
        rare["SRC"]          = [0.4,0.6,0.5,0.4]
        rare["SRCb"]         = [1.0,1.0,1.0,0.6]
        
        rare["SRVZBoosted"]  = [0.15,0.40,0.35,0.03,0.04,0.14]
        rare["SRVZResolved"] = [24.0,29.5,32.2,9.7,4.2]
        rare["SRHZ"]         = [1.3,1.1,1.0,0.3]
        
        rare["SRSleptonNoJetOffZ"]   = [26.6, 26.2, 7.8, 5.1]
        rare["SRSleptonNoJetOnZ"]    = [503.4, 395.7, 96.4, 46.4]
        rare["SRSleptonOneJetOffZ"]  = [9.9, 11.3, 4.6, 3.5]
        rare["SRSleptonOneJetOnZ"]   = [186.5, 158.7, 49.8, 34.9]
        
        rare["VRA"]          = [14.4, 11.8, 9.7, 4.3, 5.1]
        rare["VRB"]          = [8.4, 6.2, 5.1, 2.2, 1.7]
        rare["VRC"]          = [1.2, 1.2, 0.9, 0.3]
        rare["VRWZBoosted"]  = [0.01, 0.03, 0.02, 0.0, 0.0, 0.0]
        rare["VRWZResolved"] = [14.3, 9.4, 7.4, 1.1, 0.5]
        rare["VRHZ"]         = [0.4, 0.3, 0.3, 0.1]
        
        for i in range(1, len(rare[region])+1):
                histRare.SetBinContent(i, rare[region][i-1])
        
        errUp = {}
        errUp["SRA"]          = [40.5,16.4,5.0,1.0,3.2]
        errUp["SRAb"]         = [27.7,10.4,3.8,1.7,1.2]
        errUp["SRB"]          = [30.8,7.1,2.3,0.7,1.0]
        errUp["SRBb"]         = [16.1,15.8,4.2,1.4,0.6]
        errUp["SRC"]          = [14.4,5.6,0.6,0.3]
        errUp["SRCb"]         = [7.1,2.1,0.9,0.2]
        
        errUp["SRVZBoosted"]  = [9.9,0.84,0.49,0.16,0.07,0.15]
        errUp["SRVZResolved"] = [80.3,46.9,19.1,3.2,2.2]
        errUp["SRHZ"]         = [15.2,4.3,2.8,0.4]
        
        errUp["SRSleptonNoJetOffZ"]   = [37.0, 16.7, 4.1, 2.3]
        errUp["SRSleptonNoJetOnZ"]    = [34.0, 26.0, 10.8, 5.3]
        errUp["SRSleptonOneJetOffZ"]  = [32.9, 12.0, 3.3, 2.3]
        errUp["SRSleptonOneJetOnZ"]   = [29.0, 15.8, 8.2, 3.8]
        
        errUp["VRA"]          = [88.0,75.2,21.7,5.6,4.3]
        errUp["VRB"]          = [49.0, 28.0, 6.2, 2.3, 1.3]
        errUp["VRC"]          = [16.2, 6.5, 1.8, 0.9]
        
        errUp["VRWZBoosted"]  = [4.54, 1.08, 0.07, 0.06, 0.06, 0.06]
        errUp["VRWZResolved"] = [94.2, 118.2, 5.7, 0.9, 0.5]
        errUp["VRHZ"]         = [9.5, 3.2, 0.4, 0.2]
        
        
        errDn = {}
        errDn["SRA"]          = [40.5,16.4,5.0,1.0,3.2]
        errDn["SRAb"]         = [27.7,10.4,3.8,1.7,1.2]
        errDn["SRB"]          = [30.8,7.1,2.3,0.7,1.0]
        errDn["SRBb"]         = [16.1,15.8,4.2,1.4,0.6]
        errDn["SRC"]          = [14.4,5.6,0.6,0.3]
        errDn["SRCb"]         = [7.1,2.1,0.9,0.2]
        
        errDn["SRVZBoosted"]  = [9.9,0.83,0.48,0.11,0.02,0.09]
        errDn["SRVZResolved"] = [80.3,46.9,19.1,3.2,2.2]
        errDn["SRHZ"]         = [15.2,4.3,2.8,0.4]
        
        errDn["SRSleptonNoJetOffZ"]   = [37.0, 16.7, 4.1, 2.3]
        errDn["SRSleptonNoJetOnZ"]    = [34.0, 26.0, 10.8, 5.3]
        errDn["SRSleptonOneJetOffZ"]  = [32.9, 12.0, 3.3, 2.3]
        errDn["SRSleptonOneJetOnZ"]   = [29.0, 15.8, 8.2, 3.8]
        
        errDn["VRA"]          = [88.0,75.2,21.7,5.6,4.3]
        errDn["VRB"]          = [49.0, 28.0, 6.2, 2.3, 1.3]
        errDn["VRC"]          = [16.2, 6.5, 1.8, 0.9]
        
        errDn["VRWZBoosted"]  = [4.54, 1.08, 0.03, 0.1, 0.001, 0.001]
        errDn["VRWZResolved"] = [94.2, 118.2, 5.8, 0.9, 0.4]
        errDn["VRHZ"]         = [9.5, 3.2, 0.4, 0.2]
        
        # signal
        
        signal = {}
        signal["SRA"]          = [0.0071935, 0.016909095, 0.07875599999999999, 0.0367012, 0.8305945]
        signal["SRAb"]         = [0.002134055, 0.00871634, 0.04859025, 0.05038625, 0.40707099999999996]
        signal["SRB"]          = [0.11352024999999999, 0.14377800000000002, 0.44949649999999997, 0.6174265, 6.767995]
        signal["SRBb"]         = [0.08117250000000001, 0.1578915, 0.47539549999999997, 0.5763495000000001, 5.66821]
        signal["SRC"]          = [0.15294750000000001, 0.347351, 0.9920385, 10.0676]
        signal["SRCb"]         = [0.1397876, 0.4040675, 1.231535, 12.576450000000001]

        signal["SRVZBoosted"]  = [0.235,0.508,0.405,0.243,0.084,0.0298]
        signal["SRVZResolved"] = [3.3675100000000002, 7.008025, 19.749000000000002, 7.671749999999999, 1.20851]
        signal["SRHZ"]         = [0.2547025, 0.378694, 1.060945, 3.00948]
        
        signal["SRSleptonNoJetOffZ"]   = [0.58, 1.89,  2.53, 13.75]
        signal["SRSleptonNoJetOnZ"]    = [0.01, 0.02,  0.03, 0.33]
        signal["SRSleptonOneJetOffZ"]  = [0.51, 1.58, 2.29, 12.60]
        signal["SRSleptonOneJetOnZ"]   = [0.01, 0.01, 0.02, 0.22]
        
        if region in signal:
                for i in range(1, len(rare[region])+1):
                        histSignal.SetBinContent(i, signal[region][i-1])
        
        signalName = {}
        signalName["SRA"]          = "Signal (1600, 700)"
        signalName["SRAb"]         = "Signal (1600, 700)"
        signalName["SRB"]          = "Signal (1600, 700)"
        signalName["SRBb"]         = "Signal (1600, 700)"
        signalName["SRC"]          = "Signal (1600, 700)"
        signalName["SRCb"]         = "Signal (1600, 700)"
        signalName["SRVZBoosted"]  = "Signal (400, 200)"
        signalName["SRVZResolved"] = "Signal (400, 200)"
        signalName["SRHZ"]         = "Signal (500)"
        
        signalName["SRSleptonNoJetOffZ"]   = "Signal (600, 0)"
        signalName["SRSleptonNoJetOnZ"]    = "Signal (600, 0)"
        signalName["SRSleptonOneJetOffZ"]  = "Signal (600, 0)"
        signalName["SRSleptonOneJetOnZ"]   = "Signal (600, 0)"
        
        errGraph = ROOT.TGraphAsymmErrors()
        errGraphRatio = ROOT.TGraphAsymmErrors()
        graphObs = ROOT.TGraphAsymmErrors()
        
        
        for i in range(1,histFlavSym.GetNbinsX()+1):
                graphObs.SetPoint(i,histObs.GetBinCenter(i),histObs.GetBinContent(i))
                errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
                        
        
        for i in range(1,histFlavSym.GetNbinsX()+1):
                graphObs.SetPoint(i,histObs.GetBinCenter(i),histObs.GetBinContent(i))
                errGraph.SetPoint(i,histObs.GetBinCenter(i),histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
                
                yield_up = ctypes.c_double(1.)
                yield_down = ctypes.c_double(1.)
                ROOT.RooHistError.instance().getPoissonInterval(int(histObs.GetBinContent(i)),yield_down,yield_up,1.)
                width = histObs.GetBinWidth(i)/2
                graphObs.SetPointError(i,width,width,int(histObs.GetBinContent(i))-yield_down.value,yield_up.value-int(histObs.GetBinContent(i)))
                
                errGraphRatio.SetPoint(i,histFlavSym.GetBinCenter(i),1)
                
                
                
        for i in range(1,len(errUp[region])+1):
                errGraph.SetPointError(i,histObs.GetBinWidth(i)/2,histObs.GetBinWidth(i)/2,errDn[region][i-1],errUp[region][i-1])
                pred = histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i)
                errGraphRatio.SetPointError(i,histObs.GetBinWidth(i)/2,histObs.GetBinWidth(i)/2,errDn[region][i-1]/pred, errUp[region][i-1]/pred)
        
        errGraph.SetFillColor(ROOT.kGray+3)     
        errGraph.SetFillStyle(3644)     
        errGraphRatio.SetFillColor(ROOT.kGray+3)     
        errGraphRatio.SetFillStyle(3644)     
        histFlavSym.SetLineColor(ROOT.kBlack)
        histFlavSym.SetFillColor(ROOT.kGray+1)    
        histDY.SetFillColor(ROOT.kGreen+2)  
        # histDY.SetFillColor(30)  
        histRare.SetFillColor(ROOT.kBlue-7)
        # histRare.SetFillColor(40)
        histDY.SetLineColor(ROOT.kBlack)
        histRare.SetLineColor(ROOT.kBlack)
        histSignal.SetLineColor(ROOT.kRed)
        histSignal.SetLineWidth(4)
        histSignal.SetLineStyle(2)
        
        histSignal.SetName("Signal")
        histRare.SetName("Znu")
        histDY.SetName("DY")
        histFlavSym.SetName("FS")
        histObs.SetName("Data")

        from ROOT import THStack
        
        stack = THStack()
        if "Slepton" in region:
                stack.Add(histRare)     
                stack.Add(histDY)  
                stack.Add(histFlavSym)
        else:
                stack.Add(histFlavSym)
                stack.Add(histRare)     
                stack.Add(histDY)  

        if "Slepton" in region:
                histObs.GetYaxis().SetRangeUser(0.9,1e5)
        else:
                histObs.GetYaxis().SetRangeUser(0.02,1e5)
        histObs.GetYaxis().SetTitle("Events")
        histObs.GetXaxis().SetTitle("p_{T}^{miss} [GeV]")
        histObs.LabelsOption("v")

        histObs.UseCurrentStyle()
        histObs.Draw("pe")
        
        # for h in stack.GetHists():
                # print h.GetName()
        # exit()
        
        latex = ROOT.TLatex()
        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(0.055)
        latex.SetNDC(True)
        latexCMS = ROOT.TLatex()
        latexCMS.SetTextFont(61)
        latexCMS.SetTextAlign(13)
        latexCMS.SetTextSize(0.08)
        latexCMS.SetNDC(True)
        latexCMSExtra = ROOT.TLatex()
        latexCMSExtra.SetTextFont(52)
        #latexCMSExtra.SetTextAlign(31)
        latexCMSExtra.SetTextSize(0.045)
        latexCMSExtra.SetNDC(True)
        latexArxive = ROOT.TLatex()
        latexArxive.SetTextFont(42)
        latexArxive.SetTextSize(0.04)
        latexArxive.SetNDC(True)        
        


        intlumi = ROOT.TLatex()
        intlumi.SetTextAlign(12)
        intlumi.SetTextSize(0.03)
        intlumi.SetNDC(True)            

        latex.DrawLatex(0.95, 0.9475, "%s fb^{-1} (13 TeV)"%"137")
        
        #~ cmsExtra = "Preliminary"
        cmsExtra = ""
        # cmsExtra = "Preliminary"
        latexCMS.DrawLatex(0.15,0.9125,"CMS")
        latexCMSExtra.DrawLatex(0.17,0.82,"%s"%(cmsExtra))
        
        #if useEWRegions:
                #latexCMSExtra.DrawLatex(0.24,0.88,"%s"%(cmsExtra))
        #else:
                #latexCMSExtra.DrawLatex(0.255,0.88,"%s"%(cmsExtra))
        #latexArxive.DrawLatex(0.16,0.83,"arxiv:1709.08908")

        leg = ROOT.TLegend(0.32, 0.66, 0.92, 0.905, "","brNDC")
        leg.SetNColumns(2)
        leg.SetFillColor(10)
        leg.SetLineColor(10)
        leg.SetShadowColor(0)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.SetTextSize(0.056)
        
        obsGraph = ROOT.TGraphAsymmErrors()
        leg.AddEntry(obsGraph,"Observed","pe")
        leg.AddEntry(histDY,"DY+jets", "f")
        leg.AddEntry(histFlavSym, "Flavor-symmetric","f")
        leg.AddEntry(histRare,"Z+#nu", "f")
        if region in signal:
                leg.AddEntry(histSignal,signalName[region], "l")
        leg.AddEntry(errGraph,"Tot. unc.", "f") 
        
        
        
        

        stack.Draw("samehist")
        errGraph.Draw("same02")
        
        if region in signal:
                histSignal.Draw("samehist")
        
        graphObs.Draw("pesame")
        
        leg.Draw("same")
        
        if "SRHZ" in region:
                labelHZ = ROOT.TLatex()
                labelHZ.SetTextAlign(32)
                labelHZ.SetTextSize(0.045)
                labelHZ.SetTextColor(ROOT.kBlack) 
                labelHZ.SetNDC(True)
                labelHZ.DrawLatex(0.59,0.65,"m#kern[0.1]{_{#lower[-0.12]{#tilde{G}}}} = 1 GeV")
                
        

        label = ROOT.TLatex()
        label.SetTextAlign(32)
        label.SetTextSize(0.06)
        label.SetTextColor(ROOT.kBlack)  
        #~ label.SetTextAngle(-45)      
        label.SetNDC(True)
        
        toReplace = {}
        toReplace["SRA"] = "SRA b veto"
        toReplace["SRAb"] = "SRA b tag"
        toReplace["SRB"] = "SRB b veto"
        toReplace["SRBb"] = "SRB b tag"
        toReplace["SRC"] = "SRC b veto"
        toReplace["SRCb"] = "SRC b tag"
        toReplace["SRVZResolved"] = "Resolved VZ"
        toReplace["SRVZBoosted"] = "Boosted VZ"
        toReplace["SRHZ"] = "HZ"
        toReplace["VRWZResolved"] = "VR Resolved VZ"
        toReplace["VRWZBoosted"] = "VR Boosted VZ"
        toReplace["VRHZ"] = "VR HZ"
        
        regionName = region
        if "Slepton" in region:
                if "OffZ" in region:
                        z = "\\mathrm{m}_{\\ell\\ell} < 65 \\mbox{ or } \\mathrm{m}_{\\ell\\ell} > 120\\mbox{ GeV}"
                        s = "SR"
                else:
                        z = "65 < \mathrm{m}_{\\ell\\ell} < 120\\mbox{ GeV}"
                        s = "CR"
                if "NoJet" in region:
                        j = "n_{#kern[0.5]{j}} = 0"
                else:
                        j = "n_{#kern[0.5]{j}} > 0"
                #regionName = "#splitline{%s}{%s}"%(z,j)
                label.SetTextFont(42)
                label.DrawLatex(0.92,0.63,z)
                label.DrawLatex(0.92,0.56,j)
                label.SetTextFont(62)
                label.DrawLatex(0.92,0.495,s)
        else:
                if region in toReplace.keys():
                        regionName = toReplace[region]
                label.DrawLatex(0.92,0.62,regionName)
        
        ratioPad.cd()
        
        xs = []
        ys = []
        yErrorsUp = []
        yErrorsDown = []
        widths = []
        
        for i in range(1,histObs.GetNbinsX()+1):
                xs.append(histObs.GetBinCenter(i))
                widths.append(0.5*histObs.GetBinWidth(i)) 
                predI = histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i)              
                if predI > 0:
                        ys.append(histObs.GetBinContent(i)/predI)
                        yErrorsUp.append(graphObs.GetErrorYhigh(i)/predI)                 
                        yErrorsDown.append(graphObs.GetErrorYlow(i)/predI)                                
                else:
                        ys.append(10.)
                        yErrorsUp.append(0)                     
                        yErrorsDown.append(0)
        
        
        nBinsY = 10
        if "Slepton" in region and "OnZ" in region:
                hAxis = ROOT.TH2F("hAxis", "", len(binning)-1, binning[0], binning[-1], nBinsY, 0.5, 1.5)
        else:
                if "VR" in region:
                        hAxis = ROOT.TH2F("hAxis", "", len(binning)-1, binning[0], binning[-1], nBinsY, 0, 2.0)
                elif max(ys) < 2.2:
                        hAxis = ROOT.TH2F("hAxis", "", len(binning)-1, binning[0], binning[-1], nBinsY, 0, 2.2)
                else:
                        hAxis = ROOT.TH2F("hAxis", "", len(binning)-1, binning[0], binning[-1], nBinsY, 0, max(ys)*1.1)
        hAxis.Draw("AXIS")
        
        
        hAxis.GetXaxis().SetLabelSize(0)

        hAxis.GetYaxis().CenterTitle()
        hAxis.GetYaxis().SetNdivisions(408)
        hAxis.SetTitleOffset(0.5, "Y")
        #hAxis.SetTitleSize(0.08, "Y")
        hAxis.GetYaxis().SetTitleSize(0.12)
        hAxis.GetYaxis().SetTitle("#frac{Observed}{Prediction}    ")
        hAxis.GetYaxis().SetLabelSize(0.12)

        oneLine = ROOT.TLine(binning[0], 1.0, binning[-1], 1.0)
        #~ oneLine.SetLineStyle(2)
        oneLine.Draw()
        oneLine2 = ROOT.TLine(binning[0], 0.5, binning[-1], 0.5)
        oneLine2.SetLineStyle(2)
        oneLine2.Draw()
        oneLine3 = ROOT.TLine(binning[0], 1.5, binning[-1], 1.5)
        oneLine3.SetLineStyle(2)
        oneLine3.Draw()
        
        errGraphRatio.Draw("same02")
        
        ratioGraph = ROOT.TGraphAsymmErrors(len(xs), array("d", xs), array("d", ys), array("d", widths), array("d", widths), array("d", yErrorsDown), array("d", yErrorsUp))
                
        ratioGraph.Draw("same pe0")     

        ROOT.gPad.RedrawAxis()
        plotPad.RedrawAxis()
        ratioPad.RedrawAxis()
        
        if not "Slepton" in region:
                if "SR" in region:
                        hCanvas.Print("onZResults_%s.pdf"%(region))
                        # hCanvas.Print("root/onZResults_%s.root"%(region))
                else:
                        hCanvas.Print("onZValidation_%s.pdf"%(region))
                        # hCanvas.Print("root/onZValidation_%s.root"%(region))
        else:   
                fn = "sleptonResults_%s.eps"%(region)
                hCanvas.Print(fn)
                # hCanvas.Print("root/"+fn.replace("eps","root"))
                
                from locations import locations
                import os
                os.system("sed -i 's/STIX/STIXX/' %s"%(fn))
                os.system("%s %s"%(locations.epsToPdfPath, fn))
                os.remove(fn)

        
def main():
        
        #OnZPickleICHEP = loadPickles("shelves/OnZBG_ICHEPLegacy_36fb.pkl")
        #RaresPickle8TeVLegacy = loadPickles("shelves/RareOnZBG_8TeVLegacy_36fb.pkl")
        RaresPickle2016 = loadPickles("shelves/RareOnZBG_Run2016_36fb.pkl")
        RaresPickle2017 = loadPickles("shelves/RareOnZBG_Run2017_42fb.pkl")
        RaresPickle2018 = loadPickles("shelves/RareOnZBG_Run2018_60fb.pkl")
        #RaresPickle = loadPickles("shelves/RareOnZBG_8TeVLegacy_36fb.pkl")
        
        
        name = "cutAndCount"
        countingShelves2016= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , "Run2016_36fb"),"Rares":RaresPickle2016}      
        countingShelves2017= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , "Run2017_42fb"),"Rares":RaresPickle2017}      
        countingShelves2018= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , "Run2018_60fb"),"Rares":RaresPickle2018}      
        
        countingShelves = {"Run2016_36fb": countingShelves2016,"Run2017_42fb": countingShelves2017,"Run2018_60fb": countingShelves2018}
        
        # makeOverviewPlot(countingShelves, "zeroBJets")
        # makeOverviewPlot(countingShelves, "oneOrMoreBJets")
        # setTDRStyle()
        # makeOverviewPlot(countingShelves, "zeroBJets", ratio=True)
        # makeOverviewPlot(countingShelves, "oneOrMoreBJets", ratio=True)
        
        # makeOverviewPlotOnZ("VRA")
        # makeOverviewPlotOnZ("VRB")
        # makeOverviewPlotOnZ("VRC")
        # makeOverviewPlotOnZ("VRWZResolved")
        # makeOverviewPlotOnZ("VRWZBoosted")
        # makeOverviewPlotOnZ("VRHZ")
        # makeOverviewPlotOnZ("SRA")
        # makeOverviewPlotOnZ("SRAb")
        # makeOverviewPlotOnZ("SRB")
        # makeOverviewPlotOnZ("SRBb")
        # makeOverviewPlotOnZ("SRC")
        # makeOverviewPlotOnZ("SRCb")
        # makeOverviewPlotOnZ("SRVZResolved")
        # makeOverviewPlotOnZ("SRVZBoosted")
        makeOverviewPlotOnZ("SRHZ")
        # makeOverviewPlotOnZ("SRSleptonOneJetOffZ")
        # makeOverviewPlotOnZ("SRSleptonOneJetOnZ")
        # makeOverviewPlotOnZ("SRSleptonNoJetOffZ")
        # makeOverviewPlotOnZ("SRSleptonNoJetOnZ")
        
main()

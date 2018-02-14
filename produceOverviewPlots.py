import pickle
import os
import sys


from setTDRStyle import setTDRStyle

from corrections import rSFOF,rSFOFDirect,rSFOFTrig, rEEOF, rMMOF, rOutIn
from centralConfig import zPredictions, regionsToUse, runRanges, OtherPredictions, OnlyZPredictions,systematics
from helpers import createMyColors
from defs import myColors,thePlots,getPlot,theCuts

import ratios

from array import array

import ROOT
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphErrors, TF1, gStyle, TGraphAsymmErrors, TFile, TH2F

def saveTable(table, name):
	tabFile = open("tab/table_%s.tex"%name, "w")
	tabFile.write(table)
	tabFile.close()

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

def getResultsOld(shelve,region,selection):
	
	result = {}
	
	result["rSFOF"] = getattr(rSFOF,region).val
	result["rSFOFErr"] = getattr(rSFOF,region).err
	result["rEEOF"] = getattr(rEEOF,region).val
	result["rEEOFErr"] = getattr(rEEOF,region).err
	result["rMMOF"] = getattr(rMMOF,region).val
	result["rMMOFErr"] = getattr(rMMOF,region).err
	
	result["lowMassEE"] = shelve[region][selection]["edgeMass"]["EE"]
	result["lowMassMM"] = shelve[region][selection]["edgeMass"]["MM"]
	result["lowMassSF"] = shelve[region][selection]["edgeMass"]["EE"] + shelve[region][selection]["edgeMass"]["MM"]
	result["lowMassOF"] = shelve[region][selection]["edgeMass"]["EM"]
	result["lowMassPredSF"] = result["lowMassOF"]*getattr(rSFOF,region).val
	result["lowMassPredStatErrSF"] = result["lowMassOF"]**0.5*getattr(rSFOF,region).val
	result["lowMassPredSystErrSF"] = result["lowMassOF"]*getattr(rSFOF,region).err
	
	result["lowMassPredEE"] = result["lowMassOF"]*getattr(rEEOF,region).val
	result["lowMassPredStatErrEE"] = result["lowMassOF"]**0.5*getattr(rEEOF,region).val
	result["lowMassPredSystErrEE"] = result["lowMassOF"]*getattr(rEEOF,region).err
	
	result["lowMassPredMM"] = result["lowMassOF"]*getattr(rMMOF,region).val
	result["lowMassPredStatErrMM"] = result["lowMassOF"]**0.5*getattr(rMMOF,region).val
	result["lowMassPredSystErrMM"] = result["lowMassOF"]*getattr(rMMOF,region).err
	
	result["lowMassZPredSF"] = getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.lowMass,region).val
	result["lowMassZPredErrSF"] = ((getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.lowMass,region).err)**2 + (getattr(getattr(zPredictions,selection).SF,region).err*getattr(rOutIn.lowMass,region).val)**2 )**0.5
	
	result["lowMassOnlyZPredSF"] = getattr(getattr(OnlyZPredictions,selection).SF,region).val*getattr(rOutIn.lowMass,region).val
	
	result["lowMassOtherPredSF"] = getattr(getattr(OtherPredictions,selection).SF,region).val*getattr(rOutIn.lowMass,region).val
	
	result["lowMassZPredEE"] = getattr(getattr(zPredictions,selection).EE,region).val*getattr(rOutInEE.lowMass,region).val
	result["lowMassZPredErrEE"] = ((getattr(getattr(zPredictions,selection).EE,region).val*getattr(rOutInEE.lowMass,region).err)**2 + (getattr(getattr(zPredictions,selection).EE,region).err*getattr(rOutInEE.lowMass,region).val)**2 )**0.5
	
	result["lowMassZPredMM"] = getattr(getattr(zPredictions,selection).MM,region).val*getattr(rOutInMM.lowMass,region).val
	result["lowMassZPredErrMM"] = ((getattr(getattr(zPredictions,selection).MM,region).val*getattr(rOutInMM.lowMass,region).err)**2 + (getattr(getattr(zPredictions,selection).MM,region).err*getattr(rOutInMM.lowMass,region).val)**2 )**0.5
	
	result["lowMassTotalPredSF"] = result["lowMassPredSF"] + result["lowMassZPredSF"]
	result["lowMassTotalPredErrSF"] = ( result["lowMassPredStatErrSF"]**2 +  result["lowMassPredSystErrSF"]**2 + result["lowMassZPredErrSF"]**2 )**0.5
	
	result["lowMassTotalPredEE"] = result["lowMassPredEE"] + result["lowMassZPredEE"]
	result["lowMassTotalPredErrEE"] = ( result["lowMassPredStatErrEE"]**2 +  result["lowMassPredSystErrEE"]**2 + result["lowMassZPredErrEE"]**2 )**0.5
	
	result["lowMassTotalPredMM"] = result["lowMassPredMM"] + result["lowMassZPredMM"]
	result["lowMassTotalPredErrMM"] = ( result["lowMassPredStatErrMM"]**2 +  result["lowMassPredSystErrMM"]**2 + result["lowMassZPredErrMM"]**2 )**0.5

	
	result["belowZEE"] = shelve[region][selection]["belowZ"]["EE"]
	result["belowZMM"] = shelve[region][selection]["belowZ"]["MM"]
	result["belowZSF"] = shelve[region][selection]["belowZ"]["EE"] + shelve[region][selection]["belowZ"]["MM"]
	result["belowZOF"] = shelve[region][selection]["belowZ"]["EM"]
	
	result["belowZPredSF"] = result["belowZOF"]*getattr(rSFOF,region).val
	result["belowZPredStatErrSF"] = result["belowZOF"]**0.5*getattr(rSFOF,region).val
	result["belowZPredSystErrSF"] = result["belowZOF"]*getattr(rSFOF,region).err
	
	result["belowZPredEE"] = result["belowZOF"]*getattr(rEEOF,region).val
	result["belowZPredStatErrEE"] = result["belowZOF"]**0.5*getattr(rEEOF,region).val
	result["belowZPredSystErrEE"] = result["belowZOF"]*getattr(rEEOF,region).err
	
	result["belowZPredMM"] = result["belowZOF"]*getattr(rMMOF,region).val
	result["belowZPredStatErrMM"] = result["belowZOF"]**0.5*getattr(rMMOF,region).val
	result["belowZPredSystErrMM"] = result["belowZOF"]*getattr(rMMOF,region).err
	
	result["belowZZPredSF"] = getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.belowZ,region).val
	result["belowZZPredErrSF"] = ((getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.belowZ,region).err)**2 + (getattr(getattr(zPredictions,selection).SF,region).err*getattr(rOutIn.belowZ,region).val)**2 )**0.5
	
	result["belowZOnlyZPredSF"] = getattr(getattr(OnlyZPredictions,selection).SF,region).val*getattr(rOutIn.belowZ,region).val
	
	result["belowZOtherPredSF"] = getattr(getattr(OtherPredictions,selection).SF,region).val*getattr(rOutIn.belowZ,region).val
	
	result["belowZZPredEE"] = getattr(getattr(zPredictions,selection).EE,region).val*getattr(rOutInEE.belowZ,region).val
	result["belowZZPredErrEE"] = ((getattr(getattr(zPredictions,selection).EE,region).val*getattr(rOutInEE.belowZ,region).err)**2 + (getattr(getattr(zPredictions,selection).EE,region).err*getattr(rOutInEE.belowZ,region).val)**2 )**0.5
	
	result["belowZZPredMM"] = getattr(getattr(zPredictions,selection).MM,region).val*getattr(rOutInMM.belowZ,region).val
	result["belowZZPredErrMM"] = ((getattr(getattr(zPredictions,selection).MM,region).val*getattr(rOutInMM.belowZ,region).err)**2 + (getattr(getattr(zPredictions,selection).MM,region).err*getattr(rOutInMM.belowZ,region).val)**2 )**0.5
	
	result["belowZTotalPredSF"] = result["belowZPredSF"] + result["belowZZPredSF"]
	result["belowZTotalPredErrSF"] = ( result["belowZPredStatErrSF"]**2 +  result["belowZPredSystErrSF"]**2 + result["belowZZPredErrSF"]**2 )**0.5
	
	result["belowZTotalPredEE"] = result["belowZPredEE"] + result["belowZZPredEE"]
	result["belowZTotalPredErrEE"] = ( result["belowZPredStatErrEE"]**2 +  result["belowZPredSystErrEE"]**2 + result["belowZZPredErrEE"]**2 )**0.5
	
	result["belowZTotalPredMM"] = result["belowZPredMM"] + result["belowZZPredMM"]
	result["belowZTotalPredErrMM"] = ( result["belowZPredStatErrMM"]**2 +  result["belowZPredSystErrMM"]**2 + result["belowZZPredErrMM"]**2 )**0.5
	
	result["aboveZEE"] = shelve[region][selection]["aboveZ"]["EE"]
	result["aboveZMM"] = shelve[region][selection]["aboveZ"]["MM"]
	result["aboveZSF"] = shelve[region][selection]["aboveZ"]["EE"] + shelve[region][selection]["aboveZ"]["MM"]
	result["aboveZOF"] = shelve[region][selection]["aboveZ"]["EM"]
	
	result["aboveZPredSF"] = result["aboveZOF"]*getattr(rSFOF,region).val
	result["aboveZPredStatErrSF"] = result["aboveZOF"]**0.5*getattr(rSFOF,region).val
	result["aboveZPredSystErrSF"] = result["aboveZOF"]*getattr(rSFOF,region).err
	
	result["aboveZPredEE"] = result["aboveZOF"]*getattr(rEEOF,region).val
	result["aboveZPredStatErrEE"] = result["aboveZOF"]**0.5*getattr(rEEOF,region).val
	result["aboveZPredSystErrEE"] = result["aboveZOF"]*getattr(rEEOF,region).err
	
	result["aboveZPredMM"] = result["aboveZOF"]*getattr(rMMOF,region).val
	result["aboveZPredStatErrMM"] = result["aboveZOF"]**0.5*getattr(rMMOF,region).val
	result["aboveZPredSystErrMM"] = result["aboveZOF"]*getattr(rMMOF,region).err
	
	result["aboveZZPredSF"] = getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.aboveZ,region).val
	result["aboveZZPredErrSF"] = ((getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.aboveZ,region).err)**2 + (getattr(getattr(zPredictions,selection).SF,region).err*getattr(rOutIn.aboveZ,region).val)**2 )**0.5
	
	result["aboveZOnlyZPredSF"] = getattr(getattr(OnlyZPredictions,selection).SF,region).val*getattr(rOutIn.aboveZ,region).val
	
	result["aboveZOtherPredSF"] = getattr(getattr(OtherPredictions,selection).SF,region).val*getattr(rOutIn.aboveZ,region).val
	
	result["aboveZZPredEE"] = getattr(getattr(zPredictions,selection).EE,region).val*getattr(rOutInEE.aboveZ,region).val
	result["aboveZZPredErrEE"] = ((getattr(getattr(zPredictions,selection).EE,region).val*getattr(rOutInEE.aboveZ,region).err)**2 + (getattr(getattr(zPredictions,selection).EE,region).err*getattr(rOutInEE.aboveZ,region).val)**2 )**0.5
	
	result["aboveZZPredMM"] = getattr(getattr(zPredictions,selection).MM,region).val*getattr(rOutInMM.aboveZ,region).val
	result["aboveZZPredErrMM"] = ((getattr(getattr(zPredictions,selection).MM,region).val*getattr(rOutInMM.aboveZ,region).err)**2 + (getattr(getattr(zPredictions,selection).MM,region).err*getattr(rOutInMM.aboveZ,region).val)**2 )**0.5
	
	result["aboveZTotalPredSF"] = result["aboveZPredSF"] + result["aboveZZPredSF"]
	result["aboveZTotalPredErrSF"] = ( result["aboveZPredStatErrSF"]**2 +  result["aboveZPredSystErrSF"]**2 + result["aboveZZPredErrSF"]**2 )**0.5
	
	result["aboveZTotalPredEE"] = result["aboveZPredEE"] + result["aboveZZPredEE"]
	result["aboveZTotalPredErrEE"] = ( result["aboveZPredStatErrEE"]**2 +  result["aboveZPredSystErrEE"]**2 + result["aboveZZPredErrEE"]**2 )**0.5
	
	result["aboveZTotalPredMM"] = result["aboveZPredMM"] + result["aboveZZPredMM"]
	result["aboveZTotalPredErrMM"] = ( result["aboveZPredStatErrMM"]**2 +  result["aboveZPredSystErrMM"]**2 + result["aboveZZPredErrMM"]**2 )**0.5
	
	
	
	
	result["highMassEE"] = shelve[region][selection]["highMass"]["EE"]
	result["highMassMM"] = shelve[region][selection]["highMass"]["MM"]
	result["highMassSF"] = shelve[region][selection]["highMass"]["EE"] + shelve[region][selection]["highMass"]["MM"]
	result["highMassOF"] = shelve[region][selection]["highMass"]["EM"]
	
	result["highMassPredSF"] = result["highMassOF"]*getattr(rSFOF,region).val
	result["highMassPredStatErrSF"] = result["highMassOF"]**0.5*getattr(rSFOF,region).val
	result["highMassPredSystErrSF"] = result["highMassOF"]*getattr(rSFOF,region).err
	
	result["highMassPredEE"] = result["highMassOF"]*getattr(rEEOF,region).val
	result["highMassPredStatErrEE"] = result["highMassOF"]**0.5*getattr(rEEOF,region).val
	result["highMassPredSystErrEE"] = result["highMassOF"]*getattr(rEEOF,region).err
	
	result["highMassPredMM"] = result["highMassOF"]*getattr(rMMOF,region).val
	result["highMassPredStatErrMM"] = result["highMassOF"]**0.5*getattr(rMMOF,region).val
	result["highMassPredSystErrMM"] = result["highMassOF"]*getattr(rMMOF,region).err
	
	result["highMassZPredSF"] = getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.highMass,region).val
	result["highMassZPredErrSF"] = ((getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.highMass,region).err)**2 + (getattr(getattr(zPredictions,selection).SF,region).err*getattr(rOutIn.highMass,region).val)**2 )**0.5
	
	result["highMassOnlyZPredSF"] = getattr(getattr(OnlyZPredictions,selection).SF,region).val*getattr(rOutIn.highMass,region).val
	
	result["highMassOtherPredSF"] = getattr(getattr(OtherPredictions,selection).SF,region).val*getattr(rOutIn.highMass,region).val
	
	result["highMassZPredEE"] = getattr(getattr(zPredictions,selection).EE,region).val*getattr(rOutInEE.highMass,region).val
	result["highMassZPredErrEE"] = ((getattr(getattr(zPredictions,selection).EE,region).val*getattr(rOutInEE.highMass,region).err)**2 + (getattr(getattr(zPredictions,selection).EE,region).err*getattr(rOutInEE.highMass,region).val)**2 )**0.5
	
	result["highMassZPredMM"] = getattr(getattr(zPredictions,selection).MM,region).val*getattr(rOutInMM.highMass,region).val
	result["highMassZPredErrMM"] = ((getattr(getattr(zPredictions,selection).MM,region).val*getattr(rOutInMM.highMass,region).err)**2 + (getattr(getattr(zPredictions,selection).MM,region).err*getattr(rOutInMM.highMass,region).val)**2 )**0.5
	

	result["highMassTotalPredSF"] = result["highMassPredSF"] + result["highMassZPredSF"]
	result["highMassTotalPredErrSF"] = ( result["highMassPredStatErrSF"]**2 +  result["highMassPredSystErrSF"]**2 + result["highMassZPredErrSF"]**2 )**0.5
	
	result["highMassTotalPredEE"] = result["highMassPredEE"] + result["highMassZPredEE"]
	result["highMassTotalPredErrEE"] = ( result["highMassPredStatErrEE"]**2 +  result["highMassPredSystErrEE"]**2 + result["highMassZPredErrEE"]**2 )**0.5
	
	result["highMassTotalPredMM"] = result["highMassPredMM"] + result["highMassZPredMM"]
	result["highMassTotalPredErrMM"] = ( result["highMassPredStatErrMM"]**2 +  result["highMassPredSystErrMM"]**2 + result["highMassZPredErrMM"]**2 )**0.5	

	
	
	
	result["onZEE"] = shelve[region][selection]["zMass"]["EE"]
	result["onZMM"] = shelve[region][selection]["zMass"]["MM"]
	result["onZSF"] = shelve[region][selection]["zMass"]["EE"] + shelve[region][selection]["zMass"]["MM"]
	result["onZOF"] = shelve[region][selection]["zMass"]["EM"]	
	
	result["onZPredSF"] = result["onZOF"]*getattr(rSFOF,region).val
	result["onZPredStatErrSF"] = result["onZOF"]**0.5*getattr(rSFOF,region).val
	result["onZPredSystErrSF"] = result["onZOF"]*getattr(rSFOF,region).err
	
	result["onZPredEE"] = result["onZOF"]*getattr(rEEOF,region).val
	result["onZPredStatErrEE"] = result["onZOF"]**0.5*getattr(rEEOF,region).val
	result["onZPredSystErrEE"] = result["onZOF"]*getattr(rEEOF,region).err
	
	result["onZPredMM"] = result["onZOF"]*getattr(rMMOF,region).val
	result["onZPredStatErrMM"] = result["onZOF"]**0.5*getattr(rMMOF,region).val
	result["onZPredSystErrMM"] = result["onZOF"]*getattr(rMMOF,region).err
	
	result["onZZPredSF"] = getattr(getattr(zPredictions,selection).SF,region).val
	result["onZZPredErrSF"] = getattr(getattr(zPredictions,selection).SF,region).err
	
	result["onZOnlyZPredSF"] = getattr(getattr(OnlyZPredictions,selection).SF,region).val
	
	result["onZOtherPredSF"] = getattr(getattr(OtherPredictions,selection).SF,region).val
	
	result["onZZPredEE"] = getattr(getattr(zPredictions,selection).EE,region).val
	result["onZZPredErrEE"] = getattr(getattr(zPredictions,selection).EE,region).err
	
	result["onZZPredMM"] = getattr(getattr(zPredictions,selection).MM,region).val
	result["onZZPredErrMM"] = getattr(getattr(zPredictions,selection).MM,region).err
	

	result["onZTotalPredSF"] = result["onZPredSF"] + result["onZZPredSF"]
	result["onZTotalPredErrSF"] = ( result["onZPredStatErrSF"]**2 +  result["onZPredSystErrSF"]**2 + result["onZZPredErrSF"]**2 )**0.5
	
	result["onZTotalPredEE"] = result["onZPredEE"] + result["onZZPredEE"]
	result["onZTotalPredErrEE"] = ( result["onZPredStatErrEE"]**2 +  result["onZPredSystErrEE"]**2 + result["onZZPredErrEE"]**2 )**0.5
	
	result["onZTotalPredMM"] = result["onZPredMM"] + result["onZZPredMM"]
	result["onZTotalPredErrMM"] = ( result["onZPredStatErrMM"]**2 +  result["onZPredSystErrMM"]**2 + result["onZZPredErrMM"]**2 )**0.5

	
	return result

			
def getResultsNLL(shelve,signalRegion):
	
	NLLRegions = ["lowNLL","highNLL"]
	massRegions = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400","lowMass","highMass","highMassOld"]	
	MT2Regions = ["highMT2"]
	result = {}
	
	region = "inclusive"
	

	result["rSFOFDirect"] = getattr(rSFOFDirect,region).val
	result["rSFOFDirectErr"] = getattr(rSFOFDirect,region).err
	result["rSFOFTrig"] = getattr(rSFOFTrig,region).val
	result["rSFOFTrigErr"] = getattr(rSFOFTrig,region).err

	result["onZPrediction_highNLL_highMT2"] = OnlyZPredictions.MT2.SF.highNLL.val
	result["onZPrediction_lowNLL_highMT2"] = OnlyZPredictions.MT2.SF.lowNLL.val
	result["onZPrediction_highNLL_highMT2_Err"] = OnlyZPredictions.MT2.SF.highNLL.err
	result["onZPrediction_lowNLL_highMT2_Err"] = OnlyZPredictions.MT2.SF.lowNLL.err
	
	result["rarePrediction_highNLL_highMT2"] = OtherPredictions.MT2.SF.highNLL.val
	result["rarePrediction_lowNLL_highMT2"] = OtherPredictions.MT2.SF.lowNLL.val
	result["rarePrediction_highNLL_highMT2_Err"] = OtherPredictions.MT2.SF.highNLL.err
	result["rarePrediction_lowNLL_highMT2_Err"] = OtherPredictions.MT2.SF.lowNLL.err
	

	
	for selection in NLLRegions:
		result[selection] = {}
		for MT2Region in MT2Regions:
			for massRegion in massRegions:		
			
				result[selection]["%s_%s_EE"%(MT2Region,massRegion)] = shelve[signalRegion][selection][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.massCuts,massRegion).name]["EE"]
				result[selection]["%s_%s_MM"%(MT2Region,massRegion)] = shelve[signalRegion][selection][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.massCuts,massRegion).name]["MM"]
				result[selection]["%s_%s_SF"%(MT2Region,massRegion)] = shelve[signalRegion][selection][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.massCuts,massRegion).name]["EE"] + shelve[signalRegion][selection][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.massCuts,massRegion).name]["MM"]
				result[selection]["%s_%s_OF"%(MT2Region,massRegion)] = shelve[signalRegion][selection][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.massCuts,massRegion).name]["EM"]
				result[selection]["%s_%s_OFRMuEScaled"%(MT2Region,massRegion)] = shelve[signalRegion][selection][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.massCuts,massRegion).name]["EMRMuEScaled"]
				result[selection]["%s_%s_OFRMuEScaledUp"%(MT2Region,massRegion)] = shelve[signalRegion][selection][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.massCuts,massRegion).name]["EMRMuEScaledUp"]
				result[selection]["%s_%s_OFRMuEScaledDown"%(MT2Region,massRegion)] = shelve[signalRegion][selection][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.massCuts,massRegion).name]["EMRMuEScaledDown"]
				
				yield_up = ROOT.Double(1.)
				yield_down = ROOT.Double(1.)
				## calculate poisson error
				ROOT.RooHistError.instance().getPoissonInterval(result[selection]["%s_%s_OF"%(MT2Region,massRegion)],yield_down,yield_up,1.)
				
				yieldSF_up = ROOT.Double(1.)
				yieldSF_down = ROOT.Double(1.)
				ROOT.RooHistError.instance().getPoissonInterval(result[selection]["%s_%s_SF"%(MT2Region,massRegion)],yieldSF_down,yieldSF_up,1.)
				
				result[selection]["%s_%s_SFUp"%(MT2Region,massRegion)] = yieldSF_up - result[selection]["%s_%s_SF"%(MT2Region,massRegion)]
				result[selection]["%s_%s_SFDown"%(MT2Region,massRegion)] = result[selection]["%s_%s_SF"%(MT2Region,massRegion)] - yieldSF_down

				result[selection]["%s_%s_PredFactSF"%(MT2Region,massRegion)] = result[selection]["%s_%s_OFRMuEScaled"%(MT2Region,massRegion)]*getattr(rSFOFTrig,region).val
				if result[selection]["%s_%s_OF"%(MT2Region,massRegion)] > 0:
					result[selection]["%s_%s_PredFactStatUpSF"%(MT2Region,massRegion)] = yield_up*result[selection]["%s_%s_PredFactSF"%(MT2Region,massRegion)]/result[selection]["%s_%s_OF"%(MT2Region,massRegion)] - result[selection]["%s_%s_PredFactSF"%(MT2Region,massRegion)]
					result[selection]["%s_%s_PredFactStatDownSF"%(MT2Region,massRegion)] = result[selection]["%s_%s_PredFactSF"%(MT2Region,massRegion)] - yield_down*result[selection]["%s_%s_PredFactSF"%(MT2Region,massRegion)]/result[selection]["%s_%s_OF"%(MT2Region,massRegion)]
					result[selection]["%s_%s_PredFactSystErrSF"%(MT2Region,massRegion)] = result[selection]["%s_%s_OFRMuEScaled"%(MT2Region,massRegion)]*(getattr(rSFOFTrig,region).err**2 + max(abs(result[selection]["%s_%s_OFRMuEScaled"%(MT2Region,massRegion)] - result[selection]["%s_%s_OFRMuEScaledUp"%(MT2Region,massRegion)])/result[selection]["%s_%s_OFRMuEScaled"%(MT2Region,massRegion)],abs(result[selection]["%s_%s_OFRMuEScaled"%(MT2Region,massRegion)] - result[selection]["%s_%s_OFRMuEScaledDown"%(MT2Region,massRegion)])/result[selection]["%s_%s_OFRMuEScaled"%(MT2Region,massRegion)])**2)**0.5		
				else:
					result[selection]["%s_%s_PredFactStatUpSF"%(MT2Region,massRegion)] = 1.8*getattr(rSFOFTrig,region).val
					result[selection]["%s_%s_PredFactStatDownSF"%(MT2Region,massRegion)] = yield_down*getattr(rSFOFTrig,region).val
					result[selection]["%s_%s_PredFactSystErrSF"%(MT2Region,massRegion)] = 0
				
				if result[selection]["%s_%s_OF"%(MT2Region,massRegion)] > 0:
					result[selection]["%s_%s_RSFOF_Fact"%(MT2Region,massRegion)] = result[selection]["%s_%s_PredFactSF"%(MT2Region,massRegion)] / result[selection]["%s_%s_OF"%(MT2Region,massRegion)]
					result[selection]["%s_%s_RSFOF_Fact_Err"%(MT2Region,massRegion)] = result[selection]["%s_%s_PredFactSystErrSF"%(MT2Region,massRegion)] / result[selection]["%s_%s_OF"%(MT2Region,massRegion)]
				else:
					result[selection]["%s_%s_RSFOF_Fact"%(MT2Region,massRegion)] = 0.
					result[selection]["%s_%s_RSFOF_Fact_Err"%(MT2Region,massRegion)] = 0.
				
				if result[selection]["%s_%s_OF"%(MT2Region,massRegion)] > 0:
					result[selection]["%s_%s_RSFOF_Combined"%(MT2Region,massRegion)],result[selection]["%s_%s_RSFOF_Combined_Err"%(MT2Region,massRegion)] = getWeightedAverage(result[selection]["%s_%s_RSFOF_Fact"%(MT2Region,massRegion)],result[selection]["%s_%s_RSFOF_Fact_Err"%(MT2Region,massRegion)],getattr(rSFOFDirect,region).val,getattr(rSFOFDirect,region).err)
				else:
					result[selection]["%s_%s_RSFOF_Combined"%(MT2Region,massRegion)] = getattr(rSFOFDirect,region).val
					result[selection]["%s_%s_RSFOF_Combined_Err"%(MT2Region,massRegion)] = getattr(rSFOFDirect,region).err
				
				result[selection]["%s_%s_PredSF"%(MT2Region,massRegion)] = result[selection]["%s_%s_OF"%(MT2Region,massRegion)]*result[selection]["%s_%s_RSFOF_Combined"%(MT2Region,massRegion)]
				if result[selection]["%s_%s_PredSF"%(MT2Region,massRegion)] > 0:
					result[selection]["%s_%s_PredStatUpSF"%(MT2Region,massRegion)] = yield_up*result[selection]["%s_%s_RSFOF_Combined"%(MT2Region,massRegion)] - result[selection]["%s_%s_PredSF"%(MT2Region,massRegion)]
				else:
					result[selection]["%s_%s_PredStatUpSF"%(MT2Region,massRegion)] = 1.8*result[selection]["%s_%s_RSFOF_Combined"%(MT2Region,massRegion)] 
				result[selection]["%s_%s_PredStatDownSF"%(MT2Region,massRegion)] = result[selection]["%s_%s_PredSF"%(MT2Region,massRegion)] - yield_down*result[selection]["%s_%s_RSFOF_Combined"%(MT2Region,massRegion)] 
				result[selection]["%s_%s_PredSystErrSF"%(MT2Region,massRegion)] = result[selection]["%s_%s_OF"%(MT2Region,massRegion)]*result[selection]["%s_%s_RSFOF_Combined_Err"%(MT2Region,massRegion)]
				
				result[selection]["%s_%s_ZPredSF"%(MT2Region,massRegion)] = result["onZPrediction_%s_%s"%(selection,MT2Region)]*getattr(getattr(rOutIn,massRegion),region).val
				if MT2Region == "highMT2":
					result[selection]["%s_%s_ZPredErrSF"%(MT2Region,massRegion)] = ((result["onZPrediction_%s_%s"%(selection,MT2Region)]*getattr(getattr(rOutIn,massRegion),region).err)**2 + (result["onZPrediction_%s_%s_Err"%(selection,MT2Region)] * getattr(getattr(rOutIn,massRegion),region).val)**2 )**0.5
				else:
					result[selection]["%s_%s_ZPredErrSF"%(MT2Region,massRegion)] = ((result["onZPrediction_%s_%s"%(selection,MT2Region)]*getattr(getattr(rOutIn,massRegion),region).err)**2 + result["onZPrediction_%s_%s"%(selection,MT2Region)] * getattr(getattr(rOutIn,massRegion),region).val**2 )**0.5
				
				result[selection]["%s_%s_RarePredROutInSF"%(MT2Region,massRegion)] = result["rarePrediction_%s_%s"%(selection,MT2Region)]*getattr(getattr(rOutIn,massRegion),region).val
				result[selection]["%s_%s_RarePredROutInErrSF"%(MT2Region,massRegion)] = ((result["rarePrediction_%s_%s"%(selection,MT2Region)]*getattr(getattr(rOutIn,massRegion),region).err)**2 + (result["rarePrediction_%s_%s_Err"%(selection,MT2Region)] * getattr(getattr(rOutIn,massRegion),region).val)**2 )**0.5
					
				result[selection]["%s_%s_RarePredSF"%(MT2Region,massRegion)] = shelve["Rares"]["%s_%s_SF"%(massRegion,selection)] - shelve["Rares"]["%s_%s_OF"%(massRegion,selection)]
				result[selection]["%s_%s_RarePredSF_Up"%(MT2Region,massRegion)] = shelve["Rares"]["%s_%s_SF_Up"%(massRegion,selection)] - shelve["Rares"]["%s_%s_OF_Up"%(massRegion,selection)]
				result[selection]["%s_%s_RarePredSF_Down"%(MT2Region,massRegion)] = shelve["Rares"]["%s_%s_SF_Down"%(massRegion,selection)] - shelve["Rares"]["%s_%s_OF_Down"%(massRegion,selection)]
				result[selection]["%s_%s_RarePredErrSF"%(MT2Region,massRegion)] = max(abs(result[selection]["%s_%s_RarePredSF_Up"%(MT2Region,massRegion)]-result[selection]["%s_%s_RarePredSF"%(MT2Region,massRegion)]),abs(result[selection]["%s_%s_RarePredSF_Down"%(MT2Region,massRegion)]-result[selection]["%s_%s_RarePredSF"%(MT2Region,massRegion)]))
		
				
				result[selection]["%s_%s_TotalPredROutInSF"%(MT2Region,massRegion)] = result[selection]["%s_%s_PredSF"%(MT2Region,massRegion)] + result[selection]["%s_%s_ZPredSF"%(MT2Region,massRegion)] + result[selection]["%s_%s_RarePredROutInSF"%(MT2Region,massRegion)]
				result[selection]["%s_%s_TotalPredROutInErrUpSF"%(MT2Region,massRegion)] = ( result[selection]["%s_%s_PredStatUpSF"%(MT2Region,massRegion)]**2 +  result[selection]["%s_%s_PredSystErrSF"%(MT2Region,massRegion)]**2 + result[selection]["%s_%s_ZPredErrSF"%(MT2Region,massRegion)]**2 + result[selection]["%s_%s_RarePredROutInErrSF"%(MT2Region,massRegion)]**2)**0.5
				result[selection]["%s_%s_TotalPredROutInErrDownSF"%(MT2Region,massRegion)] = ( result[selection]["%s_%s_PredStatDownSF"%(MT2Region,massRegion)]**2 +  result[selection]["%s_%s_PredSystErrSF"%(MT2Region,massRegion)]**2 + result[selection]["%s_%s_ZPredErrSF"%(MT2Region,massRegion)]**2 + result[selection]["%s_%s_RarePredROutInErrSF"%(MT2Region,massRegion)]**2)**0.5
				
				result[selection]["%s_%s_TotalPredSF"%(MT2Region,massRegion)] = result[selection]["%s_%s_PredSF"%(MT2Region,massRegion)] + result[selection]["%s_%s_ZPredSF"%(MT2Region,massRegion)] + result[selection]["%s_%s_RarePredSF"%(MT2Region,massRegion)]
				result[selection]["%s_%s_TotalPredErrUpSF"%(MT2Region,massRegion)] = ( result[selection]["%s_%s_PredStatUpSF"%(MT2Region,massRegion)]**2 +  result[selection]["%s_%s_PredSystErrSF"%(MT2Region,massRegion)]**2 + result[selection]["%s_%s_ZPredErrSF"%(MT2Region,massRegion)]**2 + result[selection]["%s_%s_RarePredErrSF"%(MT2Region,massRegion)]**2)**0.5
				result[selection]["%s_%s_TotalPredErrDownSF"%(MT2Region,massRegion)] = ( result[selection]["%s_%s_PredStatDownSF"%(MT2Region,massRegion)]**2 +  result[selection]["%s_%s_PredSystErrSF"%(MT2Region,massRegion)]**2 + result[selection]["%s_%s_ZPredErrSF"%(MT2Region,massRegion)]**2 + result[selection]["%s_%s_RarePredErrSF"%(MT2Region,massRegion)]**2)**0.5

	for massRegion in ["highMassOld"]:		
	
		result["highNLL"]["%s_EE"%massRegion] = shelve[signalRegion]["highNLL"][getattr(theCuts.massCuts,massRegion).name]["EE"]
		result["highNLL"]["%s_MM"%massRegion] = shelve[signalRegion]["highNLL"][getattr(theCuts.massCuts,massRegion).name]["MM"]
		result["highNLL"]["%s_SF"%massRegion] = shelve[signalRegion]["highNLL"][getattr(theCuts.massCuts,massRegion).name]["EE"] + shelve[signalRegion]["highNLL"][getattr(theCuts.massCuts,massRegion).name]["MM"]
		result["highNLL"]["%s_OF"%massRegion] = shelve[signalRegion]["highNLL"][getattr(theCuts.massCuts,massRegion).name]["EM"]
		result["highNLL"]["%s_OFRMuEScaled"%massRegion] = shelve[signalRegion]["highNLL"][getattr(theCuts.massCuts,massRegion).name]["EMRMuEScaled"]
		result["highNLL"]["%s_OFRMuEScaledUp"%massRegion] = shelve[signalRegion]["highNLL"][getattr(theCuts.massCuts,massRegion).name]["EMRMuEScaledUp"]
		result["highNLL"]["%s_OFRMuEScaledDown"%massRegion] = shelve[signalRegion]["highNLL"][getattr(theCuts.massCuts,massRegion).name]["EMRMuEScaledDown"]
		
		yield_up = ROOT.Double(1.)
		yield_down = ROOT.Double(1.)
		## calculate poisson error
		ROOT.RooHistError.instance().getPoissonInterval(result["highNLL"]["%s_OF"%massRegion],yield_down,yield_up,1.)
		
		result["highNLL"]["%s_PredFactSF"%massRegion] = result["highNLL"]["%s_OFRMuEScaled"%massRegion]*getattr(rSFOFTrig,region).val
		if result["highNLL"]["%s_OF"%massRegion] > 0:
			result["highNLL"]["%s_PredFactStatUpSF"%massRegion] = yield_up*result["highNLL"]["%s_PredFactSF"%massRegion]/result["highNLL"]["%s_OF"%massRegion] - result["highNLL"]["%s_PredFactSF"%massRegion]
			result["highNLL"]["%s_PredFactStatDownSF"%massRegion] = result["highNLL"]["%s_PredFactSF"%massRegion] - yield_down*result["highNLL"]["%s_PredFactSF"%massRegion]/result["highNLL"]["%s_OF"%massRegion]
			result["highNLL"]["%s_PredFactSystErrSF"%massRegion] = result["highNLL"]["%s_OFRMuEScaled"%massRegion]*(getattr(rSFOFTrig,region).err**2 + max(abs(result["highNLL"]["%s_OFRMuEScaled"%massRegion] - result["highNLL"]["%s_OFRMuEScaledUp"%massRegion])/result["highNLL"]["%s_OFRMuEScaled"%massRegion],abs(result["highNLL"]["%s_OFRMuEScaled"%massRegion] - result["highNLL"]["%s_OFRMuEScaledDown"%massRegion])/result["highNLL"]["%s_OFRMuEScaled"%massRegion])**2)**0.5		
		else:
			result["highNLL"]["%s_PredFactStatUpSF"%massRegion] = 1.8*getattr(rSFOFTrig,region).val
			result["highNLL"]["%s_PredFactStatDownSF"%massRegion] = yield_down*getattr(rSFOFTrig,region).val
			result["highNLL"]["%s_PredFactSystErrSF"%massRegion] = 0
		
		if result["highNLL"]["%s_OF"%massRegion] > 0:
			result["highNLL"]["%s_RSFOF_Fact"%massRegion] = result["highNLL"]["%s_PredFactSF"%massRegion] / result["highNLL"]["%s_OF"%massRegion]
			result["highNLL"]["%s_RSFOF_Fact_Err"%massRegion] = result["highNLL"]["%s_PredFactSystErrSF"%massRegion] / result["highNLL"]["%s_OF"%massRegion]
		else:
			result["highNLL"]["%s_RSFOF_Fact"%massRegion] = 0.
			result["highNLL"]["%s_RSFOF_Fact_Err"%massRegion] = 0.
		
		if result["highNLL"]["%s_OF"%massRegion] > 0:
			result["highNLL"]["%s_RSFOF_Combined"%massRegion],result["highNLL"]["%s_RSFOF_Combined_Err"%massRegion] = getWeightedAverage(result["highNLL"]["%s_RSFOF_Fact"%massRegion],result["highNLL"]["%s_RSFOF_Fact_Err"%massRegion],getattr(rSFOFDirect,region).val,getattr(rSFOFDirect,region).err)
		else:
			result["highNLL"]["%s_RSFOF_Combined"%massRegion] = getattr(rSFOFDirect,region).val
			result["highNLL"]["%s_RSFOF_Combined_Err"%massRegion] = getattr(rSFOFDirect,region).err
		
		result["highNLL"]["%s_PredSF"%massRegion] = result["highNLL"]["%s_OF"%massRegion]*result["highNLL"]["%s_RSFOF_Combined"%massRegion]
		if result["highNLL"]["%s_PredSF"%massRegion] > 0:
			result["highNLL"]["%s_PredStatUpSF"%massRegion] = yield_up*result["highNLL"]["%s_RSFOF_Combined"%massRegion] - result["highNLL"]["%s_PredSF"%massRegion]
		else:
			result["highNLL"]["%s_PredStatUpSF"%massRegion] =1.8*result["highNLL"]["%s_RSFOF_Combined"%massRegion]
		result["highNLL"]["%s_PredStatDownSF"%massRegion] = result["highNLL"]["%s_PredSF"%massRegion] - yield_down*result["highNLL"]["%s_RSFOF_Combined"%massRegion] 
		result["highNLL"]["%s_PredSystErrSF"%massRegion] = result["highNLL"]["%s_OF"%massRegion]*result["highNLL"]["%s_RSFOF_Combined_Err"%massRegion]
		
		result["highNLL"]["%s_ZPredSF"%massRegion] = shelve["onZICHEP"]["%s_%s_SF"%(massRegion,"highNLL")] - shelve["onZICHEP"]["%s_%s_OF"%(massRegion,"highNLL")]
		result["highNLL"]["%s_ZPredSF_Up"%massRegion] = shelve["onZICHEP"]["%s_%s_SF_Up"%(massRegion,"highNLL")] - shelve["onZICHEP"]["%s_%s_OF_Up"%(massRegion,"highNLL")]
		result["highNLL"]["%s_ZPredSF_Down"%massRegion] = shelve["onZICHEP"]["%s_%s_SF_Down"%(massRegion,"highNLL")] - shelve["onZICHEP"]["%s_%s_OF_Down"%(massRegion,"highNLL")]
		result["highNLL"]["%s_ZPredErrSF"%massRegion] = max(abs(result["highNLL"]["%s_ZPredSF_Up"%massRegion]-result["highNLL"]["%s_ZPredSF"%massRegion]),abs(result["highNLL"]["%s_ZPredSF_Down"%massRegion]-result["highNLL"]["%s_ZPredSF"%massRegion]))
		
		result["highNLL"]["%s_TotalPredSF"%massRegion] = result["highNLL"]["%s_PredSF"%massRegion] + result["highNLL"]["%s_ZPredSF"%massRegion]
		result["highNLL"]["%s_TotalPredErrUpSF"%massRegion] = ( result["highNLL"]["%s_PredStatUpSF"%massRegion]**2 +  result["highNLL"]["%s_PredSystErrSF"%massRegion]**2 + result["highNLL"]["%s_ZPredErrSF"%massRegion]**2 )**0.5
		result["highNLL"]["%s_TotalPredErrDownSF"%massRegion] = ( result["highNLL"]["%s_PredStatDownSF"%massRegion]**2 +  result["highNLL"]["%s_PredSystErrSF"%massRegion]**2 + result["highNLL"]["%s_ZPredErrSF"%massRegion]**2 )**0.5			
	
	
	return result
	
def getResultsLegacy(shelve,signalRegion):
	
	region = "central"
	result = {}
	
	result["rSFOF"] = getattr(rSFOF,region).val
	result["rSFOFErr"] = getattr(rSFOF,region).err
	result["rEEOF"] = getattr(rEEOF,region).val
	result["rEEOFErr"] = getattr(rEEOF,region).err
	result["rMMOF"] = getattr(rMMOF,region).val
	result["rMMOFErr"] = getattr(rMMOF,region).err
	
	result["onZPrediction"] = shelve["onZLegacy"]["86To96_SF"] - shelve["onZLegacy"]["86To96_OF"]
	
	## Rescale MC to unblinded dataset
	result["onZPrediction"] = result["onZPrediction"]  * 17.3/36.2
	
		
	result["EdgeMassEE"] = shelve[signalRegion]["default"]["edgeMass"]["EE"]
	result["EdgeMassMM"] = shelve[signalRegion]["default"]["edgeMass"]["MM"]
	result["EdgeMassSF"] = shelve[signalRegion]["default"]["edgeMass"]["EE"] + shelve[signalRegion]["default"]["edgeMass"]["MM"]
	result["EdgeMassOF"] = shelve[signalRegion]["default"]["edgeMass"]["EM"]
	
	result["EdgeMassOFRMuEScaled"] = shelve[signalRegion]["default"]["edgeMass"]["EMRMuEScaled"]
	result["EdgeMassOFRMuEScaledUp"] = shelve[signalRegion]["default"]["edgeMass"]["EMRMuEScaledUp"]
	result["EdgeMassOFRMuEScaledDown"] = shelve[signalRegion]["default"]["edgeMass"]["EMRMuEScaledDown"]
	
	
	
	yield_up = ROOT.Double(1.)
	yield_down = ROOT.Double(1.)
	## calculate poisson error
	ROOT.RooHistError.instance().getPoissonInterval(result["EdgeMassOF"],yield_down,yield_up,1.)
	
	yieldSF_up = ROOT.Double(1.)
	yieldSF_down = ROOT.Double(1.)
	ROOT.RooHistError.instance().getPoissonInterval(result["EdgeMassSF"],yieldSF_down,yieldSF_up,1.)
	
	result["EdgeMassSFUp"] = yieldSF_up - result["EdgeMassSF"]
	result["EdgeMassSFDown"] = result["EdgeMassSF"] - yieldSF_down
	
	result["EdgeMassPredFactSF"] = result["EdgeMassOFRMuEScaled"]*getattr(rSFOFTrig,region).val
	result["EdgeMassPredFactStatUpSF"] = yield_up*result["EdgeMassPredFactSF"]/result["EdgeMassOF"] - result["EdgeMassPredFactSF"]
	result["EdgeMassPredFactStatDownSF"] = result["EdgeMassPredFactSF"] - yield_down*result["EdgeMassPredFactSF"]/result["EdgeMassOF"]
	result["EdgeMassPredFactSystErrSF"] = result["EdgeMassOFRMuEScaled"]*(getattr(rSFOFTrig,region).err**2 + max(abs(result["EdgeMassOFRMuEScaled"] - result["EdgeMassOFRMuEScaledUp"])/result["EdgeMassOFRMuEScaled"],abs(result["EdgeMassOFRMuEScaled"] - result["EdgeMassOFRMuEScaledUp"])/result["EdgeMassOFRMuEScaled"])**2)**0.5		
	
	result["EdgeMassRSFOFFact"] = result["EdgeMassPredFactSF"] / result["EdgeMassOF"]
	result["EdgeMassRSFOFFactErr"] = result["EdgeMassPredFactSystErrSF"] / result["EdgeMassOF"]

	result["EdgeMassRSFOFCombined"],result["EdgeMassRSFOFCombinedErr"] = getWeightedAverage(result["EdgeMassRSFOFFact"],result["EdgeMassRSFOFFactErr"],getattr(rSFOFDirect,region).val,getattr(rSFOFDirect,region).err)
				
	result["EdgeMassPredSF"] = result["EdgeMassOF"]*result["EdgeMassRSFOFCombined"]
	result["EdgeMassPredStatUpSF"] = yield_up*result["EdgeMassRSFOFCombined"] - result["EdgeMassPredSF"] 
	result["EdgeMassPredStatDownSF"] = result["EdgeMassPredSF"]  - yield_down*result["EdgeMassRSFOFCombined"]
	result["EdgeMassPredSystErrSF"] = result["EdgeMassOF"]*result["EdgeMassRSFOFCombinedErr"]
			
			
	
	result["EdgeMassZPredSF"] = result["onZPrediction"]*getattr(rOutIn.edgeMass,region).val
	result["EdgeMassZPredErrSF"] =  ((result["onZPrediction"]*getattr(rOutIn.edgeMass,region).err)**2 + result["onZPrediction"] * getattr(rOutIn.edgeMass,region).val**2 )**0.5
					
	result["EdgeMassTotalPredSF"] = result["EdgeMassPredSF"] + result["EdgeMassZPredSF"]
	result["EdgeMassTotalPredErrUpSF"] = ( result["EdgeMassPredStatUpSF"]**2 +  result["EdgeMassPredSystErrSF"]**2 + result["EdgeMassZPredErrSF"]**2 )**0.5
	result["EdgeMassTotalPredErrDownSF"] = ( result["EdgeMassPredStatDownSF"]**2 +  result["EdgeMassPredSystErrSF"]**2 + result["EdgeMassZPredErrSF"]**2 )**0.5

	
	return result


def makeOverviewMllPlotBkgOnly(shelves,region,normalizeToBinWidth=False):


	colors = createMyColors()
	
	plot = getPlot("mllResultPlot")
	
	results = getResultsNLL(shelves,"NLL")
	
	
	histPred = ROOT.TH1F("histPred","histPred",len(plot.binning)-1, array("f",plot.binning))
	histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",len(plot.binning)-1, array("f",plot.binning))
	histDY = ROOT.TH1F("histDY","histDY",len(plot.binning)-1, array("f",plot.binning))
	histFullBG = ROOT.TH1F("histFullBG","histFullBG",len(plot.binning)-1, array("f",plot.binning))
	
				
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style = setTDRStyle()
	style.SetPadTopMargin(0.07)
	ROOT.gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()
	
	
	histFlavSym.SetBinContent(1,results[region]["highMT2_mass20To60_PredSF"])
	histFlavSym.SetBinContent(2,results[region]["highMT2_mass60To86_PredSF"])
	histFlavSym.SetBinContent(3,0)
	histFlavSym.SetBinContent(4,results[region]["highMT2_mass96To150_PredSF"])
	histFlavSym.SetBinContent(5,results[region]["highMT2_mass150To200_PredSF"])
	histFlavSym.SetBinContent(6,results[region]["highMT2_mass200To300_PredSF"])
	histFlavSym.SetBinContent(7,results[region]["highMT2_mass300To400_PredSF"])
	histFlavSym.SetBinContent(8,results[region]["highMT2_mass400_PredSF"])

	histDY.SetBinContent(1,results[region]["highMT2_mass20To60_ZPredSF"])
	histDY.SetBinContent(2,results[region]["highMT2_mass60To86_ZPredSF"])
	histDY.SetBinContent(3,0)
	histDY.SetBinContent(4,results[region]["highMT2_mass96To150_ZPredSF"])
	histDY.SetBinContent(5,results[region]["highMT2_mass150To200_ZPredSF"])
	histDY.SetBinContent(6,results[region]["highMT2_mass200To300_ZPredSF"])
	histDY.SetBinContent(7,results[region]["highMT2_mass300To400_ZPredSF"])
	histDY.SetBinContent(8,results[region]["highMT2_mass400_ZPredSF"])	
	
	errGraph = ROOT.TGraphAsymmErrors()
	
	for i in range(1,histFlavSym.GetNbinsX()+1):
		if i <= 3:
			errGraph.SetPoint(i,histFlavSym.GetBinCenter(i),histFlavSym.GetBinContent(i)+histDY.GetBinContent(i))
		else:
			errGraph.SetPoint(i-1,histFlavSym.GetBinCenter(i),histFlavSym.GetBinContent(i)+histDY.GetBinContent(i))
		

	errGraph.SetPointError(1,0.5*histFlavSym.GetBinWidth(1),0.5*histFlavSym.GetBinWidth(1),results[region]["highMT2_mass20To60_TotalPredErrDownSF"],results[region]["highMT2_mass20To60_TotalPredErrUpSF"])
	errGraph.SetPointError(2,0.5*histFlavSym.GetBinWidth(2),0.5*histFlavSym.GetBinWidth(2),results[region]["highMT2_mass60To86_TotalPredErrDownSF"],results[region]["highMT2_mass60To86_TotalPredErrUpSF"])
	#~ errGraph.SetPointError(3,0.5*histFlavSym.GetBinWidth(3),0.5*histFlavSym.GetBinWidth(3),0,0)
	errGraph.SetPointError(3,0.5*histFlavSym.GetBinWidth(4),0.5*histFlavSym.GetBinWidth(4),results[region]["highMT2_mass96To150_TotalPredErrDownSF"],results[region]["highMT2_mass96To150_TotalPredErrUpSF"])
	errGraph.SetPointError(4,0.5*histFlavSym.GetBinWidth(5),0.5*histFlavSym.GetBinWidth(5),results[region]["highMT2_mass150To200_TotalPredErrDownSF"],results[region]["highMT2_mass150To200_TotalPredErrUpSF"])
	errGraph.SetPointError(5,0.5*histFlavSym.GetBinWidth(6),0.5*histFlavSym.GetBinWidth(6),results[region]["highMT2_mass200To300_TotalPredErrDownSF"],results[region]["highMT2_mass200To300_TotalPredErrUpSF"])
	errGraph.SetPointError(6,0.5*histFlavSym.GetBinWidth(7),0.5*histFlavSym.GetBinWidth(7),results[region]["highMT2_mass300To400_TotalPredErrDownSF"],results[region]["highMT2_mass300To400_TotalPredErrUpSF"])
	errGraph.SetPointError(7,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),results[region]["highMT2_mass400_TotalPredErrDownSF"],results[region]["highMT2_mass400_TotalPredErrUpSF"])
	
	errGraph.SetFillColor(myColors["MyBlueOverview"])
	errGraph.SetFillStyle(3002)	
	errGraph.SetLineWidth(0)	
	
	histFlavSym.SetLineColor(ROOT.kBlue+3)
	histFlavSym.SetLineWidth(2)
	
	histDY.SetLineColor(ROOT.kGreen+3)
	histDY.SetFillColor(ROOT.kGreen+3)
	#~ histDY.SetFillStyle(3002)


	#~ histFlavSym.SetFillColor(ROOT.kBlue-2)
	#~ histDY.SetFillColor(ROOT.kGreen+2)
	
	if normalizeToBinWidth:
		print histFlavSym.GetNbinsX()
		for i in range(1,histFlavSym.GetNbinsX()+1):
			if i < 3:
				histFlavSym.SetBinContent(i,histFlavSym.GetBinContent(i)/histFlavSym.GetBinWidth(i))
				histDY.SetBinContent(i,histDY.GetBinContent(i)/histDY.GetBinWidth(i))
				errGraph.SetPoint(i,histFlavSym.GetBinCenter(i),histFlavSym.GetBinContent(i)+histDY.GetBinContent(i))
				errGraph.SetPointError(i,0.5*histFlavSym.GetBinWidth(i),0.5*histFlavSym.GetBinWidth(i),errGraph.GetErrorYlow(i)/histFlavSym.GetBinWidth(i),errGraph.GetErrorYhigh(i)/histFlavSym.GetBinWidth(i))
			elif i > 3 and i < histFlavSym.GetNbinsX():
				histFlavSym.SetBinContent(i,histFlavSym.GetBinContent(i)/histFlavSym.GetBinWidth(i))
				histDY.SetBinContent(i,histDY.GetBinContent(i)/histDY.GetBinWidth(i))
				errGraph.SetPoint(i-1,histFlavSym.GetBinCenter(i),histFlavSym.GetBinContent(i)+histDY.GetBinContent(i))
				errGraph.SetPointError(i-1,0.5*histFlavSym.GetBinWidth(i),0.5*histFlavSym.GetBinWidth(i),errGraph.GetErrorYlow(i-1)/histFlavSym.GetBinWidth(i),errGraph.GetErrorYhigh(i-1)/histFlavSym.GetBinWidth(i))
			elif i == histFlavSym.GetNbinsX():
				histFlavSym.SetBinContent(i,histFlavSym.GetBinContent(i)/histFlavSym.GetBinWidth(i-1))
				histDY.SetBinContent(i,histDY.GetBinContent(i)/histDY.GetBinWidth(i-1))
				errGraph.SetPoint(i-1,histFlavSym.GetBinCenter(i),histFlavSym.GetBinContent(i)+histDY.GetBinContent(i))
				errGraph.SetPointError(i-1,0.5*histFlavSym.GetBinWidth(i),0.5*histFlavSym.GetBinWidth(i),errGraph.GetErrorYlow(i-1)/histFlavSym.GetBinWidth(i-1),errGraph.GetErrorYhigh(i-1)/histFlavSym.GetBinWidth(i-1))
	
	
	from ROOT import THStack
	
	stack = THStack()
	stack.Add(histDY)	
	stack.Add(histFlavSym)
	
	histFullBG.Add(histDY)	
	histFullBG.Add(histFlavSym)
	
	
	ymax = histFullBG.GetBinContent(histFullBG.GetMaximumBin()) * 2.
	ymin = 0
	if region == "highNLL":
		regionLabel = "non t#bar{t} like signal region"
	else:
		regionLabel = "t#bar{t} like signal region"

	
	
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

	latex.DrawLatex(0.95, 0.95, "%s fb^{-1} (13 TeV)"%"36.2")
	
	cmsExtra = "Preliminary"
	latexCMS.DrawLatex(0.18,0.87,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.80	
	else:
		yLabelPos = 0.83	

	latexCMSExtra.DrawLatex(0.18,yLabelPos,"%s"%(cmsExtra))
	

	leg = ROOT.TLegend(0.55, 0.45, 0.95, 0.92,regionLabel,"brNDC")

	#~ leg.SetNColumns(2)
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)
	
	bkgHistForLegend = histFlavSym.Clone("bkgHistForLegend")
	bkgHistForLegend.SetLineColor(ROOT.kBlue+3)
	bkgHistForLegend.SetFillColor(ROOT.kWhite)
	bkgHistForLegend.SetLineWidth(2)
	
	leg.AddEntry(bkgHistForLegend, "Flavor symmetric","f")
	leg.AddEntry(histDY,"Drell-Yan", "f")
	leg.AddEntry(errGraph,"Total uncertainty", "f")	
	

	#~ errGraph.Draw("same02")
	stack.Draw("samehist")	
	errGraph.Draw("same02")
	
	
	leg.Draw("same")


	plotPad.RedrawAxis()	
	
	ROOT.gPad.RedrawAxis()
	plotPad.RedrawAxis()
	
	hCanvas.Print("cutNCountResultMllBkgOnly_%s.pdf"%region)

def makeOverviewMllPlot(shelves,region,normalizeToBinWidth=False):


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
	
	histObs.SetBinContent(1,results[region]["highMT2_mass20To60_SF"])
	histObs.SetBinContent(2,results[region]["highMT2_mass60To86_SF"])
	histObs.SetBinContent(3,0)
	histObs.SetBinContent(4,results[region]["highMT2_mass96To150_SF"])
	histObs.SetBinContent(5,results[region]["highMT2_mass150To200_SF"])
	histObs.SetBinContent(6,results[region]["highMT2_mass200To300_SF"])
	histObs.SetBinContent(7,results[region]["highMT2_mass300To400_SF"])
	histObs.SetBinContent(8,results[region]["highMT2_mass400_SF"])	
	
	histFlavSym.SetBinContent(1,results[region]["highMT2_mass20To60_PredSF"])
	histFlavSym.SetBinContent(2,results[region]["highMT2_mass60To86_PredSF"])
	histFlavSym.SetBinContent(3,0)
	histFlavSym.SetBinContent(4,results[region]["highMT2_mass96To150_PredSF"])
	histFlavSym.SetBinContent(5,results[region]["highMT2_mass150To200_PredSF"])
	histFlavSym.SetBinContent(6,results[region]["highMT2_mass200To300_PredSF"])
	histFlavSym.SetBinContent(7,results[region]["highMT2_mass300To400_PredSF"])
	histFlavSym.SetBinContent(8,results[region]["highMT2_mass400_PredSF"])

	histDY.SetBinContent(1,results[region]["highMT2_mass20To60_ZPredSF"])
	histDY.SetBinContent(2,results[region]["highMT2_mass60To86_ZPredSF"])
	histDY.SetBinContent(3,0)
	histDY.SetBinContent(4,results[region]["highMT2_mass96To150_ZPredSF"])
	histDY.SetBinContent(5,results[region]["highMT2_mass150To200_ZPredSF"])
	histDY.SetBinContent(6,results[region]["highMT2_mass200To300_ZPredSF"])
	histDY.SetBinContent(7,results[region]["highMT2_mass300To400_ZPredSF"])
	histDY.SetBinContent(8,results[region]["highMT2_mass400_ZPredSF"])	
	
	histRare.SetBinContent(1,results[region]["highMT2_mass20To60_RarePredSF"])
	histRare.SetBinContent(2,results[region]["highMT2_mass60To86_RarePredSF"])
	histRare.SetBinContent(3,0)
	histRare.SetBinContent(4,results[region]["highMT2_mass96To150_RarePredSF"])
	histRare.SetBinContent(5,results[region]["highMT2_mass150To200_RarePredSF"])
	histRare.SetBinContent(6,results[region]["highMT2_mass200To300_RarePredSF"])
	histRare.SetBinContent(7,results[region]["highMT2_mass300To400_RarePredSF"])
	histRare.SetBinContent(8,results[region]["highMT2_mass400_RarePredSF"])	
	
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
		

	graphObs.SetPointError(1,0,0,results[region]["highMT2_mass20To60_SFDown"],results[region]["highMT2_mass20To60_SFUp"])
	graphObs.SetPointError(2,0,0,results[region]["highMT2_mass60To86_SFDown"],results[region]["highMT2_mass60To86_SFUp"])
	graphObs.SetPointError(3,0,0,results[region]["highMT2_mass96To150_SFDown"],results[region]["highMT2_mass96To150_SFUp"])
	graphObs.SetPointError(4,0,0,results[region]["highMT2_mass150To200_SFDown"],results[region]["highMT2_mass150To200_SFUp"])
	graphObs.SetPointError(5,0,0,results[region]["highMT2_mass200To300_SFDown"],results[region]["highMT2_mass200To300_SFUp"])
	graphObs.SetPointError(6,0,0,results[region]["highMT2_mass300To400_SFDown"],results[region]["highMT2_mass300To400_SFUp"])
	graphObs.SetPointError(7,0,0,results[region]["highMT2_mass400_SFDown"],results[region]["highMT2_mass400_SFUp"])

	errGraph.SetPointError(1,0.5*histFlavSym.GetBinWidth(1),0.5*histFlavSym.GetBinWidth(1),results[region]["highMT2_mass20To60_TotalPredErrDownSF"],results[region]["highMT2_mass20To60_TotalPredErrUpSF"])
	errGraph.SetPointError(2,0.5*histFlavSym.GetBinWidth(2),0.5*histFlavSym.GetBinWidth(2),results[region]["highMT2_mass60To86_TotalPredErrDownSF"],results[region]["highMT2_mass60To86_TotalPredErrUpSF"])
	errGraph.SetPointError(3,0.5*histFlavSym.GetBinWidth(4),0.5*histFlavSym.GetBinWidth(4),results[region]["highMT2_mass96To150_TotalPredErrDownSF"],results[region]["highMT2_mass96To150_TotalPredErrUpSF"])
	errGraph.SetPointError(4,0.5*histFlavSym.GetBinWidth(5),0.5*histFlavSym.GetBinWidth(5),results[region]["highMT2_mass150To200_TotalPredErrDownSF"],results[region]["highMT2_mass150To200_TotalPredErrUpSF"])
	errGraph.SetPointError(5,0.5*histFlavSym.GetBinWidth(6),0.5*histFlavSym.GetBinWidth(6),results[region]["highMT2_mass200To300_TotalPredErrDownSF"],results[region]["highMT2_mass200To300_TotalPredErrUpSF"])
	errGraph.SetPointError(6,0.5*histFlavSym.GetBinWidth(7),0.5*histFlavSym.GetBinWidth(7),results[region]["highMT2_mass300To400_TotalPredErrDownSF"],results[region]["highMT2_mass300To400_TotalPredErrUpSF"])
	errGraph.SetPointError(7,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),results[region]["highMT2_mass400_TotalPredErrDownSF"],results[region]["highMT2_mass400_TotalPredErrUpSF"])
	
	errGraphRatio.SetPointError(1,0.5*histFlavSym.GetBinWidth(1),0.5*histFlavSym.GetBinWidth(1),results[region]["highMT2_mass20To60_TotalPredErrDownSF"]/results[region]["highMT2_mass20To60_TotalPredSF"],results[region]["highMT2_mass20To60_TotalPredErrUpSF"]/results[region]["highMT2_mass20To60_TotalPredSF"])
	errGraphRatio.SetPointError(2,0.5*histFlavSym.GetBinWidth(2),0.5*histFlavSym.GetBinWidth(2),results[region]["highMT2_mass60To86_TotalPredErrDownSF"]/results[region]["highMT2_mass60To86_TotalPredSF"],results[region]["highMT2_mass60To86_TotalPredErrUpSF"]/results[region]["highMT2_mass60To86_TotalPredSF"])
	errGraphRatio.SetPointError(3,0.5*histFlavSym.GetBinWidth(4),0.5*histFlavSym.GetBinWidth(4),results[region]["highMT2_mass96To150_TotalPredErrDownSF"]/results[region]["highMT2_mass96To150_TotalPredSF"],results[region]["highMT2_mass96To150_TotalPredErrUpSF"]/results[region]["highMT2_mass96To150_TotalPredSF"])
	errGraphRatio.SetPointError(4,0.5*histFlavSym.GetBinWidth(5),0.5*histFlavSym.GetBinWidth(5),results[region]["highMT2_mass150To200_TotalPredErrDownSF"]/results[region]["highMT2_mass150To200_TotalPredSF"],results[region]["highMT2_mass150To200_TotalPredErrUpSF"]/results[region]["highMT2_mass150To200_TotalPredSF"])
	errGraphRatio.SetPointError(5,0.5*histFlavSym.GetBinWidth(6),0.5*histFlavSym.GetBinWidth(6),results[region]["highMT2_mass200To300_TotalPredErrDownSF"]/results[region]["highMT2_mass200To300_TotalPredSF"],results[region]["highMT2_mass200To300_TotalPredErrUpSF"]/results[region]["highMT2_mass200To300_TotalPredSF"])
	errGraphRatio.SetPointError(6,0.5*histFlavSym.GetBinWidth(7),0.5*histFlavSym.GetBinWidth(7),results[region]["highMT2_mass300To400_TotalPredErrDownSF"]/results[region]["highMT2_mass300To400_TotalPredSF"],results[region]["highMT2_mass300To400_TotalPredErrUpSF"]/results[region]["highMT2_mass300To400_TotalPredSF"])
	errGraphRatio.SetPointError(7,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),results[region]["highMT2_mass400_TotalPredErrDownSF"]/results[region]["highMT2_mass400_TotalPredSF"],results[region]["highMT2_mass400_TotalPredErrUpSF"]/results[region]["highMT2_mass400_TotalPredSF"])
	
	errGraph.SetFillColor(myColors["MyBlueOverview"])
	errGraph.SetFillStyle(3354)	
	errGraph.SetLineWidth(0)	
	
	errGraphRatio.SetFillColor(myColors["MyBlueOverview"])
	errGraphRatio.SetFillStyle(3354)

	histFlavSym.SetLineColor(ROOT.kBlue+3)
	histFlavSym.SetLineWidth(2)
	
	histDY.SetLineColor(ROOT.kGreen+3)
	histDY.SetFillColor(ROOT.kGreen+3)
	#~ histDY.SetFillStyle(3002)
	
	histRare.SetLineColor(ROOT.kViolet+2)
	histRare.SetFillColor(ROOT.kViolet+2)

	
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
	if region == "highNLL":
		regionLabel = "non t#bar{t} like signal region"
	else:
		regionLabel = "t#bar{t} like signal region"

	
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
	

	leg = ROOT.TLegend(0.55, 0.45, 0.95, 0.92,regionLabel,"brNDC")

	#~ leg.SetNColumns(2)
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)
	
	bkgHistForLegend = histFlavSym.Clone("bkgHistForLegend")
	bkgHistForLegend.SetLineColor(ROOT.kBlue+3)
	bkgHistForLegend.SetFillColor(ROOT.kWhite)
	bkgHistForLegend.SetLineWidth(2)
	
	#~ leg.AddEntry(histObs,"Data","pe")
	leg.AddEntry(graphObs,"Data","pe")
	#~ leg.AddEntry(histFlavSym, "Total backgrounds","l")
	leg.AddEntry(bkgHistForLegend, "FS","f")
	leg.AddEntry(errGraph,"Tot. unc.", "f")	
	leg.AddEntry(histDY,"Template", "f")
	leg.AddEntry(histRare,"Rares", "f")	

	errGraph.Draw("same02")
	stack.Draw("samehist")	
	
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
	hAxis.SetYTitle("#frac{Data}{Prediction}  ")
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
	
	hCanvas.Print("cutNCountResultMll_%s.pdf"%region)
	
def makeOverviewPlot(shelves):

	from helpers import createMyColors
	from defs import myColors
	colors = createMyColors()	

	
	resultsNLL = getResultsNLL(shelves,"NLL")
	resultsLegacy = getResultsLegacy(shelves,"legacy")
	
	
	histObs = ROOT.TH1F("histObs","histObs",16,0,16)
	
	histObs.SetMarkerColor(ROOT.kBlack)
	histObs.SetLineColor(ROOT.kBlack)
	histObs.SetMarkerStyle(20)
	
	histPred = ROOT.TH1F("histPred","histPred",16,0,16)
	histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",16,0,16)
	histDY = ROOT.TH1F("histDY","histDY",16,0,16)
	
	hCanvas = TCanvas("hCanvas", "Distribution", 1000,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style=setTDRStyle()
	style.SetPadBottomMargin(0.3)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()
	plotPad.SetLogy()	
	
	
	histObs.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_mass20To60_SF"])
	histObs.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_mass60To86_SF"])
	histObs.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_mass96To150_SF"])
	histObs.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_mass150To200_SF"])
	histObs.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_mass200To300_SF"])
	histObs.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_mass300To400_SF"])
	histObs.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_mass400_SF"])	
	
	histObs.SetBinContent(8,resultsNLL["highNLL"]["highMT2_mass20To60_SF"])
	histObs.SetBinContent(9,resultsNLL["highNLL"]["highMT2_mass60To86_SF"])
	histObs.SetBinContent(10,resultsNLL["highNLL"]["highMT2_mass96To150_SF"])
	histObs.SetBinContent(11,resultsNLL["highNLL"]["highMT2_mass150To200_SF"])
	histObs.SetBinContent(12,resultsNLL["highNLL"]["highMT2_mass200To300_SF"])
	histObs.SetBinContent(13,resultsNLL["highNLL"]["highMT2_mass300To400_SF"])
	histObs.SetBinContent(14,resultsNLL["highNLL"]["highMT2_mass400_SF"])	
	
	histObs.SetBinContent(15,resultsNLL["highNLL"]["highMassOld_SF"])	
	histObs.SetBinContent(16,resultsLegacy["EdgeMassSF"])	

	
	
	names = ["m_{ll}: 20-60 GeV","m_{ll}: 60-86 GeV","m_{ll}: 96-150 GeV","m_{ll}: 150-200 GeV","m_{ll}: 200-300 GeV","m_{ll}: 300-400 GeV","m_{ll}: > 400 GeV","m_{ll}: 20-60 GeV","m_{ll}: 60-86 GeV","m_{ll}: 96-150 GeV","m_{ll}: 150-200 GeV","m_{ll}: 200-300 GeV","m_{ll}: 300-400 GeV","m_{ll}: > 400 GeV","ICHEP legacy","8 TeV legacy"]
	
	for index, name in enumerate(names):
	
		histObs.GetXaxis().SetBinLabel(index+1,name)
		
	histFlavSym.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_mass20To60_PredSF"])
	histFlavSym.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_mass60To86_PredSF"])
	histFlavSym.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_mass96To150_PredSF"])
	histFlavSym.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_mass150To200_PredSF"])
	histFlavSym.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_mass200To300_PredSF"])
	histFlavSym.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_mass300To400_PredSF"])
	histFlavSym.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_mass400_PredSF"])	
	
	histFlavSym.SetBinContent(8,resultsNLL["highNLL"]["highMT2_mass20To60_PredSF"])
	histFlavSym.SetBinContent(9,resultsNLL["highNLL"]["highMT2_mass60To86_PredSF"])
	histFlavSym.SetBinContent(10,resultsNLL["highNLL"]["highMT2_mass96To150_PredSF"])
	histFlavSym.SetBinContent(11,resultsNLL["highNLL"]["highMT2_mass150To200_PredSF"])
	histFlavSym.SetBinContent(12,resultsNLL["highNLL"]["highMT2_mass200To300_PredSF"])
	histFlavSym.SetBinContent(13,resultsNLL["highNLL"]["highMT2_mass300To400_PredSF"])
	histFlavSym.SetBinContent(14,resultsNLL["highNLL"]["highMT2_mass400_PredSF"])	
	
	histFlavSym.SetBinContent(15,resultsNLL["highNLL"]["highMassOld_PredSF"])	
	histFlavSym.SetBinContent(16,resultsLegacy["EdgeMassPredSF"])

	histDY.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_mass20To60_ZPredSF"])
	histDY.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_mass60To86_ZPredSF"])
	histDY.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_mass96To150_ZPredSF"])
	histDY.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_mass150To200_ZPredSF"])
	histDY.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_mass200To300_ZPredSF"])
	histDY.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_mass300To400_ZPredSF"])
	histDY.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_mass400_ZPredSF"])	
	
	histDY.SetBinContent(8,resultsNLL["highNLL"]["highMT2_mass20To60_ZPredSF"])
	histDY.SetBinContent(9,resultsNLL["highNLL"]["highMT2_mass60To86_ZPredSF"])
	histDY.SetBinContent(10,resultsNLL["highNLL"]["highMT2_mass96To150_ZPredSF"])
	histDY.SetBinContent(11,resultsNLL["highNLL"]["highMT2_mass150To200_ZPredSF"])
	histDY.SetBinContent(12,resultsNLL["highNLL"]["highMT2_mass200To300_ZPredSF"])
	histDY.SetBinContent(13,resultsNLL["highNLL"]["highMT2_mass300To400_ZPredSF"])
	histDY.SetBinContent(14,resultsNLL["highNLL"]["highMT2_mass400_ZPredSF"])	
	
	histDY.SetBinContent(15,resultsNLL["highNLL"]["highMassOld_ZPredSF"])	
	histDY.SetBinContent(16,resultsLegacy["EdgeMassZPredSF"])

	errGraph = ROOT.TGraphAsymmErrors()
	graphObs = ROOT.TGraphAsymmErrors()
	
	for i in range(1,histFlavSym.GetNbinsX()+1):
		graphObs.SetPoint(i,histObs.GetBinCenter(i),histObs.GetBinContent(i))
		errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histDY.GetBinContent(i))
		
		

	graphObs.SetPointError(1,0,0,resultsNLL["lowNLL"]["highMT2_mass20To60_SFDown"],resultsNLL["lowNLL"]["highMT2_mass20To60_SFUp"])
	graphObs.SetPointError(2,0,0,resultsNLL["lowNLL"]["highMT2_mass60To86_SFDown"],resultsNLL["lowNLL"]["highMT2_mass60To86_SFUp"])
	graphObs.SetPointError(3,0,0,resultsNLL["lowNLL"]["highMT2_mass96To150_SFDown"],resultsNLL["lowNLL"]["highMT2_mass96To150_SFUp"])
	graphObs.SetPointError(4,0,0,resultsNLL["lowNLL"]["highMT2_mass150To200_SFDown"],resultsNLL["lowNLL"]["highMT2_mass150To200_SFUp"])
	graphObs.SetPointError(5,0,0,resultsNLL["lowNLL"]["highMT2_mass200To300_SFDown"],resultsNLL["lowNLL"]["highMT2_mass200To300_SFUp"])
	graphObs.SetPointError(6,0,0,resultsNLL["lowNLL"]["highMT2_mass300To400_SFDown"],resultsNLL["lowNLL"]["highMT2_mass300To400_SFUp"])
	graphObs.SetPointError(7,0,0,resultsNLL["lowNLL"]["highMT2_mass400_SFDown"],resultsNLL["lowNLL"]["highMT2_mass400_SFUp"])

	graphObs.SetPointError(8,0,0,resultsNLL["highNLL"]["highMT2_mass20To60_SFDown"],resultsNLL["highNLL"]["highMT2_mass20To60_SFUp"])
	graphObs.SetPointError(9,0,0,resultsNLL["highNLL"]["highMT2_mass60To86_SFDown"],resultsNLL["highNLL"]["highMT2_mass60To86_SFUp"])
	graphObs.SetPointError(10,0,0,resultsNLL["highNLL"]["highMT2_mass96To150_SFDown"],resultsNLL["highNLL"]["highMT2_mass96To150_SFUp"])
	graphObs.SetPointError(11,0,0,resultsNLL["highNLL"]["highMT2_mass150To200_SFDown"],resultsNLL["highNLL"]["highMT2_mass150To200_SFUp"])
	graphObs.SetPointError(12,0,0,resultsNLL["highNLL"]["highMT2_mass200To300_SFDown"],resultsNLL["highNLL"]["highMT2_mass200To300_SFUp"])
	graphObs.SetPointError(13,0,0,resultsNLL["highNLL"]["highMT2_mass300To400_SFDown"],resultsNLL["highNLL"]["highMT2_mass300To400_SFUp"])
	graphObs.SetPointError(14,0,0,resultsNLL["highNLL"]["highMT2_mass400_SFDown"],resultsNLL["highNLL"]["highMT2_mass400_SFUp"])
	
	graphObs.SetPointError(15,0,0,resultsNLL["highNLL"]["highMassOld_SFDown"],resultsNLL["highNLL"]["highMassOld_SFUp"])
	graphObs.SetPointError(16,0,0,resultsLegacy["EdgeMassSFDown"],resultsLegacy["EdgeMassSFUp"])


	errGraph.SetPointError(1,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass20To60_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass20To60_TotalPredErrUpSF"])
	errGraph.SetPointError(2,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass60To86_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass60To86_TotalPredErrUpSF"])
	errGraph.SetPointError(3,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass96To150_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass96To150_TotalPredErrUpSF"])
	errGraph.SetPointError(4,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass150To200_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass150To200_TotalPredErrUpSF"])
	errGraph.SetPointError(5,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass200To300_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass200To300_TotalPredErrUpSF"])
	errGraph.SetPointError(6,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass300To400_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass300To400_TotalPredErrUpSF"])
	errGraph.SetPointError(7,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass400_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass400_TotalPredErrUpSF"])
	
	errGraph.SetPointError(8,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass20To60_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass20To60_TotalPredErrUpSF"])
	errGraph.SetPointError(9,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass60To86_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass60To86_TotalPredErrUpSF"])
	errGraph.SetPointError(10,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass96To150_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass96To150_TotalPredErrUpSF"])
	errGraph.SetPointError(11,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass150To200_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass150To200_TotalPredErrUpSF"])
	errGraph.SetPointError(12,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass200To300_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass200To300_TotalPredErrUpSF"])
	errGraph.SetPointError(13,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass300To400_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass300To400_TotalPredErrUpSF"])
	errGraph.SetPointError(14,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass400_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass400_TotalPredErrUpSF"])
	
	errGraph.SetPointError(15,0.5,0.5,resultsNLL["highNLL"]["highMassOld_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMassOld_TotalPredErrUpSF"])
	errGraph.SetPointError(16,0.5,0.5,resultsLegacy["EdgeMassTotalPredErrDownSF"],resultsLegacy["EdgeMassTotalPredErrUpSF"])

	errGraph.SetFillColor(myColors["MyBlueOverview"])
	errGraph.SetFillStyle(3354)	

	histFlavSym.SetLineColor(ROOT.kBlue+3)
	histFlavSym.SetLineWidth(2)
	
	histDY.SetLineColor(ROOT.kGreen+3)
	histDY.SetFillColor(ROOT.kGreen+3)
	#~ histDY.SetFillStyle(3002)
	
	from ROOT import THStack
	
	stack = THStack()
	stack.Add(histDY)	
	stack.Add(histFlavSym)	
	
	histObs.GetYaxis().SetRangeUser(0.5,90000)
	histObs.GetYaxis().SetTitle("Events")
	histObs.LabelsOption("v")

	histObs.UseCurrentStyle()
	histObs.Draw("pe")

	
	
	#~ hCanvas.DrawFrame(-0.5,0,30.5,65,"; %s ; %s" %("","Events"))
	
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

	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%"35.9")
	
	#~ cmsExtra = "Preliminary"
	cmsExtra = ""
	latexCMS.DrawLatex(0.19,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))

	leg = ROOT.TLegend(0.37, 0.7, 0.89, 0.95,"","brNDC")
	leg.SetNColumns(2)
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)
	
	bkgHistForLegend = histFlavSym.Clone("bkgHistForLegend")
	bkgHistForLegend.SetLineColor(ROOT.kBlue+3)
	bkgHistForLegend.SetFillColor(ROOT.kWhite)
	bkgHistForLegend.SetLineWidth(2)
	
	leg.AddEntry(histObs,"Data","pe")
	#~ leg.AddEntry(histFlavSym, "Total backgrounds","l")
	leg.AddEntry(bkgHistForLegend, "Flavor symmetric","f")
	leg.AddEntry(histDY,"Non FS", "f")
	leg.AddEntry(errGraph,"Total uncertainty", "f")	
	

	errGraph.Draw("same02")
	stack.Draw("samehist")	
	
	graphObs.Draw("pesame")
	
	leg.Draw("same")

	
	
	line1 = ROOT.TLine(7,0,7,500)
	line2 = ROOT.TLine(14,0,14,500)
	line3 = ROOT.TLine(15,0,15,300)

	line1.SetLineColor(ROOT.kBlack)
	line2.SetLineColor(ROOT.kBlack)
	line3.SetLineColor(ROOT.kBlack)

	line1.SetLineWidth(2)
	line2.SetLineWidth(2)
	line3.SetLineWidth(2)

	line1.Draw("same")
	line2.Draw("same")
	line3.Draw("same")
	


	label = ROOT.TLatex()
	label.SetTextAlign(12)
	label.SetTextSize(0.04)
	label.SetTextColor(ROOT.kBlack)	
	label.SetTextAlign(22)	
	#~ label.SetTextAngle(-45)	
	
	label.DrawLatex(3.5,400,"t#bar{t} like")
	label.DrawLatex(10.5,400,"non t#bar{t} like")
	

	plotPad.RedrawAxis()
	
	hCanvas.Print("edgeOverview.pdf")
	#~ hCanvas.Print("edgeOverview.root")
	
def makeOverviewPlotNoLegacy(shelves):

	from helpers import createMyColors
	from defs import myColors
	colors = createMyColors()	

	
	resultsNLL = getResultsNLL(shelves,"NLL")
	
	
	histObs = ROOT.TH1F("histObs","histObs",14,0,14)
	
	histObs.SetMarkerColor(ROOT.kBlack)
	histObs.SetLineColor(ROOT.kBlack)
	histObs.SetMarkerStyle(20)
	
	histPred = ROOT.TH1F("histPred","histPred",14,0,14)
	histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",14,0,14)
	histDY = ROOT.TH1F("histDY","histDY",14,0,14)
	histRare = ROOT.TH1F("histRare","histRare",14,0,14)
	
	hCanvas = TCanvas("hCanvas", "Distribution", 1000,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style=setTDRStyle()
	style.SetPadBottomMargin(0.28)
	style.SetPadLeftMargin(0.13)
	style.SetTitleYOffset(0.9)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()
	plotPad.SetLogy()	
	
	
	histObs.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_mass20To60_SF"])
	histObs.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_mass60To86_SF"])
	histObs.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_mass96To150_SF"])
	histObs.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_mass150To200_SF"])
	histObs.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_mass200To300_SF"])
	histObs.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_mass300To400_SF"])
	histObs.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_mass400_SF"])	
	
	histObs.SetBinContent(8,resultsNLL["highNLL"]["highMT2_mass20To60_SF"])
	histObs.SetBinContent(9,resultsNLL["highNLL"]["highMT2_mass60To86_SF"])
	histObs.SetBinContent(10,resultsNLL["highNLL"]["highMT2_mass96To150_SF"])
	histObs.SetBinContent(11,resultsNLL["highNLL"]["highMT2_mass150To200_SF"])
	histObs.SetBinContent(12,resultsNLL["highNLL"]["highMT2_mass200To300_SF"])
	histObs.SetBinContent(13,resultsNLL["highNLL"]["highMT2_mass300To400_SF"])
	histObs.SetBinContent(14,resultsNLL["highNLL"]["highMT2_mass400_SF"])	

	
	
	names = ["m_{ll}: 20-60 GeV","m_{ll}: 60-86 GeV","m_{ll}: 96-150 GeV","m_{ll}: 150-200 GeV","m_{ll}: 200-300 GeV","m_{ll}: 300-400 GeV","m_{ll}: > 400 GeV","m_{ll}: 20-60 GeV","m_{ll}: 60-86 GeV","m_{ll}: 96-150 GeV","m_{ll}: 150-200 GeV","m_{ll}: 200-300 GeV","m_{ll}: 300-400 GeV","m_{ll}: > 400 GeV"]
	
	for index, name in enumerate(names):
	
		histObs.GetXaxis().SetBinLabel(index+1,name)
		
	histFlavSym.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_mass20To60_PredSF"])
	histFlavSym.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_mass60To86_PredSF"])
	histFlavSym.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_mass96To150_PredSF"])
	histFlavSym.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_mass150To200_PredSF"])
	histFlavSym.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_mass200To300_PredSF"])
	histFlavSym.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_mass300To400_PredSF"])
	histFlavSym.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_mass400_PredSF"])	
	
	histFlavSym.SetBinContent(8,resultsNLL["highNLL"]["highMT2_mass20To60_PredSF"])
	histFlavSym.SetBinContent(9,resultsNLL["highNLL"]["highMT2_mass60To86_PredSF"])
	histFlavSym.SetBinContent(10,resultsNLL["highNLL"]["highMT2_mass96To150_PredSF"])
	histFlavSym.SetBinContent(11,resultsNLL["highNLL"]["highMT2_mass150To200_PredSF"])
	histFlavSym.SetBinContent(12,resultsNLL["highNLL"]["highMT2_mass200To300_PredSF"])
	histFlavSym.SetBinContent(13,resultsNLL["highNLL"]["highMT2_mass300To400_PredSF"])
	histFlavSym.SetBinContent(14,resultsNLL["highNLL"]["highMT2_mass400_PredSF"])	

	histDY.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_mass20To60_ZPredSF"])
	histDY.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_mass60To86_ZPredSF"])
	histDY.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_mass96To150_ZPredSF"])
	histDY.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_mass150To200_ZPredSF"])
	histDY.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_mass200To300_ZPredSF"])
	histDY.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_mass300To400_ZPredSF"])
	histDY.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_mass400_ZPredSF"])	
	
	histDY.SetBinContent(8,resultsNLL["highNLL"]["highMT2_mass20To60_ZPredSF"])
	histDY.SetBinContent(9,resultsNLL["highNLL"]["highMT2_mass60To86_ZPredSF"])
	histDY.SetBinContent(10,resultsNLL["highNLL"]["highMT2_mass96To150_ZPredSF"])
	histDY.SetBinContent(11,resultsNLL["highNLL"]["highMT2_mass150To200_ZPredSF"])
	histDY.SetBinContent(12,resultsNLL["highNLL"]["highMT2_mass200To300_ZPredSF"])
	histDY.SetBinContent(13,resultsNLL["highNLL"]["highMT2_mass300To400_ZPredSF"])
	histDY.SetBinContent(14,resultsNLL["highNLL"]["highMT2_mass400_ZPredSF"])	

	histRare.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_mass20To60_RarePredSF"])
	histRare.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_mass60To86_RarePredSF"])
	histRare.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_mass96To150_RarePredSF"])
	histRare.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_mass150To200_RarePredSF"])
	histRare.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_mass200To300_RarePredSF"])
	histRare.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_mass300To400_RarePredSF"])
	histRare.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_mass400_RarePredSF"])	
	
	histRare.SetBinContent(8,resultsNLL["highNLL"]["highMT2_mass20To60_RarePredSF"])
	histRare.SetBinContent(9,resultsNLL["highNLL"]["highMT2_mass60To86_RarePredSF"])
	histRare.SetBinContent(10,resultsNLL["highNLL"]["highMT2_mass96To150_RarePredSF"])
	histRare.SetBinContent(11,resultsNLL["highNLL"]["highMT2_mass150To200_RarePredSF"])
	histRare.SetBinContent(12,resultsNLL["highNLL"]["highMT2_mass200To300_RarePredSF"])
	histRare.SetBinContent(13,resultsNLL["highNLL"]["highMT2_mass300To400_RarePredSF"])
	histRare.SetBinContent(14,resultsNLL["highNLL"]["highMT2_mass400_RarePredSF"])	

	errGraph = ROOT.TGraphAsymmErrors()
	graphObs = ROOT.TGraphAsymmErrors()
	
	for i in range(1,histFlavSym.GetNbinsX()+1):
		graphObs.SetPoint(i,histObs.GetBinCenter(i),histObs.GetBinContent(i))
		errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
		
		

	graphObs.SetPointError(1,0,0,resultsNLL["lowNLL"]["highMT2_mass20To60_SFDown"],resultsNLL["lowNLL"]["highMT2_mass20To60_SFUp"])
	graphObs.SetPointError(2,0,0,resultsNLL["lowNLL"]["highMT2_mass60To86_SFDown"],resultsNLL["lowNLL"]["highMT2_mass60To86_SFUp"])
	graphObs.SetPointError(3,0,0,resultsNLL["lowNLL"]["highMT2_mass96To150_SFDown"],resultsNLL["lowNLL"]["highMT2_mass96To150_SFUp"])
	graphObs.SetPointError(4,0,0,resultsNLL["lowNLL"]["highMT2_mass150To200_SFDown"],resultsNLL["lowNLL"]["highMT2_mass150To200_SFUp"])
	graphObs.SetPointError(5,0,0,resultsNLL["lowNLL"]["highMT2_mass200To300_SFDown"],resultsNLL["lowNLL"]["highMT2_mass200To300_SFUp"])
	graphObs.SetPointError(6,0,0,resultsNLL["lowNLL"]["highMT2_mass300To400_SFDown"],resultsNLL["lowNLL"]["highMT2_mass300To400_SFUp"])
	graphObs.SetPointError(7,0,0,resultsNLL["lowNLL"]["highMT2_mass400_SFDown"],resultsNLL["lowNLL"]["highMT2_mass400_SFUp"])

	graphObs.SetPointError(8,0,0,resultsNLL["highNLL"]["highMT2_mass20To60_SFDown"],resultsNLL["highNLL"]["highMT2_mass20To60_SFUp"])
	graphObs.SetPointError(9,0,0,resultsNLL["highNLL"]["highMT2_mass60To86_SFDown"],resultsNLL["highNLL"]["highMT2_mass60To86_SFUp"])
	graphObs.SetPointError(10,0,0,resultsNLL["highNLL"]["highMT2_mass96To150_SFDown"],resultsNLL["highNLL"]["highMT2_mass96To150_SFUp"])
	graphObs.SetPointError(11,0,0,resultsNLL["highNLL"]["highMT2_mass150To200_SFDown"],resultsNLL["highNLL"]["highMT2_mass150To200_SFUp"])
	graphObs.SetPointError(12,0,0,resultsNLL["highNLL"]["highMT2_mass200To300_SFDown"],resultsNLL["highNLL"]["highMT2_mass200To300_SFUp"])
	graphObs.SetPointError(13,0,0,resultsNLL["highNLL"]["highMT2_mass300To400_SFDown"],resultsNLL["highNLL"]["highMT2_mass300To400_SFUp"])
	graphObs.SetPointError(14,0,0,resultsNLL["highNLL"]["highMT2_mass400_SFDown"],resultsNLL["highNLL"]["highMT2_mass400_SFUp"])


	errGraph.SetPointError(1,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass20To60_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass20To60_TotalPredErrUpSF"])
	errGraph.SetPointError(2,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass60To86_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass60To86_TotalPredErrUpSF"])
	errGraph.SetPointError(3,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass96To150_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass96To150_TotalPredErrUpSF"])
	errGraph.SetPointError(4,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass150To200_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass150To200_TotalPredErrUpSF"])
	errGraph.SetPointError(5,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass200To300_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass200To300_TotalPredErrUpSF"])
	errGraph.SetPointError(6,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass300To400_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass300To400_TotalPredErrUpSF"])
	errGraph.SetPointError(7,0.5,0.5,resultsNLL["lowNLL"]["highMT2_mass400_TotalPredErrDownSF"],resultsNLL["lowNLL"]["highMT2_mass400_TotalPredErrUpSF"])
	
	errGraph.SetPointError(8,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass20To60_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass20To60_TotalPredErrUpSF"])
	errGraph.SetPointError(9,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass60To86_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass60To86_TotalPredErrUpSF"])
	errGraph.SetPointError(10,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass96To150_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass96To150_TotalPredErrUpSF"])
	errGraph.SetPointError(11,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass150To200_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass150To200_TotalPredErrUpSF"])
	errGraph.SetPointError(12,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass200To300_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass200To300_TotalPredErrUpSF"])
	errGraph.SetPointError(13,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass300To400_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass300To400_TotalPredErrUpSF"])
	errGraph.SetPointError(14,0.5,0.5,resultsNLL["highNLL"]["highMT2_mass400_TotalPredErrDownSF"],resultsNLL["highNLL"]["highMT2_mass400_TotalPredErrUpSF"])

	errGraph.SetFillColor(myColors["MyBlueOverview"])
	errGraph.SetFillStyle(3354)	

	histFlavSym.SetLineColor(ROOT.kBlue+3)
	histFlavSym.SetLineWidth(2)
	
	histDY.SetLineColor(ROOT.kGreen+3)
	histDY.SetFillColor(ROOT.kGreen+3)
	#~ histDY.SetFillStyle(3002)
	
	histRare.SetLineColor(ROOT.kViolet+2)
	histRare.SetFillColor(ROOT.kViolet+2)
	
	from ROOT import THStack
	
	stack = THStack()
	stack.Add(histDY)	
	stack.Add(histRare)	
	stack.Add(histFlavSym)	
	
	histObs.GetYaxis().SetRangeUser(0.5,90000)
	histObs.GetYaxis().SetTitle("Events")
	histObs.LabelsOption("v")

	histObs.UseCurrentStyle()
	histObs.Draw("pe")

	
	
	#~ hCanvas.DrawFrame(-0.5,0,30.5,65,"; %s ; %s" %("","Events"))
	
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

	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%"35.9")
	
	#~ cmsExtra = "Preliminary"
	cmsExtra = ""
	latexCMS.DrawLatex(0.17,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.17,yLabelPos,"%s"%(cmsExtra))

	leg = ROOT.TLegend(0.37, 0.7, 0.89, 0.95,"","brNDC")
	leg.SetNColumns(3)
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)
	
	bkgHistForLegend = histFlavSym.Clone("bkgHistForLegend")
	bkgHistForLegend.SetLineColor(ROOT.kBlue+3)
	bkgHistForLegend.SetFillColor(ROOT.kWhite)
	bkgHistForLegend.SetLineWidth(2)
	
	leg.AddEntry(histObs,"Data","pe")
	#~ leg.AddEntry(histFlavSym, "Total backgrounds","l")
	leg.AddEntry(bkgHistForLegend, "FS","f")
	leg.AddEntry(errGraph,"Tot. unc.", "f")	
	leg.AddEntry(histDY,"Template", "f")
	leg.AddEntry(histRare,"Rares", "f")
	

	errGraph.Draw("same02")
	stack.Draw("samehist")	
	
	graphObs.Draw("pesame")
	
	leg.Draw("same")

	
	
	line1 = ROOT.TLine(7,0,7,500)
	line1.SetLineColor(ROOT.kBlack)
	line1.SetLineWidth(2)
	line1.Draw("same")


	label = ROOT.TLatex()
	label.SetTextAlign(12)
	label.SetTextSize(0.04)
	label.SetTextColor(ROOT.kBlack)	
	label.SetTextAlign(22)	
	#~ label.SetTextAngle(-45)	
	
	label.DrawLatex(3.5,400,"t#bar{t} like")
	label.DrawLatex(10.5,400,"non t#bar{t} like")

	plotPad.RedrawAxis()
	
	hCanvas.Print("edgeOverviewNoLegacy.pdf")
	#~ hCanvas.Print("edgeOverview.root")
		
def makeOverviewPlotOnZ(useEWRegions=True):

	from helpers import createMyColors
	from defs import myColors
	colors = createMyColors()		
	
	if useEWRegions:
		histObs = ROOT.TH1F("histObs","histObs",23,0,23)
		histPred = ROOT.TH1F("histPred","histPred",23,0,23)
		histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",23,0,23)
		histDY = ROOT.TH1F("histDY","histDY",23,0,23)
		histRare = ROOT.TH1F("histRare","histRare",23,0,23)
		hCanvas = TCanvas("hCanvas", "Distribution", 1200,800)
	else:
		histObs = ROOT.TH1F("histObs","histObs",16,0,16)
		histPred = ROOT.TH1F("histPred","histPred",16,0,16)
		histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",16,0,16)
		histDY = ROOT.TH1F("histDY","histDY",16,0,16)
		histRare = ROOT.TH1F("histRare","histRare",16,0,16)
		hCanvas = TCanvas("hCanvas", "Distribution", 1050,800)
	
	histObs.SetMarkerColor(ROOT.kBlack)
	histObs.SetLineColor(ROOT.kBlack)
	histObs.SetMarkerStyle(20)

	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style=setTDRStyle()
	style.SetPadBottomMargin(0.28)
	style.SetPadLeftMargin(0.13)
	style.SetTitleYOffset(0.9)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()
	plotPad.SetLogy()	
	
	### SRA b-veto
	histObs.SetBinContent(1,23)
	histObs.SetBinContent(2,5)
	histObs.SetBinContent(3,4)
	### SRA b-tag
	histObs.SetBinContent(4,14)
	histObs.SetBinContent(5,7)
	histObs.SetBinContent(6,1)
	### SRB b-veto
	histObs.SetBinContent(7,10)		
	histObs.SetBinContent(8,4)
	histObs.SetBinContent(9,0)
	### SRB b-tag
	histObs.SetBinContent(10,10)
	histObs.SetBinContent(11,5)
	histObs.SetBinContent(12,0)
	### SRC b-veto
	histObs.SetBinContent(13,4)
	histObs.SetBinContent(14,0)	
	### SRC b-tag
	histObs.SetBinContent(15,2)
	histObs.SetBinContent(16,2)
	
	if useEWRegions:
		### EWK WZ/ZZ
		histObs.SetBinContent(17,57)
		histObs.SetBinContent(18,29)		
		histObs.SetBinContent(19,2)		
		histObs.SetBinContent(20,0)		
		### EWK HT
		histObs.SetBinContent(21,9)
		histObs.SetBinContent(22,5)		
		histObs.SetBinContent(23,1)	

	
	if useEWRegions:
		names = ["p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: 150-250 GeV","p_{T}^{miss}: > 250 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: 150-250 GeV","p_{T}^{miss}: > 250 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: 150-250 GeV","p_{T}^{miss}: > 250 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: 150-250 GeV","p_{T}^{miss}: > 250 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: > 150 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: > 150 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: 150-250 GeV","p_{T}^{miss}: 250-350 GeV","p_{T}^{miss}: > 350 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: 150-250 GeV","p_{T}^{miss}: > 250 GeV"]
	else:
		names = ["p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: 150-250 GeV","p_{T}^{miss}: > 250 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: 150-250 GeV","p_{T}^{miss}: > 250 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: 150-250 GeV","p_{T}^{miss}: > 250 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: 150-250 GeV","p_{T}^{miss}: > 250 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: > 150 GeV","p_{T}^{miss}: 100-150 GeV","p_{T}^{miss}: > 150 GeV"]
	
	for index, name in enumerate(names):
	
		histObs.GetXaxis().SetBinLabel(index+1,name)
	
	### SRA b-veto
	histFlavSym.SetBinContent(1,0.4)
	histFlavSym.SetBinContent(2,0.2)
	histFlavSym.SetBinContent(3,0.2)
	### SRA b-tag
	histFlavSym.SetBinContent(4,2.3)
	histFlavSym.SetBinContent(5,1.7)
	histFlavSym.SetBinContent(6,0.1)
	### SRB b-veto
	histFlavSym.SetBinContent(7,0.4)		
	histFlavSym.SetBinContent(8,0.4)
	histFlavSym.SetBinContent(9,0.1)
	### SRB b-tag
	histFlavSym.SetBinContent(10,1.4)
	histFlavSym.SetBinContent(11,1.1)
	histFlavSym.SetBinContent(12,0.2)
	### SRC b-veto
	histFlavSym.SetBinContent(13,0.4)
	histFlavSym.SetBinContent(14,0.1)	
	### SRC b-tag
	histFlavSym.SetBinContent(15,0.0)
	histFlavSym.SetBinContent(16,0.3)
	
	if useEWRegions:
		### EWK WZ/ZZ
		histFlavSym.SetBinContent(17,11.1)
		histFlavSym.SetBinContent(18,3.2)		
		histFlavSym.SetBinContent(19,0.1)		
		histFlavSym.SetBinContent(20,0.1)		
		### EWK HT
		histFlavSym.SetBinContent(21,4.0)
		histFlavSym.SetBinContent(22,4.7)		
		histFlavSym.SetBinContent(23,0.9)	

	### SRA b-veto
	histDY.SetBinContent(1,13.6)
	histDY.SetBinContent(2,2.5)
	histDY.SetBinContent(3,3.3)
	### SRA b-tag
	histDY.SetBinContent(4,8.2)
	histDY.SetBinContent(5,1.2)
	histDY.SetBinContent(6,0.5)
	### SRB b-veto
	histDY.SetBinContent(7,12.8)		
	histDY.SetBinContent(8,0.9)
	histDY.SetBinContent(9,0.4)
	### SRB b-tag
	histDY.SetBinContent(10,7.7)
	histDY.SetBinContent(11,4.0)
	histDY.SetBinContent(12,0.1)
	### SRC b-veto
	histDY.SetBinContent(13,1.2)
	histDY.SetBinContent(14,0.1)	
	### SRC b-tag
	histDY.SetBinContent(15,0.1)
	histDY.SetBinContent(16,0.0)
	
	if useEWRegions:
		### EWK WZ/ZZ
		histDY.SetBinContent(17,29.3)
		histDY.SetBinContent(18,2.9)		
		histDY.SetBinContent(19,1.0)		
		histDY.SetBinContent(20,0.3)		
		### EWK HT
		histDY.SetBinContent(21,2.9)
		histDY.SetBinContent(22,0.3)		
		histDY.SetBinContent(23,0.1)

	### SRA b-veto
	histRare.SetBinContent(1,0.8)
	histRare.SetBinContent(2,1.4)
	histRare.SetBinContent(3,2.4)
	### SRA b-tag
	histRare.SetBinContent(4,1.9)
	histRare.SetBinContent(5,2.0)
	histRare.SetBinContent(6,1.8)
	### SRB b-veto
	histRare.SetBinContent(7,0.3)		
	histRare.SetBinContent(8,0.7)
	histRare.SetBinContent(9,1.2)
	### SRB b-tag
	histRare.SetBinContent(10,2.0)
	histRare.SetBinContent(11,2.3)
	histRare.SetBinContent(12,1.0)
	### SRC b-veto
	histRare.SetBinContent(13,0.1)
	histRare.SetBinContent(14,0.5)	
	### SRC b-tag
	histRare.SetBinContent(15,0.6)
	histRare.SetBinContent(16,0.6)
	
	if useEWRegions:
		### EWK WZ/ZZ
		histRare.SetBinContent(17,14.5)
		histRare.SetBinContent(18,15.5)		
		histRare.SetBinContent(19,5.0)		
		histRare.SetBinContent(20,2.2)		
		### EWK HT
		histRare.SetBinContent(21,0.7)
		histRare.SetBinContent(22,0.6)		
		histRare.SetBinContent(23,0.3)


	errGraph = ROOT.TGraphAsymmErrors()
	graphObs = ROOT.TGraphAsymmErrors()
	
	for i in range(1,histFlavSym.GetNbinsX()+1):
		graphObs.SetPoint(i,histObs.GetBinCenter(i),histObs.GetBinContent(i))
		errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
		
		yield_up = ROOT.Double(1.)
		yield_down = ROOT.Double(1.)
		ROOT.RooHistError.instance().getPoissonInterval(int(histObs.GetBinContent(i)),yield_down,yield_up,1.)
		graphObs.SetPointError(i,0,0,int(histObs.GetBinContent(i))-yield_down,yield_up-int(histObs.GetBinContent(i)))
		

	### SRA b-veto
	errGraph.SetPointError(1,0.5,0.5,3.2,3.2)
	errGraph.SetPointError(2,0.5,0.5,1.0,1.0)
	errGraph.SetPointError(3,0.5,0.5,2.5,2.5)
	### SRA b-tag
	errGraph.SetPointError(4,0.5,0.5,2.3,2.3)
	errGraph.SetPointError(5,0.5,0.5,1.0,1.0)
	errGraph.SetPointError(6,0.5,0.5,0.7,0.7)
	### SRB b-veto
	errGraph.SetPointError(7,0.5,0.5,2.4,2.4)
	errGraph.SetPointError(8,0.5,0.5,0.5,0.5)
	errGraph.SetPointError(9,0.5,0.5,0.4,0.4)
	### SRB b-tag
	errGraph.SetPointError(10,0.5,0.5,3.3,3.3)
	errGraph.SetPointError(11,0.5,0.5,3.4,3.5)
	errGraph.SetPointError(12,0.5,0.5,0.3,0.4)
	### SRC b-veto
	errGraph.SetPointError(13,0.5,0.5,0.5,0.5)
	errGraph.SetPointError(14,0.5,0.5,0.2,0.3)
	### SRC b-tag
	errGraph.SetPointError(15,0.5,0.5,0.5,0.5)
	errGraph.SetPointError(16,0.5,0.5,0.4,0.5)

	if useEWRegions:
		### EWK WZ/ZZ
		errGraph.SetPointError(17,0.5,0.5,7.0,7.0)
		errGraph.SetPointError(18,0.5,0.5,5.6,5.6)
		errGraph.SetPointError(19,0.5,0.5,1.9,1.9)
		errGraph.SetPointError(20,0.5,0.5,0.9,0.9)
		### EWK HT
		errGraph.SetPointError(21,0.5,0.5,2.8,2.8)
		errGraph.SetPointError(18,0.5,0.5,1.6,1.6)
		errGraph.SetPointError(19,0.5,0.5,0.4,0.4)

	errGraph.SetFillColor(ROOT.kGray+3)
	errGraph.SetFillStyle(3244)	

	histFlavSym.SetFillColor(17)	
	histDY.SetFillColor(ROOT.kRed)
	histRare.SetFillColor(38)
	
	from ROOT import THStack
	
	stack = THStack()
	stack.Add(histFlavSym)
	stack.Add(histRare)	
	stack.Add(histDY)		
	
	histObs.GetYaxis().SetRangeUser(0.2,10000)
	histObs.GetYaxis().SetTitle("Events")
	histObs.LabelsOption("v")

	histObs.UseCurrentStyle()
	histObs.Draw("pe")

	
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
	latexArxive = ROOT.TLatex()
	latexArxive.SetTextFont(42)
	latexArxive.SetTextSize(0.04)
	latexArxive.SetNDC(True)	
	


	intlumi = ROOT.TLatex()
	intlumi.SetTextAlign(12)
	intlumi.SetTextSize(0.03)
	intlumi.SetNDC(True)		

	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%"35.9")
	
	#~ cmsExtra = "Preliminary"
	#~ cmsExtra = ""
	cmsExtra = "Supplementary"
	latexCMS.DrawLatex(0.16,0.88,"CMS")
	
	if useEWRegions:
		latexCMSExtra.DrawLatex(0.24,0.88,"%s"%(cmsExtra))
	else:
		latexCMSExtra.DrawLatex(0.255,0.88,"%s"%(cmsExtra))
	latexArxive.DrawLatex(0.16,0.83,"arxiv:1709.08908")

	leg = ROOT.TLegend(0.55, 0.725, 0.92, 0.95,"","brNDC")
	leg.SetNColumns(2)
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)
	
	
	leg.AddEntry(histObs,"Data","pe")
	leg.AddEntry(histDY,"DY+jets", "f")
	leg.AddEntry(histRare,"Rares", "f")
	leg.AddEntry(histFlavSym, "FS","f")
	

	stack.Draw("samehist")
	errGraph.Draw("same02")
		
	graphObs.Draw("pesame")
	
	leg.Draw("same")
	
	if useEWRegions:
		line1 = ROOT.TLine(3,0,3,70)
		line1.SetLineColor(ROOT.kBlack)
		line1.SetLineWidth(2)
		line1.SetLineStyle(2)
		line1.Draw("same")
		
		line2 = ROOT.TLine(6,0,6,150)
		line2.SetLineColor(ROOT.kBlack)
		line2.SetLineWidth(2)
		line2.Draw("same")
		
		line3 = ROOT.TLine(9,0,9,70)
		line3.SetLineColor(ROOT.kBlack)
		line3.SetLineWidth(2)
		line3.SetLineStyle(2)
		line3.Draw("same")
		
		line4 = ROOT.TLine(12,0,12,150)
		line4.SetLineColor(ROOT.kBlack)
		line4.SetLineWidth(2)
		line4.Draw("same")
		
		line5 = ROOT.TLine(14,0,14,70)
		line5.SetLineColor(ROOT.kBlack)
		line5.SetLineWidth(2)
		line5.SetLineStyle(2)
		line5.Draw("same")
		
		line6 = ROOT.TLine(16,0,16,150)
		line6.SetLineColor(ROOT.kBlack)
		line6.SetLineWidth(3)
		line6.Draw("same")
		
		line7 = ROOT.TLine(20,0,20,150)
		line7.SetLineColor(ROOT.kBlack)
		line7.SetLineWidth(2)
		line7.Draw("same")
		
	else:
		line1 = ROOT.TLine(3,0,3,50)
		line1.SetLineColor(ROOT.kBlack)
		line1.SetLineWidth(2)
		line1.SetLineStyle(2)
		line1.Draw("same")
		
		line2 = ROOT.TLine(6,0,6,120)
		line2.SetLineColor(ROOT.kBlack)
		line2.SetLineWidth(2)
		line2.Draw("same")
		
		line3 = ROOT.TLine(9,0,9,50)
		line3.SetLineColor(ROOT.kBlack)
		line3.SetLineWidth(2)
		line3.SetLineStyle(2)
		line3.Draw("same")
		
		line4 = ROOT.TLine(12,0,12,120)
		line4.SetLineColor(ROOT.kBlack)
		line4.SetLineWidth(2)
		line4.Draw("same")
		
		line5 = ROOT.TLine(14,0,14,50)
		line5.SetLineColor(ROOT.kBlack)
		line5.SetLineWidth(2)
		line5.SetLineStyle(2)
		line5.Draw("same")


	label = ROOT.TLatex()
	label.SetTextSize(0.04)
	label.SetTextColor(ROOT.kBlack)	
	label.SetTextAlign(23)	
	label2 = ROOT.TLatex()
	label2.SetTextSize(0.035)
	label2.SetTextColor(ROOT.kBlack)	
	label2.SetTextAlign(23)	
	
	if useEWRegions:
		label.DrawLatex(3,150,"SRA")
		label.DrawLatex(9,150,"SRB")
		label.DrawLatex(14,150,"SRC")
		label.DrawLatex(18,150,"EW VZ")
		label.DrawLatex(21.5,150,"EW HZ")
		
		label2.DrawLatex(1.5,70,"b veto")
		label2.DrawLatex(4.5,70,"b tag")
		label2.DrawLatex(7.5,70,"b veto")
		label2.DrawLatex(10.5,70,"b tag")
		label2.DrawLatex(13,70,"b veto")
		label2.DrawLatex(15,70,"b tag")
		
	else:
		label.DrawLatex(3,120,"SRA")
		label.DrawLatex(9,120,"SRB")
		label.DrawLatex(14,120,"SRC")
		label2.DrawLatex(1.5,50,"b veto")
		label2.DrawLatex(4.5,50,"b tag")
		label2.DrawLatex(7.5,50,"b veto")
		label2.DrawLatex(10.5,50,"b tag")
		label2.DrawLatex(13,50,"b veto")
		label2.DrawLatex(15,50,"b tag")

	plotPad.RedrawAxis()
	
	if useEWRegions:
		hCanvas.Print("onZOverviewAll.png")
		hCanvas.Print("onZOverviewAll.pdf")
	else:
		hCanvas.Print("onZOverviewStrongSRs.png")
		hCanvas.Print("onZOverviewStrongSRs.pdf")
		

	
def main():
	
	OnZPickle = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelvesMT2/OnZBG_36fb.pkl")
	OnZPickleICHEP = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelves/OnZBG_ICHEP_36fb.pkl")
	OnZPickleLegacy = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelves/OnZBG_legacy_36fb.pkl")
	RaresPickle = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelvesMT2/RareOnZ_Powheg.pkl")
	
	
	name = "cutAndCount"
	countingShelves= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , runRanges.name),"legacy": readPickle("cutAndCount",regionsToUse.signal.legacy.name,runRanges.name),"onZ":OnZPickle,"onZICHEP":OnZPickleICHEP,"onZLegacy":OnZPickleLegacy,"Rares":RaresPickle}	
	#~ countingShelves = {"inclusive":readPickle(name,regionsToUse.signal.inclusive.name , runRanges.name),"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	
	
	makeOverviewPlotOnZ(useEWRegions=True)
	makeOverviewPlotOnZ(useEWRegions=False)

	#~ makeOverviewPlot(countingShelves)	
	makeOverviewPlotNoLegacy(countingShelves)	
	makeOverviewMllPlot(countingShelves,"highNLL",normalizeToBinWidth=True)	
	makeOverviewMllPlot(countingShelves,"lowNLL",normalizeToBinWidth=True)	
	#~ makeOverviewMllPlot(countingShelves,"highNLL",normalizeToBinWidth=False)	
	#~ makeOverviewMllPlot(countingShelves,"lowNLL",normalizeToBinWidth=False)	
	#~ makeOverviewMllPlotBkgOnly(countingShelves,"highNLL",normalizeToBinWidth=True)	
	#~ makeOverviewMllPlotBkgOnly(countingShelves,"lowNLL",normalizeToBinWidth=True)
main()

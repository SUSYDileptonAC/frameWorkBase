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
	
def makeOverviewPlotOld(countingShelves,region):

	from helpers import createMyColors
	from defs import myColors
	colors = createMyColors()	

	
	resultsCentral = getResults(countingShelves,"central","default")
	resultsForward = getResults(countingShelves,"forward","default")
	resultsCentralGeOneBTags = getResults(countingShelves,"central","noBTags")
	resultsForwardGeOneBTags = getResults(countingShelves,"forward","noBTags")
	resultsCentralGeTwoBTags = getResults(countingShelves,"central","geOneBTags")
	resultsForwardGeTwoBTags = getResults(countingShelves,"forward","geOneBTags")
	
	
	histObs = ROOT.TH1F("histObs","histObs",30,0,30)
	
	histObs.SetMarkerColor(ROOT.kBlack)
	histObs.SetLineColor(ROOT.kBlack)
	histObs.SetMarkerStyle(20)
	
	histPred = ROOT.TH1F("histPred","histPred",30,0,30)
	histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",30,0,30)
	histDY = ROOT.TH1F("histDY","histDY",30,0,30)
	
	hCanvas = TCanvas("hCanvas", "Distribution", 1000,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style=setTDRStyle()
	style.SetPadBottomMargin(0.2)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()	
	
	histObs.SetBinContent(1,resultsCentral["lowMassSF"])
	histObs.SetBinContent(2,resultsCentralGeOneBTags["lowMassSF"])
	histObs.SetBinContent(3,resultsCentralGeTwoBTags["lowMassSF"])
	histObs.SetBinContent(4,resultsForward["lowMassSF"])
	histObs.SetBinContent(5,resultsForwardGeOneBTags["lowMassSF"])
	histObs.SetBinContent(6,resultsForwardGeTwoBTags["lowMassSF"])

	histObs.SetBinContent(7,resultsCentral["onZSF"])
	histObs.SetBinContent(8,resultsCentralGeOneBTags["onZSF"])
	histObs.SetBinContent(9,resultsCentralGeTwoBTags["onZSF"])
	histObs.SetBinContent(10,resultsForward["onZSF"])
	histObs.SetBinContent(11,resultsForwardGeOneBTags["onZSF"])
	histObs.SetBinContent(12,resultsForwardGeTwoBTags["onZSF"])

	histObs.SetBinContent(13,resultsCentral["highMassSF"])
	histObs.SetBinContent(14,resultsCentralGeOneBTags["highMassSF"])
	histObs.SetBinContent(15,resultsCentralGeTwoBTags["highMassSF"])
	histObs.SetBinContent(16,resultsForward["highMassSF"])
	histObs.SetBinContent(17,resultsForwardGeOneBTags["highMassSF"])	
	histObs.SetBinContent(18,resultsForwardGeTwoBTags["highMassSF"])

	
	histObs.SetBinContent(19,resultsCentral["belowZSF"])
	histObs.SetBinContent(20,resultsCentralGeOneBTags["belowZSF"])
	histObs.SetBinContent(21,resultsCentralGeTwoBTags["belowZSF"])
	histObs.SetBinContent(22,resultsForward["belowZSF"])
	histObs.SetBinContent(23,resultsForwardGeOneBTags["belowZSF"])
	histObs.SetBinContent(24,resultsForwardGeTwoBTags["belowZSF"])
	
	histObs.SetBinContent(25,resultsCentral["aboveZSF"])
	histObs.SetBinContent(26,resultsCentralGeOneBTags["aboveZSF"])
	histObs.SetBinContent(27,resultsCentralGeTwoBTags["aboveZSF"])		
	histObs.SetBinContent(28,resultsForward["aboveZSF"])
	histObs.SetBinContent(29,resultsForwardGeOneBTags["aboveZSF"])
	histObs.SetBinContent(30,resultsForwardGeTwoBTags["aboveZSF"])
	
	names = ["inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)"]
	
	for index, name in enumerate(names):
	
		histObs.GetXaxis().SetBinLabel(index+1,name)
	

	histFlavSym.SetBinContent(1,resultsCentral["lowMassPredSF"])
	histFlavSym.SetBinContent(2,resultsCentralGeOneBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(3,resultsCentralGeTwoBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(4,resultsForward["lowMassPredSF"])
	histFlavSym.SetBinContent(5,resultsForwardGeOneBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(6,resultsForwardGeTwoBTags["lowMassPredSF"])

	histFlavSym.SetBinContent(7,resultsCentral["onZPredSF"])
	histFlavSym.SetBinContent(8,resultsCentralGeOneBTags["onZPredSF"])
	histFlavSym.SetBinContent(9,resultsCentralGeTwoBTags["onZPredSF"])
	histFlavSym.SetBinContent(10,resultsForward["onZPredSF"])
	histFlavSym.SetBinContent(11,resultsForwardGeOneBTags["onZPredSF"])
	histFlavSym.SetBinContent(12,resultsForwardGeTwoBTags["onZPredSF"])

	histFlavSym.SetBinContent(13,resultsCentral["highMassPredSF"])
	histFlavSym.SetBinContent(14,resultsCentralGeOneBTags["highMassPredSF"])
	histFlavSym.SetBinContent(15,resultsCentralGeTwoBTags["highMassPredSF"])
	histFlavSym.SetBinContent(16,resultsForward["highMassPredSF"])
	histFlavSym.SetBinContent(17,resultsForwardGeOneBTags["highMassPredSF"])	
	histFlavSym.SetBinContent(18,resultsForwardGeTwoBTags["highMassPredSF"])

	
	histFlavSym.SetBinContent(19,resultsCentral["belowZPredSF"])
	histFlavSym.SetBinContent(20,resultsCentralGeOneBTags["belowZPredSF"])
	histFlavSym.SetBinContent(21,resultsCentralGeTwoBTags["belowZPredSF"])
	histFlavSym.SetBinContent(22,resultsForward["belowZPredSF"])
	histFlavSym.SetBinContent(23,resultsForwardGeOneBTags["belowZPredSF"])
	histFlavSym.SetBinContent(24,resultsForwardGeTwoBTags["belowZPredSF"])
	
	histFlavSym.SetBinContent(25,resultsCentral["aboveZPredSF"])
	histFlavSym.SetBinContent(26,resultsCentralGeOneBTags["aboveZPredSF"])
	histFlavSym.SetBinContent(27,resultsCentralGeTwoBTags["aboveZPredSF"])		
	histFlavSym.SetBinContent(28,resultsForward["aboveZPredSF"])
	histFlavSym.SetBinContent(29,resultsForwardGeOneBTags["aboveZPredSF"])
	histFlavSym.SetBinContent(30,resultsForwardGeTwoBTags["aboveZPredSF"])


	histDY.SetBinContent(1,resultsCentral["lowMassZPredSF"])
	histDY.SetBinContent(2,resultsCentralGeOneBTags["lowMassZPredSF"])
	histDY.SetBinContent(3,resultsCentralGeTwoBTags["lowMassZPredSF"])
	histDY.SetBinContent(4,resultsForward["lowMassZPredSF"])
	histDY.SetBinContent(5,resultsForwardGeOneBTags["lowMassZPredSF"])
	histDY.SetBinContent(6,resultsForwardGeTwoBTags["lowMassZPredSF"])

	histDY.SetBinContent(7,resultsCentral["onZZPredSF"])
	histDY.SetBinContent(8,resultsCentralGeOneBTags["onZZPredSF"])
	histDY.SetBinContent(9,resultsCentralGeTwoBTags["onZZPredSF"])
	histDY.SetBinContent(10,resultsForward["onZZPredSF"])
	histDY.SetBinContent(11,resultsForwardGeOneBTags["onZZPredSF"])
	histDY.SetBinContent(12,resultsForwardGeTwoBTags["onZZPredSF"])

	histDY.SetBinContent(13,resultsCentral["highMassZPredSF"])
	histDY.SetBinContent(14,resultsCentralGeOneBTags["highMassZPredSF"])
	histDY.SetBinContent(15,resultsCentralGeTwoBTags["highMassZPredSF"])
	histDY.SetBinContent(16,resultsForward["highMassZPredSF"])
	histDY.SetBinContent(17,resultsForwardGeOneBTags["highMassZPredSF"])	
	histDY.SetBinContent(18,resultsForwardGeTwoBTags["highMassZPredSF"])

	
	histDY.SetBinContent(19,resultsCentral["belowZZPredSF"])
	histDY.SetBinContent(20,resultsCentralGeOneBTags["belowZZPredSF"])
	histDY.SetBinContent(21,resultsCentralGeTwoBTags["belowZZPredSF"])
	histDY.SetBinContent(22,resultsForward["belowZZPredSF"])
	histDY.SetBinContent(23,resultsForwardGeOneBTags["belowZZPredSF"])
	histDY.SetBinContent(24,resultsForwardGeTwoBTags["belowZZPredSF"])
	
	histDY.SetBinContent(25,resultsCentral["aboveZZPredSF"])
	histDY.SetBinContent(26,resultsCentralGeOneBTags["aboveZZPredSF"])
	histDY.SetBinContent(27,resultsCentralGeTwoBTags["aboveZZPredSF"])		
	histDY.SetBinContent(28,resultsForward["aboveZZPredSF"])
	histDY.SetBinContent(29,resultsForwardGeOneBTags["aboveZZPredSF"])
	histDY.SetBinContent(30,resultsForwardGeTwoBTags["aboveZZPredSF"])	
	
	
	
	errGraph = ROOT.TGraphAsymmErrors()
	
	for i in range(1,histFlavSym.GetNbinsX()+1):
		errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histDY.GetBinContent(i))


	errGraph.SetPointError(1,0.5,0.5,resultsCentral["lowMassTotalPredErrSF"],resultsCentral["lowMassTotalPredErrSF"])
	errGraph.SetPointError(2,0.5,0.5,resultsCentralGeOneBTags["lowMassTotalPredErrSF"],resultsCentralGeOneBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(3,0.5,0.5,resultsCentralGeTwoBTags["lowMassTotalPredErrSF"],resultsCentralGeTwoBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(4,0.5,0.5,resultsForward["lowMassTotalPredErrSF"],resultsForward["lowMassTotalPredErrSF"])
	errGraph.SetPointError(5,0.5,0.5,resultsForwardGeOneBTags["lowMassTotalPredErrSF"],resultsForwardGeOneBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(6,0.5,0.5,resultsForwardGeTwoBTags["lowMassTotalPredErrSF"],resultsForwardGeTwoBTags["lowMassTotalPredErrSF"])

	errGraph.SetPointError(7,0.5,0.5,resultsCentral["onZTotalPredErrSF"],resultsCentral["onZTotalPredErrSF"])
	errGraph.SetPointError(8,0.5,0.5,resultsCentralGeOneBTags["onZTotalPredErrSF"],resultsCentralGeOneBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(9,0.5,0.5,resultsCentralGeTwoBTags["onZTotalPredErrSF"],resultsCentralGeTwoBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(10,0.5,0.5,resultsForward["onZTotalPredErrSF"],resultsForward["onZTotalPredErrSF"])
	errGraph.SetPointError(11,0.5,0.5,resultsForwardGeOneBTags["onZTotalPredErrSF"],resultsForwardGeOneBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(12,0.5,0.5,resultsForwardGeTwoBTags["onZTotalPredErrSF"],resultsForwardGeTwoBTags["onZTotalPredErrSF"])

	errGraph.SetPointError(13,0.5,0.5,resultsCentral["highMassTotalPredErrSF"],resultsCentral["highMassTotalPredErrSF"])
	errGraph.SetPointError(14,0.5,0.5,resultsCentralGeOneBTags["highMassTotalPredErrSF"],resultsCentralGeOneBTags["highMassTotalPredErrSF"])
	errGraph.SetPointError(15,0.5,0.5,resultsCentralGeTwoBTags["highMassTotalPredErrSF"],resultsCentralGeTwoBTags["highMassTotalPredErrSF"])
	errGraph.SetPointError(16,0.5,0.5,resultsForward["highMassTotalPredErrSF"],resultsForward["highMassTotalPredErrSF"])
	errGraph.SetPointError(17,0.5,0.5,resultsForwardGeOneBTags["highMassTotalPredErrSF"],resultsForwardGeOneBTags["highMassTotalPredErrSF"])	
	errGraph.SetPointError(18,0.5,0.5,resultsForwardGeTwoBTags["highMassTotalPredErrSF"],resultsForwardGeTwoBTags["highMassTotalPredErrSF"])
		
	errGraph.SetPointError(19,0.5,0.5,resultsCentral["belowZTotalPredErrSF"],resultsCentral["belowZTotalPredErrSF"])
	errGraph.SetPointError(20,0.5,0.5,resultsCentralGeOneBTags["belowZTotalPredErrSF"],resultsCentralGeOneBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(21,0.5,0.5,resultsCentralGeTwoBTags["belowZTotalPredErrSF"],resultsCentralGeTwoBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(22,0.5,0.5,resultsForward["belowZTotalPredErrSF"],resultsForward["belowZTotalPredErrSF"])
	errGraph.SetPointError(23,0.5,0.5,resultsForwardGeOneBTags["belowZTotalPredErrSF"],resultsForwardGeOneBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(24,0.5,0.5,resultsForwardGeTwoBTags["belowZTotalPredErrSF"],resultsForwardGeTwoBTags["belowZTotalPredErrSF"])
	
	errGraph.SetPointError(25,0.5,0.5,resultsCentral["aboveZTotalPredErrSF"],resultsCentral["aboveZTotalPredErrSF"])
	errGraph.SetPointError(26,0.5,0.5,resultsForward["aboveZTotalPredErrSF"],resultsForward["aboveZTotalPredErrSF"])
	errGraph.SetPointError(27,0.5,0.5,resultsCentralGeOneBTags["aboveZTotalPredErrSF"],resultsCentralGeOneBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(28,0.5,0.5,resultsForwardGeOneBTags["aboveZTotalPredErrSF"],resultsForwardGeOneBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(29,0.5,0.5,resultsCentralGeTwoBTags["aboveZTotalPredErrSF"],resultsCentralGeTwoBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(30,0.5,0.5,resultsForwardGeTwoBTags["aboveZTotalPredErrSF"],resultsForwardGeTwoBTags["aboveZTotalPredErrSF"])

	errGraph.SetFillColor(myColors["MyBlueOverview"])
	errGraph.SetFillStyle(3004)	

	histFlavSym.SetLineColor(ROOT.kBlue+3)
	histFlavSym.SetLineWidth(2)
	
	histDY.SetLineColor(ROOT.kGreen+3)
	histDY.SetFillColor(ROOT.kGreen+3)
	histDY.SetFillStyle(3002)


	from ROOT import THStack
	
	stack = THStack()
	stack.Add(histDY)	
	stack.Add(histFlavSym)

	
	
	histObs.GetYaxis().SetRangeUser(0,900)
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
	
	intlumi = ROOT.TLatex()
	intlumi.SetTextAlign(12)
	intlumi.SetTextSize(0.03)
	intlumi.SetNDC(True)		

	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%"2.3")
	
	cmsExtra = "Preliminary"
	latexCMS.DrawLatex(0.19,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))

	leg = ROOT.TLegend(0.4, 0.7, 0.925, 0.95,"","brNDC")
	leg.SetNColumns(2)
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)
	
	leg.AddEntry(histObs,"Data","pe")
	leg.AddEntry(histFlavSym, "Total backgrounds","l")
	leg.AddEntry(histDY,"Drell-Yan", "f")
	leg.AddEntry(errGraph,"Total uncert.", "f")	
	

	errGraph.Draw("same02")
	stack.Draw("samehist")	
	
	histObs.Draw("pesame")
	
	leg.Draw("same")

	line1 = ROOT.TLine(6,0,6,350)
	line2 = ROOT.TLine(12,0,12,350)
	line3 = ROOT.TLine(18,0,18,350)
	line4 = ROOT.TLine(24,0,24,350)

	line1.SetLineColor(ROOT.kBlack)
	line2.SetLineColor(ROOT.kBlack)
	line3.SetLineColor(ROOT.kBlack)
	line4.SetLineColor(ROOT.kBlack)

	line1.SetLineWidth(2)
	line2.SetLineWidth(2)
	line3.SetLineWidth(4)
	line4.SetLineWidth(2)

	line1.Draw("same")
	line2.Draw("same")
	line3.Draw("same")
	line4.Draw("same")
	
	line5 = ROOT.TLine(3,0,3,320)
	line6 = ROOT.TLine(9,0,9,320)
	line7 = ROOT.TLine(15,0,15,320)
	line8 = ROOT.TLine(21,0,21,320)
	line9 = ROOT.TLine(27,0,27,320)

	line5.SetLineColor(ROOT.kBlack)
	line6.SetLineColor(ROOT.kBlack)
	line7.SetLineColor(ROOT.kBlack)
	line8.SetLineColor(ROOT.kBlack)
	line9.SetLineColor(ROOT.kBlack)

	line5.SetLineWidth(2)
	line6.SetLineWidth(2)
	line7.SetLineWidth(2)
	line8.SetLineWidth(2)
	line9.SetLineWidth(2)
	line5.SetLineStyle(ROOT.kDashed)
	line6.SetLineStyle(ROOT.kDashed)
	line7.SetLineStyle(ROOT.kDashed)
	line8.SetLineStyle(ROOT.kDashed)
	line9.SetLineStyle(ROOT.kDashed)

	line5.Draw("same")
	line6.Draw("same")
	line7.Draw("same")
	line8.Draw("same")
	line9.Draw("same")


	label = ROOT.TLatex()
	label.SetTextAlign(12)
	label.SetTextSize(0.04)
	label.SetTextColor(ROOT.kBlack)	
	label.SetTextAngle(45)	
	
	label.DrawLatex(1,380,"low-mass")
	label.DrawLatex(8,380,"on-Z")
	label.DrawLatex(13,380,"high-mass")
	label.DrawLatex(19,380,"below-Z")
	label.DrawLatex(25,380,"above-Z")


	plotPad.RedrawAxis()
	
	hCanvas.Print("edgeOverview.pdf")
	hCanvas.Print("edgeOverview.root")
	
def makeOverviewPlotSplitted(countingShelves,region):

	from helpers import createMyColors
	from defs import myColors
	colors = createMyColors()	

	
	resultsCentral = getResults(countingShelves,"central","default")
	resultsForward = getResults(countingShelves,"forward","default")
	resultsCentralGeOneBTags = getResults(countingShelves,"central","noBTags")
	resultsForwardGeOneBTags = getResults(countingShelves,"forward","noBTags")
	resultsCentralGeTwoBTags = getResults(countingShelves,"central","geOneBTags")
	resultsForwardGeTwoBTags = getResults(countingShelves,"forward","geOneBTags")
	
	histTotal = ROOT.TH1F("histTotal","histTotal",30,0,30)
	
	histObs = ROOT.TH1F("histObs","histObs",30,0,30)
	
	histObs.SetMarkerColor(ROOT.kBlack)
	histObs.SetLineColor(ROOT.kBlack)
	histObs.SetMarkerStyle(20)
	
	histPred = ROOT.TH1F("histPred","histPred",30,0,30)
	histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",30,0,30)
	histOnlyDY = ROOT.TH1F("histDY","histDY",30,0,30)
	histOther = ROOT.TH1F("histOther","histOther",30,0,30)
	
	hCanvas = TCanvas("hCanvas", "Distribution", 1000,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style=setTDRStyle()
	style.SetPadBottomMargin(0.2)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()	
	
	histObs.SetBinContent(1,resultsCentral["lowMassSF"])
	histObs.SetBinContent(2,resultsCentralGeOneBTags["lowMassSF"])
	histObs.SetBinContent(3,resultsCentralGeTwoBTags["lowMassSF"])
	histObs.SetBinContent(4,resultsForward["lowMassSF"])
	histObs.SetBinContent(5,resultsForwardGeOneBTags["lowMassSF"])
	histObs.SetBinContent(6,resultsForwardGeTwoBTags["lowMassSF"])
	
	histObs.SetBinContent(7,resultsCentral["belowZSF"])
	histObs.SetBinContent(8,resultsCentralGeOneBTags["belowZSF"])
	histObs.SetBinContent(9,resultsCentralGeTwoBTags["belowZSF"])
	histObs.SetBinContent(10,resultsForward["belowZSF"])
	histObs.SetBinContent(11,resultsForwardGeOneBTags["belowZSF"])
	histObs.SetBinContent(12,resultsForwardGeTwoBTags["belowZSF"])

	histObs.SetBinContent(13,resultsCentral["onZSF"])
	histObs.SetBinContent(14,resultsCentralGeOneBTags["onZSF"])
	histObs.SetBinContent(15,resultsCentralGeTwoBTags["onZSF"])
	histObs.SetBinContent(16,resultsForward["onZSF"])
	histObs.SetBinContent(17,resultsForwardGeOneBTags["onZSF"])
	histObs.SetBinContent(18,resultsForwardGeTwoBTags["onZSF"])
	
	histObs.SetBinContent(19,resultsCentral["aboveZSF"])
	histObs.SetBinContent(20,resultsCentralGeOneBTags["aboveZSF"])
	histObs.SetBinContent(21,resultsCentralGeTwoBTags["aboveZSF"])		
	histObs.SetBinContent(22,resultsForward["aboveZSF"])
	histObs.SetBinContent(23,resultsForwardGeOneBTags["aboveZSF"])
	histObs.SetBinContent(24,resultsForwardGeTwoBTags["aboveZSF"])

	histObs.SetBinContent(25,resultsCentral["highMassSF"])
	histObs.SetBinContent(26,resultsCentralGeOneBTags["highMassSF"])
	histObs.SetBinContent(27,resultsCentralGeTwoBTags["highMassSF"])
	histObs.SetBinContent(28,resultsForward["highMassSF"])
	histObs.SetBinContent(29,resultsForwardGeOneBTags["highMassSF"])	
	histObs.SetBinContent(30,resultsForwardGeTwoBTags["highMassSF"])

	
	names = ["inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)"]
	
	for index, name in enumerate(names):
	
		histObs.GetXaxis().SetBinLabel(index+1,name)
	

	histFlavSym.SetBinContent(1,resultsCentral["lowMassPredSF"])
	histFlavSym.SetBinContent(2,resultsCentralGeOneBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(3,resultsCentralGeTwoBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(4,resultsForward["lowMassPredSF"])
	histFlavSym.SetBinContent(5,resultsForwardGeOneBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(6,resultsForwardGeTwoBTags["lowMassPredSF"])
	
	histFlavSym.SetBinContent(7,resultsCentral["belowZPredSF"])
	histFlavSym.SetBinContent(8,resultsCentralGeOneBTags["belowZPredSF"])
	histFlavSym.SetBinContent(9,resultsCentralGeTwoBTags["belowZPredSF"])
	histFlavSym.SetBinContent(10,resultsForward["belowZPredSF"])
	histFlavSym.SetBinContent(11,resultsForwardGeOneBTags["belowZPredSF"])
	histFlavSym.SetBinContent(12,resultsForwardGeTwoBTags["belowZPredSF"])

	histFlavSym.SetBinContent(13,resultsCentral["onZPredSF"])
	histFlavSym.SetBinContent(14,resultsCentralGeOneBTags["onZPredSF"])
	histFlavSym.SetBinContent(15,resultsCentralGeTwoBTags["onZPredSF"])
	histFlavSym.SetBinContent(16,resultsForward["onZPredSF"])
	histFlavSym.SetBinContent(17,resultsForwardGeOneBTags["onZPredSF"])
	histFlavSym.SetBinContent(18,resultsForwardGeTwoBTags["onZPredSF"])
	
	histFlavSym.SetBinContent(19,resultsCentral["aboveZPredSF"])
	histFlavSym.SetBinContent(20,resultsCentralGeOneBTags["aboveZPredSF"])
	histFlavSym.SetBinContent(21,resultsCentralGeTwoBTags["aboveZPredSF"])		
	histFlavSym.SetBinContent(22,resultsForward["aboveZPredSF"])
	histFlavSym.SetBinContent(23,resultsForwardGeOneBTags["aboveZPredSF"])
	histFlavSym.SetBinContent(24,resultsForwardGeTwoBTags["aboveZPredSF"])

	histFlavSym.SetBinContent(25,resultsCentral["highMassPredSF"])
	histFlavSym.SetBinContent(26,resultsCentralGeOneBTags["highMassPredSF"])
	histFlavSym.SetBinContent(27,resultsCentralGeTwoBTags["highMassPredSF"])
	histFlavSym.SetBinContent(28,resultsForward["highMassPredSF"])
	histFlavSym.SetBinContent(29,resultsForwardGeOneBTags["highMassPredSF"])	
	histFlavSym.SetBinContent(30,resultsForwardGeTwoBTags["highMassPredSF"])


	histOnlyDY.SetBinContent(1,resultsCentral["lowMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(2,resultsCentralGeOneBTags["lowMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(3,resultsCentralGeTwoBTags["lowMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(4,resultsForward["lowMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(5,resultsForwardGeOneBTags["lowMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(6,resultsForwardGeTwoBTags["lowMassOnlyZPredSF"])
	
	histOnlyDY.SetBinContent(7,resultsCentral["belowZOnlyZPredSF"])
	histOnlyDY.SetBinContent(8,resultsCentralGeOneBTags["belowZOnlyZPredSF"])
	histOnlyDY.SetBinContent(9,resultsCentralGeTwoBTags["belowZOnlyZPredSF"])
	histOnlyDY.SetBinContent(10,resultsForward["belowZOnlyZPredSF"])
	histOnlyDY.SetBinContent(11,resultsForwardGeOneBTags["belowZOnlyZPredSF"])
	histOnlyDY.SetBinContent(12,resultsForwardGeTwoBTags["belowZOnlyZPredSF"])

	histOnlyDY.SetBinContent(13,resultsCentral["onZOnlyZPredSF"])
	histOnlyDY.SetBinContent(14,resultsCentralGeOneBTags["onZOnlyZPredSF"])
	histOnlyDY.SetBinContent(15,resultsCentralGeTwoBTags["onZOnlyZPredSF"])
	histOnlyDY.SetBinContent(16,resultsForward["onZOnlyZPredSF"])
	histOnlyDY.SetBinContent(17,resultsForwardGeOneBTags["onZOnlyZPredSF"])
	histOnlyDY.SetBinContent(18,resultsForwardGeTwoBTags["onZOnlyZPredSF"])
	
	histOnlyDY.SetBinContent(19,resultsCentral["aboveZOnlyZPredSF"])
	histOnlyDY.SetBinContent(20,resultsCentralGeOneBTags["aboveZOnlyZPredSF"])
	histOnlyDY.SetBinContent(21,resultsCentralGeTwoBTags["aboveZOnlyZPredSF"])		
	histOnlyDY.SetBinContent(22,resultsForward["aboveZOnlyZPredSF"])
	histOnlyDY.SetBinContent(23,resultsForwardGeOneBTags["aboveZOnlyZPredSF"])
	histOnlyDY.SetBinContent(24,resultsForwardGeTwoBTags["aboveZOnlyZPredSF"])	

	histOnlyDY.SetBinContent(25,resultsCentral["highMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(26,resultsCentralGeOneBTags["highMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(27,resultsCentralGeTwoBTags["highMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(28,resultsForward["highMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(29,resultsForwardGeOneBTags["highMassOnlyZPredSF"])	
	histOnlyDY.SetBinContent(30,resultsForwardGeTwoBTags["highMassOnlyZPredSF"])
	
	

	histOther.SetBinContent(1,resultsCentral["lowMassOtherPredSF"])
	histOther.SetBinContent(2,resultsCentralGeOneBTags["lowMassOtherPredSF"])
	histOther.SetBinContent(3,resultsCentralGeTwoBTags["lowMassOtherPredSF"])
	histOther.SetBinContent(4,resultsForward["lowMassOtherPredSF"])
	histOther.SetBinContent(5,resultsForwardGeOneBTags["lowMassOtherPredSF"])
	histOther.SetBinContent(6,resultsForwardGeTwoBTags["lowMassOtherPredSF"])
	
	histOther.SetBinContent(7,resultsCentral["belowZOtherPredSF"])
	histOther.SetBinContent(8,resultsCentralGeOneBTags["belowZOtherPredSF"])
	histOther.SetBinContent(9,resultsCentralGeTwoBTags["belowZOtherPredSF"])
	histOther.SetBinContent(10,resultsForward["belowZOtherPredSF"])
	histOther.SetBinContent(11,resultsForwardGeOneBTags["belowZOtherPredSF"])
	histOther.SetBinContent(12,resultsForwardGeTwoBTags["belowZOtherPredSF"])

	histOther.SetBinContent(13,resultsCentral["onZOtherPredSF"])
	histOther.SetBinContent(14,resultsCentralGeOneBTags["onZOtherPredSF"])
	histOther.SetBinContent(15,resultsCentralGeTwoBTags["onZOtherPredSF"])
	histOther.SetBinContent(16,resultsForward["onZOtherPredSF"])
	histOther.SetBinContent(17,resultsForwardGeOneBTags["onZOtherPredSF"])
	histOther.SetBinContent(18,resultsForwardGeTwoBTags["onZOtherPredSF"])
	
	histOther.SetBinContent(19,resultsCentral["aboveZOtherPredSF"])
	histOther.SetBinContent(20,resultsCentralGeOneBTags["aboveZOtherPredSF"])
	histOther.SetBinContent(21,resultsCentralGeTwoBTags["aboveZOtherPredSF"])		
	histOther.SetBinContent(22,resultsForward["aboveZOtherPredSF"])
	histOther.SetBinContent(23,resultsForwardGeOneBTags["aboveZOtherPredSF"])
	histOther.SetBinContent(24,resultsForwardGeTwoBTags["aboveZOtherPredSF"])	

	histOther.SetBinContent(25,resultsCentral["highMassOtherPredSF"])
	histOther.SetBinContent(26,resultsCentralGeOneBTags["highMassOtherPredSF"])
	histOther.SetBinContent(27,resultsCentralGeTwoBTags["highMassOtherPredSF"])
	histOther.SetBinContent(28,resultsForward["highMassOtherPredSF"])
	histOther.SetBinContent(29,resultsForwardGeOneBTags["highMassOtherPredSF"])	
	histOther.SetBinContent(30,resultsForwardGeTwoBTags["highMassOtherPredSF"])

	
	
	
	errGraph = ROOT.TGraphAsymmErrors()
	
	for i in range(1,histFlavSym.GetNbinsX()+1):
		errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histOnlyDY.GetBinContent(i)+histOther.GetBinContent(i))
		histTotal.SetBinContent(i,histFlavSym.GetBinContent(i)+histOnlyDY.GetBinContent(i)+histOther.GetBinContent(i))


	errGraph.SetPointError(1,0.5,0.5,resultsCentral["lowMassTotalPredErrSF"],resultsCentral["lowMassTotalPredErrSF"])
	errGraph.SetPointError(2,0.5,0.5,resultsCentralGeOneBTags["lowMassTotalPredErrSF"],resultsCentralGeOneBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(3,0.5,0.5,resultsCentralGeTwoBTags["lowMassTotalPredErrSF"],resultsCentralGeTwoBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(4,0.5,0.5,resultsForward["lowMassTotalPredErrSF"],resultsForward["lowMassTotalPredErrSF"])
	errGraph.SetPointError(5,0.5,0.5,resultsForwardGeOneBTags["lowMassTotalPredErrSF"],resultsForwardGeOneBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(6,0.5,0.5,resultsForwardGeTwoBTags["lowMassTotalPredErrSF"],resultsForwardGeTwoBTags["lowMassTotalPredErrSF"])

	errGraph.SetPointError(7,0.5,0.5,resultsCentral["onZTotalPredErrSF"],resultsCentral["onZTotalPredErrSF"])
	errGraph.SetPointError(8,0.5,0.5,resultsCentralGeOneBTags["onZTotalPredErrSF"],resultsCentralGeOneBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(9,0.5,0.5,resultsCentralGeTwoBTags["onZTotalPredErrSF"],resultsCentralGeTwoBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(10,0.5,0.5,resultsForward["onZTotalPredErrSF"],resultsForward["onZTotalPredErrSF"])
	errGraph.SetPointError(11,0.5,0.5,resultsForwardGeOneBTags["onZTotalPredErrSF"],resultsForwardGeOneBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(12,0.5,0.5,resultsForwardGeTwoBTags["onZTotalPredErrSF"],resultsForwardGeTwoBTags["onZTotalPredErrSF"])

	errGraph.SetPointError(13,0.5,0.5,resultsCentral["highMassTotalPredErrSF"],resultsCentral["highMassTotalPredErrSF"])
	errGraph.SetPointError(14,0.5,0.5,resultsCentralGeOneBTags["highMassTotalPredErrSF"],resultsCentralGeOneBTags["highMassTotalPredErrSF"])
	errGraph.SetPointError(15,0.5,0.5,resultsCentralGeTwoBTags["highMassTotalPredErrSF"],resultsCentralGeTwoBTags["highMassTotalPredErrSF"])
	errGraph.SetPointError(16,0.5,0.5,resultsForward["highMassTotalPredErrSF"],resultsForward["highMassTotalPredErrSF"])
	errGraph.SetPointError(17,0.5,0.5,resultsForwardGeOneBTags["highMassTotalPredErrSF"],resultsForwardGeOneBTags["highMassTotalPredErrSF"])	
	errGraph.SetPointError(18,0.5,0.5,resultsForwardGeTwoBTags["highMassTotalPredErrSF"],resultsForwardGeTwoBTags["highMassTotalPredErrSF"])
		
	errGraph.SetPointError(19,0.5,0.5,resultsCentral["belowZTotalPredErrSF"],resultsCentral["belowZTotalPredErrSF"])
	errGraph.SetPointError(20,0.5,0.5,resultsCentralGeOneBTags["belowZTotalPredErrSF"],resultsCentralGeOneBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(21,0.5,0.5,resultsCentralGeTwoBTags["belowZTotalPredErrSF"],resultsCentralGeTwoBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(22,0.5,0.5,resultsForward["belowZTotalPredErrSF"],resultsForward["belowZTotalPredErrSF"])
	errGraph.SetPointError(23,0.5,0.5,resultsForwardGeOneBTags["belowZTotalPredErrSF"],resultsForwardGeOneBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(24,0.5,0.5,resultsForwardGeTwoBTags["belowZTotalPredErrSF"],resultsForwardGeTwoBTags["belowZTotalPredErrSF"])
	
	errGraph.SetPointError(25,0.5,0.5,resultsCentral["aboveZTotalPredErrSF"],resultsCentral["aboveZTotalPredErrSF"])
	errGraph.SetPointError(26,0.5,0.5,resultsForward["aboveZTotalPredErrSF"],resultsForward["aboveZTotalPredErrSF"])
	errGraph.SetPointError(27,0.5,0.5,resultsCentralGeOneBTags["aboveZTotalPredErrSF"],resultsCentralGeOneBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(28,0.5,0.5,resultsForwardGeOneBTags["aboveZTotalPredErrSF"],resultsForwardGeOneBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(29,0.5,0.5,resultsCentralGeTwoBTags["aboveZTotalPredErrSF"],resultsCentralGeTwoBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(30,0.5,0.5,resultsForwardGeTwoBTags["aboveZTotalPredErrSF"],resultsForwardGeTwoBTags["aboveZTotalPredErrSF"])

	errGraph.SetFillColor(myColors["MyBlueOverview"])
	errGraph.SetFillStyle(3001)

	histFlavSym.SetLineColor(ROOT.kBlue+3)
	histFlavSym.SetFillColor(ROOT.kWhite)
	histFlavSym.SetLineWidth(3)
	
	histOnlyDY.SetLineColor(ROOT.kGreen+2)
	histOnlyDY.SetFillColor(ROOT.kGreen+2)
	#~ histOnlyDY.SetFillStyle(3002)
	
	histOther.SetLineColor(ROOT.kViolet+2)
	histOther.SetFillColor(ROOT.kViolet+2)
	#~ histOther.SetFillStyle(3002)
	
	histTotal.SetLineColor(ROOT.kBlue+3)
	histTotal.SetLineWidth(3)
	
	from ROOT import THStack
	
	stack = THStack()
	stack.Add(histOther)	
	stack.Add(histOnlyDY)	
	#~ stack.Add(histFlavSym)

	
	
	histObs.GetYaxis().SetRangeUser(0,800)
	histObs.GetYaxis().SetTitle("Events")
	histObs.LabelsOption("v")

	histObs.UseCurrentStyle()
	histObs.SetMarkerSize(2)
	histObs.SetLineWidth(2)
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
	latexCMS.SetTextSize(0.075)
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

	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%"2.3")
	
	cmsExtra = "Preliminary"
	latexCMS.DrawLatex(0.19,0.87,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	
	
	
	leg1 = ROOT.TLegend(0.42, 0.84, 0.57, 0.93,"","brNDC")
	leg1.SetNColumns(2)
	leg1.SetFillColor(10)
	leg1.SetLineColor(10)
	leg1.SetShadowColor(0)
	leg1.SetBorderSize(1)
	
	
	leg1.AddEntry(histObs,"  Data  ","pe")
	
	leg2 = ROOT.TLegend(0.65, 0.84, 0.95, 0.93,"","brNDC")
	leg2.SetNColumns(2)
	leg2.SetFillColor(10)
	leg2.SetLineColor(10)
	leg2.SetShadowColor(0)
	leg2.SetBorderSize(1)
	
	leg2.AddEntry(errGraph,"Total uncertainty  ", "f")
	
	
	leg3 = ROOT.TLegend(0.41, 0.74, 0.925, 0.84,"","brNDC")
	leg3.SetNColumns(3)
	leg3.SetFillColor(10)
	leg3.SetLineColor(10)
	leg3.SetShadowColor(0)
	leg3.SetBorderSize(1)
	
	leg3.AddEntry(histFlavSym,"Flavor symmetric", "f")	
	leg3.AddEntry(histOnlyDY,"Z+jets  ", "f")
	leg3.AddEntry(histOther,"Other SM", "f")
	

	#~ errGraph.Draw("same02")
	stack.Draw("samehist")
	errGraph.Draw("same02")
	histTotal.Draw("samehist")	
	
	histObs.Draw("pesame")
	
	leg1.Draw("same")
	leg2.Draw("same")
	leg3.Draw("same")

	
	
	line1 = ROOT.TLine(6,0,6,400)
	line2 = ROOT.TLine(12,0,12,400)
	line3 = ROOT.TLine(18,0,18,400)
	line4 = ROOT.TLine(24,0,24,400)

	line1.SetLineColor(ROOT.kBlack)
	line2.SetLineColor(ROOT.kBlack)
	line3.SetLineColor(ROOT.kBlack)
	line4.SetLineColor(ROOT.kBlack)

	line1.SetLineWidth(2)
	line2.SetLineWidth(2)
	line3.SetLineWidth(2)
	line4.SetLineWidth(2)

	line1.Draw("same")
	line2.Draw("same")
	line3.Draw("same")
	line4.Draw("same")
	
	line5 = ROOT.TLine(3,0,3,350)
	line6 = ROOT.TLine(9,0,9,350)
	line7 = ROOT.TLine(15,0,15,350)
	line8 = ROOT.TLine(21,0,21,350)
	line9 = ROOT.TLine(27,0,27,350)

	line5.SetLineColor(ROOT.kBlack)
	line6.SetLineColor(ROOT.kBlack)
	line7.SetLineColor(ROOT.kBlack)
	line8.SetLineColor(ROOT.kBlack)
	line9.SetLineColor(ROOT.kBlack)

	line5.SetLineWidth(2)
	line6.SetLineWidth(2)
	line7.SetLineWidth(2)
	line8.SetLineWidth(2)
	line9.SetLineWidth(2)
	line5.SetLineStyle(ROOT.kDashed)
	line6.SetLineStyle(ROOT.kDashed)
	line7.SetLineStyle(ROOT.kDashed)
	line8.SetLineStyle(ROOT.kDashed)
	line9.SetLineStyle(ROOT.kDashed)

	line5.Draw("same")
	line6.Draw("same")
	line7.Draw("same")
	line8.Draw("same")
	line9.Draw("same")


	label = ROOT.TLatex()
	label.SetTextAlign(12)
	label.SetTextSize(0.04)
	label.SetTextColor(ROOT.kBlack)	
	label.SetTextAngle(45)	
	
	label.DrawLatex(1.4,430,"low-mass")
	label.DrawLatex(7,430,"below-Z")
	label.DrawLatex(14,430,"on-Z")
	label.DrawLatex(19,430,"above-Z")
	label.DrawLatex(25.4,430,"high-mass")


	plotPad.RedrawAxis()
	
	hCanvas.Print("edgeOverviewRare.pdf")
	hCanvas.Print("edgeOverviewRare.root")
	

	
def main():
	
	OnZPickle = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelvesMT2/OnZBG_36fb.pkl")
	OnZPickleICHEP = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelves/OnZBG_ICHEP_36fb.pkl")
	OnZPickleLegacy = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelves/OnZBG_legacy_36fb.pkl")
	RaresPickle = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelvesMT2/RareOnZ_Powheg.pkl")
	
	
	name = "cutAndCount"
	countingShelves= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , runRanges.name),"legacy": readPickle("cutAndCount",regionsToUse.signal.legacy.name,runRanges.name),"onZ":OnZPickle,"onZICHEP":OnZPickleICHEP,"onZLegacy":OnZPickleLegacy,"Rares":RaresPickle}	
	#~ countingShelves = {"inclusive":readPickle(name,regionsToUse.signal.inclusive.name , runRanges.name),"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	
	

	#~ makeOverviewPlot(countingShelves)	
	makeOverviewPlotNoLegacy(countingShelves)	
	makeOverviewMllPlot(countingShelves,"highNLL",normalizeToBinWidth=True)	
	makeOverviewMllPlot(countingShelves,"lowNLL",normalizeToBinWidth=True)	
	#~ makeOverviewMllPlot(countingShelves,"highNLL",normalizeToBinWidth=False)	
	#~ makeOverviewMllPlot(countingShelves,"lowNLL",normalizeToBinWidth=False)	
	#~ makeOverviewMllPlotBkgOnly(countingShelves,"highNLL",normalizeToBinWidth=True)	
	#~ makeOverviewMllPlotBkgOnly(countingShelves,"lowNLL",normalizeToBinWidth=True)	
	#~ makeOverviewPlotSplitted(countingShelves,"SF")	
main()

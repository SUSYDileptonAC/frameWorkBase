import pickle
import os
import sys


from setTDRStyle import setTDRStyle

from corrections import rSFOF, rEEOF, rMMOF, rOutIn, rSFOFDirect,rSFOFTrig
from centralConfig import zPredictions,OnlyZPredictions, OtherPredictions, regionsToUse, runRanges,systematics
from defs import theCuts

import ROOT
from ROOT import TCanvas

massRanges = {
			"mass20To60":"20-60",
			"mass60To86":"60-86",
			"mass96To150":"96-150",
			"mass150To200":"150-200",
			"mass200To300":"200-300",
			"mass300To400":"300-400",
			"mass400":"$>$400",
			"edgeMass":"20-70",
			"lowMass":"20-86",
			"highMass":"$>$96",
			"highMassOld":"$>$101",
			}

def saveTable(table, name):
	tabFile = open("tab/table_%s.tex"%name, "w")
	tabFile.write(table)
	tabFile.close()
	
### load pickles for the systematics
def loadPickles(path):
	from glob import glob
	result = {}
	for pklPath in glob(path):
		pklFile = open(pklPath, "r")
		result.update(pickle.load(pklFile))
	return result

def readPickle(name,regionName,runName,MC=False):
	
	if MC:
		if os.path.isfile("shelves/%s_%s_%s_MC.pkl"%(name,regionName,runName)):
			result = pickle.load(open("shelves/%s_%s_%s_MC.pkl"%(name,regionName,runName),"rb"))
		else:
			print "shelves/%s_%s_%s_MC.pkl not found, exiting"%(name,regionName,runName) 		
			sys.exit()		
	else:
		if os.path.isfile("shelves/%s_%s_%s.pkl"%(name,regionName,runName)):
			result = pickle.load(open("shelves/%s_%s_%s.pkl"%(name,regionName,runName),"rb"))
		else:
			print "shelves/%s_%s_%s.pkl not found, exiting"%(name,regionName,runName) 		
			sys.exit()

	return result	


tableHeaders = {"default":"being inclusive in the number of b-tagged jets","geOneBTags":"requiring at least one b-tagged jet","geTwoBTags":"requiring at least two b-tagged jets"}
tableColumnHeaders = {"default":"no b-tag requirement","noBTags":"veto on b-tagged jets","geOneBTags":"$\geq$ 1 b-tagged jets","geTwoBTags":"$\geq$ 2 b-tagged jets"}
    
def getWeightedAverage(val1,err1,val2,err2):
	
	weightedAverage = (val1/(err1**2) +val2/(err2**2))/(1./err1**2+1./err2**2)
	weightedAverageErr = 1./(1./err1**2+1./err2**2)**0.5
	
	return weightedAverage, weightedAverageErr

			
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
				
	result["EdgeMassZPredSF"] = shelve["onZLegacy"]["edgeMass_SF"] - shelve["onZLegacy"]["edgeMass_OF"]
	result["EdgeMassZPredSF_Up"] = shelve["onZLegacy"]["edgeMass_SF_Up"] - shelve["onZLegacy"]["edgeMass_OF_Up"]
	result["EdgeMassZPredSF_Down"] = shelve["onZLegacy"]["edgeMass_SF_Down"] - shelve["onZLegacy"]["edgeMass_OF_Down"]
	result["EdgeMassZPredErrSF"] = max(abs(result["EdgeMassZPredSF_Up"]-result["EdgeMassZPredSF"]),abs(result["EdgeMassZPredSF_Down"]-result["EdgeMassZPredSF"]))
						
	result["EdgeMassTotalPredSF"] = result["EdgeMassPredSF"] + result["EdgeMassZPredSF"]
	result["EdgeMassTotalPredErrUpSF"] = ( result["EdgeMassPredStatUpSF"]**2 +  result["EdgeMassPredSystErrSF"]**2 + result["EdgeMassZPredErrSF"]**2 )**0.5
	result["EdgeMassTotalPredErrDownSF"] = ( result["EdgeMassPredStatDownSF"]**2 +  result["EdgeMassPredSystErrSF"]**2 + result["EdgeMassZPredErrSF"]**2 )**0.5
	
	return result


def produceFinalTableOld(shelves):
	
	
	
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Results of the edge-search counting experiment for event yields in the signal regions.
     The statistical and systematic uncertainties are added in quadrature, except for the flavor-symmetric backgrounds.
     Low-mass refers to 20 $<$ \mll $<$ 81\GeV, high-mass to \mll $>$ 101\GeV, ttbar like to \nll < 21, non-ttbar like to \nll $geq$ 21.
     }
  \label{tab:edgeResults}
  \\begin{tabular}{l| c | c | c | c | c}
    \\hline
    \hline
 & \multicolumn{4}{c|}{Baseline signal region} &  \\\\ \n
 \hline
  & Low-mass & Low-mass & High-mass & High-mass & 8 TeV Legacy\\\\ \n
 & ttbar like & non-ttbar like  & ttbar like & non-ttbar like  & region\\\\ \n
 \hline

%s
\hline

%s
\hline
%s
\hline
%s

  \hline
  \hline
       
  \end{tabular}
\end{table}


"""


	observedTemplate = r"        Observed       &  %d                   & %d              &  %d            &  %d       &   %d        \\" +"\n"

	flavSysmTemplate = r"        Flavor-symmetric    & $%.1f\pm%.1f\pm%.1f$        & $%.1f\pm%.1f\pm%.1f$   &  $%.1f\pm%.1f\pm%.1f$  & $%.1f\pm%.1f\pm%.1f$  & $%.1f\pm%.1f\pm%.1f$  \\"+"\n"

	dyTemplate = r"            Drell--Yan          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$  \\"+"\n"
	
	totalTemplate = r"            Total estimated          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ \\"+"\n"
	
	resultsNLL = getResultsNLL(shelves,"NLL")
	resultsLegacy = getResultsLegacy(shelves,"legacy")
		

	observed = observedTemplate%(resultsNLL["lowNLL"]["lowMassSF"],resultsNLL["highNLL"]["lowMassSF"],resultsNLL["lowNLL"]["highMassSF"],resultsNLL["highNLL"]["highMassSF"],resultsLegacy["edgeMassSF"])
		
	flavSym = flavSysmTemplate%(resultsNLL["lowNLL"]["lowMassPredSF"],resultsNLL["lowNLL"]["lowMassPredStatErrSF"],resultsNLL["lowNLL"]["lowMassPredSystErrSF"],resultsNLL["highNLL"]["lowMassPredSF"],resultsNLL["highNLL"]["lowMassPredStatErrSF"],resultsNLL["highNLL"]["lowMassPredSystErrSF"],resultsNLL["lowNLL"]["highMassPredSF"],resultsNLL["lowNLL"]["highMassPredStatErrSF"],resultsNLL["lowNLL"]["highMassPredSystErrSF"],resultsNLL["highNLL"]["highMassPredSF"],resultsNLL["highNLL"]["highMassPredStatErrSF"],resultsNLL["highNLL"]["highMassPredSystErrSF"],resultsLegacy["edgeMassPredSF"],resultsLegacy["edgeMassPredStatErrSF"],resultsLegacy["edgeMassPredSystErrSF"])
	
	dy = dyTemplate%(resultsNLL["lowNLL"]["lowMassZPredSF"],resultsNLL["lowNLL"]["lowMassZPredErrSF"],resultsNLL["highNLL"]["lowMassZPredSF"],resultsNLL["highNLL"]["lowMassZPredErrSF"],resultsNLL["lowNLL"]["highMassZPredSF"],resultsNLL["lowNLL"]["highMassZPredErrSF"],resultsNLL["highNLL"]["highMassZPredSF"],resultsNLL["highNLL"]["highMassZPredErrSF"],resultsLegacy["edgeMassZPredSF"],resultsLegacy["edgeMassZPredErrSF"])
		
	totalPrediction = totalTemplate%(resultsNLL["lowNLL"]["lowMassTotalPredSF"],resultsNLL["lowNLL"]["lowMassTotalPredErrSF"],resultsNLL["highNLL"]["lowMassTotalPredSF"],resultsNLL["highNLL"]["lowMassTotalPredErrSF"],resultsNLL["lowNLL"]["highMassTotalPredSF"],resultsNLL["lowNLL"]["highMassTotalPredErrSF"],resultsNLL["highNLL"]["highMassTotalPredSF"],resultsNLL["highNLL"]["highMassTotalPredErrSF"],resultsLegacy["edgeMassTotalPredSF"],resultsLegacy["edgeMassTotalPredErrSF"])


		
	table = tableTemplate%(observed,flavSym,dy,totalPrediction)
	saveTable(table,"cutNCount_Result_SF")

def produceFinalTable(shelves):
	
	
	
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Results of the edge-search counting experiment for event yields in the signal regions.
     The statistical and systematic uncertainties are added in quadrature.
     ttbar like refers to $NLL<$ 21, non-ttbar like to $NLL\geq$ 21.
     }
  \label{tab:edgeResults}
  \\begin{tabular}{ c | c | c | c | c| c}
    \hline

Mass range [GeV] & FS & Template & Rares & Sum & Observed \\\\ \n

    \hline
 \multicolumn{6}{c}{ttbar like}  \\\\ \n
    \hline
%s
%s
%s
%s
%s
%s
%s
\hline
  \multicolumn{6}{c}{non ttbar like}   \\\\ \n
\hline
%s
%s
%s
%s
%s
%s
%s
\hline
  \multicolumn{6}{c}{Super signal regions (non ttbar like)}  \\\\ \n
\hline
%s
%s
\hline
  \multicolumn{6}{c}{ICHEP legacy region}  \\\\ \n
\hline
%s
\hline
  \multicolumn{6}{c}{8 TeV legacy region}  \\\\ \n 
\hline
%s


  \end{tabular}
\end{table}


"""

	lineTemplate = r" %s   &  %.1f$^{+%.1f}_{-%.1f}$    & %.1f$\pm$%.1f   & %.1f$\pm$%.1f  &  %.1f$^{+%.1f}_{-%.1f}$ & %d \\"+"\n"
	lineTemplateLegacy = r" %s   &  %.1f$^{+%.1f}_{-%.1f}$    & \multicolumn{2}{c|}{%.1f$\pm$%.1f}  &  %.1f$^{+%.1f}_{-%.1f}$ & %d \\"+"\n"

		
	resultsNLL = getResultsNLL(shelves,"NLL")
	resultsLegacy = getResultsLegacy(shelves,"legacy")
		
	massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
	
	lines = {}
	
	
	for massBin in massBins:
		lines["lowNLL_"+massBin] = lineTemplate%(massRanges[massBin],
													#~ resultsNLL["lowNLL"]["highMT2_%s_PredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredStatUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredStatDownSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredSystErrSF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_PredSF"%massBin],(resultsNLL["lowNLL"]["highMT2_%s_PredStatUpSF"%massBin]**2 + resultsNLL["lowNLL"]["highMT2_%s_PredSystErrSF"%massBin]**2)**0.5,(resultsNLL["lowNLL"]["highMT2_%s_PredStatDownSF"%massBin]**2 + resultsNLL["lowNLL"]["highMT2_%s_PredSystErrSF"%massBin]**2)**0.5,
													resultsNLL["lowNLL"]["highMT2_%s_ZPredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_ZPredErrSF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_RarePredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_RarePredErrSF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_TotalPredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_TotalPredErrUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_TotalPredErrDownSF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_SF"%massBin])
		
		lines["highNLL_"+massBin] = lineTemplate%(massRanges[massBin],
													#~ resultsNLL["highNLL"]["highMT2_%s_PredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredStatUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredStatDownSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredSystErrSF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_PredSF"%massBin],(resultsNLL["highNLL"]["highMT2_%s_PredStatUpSF"%massBin]**2 + resultsNLL["highNLL"]["highMT2_%s_PredSystErrSF"%massBin]**2)**0.5,(resultsNLL["highNLL"]["highMT2_%s_PredStatDownSF"%massBin]**2 + resultsNLL["highNLL"]["highMT2_%s_PredSystErrSF"%massBin]**2)**0.5,
													resultsNLL["highNLL"]["highMT2_%s_ZPredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_ZPredErrSF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_RarePredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_RarePredErrSF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_TotalPredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_TotalPredErrUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_TotalPredErrDownSF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_SF"%massBin])
	
	lines["highNLL_lowMass"] = lineTemplate%(massRanges["lowMass"],
												#~ resultsNLL["highNLL"]["highMT2_lowMass_PredSF"],resultsNLL["highNLL"]["highMT2_lowMass_PredStatUpSF"],resultsNLL["highNLL"]["highMT2_lowMass_PredStatDownSF"],resultsNLL["highNLL"]["highMT2_lowMass_PredSystErrSF"],
												resultsNLL["highNLL"]["highMT2_lowMass_PredSF"],(resultsNLL["highNLL"]["highMT2_lowMass_PredStatUpSF"]**2 + resultsNLL["highNLL"]["highMT2_lowMass_PredSystErrSF"]**2)**0.5,(resultsNLL["highNLL"]["highMT2_lowMass_PredStatDownSF"]**2 + resultsNLL["highNLL"]["highMT2_lowMass_PredSystErrSF"]**2)**0.5,
												resultsNLL["highNLL"]["highMT2_lowMass_ZPredSF"],resultsNLL["highNLL"]["highMT2_lowMass_ZPredErrSF"],
												resultsNLL["highNLL"]["highMT2_lowMass_RarePredSF"],resultsNLL["highNLL"]["highMT2_lowMass_RarePredErrSF"],
												resultsNLL["highNLL"]["highMT2_lowMass_TotalPredSF"],resultsNLL["highNLL"]["highMT2_lowMass_TotalPredErrUpSF"],resultsNLL["highNLL"]["highMT2_lowMass_TotalPredErrDownSF"],
												resultsNLL["highNLL"]["highMT2_lowMass_SF"])
												
	lines["highNLL_highMass"] = lineTemplate%(massRanges["highMass"],
												#~ resultsNLL["highNLL"]["highMT2_highMass_PredSF"],resultsNLL["highNLL"]["highMT2_highMass_PredStatUpSF"],resultsNLL["highNLL"]["highMT2_highMass_PredStatDownSF"],resultsNLL["highNLL"]["highMT2_highMass_PredSystErrSF"],
												resultsNLL["highNLL"]["highMT2_highMass_PredSF"],(resultsNLL["highNLL"]["highMT2_highMass_PredStatUpSF"]**2 + resultsNLL["highNLL"]["highMT2_highMass_PredSystErrSF"]**2)**0.5,(resultsNLL["highNLL"]["highMT2_highMass_PredStatDownSF"]**2 + resultsNLL["highNLL"]["highMT2_highMass_PredSystErrSF"]**2)**0.5,
												resultsNLL["highNLL"]["highMT2_highMass_ZPredSF"],resultsNLL["highNLL"]["highMT2_highMass_ZPredErrSF"],
												resultsNLL["highNLL"]["highMT2_highMass_RarePredSF"],resultsNLL["highNLL"]["highMT2_highMass_RarePredErrSF"],
												resultsNLL["highNLL"]["highMT2_highMass_TotalPredSF"],resultsNLL["highNLL"]["highMT2_highMass_TotalPredErrUpSF"],resultsNLL["highNLL"]["highMT2_highMass_TotalPredErrDownSF"],
												resultsNLL["highNLL"]["highMT2_highMass_SF"])
		
	lines["highNLL_highMassOld"] = lineTemplateLegacy%(massRanges["highMassOld"],
												#~ resultsNLL["highNLL"]["highMassOld_PredSF"],resultsNLL["highNLL"]["highMassOld_PredStatUpSF"],resultsNLL["highNLL"]["highMassOld_PredStatDownSF"],resultsNLL["highNLL"]["highMassOld_PredSystErrSF"],
												resultsNLL["highNLL"]["highMassOld_PredSF"],(resultsNLL["highNLL"]["highMassOld_PredStatUpSF"]**2 + resultsNLL["highNLL"]["highMassOld_PredSystErrSF"]**2)**0.5,(resultsNLL["highNLL"]["highMassOld_PredStatDownSF"]**2 + resultsNLL["highNLL"]["highMassOld_PredSystErrSF"]**2)**0.5,
												resultsNLL["highNLL"]["highMassOld_ZPredSF"],resultsNLL["highNLL"]["highMassOld_ZPredErrSF"],
												resultsNLL["highNLL"]["highMassOld_TotalPredSF"],resultsNLL["highNLL"]["highMassOld_TotalPredErrUpSF"],resultsNLL["highNLL"]["highMassOld_TotalPredErrDownSF"],
												resultsNLL["highNLL"]["highMassOld_SF"])
												
		
	lines["EdgeMass"] = lineTemplateLegacy%(massRanges["edgeMass"],
												#~ resultsLegacy["EdgeMassPredSF"],resultsLegacy["EdgeMassPredStatUpSF"],resultsLegacy["EdgeMassPredStatDownSF"],resultsLegacy["EdgeMassPredSystErrSF"],
												resultsLegacy["EdgeMassPredSF"],(resultsLegacy["EdgeMassPredStatUpSF"]**2 + resultsLegacy["EdgeMassPredSystErrSF"]**2)**0.5,(resultsLegacy["EdgeMassPredStatDownSF"]**2 + resultsLegacy["EdgeMassPredSystErrSF"]**2)**0.5,
												resultsLegacy["EdgeMassZPredSF"],resultsLegacy["EdgeMassZPredErrSF"],
												resultsLegacy["EdgeMassTotalPredSF"],resultsLegacy["EdgeMassTotalPredErrUpSF"],resultsLegacy["EdgeMassTotalPredErrDownSF"],
												resultsLegacy["EdgeMassSF"])
		
	
	table = tableTemplate%(
							lines["lowNLL_mass20To60"],lines["lowNLL_mass60To86"],lines["lowNLL_mass96To150"],lines["lowNLL_mass150To200"],lines["lowNLL_mass200To300"],lines["lowNLL_mass300To400"],lines["lowNLL_mass400"],
							lines["highNLL_mass20To60"],lines["highNLL_mass60To86"],lines["highNLL_mass96To150"],lines["highNLL_mass150To200"],lines["highNLL_mass200To300"],lines["highNLL_mass300To400"],lines["highNLL_mass400"],
							lines["highNLL_lowMass"],lines["highNLL_highMass"],
							lines["highNLL_highMassOld"],lines["EdgeMass"]
							)
							
	saveTable(table,"cutNCount_Result_SF")	

def produceROutInStudyTable(shelves):
	
	
	
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Background prediction of the edge-search counting experiment for event yields in the signal regions.
     The statistical and systematic uncertainties are added in quadrature, except for the flavor-symmetric backgrounds.
     ttbar like refers to \nll $<$ 21, non-ttbar like to \nll $\geq$ 21.
     }
  \label{tab:edgeResults}
  \\begin{tabular}{ c | c | c | c | c}
    \hline

mass range [GeV] & Flavor-symmetric & DY (template) & Rare*r$_{out/in}$ & Rare direct & tot. est. r$_{out/in}$ & tot. direct \\\\ \n

    \hline
 \multicolumn{7}{c}{ttbar like}  \\\\ \n
    \hline
%s
%s
%s
%s
%s
%s
%s
\hline
  \multicolumn{7}{c}{non ttbar like}   \\\\ \n
\hline
%s
%s
%s
%s
%s
%s
%s



  \end{tabular}
\end{table}


"""

	lineTemplate = r" %s   &  %.1f$^{+%.1f}_{-%.1f}\pm$%.1f    & %.2f$\pm$%.2f & %.2f$\pm$%.2f   & %.2f$\pm$%.2f  &  %.1f$^{+%.1f}_{-%.1f}$ &  %.1f$^{+%.1f}_{-%.1f}$ \\"+"\n"

		
	resultsNLL = getResultsNLL(shelves,"NLL")
	resultsLegacy = getResultsLegacy(shelves,"legacy")
		
	massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
	
	lines = {}
	
	
	for massBin in massBins:
		lines["lowNLL_"+massBin] = lineTemplate%(massRanges[massBin],
													resultsNLL["lowNLL"]["highMT2_%s_PredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredStatUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredStatDownSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredSystErrSF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_ZPredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_ZPredErrSF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_RarePredROutInSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_RarePredROutInErrSF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_RarePredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_RarePredErrSF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_TotalPredROutInSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_TotalPredROutInErrUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_TotalPredROutInErrDownSF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_TotalPredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_TotalPredErrUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_TotalPredErrDownSF"%massBin]
													)
		
		lines["highNLL_"+massBin] = lineTemplate%(massRanges[massBin],
													resultsNLL["highNLL"]["highMT2_%s_PredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredStatUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredStatDownSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredSystErrSF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_ZPredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_ZPredErrSF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_RarePredROutInSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_RarePredROutInErrSF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_RarePredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_RarePredErrSF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_TotalPredROutInSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_TotalPredROutInErrUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_TotalPredROutInErrDownSF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_TotalPredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_TotalPredErrUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_TotalPredErrDownSF"%massBin]
													)
	
	
	
	table = tableTemplate%(
							lines["lowNLL_mass20To60"],lines["lowNLL_mass60To86"],lines["lowNLL_mass96To150"],lines["lowNLL_mass150To200"],lines["lowNLL_mass200To300"],lines["lowNLL_mass300To400"],lines["lowNLL_mass400"],
							lines["highNLL_mass20To60"],lines["highNLL_mass60To86"],lines["highNLL_mass96To150"],lines["highNLL_mass150To200"],lines["highNLL_mass200To300"],lines["highNLL_mass300To400"],lines["highNLL_mass400"],
							
							)
							
	saveTable(table,"cutNCount_RareStudy_SF")	
	
	
	


def produceFlavSymTable(shelves):
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Resulting estimates for flavour-symmetric backgrounds. Given is the observed event yield in \EM events,
 the estimate in the SF channel using the event-by-event reweighting of the factorization method,  
 R$_{SF/OF}$ for the factorization method, R$_{SF/OF}$ when combining this value with the constant R$_{SF/OF}$ from
   direct measurement,  and the combined final prediction. 
   Statistical and systematic uncertainties are given separately.
     }
  \label{tab:FlavSymBackgrounds}
  \\begin{tabular}{ c | c | c | c | c | c}
    \hline

Mass range [GeV] & OF events & pred. fact. method & R$_{SF/OF}$ fact. method & comb. R$_{SF/OF}$ & pred. \\\\ \n

    \hline
 \multicolumn{6}{c}{ttbar like} \\\\ \n
    \hline
%s
%s
%s
%s
%s
%s
%s
\hline
  \multicolumn{6}{c}{non ttbar like}  \\\\ \n
\hline
%s
%s
%s
%s
%s
%s
%s
\hline
  \multicolumn{6}{c}{ICHEP legacy region}  \\\\ \n
\hline
%s
\hline
  \multicolumn{6}{c}{8 TeV legacy region}  \\\\ \n 
\hline
%s


  \end{tabular}
\end{table}


"""

	flavSysmTemplate = r" %s   & %d    & %.1f$^{+%.1f}_{-%.1f}\pm$%.1f  &  %.2f$\pm$%.2f & %.2f$\pm$%.2f & %.1f$^{+%.1f}_{-%.1f}\pm$%.1f \\"+"\n"

		
	resultsNLL = getResultsNLL(shelves,"NLL")
	resultsLegacy = getResultsLegacy(shelves,"legacy")
		
	massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
	
	lines = {}
	
	for massBin in massBins:
		lines["lowNLL_"+massBin] = flavSysmTemplate%(massRanges[massBin],
													resultsNLL["lowNLL"]["highMT2_%s_OF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_PredFactSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredFactStatUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredFactStatDownSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredFactSystErrSF"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_RSFOF_Fact"%massBin],resultsNLL["lowNLL"]["highMT2_%s_RSFOF_Fact_Err"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_RSFOF_Combined"%massBin],resultsNLL["lowNLL"]["highMT2_%s_RSFOF_Combined_Err"%massBin],
													resultsNLL["lowNLL"]["highMT2_%s_PredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredStatUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredStatDownSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredSystErrSF"%massBin])
		
		lines["highNLL_"+massBin] = flavSysmTemplate%(massRanges[massBin],
													resultsNLL["highNLL"]["highMT2_%s_OF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_PredFactSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredFactStatUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredFactStatDownSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredFactSystErrSF"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_RSFOF_Fact"%massBin],resultsNLL["highNLL"]["highMT2_%s_RSFOF_Fact_Err"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_RSFOF_Combined"%massBin],resultsNLL["highNLL"]["highMT2_%s_RSFOF_Combined_Err"%massBin],
													resultsNLL["highNLL"]["highMT2_%s_PredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredStatUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredStatDownSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredSystErrSF"%massBin])
		
	lines["highNLLHighMass"] = flavSysmTemplate%(massRanges["highMassOld"],
												resultsNLL["highNLL"]["highMassOld_OF"],
												resultsNLL["highNLL"]["highMassOld_PredFactSF"],resultsNLL["highNLL"]["highMassOld_PredFactStatUpSF"],resultsNLL["highNLL"]["highMassOld_PredFactStatDownSF"],resultsNLL["highNLL"]["highMassOld_PredFactSystErrSF"],
												resultsNLL["highNLL"]["highMassOld_RSFOF_Fact"],resultsNLL["highNLL"]["highMassOld_RSFOF_Fact_Err"],
												resultsNLL["highNLL"]["highMassOld_RSFOF_Combined"],resultsNLL["highNLL"]["highMassOld_RSFOF_Combined_Err"],
												resultsNLL["highNLL"]["highMassOld_PredSF"],resultsNLL["highNLL"]["highMassOld_PredStatUpSF"],resultsNLL["highNLL"]["highMassOld_PredStatDownSF"],resultsNLL["highNLL"]["highMassOld_PredSystErrSF"])
		
	lines["EdgeMass"] = flavSysmTemplate%(massRanges["edgeMass"],
												resultsLegacy["EdgeMassOF"],
												resultsLegacy["EdgeMassPredFactSF"],resultsLegacy["EdgeMassPredFactStatUpSF"],resultsLegacy["EdgeMassPredFactStatDownSF"],resultsLegacy["EdgeMassPredFactSystErrSF"],
												resultsLegacy["EdgeMassRSFOFFact"],resultsLegacy["EdgeMassRSFOFFactErr"],
												resultsLegacy["EdgeMassRSFOFCombined"],resultsLegacy["EdgeMassRSFOFCombinedErr"],
												resultsLegacy["EdgeMassPredSF"],resultsLegacy["EdgeMassPredStatUpSF"],resultsLegacy["EdgeMassPredStatDownSF"],resultsLegacy["EdgeMassPredSystErrSF"])
		
	table = tableTemplate%(
							lines["lowNLL_mass20To60"],lines["lowNLL_mass60To86"],lines["lowNLL_mass96To150"],lines["lowNLL_mass150To200"],lines["lowNLL_mass200To300"],lines["lowNLL_mass300To400"],lines["lowNLL_mass400"],
							lines["highNLL_mass20To60"],lines["highNLL_mass60To86"],lines["highNLL_mass96To150"],lines["highNLL_mass150To200"],lines["highNLL_mass200To300"],lines["highNLL_mass300To400"],lines["highNLL_mass400"],
							lines["highNLLHighMass"],lines["EdgeMass"]
							)
		
	saveTable(table,"cutNCount_FlavSymBkgs")	
	
def produceFlavSymTableLowMT2(shelves):
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Resulting estimates for flavour-symmetric backgrounds. Given is the observed event yield in \EM events and the resulting estimate in the SF channel using the factorization method,
   the control region method and the combination of both methods. 
   Statistical and systematic uncertainties are given separately.
     }
  \label{tab:FlavSymBackgrounds}
  \\begin{tabular}{ c | c | c | c | c | c | c}
    \hline

mass range [GeV] & OF events & pred. fact. method & R$_{SF/OF}$ fact. method & comb. R$_{SF/OF}$ & pred. & SF yield \\\\ \n

    \hline
 \multicolumn{7}{c}{ttbar like}  \\\\ \n
    \hline
%s
%s
%s
%s
%s
%s
%s
\hline
  \multicolumn{7}{c}{non ttbar like} \\\\ \n
\hline
%s
%s
%s
%s
%s
%s
%s



  \end{tabular}
\end{table}


"""

	flavSysmTemplate = r" %s   & %d    & %.1f$^{+%.1f}_{-%.1f}\pm$%.1f  &  %.2f$\pm$%.2f & %.2f$\pm$%.2f & %.1f$^{+%.1f}_{-%.1f}\pm$%.1f & %d \\"+"\n"

		
	resultsNLL = getResultsNLL(shelves,"NLL")
		
	massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
	
	lines = {}
	
	for massBin in massBins:
		lines["lowNLL_"+massBin] = flavSysmTemplate%(massRanges[massBin],
													resultsNLL["lowNLL"]["lowMT2_%s_OF"%massBin],
													resultsNLL["lowNLL"]["lowMT2_%s_PredFactSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredFactStatUpSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredFactStatDownSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredFactSystErrSF"%massBin],
													resultsNLL["lowNLL"]["lowMT2_%s_RSFOF_Fact"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_RSFOF_Fact_Err"%massBin],
													resultsNLL["lowNLL"]["lowMT2_%s_RSFOF_Combined"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_RSFOF_Combined_Err"%massBin],
													resultsNLL["lowNLL"]["lowMT2_%s_PredSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredStatUpSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredStatDownSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredSystErrSF"%massBin],
													resultsNLL["lowNLL"]["lowMT2_%s_SF"%massBin])
		
		lines["highNLL_"+massBin] = flavSysmTemplate%(massRanges[massBin],
													resultsNLL["highNLL"]["lowMT2_%s_OF"%massBin],
													resultsNLL["highNLL"]["lowMT2_%s_PredFactSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredFactStatUpSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredFactStatDownSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredFactSystErrSF"%massBin],
													resultsNLL["highNLL"]["lowMT2_%s_RSFOF_Fact"%massBin],resultsNLL["highNLL"]["lowMT2_%s_RSFOF_Fact_Err"%massBin],
													resultsNLL["highNLL"]["lowMT2_%s_RSFOF_Combined"%massBin],resultsNLL["highNLL"]["lowMT2_%s_RSFOF_Combined_Err"%massBin],
													resultsNLL["highNLL"]["lowMT2_%s_PredSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredStatUpSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredStatDownSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredSystErrSF"%massBin],
													resultsNLL["highNLL"]["lowMT2_%s_SF"%massBin])
		
		
	table = tableTemplate%(
							lines["lowNLL_mass20To60"],lines["lowNLL_mass60To86"],lines["lowNLL_mass96To150"],lines["lowNLL_mass150To200"],lines["lowNLL_mass200To300"],lines["lowNLL_mass300To400"],lines["lowNLL_mass400"],
							lines["highNLL_mass20To60"],lines["highNLL_mass60To86"],lines["highNLL_mass96To150"],lines["highNLL_mass150To200"],lines["highNLL_mass200To300"],lines["highNLL_mass300To400"],lines["highNLL_mass400"],
							)
		
	saveTable(table,"cutNCount_FlavSymBkgs_LowMT2")	
	
	
def main():
	
	OnZPickle = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelvesMT2/OnZBG_36fb.pkl")
	OnZPickleICHEP = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelves/OnZBG_ICHEP_36fb.pkl")
	OnZPickleLegacy = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelves/OnZBG_legacy_36fb.pkl")
	RaresPickle = loadPickles("/disk1/user/schomakers/SignalRegionOptimationStudies/shelvesMT2/RareOnZ_Powheg.pkl")
	
	name = "cutAndCount"
	countingShelves= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , runRanges.name),"legacy": readPickle("cutAndCount",regionsToUse.signal.legacy.name,runRanges.name),"Rares":RaresPickle,"onZ":OnZPickle,"onZICHEP":OnZPickleICHEP,"onZLegacy":OnZPickleLegacy}	
		
	
	produceFlavSymTable(countingShelves)
	#~ produceFlavSymTableLowMT2(countingShelves)
	produceFinalTable(countingShelves)
	#~ produceROutInStudyTable(countingShelves)
	
main()

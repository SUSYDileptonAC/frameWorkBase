### script to make a single overview plot off all 30 signal regions

import pickle
import os
import sys


from setTDRStyle import setTDRStyle

from corrections import rSFOF, rEEOF, rMMOF, rOutIn, rOutInEE, rOutInMM
from centralConfig import zPredictions, regionsToUse, runRanges, OtherPredictions, OnlyZPredictions

import ROOT
from ROOT import TCanvas
ROOT.gROOT.SetBatch(True)

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


def getResults(shelve,region,selection):
	
	### get the corrections from corrections.py, z predicition from centralConfig.py and the results from the .pkl files
	
	result = {}
	
	result["rSFOF"] = getattr(rSFOF,region).val
	result["rSFOFErr"] = getattr(rSFOF,region).err
	result["rEEOF"] = getattr(rEEOF,region).val
	result["rEEOFErr"] = getattr(rEEOF,region).err
	result["rMMOF"] = getattr(rMMOF,region).val
	result["rMMOFErr"] = getattr(rMMOF,region).err
	
	### low mass region
	
	### fetch event counts from pkls	
	result["lowMassEE"] = shelve[region][selection]["edgeMass"]["EE"]
	result["lowMassMM"] = shelve[region][selection]["edgeMass"]["MM"]
	result["lowMassSF"] = shelve[region][selection]["edgeMass"]["EE"] + shelve[region][selection]["edgeMass"]["MM"]
	result["lowMassOF"] = shelve[region][selection]["edgeMass"]["EM"]
	### take R_SF/OF into account
	result["lowMassPredSF"] = result["lowMassOF"]*getattr(rSFOF,region).val
	result["lowMassPredStatErrSF"] = result["lowMassOF"]**0.5*getattr(rSFOF,region).val
	result["lowMassPredSystErrSF"] = result["lowMassOF"]*getattr(rSFOF,region).err
	
	### Z predcition from centralConfig multiplied by R_Out/In for the region
	result["lowMassZPredSF"] = getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.lowMass,region).val
	result["lowMassZPredErrSF"] = ((getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.lowMass,region).err)**2 + (getattr(getattr(zPredictions,selection).SF,region).err*getattr(rOutIn.lowMass,region).val)**2 )**0.5
	
	result["lowMassOnlyZPredSF"] = getattr(getattr(OnlyZPredictions,selection).SF,region).val*getattr(rOutIn.lowMass,region).val	
	result["lowMassOtherPredSF"] = getattr(getattr(OtherPredictions,selection).SF,region).val*getattr(rOutIn.lowMass,region).val
	
	result["lowMassTotalPredSF"] = result["lowMassPredSF"] + result["lowMassZPredSF"]
	result["lowMassTotalPredErrSF"] = ( result["lowMassPredStatErrSF"]**2 +  result["lowMassPredSystErrSF"]**2 + result["lowMassZPredErrSF"]**2 )**0.5
	
	### same for below Z region
	result["belowZEE"] = shelve[region][selection]["belowZ"]["EE"]
	result["belowZMM"] = shelve[region][selection]["belowZ"]["MM"]
	result["belowZSF"] = shelve[region][selection]["belowZ"]["EE"] + shelve[region][selection]["belowZ"]["MM"]
	result["belowZOF"] = shelve[region][selection]["belowZ"]["EM"]
	
	result["belowZPredSF"] = result["belowZOF"]*getattr(rSFOF,region).val
	result["belowZPredStatErrSF"] = result["belowZOF"]**0.5*getattr(rSFOF,region).val
	result["belowZPredSystErrSF"] = result["belowZOF"]*getattr(rSFOF,region).err
	
	result["belowZZPredSF"] = getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.belowZ,region).val
	result["belowZZPredErrSF"] = ((getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.belowZ,region).err)**2 + (getattr(getattr(zPredictions,selection).SF,region).err*getattr(rOutIn.belowZ,region).val)**2 )**0.5
	
	result["belowZOnlyZPredSF"] = getattr(getattr(OnlyZPredictions,selection).SF,region).val*getattr(rOutIn.belowZ,region).val	
	result["belowZOtherPredSF"] = getattr(getattr(OtherPredictions,selection).SF,region).val*getattr(rOutIn.belowZ,region).val
	
	result["belowZTotalPredSF"] = result["belowZPredSF"] + result["belowZZPredSF"]
	result["belowZTotalPredErrSF"] = ( result["belowZPredStatErrSF"]**2 +  result["belowZPredSystErrSF"]**2 + result["belowZZPredErrSF"]**2 )**0.5
	
	### same for above Z region
	result["aboveZEE"] = shelve[region][selection]["aboveZ"]["EE"]
	result["aboveZMM"] = shelve[region][selection]["aboveZ"]["MM"]
	result["aboveZSF"] = shelve[region][selection]["aboveZ"]["EE"] + shelve[region][selection]["aboveZ"]["MM"]
	result["aboveZOF"] = shelve[region][selection]["aboveZ"]["EM"]
	
	result["aboveZPredSF"] = result["aboveZOF"]*getattr(rSFOF,region).val
	result["aboveZPredStatErrSF"] = result["aboveZOF"]**0.5*getattr(rSFOF,region).val
	result["aboveZPredSystErrSF"] = result["aboveZOF"]*getattr(rSFOF,region).err
	
	result["aboveZZPredSF"] = getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.aboveZ,region).val
	result["aboveZZPredErrSF"] = ((getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.aboveZ,region).err)**2 + (getattr(getattr(zPredictions,selection).SF,region).err*getattr(rOutIn.aboveZ,region).val)**2 )**0.5
	
	result["aboveZOnlyZPredSF"] = getattr(getattr(OnlyZPredictions,selection).SF,region).val*getattr(rOutIn.aboveZ,region).val	
	result["aboveZOtherPredSF"] = getattr(getattr(OtherPredictions,selection).SF,region).val*getattr(rOutIn.aboveZ,region).val
	
	result["aboveZTotalPredSF"] = result["aboveZPredSF"] + result["aboveZZPredSF"]
	result["aboveZTotalPredErrSF"] = ( result["aboveZPredStatErrSF"]**2 +  result["aboveZPredSystErrSF"]**2 + result["aboveZZPredErrSF"]**2 )**0.5
	
	### same for high mass region	
	result["highMassEE"] = shelve[region][selection]["highMass"]["EE"]
	result["highMassMM"] = shelve[region][selection]["highMass"]["MM"]
	result["highMassSF"] = shelve[region][selection]["highMass"]["EE"] + shelve[region][selection]["highMass"]["MM"]
	result["highMassOF"] = shelve[region][selection]["highMass"]["EM"]
	
	result["highMassPredSF"] = result["highMassOF"]*getattr(rSFOF,region).val
	result["highMassPredStatErrSF"] = result["highMassOF"]**0.5*getattr(rSFOF,region).val
	result["highMassPredSystErrSF"] = result["highMassOF"]*getattr(rSFOF,region).err
	
	result["highMassZPredSF"] = getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.highMass,region).val
	result["highMassZPredErrSF"] = ((getattr(getattr(zPredictions,selection).SF,region).val*getattr(rOutIn.highMass,region).err)**2 + (getattr(getattr(zPredictions,selection).SF,region).err*getattr(rOutIn.highMass,region).val)**2 )**0.5
	
	result["highMassOnlyZPredSF"] = getattr(getattr(OnlyZPredictions,selection).SF,region).val*getattr(rOutIn.highMass,region).val	
	result["highMassOtherPredSF"] = getattr(getattr(OtherPredictions,selection).SF,region).val*getattr(rOutIn.highMass,region).val
	
	result["highMassTotalPredSF"] = result["highMassPredSF"] + result["highMassZPredSF"]
	result["highMassTotalPredErrSF"] = ( result["highMassPredStatErrSF"]**2 +  result["highMassPredSystErrSF"]**2 + result["highMassZPredErrSF"]**2 )**0.5
	
	### on Z region: No R_Out/In required
	result["onZEE"] = shelve[region][selection]["zMass"]["EE"]
	result["onZMM"] = shelve[region][selection]["zMass"]["MM"]
	result["onZSF"] = shelve[region][selection]["zMass"]["EE"] + shelve[region][selection]["zMass"]["MM"]
	result["onZOF"] = shelve[region][selection]["zMass"]["EM"]	
	
	result["onZPredSF"] = result["onZOF"]*getattr(rSFOF,region).val
	result["onZPredStatErrSF"] = result["onZOF"]**0.5*getattr(rSFOF,region).val
	result["onZPredSystErrSF"] = result["onZOF"]*getattr(rSFOF,region).err
	
	result["onZZPredSF"] = getattr(getattr(zPredictions,selection).SF,region).val
	result["onZZPredErrSF"] = getattr(getattr(zPredictions,selection).SF,region).err
	
	result["onZOnlyZPredSF"] = getattr(getattr(OnlyZPredictions,selection).SF,region).val	
	result["onZOtherPredSF"] = getattr(getattr(OtherPredictions,selection).SF,region).val
	
	result["onZTotalPredSF"] = result["onZPredSF"] + result["onZZPredSF"]
	result["onZTotalPredErrSF"] = ( result["onZPredStatErrSF"]**2 +  result["onZPredSystErrSF"]**2 + result["onZZPredErrSF"]**2 )**0.5
	
	
	return result

	
def makeOverviewPlot(countingShelves,region):
	
	### make an overview plot that contains all 30 signal regions as bar charts

	from helpers import createMyColors
	from defs import myColors
	colors = createMyColors()	

	### fetch results for central/forward and the 3 b-tag regions
	resultsCentral = getResults(countingShelves,"central","default")
	resultsForward = getResults(countingShelves,"forward","default")
	resultsCentralNoBTags = getResults(countingShelves,"central","noBTags")
	resultsForwardNoBTags = getResults(countingShelves,"forward","noBTags")
	resultsCentralGeOneBTags = getResults(countingShelves,"central","geOneBTags")
	resultsForwardGeOneBTags = getResults(countingShelves,"forward","geOneBTags")
	
	### histograms for data, the different and the total background
	histTotal = ROOT.TH1F("histTotal","histTotal",30,0,30)
	
	histObs = ROOT.TH1F("histObs","histObs",30,0,30)
	
	histObs.SetMarkerColor(ROOT.kBlack)
	histObs.SetLineColor(ROOT.kBlack)
	histObs.SetMarkerStyle(20)
	
	histPred = ROOT.TH1F("histPred","histPred",30,0,30)
	histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",30,0,30)
	histOnlyDY = ROOT.TH1F("histDY","histDY",30,0,30)
	histOther = ROOT.TH1F("histOther","histOther",30,0,30)
	
	### get canvas and style
	hCanvas = TCanvas("hCanvas", "Distribution", 1000,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style=setTDRStyle()
	style.SetPadBottomMargin(0.2)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()	
	
	### fill the histogram for observed data for each region
	histObs.SetBinContent(1,resultsCentral["lowMassSF"])
	histObs.SetBinContent(2,resultsCentralNoBTags["lowMassSF"])
	histObs.SetBinContent(3,resultsCentralGeOneBTags["lowMassSF"])
	histObs.SetBinContent(4,resultsForward["lowMassSF"])
	histObs.SetBinContent(5,resultsForwardNoBTags["lowMassSF"])
	histObs.SetBinContent(6,resultsForwardGeOneBTags["lowMassSF"])
	
	histObs.SetBinContent(7,resultsCentral["belowZSF"])
	histObs.SetBinContent(8,resultsCentralNoBTags["belowZSF"])
	histObs.SetBinContent(9,resultsCentralGeOneBTags["belowZSF"])
	histObs.SetBinContent(10,resultsForward["belowZSF"])
	histObs.SetBinContent(11,resultsForwardNoBTags["belowZSF"])
	histObs.SetBinContent(12,resultsForwardGeOneBTags["belowZSF"])

	histObs.SetBinContent(13,resultsCentral["onZSF"])
	histObs.SetBinContent(14,resultsCentralNoBTags["onZSF"])
	histObs.SetBinContent(15,resultsCentralGeOneBTags["onZSF"])
	histObs.SetBinContent(16,resultsForward["onZSF"])
	histObs.SetBinContent(17,resultsForwardNoBTags["onZSF"])
	histObs.SetBinContent(18,resultsForwardGeOneBTags["onZSF"])
	
	histObs.SetBinContent(19,resultsCentral["aboveZSF"])
	histObs.SetBinContent(20,resultsCentralNoBTags["aboveZSF"])
	histObs.SetBinContent(21,resultsCentralGeOneBTags["aboveZSF"])		
	histObs.SetBinContent(22,resultsForward["aboveZSF"])
	histObs.SetBinContent(23,resultsForwardNoBTags["aboveZSF"])
	histObs.SetBinContent(24,resultsForwardGeOneBTags["aboveZSF"])

	histObs.SetBinContent(25,resultsCentral["highMassSF"])
	histObs.SetBinContent(26,resultsCentralNoBTags["highMassSF"])
	histObs.SetBinContent(27,resultsCentralGeOneBTags["highMassSF"])
	histObs.SetBinContent(28,resultsForward["highMassSF"])
	histObs.SetBinContent(29,resultsForwardNoBTags["highMassSF"])	
	histObs.SetBinContent(30,resultsForwardGeOneBTags["highMassSF"])

	### put labels below each bar
	names = ["inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)","inclusive (c)","b-Veto (c)","b-Tagged (c)","inclusive (f)","b-Veto (f)","b-Tagged (f)"]
	
	for index, name in enumerate(names):
	
		histObs.GetXaxis().SetBinLabel(index+1,name)
	

	### fill histogram for FS background
	histFlavSym.SetBinContent(1,resultsCentral["lowMassPredSF"])
	histFlavSym.SetBinContent(2,resultsCentralNoBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(3,resultsCentralGeOneBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(4,resultsForward["lowMassPredSF"])
	histFlavSym.SetBinContent(5,resultsForwardNoBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(6,resultsForwardGeOneBTags["lowMassPredSF"])
	
	histFlavSym.SetBinContent(7,resultsCentral["belowZPredSF"])
	histFlavSym.SetBinContent(8,resultsCentralNoBTags["belowZPredSF"])
	histFlavSym.SetBinContent(9,resultsCentralGeOneBTags["belowZPredSF"])
	histFlavSym.SetBinContent(10,resultsForward["belowZPredSF"])
	histFlavSym.SetBinContent(11,resultsForwardNoBTags["belowZPredSF"])
	histFlavSym.SetBinContent(12,resultsForwardGeOneBTags["belowZPredSF"])

	histFlavSym.SetBinContent(13,resultsCentral["onZPredSF"])
	histFlavSym.SetBinContent(14,resultsCentralNoBTags["onZPredSF"])
	histFlavSym.SetBinContent(15,resultsCentralGeOneBTags["onZPredSF"])
	histFlavSym.SetBinContent(16,resultsForward["onZPredSF"])
	histFlavSym.SetBinContent(17,resultsForwardNoBTags["onZPredSF"])
	histFlavSym.SetBinContent(18,resultsForwardGeOneBTags["onZPredSF"])
	
	histFlavSym.SetBinContent(19,resultsCentral["aboveZPredSF"])
	histFlavSym.SetBinContent(20,resultsCentralNoBTags["aboveZPredSF"])
	histFlavSym.SetBinContent(21,resultsCentralGeOneBTags["aboveZPredSF"])		
	histFlavSym.SetBinContent(22,resultsForward["aboveZPredSF"])
	histFlavSym.SetBinContent(23,resultsForwardNoBTags["aboveZPredSF"])
	histFlavSym.SetBinContent(24,resultsForwardGeOneBTags["aboveZPredSF"])

	histFlavSym.SetBinContent(25,resultsCentral["highMassPredSF"])
	histFlavSym.SetBinContent(26,resultsCentralNoBTags["highMassPredSF"])
	histFlavSym.SetBinContent(27,resultsCentralGeOneBTags["highMassPredSF"])
	histFlavSym.SetBinContent(28,resultsForward["highMassPredSF"])
	histFlavSym.SetBinContent(29,resultsForwardNoBTags["highMassPredSF"])	
	histFlavSym.SetBinContent(30,resultsForwardGeOneBTags["highMassPredSF"])


	### fill histogram for background from Z+jets, estimated using gamma+jets data
	histOnlyDY.SetBinContent(1,resultsCentral["lowMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(2,resultsCentralNoBTags["lowMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(3,resultsCentralGeOneBTags["lowMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(4,resultsForward["lowMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(5,resultsForwardNoBTags["lowMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(6,resultsForwardGeOneBTags["lowMassOnlyZPredSF"])
	
	histOnlyDY.SetBinContent(7,resultsCentral["belowZOnlyZPredSF"])
	histOnlyDY.SetBinContent(8,resultsCentralNoBTags["belowZOnlyZPredSF"])
	histOnlyDY.SetBinContent(9,resultsCentralGeOneBTags["belowZOnlyZPredSF"])
	histOnlyDY.SetBinContent(10,resultsForward["belowZOnlyZPredSF"])
	histOnlyDY.SetBinContent(11,resultsForwardNoBTags["belowZOnlyZPredSF"])
	histOnlyDY.SetBinContent(12,resultsForwardGeOneBTags["belowZOnlyZPredSF"])

	histOnlyDY.SetBinContent(13,resultsCentral["onZOnlyZPredSF"])
	histOnlyDY.SetBinContent(14,resultsCentralNoBTags["onZOnlyZPredSF"])
	histOnlyDY.SetBinContent(15,resultsCentralGeOneBTags["onZOnlyZPredSF"])
	histOnlyDY.SetBinContent(16,resultsForward["onZOnlyZPredSF"])
	histOnlyDY.SetBinContent(17,resultsForwardNoBTags["onZOnlyZPredSF"])
	histOnlyDY.SetBinContent(18,resultsForwardGeOneBTags["onZOnlyZPredSF"])
	
	histOnlyDY.SetBinContent(19,resultsCentral["aboveZOnlyZPredSF"])
	histOnlyDY.SetBinContent(20,resultsCentralNoBTags["aboveZOnlyZPredSF"])
	histOnlyDY.SetBinContent(21,resultsCentralGeOneBTags["aboveZOnlyZPredSF"])		
	histOnlyDY.SetBinContent(22,resultsForward["aboveZOnlyZPredSF"])
	histOnlyDY.SetBinContent(23,resultsForwardNoBTags["aboveZOnlyZPredSF"])
	histOnlyDY.SetBinContent(24,resultsForwardGeOneBTags["aboveZOnlyZPredSF"])	

	histOnlyDY.SetBinContent(25,resultsCentral["highMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(26,resultsCentralNoBTags["highMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(27,resultsCentralGeOneBTags["highMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(28,resultsForward["highMassOnlyZPredSF"])
	histOnlyDY.SetBinContent(29,resultsForwardNoBTags["highMassOnlyZPredSF"])	
	histOnlyDY.SetBinContent(30,resultsForwardGeOneBTags["highMassOnlyZPredSF"])
	
	

	### fill histogram for non-flavor-symmetric background containing real MET from neutrinos (WZ, ZZ, ttZ ...) taken from MC
	histOther.SetBinContent(1,resultsCentral["lowMassOtherPredSF"])
	histOther.SetBinContent(2,resultsCentralNoBTags["lowMassOtherPredSF"])
	histOther.SetBinContent(3,resultsCentralGeOneBTags["lowMassOtherPredSF"])
	histOther.SetBinContent(4,resultsForward["lowMassOtherPredSF"])
	histOther.SetBinContent(5,resultsForwardNoBTags["lowMassOtherPredSF"])
	histOther.SetBinContent(6,resultsForwardGeOneBTags["lowMassOtherPredSF"])
	
	histOther.SetBinContent(7,resultsCentral["belowZOtherPredSF"])
	histOther.SetBinContent(8,resultsCentralNoBTags["belowZOtherPredSF"])
	histOther.SetBinContent(9,resultsCentralGeOneBTags["belowZOtherPredSF"])
	histOther.SetBinContent(10,resultsForward["belowZOtherPredSF"])
	histOther.SetBinContent(11,resultsForwardNoBTags["belowZOtherPredSF"])
	histOther.SetBinContent(12,resultsForwardGeOneBTags["belowZOtherPredSF"])

	histOther.SetBinContent(13,resultsCentral["onZOtherPredSF"])
	histOther.SetBinContent(14,resultsCentralNoBTags["onZOtherPredSF"])
	histOther.SetBinContent(15,resultsCentralGeOneBTags["onZOtherPredSF"])
	histOther.SetBinContent(16,resultsForward["onZOtherPredSF"])
	histOther.SetBinContent(17,resultsForwardNoBTags["onZOtherPredSF"])
	histOther.SetBinContent(18,resultsForwardGeOneBTags["onZOtherPredSF"])
	
	histOther.SetBinContent(19,resultsCentral["aboveZOtherPredSF"])
	histOther.SetBinContent(20,resultsCentralNoBTags["aboveZOtherPredSF"])
	histOther.SetBinContent(21,resultsCentralGeOneBTags["aboveZOtherPredSF"])		
	histOther.SetBinContent(22,resultsForward["aboveZOtherPredSF"])
	histOther.SetBinContent(23,resultsForwardNoBTags["aboveZOtherPredSF"])
	histOther.SetBinContent(24,resultsForwardGeOneBTags["aboveZOtherPredSF"])	

	histOther.SetBinContent(25,resultsCentral["highMassOtherPredSF"])
	histOther.SetBinContent(26,resultsCentralNoBTags["highMassOtherPredSF"])
	histOther.SetBinContent(27,resultsCentralGeOneBTags["highMassOtherPredSF"])
	histOther.SetBinContent(28,resultsForward["highMassOtherPredSF"])
	histOther.SetBinContent(29,resultsForwardNoBTags["highMassOtherPredSF"])	
	histOther.SetBinContent(30,resultsForwardGeOneBTags["highMassOtherPredSF"])

	
	
	### fill a histogram for the total background and an error graph for the uncertainty
	errGraph = ROOT.TGraphAsymmErrors()
	
	for i in range(1,histFlavSym.GetNbinsX()+1):
		errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histOnlyDY.GetBinContent(i)+histOther.GetBinContent(i))
		histTotal.SetBinContent(i,histFlavSym.GetBinContent(i)+histOnlyDY.GetBinContent(i)+histOther.GetBinContent(i))


	errGraph.SetPointError(1,0.5,0.5,resultsCentral["lowMassTotalPredErrSF"],resultsCentral["lowMassTotalPredErrSF"])
	errGraph.SetPointError(2,0.5,0.5,resultsCentralNoBTags["lowMassTotalPredErrSF"],resultsCentralNoBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(3,0.5,0.5,resultsCentralGeOneBTags["lowMassTotalPredErrSF"],resultsCentralGeOneBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(4,0.5,0.5,resultsForward["lowMassTotalPredErrSF"],resultsForward["lowMassTotalPredErrSF"])
	errGraph.SetPointError(5,0.5,0.5,resultsForwardNoBTags["lowMassTotalPredErrSF"],resultsForwardNoBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(6,0.5,0.5,resultsForwardGeOneBTags["lowMassTotalPredErrSF"],resultsForwardGeOneBTags["lowMassTotalPredErrSF"])

	errGraph.SetPointError(7,0.5,0.5,resultsCentral["onZTotalPredErrSF"],resultsCentral["onZTotalPredErrSF"])
	errGraph.SetPointError(8,0.5,0.5,resultsCentralNoBTags["onZTotalPredErrSF"],resultsCentralNoBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(9,0.5,0.5,resultsCentralGeOneBTags["onZTotalPredErrSF"],resultsCentralGeOneBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(10,0.5,0.5,resultsForward["onZTotalPredErrSF"],resultsForward["onZTotalPredErrSF"])
	errGraph.SetPointError(11,0.5,0.5,resultsForwardNoBTags["onZTotalPredErrSF"],resultsForwardNoBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(12,0.5,0.5,resultsForwardGeOneBTags["onZTotalPredErrSF"],resultsForwardGeOneBTags["onZTotalPredErrSF"])

	errGraph.SetPointError(13,0.5,0.5,resultsCentral["highMassTotalPredErrSF"],resultsCentral["highMassTotalPredErrSF"])
	errGraph.SetPointError(14,0.5,0.5,resultsCentralNoBTags["highMassTotalPredErrSF"],resultsCentralNoBTags["highMassTotalPredErrSF"])
	errGraph.SetPointError(15,0.5,0.5,resultsCentralGeOneBTags["highMassTotalPredErrSF"],resultsCentralGeOneBTags["highMassTotalPredErrSF"])
	errGraph.SetPointError(16,0.5,0.5,resultsForward["highMassTotalPredErrSF"],resultsForward["highMassTotalPredErrSF"])
	errGraph.SetPointError(17,0.5,0.5,resultsForwardNoBTags["highMassTotalPredErrSF"],resultsForwardNoBTags["highMassTotalPredErrSF"])	
	errGraph.SetPointError(18,0.5,0.5,resultsForwardGeOneBTags["highMassTotalPredErrSF"],resultsForwardGeOneBTags["highMassTotalPredErrSF"])
		
	errGraph.SetPointError(19,0.5,0.5,resultsCentral["belowZTotalPredErrSF"],resultsCentral["belowZTotalPredErrSF"])
	errGraph.SetPointError(20,0.5,0.5,resultsCentralNoBTags["belowZTotalPredErrSF"],resultsCentralNoBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(21,0.5,0.5,resultsCentralGeOneBTags["belowZTotalPredErrSF"],resultsCentralGeOneBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(22,0.5,0.5,resultsForward["belowZTotalPredErrSF"],resultsForward["belowZTotalPredErrSF"])
	errGraph.SetPointError(23,0.5,0.5,resultsForwardNoBTags["belowZTotalPredErrSF"],resultsForwardNoBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(24,0.5,0.5,resultsForwardGeOneBTags["belowZTotalPredErrSF"],resultsForwardGeOneBTags["belowZTotalPredErrSF"])
	
	errGraph.SetPointError(25,0.5,0.5,resultsCentral["aboveZTotalPredErrSF"],resultsCentral["aboveZTotalPredErrSF"])
	errGraph.SetPointError(26,0.5,0.5,resultsForward["aboveZTotalPredErrSF"],resultsForward["aboveZTotalPredErrSF"])
	errGraph.SetPointError(27,0.5,0.5,resultsCentralNoBTags["aboveZTotalPredErrSF"],resultsCentralNoBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(28,0.5,0.5,resultsForwardNoBTags["aboveZTotalPredErrSF"],resultsForwardNoBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(29,0.5,0.5,resultsCentralGeOneBTags["aboveZTotalPredErrSF"],resultsCentralGeOneBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(30,0.5,0.5,resultsForwardGeOneBTags["aboveZTotalPredErrSF"],resultsForwardGeOneBTags["aboveZTotalPredErrSF"])

	errGraph.SetFillColor(myColors["MyBlueOverview"])
	errGraph.SetFillStyle(3001)

	histFlavSym.SetLineColor(ROOT.kBlue+3)
	histFlavSym.SetFillColor(ROOT.kWhite)
	histFlavSym.SetLineWidth(3)
	
	histOnlyDY.SetLineColor(ROOT.kGreen+2)
	histOnlyDY.SetFillColor(ROOT.kGreen+2)
	
	histOther.SetLineColor(ROOT.kViolet+2)
	histOther.SetFillColor(ROOT.kViolet+2)
	
	histTotal.SetLineColor(ROOT.kBlue+3)
	histTotal.SetLineWidth(3)
	
	from ROOT import THStack
	
	### put Z background into one stack
	stack = THStack()
	stack.Add(histOther)	
	stack.Add(histOnlyDY)	

	
	### Set y-range and title
	histObs.GetYaxis().SetRangeUser(0,800)
	histObs.GetYaxis().SetTitle("Events")
	histObs.LabelsOption("v")

	histObs.UseCurrentStyle()
	histObs.SetMarkerSize(2)
	histObs.SetLineWidth(2)
	histObs.Draw("pe")
	
	
	### Set size and style for diffent labels
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.075)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
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

	
	### Somehow putting 5 contributions into one legend never looked very good
	### Thus we are using 3 legends now
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
	

	stack.Draw("samehist")
	errGraph.Draw("same02")
	histTotal.Draw("samehist")	
	
	histObs.Draw("pesame")
	
	leg1.Draw("same")
	leg2.Draw("same")
	leg3.Draw("same")

	### Draw lines to seperate the mass regions
	
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
	
	### Draw lines to seperate central and forward
	
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


	### Put additional labels into the plot
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
	
	hCanvas.Print("edgeOverview.pdf")
	
	
def main():
	
	
	name = "cutAndCount"
	countingShelves = {"inclusive":readPickle(name,regionsToUse.signal.inclusive.name , runRanges.name),"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	
	

	makeOverviewPlot(countingShelves,"SF")	
main()

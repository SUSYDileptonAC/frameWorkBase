import pickle
import os
import sys


from setTDRStyle import setTDRStyle

from corrections import rSFOF, rEEOF, rMMOF, rOutIn, rOutInEE, rOutInMM, rSFOFDirect,rSFOFTrig
from centralConfig import zPredictions, regionsToUse, runRanges

import ROOT
from ROOT import TCanvas

def saveTable(table, name):
	tabFile = open("tab/table_%s.tex"%name, "w")
	tabFile.write(table)
	tabFile.close()

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


def makeDC(anaDict):
	

    txt = """# Simple counting experiment, with one signal and one background process
imax 1  number of channels
jmax 2  number of backgrounds 
kmax *  number of nuisance parameters (sources of systematical uncertainties)
------------
# we have just one channel, in which we observe 0 events
bin         1
observation %(nObs).0f
------------
# now we list the expected events for signal and all backgrounds in that bin
# the second 'process' line must have a positive number for backgrounds, and 0 for signal
# then we list the independent sources of uncertainties, and give their effect (syst. error)
# on each process and bin
bin                 1           1           1           
process             sig         EMu         DY       
process             0           1           2           
rate                1           %(nEM).3f   %(nDY).3f 
------------
deltaS  lnN         1.          -           -            
uncEMu  lnN         -           %(uncertEM).4f        -         
EmuStat gmN %(nEMRaw).d      -       %(rSFOF).4f    -          
uncDY  lnN       -           -       %(uncertDY).2f      
""" %anaDict
    return txt
    
def getWeightedAverage(val1,err1,val2,err2):
	
	weightedAverage = (val1/(err1**2) +val2/(err2**2))/(1./err1**2+1./err2**2)
	weightedAverageErr = 1./(1./err1**2+1./err2**2)**0.5
	
	return weightedAverage, weightedAverageErr


def getDataCards(shelves,combination,selection):
	
	#~ results = {"central":getResults(shelves,"central",selection),"forward":getResults(shelves,"forward",selection)}
	results = {"central":getResultsLegacy(shelves,"legacy")}
	#~ for etaRegion in ["forward","central"]:
		#~ for region in ["lowMass","belowZ","onZ","aboveZ","highMass"]:
	for etaRegion in ["central"]:
		for region in ["edgeMass"]:
			theDict = {
				"nObs": int(results[etaRegion]["%s%s"%(region,combination)]),
				"uncertEM":  1.+results[etaRegion]["r%sOFErr"%(combination)] ,
				"nEM":  results[etaRegion]["%sPred%s"%(region,combination)] ,
				"nEMRaw":int(results[etaRegion]["%sOF"%(region)]),
				"nDY": results[etaRegion]["%sZPred%s"%(region,combination)],
				"uncertDY":1.+results[etaRegion]["%sZPredErr%s"%(region,combination)]/results[etaRegion]["%sZPred%s"%(region,combination)],
				"rSFOF": results[etaRegion]["r%sOF"%(combination)]
				
				}
			result = makeDC(theDict)
			outFile = open("dataCards/dataCard_%s_%s_%s_%s.txt"%(selection,region, etaRegion, combination), "w")
			outFile.write(result)
			outFile.close()		
			
def getResultsNLL(shelve,signalRegion):
	
	selections = ["lowNLL","highNLL"]
	massRegions = ["lowMass","highMass"]
	result = {}
	
	region = "inclusive"
	
	result["rSFOF"] = getattr(rSFOF,region).val
	result["rSFOFErr"] = getattr(rSFOF,region).err
	result["rSFOFDirect"] = getattr(rSFOFDirect,region).val
	result["rSFOFDirectErr"] = getattr(rSFOFDirect,region).err
	result["rSFOFTrig"] = getattr(rSFOFTrig,region).val
	result["rSFOFTrigErr"] = getattr(rSFOFTrig,region).err
	result["rEEOF"] = getattr(rEEOF,region).val
	result["rEEOFErr"] = getattr(rEEOF,region).err
	result["rMMOF"] = getattr(rMMOF,region).val
	result["rMMOFErr"] = getattr(rMMOF,region).err
	
	
	for selection in selections:
		result[selection] = {}
		for massRegion in massRegions:
		
		
			
			result[selection]["%sEE"%massRegion] = shelve[signalRegion][selection][massRegion]["EE"]
			result[selection]["%sMM"%massRegion] = shelve[signalRegion][selection][massRegion]["MM"]
			result[selection]["%sSF"%massRegion] = shelve[signalRegion][selection][massRegion]["EE"] + shelve[signalRegion][selection][massRegion]["MM"]
			result[selection]["%sOF"%massRegion] = shelve[signalRegion][selection][massRegion]["EM"]
			result[selection]["%sOFRMuEScaled"%massRegion] = shelve[signalRegion][selection][massRegion]["EMRMuEScaled"]
			result[selection]["%sOFRMuEScaledUp"%massRegion] = shelve[signalRegion][selection][massRegion]["EMRMuEScaledUp"]
			result[selection]["%sOFRMuEScaledDown"%massRegion] = shelve[signalRegion][selection][massRegion]["EMRMuEScaledDown"]
			
			
			result[selection]["%sPredDirectSF"%massRegion] = result[selection]["%sOF"%massRegion]*getattr(rSFOFDirect,region).val
			result[selection]["%sPredDirectStatErrSF"%massRegion] = result[selection]["%sOF"%massRegion]**0.5*getattr(rSFOFDirect,region).val
			result[selection]["%sPredDirectSystErrSF"%massRegion] = result[selection]["%sOF"%massRegion]*getattr(rSFOFDirect,region).err
			
			result[selection]["%sPredFactSF"%massRegion] = result[selection]["%sOFRMuEScaled"%massRegion]*getattr(rSFOFTrig,region).val
			result[selection]["%sPredFactStatErrSF"%massRegion] = result[selection]["%sOF"%massRegion]**0.5*result[selection]["%sOFRMuEScaled"%massRegion]/result[selection]["%sOF"%massRegion]*getattr(rSFOFTrig,region).val
			result[selection]["%sPredFactSystErrSF"%massRegion] = result[selection]["%sOFRMuEScaled"%massRegion]*(getattr(rSFOFTrig,region).err**2 + max(abs(result[selection]["%sOFRMuEScaled"%massRegion] - result[selection]["%sOFRMuEScaledUp"%massRegion])/result[selection]["%sOFRMuEScaled"%massRegion],abs(result[selection]["%sOFRMuEScaled"%massRegion] - result[selection]["%sOFRMuEScaledDown"%massRegion])/result[selection]["%sOFRMuEScaled"%massRegion])**2)**0.5		
			
			result[selection]["%sPredSF"%massRegion],result[selection]["%sPredSystErrSF"%massRegion] = getWeightedAverage(result[selection]["%sPredDirectSF"%massRegion],result[selection]["%sPredDirectSystErrSF"%massRegion],result[selection]["%sPredFactSF"%massRegion],result[selection]["%sPredFactSystErrSF"%massRegion])
			result[selection]["%sPredStatErrSF"%massRegion] = result[selection]["%sOF"%massRegion]**0.5*result[selection]["%sPredSF"%massRegion]/result[selection]["%sOF"%massRegion]
			
			
			result[selection]["%sPredSFOld"%massRegion] = result[selection]["%sOF"%massRegion]*getattr(rSFOF,region).val
			result[selection]["%sPredStatErrSFOld"%massRegion] = result[selection]["%sOF"%massRegion]**0.5*getattr(rSFOF,region).val
			result[selection]["%sPredSystErrSFOld"%massRegion] = result[selection]["%sOF"%massRegion]*getattr(rSFOF,region).err
			
			result[selection]["%sPredEEOld"%massRegion] = result[selection]["%sOF"%massRegion]*getattr(rEEOF,region).val
			result[selection]["%sPredStatErrEEOld"%massRegion] = result[selection]["%sOF"%massRegion]**0.5*getattr(rEEOF,region).val
			result[selection]["%sPredSystErrEEOld"%massRegion] = result[selection]["%sOF"%massRegion]*getattr(rEEOF,region).err
			
			result[selection]["%sPredMMOld"%massRegion] = result[selection]["%sOF"%massRegion]*getattr(rMMOF,region).val
			result[selection]["%sPredStatErrMMOld"%massRegion] = result[selection]["%sOF"%massRegion]**0.5*getattr(rMMOF,region).val
			result[selection]["%sPredSystErrMMOld"%massRegion] = result[selection]["%sOF"%massRegion]*getattr(rMMOF,region).err
			
			result[selection]["%sZPredSF"%massRegion] = getattr(zPredictions.NLL.SF,selection).val*getattr(getattr(rOutIn,massRegion),region).val
			result[selection]["%sZPredErrSF"%massRegion] = ((getattr(zPredictions.NLL.SF,selection).val*getattr(getattr(rOutIn,massRegion),region).err)**2 + (getattr(zPredictions.NLL.SF,selection).err*getattr(getattr(rOutIn,massRegion),region).val)**2 )**0.5
			
			result[selection]["%sTotalPredSF"%massRegion] = result[selection]["%sPredSF"%massRegion] + result[selection]["%sZPredSF"%massRegion]
			result[selection]["%sTotalPredErrSF"%massRegion] = ( result[selection]["%sPredStatErrSF"%massRegion]**2 +  result[selection]["%sPredSystErrSF"%massRegion]**2 + result[selection]["%sZPredErrSF"%massRegion]**2 )**0.5
			
			result[selection]["%sTotalPredSFOld"%massRegion] = result[selection]["%sPredSFOld"%massRegion] + result[selection]["%sZPredSF"%massRegion]
			result[selection]["%sTotalPredErrSFOld"%massRegion] = ( result[selection]["%sPredStatErrSFOld"%massRegion]**2 +  result[selection]["%sPredSystErrSFOld"%massRegion]**2 + result[selection]["%sZPredErrSF"%massRegion]**2 )**0.5
		
			
	
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
	
		
	result["edgeMassEE"] = shelve[signalRegion]["default"]["edgeMass"]["EE"]
	result["edgeMassMM"] = shelve[signalRegion]["default"]["edgeMass"]["MM"]
	result["edgeMassSF"] = shelve[signalRegion]["default"]["edgeMass"]["EE"] + shelve[signalRegion]["default"]["edgeMass"]["MM"]
	result["edgeMassOF"] = shelve[signalRegion]["default"]["edgeMass"]["EM"]
	
	result["edgeMassOFRMuEScaled"] = shelve[signalRegion]["default"]["edgeMass"]["EMRMuEScaled"]
	result["edgeMassOFRMuEScaledUp"] = shelve[signalRegion]["default"]["edgeMass"]["EMRMuEScaledUp"]
	result["edgeMassOFRMuEScaledDown"] = shelve[signalRegion]["default"]["edgeMass"]["EMRMuEScaledDown"]
	
	
	
	result["edgeMassPredDirectSF"] = result["edgeMassOF"]*getattr(rSFOFDirect,region).val
	result["edgeMassPredDirectStatErrSF"] = result["edgeMassOF"]**0.5*getattr(rSFOFDirect,region).val
	result["edgeMassPredDirectSystErrSF"] = result["edgeMassOF"]*getattr(rSFOFDirect,region).err
	
	result["edgeMassPredFactSF"] = result["edgeMassOFRMuEScaled"]*getattr(rSFOFTrig,region).val
	result["edgeMassPredFactStatErrSF"] = result["edgeMassOF"]**0.5*result["edgeMassOFRMuEScaled"]/result["edgeMassOF"]*getattr(rSFOFTrig,region).val
	result["edgeMassPredFactSystErrSF"] = result["edgeMassOFRMuEScaled"]*(getattr(rSFOFTrig,region).err**2 + max(abs(result["edgeMassOFRMuEScaled"] - result["edgeMassOFRMuEScaledUp"])/result["edgeMassOFRMuEScaled"],abs(result["edgeMassOFRMuEScaled"] - result["edgeMassOFRMuEScaledUp"])/result["edgeMassOFRMuEScaled"])**2)**0.5		
	
	result["edgeMassPredSF"],result["edgeMassPredSystErrSF"] = getWeightedAverage(result["edgeMassPredDirectSF"],result["edgeMassPredDirectSystErrSF"],result["edgeMassPredFactSF"],result["edgeMassPredFactSystErrSF"])
	result["edgeMassPredStatErrSF"] = result["edgeMassOF"]**0.5*result["edgeMassPredSF"]/result["edgeMassOF"]
			
			
	result["edgeMassPredSFOld"] = result["edgeMassOF"]*getattr(rSFOF,region).val
	result["edgeMassPredStatErrSFOld"] = result["edgeMassOF"]**0.5*getattr(rSFOF,region).val
	result["edgeMassPredSystErrSFOld"] = result["edgeMassOF"]*getattr(rSFOF,region).err
	
	result["edgeMassPredEEOld"] = result["edgeMassOF"]*getattr(rEEOF,region).val
	result["edgeMassPredStatErrEEOld"] = result["edgeMassOF"]**0.5*getattr(rEEOF,region).val
	result["edgeMassPredSystErrEEOld"] = result["edgeMassOF"]*getattr(rEEOF,region).err
	
	result["edgeMassPredMMOld"] = result["edgeMassOF"]*getattr(rMMOF,region).val
	result["edgeMassPredStatErrMMOld"] = result["edgeMassOF"]**0.5*getattr(rMMOF,region).val
	result["edgeMassPredSystErrMMOld"] = result["edgeMassOF"]*getattr(rMMOF,region).err
	
	result["edgeMassZPredSF"] = getattr(zPredictions.legacy.SF,region).val*getattr(rOutIn.edgeMass,region).val
	result["edgeMassZPredErrSF"] = ((getattr(zPredictions.legacy.SF,region).val*getattr(rOutIn.edgeMass,region).err)**2 + (getattr(zPredictions.legacy.SF,region).err*getattr(rOutIn.edgeMass,region).val)**2 )**0.5
	
	result["edgeMassTotalPredSF"] = result["edgeMassPredSF"] + result["edgeMassZPredSF"]
	result["edgeMassTotalPredErrSF"] = ( result["edgeMassPredStatErrSF"]**2 +  result["edgeMassPredSystErrSF"]**2 + result["edgeMassZPredErrSF"]**2 )**0.5
	
	result["edgeMassTotalPredSFOld"] = result["edgeMassPredSFOld"] + result["edgeMassZPredSF"]
	result["edgeMassTotalPredErrSFOld"] = ( result["edgeMassPredStatErrSFOld"]**2 +  result["edgeMassPredSystErrSFOld"]**2 + result["edgeMassZPredErrSF"]**2 )**0.5

	
	return result


def produceFinalTable(shelves):
	
	
	
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Results of the edge-search counting experiment for event yields in the signal regions.
     The statistical and systematic uncertainties are added in quadrature, except for the flavor-symmetric backgrounds.
     Low-mass refers to 20 $<$ \mll $<$ 81\GeV, high-mass to \mll $>$ 101\GeV, ttbar like to \NLL < 21, non-ttbar like to \NLL $geq$ 21.
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

	#~ flavSysmTemplate = r"        Flavor-symmetric    & $%d\pm%d\pm%d$        & $%d\pm%d\pm%d$  &  $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ \\"+"\n"
	flavSysmTemplate = r"        Flavor-symmetric    & $%.1f\pm%.1f\pm%.1f$        & $%.1f\pm%.1f\pm%.1f$   &  $%.1f\pm%.1f\pm%.1f$  & $%.1f\pm%.1f\pm%.1f$  & $%.1f\pm%.1f\pm%.1f$  \\"+"\n"
	#~ flavSysmTemplate = r"        Flavor-symmetric    & $%.1f\pm%.3f\pm%.3f$        & $%.1f\pm%.3f\pm%.3f$  &  $%.1f\pm%.3f\pm%.3f$ & $%.1f\pm%.3f\pm%.3f$ & $%.1f\pm%.3f\pm%.3f$ \\"+"\n"

	dyTemplate = r"            Drell--Yan          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$  \\"+"\n"
	
	totalTemplate = r"            Total estimated          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ \\"+"\n"
	
	resultsNLL = getResultsNLL(shelves,"NLL")
	resultsLegacy = getResultsLegacy(shelves,"legacy")
		

	observed = observedTemplate%(resultsNLL["lowNLL"]["lowMassSF"],resultsNLL["highNLL"]["lowMassSF"],resultsNLL["lowNLL"]["highMassSF"],resultsNLL["highNLL"]["highMassSF"],resultsLegacy["edgeMassSF"])
		
	#~ flavSym = flavSysmTemplate%(resultsNLL["lowNLL"]["lowMassPredSF"],resultsNLL["lowNLL"]["lowMassPredStatErrSF"],resultsNLL["lowNLL"]["lowMassPredSystErrSF"],resultsNLL["highNLL"]["lowMassPredSF"],resultsNLL["highNLL"]["lowMassPredStatErrSF"],resultsNLL["highNLL"]["lowMassPredSystErrSF"],resultsNLL["lowNLL"]["highMassPredSF"],resultsNLL["lowNLL"]["highMassPredStatErrSF"],resultsNLL["lowNLL"]["highMassPredSystErrSF"],resultsNLL["highNLL"]["highMassPredSF"],resultsNLL["highNLL"]["highMassPredStatErrSF"],resultsNLL["highNLL"]["highMassPredSystErrSF"],resultsLegacy["edgeMassPredSF"],resultsLegacy["edgeMassPredStatErrSF"],resultsLegacy["edgeMassPredSystErrSF"])
	flavSym = flavSysmTemplate%(resultsNLL["lowNLL"]["lowMassPredSF"],resultsNLL["lowNLL"]["lowMassPredStatErrSF"],resultsNLL["lowNLL"]["lowMassPredSystErrSF"],resultsNLL["highNLL"]["lowMassPredSF"],resultsNLL["highNLL"]["lowMassPredStatErrSF"],resultsNLL["highNLL"]["lowMassPredSystErrSF"],resultsNLL["lowNLL"]["highMassPredSF"],resultsNLL["lowNLL"]["highMassPredStatErrSF"],resultsNLL["lowNLL"]["highMassPredSystErrSF"],resultsNLL["highNLL"]["highMassPredSF"],resultsNLL["highNLL"]["highMassPredStatErrSF"],resultsNLL["highNLL"]["highMassPredSystErrSF"],resultsLegacy["edgeMassPredSF"],resultsLegacy["edgeMassPredStatErrSF"],resultsLegacy["edgeMassPredSystErrSF"])
	
	dy = dyTemplate%(resultsNLL["lowNLL"]["lowMassZPredSF"],resultsNLL["lowNLL"]["lowMassZPredErrSF"],resultsNLL["highNLL"]["lowMassZPredSF"],resultsNLL["highNLL"]["lowMassZPredErrSF"],resultsNLL["lowNLL"]["highMassZPredSF"],resultsNLL["lowNLL"]["highMassZPredErrSF"],resultsNLL["highNLL"]["highMassZPredSF"],resultsNLL["highNLL"]["highMassZPredErrSF"],resultsLegacy["edgeMassZPredSF"],resultsLegacy["edgeMassZPredErrSF"])
		
	totalPrediction = totalTemplate%(resultsNLL["lowNLL"]["lowMassTotalPredSF"],resultsNLL["lowNLL"]["lowMassTotalPredErrSF"],resultsNLL["highNLL"]["lowMassTotalPredSF"],resultsNLL["highNLL"]["lowMassTotalPredErrSF"],resultsNLL["lowNLL"]["highMassTotalPredSF"],resultsNLL["lowNLL"]["highMassTotalPredErrSF"],resultsNLL["highNLL"]["highMassTotalPredSF"],resultsNLL["highNLL"]["highMassTotalPredErrSF"],resultsLegacy["edgeMassTotalPredSF"],resultsLegacy["edgeMassTotalPredErrSF"])


		
	table = tableTemplate%(observed,flavSym,dy,totalPrediction)
	saveTable(table,"cutNCount_Result_SF")
	
	
	


def produceFlavSymTable(shelves):
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Resulting estimates for flavour-symmetric backgrounds. Given is the observed event yield in \EM events and the resulting estimate after applying the correction, 
	 seperately for the SF, \EE, and \MM channels. Statistical and systematic uncertainties are given separately.
     Low-mass refers to 20 $<$ \mll $<$ 81\GeV, high-mass to \mll $>$ 101\GeV, ttbar like to \NLL $<$ 21, non-ttbar like to \NLL $\geq$ 21.
     }
  \label{tab:FlavSymBackgrounds}
  \\begin{tabular}{l| c | c | c | c | c}
    \hline
    \hline
     & \multicolumn{4}{c|}{Baseline signal region} &  \\\\ \n
    \hline
    & Low-mass & Low-mass & High-mass & High-mass & 8 TeV Legacy\\\\ \n
    & ttbar like & non-ttbar like  & ttbar like & non ttbar like  & region\\\\ \n
    \hline
%s
    \hline
%s
%s
%s
%s
\hline

  \end{tabular}
\end{table}


"""


	observedTemplate = r"        Observed OF events       &  %d                   & %d              &  %d            &  %d       &   %d     \\" +"\n"

	flavSysmTemplate = r"        Estimate %s method    & $%d\pm%d\pm%d$        & $%d\pm%d\pm%d$  &  $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ \\"+"\n"

		
	resultsNLL = getResultsNLL(shelves,"NLL")
	resultsLegacy = getResultsLegacy(shelves,"legacy")
		
	observed = observedTemplate%(resultsNLL["lowNLL"]["lowMassOF"],resultsNLL["highNLL"]["lowMassOF"],resultsNLL["lowNLL"]["highMassOF"],resultsNLL["highNLL"]["highMassOF"],resultsLegacy["edgeMassOF"])

		
	SFPredicitonOld = flavSysmTemplate%("SF, old",resultsNLL["lowNLL"]["lowMassPredSFOld"],resultsNLL["lowNLL"]["lowMassPredStatErrSFOld"],resultsNLL["lowNLL"]["lowMassPredSystErrSFOld"],resultsNLL["highNLL"]["lowMassPredSFOld"],resultsNLL["highNLL"]["lowMassPredStatErrSFOld"],resultsNLL["highNLL"]["lowMassPredSystErrSFOld"],resultsNLL["lowNLL"]["highMassPredSFOld"],resultsNLL["lowNLL"]["highMassPredStatErrSFOld"],resultsNLL["lowNLL"]["highMassPredSystErrSFOld"],resultsNLL["highNLL"]["highMassPredSFOld"],resultsNLL["highNLL"]["highMassPredStatErrSFOld"],resultsNLL["highNLL"]["highMassPredSystErrSFOld"],resultsLegacy["edgeMassPredSFOld"],resultsLegacy["edgeMassPredStatErrSFOld"],resultsLegacy["edgeMassPredSystErrSFOld"])
	SFPredicitonDirect = flavSysmTemplate%("SF, direct",resultsNLL["lowNLL"]["lowMassPredDirectSF"],resultsNLL["lowNLL"]["lowMassPredDirectStatErrSF"],resultsNLL["lowNLL"]["lowMassPredDirectSystErrSF"],resultsNLL["highNLL"]["lowMassPredDirectSF"],resultsNLL["highNLL"]["lowMassPredDirectStatErrSF"],resultsNLL["highNLL"]["lowMassPredDirectSystErrSF"],resultsNLL["lowNLL"]["highMassPredDirectSF"],resultsNLL["lowNLL"]["highMassPredDirectStatErrSF"],resultsNLL["lowNLL"]["highMassPredDirectSystErrSF"],resultsNLL["highNLL"]["highMassPredDirectSF"],resultsNLL["highNLL"]["highMassPredDirectStatErrSF"],resultsNLL["highNLL"]["highMassPredDirectSystErrSF"],resultsLegacy["edgeMassPredDirectSF"],resultsLegacy["edgeMassPredDirectStatErrSF"],resultsLegacy["edgeMassPredDirectSystErrSF"])
	SFPredicitonFact = flavSysmTemplate%("SF, Fact",resultsNLL["lowNLL"]["lowMassPredFactSF"],resultsNLL["lowNLL"]["lowMassPredFactStatErrSF"],resultsNLL["lowNLL"]["lowMassPredFactSystErrSF"],resultsNLL["highNLL"]["lowMassPredFactSF"],resultsNLL["highNLL"]["lowMassPredFactStatErrSF"],resultsNLL["highNLL"]["lowMassPredFactSystErrSF"],resultsNLL["lowNLL"]["highMassPredFactSF"],resultsNLL["lowNLL"]["highMassPredFactStatErrSF"],resultsNLL["lowNLL"]["highMassPredFactSystErrSF"],resultsNLL["highNLL"]["highMassPredFactSF"],resultsNLL["highNLL"]["highMassPredFactStatErrSF"],resultsNLL["highNLL"]["highMassPredFactSystErrSF"],resultsLegacy["edgeMassPredFactSF"],resultsLegacy["edgeMassPredFactStatErrSF"],resultsLegacy["edgeMassPredFactSystErrSF"])
	#~ EEPrediciton = flavSysmTemplate%("EE",resultsNLL["lowNLL"]["lowMassPredEE"],resultsNLL["lowNLL"]["lowMassPredStatErrEE"],resultsNLL["lowNLL"]["lowMassPredSystErrEE"],resultsNLL["highNLL"]["lowMassPredEE"],resultsNLL["highNLL"]["lowMassPredStatErrEE"],resultsNLL["highNLL"]["lowMassPredSystErrEE"],resultsNLL["lowNLL"]["highMassPredEE"],resultsNLL["lowNLL"]["highMassPredStatErrEE"],resultsNLL["lowNLL"]["highMassPredSystErrEE"],resultsNLL["highNLL"]["highMassPredEE"],resultsNLL["highNLL"]["highMassPredStatErrEE"],resultsNLL["highNLL"]["highMassPredSystErrEE"],resultsLegacy["edgeMassPredEE"],resultsLegacy["edgeMassPredStatErrEE"],resultsLegacy["edgeMassPredSystErrEE"])
	#~ MMPrediciton= flavSysmTemplate%("MM",resultsNLL["lowNLL"]["lowMassPredMM"],resultsNLL["lowNLL"]["lowMassPredStatErrMM"],resultsNLL["lowNLL"]["lowMassPredSystErrMM"],resultsNLL["highNLL"]["lowMassPredMM"],resultsNLL["highNLL"]["lowMassPredStatErrMM"],resultsNLL["highNLL"]["lowMassPredSystErrMM"],resultsNLL["lowNLL"]["highMassPredMM"],resultsNLL["lowNLL"]["highMassPredStatErrMM"],resultsNLL["lowNLL"]["highMassPredSystErrMM"],resultsNLL["highNLL"]["highMassPredMM"],resultsNLL["highNLL"]["highMassPredStatErrMM"],resultsNLL["highNLL"]["highMassPredSystErrMM"],resultsLegacy["edgeMassPredMM"],resultsLegacy["edgeMassPredStatErrMM"],resultsLegacy["edgeMassPredSystErrMM"])
	SFPrediciton = flavSysmTemplate%("SF, new",resultsNLL["lowNLL"]["lowMassPredSF"],resultsNLL["lowNLL"]["lowMassPredStatErrSF"],resultsNLL["lowNLL"]["lowMassPredSystErrSF"],resultsNLL["highNLL"]["lowMassPredSF"],resultsNLL["highNLL"]["lowMassPredStatErrSF"],resultsNLL["highNLL"]["lowMassPredSystErrSF"],resultsNLL["lowNLL"]["highMassPredSF"],resultsNLL["lowNLL"]["highMassPredStatErrSF"],resultsNLL["lowNLL"]["highMassPredSystErrSF"],resultsNLL["highNLL"]["highMassPredSF"],resultsNLL["highNLL"]["highMassPredStatErrSF"],resultsNLL["highNLL"]["highMassPredSystErrSF"],resultsLegacy["edgeMassPredSF"],resultsLegacy["edgeMassPredStatErrSF"],resultsLegacy["edgeMassPredSystErrSF"])
		
		
	saveTable(tableTemplate%(observed,SFPredicitonOld,SFPredicitonDirect,SFPredicitonFact,SFPrediciton),"cutNCount_FlavSymBkgs")	
	
	
def produceZTable(shelves,selection):

	shelvesROutIn = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRanges.name),"central": readPickle("rOutIn",regionsToUse.rOutIn.central.name,runRanges.name), "forward":readPickle("rOutIn",regionsToUse.rOutIn.forward.name,runRanges.name)}

	
	tableTemplate = r"""
\begin{table}[!htbp]
 \renewcommand{\arraystretch}{1.2}
 \begin{center}
  \caption{Estimate of the \Z background yields in the \Z peak region and extrapolation to the signal mass region for the full dataset.}
  \begin{tabular}{l|cc|c|}
   \hline
   \hline
                                    & \multicolumn{3}{c|}{\central}            \\
                                    & \EE                   & \MM                   & SF          \\
   \hline
   \Z bkgd estimate (\JZB)                  & $57.9\pm13.8\pm10.1$   & $46.1\pm13.8\pm8.0$          &    $104\pm21\pm18$  \\
   
   \Z bkgd estimate (\MET templates) & $63.2\pm 4.3\pm 15.3$    & $69.5\pm 4.0\pm 16.9$       &    $133\pm7\pm32$  \\
   \Z bkgd estimate (Combined)         & $60.7\pm 11.6$                & $56.8\pm 11.7$                   &    $116\pm21$  \\
   \hline
%s 
   \hline
%s
   \hline
%s 
   \hline
%s  
   \hline
                                    & \multicolumn{3}{c|}{\forward} \\
                                    & \EE                  & \MM                        & SF \\
   \hline
   \Z bkgd estimate (\JZB)                   & $15.6\pm 8.3\pm 2.9$ & $13.8 \pm 8.3\pm 2.8$       & $29\pm11\pm6$ \\
   \Z bkgd estimate (MET templates)          & $24.4\pm 1.8\pm 6.0$ & $32.3\pm 2.2\pm 7.9$       & $56.9\pm3.6\pm14.0$ \\
   \Z bkgd estimate (Combined)          & $21\pm 5$        & $25\pm 6$             & $42\pm 9$  \\

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
 \label{tab:dyResults}
 \end{center}
\end{table}
"""
	


	rOutInTemplate = r"       \Routin %s-Mass       &  %.3f$\pm$%.3f$\pm$%.3f                   & %.3f$\pm$%.3f$\pm$%.3f            &  %.3f$\pm$%.3f$\pm$%.3f    \\" +"\n"

	predictionTemplate = r"     %s-Mass estimate    & %.1f$\pm$%.1f        & %.1f$\pm$%.1f  &  %.1f$\pm$%.1f \\"+"\n"



	
	
	resultsCentral = getResults(shelves,"central",selection)
	resultsForward = getResults(shelves,"forward",selection)

	rOutInLowMassCentral = rOutInTemplate%("low",shelvesROutIn["central"]["rOutInLowMassEE"],shelvesROutIn["central"]["rOutInLowMassErrEE"],shelvesROutIn["central"]["rOutInLowMassSystEE"],shelvesROutIn["central"]["rOutInLowMassMM"],shelvesROutIn["central"]["rOutInLowMassErrMM"],shelvesROutIn["central"]["rOutInLowMassSystMM"],shelvesROutIn["central"]["rOutInLowMassSF"],shelvesROutIn["central"]["rOutInLowMassErrSF"],shelvesROutIn["central"]["rOutInLowMassSystSF"])
	rOutInLowMassForward = rOutInTemplate%("low",shelvesROutIn["forward"]["rOutInLowMassEE"],shelvesROutIn["forward"]["rOutInLowMassErrEE"],shelvesROutIn["forward"]["rOutInLowMassSystEE"],shelvesROutIn["forward"]["rOutInLowMassMM"],shelvesROutIn["forward"]["rOutInLowMassErrMM"],shelvesROutIn["forward"]["rOutInLowMassSystMM"],shelvesROutIn["forward"]["rOutInLowMassSF"],shelvesROutIn["forward"]["rOutInLowMassErrSF"],shelvesROutIn["forward"]["rOutInLowMassSystSF"])

	rOutInHighMassCentral = rOutInTemplate%("high",shelvesROutIn["central"]["rOutInHighMassEE"],shelvesROutIn["central"]["rOutInHighMassErrEE"],shelvesROutIn["central"]["rOutInHighMassSystEE"],shelvesROutIn["central"]["rOutInHighMassMM"],shelvesROutIn["central"]["rOutInHighMassErrMM"],shelvesROutIn["central"]["rOutInHighMassSystMM"],shelvesROutIn["central"]["rOutInHighMassSF"],shelvesROutIn["central"]["rOutInHighMassErrSF"],shelvesROutIn["central"]["rOutInHighMassSystSF"])
	rOutInHighMassForward = rOutInTemplate%("high",shelvesROutIn["forward"]["rOutInHighMassEE"],shelvesROutIn["forward"]["rOutInHighMassErrEE"],shelvesROutIn["forward"]["rOutInHighMassSystEE"],shelvesROutIn["forward"]["rOutInHighMassMM"],shelvesROutIn["forward"]["rOutInHighMassErrMM"],shelvesROutIn["forward"]["rOutInHighMassSystMM"],shelvesROutIn["forward"]["rOutInHighMassSF"],shelvesROutIn["forward"]["rOutInHighMassErrSF"],shelvesROutIn["forward"]["rOutInHighMassSystSF"])

	predictionLowMassCentral = predictionTemplate%("low",resultsCentral["lowMassZPredEE"],resultsCentral["lowMassZPredErrEE"],resultsCentral["lowMassZPredMM"],resultsCentral["lowMassZPredErrMM"],resultsCentral["lowMassZPredSF"],resultsCentral["lowMassZPredErrSF"])
	predictionLowMassForward = predictionTemplate%("low",resultsForward["lowMassZPredEE"],resultsForward["lowMassZPredErrEE"],resultsForward["lowMassZPredMM"],resultsForward["lowMassZPredErrMM"],resultsForward["lowMassZPredSF"],resultsForward["lowMassZPredErrSF"])

	predictionHighMassCentral = predictionTemplate%("high",resultsCentral["highMassZPredEE"],resultsCentral["highMassZPredErrEE"],resultsCentral["highMassZPredMM"],resultsCentral["highMassZPredErrMM"],resultsCentral["highMassZPredSF"],resultsCentral["highMassZPredErrSF"])
	predictionHighMassForward = predictionTemplate%("high",resultsForward["highMassZPredEE"],resultsForward["highMassZPredErrEE"],resultsForward["highMassZPredMM"],resultsForward["highMassZPredErrMM"],resultsForward["highMassZPredSF"],resultsForward["highMassZPredErrSF"])
	

	
	table = tableTemplate%(rOutInLowMassCentral,predictionLowMassCentral,rOutInHighMassCentral,predictionHighMassCentral,rOutInLowMassForward,predictionLowMassForward,rOutInHighMassForward,predictionHighMassForward)
	
	saveTable(table,"cutNCount_ZBkgs_%s"%selection)		
	
def main():
	
	
	name = "cutAndCount"
	countingShelves= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , runRanges.name),"legacy": readPickle("cutAndCount",regionsToUse.signal.central.name,runRanges.name)}	
	

	
	produceFinalTable(countingShelves)
	#~ produceFinalTable(countingShelves,"EE")
	#~ produceFinalTable(countingShelves,"MM")
	
	#~ for selection in ["default","geOneBTags","noBTags"]:
	for selection in ["default"]:
		getDataCards(countingShelves,"SF",selection)
		#~ getDataCards(countingShelves,"EE",selection)
		#~ getDataCards(countingShelves,"MM",selection)
	produceFlavSymTable(countingShelves)
		#~ produceZTable(countingShelves,selection)
main()

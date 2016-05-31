import pickle
import os
import sys


from setTDRStyle import setTDRStyle

from corrections import rSFOF, rEEOF, rMMOF, rOutIn, rOutInEE, rOutInMM
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
			print "shelves/%s_%s_%s.pkl not found, exiting"%(name,regionName,runName) 		
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

	
def getResults(shelve,region,selection):
	
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


def produceFinalTable(shelves,region):
	
	
	
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Results of the edge-search counting experiment for event yields in the signal regions.
     The statistical and systematic uncertainties are added in quadrature, except for the flavor-symmetric backgrounds.
     Low-mass refers to 20 $<$ \mll $<$ 70\GeV, below-\Z to 71 $<$ \mll $<$ 81\GeV, on-\Z to  81 $<$ \mll $<$ 101\GeV, above-\Z to 81 $<$ \mll $<$ 120\GeV and high-mass to \mll $>$ 120\GeV.
     }
  \label{tab:edgeResults}
  \\begin{tabular}{l| c | c | c | c | c}
    \hline
    \hline
%s

\hline
\hline 

%s

   \hline
    \hline
 %s
   \hline
    \hline        
  \end{tabular}
\end{table}


"""

	subTemplate = """
    & \multicolumn{5}{c}{%s} \\\\ \n
    \hline    
    							& Low-mass & below-\Z & On-\Z & above-\Z & High-mass \\\\ \n
    \hline
                                &  \multicolumn{5}{c}{Central} \\\\ \n
    \hline
%s
%s
    \hline
%s

    \hline
%s
\hline
                                &  \multicolumn{5}{c}{Forward} \\\\ \n
    \hline
%s
%s
    \hline

%s
    \hline
%s
	
	
"""	

	observedTemplate = r"        Observed       &  %d                   & %d              &  %d            &  %d       &   %d        \\" +"\n"

	flavSysmTemplate = r"        Flavor-symmetric    & $%d\pm%d\pm%d$        & $%d\pm%d\pm%d$  &  $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ \\"+"\n"
	#~ flavSysmTemplate = r"        Flavor-symmetric    & $%.1f\pm%.3f\pm%.3f$        & $%.1f\pm%.3f\pm%.3f$  &  $%.1f\pm%.3f\pm%.3f$ & $%.1f\pm%.3f\pm%.3f$ & $%.1f\pm%.3f\pm%.3f$ \\"+"\n"

	dyTemplate = r"            Drell--Yan          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$  \\"+"\n"
	
	totalTemplate = r"            Total estimated          & $%d\pm%d$            & $%d\pm%d$      & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ \\"+"\n"


	tables = []
	for selection in ["default","noBTags","geOneBTags"]:
		
		resultsCentral = getResults(shelves,"central",selection)
		resultsForward = getResults(shelves,"forward",selection)

		observedCentral = observedTemplate%(resultsCentral["lowMass%s"%region],resultsCentral["belowZ%s"%region],resultsCentral["onZ%s"%region],resultsCentral["aboveZ%s"%region],resultsCentral["highMass%s"%region])
		
		flavSymCentral = flavSysmTemplate%(resultsCentral["lowMassPred%s"%region],resultsCentral["lowMassPredStatErr%s"%region],resultsCentral["lowMassPredSystErr%s"%region],resultsCentral["belowZPred%s"%region],resultsCentral["belowZPredStatErr%s"%region],resultsCentral["belowZPredSystErr%s"%region],resultsCentral["onZPred%s"%region],resultsCentral["onZPredStatErr%s"%region],resultsCentral["onZPredSystErr%s"%region],resultsCentral["aboveZPred%s"%region],resultsCentral["aboveZPredStatErr%s"%region],resultsCentral["aboveZPredSystErr%s"%region],resultsCentral["highMassPred%s"%region],resultsCentral["highMassPredStatErr%s"%region],resultsCentral["highMassPredSystErr%s"%region])
		#~ flavSymCentral = flavSysmTemplate%(resultsCentral["lowMassPred%s"%region],resultsCentral["lowMassPredStatErr%s"%region]/resultsCentral["lowMassPred%s"%region],resultsCentral["lowMassPredSystErr%s"%region]/resultsCentral["lowMassPred%s"%region],resultsCentral["belowZPred%s"%region],resultsCentral["belowZPredStatErr%s"%region]/resultsCentral["belowZPred%s"%region],resultsCentral["belowZPredSystErr%s"%region]/resultsCentral["belowZPred%s"%region],resultsCentral["onZPred%s"%region],resultsCentral["onZPredStatErr%s"%region]/resultsCentral["onZPred%s"%region],resultsCentral["onZPredSystErr%s"%region]/resultsCentral["onZPred%s"%region],resultsCentral["aboveZPred%s"%region],resultsCentral["aboveZPredStatErr%s"%region]/resultsCentral["aboveZPred%s"%region],resultsCentral["aboveZPredSystErr%s"%region]/resultsCentral["aboveZPred%s"%region],resultsCentral["highMassPred%s"%region],resultsCentral["highMassPredStatErr%s"%region]/resultsCentral["highMassPred%s"%region],resultsCentral["highMassPredSystErr%s"%region]/resultsCentral["highMassPred%s"%region])
		
		dyCentral = dyTemplate%(resultsCentral["lowMassZPred%s"%region],resultsCentral["lowMassZPredErr%s"%region],resultsCentral["belowZZPred%s"%region],resultsCentral["belowZZPredErr%s"%region],resultsCentral["onZZPred%s"%region],resultsCentral["onZZPredErr%s"%region],resultsCentral["aboveZZPred%s"%region],resultsCentral["aboveZZPredErr%s"%region],resultsCentral["highMassZPred%s"%region],resultsCentral["highMassZPredErr%s"%region])
		
		totalCentral = totalTemplate%(resultsCentral["lowMassTotalPred%s"%region],resultsCentral["lowMassTotalPredErr%s"%region],resultsCentral["belowZTotalPred%s"%region],resultsCentral["belowZTotalPredErr%s"%region],resultsCentral["onZTotalPred%s"%region],resultsCentral["onZTotalPredErr%s"%region],resultsCentral["aboveZTotalPred%s"%region],resultsCentral["aboveZTotalPredErr%s"%region],resultsCentral["highMassTotalPred%s"%region],resultsCentral["highMassTotalPredErr%s"%region])

		observedForward = observedTemplate%(resultsForward["lowMass%s"%region],resultsForward["belowZ%s"%region],resultsForward["onZ%s"%region],resultsForward["aboveZ%s"%region],resultsForward["highMass%s"%region])
		
		flavSymForward = flavSysmTemplate%(resultsForward["lowMassPred%s"%region],resultsForward["lowMassPredStatErr%s"%region],resultsForward["lowMassPredSystErr%s"%region],resultsForward["belowZPred%s"%region],resultsForward["belowZPredStatErr%s"%region],resultsForward["belowZPredSystErr%s"%region],resultsForward["onZPred%s"%region],resultsForward["onZPredStatErr%s"%region],resultsForward["onZPredSystErr%s"%region],resultsForward["aboveZPred%s"%region],resultsForward["aboveZPredStatErr%s"%region],resultsForward["aboveZPredSystErr%s"%region],resultsForward["highMassPred%s"%region],resultsForward["highMassPredStatErr%s"%region],resultsForward["highMassPredSystErr%s"%region])
		#~ flavSymForward = flavSysmTemplate%(resultsForward["lowMassPred%s"%region],resultsForward["lowMassPredStatErr%s"%region]/resultsForward["lowMassPred%s"%region],resultsForward["lowMassPredSystErr%s"%region]/resultsForward["lowMassPred%s"%region],resultsForward["belowZPred%s"%region],resultsForward["belowZPredStatErr%s"%region]/resultsForward["belowZPred%s"%region],resultsForward["belowZPredSystErr%s"%region]/resultsForward["belowZPred%s"%region],resultsForward["onZPred%s"%region],resultsForward["onZPredStatErr%s"%region]/resultsForward["onZPred%s"%region],resultsForward["onZPredSystErr%s"%region]/resultsForward["onZPred%s"%region],resultsForward["aboveZPred%s"%region],resultsForward["aboveZPredStatErr%s"%region]/resultsForward["aboveZPred%s"%region],resultsForward["aboveZPredSystErr%s"%region]/resultsForward["aboveZPred%s"%region],resultsForward["highMassPred%s"%region],resultsForward["highMassPredStatErr%s"%region]/resultsForward["highMassPred%s"%region],resultsForward["highMassPredSystErr%s"%region]/resultsForward["highMassPred%s"%region])
		
		dyForward = dyTemplate%(resultsForward["lowMassZPred%s"%region],resultsForward["lowMassZPredErr%s"%region],resultsForward["belowZZPred%s"%region],resultsForward["belowZZPredErr%s"%region],resultsForward["onZZPred%s"%region],resultsForward["onZZPredErr%s"%region],resultsForward["aboveZZPred%s"%region],resultsForward["aboveZZPredErr%s"%region],resultsForward["highMassZPred%s"%region],resultsForward["highMassZPredErr%s"%region])
		
		totalForward = totalTemplate%(resultsForward["lowMassTotalPred%s"%region],resultsForward["lowMassTotalPredErr%s"%region],resultsForward["belowZTotalPred%s"%region],resultsForward["belowZTotalPredErr%s"%region],resultsForward["onZTotalPred%s"%region],resultsForward["onZTotalPredErr%s"%region],resultsForward["aboveZTotalPred%s"%region],resultsForward["aboveZTotalPredErr%s"%region],resultsForward["highMassTotalPred%s"%region],resultsForward["highMassTotalPredErr%s"%region])

		tables.append(subTemplate%(tableColumnHeaders[selection],observedCentral,flavSymCentral,dyCentral,totalCentral,observedForward,flavSymForward,dyForward,totalForward))
	table = tableTemplate%(tables[0],tables[1],tables[2])
	saveTable(table,"cutNCount_Result_%s"%(region))
	
	
	


def produceFlavSymTable(shelves):
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Resulting estimates for flavour-symmetric backgrounds. Given is the observed event yield in \EM events and the resulting estimate after applying the correction, seperately for the SF, \EE, and \MM channels. Statistical and systematic uncertainties are given separately.
     Low-mass refers to 20 $<$ \mll $<$ 70\GeV, below-\Z to 71 $<$ \mll $<$ 81\GeV, on-\Z to  81 $<$ \mll $<$ 101\GeV, above-\Z to 81 $<$ \mll $<$ 120\GeV and high-mass to \mll $>$ 120\GeV.
     }
  \label{tab:FlavSymBackgrounds}
  \\begin{tabular}{l| c | c | c | c | c}
    \hline
    \hline
%s
\hline 
\hline
%s
\hline
\hline
%s
  \end{tabular}
\end{table}


"""

	subTemplate = """
     & \multicolumn{5}{c}{%s} \\\\ \n
    \hline
    							& Low-mass & below-\Z & On-\Z & above-\Z & High-mass \\\\ \n
    \hline
                                &  \multicolumn{5}{c}{Central} \\\\ \n
    \hline
%s
    \hline
%s
%s
%s
    \hline
                                &  \multicolumn{5}{c}{Forward} \\\\ \n
    \hline
%s
    \hline
%s
%s
%s	
"""

	observedTemplate = r"        Observed OF events       &  %d                   & %d              &  %d            &  %d       &   %d     \\" +"\n"

	flavSysmTemplate = r"        Estimate in %s channel    & $%d\pm%d\pm%d$        & $%d\pm%d\pm%d$  &  $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ \\"+"\n"



	tables = []
	
	for selection in ["default","noBTags","geOneBTags"]:

		
		resultsCentral = getResults(shelves,"central",selection)
		resultsForward = getResults(shelves,"forward",selection)
		
		observedCentral = observedTemplate%(resultsCentral["lowMassOF"],resultsCentral["belowZOF"],resultsCentral["onZOF"],resultsCentral["aboveZOF"],resultsCentral["highMassOF"])

		
		flavSymSFCentral = flavSysmTemplate%("SF",resultsCentral["lowMassPredSF"],resultsCentral["lowMassPredStatErrSF"],resultsCentral["lowMassPredSystErrSF"],resultsCentral["belowZPredSF"],resultsCentral["belowZPredStatErrSF"],resultsCentral["belowZPredSystErrSF"],resultsCentral["onZPredSF"],resultsCentral["onZPredStatErrSF"],resultsCentral["onZPredSystErrSF"],resultsCentral["aboveZPredSF"],resultsCentral["aboveZPredStatErrSF"],resultsCentral["aboveZPredSystErrSF"],resultsCentral["highMassPredSF"],resultsCentral["highMassPredStatErrSF"],resultsCentral["highMassPredSystErrSF"])
		flavSymEECentral = flavSysmTemplate%("EE",resultsCentral["lowMassPredEE"],resultsCentral["lowMassPredStatErrEE"],resultsCentral["lowMassPredSystErrEE"],resultsCentral["belowZPredEE"],resultsCentral["belowZPredStatErrEE"],resultsCentral["belowZPredSystErrEE"],resultsCentral["onZPredEE"],resultsCentral["onZPredStatErrEE"],resultsCentral["onZPredSystErrEE"],resultsCentral["aboveZPredEE"],resultsCentral["aboveZPredStatErrEE"],resultsCentral["aboveZPredSystErrEE"],resultsCentral["highMassPredEE"],resultsCentral["highMassPredStatErrEE"],resultsCentral["highMassPredSystErrEE"])
		flavSymMMCentral = flavSysmTemplate%("MM",resultsCentral["lowMassPredMM"],resultsCentral["lowMassPredStatErrMM"],resultsCentral["lowMassPredSystErrMM"],resultsCentral["belowZPredMM"],resultsCentral["belowZPredStatErrMM"],resultsCentral["belowZPredSystErrMM"],resultsCentral["onZPredMM"],resultsCentral["onZPredStatErrMM"],resultsCentral["onZPredSystErrMM"],resultsCentral["aboveZPredMM"],resultsCentral["aboveZPredStatErrMM"],resultsCentral["aboveZPredSystErrMM"],resultsCentral["highMassPredMM"],resultsCentral["highMassPredStatErrMM"],resultsCentral["highMassPredSystErrMM"])

		observedForward = observedTemplate%(resultsForward["lowMassOF"],resultsForward["belowZOF"],resultsForward["onZOF"],resultsForward["aboveZOF"],resultsForward["highMassOF"])

		
		flavSymSFForward = flavSysmTemplate%("SF",resultsForward["lowMassPredSF"],resultsForward["lowMassPredStatErrSF"],resultsForward["lowMassPredSystErrSF"],resultsForward["belowZPredSF"],resultsForward["belowZPredStatErrSF"],resultsForward["belowZPredSystErrSF"],resultsForward["onZPredSF"],resultsForward["onZPredStatErrSF"],resultsForward["onZPredSystErrSF"],resultsForward["aboveZPredSF"],resultsForward["aboveZPredStatErrSF"],resultsForward["aboveZPredSystErrSF"],resultsForward["highMassPredSF"],resultsForward["highMassPredStatErrSF"],resultsForward["highMassPredSystErrSF"])
		flavSymEEForward = flavSysmTemplate%("EE",resultsForward["lowMassPredEE"],resultsForward["lowMassPredStatErrEE"],resultsForward["lowMassPredSystErrEE"],resultsForward["belowZPredEE"],resultsForward["belowZPredStatErrEE"],resultsForward["belowZPredSystErrEE"],resultsForward["onZPredEE"],resultsForward["onZPredStatErrEE"],resultsForward["onZPredSystErrEE"],resultsForward["aboveZPredEE"],resultsForward["aboveZPredStatErrEE"],resultsForward["aboveZPredSystErrEE"],resultsForward["highMassPredEE"],resultsForward["highMassPredStatErrEE"],resultsForward["highMassPredSystErrEE"])
		flavSymMMForward = flavSysmTemplate%("MM",resultsForward["lowMassPredMM"],resultsForward["lowMassPredStatErrMM"],resultsForward["lowMassPredSystErrMM"],resultsForward["belowZPredMM"],resultsForward["belowZPredStatErrMM"],resultsForward["belowZPredSystErrMM"],resultsForward["onZPredMM"],resultsForward["onZPredStatErrMM"],resultsForward["onZPredSystErrMM"],resultsForward["aboveZPredMM"],resultsForward["aboveZPredStatErrMM"],resultsForward["aboveZPredSystErrMM"],resultsForward["highMassPredMM"],resultsForward["highMassPredStatErrMM"],resultsForward["highMassPredSystErrMM"])

		tables.append(subTemplate%(tableColumnHeaders[selection],observedCentral,flavSymSFCentral,flavSymEECentral,flavSymMMCentral,observedForward,flavSymSFForward,flavSymEEForward,flavSymMMForward))

	table = tableTemplate%(tables[0],tables[1],tables[2])
	
	saveTable(table,"cutNCount_FlavSymBkgs")	
	
	
def main():
	
	
	name = "cutAndCount"
	countingShelves = {"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	
	

	
	produceFinalTable(countingShelves,"SF")
	produceFinalTable(countingShelves,"EE")
	produceFinalTable(countingShelves,"MM")

	produceFlavSymTable(countingShelves)
	

main()

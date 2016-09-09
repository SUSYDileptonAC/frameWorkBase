### script to produce the final result tables (SF, ee and mumu) and one 
### containing the flavor symmetric prediction from OF events for each of the cases

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
	print "table tab/table_%s.tex created"%name

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

tableColumnHeaders = {"default":"no b-tag requirement","noBTags":"veto on b-tagged jets","geOneBTags":"$\geq$ 1 b-tagged jets","geTwoBTags":"$\geq$ 2 b-tagged jets"}

	
def getResults(shelve,region,selection):
	
	### get the corrections from corrections.py, z predicition from centralConfig.py and the results from the .pkl files
	
	result = {}
	
	result["rSFOF"] = getattr(rSFOF,region).val
	result["rSFOFErr"] = getattr(rSFOF,region).err
	
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
	

	result["onZTotalPredSF"] = result["onZPredSF"] + result["onZZPredSF"]
	result["onZTotalPredErrSF"] = ( result["onZPredStatErrSF"]**2 +  result["onZPredSystErrSF"]**2 + result["onZZPredErrSF"]**2 )**0.5

	
	return result


def produceFinalTable(shelves,region):
	
### template for the final result tables
### region refers to the lepton flavors here
### and can be SF, EE and MM	
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

### sub template used for each b-tag region
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
	
	dyTemplate = r"            Drell--Yan          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$  \\"+"\n"
	
	totalTemplate = r"            Total estimated          & $%d\pm%d$            & $%d\pm%d$      & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ \\"+"\n"


	tables = []
	for selection in ["default","noBTags","geOneBTags"]:
		
		resultsCentral = getResults(shelves,"central",selection)
		resultsForward = getResults(shelves,"forward",selection)

		observedCentral = observedTemplate%(resultsCentral["lowMass%s"%region],resultsCentral["belowZ%s"%region],resultsCentral["onZ%s"%region],resultsCentral["aboveZ%s"%region],resultsCentral["highMass%s"%region])
		
		flavSymCentral = flavSysmTemplate%(resultsCentral["lowMassPred%s"%region],resultsCentral["lowMassPredStatErr%s"%region],resultsCentral["lowMassPredSystErr%s"%region],resultsCentral["belowZPred%s"%region],resultsCentral["belowZPredStatErr%s"%region],resultsCentral["belowZPredSystErr%s"%region],resultsCentral["onZPred%s"%region],resultsCentral["onZPredStatErr%s"%region],resultsCentral["onZPredSystErr%s"%region],resultsCentral["aboveZPred%s"%region],resultsCentral["aboveZPredStatErr%s"%region],resultsCentral["aboveZPredSystErr%s"%region],resultsCentral["highMassPred%s"%region],resultsCentral["highMassPredStatErr%s"%region],resultsCentral["highMassPredSystErr%s"%region])
		
		dyCentral = dyTemplate%(resultsCentral["lowMassZPred%s"%region],resultsCentral["lowMassZPredErr%s"%region],resultsCentral["belowZZPred%s"%region],resultsCentral["belowZZPredErr%s"%region],resultsCentral["onZZPred%s"%region],resultsCentral["onZZPredErr%s"%region],resultsCentral["aboveZZPred%s"%region],resultsCentral["aboveZZPredErr%s"%region],resultsCentral["highMassZPred%s"%region],resultsCentral["highMassZPredErr%s"%region])
		
		totalCentral = totalTemplate%(resultsCentral["lowMassTotalPred%s"%region],resultsCentral["lowMassTotalPredErr%s"%region],resultsCentral["belowZTotalPred%s"%region],resultsCentral["belowZTotalPredErr%s"%region],resultsCentral["onZTotalPred%s"%region],resultsCentral["onZTotalPredErr%s"%region],resultsCentral["aboveZTotalPred%s"%region],resultsCentral["aboveZTotalPredErr%s"%region],resultsCentral["highMassTotalPred%s"%region],resultsCentral["highMassTotalPredErr%s"%region])

		observedForward = observedTemplate%(resultsForward["lowMass%s"%region],resultsForward["belowZ%s"%region],resultsForward["onZ%s"%region],resultsForward["aboveZ%s"%region],resultsForward["highMass%s"%region])
		
		flavSymForward = flavSysmTemplate%(resultsForward["lowMassPred%s"%region],resultsForward["lowMassPredStatErr%s"%region],resultsForward["lowMassPredSystErr%s"%region],resultsForward["belowZPred%s"%region],resultsForward["belowZPredStatErr%s"%region],resultsForward["belowZPredSystErr%s"%region],resultsForward["onZPred%s"%region],resultsForward["onZPredStatErr%s"%region],resultsForward["onZPredSystErr%s"%region],resultsForward["aboveZPred%s"%region],resultsForward["aboveZPredStatErr%s"%region],resultsForward["aboveZPredSystErr%s"%region],resultsForward["highMassPred%s"%region],resultsForward["highMassPredStatErr%s"%region],resultsForward["highMassPredSystErr%s"%region])
		
		dyForward = dyTemplate%(resultsForward["lowMassZPred%s"%region],resultsForward["lowMassZPredErr%s"%region],resultsForward["belowZZPred%s"%region],resultsForward["belowZZPredErr%s"%region],resultsForward["onZZPred%s"%region],resultsForward["onZZPredErr%s"%region],resultsForward["aboveZZPred%s"%region],resultsForward["aboveZZPredErr%s"%region],resultsForward["highMassZPred%s"%region],resultsForward["highMassZPredErr%s"%region])
		
		totalForward = totalTemplate%(resultsForward["lowMassTotalPred%s"%region],resultsForward["lowMassTotalPredErr%s"%region],resultsForward["belowZTotalPred%s"%region],resultsForward["belowZTotalPredErr%s"%region],resultsForward["onZTotalPred%s"%region],resultsForward["onZTotalPredErr%s"%region],resultsForward["aboveZTotalPred%s"%region],resultsForward["aboveZTotalPredErr%s"%region],resultsForward["highMassTotalPred%s"%region],resultsForward["highMassTotalPredErr%s"%region])

		tables.append(subTemplate%(tableColumnHeaders[selection],observedCentral,flavSymCentral,dyCentral,totalCentral,observedForward,flavSymForward,dyForward,totalForward))
	table = tableTemplate%(tables[0],tables[1],tables[2])
	saveTable(table,"cutNCount_Result_%s"%(region))
	
	
	


def produceFlavSymTable(shelves):

### table containing the flavor symmetric background prediciton estimated from OF events
	
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

### sub template for each b-tag region
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
    \hline
                                &  \multicolumn{5}{c}{Forward} \\\\ \n
    \hline
%s
    \hline
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
		
		observedForward = observedTemplate%(resultsForward["lowMassOF"],resultsForward["belowZOF"],resultsForward["onZOF"],resultsForward["aboveZOF"],resultsForward["highMassOF"])

		
		flavSymSFForward = flavSysmTemplate%("SF",resultsForward["lowMassPredSF"],resultsForward["lowMassPredStatErrSF"],resultsForward["lowMassPredSystErrSF"],resultsForward["belowZPredSF"],resultsForward["belowZPredStatErrSF"],resultsForward["belowZPredSystErrSF"],resultsForward["onZPredSF"],resultsForward["onZPredStatErrSF"],resultsForward["onZPredSystErrSF"],resultsForward["aboveZPredSF"],resultsForward["aboveZPredStatErrSF"],resultsForward["aboveZPredSystErrSF"],resultsForward["highMassPredSF"],resultsForward["highMassPredStatErrSF"],resultsForward["highMassPredSystErrSF"])
		
		tables.append(subTemplate%(tableColumnHeaders[selection],observedCentral,flavSymSFCentral,observedForward,flavSymSFForward))

	table = tableTemplate%(tables[0],tables[1],tables[2])
	
	saveTable(table,"cutNCount_FlavSymBkgs")
	
	
def main():
	
	
	name = "cutAndCount"
	countingShelves = {"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	
	
	produceFinalTable(countingShelves,"SF")

	produceFlavSymTable(countingShelves)
	

main()

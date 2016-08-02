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
	result = {}
	
	region = "inclusive"
	
	result["rSFOF"] = getattr(rSFOF,region).val
	result["rSFOFErr"] = getattr(rSFOF,region).err
	result["rEEOF"] = getattr(rEEOF,region).val
	result["rEEOFErr"] = getattr(rEEOF,region).err
	result["rMMOF"] = getattr(rMMOF,region).val
	result["rMMOFErr"] = getattr(rMMOF,region).err
	
	for selection in selections:
		
		result[selection] = {}
		
		result[selection]["lowMassEE"] = shelve[signalRegion][selection]["lowMass"]["EE"]
		result[selection]["lowMassMM"] = shelve[signalRegion][selection]["lowMass"]["MM"]
		result[selection]["lowMassSF"] = shelve[signalRegion][selection]["lowMass"]["EE"] + shelve[signalRegion][selection]["lowMass"]["MM"]
		result[selection]["lowMassOF"] = shelve[signalRegion][selection]["lowMass"]["EM"]
		result[selection]["lowMassPredSF"] = result[selection]["lowMassOF"]*getattr(rSFOF,region).val
		result[selection]["lowMassPredStatErrSF"] = result[selection]["lowMassOF"]**0.5*getattr(rSFOF,region).val
		result[selection]["lowMassPredSystErrSF"] = result[selection]["lowMassOF"]*getattr(rSFOF,region).err
		
		result[selection]["lowMassPredEE"] = result[selection]["lowMassOF"]*getattr(rEEOF,region).val
		result[selection]["lowMassPredStatErrEE"] = result[selection]["lowMassOF"]**0.5*getattr(rEEOF,region).val
		result[selection]["lowMassPredSystErrEE"] = result[selection]["lowMassOF"]*getattr(rEEOF,region).err
		
		result[selection]["lowMassPredMM"] = result[selection]["lowMassOF"]*getattr(rMMOF,region).val
		result[selection]["lowMassPredStatErrMM"] = result[selection]["lowMassOF"]**0.5*getattr(rMMOF,region).val
		result[selection]["lowMassPredSystErrMM"] = result[selection]["lowMassOF"]*getattr(rMMOF,region).err
		
		result[selection]["lowMassZPredSF"] = getattr(zPredictions.NLL.SF,selection).val*getattr(rOutIn.lowMass,region).val
		result[selection]["lowMassZPredErrSF"] = ((getattr(zPredictions.NLL.SF,selection).val*getattr(rOutIn.lowMass,region).err)**2 + (getattr(zPredictions.NLL.SF,selection).err*getattr(rOutIn.lowMass,region).val)**2 )**0.5
		
		result[selection]["lowMassTotalPredSF"] = result[selection]["lowMassPredSF"] + result[selection]["lowMassZPredSF"]
		result[selection]["lowMassTotalPredErrSF"] = ( result[selection]["lowMassPredStatErrSF"]**2 +  result[selection]["lowMassPredSystErrSF"]**2 + result[selection]["lowMassZPredErrSF"]**2 )**0.5
	
		
		result[selection]["highMassEE"] = shelve[signalRegion][selection]["highMass"]["EE"]
		result[selection]["highMassMM"] = shelve[signalRegion][selection]["highMass"]["MM"]
		result[selection]["highMassSF"] = shelve[signalRegion][selection]["highMass"]["EE"] + shelve[signalRegion][selection]["highMass"]["MM"]
		result[selection]["highMassOF"] = shelve[signalRegion][selection]["highMass"]["EM"]
		
		result[selection]["highMassPredSF"] = result[selection]["highMassOF"]*getattr(rSFOF,region).val
		result[selection]["highMassPredStatErrSF"] = result[selection]["highMassOF"]**0.5*getattr(rSFOF,region).val
		result[selection]["highMassPredSystErrSF"] = result[selection]["highMassOF"]*getattr(rSFOF,region).err
		
		result[selection]["highMassPredEE"] = result[selection]["highMassOF"]*getattr(rEEOF,region).val
		result[selection]["highMassPredStatErrEE"] = result[selection]["highMassOF"]**0.5*getattr(rEEOF,region).val
		result[selection]["highMassPredSystErrEE"] = result[selection]["highMassOF"]*getattr(rEEOF,region).err
		
		result[selection]["highMassPredMM"] = result[selection]["highMassOF"]*getattr(rMMOF,region).val
		result[selection]["highMassPredStatErrMM"] = result[selection]["highMassOF"]**0.5*getattr(rMMOF,region).val
		result[selection]["highMassPredSystErrMM"] = result[selection]["highMassOF"]*getattr(rMMOF,region).err
		
		result[selection]["highMassZPredSF"] = getattr(zPredictions.NLL.SF,selection).val*getattr(rOutIn.highMass,region).val
		result[selection]["highMassZPredErrSF"] = ((getattr(zPredictions.NLL.SF,selection).val*getattr(rOutIn.highMass,region).err)**2 + (getattr(zPredictions.NLL.SF,selection).err*getattr(rOutIn.highMass,region).val)**2 )**0.5
		
		result[selection]["highMassTotalPredSF"] = result[selection]["highMassPredSF"] + result[selection]["highMassZPredSF"]
		result[selection]["highMassTotalPredErrSF"] = ( result[selection]["highMassPredStatErrSF"]**2 +  result[selection]["highMassPredSystErrSF"]**2 + result[selection]["highMassZPredErrSF"]**2 )**0.5
	#~ 
	
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
	result["edgeMassPredSF"] = result["edgeMassOF"]*getattr(rSFOF,region).val
	result["edgeMassPredStatErrSF"] = result["edgeMassOF"]**0.5*getattr(rSFOF,region).val
	result["edgeMassPredSystErrSF"] = result["edgeMassOF"]*getattr(rSFOF,region).err
	
	result["edgeMassPredEE"] = result["edgeMassOF"]*getattr(rEEOF,region).val
	result["edgeMassPredStatErrEE"] = result["edgeMassOF"]**0.5*getattr(rEEOF,region).val
	result["edgeMassPredSystErrEE"] = result["edgeMassOF"]*getattr(rEEOF,region).err
	
	result["edgeMassPredMM"] = result["edgeMassOF"]*getattr(rMMOF,region).val
	result["edgeMassPredStatErrMM"] = result["edgeMassOF"]**0.5*getattr(rMMOF,region).val
	result["edgeMassPredSystErrMM"] = result["edgeMassOF"]*getattr(rMMOF,region).err
	
	result["edgeMassZPredSF"] = getattr(zPredictions.legacy.SF,region).val*getattr(rOutIn.edgeMass,region).val
	result["edgeMassZPredErrSF"] = ((getattr(zPredictions.legacy.SF,region).val*getattr(rOutIn.edgeMass,region).err)**2 + (getattr(zPredictions.legacy.SF,region).err*getattr(rOutIn.edgeMass,region).val)**2 )**0.5
	
	result["edgeMassTotalPredSF"] = result["edgeMassPredSF"] + result["edgeMassZPredSF"]
	result["edgeMassTotalPredErrSF"] = ( result["edgeMassPredStatErrSF"]**2 +  result["edgeMassPredSystErrSF"]**2 + result["edgeMassZPredErrSF"]**2 )**0.5

	
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
		

	observed = observedTemplate%(resultsNLL["lowNLL"]["lowMass%s"%region],resultsNLL["highNLL"]["lowMass%s"%region],resultsNLL["lowNLL"]["highMass%s"%region],resultsNLL["highNLL"]["highMass%s"%region],resultsLegacy["edgeMass%s"%region])
		
	flavSym = flavSysmTemplate%(resultsNLL["lowNLL"]["lowMassPred%s"%region],resultsNLL["lowNLL"]["lowMassPredStatErr%s"%region],resultsNLL["lowNLL"]["lowMassPredSystErr%s"%region],resultsNLL["highNLL"]["lowMassPred%s"%region],resultsNLL["highNLL"]["lowMassPredStatErr%s"%region],resultsNLL["highNLL"]["lowMassPredSystErr%s"%region],resultsNLL["lowNLL"]["highMassPred%s"%region],resultsNLL["lowNLL"]["highMassPredStatErr%s"%region],resultsNLL["lowNLL"]["highMassPredSystErr%s"%region],resultsNLL["highNLL"]["highMassPred%s"%region],resultsNLL["highNLL"]["highMassPredStatErr%s"%region],resultsNLL["highNLL"]["highMassPredSystErr%s"%region],resultsLegacy["edgeMassPred%s"%region],resultsLegacy["edgeMassPredStatErr%s"%region],resultsLegacy["edgeMassPredSystErr%s"%region])
	
	dy = dyTemplate%(resultsNLL["lowNLL"]["lowMassZPred%s"%region],resultsNLL["lowNLL"]["lowMassZPredErr%s"%region],resultsNLL["highNLL"]["lowMassZPred%s"%region],resultsNLL["highNLL"]["lowMassZPredErr%s"%region],resultsNLL["lowNLL"]["highMassZPred%s"%region],resultsNLL["lowNLL"]["highMassZPredErr%s"%region],resultsNLL["highNLL"]["highMassZPred%s"%region],resultsNLL["highNLL"]["highMassZPredErr%s"%region],resultsLegacy["edgeMassZPred%s"%region],resultsLegacy["edgeMassZPredErr%s"%region])
		
	totalPrediction = totalTemplate%(resultsNLL["lowNLL"]["lowMassTotalPred%s"%region],resultsNLL["lowNLL"]["lowMassTotalPredErr%s"%region],resultsNLL["highNLL"]["lowMassTotalPred%s"%region],resultsNLL["highNLL"]["lowMassTotalPredErr%s"%region],resultsNLL["lowNLL"]["highMassTotalPred%s"%region],resultsNLL["lowNLL"]["highMassTotalPredErr%s"%region],resultsNLL["highNLL"]["highMassTotalPred%s"%region],resultsNLL["highNLL"]["highMassTotalPredErr%s"%region],resultsLegacy["edgeMassTotalPred%s"%region],resultsLegacy["edgeMassTotalPredErr%s"%region])


		
	table = tableTemplate%(observed,flavSym,dy,totalPrediction)
	saveTable(table,"cutNCount_Result_%s"%(region))
	
	
	


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
\hline 
\hline

  \end{tabular}
\end{table}


"""


	observedTemplate = r"        Observed OF events       &  %d                   & %d              &  %d            &  %d       &   %d     \\" +"\n"

	flavSysmTemplate = r"        Estimate in %s channel    & $%d\pm%d\pm%d$        & $%d\pm%d\pm%d$  &  $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ \\"+"\n"

		
	resultsNLL = getResultsNLL(shelves,"NLL")
	resultsLegacy = getResultsLegacy(shelves,"legacy")
		
	observed = observedTemplate%(resultsNLL["lowNLL"]["lowMassOF"],resultsNLL["highNLL"]["lowMassOF"],resultsNLL["lowNLL"]["highMassOF"],resultsNLL["highNLL"]["highMassOF"],resultsLegacy["edgeMassOF"])

		
	SFPrediciton = flavSysmTemplate%("SF",resultsNLL["lowNLL"]["lowMassPredSF"],resultsNLL["lowNLL"]["lowMassPredStatErrSF"],resultsNLL["lowNLL"]["lowMassPredSystErrSF"],resultsNLL["highNLL"]["lowMassPredSF"],resultsNLL["highNLL"]["lowMassPredStatErrSF"],resultsNLL["highNLL"]["lowMassPredSystErrSF"],resultsNLL["lowNLL"]["highMassPredSF"],resultsNLL["lowNLL"]["highMassPredStatErrSF"],resultsNLL["lowNLL"]["highMassPredSystErrSF"],resultsNLL["highNLL"]["highMassPredSF"],resultsNLL["highNLL"]["highMassPredStatErrSF"],resultsNLL["highNLL"]["highMassPredSystErrSF"],resultsLegacy["edgeMassPredSF"],resultsLegacy["edgeMassPredStatErrSF"],resultsLegacy["edgeMassPredSystErrSF"],)
	EEPrediciton = flavSysmTemplate%("EE",resultsNLL["lowNLL"]["lowMassPredEE"],resultsNLL["lowNLL"]["lowMassPredStatErrEE"],resultsNLL["lowNLL"]["lowMassPredSystErrEE"],resultsNLL["highNLL"]["lowMassPredEE"],resultsNLL["highNLL"]["lowMassPredStatErrEE"],resultsNLL["highNLL"]["lowMassPredSystErrEE"],resultsNLL["lowNLL"]["highMassPredEE"],resultsNLL["lowNLL"]["highMassPredStatErrEE"],resultsNLL["lowNLL"]["highMassPredSystErrEE"],resultsNLL["highNLL"]["highMassPredEE"],resultsNLL["highNLL"]["highMassPredStatErrEE"],resultsNLL["highNLL"]["highMassPredSystErrEE"],resultsLegacy["edgeMassPredEE"],resultsLegacy["edgeMassPredStatErrEE"],resultsLegacy["edgeMassPredSystErrEE"],)
	MMPrediciton= flavSysmTemplate%("MM",resultsNLL["lowNLL"]["lowMassPredMM"],resultsNLL["lowNLL"]["lowMassPredStatErrMM"],resultsNLL["lowNLL"]["lowMassPredSystErrMM"],resultsNLL["highNLL"]["lowMassPredMM"],resultsNLL["highNLL"]["lowMassPredStatErrMM"],resultsNLL["highNLL"]["lowMassPredSystErrMM"],resultsNLL["lowNLL"]["highMassPredMM"],resultsNLL["lowNLL"]["highMassPredStatErrMM"],resultsNLL["lowNLL"]["highMassPredSystErrMM"],resultsNLL["highNLL"]["highMassPredMM"],resultsNLL["highNLL"]["highMassPredStatErrMM"],resultsNLL["highNLL"]["highMassPredSystErrMM"],resultsLegacy["edgeMassPredMM"],resultsLegacy["edgeMassPredStatErrMM"],resultsLegacy["edgeMassPredSystErrMM"],)
		
		
	saveTable(tableTemplate%(observed,SFPrediciton,EEPrediciton,MMPrediciton),"cutNCount_FlavSymBkgs")	
	
	
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
	

	
	produceFinalTable(countingShelves,"SF")
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

import pickle
import os
import sys


from corrections import rSFOF, rEEOF, rMMOF, rOutIn, rOutInEE, rOutInMM
from centralConfig import zPredictions, regionsToUse, runRanges

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


def getDataCards(shelves,combination):
	
	results = {"central":getResults(shelves,"central"),"forward":getResults(shelves,"forward")}
	for etaRegion in ["forward","central"]:
		for region in ["lowMass","onZ","highMass"]:
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
			outFile = open("dataCards/dataCard_%s_%s_%s.txt"%(region, etaRegion, combination), "w")
			outFile.write(result)
			outFile.close()		
def getResults(shelve,region):
	
	result = {}
	
	result["rSFOF"] = getattr(rSFOF,region).val
	result["rSFOFErr"] = getattr(rSFOF,region).err
	result["rEEOF"] = getattr(rEEOF,region).val
	result["rEEOFErr"] = getattr(rEEOF,region).err
	result["rMMOF"] = getattr(rMMOF,region).val
	result["rMMOFErr"] = getattr(rMMOF,region).err
	
	result["lowMassEE"] = shelve[region]["default"]["edgeMass"]["EE"]
	result["lowMassMM"] = shelve[region]["default"]["edgeMass"]["MM"]
	result["lowMassSF"] = shelve[region]["default"]["edgeMass"]["EE"] + shelve[region]["default"]["edgeMass"]["MM"]
	result["lowMassOF"] = shelve[region]["default"]["edgeMass"]["EM"]
	
	result["lowMassPredSF"] = result["lowMassOF"]*getattr(rSFOF,region).val
	result["lowMassPredStatErrSF"] = result["lowMassOF"]**0.5*getattr(rSFOF,region).val
	result["lowMassPredSystErrSF"] = result["lowMassOF"]*getattr(rSFOF,region).err
	
	result["lowMassPredEE"] = result["lowMassOF"]*getattr(rEEOF,region).val
	result["lowMassPredStatErrEE"] = result["lowMassOF"]**0.5*getattr(rEEOF,region).val
	result["lowMassPredSystErrEE"] = result["lowMassOF"]*getattr(rEEOF,region).err
	
	result["lowMassPredMM"] = result["lowMassOF"]*getattr(rMMOF,region).val
	result["lowMassPredStatErrMM"] = result["lowMassOF"]**0.5*getattr(rMMOF,region).val
	result["lowMassPredSystErrMM"] = result["lowMassOF"]*getattr(rMMOF,region).err
	
	result["lowMassZPredSF"] = getattr(zPredictions.SF,region).val*getattr(rOutIn.lowMass,region).val
	result["lowMassZPredErrSF"] = ((getattr(zPredictions.SF,region).val*getattr(rOutIn.lowMass,region).err)**2 + (getattr(zPredictions.SF,region).err*getattr(rOutIn.lowMass,region).val)**2 )**0.5
	
	result["lowMassZPredEE"] = getattr(zPredictions.EE,region).val*getattr(rOutInEE.lowMass,region).val
	result["lowMassZPredErrEE"] = ((getattr(zPredictions.EE,region).val*getattr(rOutInEE.lowMass,region).err)**2 + (getattr(zPredictions.EE,region).err*getattr(rOutInEE.lowMass,region).val)**2 )**0.5
	
	result["lowMassZPredMM"] = getattr(zPredictions.MM,region).val*getattr(rOutInMM.lowMass,region).val
	result["lowMassZPredErrMM"] = ((getattr(zPredictions.MM,region).val*getattr(rOutInMM.lowMass,region).err)**2 + (getattr(zPredictions.MM,region).err*getattr(rOutInMM.lowMass,region).val)**2 )**0.5
	
	result["lowMassTotalPredSF"] = result["lowMassPredSF"] + result["lowMassZPredSF"]
	result["lowMassTotalPredErrSF"] = ( result["lowMassPredStatErrSF"]**2 +  result["lowMassPredSystErrSF"]**2 + result["lowMassZPredErrSF"]**2 )**0.5
	
	result["lowMassTotalPredEE"] = result["lowMassPredEE"] + result["lowMassZPredEE"]
	result["lowMassTotalPredErrEE"] = ( result["lowMassPredStatErrEE"]**2 +  result["lowMassPredSystErrEE"]**2 + result["lowMassZPredErrEE"]**2 )**0.5
	
	result["lowMassTotalPredMM"] = result["lowMassPredMM"] + result["lowMassZPredMM"]
	result["lowMassTotalPredErrMM"] = ( result["lowMassPredStatErrMM"]**2 +  result["lowMassPredSystErrMM"]**2 + result["lowMassZPredErrMM"]**2 )**0.5
	
	
	
	
	result["highMassEE"] = shelve[region]["default"]["highMass"]["EE"]
	result["highMassMM"] = shelve[region]["default"]["highMass"]["MM"]
	result["highMassSF"] = shelve[region]["default"]["highMass"]["EE"] + shelve[region]["default"]["highMass"]["MM"]
	result["highMassOF"] = shelve[region]["default"]["highMass"]["EM"]
	
	result["highMassPredSF"] = result["highMassOF"]*getattr(rSFOF,region).val
	result["highMassPredStatErrSF"] = result["highMassOF"]**0.5*getattr(rSFOF,region).val
	result["highMassPredSystErrSF"] = result["highMassOF"]*getattr(rSFOF,region).err
	
	result["highMassPredEE"] = result["highMassOF"]*getattr(rEEOF,region).val
	result["highMassPredStatErrEE"] = result["highMassOF"]**0.5*getattr(rEEOF,region).val
	result["highMassPredSystErrEE"] = result["highMassOF"]*getattr(rEEOF,region).err
	
	result["highMassPredMM"] = result["highMassOF"]*getattr(rMMOF,region).val
	result["highMassPredStatErrMM"] = result["highMassOF"]**0.5*getattr(rMMOF,region).val
	result["highMassPredSystErrMM"] = result["highMassOF"]*getattr(rMMOF,region).err
	
	result["highMassZPredSF"] = getattr(zPredictions.SF,region).val*getattr(rOutIn.highMass,region).val
	result["highMassZPredErrSF"] = ((getattr(zPredictions.SF,region).val*getattr(rOutIn.highMass,region).err)**2 + (getattr(zPredictions.SF,region).err*getattr(rOutIn.highMass,region).val)**2 )**0.5
	
	result["highMassZPredEE"] = getattr(zPredictions.EE,region).val*getattr(rOutInEE.highMass,region).val
	result["highMassZPredErrEE"] = ((getattr(zPredictions.EE,region).val*getattr(rOutInEE.highMass,region).err)**2 + (getattr(zPredictions.EE,region).err*getattr(rOutInEE.highMass,region).val)**2 )**0.5
	
	result["highMassZPredMM"] = getattr(zPredictions.MM,region).val*getattr(rOutInMM.highMass,region).val
	result["highMassZPredErrMM"] = ((getattr(zPredictions.MM,region).val*getattr(rOutInMM.highMass,region).err)**2 + (getattr(zPredictions.MM,region).err*getattr(rOutInMM.highMass,region).val)**2 )**0.5
	

	result["highMassTotalPredSF"] = result["highMassPredSF"] + result["highMassZPredSF"]
	result["highMassTotalPredErrSF"] = ( result["highMassPredStatErrSF"]**2 +  result["highMassPredSystErrSF"]**2 + result["highMassZPredErrSF"]**2 )**0.5
	
	result["highMassTotalPredEE"] = result["highMassPredEE"] + result["highMassZPredEE"]
	result["highMassTotalPredErrEE"] = ( result["highMassPredStatErrEE"]**2 +  result["highMassPredSystErrEE"]**2 + result["highMassZPredErrEE"]**2 )**0.5
	
	result["highMassTotalPredMM"] = result["highMassPredMM"] + result["highMassZPredMM"]
	result["highMassTotalPredErrMM"] = ( result["highMassPredStatErrMM"]**2 +  result["highMassPredSystErrMM"]**2 + result["highMassZPredErrMM"]**2 )**0.5	

	
	
	
	result["onZEE"] = shelve[region]["default"]["zMass"]["EE"]
	result["onZMM"] = shelve[region]["default"]["zMass"]["MM"]
	result["onZSF"] = shelve[region]["default"]["zMass"]["EE"] + shelve[region]["default"]["zMass"]["MM"]
	result["onZOF"] = shelve[region]["default"]["zMass"]["EM"]	
	
	result["onZPredSF"] = result["onZOF"]*getattr(rSFOF,region).val
	result["onZPredStatErrSF"] = result["onZOF"]**0.5*getattr(rSFOF,region).val
	result["onZPredSystErrSF"] = result["onZOF"]*getattr(rSFOF,region).err
	
	result["onZPredEE"] = result["onZOF"]*getattr(rEEOF,region).val
	result["onZPredStatErrEE"] = result["onZOF"]**0.5*getattr(rEEOF,region).val
	result["onZPredSystErrEE"] = result["onZOF"]*getattr(rEEOF,region).err
	
	result["onZPredMM"] = result["onZOF"]*getattr(rMMOF,region).val
	result["onZPredStatErrMM"] = result["onZOF"]**0.5*getattr(rMMOF,region).val
	result["onZPredSystErrMM"] = result["onZOF"]*getattr(rMMOF,region).err
	
	result["onZZPredSF"] = getattr(zPredictions.SF,region).val
	result["onZZPredErrSF"] = getattr(zPredictions.SF,region).err
	
	result["onZZPredEE"] = getattr(zPredictions.EE,region).val
	result["onZZPredErrEE"] = getattr(zPredictions.EE,region).err
	
	result["onZZPredMM"] = getattr(zPredictions.MM,region).val
	result["onZZPredErrMM"] = getattr(zPredictions.MM,region).err
	

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
 \scriptsize
 \centering
 \caption{Results of the edge-search counting experiment for event yields in the signal regions.
     The statistical and systematic uncertainties are added in quadrature, except for the flavor-symmetric backgrounds.
     Low-mass refers to $20 < \mll < 70$\GeV, on-\Z to  $81 < \mll < 101$\GeV and high-mass to $\mll > 120$\GeV.
     }
  \label{tab:METresults2012}
  \\begin{tabular}{l| cc | cc | cc}
    \hline
    \hline
    							& \multicolumn{2}{c}{Low-mass} & \multicolumn{2}{c}{On-\Z} & \multicolumn{2}{c}{High-mass} \\\\ \n
    \hline
                                &  Central        & Forward  &  Central  & Forward   &  Central        & Forward \\\\ \n
    \hline
%s
    \hline
%s
%s
    \hline
%s
    \hline
         Observed - estimated  & $xxx^{+xx}_{-xx}$      & $5^{+xx}_{-xx}$ & $xx^{+xx}_{-xx} $ & $-3^{+xx}_{-xx}$ & $47^{+xx}_{-xx}$ & $-62^{+xx}_{-xx} $ \\\\ \n
    \hline
   Significance      & xx~$\sigma$    &  xx~$\sigma$  & xx~$\sigma$ & xx~$\sigma$ & xx~$\sigma$ & xx~$\sigma$ \\\\ \n
   \hline
    \hline
  \end{tabular}
\end{table}


"""

	observedTemplate = r"        Observed       &  %d                   & %d              &  %d            &  %d       &   %d           &   %d    \\" +"\n"

	flavSysmTemplate = r"        Flavor-symmetric    & $%d\pm%d\pm%d$        & $%d\pm%d\pm%d$  &  $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ \\"+"\n"

	dyTemplate = r"            Drell--Yan          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%d\pm%d$ & $%d\pm%d$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ \\"+"\n"
	
	totalTemplate = r"            Total estimated          & $%d\pm%d$            & $%d\pm%d$      & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ \\"+"\n"


	
	
	resultsCentral = getResults(shelves,"central")
	resultsForward = getResults(shelves,"forward")

	observed = observedTemplate%(resultsCentral["lowMass%s"%region],resultsForward["lowMass%s"%region],resultsCentral["onZ%s"%region],resultsForward["onZ%s"%region],resultsCentral["highMass%s"%region],resultsForward["highMass%s"%region])
	
	flavSym = flavSysmTemplate%(resultsCentral["lowMassPred%s"%region],resultsCentral["lowMassPredStatErr%s"%region],resultsCentral["lowMassPredSystErr%s"%region],resultsForward["lowMassPred%s"%region],resultsForward["lowMassPredStatErr%s"%region],resultsForward["lowMassPredSystErr%s"%region],resultsCentral["onZPred%s"%region],resultsCentral["onZPredStatErr%s"%region],resultsCentral["onZPredSystErr%s"%region],resultsForward["onZPred%s"%region],resultsForward["onZPredStatErr%s"%region],resultsForward["onZPredSystErr%s"%region],resultsCentral["highMassPred%s"%region],resultsCentral["highMassPredStatErr%s"%region],resultsCentral["highMassPredSystErr%s"%region],resultsForward["highMassPred%s"%region],resultsForward["highMassPredStatErr%s"%region],resultsForward["highMassPredSystErr%s"%region])
	
	dy = dyTemplate%(resultsCentral["lowMassZPred%s"%region],resultsCentral["lowMassZPredErr%s"%region],resultsForward["lowMassZPred%s"%region],resultsForward["lowMassZPredErr%s"%region],resultsCentral["onZZPred%s"%region],resultsCentral["onZZPredErr%s"%region],resultsForward["onZZPred%s"%region],resultsForward["onZZPredErr%s"%region],resultsCentral["highMassZPred%s"%region],resultsCentral["highMassZPredErr%s"%region],resultsForward["highMassZPred%s"%region],resultsForward["highMassZPredErr%s"%region])
	
	total = totalTemplate%(resultsCentral["lowMassTotalPred%s"%region],resultsCentral["lowMassTotalPredErr%s"%region],resultsForward["lowMassTotalPred%s"%region],resultsForward["lowMassTotalPredErr%s"%region],resultsCentral["onZTotalPred%s"%region],resultsCentral["onZTotalPredErr%s"%region],resultsForward["onZTotalPred%s"%region],resultsForward["onZTotalPredErr%s"%region],resultsCentral["highMassTotalPred%s"%region],resultsCentral["highMassTotalPredErr%s"%region],resultsForward["highMassTotalPred%s"%region],resultsForward["highMassTotalPredErr%s"%region])

	table = tableTemplate%(observed,flavSym,dy,total)
	
	saveTable(table,"cutNCount_Result_%s"%region)
	
	
	


def produceFlavSymTable(shelves):
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \scriptsize
 \centering
 \caption{Resulting estimates for flavour-symmetric backgrounds. Given is the observed event yield in \EM events and the resulting estimate after applying the correction, seperately for the SF, \EE, and \MM channels. Statistical and systematic uncertainties are given separately.
     Low-mass refers to $20 < \mll < 70$\GeV, on-\Z to  $81 < \mll < 101$\GeV and high-mass to $\mll > 120$\GeV.
     }
  \label{tab:FlavSymBackgrounds}
  \\begin{tabular}{l| cc | cc | cc}
    \hline
    \hline
    							& \multicolumn{2}{c}{Low-mass} & \multicolumn{2}{c}{On-\Z} & \multicolumn{2}{c}{High-mass} \\\\ \n
    \hline
                                &  Central        & Forward  &  Central  & Forward   &  Central        & Forward \\\\ \n
    \hline
%s
    \hline
%s
%s
%s

  \end{tabular}
\end{table}


"""

	observedTemplate = r"        Observed OF events       &  %d                   & %d              &  %d            &  %d       &   %d           &   %d    \\" +"\n"

	flavSysmTemplate = r"        Estimate in %s channel    & $%d\pm%d\pm%d$        & $%d\pm%d\pm%d$  &  $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ \\"+"\n"



	
	
	resultsCentral = getResults(shelves,"central")
	resultsForward = getResults(shelves,"forward")
	observed = observedTemplate%(resultsCentral["lowMassOF"],resultsForward["lowMassOF"],resultsCentral["onZOF"],resultsForward["onZOF"],resultsCentral["highMassOF"],resultsForward["highMassOF"])

	
	flavSymSF = flavSysmTemplate%("SF",resultsCentral["lowMassPredSF"],resultsCentral["lowMassPredStatErrSF"],resultsCentral["lowMassPredSystErrSF"],resultsForward["lowMassPredSF"],resultsForward["lowMassPredStatErrSF"],resultsForward["lowMassPredSystErrSF"],resultsCentral["onZPredSF"],resultsCentral["onZPredStatErrSF"],resultsCentral["onZPredSystErrSF"],resultsForward["onZPredSF"],resultsForward["onZPredStatErrSF"],resultsForward["onZPredSystErrSF"],resultsCentral["highMassPredSF"],resultsCentral["highMassPredStatErrSF"],resultsCentral["highMassPredSystErrSF"],resultsForward["highMassPredSF"],resultsForward["highMassPredStatErrSF"],resultsForward["highMassPredSystErrSF"])
	flavSymEE = flavSysmTemplate%("\EE",resultsCentral["lowMassPredEE"],resultsCentral["lowMassPredStatErrEE"],resultsCentral["lowMassPredSystErrEE"],resultsForward["lowMassPredEE"],resultsForward["lowMassPredStatErrEE"],resultsForward["lowMassPredSystErrEE"],resultsCentral["onZPredEE"],resultsCentral["onZPredStatErrEE"],resultsCentral["onZPredSystErrEE"],resultsForward["onZPredEE"],resultsForward["onZPredStatErrEE"],resultsForward["onZPredSystErrEE"],resultsCentral["highMassPredEE"],resultsCentral["highMassPredStatErrEE"],resultsCentral["highMassPredSystErrEE"],resultsForward["highMassPredEE"],resultsForward["highMassPredStatErrEE"],resultsForward["highMassPredSystErrEE"])
	flavSymMM = flavSysmTemplate%("\MM",resultsCentral["lowMassPredMM"],resultsCentral["lowMassPredStatErrMM"],resultsCentral["lowMassPredSystErrMM"],resultsForward["lowMassPredMM"],resultsForward["lowMassPredStatErrMM"],resultsForward["lowMassPredSystErrMM"],resultsCentral["onZPredMM"],resultsCentral["onZPredStatErrMM"],resultsCentral["onZPredSystErrMM"],resultsForward["onZPredMM"],resultsForward["onZPredStatErrMM"],resultsForward["onZPredSystErrMM"],resultsCentral["highMassPredMM"],resultsCentral["highMassPredStatErrMM"],resultsCentral["highMassPredSystErrMM"],resultsForward["highMassPredMM"],resultsForward["highMassPredStatErrMM"],resultsForward["highMassPredSystErrMM"])


	table = tableTemplate%(observed,flavSymSF,flavSymEE,flavSymMM)
	
	saveTable(table,"cutNCount_FlavSymBkgs")	
	
	
def produceZTable(shelves):

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



	
	
	resultsCentral = getResults(shelves,"central")
	resultsForward = getResults(shelves,"forward")

	rOutInLowMassCentral = rOutInTemplate%("low",shelvesROutIn["central"]["rOutInLowMassEE"],shelvesROutIn["central"]["rOutInLowMassErrEE"],shelvesROutIn["central"]["rOutInLowMassSystEE"],shelvesROutIn["central"]["rOutInLowMassMM"],shelvesROutIn["central"]["rOutInLowMassErrMM"],shelvesROutIn["central"]["rOutInLowMassSystMM"],shelvesROutIn["central"]["rOutInLowMassSF"],shelvesROutIn["central"]["rOutInLowMassErrSF"],shelvesROutIn["central"]["rOutInLowMassSystSF"])
	rOutInLowMassForward = rOutInTemplate%("low",shelvesROutIn["forward"]["rOutInLowMassEE"],shelvesROutIn["forward"]["rOutInLowMassErrEE"],shelvesROutIn["forward"]["rOutInLowMassSystEE"],shelvesROutIn["forward"]["rOutInLowMassMM"],shelvesROutIn["forward"]["rOutInLowMassErrMM"],shelvesROutIn["forward"]["rOutInLowMassSystMM"],shelvesROutIn["forward"]["rOutInLowMassSF"],shelvesROutIn["forward"]["rOutInLowMassErrSF"],shelvesROutIn["forward"]["rOutInLowMassSystSF"])

	rOutInHighMassCentral = rOutInTemplate%("high",shelvesROutIn["central"]["rOutInHighMassEE"],shelvesROutIn["central"]["rOutInHighMassErrEE"],shelvesROutIn["central"]["rOutInHighMassSystEE"],shelvesROutIn["central"]["rOutInHighMassMM"],shelvesROutIn["central"]["rOutInHighMassErrMM"],shelvesROutIn["central"]["rOutInHighMassSystMM"],shelvesROutIn["central"]["rOutInHighMassSF"],shelvesROutIn["central"]["rOutInHighMassErrSF"],shelvesROutIn["central"]["rOutInHighMassSystSF"])
	rOutInHighMassForward = rOutInTemplate%("high",shelvesROutIn["forward"]["rOutInHighMassEE"],shelvesROutIn["forward"]["rOutInHighMassErrEE"],shelvesROutIn["forward"]["rOutInHighMassSystEE"],shelvesROutIn["forward"]["rOutInHighMassMM"],shelvesROutIn["forward"]["rOutInHighMassErrMM"],shelvesROutIn["forward"]["rOutInHighMassSystMM"],shelvesROutIn["forward"]["rOutInHighMassSF"],shelvesROutIn["forward"]["rOutInHighMassErrSF"],shelvesROutIn["forward"]["rOutInHighMassSystSF"])

	predictionLowMassCentral = predictionTemplate%("low",resultsCentral["lowMassZPredEE"],resultsCentral["lowMassZPredErrEE"],resultsCentral["lowMassZPredMM"],resultsCentral["lowMassZPredErrMM"],resultsCentral["lowMassZPredSF"],resultsCentral["lowMassZPredErrSF"])
	predictionLowMassForward = predictionTemplate%("low",resultsForward["lowMassZPredEE"],resultsForward["lowMassZPredErrEE"],resultsForward["lowMassZPredMM"],resultsForward["lowMassZPredErrMM"],resultsForward["lowMassZPredSF"],resultsForward["lowMassZPredErrSF"])

	predictionHighMassCentral = predictionTemplate%("high",resultsCentral["highMassZPredEE"],resultsCentral["highMassZPredErrEE"],resultsCentral["highMassZPredMM"],resultsCentral["highMassZPredErrMM"],resultsCentral["highMassZPredSF"],resultsCentral["highMassZPredErrSF"])
	predictionHighMassForward = predictionTemplate%("high",resultsForward["highMassZPredEE"],resultsForward["highMassZPredErrEE"],resultsForward["highMassZPredMM"],resultsForward["highMassZPredErrMM"],resultsForward["highMassZPredSF"],resultsForward["highMassZPredErrSF"])
	

	
	table = tableTemplate%(rOutInLowMassCentral,predictionLowMassCentral,rOutInHighMassCentral,predictionHighMassCentral,rOutInLowMassForward,predictionLowMassForward,rOutInHighMassForward,predictionHighMassForward)
	
	saveTable(table,"cutNCount_ZBkgs")		
	
	
def main():
	
	
	name = "cutAndCount"
	countingShelves = {"inclusive":readPickle(name,regionsToUse.signal.inclusive.name , runRanges.name),"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	
	#~ 
	#~ produceFinalTable(countingShelves,"SF")
	#~ produceFinalTable(countingShelves,"EE")
	#~ produceFinalTable(countingShelves,"MM")
#~ 
	#~ getDataCards(countingShelves,"SF")
	#~ getDataCards(countingShelves,"EE")
	#~ getDataCards(countingShelves,"MM")
	produceFlavSymTable(countingShelves)
	produceZTable(countingShelves)
main()

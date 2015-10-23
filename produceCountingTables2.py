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
tableColumnHeaders = {"default":"no b-tag requirement","geOneBTags":"$\geq$ 1 b-tagged jets","geTwoBTags":"$\geq$ 2 b-tagged jets"}


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
	
	results = {"central":getResults(shelves,"central",selection),"forward":getResults(shelves,"forward",selection)}
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
			outFile = open("dataCards/dataCard_%s_%s_%s_%s.txt"%(selection,region, etaRegion, combination), "w")
			outFile.write(result)
			outFile.close()		
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

	dyTemplate = r"            Drell--Yan          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%d\pm%d$ & $%d\pm%d$ & $%.1f\pm%.1f$  \\"+"\n"
	
	totalTemplate = r"            Total estimated          & $%d\pm%d$            & $%d\pm%d$      & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ \\"+"\n"

#~ tableHeaders = {"default":"being inclusive in the number of b-tagged jets","geOneBTags":"requiring at least one b-tagged jet","geTwoBTags":"requiring at least two b-tagged jets"}
#~ tableColumnHeaders = {"default":"no b-tag requirement","geOneBTags":"$\geq$ 1 b-tagged jets","geTwoBTags":"$\geq$ 2 b-tagged jets"}
	
	tables = []
	for selection in ["default","geOneBTags","geTwoBTags"]:
		
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
	
	for selection in ["default","geOneBTags","geTwoBTags"]:

		
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
	
	
def makeOverviewPlot(countingShelves,region):

	from helpers import createMyColors
	from defs import myColors
	colors = createMyColors()	

	
	resultsCentral = getResults(countingShelves,"central","default")
	resultsForward = getResults(countingShelves,"forward","default")
	resultsCentralGeOneBTags = getResults(countingShelves,"central","geOneBTags")
	resultsForwardGeOneBTags = getResults(countingShelves,"forward","geOneBTags")
	resultsCentralGeTwoBTags = getResults(countingShelves,"central","geTwoBTags")
	resultsForwardGeTwoBTags = getResults(countingShelves,"forward","geTwoBTags")
	
	
	histObs = ROOT.TH1F("histObs","histObs",30,0,30)
	
	histObs.SetMarkerColor(ROOT.kBlack)
	histObs.SetLineColor(ROOT.kBlack)
	histObs.SetMarkerStyle(20)
	
	histPred = ROOT.TH1F("histPred","histPred",30,0,30)
	histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",30,0,30)
	histDY = ROOT.TH1F("histDY","histDY",30,0,30)
	
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style=setTDRStyle()
	style.SetPadBottomMargin(0.275)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()	
	
	
	#~ observedCentral = observedTemplate%(resultsCentral["lowMass%s"%region],resultsCentral["belowZ%s"%region],resultsCentral["onZ%s"%region],resultsCentral["aboveZ%s"%region],resultsCentral["highMass%s"%region])
	
	
	histObs.SetBinContent(1,resultsCentral["lowMassSF"])
	histObs.SetBinContent(2,resultsCentral["belowZSF"])
	histObs.SetBinContent(3,resultsCentral["onZSF"])
	histObs.SetBinContent(4,resultsCentral["aboveZSF"])
	histObs.SetBinContent(5,resultsForward["highMassSF"])
	histObs.SetBinContent(6,resultsForward["lowMassSF"])
	histObs.SetBinContent(7,resultsForward["belowZSF"])
	histObs.SetBinContent(8,resultsForward["onZSF"])
	histObs.SetBinContent(9,resultsForward["aboveZSF"])
	histObs.SetBinContent(10,resultsForward["highMassSF"])
	histObs.SetBinContent(11,resultsCentralGeOneBTags["lowMassSF"])
	histObs.SetBinContent(12,resultsCentralGeOneBTags["belowZSF"])
	histObs.SetBinContent(13,resultsCentralGeOneBTags["onZSF"])
	histObs.SetBinContent(14,resultsCentralGeOneBTags["aboveZSF"])
	histObs.SetBinContent(15,resultsCentralGeOneBTags["highMassSF"])
	histObs.SetBinContent(16,resultsForwardGeOneBTags["lowMassSF"])
	histObs.SetBinContent(17,resultsForwardGeOneBTags["belowZSF"])
	histObs.SetBinContent(18,resultsForwardGeOneBTags["onZSF"])
	histObs.SetBinContent(19,resultsForwardGeOneBTags["aboveZSF"])
	histObs.SetBinContent(20,resultsForwardGeOneBTags["highMassSF"])	
	histObs.SetBinContent(21,resultsCentralGeTwoBTags["lowMassSF"])
	histObs.SetBinContent(22,resultsCentralGeTwoBTags["belowZSF"])
	histObs.SetBinContent(23,resultsCentralGeTwoBTags["onZSF"])
	histObs.SetBinContent(24,resultsCentralGeTwoBTags["aboveZSF"])
	histObs.SetBinContent(25,resultsCentralGeTwoBTags["highMassSF"])
	histObs.SetBinContent(26,resultsForwardGeTwoBTags["lowMassSF"])
	histObs.SetBinContent(27,resultsForwardGeTwoBTags["belowZSF"])
	histObs.SetBinContent(28,resultsForwardGeTwoBTags["onZSF"])
	histObs.SetBinContent(29,resultsForwardGeTwoBTags["aboveZSF"])
	histObs.SetBinContent(30,resultsForwardGeTwoBTags["highMassSF"])
	
	names = ["low-Mass central","below-Z central","on-Z central","above-Z central","high-Mass central","low-Mass forward","below-Z forward","on-Z forward","above-Z forward","high-Mass forward","low-Mass central","below-Z central","on-Z central","above-Z central","high-Mass central","low-Mass forward","below-Z forward","on-Z forward","above-Z forward","high-Mass forward","low-Mass central","below-Z central","on-Z central","above-Z central","high-Mass central","low-Mass forward","below-Z forward","on-Z forward","above-Z forward","high-Mass forward"]
	
	for index, name in enumerate(names):
	
		histObs.GetXaxis().SetBinLabel(index+1,name)
	
	
	histFlavSym.SetBinContent(1,resultsCentral["lowMassPredSF"])
	histFlavSym.SetBinContent(2,resultsCentral["belowZPredSF"])
	histFlavSym.SetBinContent(3,resultsCentral["onZPredSF"])
	histFlavSym.SetBinContent(4,resultsCentral["aboveZPredSF"])
	histFlavSym.SetBinContent(5,resultsForward["highMassPredSF"])
	histFlavSym.SetBinContent(6,resultsForward["lowMassPredSF"])
	histFlavSym.SetBinContent(7,resultsForward["belowZPredSF"])
	histFlavSym.SetBinContent(8,resultsForward["onZPredSF"])
	histFlavSym.SetBinContent(9,resultsForward["aboveZPredSF"])
	histFlavSym.SetBinContent(10,resultsForward["highMassPredSF"])
	histFlavSym.SetBinContent(11,resultsCentralGeOneBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(12,resultsCentralGeOneBTags["belowZPredSF"])
	histFlavSym.SetBinContent(13,resultsCentralGeOneBTags["onZPredSF"])
	histFlavSym.SetBinContent(14,resultsCentralGeOneBTags["aboveZPredSF"])
	histFlavSym.SetBinContent(15,resultsCentralGeOneBTags["highMassPredSF"])
	histFlavSym.SetBinContent(16,resultsForwardGeOneBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(17,resultsForwardGeOneBTags["belowZPredSF"])
	histFlavSym.SetBinContent(18,resultsForwardGeOneBTags["onZPredSF"])
	histFlavSym.SetBinContent(19,resultsForwardGeOneBTags["aboveZPredSF"])
	histFlavSym.SetBinContent(20,resultsForwardGeOneBTags["highMassPredSF"])	
	histFlavSym.SetBinContent(21,resultsCentralGeTwoBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(22,resultsCentralGeTwoBTags["belowZPredSF"])
	histFlavSym.SetBinContent(23,resultsCentralGeTwoBTags["onZPredSF"])
	histFlavSym.SetBinContent(24,resultsCentralGeTwoBTags["aboveZPredSF"])
	histFlavSym.SetBinContent(25,resultsCentralGeTwoBTags["highMassPredSF"])
	histFlavSym.SetBinContent(26,resultsForwardGeTwoBTags["lowMassPredSF"])
	histFlavSym.SetBinContent(27,resultsForwardGeTwoBTags["belowZPredSF"])
	histFlavSym.SetBinContent(28,resultsForwardGeTwoBTags["onZPredSF"])
	histFlavSym.SetBinContent(29,resultsForwardGeTwoBTags["aboveZPredSF"])
	histFlavSym.SetBinContent(30,resultsForwardGeTwoBTags["highMassPredSF"])
	
	histDY.SetBinContent(1,resultsCentral["lowMassZPredSF"])
	histDY.SetBinContent(2,resultsCentral["belowZZPredSF"])
	histDY.SetBinContent(3,resultsCentral["onZZPredSF"])
	histDY.SetBinContent(4,resultsCentral["aboveZZPredSF"])
	histDY.SetBinContent(5,resultsForward["highMassZPredSF"])
	histDY.SetBinContent(6,resultsForward["lowMassZPredSF"])
	histDY.SetBinContent(7,resultsForward["belowZZPredSF"])
	histDY.SetBinContent(8,resultsForward["onZZPredSF"])
	histDY.SetBinContent(9,resultsForward["aboveZZPredSF"])
	histDY.SetBinContent(10,resultsForward["highMassZPredSF"])
	histDY.SetBinContent(11,resultsCentralGeOneBTags["lowMassZPredSF"])
	histDY.SetBinContent(12,resultsCentralGeOneBTags["belowZZPredSF"])
	histDY.SetBinContent(13,resultsCentralGeOneBTags["onZZPredSF"])
	histDY.SetBinContent(14,resultsCentralGeOneBTags["aboveZZPredSF"])
	histDY.SetBinContent(15,resultsCentralGeOneBTags["highMassZPredSF"])
	histDY.SetBinContent(16,resultsForwardGeOneBTags["lowMassZPredSF"])
	histDY.SetBinContent(17,resultsForwardGeOneBTags["belowZZPredSF"])
	histDY.SetBinContent(18,resultsForwardGeOneBTags["onZZPredSF"])
	histDY.SetBinContent(19,resultsForwardGeOneBTags["aboveZZPredSF"])
	histDY.SetBinContent(20,resultsForwardGeOneBTags["highMassZPredSF"])	
	histDY.SetBinContent(21,resultsCentralGeTwoBTags["lowMassZPredSF"])
	histDY.SetBinContent(22,resultsCentralGeTwoBTags["belowZZPredSF"])
	histDY.SetBinContent(23,resultsCentralGeTwoBTags["onZZPredSF"])
	histDY.SetBinContent(24,resultsCentralGeTwoBTags["aboveZZPredSF"])
	histDY.SetBinContent(25,resultsCentralGeTwoBTags["highMassZPredSF"])
	histDY.SetBinContent(26,resultsForwardGeTwoBTags["lowMassZPredSF"])
	histDY.SetBinContent(27,resultsForwardGeTwoBTags["belowZZPredSF"])
	histDY.SetBinContent(28,resultsForwardGeTwoBTags["onZZPredSF"])
	histDY.SetBinContent(29,resultsForwardGeTwoBTags["aboveZZPredSF"])
	histDY.SetBinContent(30,resultsForwardGeTwoBTags["highMassZPredSF"])
	
	
	errGraph = ROOT.TGraphAsymmErrors()
	
	for i in range(1,histFlavSym.GetNbinsX()+1):
		errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histDY.GetBinContent(i))


	errGraph.SetPointError(1,0.5,0.5,resultsCentral["lowMassTotalPredErrSF"],resultsCentral["lowMassTotalPredErrSF"])
	errGraph.SetPointError(2,0.5,0.5,resultsCentral["belowZTotalPredErrSF"],resultsCentral["belowZTotalPredErrSF"])
	errGraph.SetPointError(3,0.5,0.5,resultsCentral["onZTotalPredErrSF"],resultsCentral["onZTotalPredErrSF"])
	errGraph.SetPointError(4,0.5,0.5,resultsCentral["aboveZTotalPredErrSF"],resultsCentral["aboveZTotalPredErrSF"])
	errGraph.SetPointError(5,0.5,0.5,resultsCentral["highMassTotalPredErrSF"],resultsCentral["highMassTotalPredErrSF"])
	errGraph.SetPointError(6,0.5,0.5,resultsForward["lowMassTotalPredErrSF"],resultsForward["lowMassTotalPredErrSF"])
	errGraph.SetPointError(7,0.5,0.5,resultsForward["belowZTotalPredErrSF"],resultsForward["belowZTotalPredErrSF"])
	errGraph.SetPointError(8,0.5,0.5,resultsForward["onZTotalPredErrSF"],resultsForward["onZTotalPredErrSF"])
	errGraph.SetPointError(9,0.5,0.5,resultsForward["aboveZTotalPredErrSF"],resultsForward["aboveZTotalPredErrSF"])
	errGraph.SetPointError(10,0.5,0.5,resultsForward["highMassTotalPredErrSF"],resultsForward["highMassTotalPredErrSF"])
	errGraph.SetPointError(11,0.5,0.5,resultsCentralGeOneBTags["lowMassTotalPredErrSF"],resultsCentralGeOneBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(12,0.5,0.5,resultsCentralGeOneBTags["belowZTotalPredErrSF"],resultsCentralGeOneBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(13,0.5,0.5,resultsCentralGeOneBTags["onZTotalPredErrSF"],resultsCentralGeOneBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(14,0.5,0.5,resultsCentralGeOneBTags["aboveZTotalPredErrSF"],resultsCentralGeOneBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(15,0.5,0.5,resultsCentralGeOneBTags["highMassTotalPredErrSF"],resultsCentralGeOneBTags["highMassTotalPredErrSF"])
	errGraph.SetPointError(16,0.5,0.5,resultsForwardGeOneBTags["lowMassTotalPredErrSF"],resultsForwardGeOneBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(17,0.5,0.5,resultsForwardGeOneBTags["belowZTotalPredErrSF"],resultsForwardGeOneBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(18,0.5,0.5,resultsForwardGeOneBTags["onZTotalPredErrSF"],resultsForwardGeOneBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(19,0.5,0.5,resultsForwardGeOneBTags["aboveZTotalPredErrSF"],resultsForwardGeOneBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(20,0.5,0.5,resultsForwardGeOneBTags["highMassTotalPredErrSF"],resultsForwardGeOneBTags["highMassTotalPredErrSF"])	
	errGraph.SetPointError(21,0.5,0.5,resultsCentralGeTwoBTags["lowMassTotalPredErrSF"],resultsCentralGeTwoBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(22,0.5,0.5,resultsCentralGeTwoBTags["belowZTotalPredErrSF"],resultsCentralGeTwoBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(23,0.5,0.5,resultsCentralGeTwoBTags["onZTotalPredErrSF"],resultsCentralGeTwoBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(24,0.5,0.5,resultsCentralGeTwoBTags["aboveZTotalPredErrSF"],resultsCentralGeTwoBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(25,0.5,0.5,resultsCentralGeTwoBTags["highMassTotalPredErrSF"],resultsCentralGeTwoBTags["highMassTotalPredErrSF"])
	errGraph.SetPointError(26,0.5,0.5,resultsForwardGeTwoBTags["lowMassTotalPredErrSF"],resultsForwardGeTwoBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(27,0.5,0.5,resultsForwardGeTwoBTags["belowZTotalPredErrSF"],resultsForwardGeTwoBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(28,0.5,0.5,resultsForwardGeTwoBTags["onZTotalPredErrSF"],resultsForwardGeTwoBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(29,0.5,0.5,resultsForwardGeTwoBTags["aboveZTotalPredErrSF"],resultsForwardGeTwoBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(30,0.5,0.5,resultsForwardGeTwoBTags["highMassTotalPredErrSF"],resultsForwardGeTwoBTags["highMassTotalPredErrSF"])

	errGraph.SetFillColor(myColors["MyBlue"])
	errGraph.SetFillStyle(3001)	

	histFlavSym.SetLineColor(ROOT.kBlue+3)
	histFlavSym.SetLineWidth(2)
	
	histDY.SetLineColor(ROOT.kGreen+3)
	histDY.SetFillColor(ROOT.kGreen+3)
	histDY.SetFillStyle(3002)


	#~ histFlavSym.SetFillColor(ROOT.kBlue-2)
	#~ histDY.SetFillColor(ROOT.kGreen+2)
	
	from ROOT import THStack
	
	stack = THStack()
	stack.Add(histDY)	
	stack.Add(histFlavSym)

	
	
	histObs.GetYaxis().SetRangeUser(0,65)
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

	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%"0.13")
	
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
	

	stack.Draw("samehist")
	errGraph.Draw("same02")
	
	histObs.Draw("pesame")
	
	leg.Draw("same")

	
	
	line1 = ROOT.TLine(10,0,10,40)
	line2 = ROOT.TLine(20,0,20,40)

	line1.SetLineColor(ROOT.kBlack)
	line2.SetLineColor(ROOT.kBlack)

	line1.SetLineWidth(2)
	line2.SetLineWidth(2)

	line1.Draw("same")
	line2.Draw("same")


	label = ROOT.TLatex()
	label.SetTextAlign(12)
	label.SetTextSize(0.04)
	label.SetTextColor(ROOT.kBlack)	
	
	
	label.DrawLatex(2,35,"Inclusive")
	label.DrawLatex(10.5,35,"N_{b-tagged jets} #geq 1")
	label.DrawLatex(20.5,35,"N_{b-tagged jets} #geq 2")

	plotPad.RedrawAxis()
	
	hCanvas.Print("edgeOverview.pdf")
	hCanvas.Print("edgeOverview.root")
def makeOverviewPlot2(countingShelves,region):

	from helpers import createMyColors
	from defs import myColors
	colors = createMyColors()	

	
	resultsCentral = getResults(countingShelves,"central","default")
	resultsForward = getResults(countingShelves,"forward","default")
	resultsCentralGeOneBTags = getResults(countingShelves,"central","geOneBTags")
	resultsForwardGeOneBTags = getResults(countingShelves,"forward","geOneBTags")
	resultsCentralGeTwoBTags = getResults(countingShelves,"central","geTwoBTags")
	resultsForwardGeTwoBTags = getResults(countingShelves,"forward","geTwoBTags")
	
	
	histObs = ROOT.TH1F("histObs","histObs",30,0,30)
	
	histObs.SetMarkerColor(ROOT.kBlack)
	histObs.SetLineColor(ROOT.kBlack)
	histObs.SetMarkerStyle(20)
	
	histPred = ROOT.TH1F("histPred","histPred",30,0,30)
	histFlavSym = ROOT.TH1F("histFlavSym","histFlavSym",30,0,30)
	histDY = ROOT.TH1F("histDY","histDY",30,0,30)
	
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style=setTDRStyle()
	style.SetPadBottomMargin(0.2)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()	
	
	
	#~ observedCentral = observedTemplate%(resultsCentral["lowMass%s"%region],resultsCentral["belowZ%s"%region],resultsCentral["onZ%s"%region],resultsCentral["aboveZ%s"%region],resultsCentral["highMass%s"%region])
	
	
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
	
	#~ names = ["low-Mass central","below-Z central","on-Z central","above-Z central","high-Mass central","low-Mass forward","below-Z forward","on-Z forward","above-Z forward","high-Mass forward","low-Mass central","below-Z central","on-Z central","above-Z central","high-Mass central","low-Mass forward","below-Z forward","on-Z forward","above-Z forward","high-Mass forward","low-Mass central","below-Z central","on-Z central","above-Z central","high-Mass central","low-Mass forward","below-Z forward","on-Z forward","above-Z forward","high-Mass forward"]
	names = ["#geq 0 b-tags c","#geq 1 b-tags c","#geq 1 b-tags c","#geq 0 b-tags f","#geq 1 b-tags f","#geq 2 b-tags f","#geq 0 b-tags c","#geq 1 b-tags c","#geq 1 b-tags c","#geq 0 b-tags f","#geq 1 b-tags f","#geq 2 b-tags f","#geq 0 b-tags c","#geq 1 b-tags c","#geq 1 b-tags c","#geq 0 b-tags f","#geq 1 b-tags f","#geq 2 b-tags f","#geq 0 b-tags c","#geq 1 b-tags c","#geq 1 b-tags c","#geq 0 b-tags f","#geq 1 b-tags f","#geq 2 b-tags f","#geq 0 b-tags c","#geq 1 b-tags c","#geq 1 b-tags c","#geq 0 b-tags f","#geq 1 b-tags f","#geq 2 b-tags f"]
	
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

#~ 
	#~ errGraph.SetPointError(1,0.5,0.5,resultsCentral["lowMassTotalPredErrSF"],resultsCentral["lowMassTotalPredErrSF"])
	#~ errGraph.SetPointError(2,0.5,0.5,resultsCentral["belowZTotalPredErrSF"],resultsCentral["belowZTotalPredErrSF"])
	#~ errGraph.SetPointError(3,0.5,0.5,resultsCentral["onZTotalPredErrSF"],resultsCentral["onZTotalPredErrSF"])
	#~ errGraph.SetPointError(4,0.5,0.5,resultsCentral["aboveZTotalPredErrSF"],resultsCentral["aboveZTotalPredErrSF"])
	#~ errGraph.SetPointError(5,0.5,0.5,resultsForward["highMassTotalPredErrSF"],resultsForward["highMassTotalPredErrSF"])
	#~ errGraph.SetPointError(6,0.5,0.5,resultsForward["lowMassTotalPredErrSF"],resultsForward["lowMassTotalPredErrSF"])
	#~ errGraph.SetPointError(7,0.5,0.5,resultsForward["belowZTotalPredErrSF"],resultsForward["belowZTotalPredErrSF"])
	#~ errGraph.SetPointError(8,0.5,0.5,resultsForward["onZTotalPredErrSF"],resultsForward["onZTotalPredErrSF"])
	#~ errGraph.SetPointError(9,0.5,0.5,resultsForward["aboveZTotalPredErrSF"],resultsForward["aboveZTotalPredErrSF"])
	#~ errGraph.SetPointError(10,0.5,0.5,resultsForward["highMassTotalPredErrSF"],resultsForward["highMassTotalPredErrSF"])
	#~ errGraph.SetPointError(11,0.5,0.5,resultsCentralGeOneBTags["lowMassTotalPredErrSF"],resultsCentralGeOneBTags["lowMassTotalPredErrSF"])
	#~ errGraph.SetPointError(12,0.5,0.5,resultsCentralGeOneBTags["belowZTotalPredErrSF"],resultsCentralGeOneBTags["belowZTotalPredErrSF"])
	#~ errGraph.SetPointError(13,0.5,0.5,resultsCentralGeOneBTags["onZTotalPredErrSF"],resultsCentralGeOneBTags["onZTotalPredErrSF"])
	#~ errGraph.SetPointError(14,0.5,0.5,resultsCentralGeOneBTags["aboveZTotalPredErrSF"],resultsCentralGeOneBTags["aboveZTotalPredErrSF"])
	#~ errGraph.SetPointError(15,0.5,0.5,resultsCentralGeOneBTags["highMassTotalPredErrSF"],resultsCentralGeOneBTags["highMassTotalPredErrSF"])
	#~ errGraph.SetPointError(16,0.5,0.5,resultsForwardGeOneBTags["lowMassTotalPredErrSF"],resultsForwardGeOneBTags["lowMassTotalPredErrSF"])
	#~ errGraph.SetPointError(17,0.5,0.5,resultsForwardGeOneBTags["belowZTotalPredErrSF"],resultsForwardGeOneBTags["belowZTotalPredErrSF"])
	#~ errGraph.SetPointError(18,0.5,0.5,resultsForwardGeOneBTags["onZTotalPredErrSF"],resultsForwardGeOneBTags["onZTotalPredErrSF"])
	#~ errGraph.SetPointError(19,0.5,0.5,resultsForwardGeOneBTags["aboveZTotalPredErrSF"],resultsForwardGeOneBTags["aboveZTotalPredErrSF"])
	#~ errGraph.SetPointError(20,0.5,0.5,resultsForwardGeOneBTags["highMassTotalPredErrSF"],resultsForwardGeOneBTags["highMassTotalPredErrSF"])	
	#~ errGraph.SetPointError(21,0.5,0.5,resultsCentralGeTwoBTags["lowMassTotalPredErrSF"],resultsCentralGeTwoBTags["lowMassTotalPredErrSF"])
	#~ errGraph.SetPointError(22,0.5,0.5,resultsCentralGeTwoBTags["belowZTotalPredErrSF"],resultsCentralGeTwoBTags["belowZTotalPredErrSF"])
	#~ errGraph.SetPointError(23,0.5,0.5,resultsCentralGeTwoBTags["onZTotalPredErrSF"],resultsCentralGeTwoBTags["onZTotalPredErrSF"])
	#~ errGraph.SetPointError(24,0.5,0.5,resultsCentralGeTwoBTags["aboveZTotalPredErrSF"],resultsCentralGeTwoBTags["aboveZTotalPredErrSF"])
	#~ errGraph.SetPointError(25,0.5,0.5,resultsCentralGeTwoBTags["highMassTotalPredErrSF"],resultsCentralGeTwoBTags["highMassTotalPredErrSF"])
	#~ errGraph.SetPointError(26,0.5,0.5,resultsForwardGeTwoBTags["lowMassTotalPredErrSF"],resultsForwardGeTwoBTags["lowMassTotalPredErrSF"])
	#~ errGraph.SetPointError(27,0.5,0.5,resultsForwardGeTwoBTags["belowZTotalPredErrSF"],resultsForwardGeTwoBTags["belowZTotalPredErrSF"])
	#~ errGraph.SetPointError(28,0.5,0.5,resultsForwardGeTwoBTags["onZTotalPredErrSF"],resultsForwardGeTwoBTags["onZTotalPredErrSF"])
	#~ errGraph.SetPointError(29,0.5,0.5,resultsForwardGeTwoBTags["aboveZTotalPredErrSF"],resultsForwardGeTwoBTags["aboveZTotalPredErrSF"])
	#~ errGraph.SetPointError(30,0.5,0.5,resultsForwardGeTwoBTags["highMassTotalPredErrSF"],resultsForwardGeTwoBTags["highMassTotalPredErrSF"])

	errGraph.SetPointError(1,0.5,0.5,resultsCentral["lowMassTotalPredErrSF"],resultsCentral["lowMassTotalPredErrSF"])
	errGraph.SetPointError(11,0.5,0.5,resultsCentralGeOneBTags["lowMassTotalPredErrSF"],resultsCentralGeOneBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(21,0.5,0.5,resultsCentralGeTwoBTags["lowMassTotalPredErrSF"],resultsCentralGeTwoBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(6,0.5,0.5,resultsForward["lowMassTotalPredErrSF"],resultsForward["lowMassTotalPredErrSF"])
	errGraph.SetPointError(16,0.5,0.5,resultsForwardGeOneBTags["lowMassTotalPredErrSF"],resultsForwardGeOneBTags["lowMassTotalPredErrSF"])
	errGraph.SetPointError(26,0.5,0.5,resultsForwardGeTwoBTags["lowMassTotalPredErrSF"],resultsForwardGeTwoBTags["lowMassTotalPredErrSF"])

	errGraph.SetPointError(3,0.5,0.5,resultsCentral["onZTotalPredErrSF"],resultsCentral["onZTotalPredErrSF"])
	errGraph.SetPointError(13,0.5,0.5,resultsCentralGeOneBTags["onZTotalPredErrSF"],resultsCentralGeOneBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(23,0.5,0.5,resultsCentralGeTwoBTags["onZTotalPredErrSF"],resultsCentralGeTwoBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(8,0.5,0.5,resultsForward["onZTotalPredErrSF"],resultsForward["onZTotalPredErrSF"])
	errGraph.SetPointError(18,0.5,0.5,resultsForwardGeOneBTags["onZTotalPredErrSF"],resultsForwardGeOneBTags["onZTotalPredErrSF"])
	errGraph.SetPointError(28,0.5,0.5,resultsForwardGeTwoBTags["onZTotalPredErrSF"],resultsForwardGeTwoBTags["onZTotalPredErrSF"])

	errGraph.SetPointError(5,0.5,0.5,resultsCentral["highMassTotalPredErrSF"],resultsCentral["highMassTotalPredErrSF"])
	errGraph.SetPointError(15,0.5,0.5,resultsCentralGeOneBTags["highMassTotalPredErrSF"],resultsCentralGeOneBTags["highMassTotalPredErrSF"])
	errGraph.SetPointError(25,0.5,0.5,resultsCentralGeTwoBTags["highMassTotalPredErrSF"],resultsCentralGeTwoBTags["highMassTotalPredErrSF"])
	errGraph.SetPointError(10,0.5,0.5,resultsForward["highMassTotalPredErrSF"],resultsForward["highMassTotalPredErrSF"])
	errGraph.SetPointError(20,0.5,0.5,resultsForwardGeOneBTags["highMassTotalPredErrSF"],resultsForwardGeOneBTags["highMassTotalPredErrSF"])	
	errGraph.SetPointError(30,0.5,0.5,resultsForwardGeTwoBTags["highMassTotalPredErrSF"],resultsForwardGeTwoBTags["highMassTotalPredErrSF"])
		
	errGraph.SetPointError(2,0.5,0.5,resultsCentral["belowZTotalPredErrSF"],resultsCentral["belowZTotalPredErrSF"])
	errGraph.SetPointError(12,0.5,0.5,resultsCentralGeOneBTags["belowZTotalPredErrSF"],resultsCentralGeOneBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(22,0.5,0.5,resultsCentralGeTwoBTags["belowZTotalPredErrSF"],resultsCentralGeTwoBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(7,0.5,0.5,resultsForward["belowZTotalPredErrSF"],resultsForward["belowZTotalPredErrSF"])
	errGraph.SetPointError(17,0.5,0.5,resultsForwardGeOneBTags["belowZTotalPredErrSF"],resultsForwardGeOneBTags["belowZTotalPredErrSF"])
	errGraph.SetPointError(27,0.5,0.5,resultsForwardGeTwoBTags["belowZTotalPredErrSF"],resultsForwardGeTwoBTags["belowZTotalPredErrSF"])
	
	errGraph.SetPointError(4,0.5,0.5,resultsCentral["aboveZTotalPredErrSF"],resultsCentral["aboveZTotalPredErrSF"])
	errGraph.SetPointError(9,0.5,0.5,resultsForward["aboveZTotalPredErrSF"],resultsForward["aboveZTotalPredErrSF"])
	errGraph.SetPointError(14,0.5,0.5,resultsCentralGeOneBTags["aboveZTotalPredErrSF"],resultsCentralGeOneBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(19,0.5,0.5,resultsForwardGeOneBTags["aboveZTotalPredErrSF"],resultsForwardGeOneBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(24,0.5,0.5,resultsCentralGeTwoBTags["aboveZTotalPredErrSF"],resultsCentralGeTwoBTags["aboveZTotalPredErrSF"])
	errGraph.SetPointError(29,0.5,0.5,resultsForwardGeTwoBTags["aboveZTotalPredErrSF"],resultsForwardGeTwoBTags["aboveZTotalPredErrSF"])

	errGraph.SetFillColor(myColors["MyBlue"])
	errGraph.SetFillStyle(3001)	

	histFlavSym.SetLineColor(ROOT.kBlue+3)
	histFlavSym.SetLineWidth(2)
	
	histDY.SetLineColor(ROOT.kGreen+3)
	histDY.SetFillColor(ROOT.kGreen+3)
	histDY.SetFillStyle(3002)


	#~ histFlavSym.SetFillColor(ROOT.kBlue-2)
	#~ histDY.SetFillColor(ROOT.kGreen+2)
	
	from ROOT import THStack
	
	stack = THStack()
	stack.Add(histDY)	
	stack.Add(histFlavSym)

	
	
	histObs.GetYaxis().SetRangeUser(0,70)
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

	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%"0.13")
	
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
	

	stack.Draw("samehist")
	errGraph.Draw("same02")
	
	histObs.Draw("pesame")
	
	leg.Draw("same")

	
	
	line1 = ROOT.TLine(6,0,6,40)
	line2 = ROOT.TLine(12,0,12,40)
	line3 = ROOT.TLine(18,0,18,40)
	line4 = ROOT.TLine(24,0,24,40)

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
	
	line5 = ROOT.TLine(3,0,3,25)
	line6 = ROOT.TLine(9,0,9,25)
	line7 = ROOT.TLine(15,0,15,25)
	line8 = ROOT.TLine(21,0,21,25)
	line9 = ROOT.TLine(27,0,27,25)

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
	
	label.DrawLatex(1,30,"low-mass")
	label.DrawLatex(7,30,"on-Z")
	label.DrawLatex(13,30,"high-mass")
	label.DrawLatex(19,30,"below-Z")
	label.DrawLatex(25,30,"above-Z")


	plotPad.RedrawAxis()
	
	hCanvas.Print("edgeOverview_newSort.pdf")
	hCanvas.Print("edgeOverview_newSort.root")

	
def main():
	
	
	name = "cutAndCount"
	countingShelves = {"inclusive":readPickle(name,regionsToUse.signal.inclusive.name , runRanges.name),"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	
	

	
	produceFinalTable(countingShelves,"SF")
	produceFinalTable(countingShelves,"EE")
	produceFinalTable(countingShelves,"MM")
	#~ 
		#~ getDataCards(countingShelves,"SF",selection)
		#~ getDataCards(countingShelves,"EE",selection)
		#~ getDataCards(countingShelves,"MM",selection)
	produceFlavSymTable(countingShelves)
		#~ produceZTable(countingShelves,selection)
	makeOverviewPlot(countingShelves,"SF")	
	makeOverviewPlot2(countingShelves,"SF")	
main()

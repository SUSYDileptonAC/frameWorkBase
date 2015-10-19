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


def produceFinalTable(shelves,region,selection):
	
	
	
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\tiny
 \centering
 \caption{Results of the edge-search counting experiment for event yields in the signal regions, %s.
     The statistical and systematic uncertainties are added in quadrature, except for the flavor-symmetric backgrounds.
     Low-mass refers to 20 $<$ \mll $<$ 70\GeV, below-\Z to 71 $<$ \mll $<$ 81\GeV, on-\Z to  81 $<$ \mll $<$ 101\GeV, above-\Z to 81 $<$ \mll $<$ 120\GeV and high-mass to \mll $>$ 120\GeV.
     }
  \label{tab:edgeResults%s}
  \\begin{tabular}{l| cc | cc | cc | cc | cc}
    \hline
    \hline
     & \multicolumn{10}{c}{%s} \\\\ \n
    \hline    
    							& \multicolumn{2}{c}{Low-mass} & \multicolumn{2}{c}{below-\Z} & \multicolumn{2}{c}{On-\Z} & \multicolumn{2}{c}{above-\Z} & \multicolumn{2}{c}{High-mass} \\\\ \n
    \hline
                                &  Central        & Forward  &  Central  & Forward   &  Central        & Forward &  Central        & Forward &  Central        & Forward \\\\ \n
    \hline
%s
    \hline
%s
%s
    \hline
%s
   \hline
    \hline
  \end{tabular}
\end{table}


"""

	observedTemplate = r"        Observed       &  %d                   & %d              &  %d            &  %d       &   %d           &   %d &   %d           &   %d &   %d           &   %d    \\" +"\n"

	flavSysmTemplate = r"        Flavor-symmetric    & $%d\pm%d\pm%d$        & $%d\pm%d\pm%d$  &  $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ \\"+"\n"

	dyTemplate = r"            Drell--Yan          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%d\pm%d$ & $%d\pm%d$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ \\"+"\n"
	
	totalTemplate = r"            Total estimated          & $%d\pm%d$            & $%d\pm%d$      & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ \\"+"\n"


	
	
	resultsCentral = getResults(shelves,"central",selection)
	resultsForward = getResults(shelves,"forward",selection)

	observed = observedTemplate%(resultsCentral["lowMass%s"%region],resultsForward["lowMass%s"%region],resultsCentral["belowZ%s"%region],resultsForward["belowZ%s"%region],resultsCentral["onZ%s"%region],resultsForward["onZ%s"%region],resultsCentral["aboveZ%s"%region],resultsForward["aboveZ%s"%region],resultsCentral["highMass%s"%region],resultsForward["highMass%s"%region])
	
	flavSym = flavSysmTemplate%(resultsCentral["lowMassPred%s"%region],resultsCentral["lowMassPredStatErr%s"%region],resultsCentral["lowMassPredSystErr%s"%region],resultsForward["lowMassPred%s"%region],resultsForward["lowMassPredStatErr%s"%region],resultsForward["lowMassPredSystErr%s"%region],resultsCentral["belowZPred%s"%region],resultsCentral["belowZPredStatErr%s"%region],resultsCentral["belowZPredSystErr%s"%region],resultsForward["belowZPred%s"%region],resultsForward["belowZPredStatErr%s"%region],resultsForward["belowZPredSystErr%s"%region],resultsCentral["onZPred%s"%region],resultsCentral["onZPredStatErr%s"%region],resultsCentral["onZPredSystErr%s"%region],resultsForward["onZPred%s"%region],resultsForward["onZPredStatErr%s"%region],resultsForward["onZPredSystErr%s"%region],resultsCentral["aboveZPred%s"%region],resultsCentral["aboveZPredStatErr%s"%region],resultsCentral["aboveZPredSystErr%s"%region],resultsForward["aboveZPred%s"%region],resultsForward["aboveZPredStatErr%s"%region],resultsForward["aboveZPredSystErr%s"%region],resultsCentral["highMassPred%s"%region],resultsCentral["highMassPredStatErr%s"%region],resultsCentral["highMassPredSystErr%s"%region],resultsForward["highMassPred%s"%region],resultsForward["highMassPredStatErr%s"%region],resultsForward["highMassPredSystErr%s"%region])
	
	dy = dyTemplate%(resultsCentral["lowMassZPred%s"%region],resultsCentral["lowMassZPredErr%s"%region],resultsForward["lowMassZPred%s"%region],resultsForward["lowMassZPredErr%s"%region],resultsCentral["belowZZPred%s"%region],resultsCentral["belowZZPredErr%s"%region],resultsForward["belowZZPred%s"%region],resultsForward["belowZZPredErr%s"%region],resultsCentral["onZZPred%s"%region],resultsCentral["onZZPredErr%s"%region],resultsForward["onZZPred%s"%region],resultsForward["onZZPredErr%s"%region],resultsCentral["aboveZZPred%s"%region],resultsCentral["aboveZZPredErr%s"%region],resultsForward["aboveZZPred%s"%region],resultsForward["aboveZZPredErr%s"%region],resultsCentral["highMassZPred%s"%region],resultsCentral["highMassZPredErr%s"%region],resultsForward["highMassZPred%s"%region],resultsForward["highMassZPredErr%s"%region])
	
	total = totalTemplate%(resultsCentral["lowMassTotalPred%s"%region],resultsCentral["lowMassTotalPredErr%s"%region],resultsForward["lowMassTotalPred%s"%region],resultsForward["lowMassTotalPredErr%s"%region],resultsCentral["belowZTotalPred%s"%region],resultsCentral["belowZTotalPredErr%s"%region],resultsForward["belowZTotalPred%s"%region],resultsForward["belowZTotalPredErr%s"%region],resultsCentral["onZTotalPred%s"%region],resultsCentral["onZTotalPredErr%s"%region],resultsForward["onZTotalPred%s"%region],resultsForward["onZTotalPredErr%s"%region],resultsCentral["aboveZTotalPred%s"%region],resultsCentral["aboveZTotalPredErr%s"%region],resultsForward["aboveZTotalPred%s"%region],resultsForward["aboveZTotalPredErr%s"%region],resultsCentral["highMassTotalPred%s"%region],resultsCentral["highMassTotalPredErr%s"%region],resultsForward["highMassTotalPred%s"%region],resultsForward["highMassTotalPredErr%s"%region])

	table = tableTemplate%(tableHeaders[selection],selection,tableColumnHeaders[selection],observed,flavSym,dy,total)
	
	saveTable(table,"cutNCount_Result_%s_%s"%(selection,region))
	
	
	


def produceFlavSymTable(shelves,selection):
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\tiny
 \centering
 \caption{Resulting estimates for flavour-symmetric backgrounds, %s. Given is the observed event yield in \EM events and the resulting estimate after applying the correction, seperately for the SF, \EE, and \MM channels. Statistical and systematic uncertainties are given separately.
     Low-mass refers to 20 $<$ \mll $<$ 70\GeV, below-\Z to 71 $<$ \mll $<$ 81\GeV, on-\Z to  81 $<$ \mll $<$ 101\GeV, above-\Z to 81 $<$ \mll $<$ 120\GeV and high-mass to \mll $>$ 120\GeV.
     }
  \label{tab:FlavSymBackgrounds}
  \\begin{tabular}{l| cc | cc | cc | cc | cc}
    \hline
    \hline
     & \multicolumn{10}{c}{%s} \\\\ \n
    \hline
    							& \multicolumn{2}{c}{Low-mass} & \multicolumn{2}{c}{below-\Z} & \multicolumn{2}{c}{On-\Z} & \multicolumn{2}{c}{above-\Z} & \multicolumn{2}{c}{High-mass} \\\\ \n
    \hline
                                &  Central        & Forward  &  Central  & Forward   &  Central        & Forward &  Central        & Forward &  Central        & Forward \\\\ \n
    \hline
%s
    \hline
%s
%s
%s

  \end{tabular}
\end{table}


"""

	observedTemplate = r"        Observed OF events       &  %d                   & %d              &  %d            &  %d       &   %d           &   %d &   %d           &   %d &   %d           &   %d    \\" +"\n"

	flavSysmTemplate = r"        Estimate in %s channel    & $%d\pm%d\pm%d$        & $%d\pm%d\pm%d$  &  $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ & $%d\pm%d\pm%d$ \\"+"\n"



	
	
	resultsCentral = getResults(shelves,"central",selection)
	resultsForward = getResults(shelves,"forward",selection)
	observed = observedTemplate%(resultsCentral["lowMassOF"],resultsForward["lowMassOF"],resultsCentral["belowZOF"],resultsForward["belowZOF"],resultsCentral["onZOF"],resultsForward["onZOF"],resultsCentral["aboveZOF"],resultsForward["aboveZOF"],resultsCentral["highMassOF"],resultsForward["highMassOF"])

	
	flavSymSF = flavSysmTemplate%("SF",resultsCentral["lowMassPredSF"],resultsCentral["lowMassPredStatErrSF"],resultsCentral["lowMassPredSystErrSF"],resultsForward["lowMassPredSF"],resultsForward["lowMassPredStatErrSF"],resultsForward["lowMassPredSystErrSF"],resultsCentral["belowZPredSF"],resultsCentral["belowZPredStatErrSF"],resultsCentral["belowZPredSystErrSF"],resultsForward["belowZPredSF"],resultsForward["belowZPredStatErrSF"],resultsForward["belowZPredSystErrSF"],resultsCentral["onZPredSF"],resultsCentral["onZPredStatErrSF"],resultsCentral["onZPredSystErrSF"],resultsForward["onZPredSF"],resultsForward["onZPredStatErrSF"],resultsForward["onZPredSystErrSF"],resultsCentral["aboveZPredSF"],resultsCentral["aboveZPredStatErrSF"],resultsCentral["aboveZPredSystErrSF"],resultsForward["aboveZPredSF"],resultsForward["aboveZPredStatErrSF"],resultsForward["aboveZPredSystErrSF"],resultsCentral["highMassPredSF"],resultsCentral["highMassPredStatErrSF"],resultsCentral["highMassPredSystErrSF"],resultsForward["highMassPredSF"],resultsForward["highMassPredStatErrSF"],resultsForward["highMassPredSystErrSF"])
	flavSymEE = flavSysmTemplate%("EE",resultsCentral["lowMassPredEE"],resultsCentral["lowMassPredStatErrEE"],resultsCentral["lowMassPredSystErrEE"],resultsForward["lowMassPredEE"],resultsForward["lowMassPredStatErrEE"],resultsForward["lowMassPredSystErrEE"],resultsCentral["belowZPredEE"],resultsCentral["belowZPredStatErrEE"],resultsCentral["belowZPredSystErrEE"],resultsForward["belowZPredEE"],resultsForward["belowZPredStatErrEE"],resultsForward["belowZPredSystErrEE"],resultsCentral["onZPredEE"],resultsCentral["onZPredStatErrEE"],resultsCentral["onZPredSystErrEE"],resultsForward["onZPredEE"],resultsForward["onZPredStatErrEE"],resultsForward["onZPredSystErrEE"],resultsCentral["aboveZPredEE"],resultsCentral["aboveZPredStatErrEE"],resultsCentral["aboveZPredSystErrEE"],resultsForward["aboveZPredEE"],resultsForward["aboveZPredStatErrEE"],resultsForward["aboveZPredSystErrEE"],resultsCentral["highMassPredEE"],resultsCentral["highMassPredStatErrEE"],resultsCentral["highMassPredSystErrEE"],resultsForward["highMassPredEE"],resultsForward["highMassPredStatErrEE"],resultsForward["highMassPredSystErrEE"])
	flavSymMM = flavSysmTemplate%("MM",resultsCentral["lowMassPredMM"],resultsCentral["lowMassPredStatErrMM"],resultsCentral["lowMassPredSystErrMM"],resultsForward["lowMassPredMM"],resultsForward["lowMassPredStatErrMM"],resultsForward["lowMassPredSystErrMM"],resultsCentral["belowZPredMM"],resultsCentral["belowZPredStatErrMM"],resultsCentral["belowZPredSystErrMM"],resultsForward["belowZPredMM"],resultsForward["belowZPredStatErrMM"],resultsForward["belowZPredSystErrMM"],resultsCentral["onZPredMM"],resultsCentral["onZPredStatErrMM"],resultsCentral["onZPredSystErrMM"],resultsForward["onZPredMM"],resultsForward["onZPredStatErrMM"],resultsForward["onZPredSystErrMM"],resultsCentral["aboveZPredMM"],resultsCentral["aboveZPredStatErrMM"],resultsCentral["aboveZPredSystErrMM"],resultsForward["aboveZPredMM"],resultsForward["aboveZPredStatErrMM"],resultsForward["aboveZPredSystErrMM"],resultsCentral["highMassPredMM"],resultsCentral["highMassPredStatErrMM"],resultsCentral["highMassPredSystErrMM"],resultsForward["highMassPredMM"],resultsForward["highMassPredStatErrMM"],resultsForward["highMassPredSystErrMM"])



	table = tableTemplate%(tableHeaders[selection],tableColumnHeaders[selection],observed,flavSymSF,flavSymEE,flavSymMM)
	
	saveTable(table,"cutNCount_FlavSymBkgs_%s"%selection)	
	
	
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
	countingShelves = {"inclusive":readPickle(name,regionsToUse.signal.inclusive.name , runRanges.name),"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	
	
	for selection in ["default","geOneBTags","geTwoBTags"]:
	
		produceFinalTable(countingShelves,"SF",selection)
		produceFinalTable(countingShelves,"EE",selection)
		produceFinalTable(countingShelves,"MM",selection)
	#~ 
		#~ getDataCards(countingShelves,"SF",selection)
		#~ getDataCards(countingShelves,"EE",selection)
		#~ getDataCards(countingShelves,"MM",selection)
		produceFlavSymTable(countingShelves,selection)
		produceZTable(countingShelves,selection)
main()

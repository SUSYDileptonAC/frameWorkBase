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

	
def getResults(shelve,region,label):
	
	result = {}
	

	
	result["lowMassSF"] = shelve[region][label]["edgeMass"]["EE"] + shelve[region][label]["edgeMass"]["MM"]
	result["lowMassOF"] = shelve[region][label]["edgeMass"]["EM"]
	
	result["lowMassPredSF"] = result["lowMassOF"]*getattr(rSFOF,region).val
	result["lowMassPredStatErrSF"] = result["lowMassOF"]**0.5*getattr(rSFOF,region).val
	result["lowMassPredSystErrSF"] = result["lowMassOF"]*getattr(rSFOF,region).err


	result["onZSF"] = shelve[region][label]["zMass"]["EE"] + shelve[region][label]["zMass"]["MM"]
	result["onZOF"] = shelve[region][label]["zMass"]["EM"]		
	
	result["lowMassZPredSF"] = (result["onZSF"] - result["onZOF"]*getattr(rSFOF,region).val)*getattr(rOutIn.lowMass,region).val
	result["lowMassZPredErrSF"] = (((result["onZSF"] - result["onZOF"]*getattr(rSFOF,region).val)*getattr(rOutIn.lowMass,region).err)**2 + ((result["onZSF"] - result["onZOF"])*0.25*getattr(rOutIn.lowMass,region).val)**2 )**0.5
	
	
	result["lowMassTotalPredSF"] = result["lowMassPredSF"] + result["lowMassZPredSF"]
	result["lowMassTotalPredErrSF"] = ( result["lowMassPredStatErrSF"]**2 +  result["lowMassPredSystErrSF"]**2 + result["lowMassZPredErrSF"]**2 )**0.5
	
	result["signal"] = result["lowMassSF"] - result["lowMassTotalPredSF"]
	result["signalErr"] = (result["lowMassSF"] + result["lowMassTotalPredErrSF"]**2)**0.5
	
	
	return result


def produceCrosscheckTable(shelves,region):
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \centering
 \caption{Results of the counting experiment in the low-mass central signal region for different variations of the event selection. The observed event yield in SF events is compared with the combined estimate from flavour-symmetric and Drell--Yan backgrounds. The estimate for the Drell--Yan backgrounds is obtained by extrapolating the event yield in the on-Z signal region after subtraction of flavour-symmetric backgrounds to the low-mass region using the \Routin factor.}
  \label{tab:CountingCrosschecks}
  \\begin{tabular}{l|c|c|c|c}
                                &  SF        & Flavour-symmetric  &  Drell--Yan  & Observed - Estimates \\\\ \n
    \hline
    \hline
%s

  \end{tabular}
\end{table}


"""

	lineTemplate = r"        %s       &  %d                   & %.1f$\pm$%.1f              &  %.1f$\pm$%.1f            &  %.1f$\pm$%.1f \\" +"\n"




	table = ""
	
	table += " & \multicolumn{4}{c}{b tagging}\\\\ \n"
	table += "\hline \n"
	result =  getResults(shelves,region,"noBTags")
	table += lineTemplate%("no b-tags",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	result =  getResults(shelves,region,"geOneBTags")
	table += lineTemplate%("$\geq$ 1 b-tags",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	table += "\hline \n"
	
	table += " & \multicolumn{4}{c}{lepton \pt requirement} \\\\ \n"
	table += "\hline \n"
	result =  getResults(shelves,region,"pt2010")
	table += lineTemplate%("\pt > 20(10)\GeV",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	result =  getResults(shelves,region,"pt3010")
	table += lineTemplate%("\pt > 30(10)\GeV",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	result =  getResults(shelves,region,"pt3020")
	table += lineTemplate%("\pt > 30(20)\GeV",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	result =  getResults(shelves,region,"pt3030")
	table += lineTemplate%("\pt > 30\GeV",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	table += "\hline \n"
	
	table += " & \multicolumn{4}{c}{tight lepton isolation} \\\\ \n"
	table += "\hline \n"
	result =  getResults(shelves,region,"TightIso")
	table += lineTemplate%("rel. isolation < 0.05",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	table += "\hline \n"
	

	table += " & \multicolumn{4}{c}{pileup} \\\\ \n"
	table += "\hline \n"
	result =  getResults(shelves,region,"lowPU")
	table += lineTemplate%("$N_{\\text{vtx}} <$ 13",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	result =  getResults(shelves,region,"midPU")
	table += lineTemplate%("13 $\leq N_{\\text{vtx}}$ < 17",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	result =  getResults(shelves,region,"highPU")
	table += lineTemplate%("$N_{\\text{vtx}} \geq$ 17",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	table += "\hline \n"
	
	#~ table += " & \multicolumn{4}{c}{\MET reconstructions}\\\\\n"
	#~ table += "\hline \n"
	#~ result =  getResults(shelves,region,"caloMet")
	#~ table += lineTemplate%("Calo \MET",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	#~ result =  getResults(shelves,region,"type1Met")
	#~ table += lineTemplate%("type I corrected PF \MET",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	#~ result =  getResults(shelves,region,"tcMet")
	#~ table += lineTemplate%("track corrected \MET",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	#~ result =  getResults(shelves,region,"mht")
	#~ table += lineTemplate%("missing $H_{\mathrm{T}}$",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	#~ table += "\hline \n"
	
	
	table += " & \multicolumn{4}{c}{$H_{\mathrm{T}}$}\\\\\n"
	table += "\hline \n"
	result =  getResults(shelves,region,"ht100to300")
	table += lineTemplate%("100\GeV $< H_{\mathrm{T}} < $ 300\GeV ",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )
	result =  getResults(shelves,region,"ht300")
	table += lineTemplate%("$H_{\mathrm{T}} > $ 300\GeV ",result["lowMassSF"],result["lowMassPredSF"],(result["lowMassPredStatErrSF"]**2 + result["lowMassPredSystErrSF"]**2)**0.5, result["lowMassZPredSF"], result["lowMassZPredErrSF"] , result["signal"], result["signalErr"] )	
	table += "\hline \n"
	

	
	saveTable(tableTemplate%table,"cutNCount_CrossChecks_%s"%region)
	
	

	
	
def main():
	
	
	name = "cutAndCount"
	countingShelves = {"inclusive":readPickle(name,regionsToUse.signal.inclusive.name , runRanges.name),"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	
	produceCrosscheckTable(countingShelves,"central")
	produceCrosscheckTable(countingShelves,"forward")
main()

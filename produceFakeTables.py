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
		if os.path.isfile("shelves/%s_%s_%s_MC"%(name,regionName,runName)):
			result = pickle.load(open("shelves/%s_%s_%s_MC"%(name,regionName,runName),"rb"))
		else:
			print "shelves/%s_%s_%s.pkl not found, exiting"%(name,regionName,runName) 		
			sys.exit()		
	else:
		if os.path.isfile("shelves/%s_%s_%s"%(name,regionName,runName)):
			result = pickle.load(open("shelves/%s_%s_%s"%(name,regionName,runName),"rb"))
		else:
			print "shelves/%s_%s_%s not found, exiting"%(name,regionName,runName) 		
			sys.exit()

	return result	

	
	
	
def produceMCTable(shelves):
	
	tableTemplate = r"""
\begin{table}[!htbp]
 \renewcommand{\arraystretch}{1.2}
 \begin{center}
  \caption{Number of events with non-prompt leptons in an inclusive dilepton selection and the central and forward signal regions for \ttbar simulation.}
  \begin{tabular}{l|ccccc}
   \hline
   \hline
                                    & \EE & \MM & SF & \EM    & \Rsfof        \\
   \hline
%s
 \end{tabular}
 \label{tab:nonPromptTableMC}
 \end{center}
\end{table}
"""
	


	template = r"       %s      &  %.1f$\pm$%.1f  & %.1f$\pm$%.1f & %.1f$\pm$%.1f  & %.1f$\pm$%.1f          &  %.2f$\pm$%.2f    \\" +"\n"


	table = ""

	table += template%("Inclusive",shelves["inclusive"]["nEEScaled"],shelves["inclusive"]["nEEScaledErr"],shelves["inclusive"]["nMMScaled"],shelves["inclusive"]["nMMScaledErr"],shelves["inclusive"]["nEEScaled"]+shelves["inclusive"]["nMMScaled"],shelves["inclusive"]["nEEScaledErr"]+shelves["inclusive"]["nMMScaledErr"],shelves["inclusive"]["nEMScaled"],shelves["inclusive"]["nEMScaledErr"],(shelves["inclusive"]["nEEScaled"]+shelves["inclusive"]["nMMScaled"])/shelves["inclusive"]["nEMScaled"],(shelves["inclusive"]["nEEScaled"]+shelves["inclusive"]["nMMScaled"])/shelves["inclusive"]["nEMScaled"]*(((shelves["inclusive"]["nEEScaledErr"]+shelves["inclusive"]["nMMScaledErr"])/(shelves["inclusive"]["nEEScaled"]+shelves["inclusive"]["nMMScaled"]))**2+(shelves["inclusive"]["nEMScaledErr"]/shelves["inclusive"]["nEMScaled"])**2)**0.5)
	table += template%("Signal central",shelves["central"]["nEEScaled"],shelves["central"]["nEEScaledErr"],shelves["central"]["nMMScaled"],shelves["central"]["nMMScaledErr"],shelves["central"]["nEEScaled"]+shelves["central"]["nMMScaled"],shelves["central"]["nEEScaledErr"]+shelves["central"]["nMMScaledErr"],shelves["central"]["nEMScaled"],shelves["central"]["nEMScaledErr"],(shelves["central"]["nEEScaled"]+shelves["central"]["nMMScaled"])/shelves["central"]["nEMScaled"],(shelves["central"]["nEEScaled"]+shelves["central"]["nMMScaled"])/shelves["central"]["nEMScaled"]*(((shelves["central"]["nEEScaledErr"]+shelves["central"]["nMMScaledErr"])/(shelves["central"]["nEEScaled"]+shelves["central"]["nMMScaled"]))**2+(shelves["central"]["nEMScaledErr"]/shelves["central"]["nEMScaled"])**2)**0.5)
	table += template%("Signal forward",shelves["forward"]["nEEScaled"],shelves["forward"]["nEEScaledErr"],shelves["forward"]["nMMScaled"],shelves["forward"]["nMMScaledErr"],shelves["forward"]["nEEScaled"]+shelves["forward"]["nMMScaled"],shelves["forward"]["nEEScaledErr"]+shelves["forward"]["nMMScaledErr"],shelves["forward"]["nEMScaled"],shelves["forward"]["nEMScaledErr"],(shelves["forward"]["nEEScaled"]+shelves["forward"]["nMMScaled"])/shelves["forward"]["nEMScaled"],(shelves["forward"]["nEEScaled"]+shelves["forward"]["nMMScaled"])/shelves["forward"]["nEMScaled"]*(((shelves["forward"]["nEEScaledErr"]+shelves["forward"]["nMMScaledErr"])/(shelves["forward"]["nEEScaled"]+shelves["forward"]["nMMScaled"]))**2+(shelves["forward"]["nEMScaledErr"]/shelves["forward"]["nEMScaled"])**2)**0.5)


	
	
	saveTable(tableTemplate%table,"nonPromptMC")		
	
def produceDataTable(shelves):
	
	tableTemplate = r"""
\begin{table}[!htbp]
 \renewcommand{\arraystretch}{1.2}
 \begin{center}
  \caption{Results of the estimation of backgrounds with non-prompt leptons using the tight-to-loose ratio.}
  \begin{tabular}{l|ccccc}
   \hline
   \hline
                                    & \EE & \MM & SF & \EM          \\
   \hline
   & \multicolumn{4}{|c}{Signal central} \\
   \hline
%s
\hline
%s
\hline
\hline
   
   & \multicolumn{4}{|c}{Signal forward} \\
   \hline
%s
\hline
%s
 \end{tabular}
 \label{tab:nonPromptTable}
 \end{center}
\end{table}
"""
	


	template = r"       %s      &  %.1f$\pm$%.1f$\pm$%.1f  & %.1f$\pm$%.1f$\pm$%.1f & %.1f$\pm$%.1f$\pm$%.1f  & %.1f$\pm$%.1f$\pm$%.1f             \\" +"\n"
	templateRaw = r"       %s      &  %d  & %d & %d  & %d             \\" +"\n"


	tableRawCentral = ""
	tableCentral = ""
	tableRawForward = ""
	tableForward = ""
	
	tableRawCentral += templateRaw%("$N_{tt}$",shelves["central"]["EE"]["nTT"],shelves["central"]["MM"]["nTT"],shelves["central"]["EE"]["nTT"]+shelves["central"]["MM"]["nTT"],shelves["central"]["EM"]["nTT"])
	tableRawCentral += templateRaw%("$N_{lt}$ + $N_{tl}$",shelves["central"]["EE"]["nTL"]+shelves["central"]["EE"]["nLT"],shelves["central"]["MM"]["nTL"]+shelves["central"]["MM"]["nLT"],shelves["central"]["EE"]["nTL"]+shelves["central"]["EE"]["nLT"]+shelves["central"]["MM"]["nTL"]+shelves["central"]["MM"]["nLT"],shelves["central"]["EM"]["nTL"]+shelves["central"]["EE"]["nLT"])
	tableRawCentral += templateRaw%("$N_{ll}$",shelves["central"]["EE"]["nLL"],shelves["central"]["MM"]["nLL"],shelves["central"]["EE"]["nLL"]+shelves["central"]["MM"]["nLL"],shelves["central"]["EM"]["nLL"])
	
	
	tableRawForward += templateRaw%("$N_{tt}$",shelves["forward"]["EE"]["nTT"],shelves["forward"]["MM"]["nTT"],shelves["forward"]["EE"]["nTT"]+shelves["forward"]["MM"]["nTT"],shelves["forward"]["EM"]["nTT"])
	tableRawForward += templateRaw%("$N_{lt}$ + $N_{tl}$",shelves["forward"]["EE"]["nTL"]+shelves["forward"]["EE"]["nLT"],shelves["forward"]["MM"]["nTL"]+shelves["forward"]["MM"]["nLT"],shelves["forward"]["EE"]["nTL"]+shelves["forward"]["EE"]["nLT"]+shelves["forward"]["MM"]["nTL"]+shelves["forward"]["MM"]["nLT"],shelves["forward"]["EM"]["nTL"]+shelves["forward"]["EE"]["nLT"])
	tableRawForward += templateRaw%("$N_{ll}$",shelves["forward"]["EE"]["nLL"],shelves["forward"]["MM"]["nLL"],shelves["forward"]["EE"]["nLL"]+shelves["forward"]["MM"]["nLL"],shelves["forward"]["EM"]["nLL"])
	
	
	tableCentral += template%("Non-prompt estimate",shelves["central"]["EE"]["nFake"],shelves["central"]["EE"]["nFakeErr"],shelves["central"]["EE"]["nFake"],shelves["central"]["MM"]["nFake"],shelves["central"]["MM"]["nFakeErr"],shelves["central"]["MM"]["nFake"],shelves["central"]["EE"]["nFake"]+shelves["central"]["MM"]["nFake"],shelves["central"]["EE"]["nFakeErr"]+shelves["central"]["MM"]["nFakeErr"],shelves["central"]["EE"]["nFake"]+shelves["central"]["MM"]["nFake"],shelves["central"]["EM"]["nFake"],shelves["central"]["EM"]["nFakeErr"],shelves["central"]["EM"]["nFake"])
	tableForward += template%("Non-prompt estiamte",shelves["forward"]["EE"]["nFake"],shelves["forward"]["EE"]["nFakeErr"],shelves["forward"]["EE"]["nFake"],shelves["forward"]["MM"]["nFake"],shelves["forward"]["MM"]["nFakeErr"],shelves["forward"]["MM"]["nFake"],shelves["forward"]["EE"]["nFake"]+shelves["forward"]["MM"]["nFake"],shelves["forward"]["EE"]["nFakeErr"]+shelves["forward"]["MM"]["nFakeErr"],shelves["forward"]["EE"]["nFake"]+shelves["forward"]["MM"]["nFake"],shelves["forward"]["EM"]["nFake"],shelves["forward"]["EM"]["nFakeErr"],shelves["forward"]["EM"]["nFake"])
	
	saveTable(tableTemplate%(tableRawCentral,tableCentral,tableRawForward,tableForward),"nonPrompt")		
	
	
def main():
	
	
	name = "nonPromptMC"
	shelves = {"inclusive":readPickle(name,"Inclusive" , runRanges.name),"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	

	produceMCTable(shelves)


	name = "nonPrompt"
	shelves = {"central": readPickle(name,regionsToUse.signal.central.name,runRanges.name), "forward":readPickle(name,regionsToUse.signal.forward.name,runRanges.name)}	
	
	
	produceDataTable(shelves)

main()

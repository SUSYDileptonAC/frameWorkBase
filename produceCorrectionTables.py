import pickle
import os
import sys


from corrections import rSFOF, rEEOF, rMMOF, rOutIn, rOutInEE, rOutInMM, rMuE, rSFOFTrig, rSFOFFact
from centralConfig import zPredictions, regionsToUse, runRanges, baselineTrigger

import argparse	
import subprocess

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

def readTriggerPickle(name,regionName,runName,source,MC=False):
	
	if MC:
		if os.path.isfile("shelves/%s_%s_%s_%s_MC.pkl"%(name,regionName,source,runName)):
			result = pickle.load(open("shelves/%s_%s_%s_%s_MC.pkl"%(name,regionName,source,runName),"rb"))
		else:
			print "shelves/%s_%s_%s_%s.pkl not found, exiting"%(name,regionName,source,runName) 		
			sys.exit()		
	else:
		if os.path.isfile("shelves/%s_%s_%s_%s.pkl"%(name,regionName,source,runName)):
			result = pickle.load(open("shelves/%s_%s_%s_%s.pkl"%(name,regionName,source,runName),"rb"))
		else:
			print "shelves/%s_%s_%s_%s.pkl not found, exiting"%(name,regionName,source,runName) 		
			sys.exit()

	return result		


def produceRSFOFTable():
	


	shelvesRSFOF = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRanges.name),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRanges.name), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRanges.name)}
	shelvesRSFOFMC = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRanges.name,MC=True),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRanges.name,MC=True), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRanges.name,MC=True)}	





	tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
  \label{tab:rSFOF}
\begin{tabular}{l|c|c|c|c}     
 & $N_{SF}$ & $N_{OF}$ & $ R_{SF/OF} \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
\hline
 & \multicolumn{4}{c}{Central} \\
\hline
%s 
 
    \hline 
& \multicolumn{4}{c}{Forward} \\
\hline
%s

  
\end{tabular}  
\end{table}
"""

	lineTemplate = r" %s & %.1f & %.1f & %.3f$\pm$%.3f & %.3f$\pm$%.3f\\"+"\n"
	lineTemplateData = r" %s & %d & %d & %.3f$\pm$%.3f & -- \\"+"\n"


	tableCentral =""
	tableForward =""


	tableCentral += lineTemplateData%("Data",shelvesRSFOF["central"]["SF"],shelvesRSFOF["central"]["OF"],shelvesRSFOF["central"]["rSFOF"],shelvesRSFOF["central"]["rSFOFErr"])	
	tableCentral+= lineTemplate%("MC",shelvesRSFOFMC["central"]["SF"],shelvesRSFOFMC["central"]["OF"],shelvesRSFOFMC["central"]["rSFOF"],shelvesRSFOFMC["central"]["rSFOFErr"],shelvesRSFOFMC["central"]["transfer"],shelvesRSFOFMC["central"]["transferErr"])	
	
	tableForward += lineTemplateData%("Data",shelvesRSFOF["forward"]["SF"],shelvesRSFOF["forward"]["OF"],shelvesRSFOF["forward"]["rSFOF"],shelvesRSFOF["forward"]["rSFOFErr"])	
	tableForward += lineTemplate%("MC",shelvesRSFOFMC["forward"]["SF"],shelvesRSFOFMC["forward"]["OF"],shelvesRSFOFMC["forward"]["rSFOF"],shelvesRSFOFMC["forward"]["rSFOFErr"],shelvesRSFOFMC["forward"]["transfer"],shelvesRSFOFMC["forward"]["transferErr"])	


	
	saveTable(tableTemplate%(tableCentral,tableForward), "Rsfof_seperated")


	tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
 \caption{Observed event yields in the control region and the resulting values of \Rsfof, \Reeof, and \Rmmof. The results are shown separately for the central and forward lepton selection and the same quantities derived on simulation are shown for comaprison.}
  \label{tab:rSFOF}
\begin{tabular}{l|c|c|c|c}     
 & $N_{SF}$ & $N_{OF}$ & $ R_{SF/OF} \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
\hline
&  \multicolumn{4}{c}{Central} \\
\hline
%s 
 
    \hline 
& \multicolumn{4}{c}{Forward} \\
\hline
%s
\hline\hline
 & $N_{ee}$ & $N_{OF}$ & $ R_{ee/OF} \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
\hline
&  \multicolumn{4}{c}{Central} \\
\hline
%s 
 
    \hline 
& \multicolumn{4}{c}{Forward} \\
\hline
%s
\hline\hline
 & $N_{\mu\mu}$ & $N_{OF}$ & $ R_{\mu\mu/OF} \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
\hline
& \multicolumn{4}{c}{Central} \\
\hline
%s 
 
    \hline 
 & \multicolumn{4}{c}{Forward} \\
\hline
%s
  
\end{tabular}  
\end{table}
"""
	tableCentralEE =""
	tableForwardEE =""

	tableCentralEE += lineTemplateData%("Data",shelvesRSFOF["central"]["EE"],shelvesRSFOF["central"]["OF"],shelvesRSFOF["central"]["rEEOF"],shelvesRSFOF["central"]["rEEOFErr"])	
	tableCentralEE += lineTemplate%("MC",shelvesRSFOFMC["central"]["EE"],shelvesRSFOFMC["central"]["OF"],shelvesRSFOFMC["central"]["rEEOF"],shelvesRSFOFMC["central"]["rEEOFErr"],shelvesRSFOFMC["central"]["transferEE"],shelvesRSFOFMC["central"]["transferEEErr"])	
	
	tableForwardEE += lineTemplateData%("Data",shelvesRSFOF["forward"]["EE"],shelvesRSFOF["forward"]["OF"],shelvesRSFOF["forward"]["rEEOF"],shelvesRSFOF["forward"]["rEEOFErr"])	
	tableForwardEE += lineTemplate%("MC",shelvesRSFOFMC["forward"]["EE"],shelvesRSFOFMC["forward"]["OF"],shelvesRSFOFMC["forward"]["rEEOF"],shelvesRSFOFMC["forward"]["rEEOFErr"],shelvesRSFOFMC["forward"]["transferEE"],shelvesRSFOFMC["forward"]["transferEEErr"])	

	tableCentralMM =""
	tableForwardMM =""

	tableCentralMM += lineTemplateData%("Data",shelvesRSFOF["central"]["MM"],shelvesRSFOF["central"]["OF"],shelvesRSFOF["central"]["rMMOF"],shelvesRSFOF["central"]["rMMOFErr"])	
	tableCentralMM += lineTemplate%("MC",shelvesRSFOFMC["central"]["MM"],shelvesRSFOFMC["central"]["OF"],shelvesRSFOFMC["central"]["rMMOF"],shelvesRSFOFMC["central"]["rMMOFErr"],shelvesRSFOFMC["central"]["transferMM"],shelvesRSFOFMC["central"]["transferMMErr"])	
	
	tableForwardMM += lineTemplateData%("Data",shelvesRSFOF["forward"]["MM"],shelvesRSFOF["forward"]["OF"],shelvesRSFOF["forward"]["rMMOF"],shelvesRSFOF["forward"]["rMMOFErr"])	
	tableForwardMM += lineTemplate%("MC",shelvesRSFOFMC["forward"]["MM"],shelvesRSFOFMC["forward"]["OF"],shelvesRSFOFMC["forward"]["rMMOF"],shelvesRSFOFMC["forward"]["rMMOFErr"],shelvesRSFOFMC["forward"]["transferMM"],shelvesRSFOFMC["forward"]["transferMMErr"])	


	
	saveTable(tableTemplate%(tableCentral,tableForward,tableCentralEE,tableForwardEE,tableCentralMM,tableForwardMM), "Rsfof_full_seperated")

	tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
  \label{tab:rSFOF}
\begin{tabular}{l|c|c|c|c}     
 & $N_{SF}$ & $N_{OF}$ & $ R_{SF/OF} \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\  
\hline
%s 
  
\end{tabular}  
\end{table}
"""

	lineTemplate = r" %s & %.1f & %.1f & %.3f$\pm$%.3f & %.3f$\pm$%.3f\\"+"\n"
	lineTemplateData = r" %s & %d & %d & %.3f$\pm$%.3f & -- \\"+"\n"


	table =""


	table += lineTemplateData%("Data",shelvesRSFOF["inclusive"]["SF"],shelvesRSFOF["inclusive"]["OF"],shelvesRSFOF["inclusive"]["rSFOF"],shelvesRSFOF["inclusive"]["rSFOFErr"])	
	table+= lineTemplate%("MC",shelvesRSFOFMC["inclusive"]["SF"],shelvesRSFOFMC["inclusive"]["OF"],shelvesRSFOFMC["inclusive"]["rSFOF"],shelvesRSFOFMC["inclusive"]["rSFOFErr"],shelvesRSFOFMC["inclusive"]["transfer"],shelvesRSFOFMC["inclusive"]["transferErr"])	
	
	

	
	saveTable(tableTemplate%(table), "Rsfof")
	tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
 \caption{Observed event yields in the control region and the resulting values for $R_{SF/OF}$, $R_{ee/OF}$,
 and $R_{\mu\mu/OF}$.}
  \label{tab:rSFOF}
\begin{tabular}{l|c|c|c|c}     
 & $N_{SF}$ & $N_{OF}$ & $ R_{SF/OF} \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
\hline
%s 
 
\hline
 & $N_{ee}$ & $N_{OF}$ & $ R_{ee/OF} \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
\hline
%s 

\hline
 & $N_{\mu\mu}$ & $N_{OF}$ & $ R_{\mu\mu/OF} \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
\hline
%s 

  
\end{tabular}  
\end{table}
"""
	tableEE =""

	tableEE += lineTemplateData%("Data",shelvesRSFOF["inclusive"]["EE"],shelvesRSFOF["inclusive"]["OF"],shelvesRSFOF["inclusive"]["rEEOF"],shelvesRSFOF["inclusive"]["rEEOFErr"])	
	tableEE += lineTemplate%("MC",shelvesRSFOFMC["inclusive"]["EE"],shelvesRSFOFMC["inclusive"]["OF"],shelvesRSFOFMC["inclusive"]["rEEOF"],shelvesRSFOFMC["inclusive"]["rEEOFErr"],shelvesRSFOFMC["inclusive"]["transferEE"],shelvesRSFOFMC["inclusive"]["transferEEErr"])	
	
	tableMM =""
	tableMM =""

	tableMM += lineTemplateData%("Data",shelvesRSFOF["inclusive"]["MM"],shelvesRSFOF["inclusive"]["OF"],shelvesRSFOF["inclusive"]["rMMOF"],shelvesRSFOF["inclusive"]["rMMOFErr"])	
	tableMM += lineTemplate%("MC",shelvesRSFOFMC["inclusive"]["MM"],shelvesRSFOFMC["inclusive"]["OF"],shelvesRSFOFMC["inclusive"]["rMMOF"],shelvesRSFOFMC["inclusive"]["rMMOFErr"],shelvesRSFOFMC["inclusive"]["transferMM"],shelvesRSFOFMC["inclusive"]["transferMMErr"])	
	

	
	saveTable(tableTemplate%(table,tableEE,tableMM,), "Rsfof_full")


def produceRMuETable():


	template = r"        %s       &  %d                   & %d              &  %.3f$\pm$%.3f$\pm$%.3f    \\" +"\n"

	shelvesRMuE = {"inclusive":readPickle("rMuE",regionsToUse.rMuE.inclusive.name , runRanges.name),"central": readPickle("rMuE",regionsToUse.rMuE.central.name,runRanges.name), "forward":readPickle("rMuE",regionsToUse.rMuE.forward.name,runRanges.name)}
	shelvesRMuEMC = {"inclusive":readPickle("rMuE",regionsToUse.rMuE.inclusive.name , runRanges.name,MC=True),"central": readPickle("rMuE",regionsToUse.rMuE.central.name,runRanges.name,MC=True), "forward":readPickle("rMuE",regionsToUse.rMuE.forward.name,runRanges.name,MC=True)}

	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \centering
 \caption{Result of the calculation of \\rmue. Shown are the observed event yields in the Drell--Yan control region for the central and forward lepton selection in the \EE and \MM channels and the resulting values of \rmue. The same quantaties derived from simulation are shown for comparison.}
  \label{tab:rMuE}
  \\begin{tabular}{l| ccc }

    							& $N_{\mu\mu}$ &  $N_{ee}$ & $\\rmue \\pm \sigma_{\\text{stat.}} \\pm \sigma_{\\text{syst.}}$ \\\\ \n    
    \hline
    							& \multicolumn{3}{c}{Central}  \\\\ \n
    \hline
%s
%s
\hline
    							& \multicolumn{3}{c}{Forward}  \\\\ \n
    \hline
%s
%s
  \end{tabular}
\end{table}


"""
	
	dataCentral = template%("Data",shelvesRMuE["central"]["nMM"],shelvesRMuE["central"]["nEE"],shelvesRMuE["central"]["rMuE"],shelvesRMuE["central"]["rMuEStatErr"],shelvesRMuE["central"]["rMuESystErr"])
	dataForward = template%("Data",shelvesRMuE["forward"]["nMM"],shelvesRMuE["forward"]["nEE"],shelvesRMuE["forward"]["rMuE"],shelvesRMuE["forward"]["rMuEStatErr"],shelvesRMuE["forward"]["rMuESystErr"])
	mcCentral = template%("MC",shelvesRMuEMC["central"]["nMM"],shelvesRMuEMC["central"]["nEE"],shelvesRMuEMC["central"]["rMuE"],shelvesRMuEMC["central"]["rMuEStatErr"],shelvesRMuEMC["central"]["rMuESystErr"])
	mcForward = template%("MC",shelvesRMuEMC["forward"]["nMM"],shelvesRMuEMC["forward"]["nEE"],shelvesRMuEMC["forward"]["rMuE"],shelvesRMuEMC["forward"]["rMuEStatErr"],shelvesRMuEMC["forward"]["rMuESystErr"])
	table = tableTemplate%(dataCentral,mcCentral,dataForward,mcForward)
	
	saveTable(table,"rMuE_result_seperated")

	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \centering
 \caption{Result of the calculation of \rmue. Shown are the observed event yields in the Drell-Yan control region
 in the $e^{+}e^{-}$ and $\mu^{+}\mu^{-}$ channels and the resulting values fro \rmue. The same quantities derived
 from simulation are shown for comparison.}
   \label{tab:rMuE}
  \\begin{tabular}{l| ccc }

    							& $N_{\mu\mu}$ &  $N_{ee}$ & $ r_{\mu e} \\pm \sigma_{\\text{stat.}} \\pm \sigma_{\\text{syst.}}$ \\\\ \n    
    \hline
%s
%s
  \end{tabular}
\end{table}


"""
	
	data = template%("Data",shelvesRMuE["inclusive"]["nMM"],shelvesRMuE["inclusive"]["nEE"],shelvesRMuE["inclusive"]["rMuE"],shelvesRMuE["inclusive"]["rMuEStatErr"],shelvesRMuE["inclusive"]["rMuESystErr"])
	mc = template%("MC",shelvesRMuEMC["inclusive"]["nMM"],shelvesRMuEMC["inclusive"]["nEE"],shelvesRMuEMC["inclusive"]["rMuE"],shelvesRMuEMC["inclusive"]["rMuEStatErr"],shelvesRMuEMC["inclusive"]["rMuESystErr"])
	table = tableTemplate%(data,mc)
	
	saveTable(table,"rMuE_result")



def produceROutInTable():




	shelvesROutIn = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRanges.name),"central": readPickle("rOutIn",regionsToUse.rOutIn.central.name,runRanges.name), "forward":readPickle("rOutIn",regionsToUse.rOutIn.forward.name,runRanges.name)}
	shelvesROutInMC = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRanges.name,MC=True),"central": readPickle("rOutIn",regionsToUse.rOutIn.central.name,runRanges.name,MC=True), "forward":readPickle("rOutIn",regionsToUse.rOutIn.forward.name,runRanges.name,MC=True)}

	
	tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
 \caption{
     }
  \label{tab:rOutIn}
\begin{tabular}{l|c|c|c}     
 & $N_{\text{out}}$ & $N_{\text{in}}$ & $ \Routin (SF) \pm \sigma_{stat}$  \\    
\hline
 & \multicolumn{3}{c}{Central} \\
\hline 
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s
 
    \hline 
& \multicolumn{3}{c}{Forward} \\
\hline 
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s

  
\end{tabular}  
\end{table}
"""

	lineTemplate = r" %s & %.1f$\pm$%.1f & %.1f$\pm$%.1f & %.3f$\pm$%.3f$\pm$%.3f \\"+"\n"
	
	tableCentralLowMass =""
	tableForwardLowMass =""
	
	tableCentralHighMass =""
	tableForwardHighMass =""

	tableCentralLowMass += lineTemplate%("Data",shelvesROutIn["central"]["correctedLowMassSF"],shelvesROutIn["central"]["lowMassErrorSF"],shelvesROutIn["central"]["correctedPeakSF"],shelvesROutIn["central"]["peakErrorSF"],shelvesROutIn["central"]["rOutInLowMassSF"],shelvesROutIn["central"]["rOutInLowMassErrSF"],shelvesROutIn["central"]["rOutInLowMassSystSF"])	
	tableCentralLowMass += lineTemplate%("MC",shelvesROutInMC["central"]["correctedLowMassSF"],shelvesROutInMC["central"]["lowMassErrorSF"],shelvesROutInMC["central"]["correctedPeakSF"],shelvesROutInMC["central"]["peakErrorSF"],shelvesROutInMC["central"]["rOutInLowMassSF"],shelvesROutInMC["central"]["rOutInLowMassErrSF"],shelvesROutInMC["central"]["rOutInLowMassSystSF"])	

	tableForwardLowMass += lineTemplate%("Data",shelvesROutIn["forward"]["correctedLowMassSF"],shelvesROutIn["forward"]["lowMassErrorSF"],shelvesROutIn["forward"]["correctedPeakSF"],shelvesROutIn["forward"]["peakErrorSF"],shelvesROutIn["forward"]["rOutInLowMassSF"],shelvesROutIn["forward"]["rOutInLowMassErrSF"],shelvesROutIn["forward"]["rOutInLowMassSystSF"])	
	tableForwardLowMass += lineTemplate%("MC",shelvesROutInMC["forward"]["correctedLowMassSF"],shelvesROutInMC["forward"]["lowMassErrorSF"],shelvesROutInMC["forward"]["correctedPeakSF"],shelvesROutInMC["forward"]["peakErrorSF"],shelvesROutInMC["forward"]["rOutInLowMassSF"],shelvesROutInMC["forward"]["rOutInLowMassErrSF"],shelvesROutInMC["forward"]["rOutInLowMassSystSF"])	


	tableCentralHighMass += lineTemplate%("Data",shelvesROutIn["central"]["correctedHighMassSF"],shelvesROutIn["central"]["highMassErrorSF"],shelvesROutIn["central"]["correctedPeakSF"],shelvesROutIn["central"]["peakErrorSF"],shelvesROutIn["central"]["rOutInHighMassSF"],shelvesROutIn["central"]["rOutInHighMassErrSF"],shelvesROutIn["central"]["rOutInHighMassSystSF"])	
	tableCentralHighMass += lineTemplate%("MC",shelvesROutInMC["central"]["correctedHighMassSF"],shelvesROutInMC["central"]["highMassErrorSF"],shelvesROutInMC["central"]["correctedPeakSF"],shelvesROutInMC["central"]["peakErrorSF"],shelvesROutInMC["central"]["rOutInHighMassSF"],shelvesROutInMC["central"]["rOutInHighMassErrSF"],shelvesROutInMC["central"]["rOutInHighMassSystSF"])	

	tableForwardHighMass += lineTemplate%("Data",shelvesROutIn["forward"]["correctedHighMassSF"],shelvesROutIn["forward"]["highMassErrorSF"],shelvesROutIn["forward"]["correctedPeakSF"],shelvesROutIn["forward"]["peakErrorSF"],shelvesROutIn["forward"]["rOutInHighMassSF"],shelvesROutIn["forward"]["rOutInHighMassErrSF"],shelvesROutIn["forward"]["rOutInHighMassSystSF"])	
	tableForwardHighMass += lineTemplate%("MC",shelvesROutInMC["forward"]["correctedHighMassSF"],shelvesROutInMC["forward"]["highMassErrorSF"],shelvesROutInMC["forward"]["correctedPeakSF"],shelvesROutInMC["forward"]["peakErrorSF"],shelvesROutInMC["forward"]["rOutInHighMassSF"],shelvesROutInMC["forward"]["rOutInHighMassErrSF"],shelvesROutInMC["forward"]["rOutInHighMassSystSF"])	


	saveTable(tableTemplate%(tableCentralLowMass,tableCentralHighMass,tableForwardLowMass,tableForwardHighMass), "ROutIn_Seperated")

	tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
 \caption{
     }
  \label{tab:rOutIn}
\begin{tabular}{l|c|c|c}     
 & $N_{\text{out}}$ & $N_{\text{in}}$ & $ \Routin (SF) \pm \sigma_{stat}$  \\    
\hline
 & \multicolumn{3}{c}{Central} \\
\hline 
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s
 
    \hline 
& \multicolumn{3}{c}{Forward} \\
\hline 
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s
\hline
 & $N_{\text{out}}$ & $N_{\text{in}}$ & $ \Routin (\EE) \pm \sigma_{stat}$  \\    
\hline
 & \multicolumn{3}{c}{Central} \\
\hline 
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s
 
    \hline 
& \multicolumn{3}{c}{Forward} \\
\hline 
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s
\hline
 & $N_{\text{out}}$ & $N_{\text{in}}$ & $ \Routin (\MM)) \pm \sigma_{stat}$  \\    
\hline
 & \multicolumn{3}{c}{Central} \\
\hline 
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s
 
    \hline 
& \multicolumn{3}{c}{Forward} \\
\hline 
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s
  
\end{tabular}  
\end{table}
"""
	
	lineTemplate = r" %s & %.1f$\pm$%.1f & %.1f$\pm$%.1f & %.3f$\pm$%.3f$\pm$%.3f \\"+"\n"
	
	
	tableCentralEELowMass =""
	tableForwardEELowMass =""
	
	tableCentralEEHighMass =""
	tableForwardEEHighMass =""

	tableCentralEELowMass += lineTemplate%("Data",shelvesROutIn["central"]["correctedLowMassEE"],shelvesROutIn["central"]["lowMassErrorEE"],shelvesROutIn["central"]["correctedPeakEE"],shelvesROutIn["central"]["peakErrorEE"],shelvesROutIn["central"]["rOutInLowMassEE"],shelvesROutIn["central"]["rOutInLowMassErrEE"],shelvesROutIn["central"]["rOutInLowMassSystEE"])	
	tableCentralEELowMass += lineTemplate%("MC",shelvesROutInMC["central"]["correctedLowMassEE"],shelvesROutInMC["central"]["lowMassErrorEE"],shelvesROutInMC["central"]["correctedPeakEE"],shelvesROutInMC["central"]["peakErrorEE"],shelvesROutInMC["central"]["rOutInLowMassEE"],shelvesROutInMC["central"]["rOutInLowMassErrEE"],shelvesROutInMC["central"]["rOutInLowMassSystEE"])	

	tableForwardEELowMass += lineTemplate%("Data",shelvesROutIn["forward"]["correctedLowMassEE"],shelvesROutIn["forward"]["lowMassErrorEE"],shelvesROutIn["forward"]["correctedPeakEE"],shelvesROutIn["forward"]["peakErrorEE"],shelvesROutIn["forward"]["rOutInLowMassEE"],shelvesROutIn["forward"]["rOutInLowMassErrEE"],shelvesROutIn["forward"]["rOutInLowMassSystEE"])	
	tableForwardEELowMass += lineTemplate%("MC",shelvesROutInMC["forward"]["correctedLowMassEE"],shelvesROutInMC["forward"]["lowMassErrorEE"],shelvesROutInMC["forward"]["correctedPeakEE"],shelvesROutInMC["forward"]["peakErrorEE"],shelvesROutInMC["forward"]["rOutInLowMassEE"],shelvesROutInMC["forward"]["rOutInLowMassErrEE"],shelvesROutInMC["forward"]["rOutInLowMassSystEE"])	


	tableCentralEEHighMass += lineTemplate%("Data",shelvesROutIn["central"]["correctedHighMassEE"],shelvesROutIn["central"]["highMassErrorEE"],shelvesROutIn["central"]["correctedPeakEE"],shelvesROutIn["central"]["peakErrorEE"],shelvesROutIn["central"]["rOutInHighMassEE"],shelvesROutIn["central"]["rOutInHighMassErrEE"],shelvesROutIn["central"]["rOutInHighMassSystEE"])	
	tableCentralEEHighMass += lineTemplate%("MC",shelvesROutInMC["central"]["correctedHighMassEE"],shelvesROutInMC["central"]["highMassErrorEE"],shelvesROutInMC["central"]["correctedPeakEE"],shelvesROutInMC["central"]["peakErrorEE"],shelvesROutInMC["central"]["rOutInHighMassEE"],shelvesROutInMC["central"]["rOutInHighMassErrEE"],shelvesROutInMC["central"]["rOutInHighMassSystEE"])	

	tableForwardEEHighMass += lineTemplate%("Data",shelvesROutIn["forward"]["correctedHighMassEE"],shelvesROutIn["forward"]["highMassErrorEE"],shelvesROutIn["forward"]["correctedPeakEE"],shelvesROutIn["forward"]["peakErrorEE"],shelvesROutIn["forward"]["rOutInHighMassEE"],shelvesROutIn["forward"]["rOutInHighMassErrEE"],shelvesROutIn["forward"]["rOutInHighMassSystEE"])	
	tableForwardEEHighMass += lineTemplate%("MC",shelvesROutInMC["forward"]["correctedHighMassEE"],shelvesROutInMC["forward"]["highMassErrorEE"],shelvesROutInMC["forward"]["correctedPeakEE"],shelvesROutInMC["forward"]["peakErrorEE"],shelvesROutInMC["forward"]["rOutInHighMassEE"],shelvesROutInMC["forward"]["rOutInHighMassErrEE"],shelvesROutInMC["forward"]["rOutInHighMassSystEE"])	

	
	tableCentralMMLowMass =""
	tableForwardMMLowMass =""
	
	tableCentralMMHighMass =""
	tableForwardMMHighMass =""

	tableCentralMMLowMass += lineTemplate%("Data",shelvesROutIn["central"]["correctedLowMassMM"],shelvesROutIn["central"]["lowMassErrorMM"],shelvesROutIn["central"]["correctedPeakMM"],shelvesROutIn["central"]["peakErrorMM"],shelvesROutIn["central"]["rOutInLowMassMM"],shelvesROutIn["central"]["rOutInLowMassErrMM"],shelvesROutIn["central"]["rOutInLowMassSystMM"])	
	tableCentralMMLowMass += lineTemplate%("MC",shelvesROutInMC["central"]["correctedLowMassMM"],shelvesROutInMC["central"]["lowMassErrorMM"],shelvesROutInMC["central"]["correctedPeakMM"],shelvesROutInMC["central"]["peakErrorMM"],shelvesROutInMC["central"]["rOutInLowMassMM"],shelvesROutInMC["central"]["rOutInLowMassErrMM"],shelvesROutInMC["central"]["rOutInLowMassSystMM"])	

	tableForwardMMLowMass += lineTemplate%("Data",shelvesROutIn["forward"]["correctedLowMassMM"],shelvesROutIn["forward"]["lowMassErrorMM"],shelvesROutIn["forward"]["correctedPeakMM"],shelvesROutIn["forward"]["peakErrorMM"],shelvesROutIn["forward"]["rOutInLowMassMM"],shelvesROutIn["forward"]["rOutInLowMassErrMM"],shelvesROutIn["forward"]["rOutInLowMassSystMM"])	
	tableForwardMMLowMass += lineTemplate%("MC",shelvesROutInMC["forward"]["correctedLowMassMM"],shelvesROutInMC["forward"]["lowMassErrorMM"],shelvesROutInMC["forward"]["correctedPeakMM"],shelvesROutInMC["forward"]["peakErrorMM"],shelvesROutInMC["forward"]["rOutInLowMassMM"],shelvesROutInMC["forward"]["rOutInLowMassErrMM"],shelvesROutInMC["forward"]["rOutInLowMassSystMM"])	


	tableCentralMMHighMass += lineTemplate%("Data",shelvesROutIn["central"]["correctedHighMassMM"],shelvesROutIn["central"]["highMassErrorMM"],shelvesROutIn["central"]["correctedPeakMM"],shelvesROutIn["central"]["peakErrorMM"],shelvesROutIn["central"]["rOutInHighMassMM"],shelvesROutIn["central"]["rOutInHighMassErrMM"],shelvesROutIn["central"]["rOutInHighMassSystMM"])	
	tableCentralMMHighMass += lineTemplate%("MC",shelvesROutInMC["central"]["correctedHighMassMM"],shelvesROutInMC["central"]["highMassErrorMM"],shelvesROutInMC["central"]["correctedPeakMM"],shelvesROutInMC["central"]["peakErrorMM"],shelvesROutInMC["central"]["rOutInHighMassMM"],shelvesROutInMC["central"]["rOutInHighMassErrMM"],shelvesROutInMC["central"]["rOutInHighMassSystMM"])	

	tableForwardMMHighMass += lineTemplate%("Data",shelvesROutIn["forward"]["correctedHighMassMM"],shelvesROutIn["forward"]["highMassErrorMM"],shelvesROutIn["forward"]["correctedPeakMM"],shelvesROutIn["forward"]["peakErrorMM"],shelvesROutIn["forward"]["rOutInHighMassMM"],shelvesROutIn["forward"]["rOutInHighMassErrMM"],shelvesROutIn["forward"]["rOutInHighMassSystMM"])	
	tableForwardMMHighMass += lineTemplate%("MC",shelvesROutInMC["forward"]["correctedHighMassMM"],shelvesROutInMC["forward"]["highMassErrorMM"],shelvesROutInMC["forward"]["correctedPeakMM"],shelvesROutInMC["forward"]["peakErrorMM"],shelvesROutInMC["forward"]["rOutInHighMassMM"],shelvesROutInMC["forward"]["rOutInHighMassErrMM"],shelvesROutInMC["forward"]["rOutInHighMassSystMM"])	


	
	saveTable(tableTemplate%(tableCentralLowMass,tableCentralHighMass,tableForwardLowMass,tableForwardHighMass,tableCentralEELowMass,tableCentralEEHighMass,tableForwardEELowMass,tableForwardEEHighMass,tableCentralMMLowMass,tableCentralMMHighMass,tableForwardMMLowMass,tableForwardMMHighMass), "ROutIn_full_seperated")

	
	tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
  \label{tab:rOutIn}
\begin{tabular}{l|c|c|c}     
 & $N_{\text{out}}$ & $N_{\text{in}}$ & $ R_{Out/In} (SF) \pm \sigma_{stat}$  \\    
\hline
 & \multicolumn{3}{c}{Edge mass}   \\ 
 %s
\hline
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s
  
\end{tabular}  
\end{table}
"""

	lineTemplate = r" %s & %.1f$\pm$%.1f & %.1f$\pm$%.1f & %.3f$\pm$%.3f$\pm$%.3f \\"+"\n"
	
	tableEdgeMass =""
	
	tableLowMass =""
	
	tableHighMass =""

	tableEdgeMass += lineTemplate%("Data",shelvesROutIn["inclusive"]["correctedEdgeMassSF"],shelvesROutIn["inclusive"]["edgeMassErrorSF"],shelvesROutIn["inclusive"]["correctedPeakSF"],shelvesROutIn["inclusive"]["peakErrorSF"],shelvesROutIn["inclusive"]["rOutInEdgeMassSF"],shelvesROutIn["inclusive"]["rOutInEdgeMassErrSF"],shelvesROutIn["inclusive"]["rOutInEdgeMassSystSF"])	
	tableEdgeMass += lineTemplate%("MC",shelvesROutInMC["inclusive"]["correctedEdgeMassSF"],shelvesROutInMC["inclusive"]["edgeMassErrorSF"],shelvesROutInMC["inclusive"]["correctedPeakSF"],shelvesROutInMC["inclusive"]["peakErrorSF"],shelvesROutInMC["inclusive"]["rOutInEdgeMassSF"],shelvesROutInMC["inclusive"]["rOutInEdgeMassErrSF"],shelvesROutInMC["inclusive"]["rOutInEdgeMassSystSF"])	

	tableLowMass += lineTemplate%("Data",shelvesROutIn["inclusive"]["correctedLowMassSF"],shelvesROutIn["inclusive"]["lowMassErrorSF"],shelvesROutIn["inclusive"]["correctedPeakSF"],shelvesROutIn["inclusive"]["peakErrorSF"],shelvesROutIn["inclusive"]["rOutInLowMassSF"],shelvesROutIn["inclusive"]["rOutInLowMassErrSF"],shelvesROutIn["inclusive"]["rOutInLowMassSystSF"])	
	tableLowMass += lineTemplate%("MC",shelvesROutInMC["inclusive"]["correctedLowMassSF"],shelvesROutInMC["inclusive"]["lowMassErrorSF"],shelvesROutInMC["inclusive"]["correctedPeakSF"],shelvesROutInMC["inclusive"]["peakErrorSF"],shelvesROutInMC["inclusive"]["rOutInLowMassSF"],shelvesROutInMC["inclusive"]["rOutInLowMassErrSF"],shelvesROutInMC["inclusive"]["rOutInLowMassSystSF"])	

	tableHighMass += lineTemplate%("Data",shelvesROutIn["inclusive"]["correctedHighMassSF"],shelvesROutIn["inclusive"]["highMassErrorSF"],shelvesROutIn["inclusive"]["correctedPeakSF"],shelvesROutIn["inclusive"]["peakErrorSF"],shelvesROutIn["inclusive"]["rOutInHighMassSF"],shelvesROutIn["inclusive"]["rOutInHighMassErrSF"],shelvesROutIn["inclusive"]["rOutInHighMassSystSF"])	
	tableHighMass += lineTemplate%("MC",shelvesROutInMC["inclusive"]["correctedHighMassSF"],shelvesROutInMC["inclusive"]["highMassErrorSF"],shelvesROutInMC["inclusive"]["correctedPeakSF"],shelvesROutInMC["inclusive"]["peakErrorSF"],shelvesROutInMC["inclusive"]["rOutInHighMassSF"],shelvesROutInMC["inclusive"]["rOutInHighMassErrSF"],shelvesROutInMC["central"]["rOutInHighMassSystSF"])	

	

	saveTable(tableTemplate%(tableEdgeMass,tableLowMass,tableHighMass), "ROutIn")

	tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
  \label{tab:rOutIn}
\begin{tabular}{l|c|c|c}     
 & $N_{\text{out}}$ & $N_{\text{in}}$ & $ R_{Out/In} (SF) \pm \sigma_{stat}$  \\    
\hline
 & \multicolumn{3}{c}{Edge mass}   \\ 
 %s
\hline
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s
\hline
 & $N_{\text{out}}$ & $N_{\text{in}}$ & $ R_{Out/In} (ee) \pm \sigma_{stat}$  \\    
\hline
 & \multicolumn{3}{c}{Edge mass}   \\ 
 %s
\hline
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s

\hline
 & $N_{\text{out}}$ & $N_{\text{in}}$ & $ R_{Out/In} (\mu\mu)) \pm \sigma_{stat}$  \\    
\hline
 & \multicolumn{3}{c}{Edge mass}   \\ 
 %s
\hline
 & \multicolumn{3}{c}{Low mass}   \\ 
 %s
\hline 
& \multicolumn{3}{c}{high Mass} \\ 
\hline
%s
  
\end{tabular}  
\end{table}
"""
	
	lineTemplate = r" %s & %.1f$\pm$%.1f & %.1f$\pm$%.1f & %.3f$\pm$%.3f$\pm$%.3f \\"+"\n"
	
	
	tableEEEdgeMass =""
	
	tableEELowMass =""
	
	tableEEHighMass =""
	
	tableEEEdgeMass += lineTemplate%("Data",shelvesROutIn["inclusive"]["correctedEdgeMassEE"],shelvesROutIn["inclusive"]["edgeMassErrorEE"],shelvesROutIn["inclusive"]["correctedPeakEE"],shelvesROutIn["inclusive"]["peakErrorEE"],shelvesROutIn["inclusive"]["rOutInEdgeMassEE"],shelvesROutIn["inclusive"]["rOutInEdgeMassErrEE"],shelvesROutIn["inclusive"]["rOutInEdgeMassSystEE"])	
	tableEEEdgeMass += lineTemplate%("MC",shelvesROutInMC["inclusive"]["correctedEdgeMassEE"],shelvesROutInMC["inclusive"]["edgeMassErrorEE"],shelvesROutInMC["inclusive"]["correctedPeakEE"],shelvesROutInMC["inclusive"]["peakErrorEE"],shelvesROutInMC["inclusive"]["rOutInEdgeMassEE"],shelvesROutInMC["inclusive"]["rOutInEdgeMassErrEE"],shelvesROutInMC["inclusive"]["rOutInEdgeMassSystEE"])	

	tableEELowMass += lineTemplate%("Data",shelvesROutIn["inclusive"]["correctedLowMassEE"],shelvesROutIn["inclusive"]["lowMassErrorEE"],shelvesROutIn["inclusive"]["correctedPeakEE"],shelvesROutIn["inclusive"]["peakErrorEE"],shelvesROutIn["inclusive"]["rOutInLowMassEE"],shelvesROutIn["inclusive"]["rOutInLowMassErrEE"],shelvesROutIn["inclusive"]["rOutInLowMassSystEE"])	
	tableEELowMass += lineTemplate%("MC",shelvesROutInMC["inclusive"]["correctedLowMassEE"],shelvesROutInMC["inclusive"]["lowMassErrorEE"],shelvesROutInMC["inclusive"]["correctedPeakEE"],shelvesROutInMC["inclusive"]["peakErrorEE"],shelvesROutInMC["inclusive"]["rOutInLowMassEE"],shelvesROutInMC["inclusive"]["rOutInLowMassErrEE"],shelvesROutInMC["inclusive"]["rOutInLowMassSystEE"])	

	tableEEHighMass += lineTemplate%("Data",shelvesROutIn["inclusive"]["correctedHighMassEE"],shelvesROutIn["inclusive"]["highMassErrorEE"],shelvesROutIn["inclusive"]["correctedPeakEE"],shelvesROutIn["inclusive"]["peakErrorEE"],shelvesROutIn["inclusive"]["rOutInHighMassEE"],shelvesROutIn["inclusive"]["rOutInHighMassErrEE"],shelvesROutIn["inclusive"]["rOutInHighMassSystEE"])	
	tableEEHighMass += lineTemplate%("MC",shelvesROutInMC["inclusive"]["correctedHighMassEE"],shelvesROutInMC["inclusive"]["highMassErrorEE"],shelvesROutInMC["inclusive"]["correctedPeakEE"],shelvesROutInMC["inclusive"]["peakErrorEE"],shelvesROutInMC["inclusive"]["rOutInHighMassEE"],shelvesROutInMC["inclusive"]["rOutInHighMassErrEE"],shelvesROutInMC["inclusive"]["rOutInHighMassSystEE"])	

	
	tableMMEdgeMass =""
	
	tableMMLowMass =""
	
	tableMMHighMass =""

	tableMMEdgeMass += lineTemplate%("Data",shelvesROutIn["inclusive"]["correctedEdgeMassMM"],shelvesROutIn["inclusive"]["edgeMassErrorMM"],shelvesROutIn["inclusive"]["correctedPeakMM"],shelvesROutIn["inclusive"]["peakErrorMM"],shelvesROutIn["inclusive"]["rOutInEdgeMassMM"],shelvesROutIn["inclusive"]["rOutInEdgeMassErrMM"],shelvesROutIn["inclusive"]["rOutInEdgeMassSystMM"])	
	tableMMEdgeMass += lineTemplate%("MC",shelvesROutInMC["inclusive"]["correctedEdgeMassMM"],shelvesROutInMC["inclusive"]["edgeMassErrorMM"],shelvesROutInMC["inclusive"]["correctedPeakMM"],shelvesROutInMC["inclusive"]["peakErrorMM"],shelvesROutInMC["inclusive"]["rOutInEdgeMassMM"],shelvesROutInMC["inclusive"]["rOutInEdgeMassErrMM"],shelvesROutInMC["inclusive"]["rOutInEdgeMassSystMM"])	

	tableMMLowMass += lineTemplate%("Data",shelvesROutIn["inclusive"]["correctedLowMassMM"],shelvesROutIn["inclusive"]["lowMassErrorMM"],shelvesROutIn["inclusive"]["correctedPeakMM"],shelvesROutIn["inclusive"]["peakErrorMM"],shelvesROutIn["inclusive"]["rOutInLowMassMM"],shelvesROutIn["inclusive"]["rOutInLowMassErrMM"],shelvesROutIn["inclusive"]["rOutInLowMassSystMM"])	
	tableMMLowMass += lineTemplate%("MC",shelvesROutInMC["inclusive"]["correctedLowMassMM"],shelvesROutInMC["inclusive"]["lowMassErrorMM"],shelvesROutInMC["inclusive"]["correctedPeakMM"],shelvesROutInMC["inclusive"]["peakErrorMM"],shelvesROutInMC["inclusive"]["rOutInLowMassMM"],shelvesROutInMC["inclusive"]["rOutInLowMassErrMM"],shelvesROutInMC["inclusive"]["rOutInLowMassSystMM"])	

	tableMMHighMass += lineTemplate%("Data",shelvesROutIn["inclusive"]["correctedHighMassMM"],shelvesROutIn["inclusive"]["highMassErrorMM"],shelvesROutIn["inclusive"]["correctedPeakMM"],shelvesROutIn["inclusive"]["peakErrorMM"],shelvesROutIn["inclusive"]["rOutInHighMassMM"],shelvesROutIn["inclusive"]["rOutInHighMassErrMM"],shelvesROutIn["inclusive"]["rOutInHighMassSystMM"])	
	tableMMHighMass += lineTemplate%("MC",shelvesROutInMC["inclusive"]["correctedHighMassMM"],shelvesROutInMC["inclusive"]["highMassErrorMM"],shelvesROutInMC["inclusive"]["correctedPeakMM"],shelvesROutInMC["inclusive"]["peakErrorMM"],shelvesROutInMC["inclusive"]["rOutInHighMassMM"],shelvesROutInMC["inclusive"]["rOutInHighMassErrMM"],shelvesROutInMC["inclusive"]["rOutInHighMassSystMM"])	


	
	saveTable(tableTemplate%(tableEdgeMass,tableLowMass,tableHighMass,tableEEEdgeMass,tableEELowMass,tableEEHighMass,tableMMEdgeMass,tableMMLowMass,tableMMHighMass), "ROutIn_full")

def produceFactorizationTable():

	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \centering
 \caption{
     }
  \label{tab:factorization}
  \\begin{tabular}{l| c c| c c }

    & \multicolumn{2}{c}{Central} & \multicolumn{2}{c}{Forward} \\\\ \n    								
    \hline
    & Data & MC & Data & MC \\\\ \n 
    \hline
%s
\hline
\hline
%s
  \end{tabular}
\end{table}


"""

	template = r"        %s       &  %.3f$\pm$%.3f  &  %.3f$\pm$%.3f      &  %.3f$\pm$%.3f &   %.3f$\pm$%.3f    \\" +"\n"
	templateTrigger = r"        %s       &  %.3f$\pm$%.3f  &  -      &  %.3f$\pm$%.3f &   -    \\" +"\n"


	tableIngredients =""
	tableResult =""

	tableIngredients += template%("\\rmue",rMuE.central.val,rMuE.central.err,rMuE.central.valMC,rMuE.central.errMC,rMuE.forward.val,rMuE.forward.err,rMuE.forward.valMC,rMuE.forward.errMC)	
	#~ tableIngredients += template%("$R_{T}$",rSFOFTrig.central.val,rSFOFTrig.central.err,rSFOFTrig.central.valMC,rSFOFTrig.central.errMC,rSFOFTrig.forward.val,rSFOFTrig.forward.err,rSFOFTrig.forward.valMC,rSFOFTrig.forward.errMC)	
	tableIngredients += templateTrigger%("$R_{T}$",rSFOFTrig.central.val,rSFOFTrig.central.err,rSFOFTrig.forward.val,rSFOFTrig.forward.err)	

	
	tableResult += template%("\Rsfof",rSFOFFact.central.SF.val,rSFOFFact.central.SF.err,rSFOFFact.central.SF.valMC,rSFOFFact.central.SF.errMC,rSFOFFact.forward.SF.val,rSFOFFact.forward.SF.err,rSFOFFact.forward.SF.valMC,rSFOFFact.forward.SF.errMC)	
	tableResult += template%("\Reeof",rSFOFFact.central.EE.val,rSFOFFact.central.EE.err,rSFOFFact.central.EE.valMC,rSFOFFact.central.EE.errMC,rSFOFFact.forward.EE.val,rSFOFFact.forward.EE.err,rSFOFFact.forward.EE.valMC,rSFOFFact.forward.EE.errMC)	
	tableResult += template%("\Rmmof",rSFOFFact.central.MM.val,rSFOFFact.central.MM.err,rSFOFFact.central.MM.valMC,rSFOFFact.central.MM.errMC,rSFOFFact.forward.MM.val,rSFOFFact.forward.MM.err,rSFOFFact.forward.MM.valMC,rSFOFFact.forward.MM.errMC)	



	table = tableTemplate%(tableIngredients,tableResult)
	
	saveTable(table,"factorization_result_seperated")
	
	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \centering
 \caption{Results of the calculations of $R_{SF/OF}$, $R_{ee/OF}$, and $R_{\mu\mu/OF}$
  using the factorization method. The factors \rmue and $R_{T}$ which are used in the
  calculation are also displayed. Since no trigger simulation was available, the data 
  trigger efficiencies are used for the MC prediction.}
  \label{tab:factorization}
  \\begin{tabular}{l| c c }

    & Data & MC  \\\\ \n 
    \hline
%s
\hline
\hline
%s
  \end{tabular}
\end{table}


"""

	template = r"        %s       &  %.3f$\pm$%.3f  &  %.3f$\pm$%.3f   \\" +"\n"
	templateTrigger = r"        %s       &  %.3f$\pm$%.3f  &  -    \\" +"\n"


	tableIngredients =""
	tableResult =""

	tableIngredients += template%("$r_{\mu e}$",rMuE.inclusive.val,rMuE.inclusive.err,rMuE.inclusive.valMC,rMuE.inclusive.errMC)	
	tableIngredients += template%("$\frac{1}{2}$( \rmue + \rmue$^{-1})$",0.5*(rMuE.inclusive.val+1./rMuE.inclusive.val),0.5*(1. - (1./(rMuE.inclusive.val**2)))*rMuE.inclusive.err,0.5*(rMuE.inclusive.valMC+1./rMuE.inclusive.valMC),0.5*(1. - (1./(rMuE.inclusive.valMC**2)))*rMuE.inclusive.errMC)	
	#~ tableIngredients += template%("$R_{T}$",rSFOFTrig.inclusive.val,rSFOFTrig.inclusive.err,rSFOFTrig.inclusive.valMC,rSFOFTrig.inclusive.errMC,rSFOFTrig.forward.val,rSFOFTrig.forward.err,rSFOFTrig.forward.valMC,rSFOFTrig.forward.errMC)	
	tableIngredients += templateTrigger%("$R_{T}$",rSFOFTrig.inclusive.val,rSFOFTrig.inclusive.err)	

	
	tableResult += template%("$R_{SF/OF}$",rSFOFFact.inclusive.SF.val,rSFOFFact.inclusive.SF.err,rSFOFFact.inclusive.SF.valMC,rSFOFFact.inclusive.SF.errMC,)	
	tableResult += template%("$R_{ee/OF}$",rSFOFFact.inclusive.EE.val,rSFOFFact.inclusive.EE.err,rSFOFFact.inclusive.EE.valMC,rSFOFFact.inclusive.EE.errMC,)	
	tableResult += template%("$R_{\mu\mu/OF}$",rSFOFFact.inclusive.MM.val,rSFOFFact.inclusive.MM.err,rSFOFFact.inclusive.MM.valMC,rSFOFFact.inclusive.MM.errMC,)	



	table = tableTemplate%(tableIngredients,tableResult)
	
	saveTable(table,"factorization_result")

def produceCombinedRSFOFTable():

	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \centering
 \caption{
     }
  \label{tab:combinedRSFOF}
  \\begin{tabular}{l| c c| c c }
    & \multicolumn{4}{c}{\Rsfof}  \\\\ \n
    & \multicolumn{2}{c}{Central} & \multicolumn{2}{c}{Forward} \\\\ \n    								
    \hline
    & Data & MC & Data & MC \\\\ \n
    \hline
%s
\hline
    & \multicolumn{4}{c}{\Reeof}  \\\\ \n
    & \multicolumn{2}{c}{Central} & \multicolumn{2}{c}{Forward} \\\\ \n    								
    \hline
    & Data & MC & Data & MC \\\\ \n
    \hline
%s
\hline
    & \multicolumn{4}{c}{\Rmmof}  \\\\ \n
    & \multicolumn{2}{c}{Central} & \multicolumn{2}{c}{Forward} \\\\ \n    								
    \hline
    & Data & MC & Data & MC \\\\ \n
    \hline
%s
\hline
  \end{tabular}
\end{table}


"""

	template = r"        %s       &  %.3f$\pm$%.3f  &  %.3f$\pm$%.3f      &  %.3f$\pm$%.3f &   %.3f$\pm$%.3f    \\" +"\n"



	shelvesRSFOF = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRanges.name),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRanges.name), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRanges.name)}
	shelvesRSFOFMC = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRanges.name,MC=True),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRanges.name,MC=True), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRanges.name,MC=True)}	



	tableResultSF =""
	tableResultEE =""
	tableResultMM =""

	
		
	tableResultSF += template%("from factorization method",rSFOFFact.central.SF.val,rSFOFFact.central.SF.err,rSFOFFact.central.SF.valMC,rSFOFFact.central.SF.errMC,rSFOFFact.forward.SF.val,rSFOFFact.forward.SF.err,rSFOFFact.forward.SF.valMC,rSFOFFact.forward.SF.errMC)	
	tableResultSF += template%("from direct measurement",shelvesRSFOF["central"]["rSFOF"],(shelvesRSFOF["central"]["rSFOFErr"]**2+shelvesRSFOFMC["central"]["transferErr"]**2)**0.5,shelvesRSFOFMC["central"]["rSFOF"],shelvesRSFOFMC["central"]["rSFOFErr"],shelvesRSFOF["forward"]["rSFOF"],(shelvesRSFOF["forward"]["rSFOFErr"]**2+shelvesRSFOF["forward"]["transferErr"]**2)**0.5,shelvesRSFOFMC["forward"]["rSFOF"],shelvesRSFOFMC["forward"]["rSFOFErr"])	
	tableResultSF += template%("weighted avarage",rSFOF.central.val,rSFOF.central.err,rSFOF.central.valMC,rSFOF.central.errMC,rSFOF.forward.val,rSFOF.forward.err,rSFOF.forward.valMC,rSFOF.forward.errMC)	

	
	tableResultEE += template%("from factorization method",rSFOFFact.central.EE.val,rSFOFFact.central.EE.err,rSFOFFact.central.EE.valMC,rSFOFFact.central.EE.errMC,rSFOFFact.forward.EE.val,rSFOFFact.forward.EE.err,rSFOFFact.forward.EE.valMC,rSFOFFact.forward.EE.errMC)	
	tableResultEE += template%("from direct measurement",shelvesRSFOF["central"]["rEEOF"],(shelvesRSFOF["central"]["rEEOFErr"]**2+shelvesRSFOFMC["central"]["transferEEErr"]**2)**0.5,shelvesRSFOFMC["central"]["rEEOF"],shelvesRSFOFMC["central"]["rEEOFErr"],shelvesRSFOF["forward"]["rEEOF"],(shelvesRSFOF["forward"]["rEEOFErr"]**2+shelvesRSFOF["forward"]["transferErr"]**2)**0.5,shelvesRSFOFMC["forward"]["rEEOF"],shelvesRSFOFMC["forward"]["rEEOFErr"])	
	tableResultEE += template%("weighted avarage",rEEOF.central.val,rEEOF.central.err,rEEOF.central.valMC,rEEOF.central.errMC,rEEOF.forward.val,rEEOF.forward.err,rEEOF.forward.valMC,rEEOF.forward.errMC)	

	
	tableResultMM += template%("from factorization method",rSFOFFact.central.MM.val,rSFOFFact.central.MM.err,rSFOFFact.central.MM.valMC,rSFOFFact.central.MM.errMC,rSFOFFact.forward.MM.val,rSFOFFact.forward.MM.err,rSFOFFact.forward.MM.valMC,rSFOFFact.forward.MM.errMC)	
	tableResultMM += template%("from direct measurement",shelvesRSFOF["central"]["rMMOF"],(shelvesRSFOF["central"]["rMMOFErr"]**2+shelvesRSFOFMC["central"]["transferMMErr"]**2)**0.5,shelvesRSFOFMC["central"]["rMMOF"],shelvesRSFOFMC["central"]["rMMOFErr"],shelvesRSFOF["forward"]["rMMOF"],(shelvesRSFOF["forward"]["rMMOFErr"]**2+shelvesRSFOF["forward"]["transferErr"]**2)**0.5,shelvesRSFOFMC["forward"]["rMMOF"],shelvesRSFOFMC["forward"]["rMMOFErr"])	
	tableResultMM += template%("weighted avarage",rMMOF.central.val,rMMOF.central.err,rMMOF.central.valMC,rMMOF.central.errMC,rMMOF.forward.val,rMMOF.forward.err,rMMOF.forward.valMC,rMMOF.forward.errMC)	



	table = tableTemplate%(tableResultSF,tableResultEE,tableResultMM)
	
	saveTable(table,"rSFOF_combination_result_seperated")

	tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \centering
 \caption{Results of the calculations of $R_{SF/OF}$, $R_{ee/OF}$, and $R_{\mu\mu/OF}$ using
  both methods and the weighted average.}
  \label{tab:combinedRSFOF}
  \\begin{tabular}{l| c c}
    & \multicolumn{2}{c}{$R_{SF/OF}$}  \\\\ \n								
    \hline
    & Data & MC \\\\ \n
    \hline
%s
\hline
    & \multicolumn{2}{c}{$R_{ee/OF}$}  \\\\ \n 								
    \hline
    & Data & MC \\\\ \n
    \hline
%s
\hline
    & \multicolumn{2}{c}{$R_{\mu\mu/OF}$}  \\\\ \n  								
    \hline
    & Data & MC \\\\ \n
    \hline
%s
\hline
  \end{tabular}
\end{table}


"""

	template = r"        %s       &  %.3f$\pm$%.3f  &  %.3f$\pm$%.3f      \\" +"\n"


	tableResultSF =""
	tableResultEE =""
	tableResultMM =""

	tableResultSF += template%("from factorization method",rSFOFFact.inclusive.SF.val,rSFOFFact.inclusive.SF.err,rSFOFFact.inclusive.SF.valMC,rSFOFFact.inclusive.SF.errMC,)	
	tableResultSF += template%("from direct measurement",shelvesRSFOF["inclusive"]["rSFOF"],(shelvesRSFOF["inclusive"]["rSFOFErr"]**2+shelvesRSFOFMC["inclusive"]["transferErr"]**2)**0.5,shelvesRSFOFMC["inclusive"]["rSFOF"],shelvesRSFOFMC["inclusive"]["rSFOFErr"])	
	tableResultSF += template%("weighted avarage",rSFOF.inclusive.val,rSFOF.inclusive.err,rSFOF.inclusive.valMC,rSFOF.inclusive.errMC)	

	
	tableResultEE += template%("from factorization method",rSFOFFact.inclusive.EE.val,rSFOFFact.inclusive.EE.err,rSFOFFact.inclusive.EE.valMC,rSFOFFact.inclusive.EE.errMC,)	
	tableResultEE += template%("from direct measurement",shelvesRSFOF["inclusive"]["rEEOF"],(shelvesRSFOF["inclusive"]["rEEOFErr"]**2+shelvesRSFOFMC["inclusive"]["transferEEErr"]**2)**0.5,shelvesRSFOFMC["inclusive"]["rEEOF"],shelvesRSFOFMC["inclusive"]["rEEOFErr"])	
	tableResultEE += template%("weighted avarage",rEEOF.inclusive.val,rEEOF.inclusive.err,rEEOF.inclusive.valMC,rEEOF.inclusive.errMC)	

	
	tableResultMM += template%("from factorization method",rSFOFFact.inclusive.MM.val,rSFOFFact.inclusive.MM.err,rSFOFFact.inclusive.MM.valMC,rSFOFFact.inclusive.MM.errMC)	
	tableResultMM += template%("from direct measurement",shelvesRSFOF["inclusive"]["rMMOF"],(shelvesRSFOF["inclusive"]["rMMOFErr"]**2+shelvesRSFOFMC["inclusive"]["transferMMErr"]**2)**0.5,shelvesRSFOFMC["inclusive"]["rMMOF"],shelvesRSFOFMC["inclusive"]["rMMOFErr"])	
	tableResultMM += template%("weighted avarage",rMMOF.inclusive.val,rMMOF.inclusive.err,rMMOF.inclusive.valMC,rMMOF.inclusive.errMC)	



	table = tableTemplate%(tableResultSF,tableResultEE,tableResultMM)
	
	saveTable(table,"rSFOF_combination_result")


def produceTriggerEffTables():


	shelvesTrigger = {"inclusive":readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.inclusive.name , runRanges.name, baselineTrigger.name),"central": readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.central.name,runRanges.name, baselineTrigger.name), "forward":readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.forward.name,runRanges.name, baselineTrigger.name)}
	#~ shelvesTriggerMC = {"inclusive":readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.inclusive.name , runRanges.name, baselineTrigger.name,MC=True),"central": readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.central.name,runRanges.name, baselineTrigger.name,MC=True), "forward":readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.forward.name,runRanges.name, baselineTrigger.name,MC=True)}	



	
	#~ tableTemplate =r"""
#~ \begin{table}[hbp] \caption{Triggerefficiency-values for data and MC with OS, $p_T>20(20)\,\GeV$ and $H_T>200\,\GeV$ for the inclusive region.} 
#~ \centering 
#~ \renewcommand{\arraystretch}{1.2} 
#~ \begin{tabular}{l|c|c|c}     
#~ 
 #~ & nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$ \\    
#~ 
#~ &\multicolumn{3}{c}{Data, Inclusive} \\
#~ \hline
#~ %s 
 #~ 
#~ \end{tabular}  
#~ \label{tab:EffValues_Inclusive}
#~ \end{table}
#~ 
#~ \hline
#~ & \multicolumn{3}{c}{MC, Inclusive } \\
#~ \hline
#~ 
#~ %s    
    #~ \hline 
#~ """
	tableTemplate =r"""
\begin{table}[hbp] \caption{Triggerefficiency-values for data with OS, $p_T>25(20)\,\GeV$ and $H_T>200\,\GeV$.} 
\centering 
\renewcommand{\arraystretch}{1.2} 
\begin{tabular}{l|c|c|c}     

 & nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$ \\    

&\multicolumn{3}{c}{Data} \\
\hline
%s 
 
\end{tabular}  
\label{tab:TriggerEffValues}
\end{table}

"""
	lineTemplate = r"%s & %d & %d & %.3f$\pm$%.3f \\"+"\n"


	tableMC =""
	tableData =""

	
	tableData += lineTemplate%("ee",shelvesTrigger["inclusive"][runRanges.name]["EE"]["Nominator"],shelvesTrigger["inclusive"][runRanges.name]["EE"]["Denominator"],shelvesTrigger["inclusive"][runRanges.name]["EE"]["Efficiency"],max(shelvesTrigger["inclusive"][runRanges.name]["EE"]["UncertaintyUp"],shelvesTrigger["inclusive"][runRanges.name]["EE"]["UncertaintyDown"]))	
	tableData += lineTemplate%("$\mu\mu$",shelvesTrigger["inclusive"][runRanges.name]["MuMu"]["Nominator"],shelvesTrigger["inclusive"][runRanges.name]["MuMu"]["Denominator"],shelvesTrigger["inclusive"][runRanges.name]["MuMu"]["Efficiency"],max(shelvesTrigger["inclusive"][runRanges.name]["MuMu"]["UncertaintyUp"],shelvesTrigger["inclusive"][runRanges.name]["MuMu"]["UncertaintyDown"]))	
	tableData += lineTemplate%("e$\mu$",shelvesTrigger["inclusive"][runRanges.name]["EMu"]["Nominator"],shelvesTrigger["inclusive"][runRanges.name]["EMu"]["Denominator"],shelvesTrigger["inclusive"][runRanges.name]["EMu"]["Efficiency"],max(shelvesTrigger["inclusive"][runRanges.name]["EMu"]["UncertaintyUp"],shelvesTrigger["inclusive"][runRanges.name]["EMu"]["UncertaintyDown"]))



	#~ tableMC += lineTemplate%("ee",shelvesTriggerMC["inclusive"][runRanges.name]["EE"]["Nominator"],shelvesTriggerMC["inclusive"][runRanges.name]["EE"]["Denominator"],shelvesTriggerMC["inclusive"][runRanges.name]["EE"]["Efficiency"],max(shelvesTriggerMC["inclusive"][runRanges.name]["EE"]["UncertaintyUp"],shelvesTriggerMC["inclusive"][runRanges.name]["EE"]["UncertaintyDown"]))	
	#~ tableMC += lineTemplate%("$\mu\mu$",shelvesTriggerMC["inclusive"][runRanges.name]["MuMu"]["Nominator"],shelvesTriggerMC["inclusive"][runRanges.name]["MuMu"]["Denominator"],shelvesTriggerMC["inclusive"][runRanges.name]["MuMu"]["Efficiency"],max(shelvesTriggerMC["inclusive"][runRanges.name]["MuMu"]["UncertaintyUp"],shelvesTriggerMC["inclusive"][runRanges.name]["MuMu"]["UncertaintyDown"]))	
	#~ tableMC += lineTemplate%("e$\mu$",shelvesTriggerMC["inclusive"][runRanges.name]["EMu"]["Nominator"],shelvesTriggerMC["inclusive"][runRanges.name]["EMu"]["Denominator"],shelvesTriggerMC["inclusive"][runRanges.name]["EMu"]["Efficiency"],max(shelvesTriggerMC["inclusive"][runRanges.name]["EMu"]["UncertaintyUp"],shelvesTriggerMC["inclusive"][runRanges.name]["EMu"]["UncertaintyDown"]))	


		
	#~ saveTable(tableTemplate%(tableData,tableMC), "TriggerEffsExclusive_Inclusive")
	saveTable(tableTemplate%(tableData), "TriggerEffsExclusive_Inclusive")


# Table with Barrel and Endcap seperated


	#~ tableTemplate =r"""
#~ \begin{table}[hbp] \caption{Triggerefficiency-values for data and MC with OS, $p_T>20(20)\,\GeV$ and $H_T>200\,\GeV$ for central and forward region seperated.} 
#~ \centering 
#~ \renewcommand{\arraystretch}{1.2} 
#~ \begin{tabular}{l|c|c|c|c|c|c}     
#~ 
 #~ & nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$ &  nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$  \\ 
#~ \hline
#~ 
#~ &\multicolumn{6}{c}{Data} \\
#~ \hline
#~ &  \multicolumn{3}{c|}{Central } & \multicolumn{3}{|c}{ Forward }\\
#~ \hline
#~ %s 
 #~ 
#~ 
#~ 
#~ & \multicolumn{6}{c}{MC} \\
#~ \hline
#~ &  \multicolumn{3}{c|}{Central } & \multicolumn{3}{|c}{ Forward } \\
#~ \hline 
#~ %s    
    #~ \hline 
#~ \end{tabular}  
#~ \label{tab:EffValues_Seperated}
#~ \end{table}	
#~ """
	tableTemplate =r"""
\begin{table}[hbp] \caption{Triggerefficiency-values for data and MC with OS, $p_T>20(20)\,\GeV$ and $H_T>200\,\GeV$ for central and forward region seperated.} 
\centering 
\renewcommand{\arraystretch}{1.2} 
\begin{tabular}{l|c|c|c|c|c|c}     

 & nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$ &  nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$  \\ 
\hline

&\multicolumn{6}{c}{Data} \\
\hline
&  \multicolumn{3}{c|}{Central } & \multicolumn{3}{|c}{ Forward }\\
\hline
%s 
 
    \hline 
\end{tabular}  
\label{tab:EffValues_Seperated}
\end{table}	
"""
	lineTemplate = r"%s & %d & %d & %.3f$\pm$%.3f & %d & %d & %.3f$\pm$%.3f \\"+"\n"
	lineTemplateMC = r"%s & %.1f & %.1f & %.3f$\pm$%.3f & %.1f & %.1f & %.3f$\pm$%.3f \\"+"\n"
	tableMC =""
	tableData =""

	tableData += lineTemplate%("ee",shelvesTrigger["central"][runRanges.name]["EE"]["Nominator"],shelvesTrigger["central"][runRanges.name]["EE"]["Denominator"],shelvesTrigger["central"][runRanges.name]["EE"]["Efficiency"],max(shelvesTrigger["central"][runRanges.name]["EE"]["UncertaintyUp"],shelvesTrigger["central"][runRanges.name]["EE"]["UncertaintyDown"]),shelvesTrigger["forward"][runRanges.name]["EE"]["Nominator"],shelvesTrigger["forward"][runRanges.name]["EE"]["Denominator"],shelvesTrigger["forward"][runRanges.name]["EE"]["Efficiency"],max(shelvesTrigger["forward"][runRanges.name]["EE"]["UncertaintyUp"],shelvesTrigger["forward"][runRanges.name]["EE"]["UncertaintyDown"]))	
	tableData += lineTemplate%("$\mu\mu$",shelvesTrigger["central"][runRanges.name]["MuMu"]["Nominator"],shelvesTrigger["central"][runRanges.name]["MuMu"]["Denominator"],shelvesTrigger["central"][runRanges.name]["MuMu"]["Efficiency"],max(shelvesTrigger["central"][runRanges.name]["MuMu"]["UncertaintyUp"],shelvesTrigger["central"][runRanges.name]["MuMu"]["UncertaintyDown"]),shelvesTrigger["forward"][runRanges.name]["MuMu"]["Nominator"],shelvesTrigger["forward"][runRanges.name]["MuMu"]["Denominator"],shelvesTrigger["forward"][runRanges.name]["MuMu"]["Efficiency"],max(shelvesTrigger["forward"][runRanges.name]["MuMu"]["UncertaintyUp"],shelvesTrigger["forward"][runRanges.name]["MuMu"]["UncertaintyDown"]))	
	tableData += lineTemplate%("e$\mu$",shelvesTrigger["central"][runRanges.name]["EMu"]["Nominator"],shelvesTrigger["central"][runRanges.name]["EMu"]["Denominator"],shelvesTrigger["central"][runRanges.name]["EMu"]["Efficiency"],max(shelvesTrigger["central"][runRanges.name]["EMu"]["UncertaintyUp"],shelvesTrigger["central"][runRanges.name]["EMu"]["UncertaintyDown"]),shelvesTrigger["forward"][runRanges.name]["EMu"]["Nominator"],shelvesTrigger["forward"][runRanges.name]["EMu"]["Denominator"],shelvesTrigger["forward"][runRanges.name]["EMu"]["Efficiency"],max(shelvesTrigger["forward"][runRanges.name]["EMu"]["UncertaintyUp"],shelvesTrigger["forward"][runRanges.name]["EMu"]["UncertaintyDown"]))


	#~ tableMC += lineTemplateMC%("ee",shelvesTriggerMC["central"][runRanges.name]["EE"]["Nominator"],shelvesTriggerMC["central"][runRanges.name]["EE"]["Denominator"],shelvesTriggerMC["central"][runRanges.name]["EE"]["Efficiency"],max(shelvesTriggerMC["central"][runRanges.name]["EE"]["UncertaintyUp"],shelvesTriggerMC["central"][runRanges.name]["EE"]["UncertaintyDown"]),shelvesTriggerMC["forward"][runRanges.name]["EE"]["Nominator"],shelvesTriggerMC["forward"][runRanges.name]["EE"]["Denominator"],shelvesTriggerMC["forward"][runRanges.name]["EE"]["Efficiency"],max(shelvesTriggerMC["forward"][runRanges.name]["EE"]["UncertaintyUp"],shelvesTriggerMC["forward"][runRanges.name]["EE"]["UncertaintyDown"]))	
	#~ tableMC += lineTemplateMC%("$\mu\mu$",shelvesTriggerMC["central"][runRanges.name]["MuMu"]["Nominator"],shelvesTriggerMC["central"][runRanges.name]["MuMu"]["Denominator"],shelvesTriggerMC["central"][runRanges.name]["MuMu"]["Efficiency"],max(shelvesTriggerMC["central"][runRanges.name]["MuMu"]["UncertaintyUp"],shelvesTriggerMC["central"][runRanges.name]["MuMu"]["UncertaintyDown"]),shelvesTriggerMC["forward"][runRanges.name]["MuMu"]["Nominator"],shelvesTriggerMC["forward"][runRanges.name]["MuMu"]["Denominator"],shelvesTriggerMC["forward"][runRanges.name]["MuMu"]["Efficiency"],max(shelvesTriggerMC["forward"][runRanges.name]["MuMu"]["UncertaintyUp"],shelvesTriggerMC["forward"][runRanges.name]["MuMu"]["UncertaintyDown"]))	
	#~ tableMC += lineTemplateMC%("e$\mu$",shelvesTriggerMC["central"][runRanges.name]["EMu"]["Nominator"],shelvesTriggerMC["central"][runRanges.name]["EMu"]["Denominator"],shelvesTriggerMC["central"][runRanges.name]["EMu"]["Efficiency"],max(shelvesTriggerMC["central"][runRanges.name]["EMu"]["UncertaintyUp"],shelvesTriggerMC["central"][runRanges.name]["EMu"]["UncertaintyDown"]),shelvesTriggerMC["forward"][runRanges.name]["EMu"]["Nominator"],shelvesTriggerMC["forward"][runRanges.name]["EMu"]["Denominator"],shelvesTriggerMC["forward"][runRanges.name]["EMu"]["Efficiency"],max(shelvesTriggerMC["forward"][runRanges.name]["EMu"]["UncertaintyUp"],shelvesTriggerMC["forward"][runRanges.name]["EMu"]["UncertaintyDown"]))	


	#~ saveTable(tableTemplate%(tableData,tableMC), "TriggerEffsExclusive_Seperated")	
	saveTable(tableTemplate%(tableData), "TriggerEffsExclusive_Seperated")	

	
def main():
	
	parser = argparse.ArgumentParser(description='rMuE measurements.')
	
	parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
						  help="write tables to thesis repo.")


	args = parser.parse_args()	
	if args.write:
		import os
		for table in os.listdir("tab/"): 
			bashCommand = "cp tab/%s /home/jan/Doktorarbeit/Thesis/tab/"%table
			process = subprocess.Popen(bashCommand.split())		
	else:	
		produceRMuETable()
		produceRSFOFTable()
		produceTriggerEffTables()
		produceFactorizationTable()
		produceCombinedRSFOFTable()
		produceROutInTable()

main()

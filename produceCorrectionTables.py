import pickle
import os
import sys


from corrections import rSFOF, rEEOF, rMMOF, rOutIn, rOutInEE, rOutInMM, rMuE, rSFOFTrig, rSFOFFact
from centralConfig import zPredictions, regionsToUse, runRanges

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


def produceRSFOFTable():
	


	shelvesRSFOF = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRanges.name),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRanges.name), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRanges.name)}
	shelvesRSFOFMC = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRanges.name,MC=True),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRanges.name,MC=True), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRanges.name,MC=True)}	





	tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
 \caption{
     }
  \label{tab:rSFOF}
\begin{tabular}{l|c|c|c|c}     
 & $N_{SF}$ & $N_{OF}$ & $ %s \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
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


	
	saveTable(tableTemplate%("\Rsfof",tableCentral,tableForward), "Rsfof")

	tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
 \caption{Observed event yields in the control region and the resulting values of \Rsfof, \Reeof, and \Rmmof. The results are shown separately for the central and forward lepton selection and the same quantities derived on simulation are shown for comaprison.}
  \label{tab:rSFOF}
\begin{tabular}{l|c|c|c|c}     
 & $N_{SF}$ & $N_{OF}$ & $ \Rsfof \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
\hline
&  \multicolumn{4}{c}{Central} \\
\hline
%s 
 
    \hline 
& \multicolumn{4}{c}{Forward} \\
\hline
%s
\hline\hline
 & $N_{ee}$ & $N_{OF}$ & $ \Reeof \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
\hline
&  \multicolumn{4}{c}{Central} \\
\hline
%s 
 
    \hline 
& \multicolumn{4}{c}{Forward} \\
\hline
%s
\hline\hline
 & $N_{\mu\mu}$ & $N_{OF}$ & $ \Rmmof \pm \sigma_{stat}$ & Transfer factor $\pm \sigma_{stat}$  \\    
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


	
	saveTable(tableTemplate%(tableCentral,tableForward,tableCentralEE,tableForwardEE,tableCentralMM,tableForwardMM), "Rsfof_full")


def produceRMuETable():

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

	template = r"        %s       &  %d                   & %d              &  %.2f$\pm$%.2f$\pm$%.2f    \\" +"\n"


	shelvesROutIn = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRanges.name),"central": readPickle("rOutIn",regionsToUse.rOutIn.central.name,runRanges.name), "forward":readPickle("rOutIn",regionsToUse.rOutIn.forward.name,runRanges.name)}
	shelvesROutInMC = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRanges.name,MC=True),"central": readPickle("rOutIn",regionsToUse.rOutIn.central.name,runRanges.name,MC=True), "forward":readPickle("rOutIn",regionsToUse.rOutIn.forward.name,runRanges.name,MC=True)}

	shelvesRMuE = {"inclusive":readPickle("rMuE",regionsToUse.rMuE.inclusive.name , runRanges.name),"central": readPickle("rMuE",regionsToUse.rMuE.central.name,runRanges.name), "forward":readPickle("rMuE",regionsToUse.rMuE.forward.name,runRanges.name)}
	shelvesRMuEMC = {"inclusive":readPickle("rMuE",regionsToUse.rMuE.inclusive.name , runRanges.name,MC=True),"central": readPickle("rMuE",regionsToUse.rMuE.central.name,runRanges.name,MC=True), "forward":readPickle("rMuE",regionsToUse.rMuE.forward.name,runRanges.name,MC=True)}
	
	dataCentral = template%("Data",shelvesRMuE["central"]["nMM"],shelvesRMuE["central"]["nEE"],shelvesRMuE["central"]["rMuE"],shelvesRMuE["central"]["rMuEStatErr"],shelvesRMuE["central"]["rMuESystErr"])
	dataForward = template%("Data",shelvesRMuE["forward"]["nMM"],shelvesRMuE["forward"]["nEE"],shelvesRMuE["forward"]["rMuE"],shelvesRMuE["forward"]["rMuEStatErr"],shelvesRMuE["forward"]["rMuESystErr"])
	mcCentral = template%("MC",shelvesRMuEMC["central"]["nMM"],shelvesRMuEMC["central"]["nEE"],shelvesRMuEMC["central"]["rMuE"],shelvesRMuEMC["central"]["rMuEStatErr"],shelvesRMuEMC["central"]["rMuESystErr"])
	mcForward = template%("MC",shelvesRMuEMC["forward"]["nMM"],shelvesRMuEMC["forward"]["nEE"],shelvesRMuEMC["forward"]["rMuE"],shelvesRMuEMC["forward"]["rMuEStatErr"],shelvesRMuEMC["forward"]["rMuESystErr"])
	table = tableTemplate%(dataCentral,mcCentral,dataForward,mcForward)
	
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


	saveTable(tableTemplate%(tableCentralLowMass,tableCentralHighMass,tableForwardLowMass,tableForwardHighMass), "ROutIn")

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


	
	saveTable(tableTemplate%(tableCentralLowMass,tableCentralHighMass,tableForwardLowMass,tableForwardHighMass,tableCentralEELowMass,tableCentralEEHighMass,tableForwardEELowMass,tableForwardEEHighMass,tableCentralMMLowMass,tableCentralMMHighMass,tableForwardMMLowMass,tableForwardMMHighMass), "ROutIn_full")

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


	tableIngredients =""
	tableResult =""

	tableIngredients += template%("\\rmue",rMuE.central.val,rMuE.central.err,rMuE.central.valMC,rMuE.central.errMC,rMuE.forward.val,rMuE.forward.err,rMuE.forward.valMC,rMuE.forward.errMC)	
	tableIngredients += template%("$R_{T}$",rSFOFTrig.central.val,rSFOFTrig.central.err,rSFOFTrig.central.valMC,rSFOFTrig.central.errMC,rSFOFTrig.forward.val,rSFOFTrig.forward.err,rSFOFTrig.forward.valMC,rSFOFTrig.forward.errMC)	

	
	tableResult += template%("\Rsfof",rSFOFFact.central.SF.val,rSFOFFact.central.SF.err,rSFOFFact.central.SF.valMC,rSFOFFact.central.SF.errMC,rSFOFFact.forward.SF.val,rSFOFFact.forward.SF.err,rSFOFFact.forward.SF.valMC,rSFOFFact.forward.SF.errMC)	
	tableResult += template%("\Reeof",rSFOFFact.central.EE.val,rSFOFFact.central.EE.err,rSFOFFact.central.EE.valMC,rSFOFFact.central.EE.errMC,rSFOFFact.forward.EE.val,rSFOFFact.forward.EE.err,rSFOFFact.forward.EE.valMC,rSFOFFact.forward.EE.errMC)	
	tableResult += template%("\Rmmof",rSFOFFact.central.MM.val,rSFOFFact.central.MM.err,rSFOFFact.central.MM.valMC,rSFOFFact.central.MM.errMC,rSFOFFact.forward.MM.val,rSFOFFact.forward.MM.err,rSFOFFact.forward.MM.valMC,rSFOFFact.forward.MM.errMC)	



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

	
	#~ 
	#~ tableResult += template%("\Rsfof",rSFOF.central.val,rSFOF.central.err,rSFOF.central.valMC,rSFOF.central.errMC,rSFOF.forward.val,rSFOF.forward.err,rSFOF.forward.valMC,rSFOF.forward.errMC)	
	#~ tableResult += template%("\Reeof",rEEOF.central.val,rEEOF.central.err,rEEOF.central.valMC,rEEOF.central.errMC,rEEOF.forward.val,rEEOF.forward.err,rEEOF.forward.valMC,rEEOF.forward.errMC)	
	#~ tableResult += template%("\Rmmof",rMMOF.central.val,rMMOF.central.err,rMMOF.central.valMC,rMMOF.central.errMC,rMMOF.forward.val,rMMOF.forward.err,rMMOF.forward.valMC,rMMOF.forward.errMC)	
	
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
	
	saveTable(table,"rSFOF_combination_result")


def produceTriggerEffTables():


	shelvesTrigger = {"inclusive":readPickle("triggerEff",regionsToUse.triggerEfficiencies.inclusive.name , runRanges.name),"central": readPickle("triggerEff",regionsToUse.triggerEfficiencies.central.name,runRanges.name), "forward":readPickle("triggerEff",regionsToUse.triggerEfficiencies.forward.name,runRanges.name)}
	shelvesTriggerMC = {"inclusive":readPickle("triggerEff",regionsToUse.triggerEfficiencies.inclusive.name , runRanges.name,MC=True),"central": readPickle("triggerEff",regionsToUse.triggerEfficiencies.central.name,runRanges.name, MC=True), "forward":readPickle("triggerEff",regionsToUse.triggerEfficiencies.forward.name,runRanges.name,MC=True)}	



	
	tableTemplate =r"""
\begin{table}[hbp] \caption{Triggerefficiency-values for data and MC with OS, $p_T>20(20)\,\GeV$ and $H_T>200\,\GeV$ for the inclusive region.} 
\centering 
\renewcommand{\arraystretch}{1.2} 
\begin{tabular}{l|c|c|c}     

 & nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$ \\    

&\multicolumn{3}{c}{Data, Inclusive} \\
\hline
%s 
 
\end{tabular}  
\label{tab:EffValues_Inclusive}
\end{table}

\hline
& \multicolumn{3}{c}{MC, Inclusive } \\
\hline

%s    
    \hline 
"""
	lineTemplate = r"%s & %d & %d & %.3f$\pm$%.3f \\"+"\n"


	tableMC =""
	tableData =""

	
	tableData += lineTemplate%("ee",shelvesTrigger["inclusive"][runRanges.name]["EE"]["Nominator"],shelvesTrigger["inclusive"][runRanges.name]["EE"]["Denominator"],shelvesTrigger["inclusive"][runRanges.name]["EE"]["Efficiency"],max(shelvesTrigger["inclusive"][runRanges.name]["EE"]["UncertaintyUp"],shelvesTrigger["inclusive"][runRanges.name]["EE"]["UncertaintyDown"]))	
	tableData += lineTemplate%("$\mu\mu$",shelvesTrigger["inclusive"][runRanges.name]["MuMu"]["Nominator"],shelvesTrigger["inclusive"][runRanges.name]["MuMu"]["Denominator"],shelvesTrigger["inclusive"][runRanges.name]["MuMu"]["Efficiency"],max(shelvesTrigger["inclusive"][runRanges.name]["MuMu"]["UncertaintyUp"],shelvesTrigger["inclusive"][runRanges.name]["MuMu"]["UncertaintyDown"]))	
	tableData += lineTemplate%("e$\mu$",shelvesTrigger["inclusive"][runRanges.name]["EMu"]["Nominator"],shelvesTrigger["inclusive"][runRanges.name]["EMu"]["Denominator"],shelvesTrigger["inclusive"][runRanges.name]["EMu"]["Efficiency"],max(shelvesTrigger["inclusive"][runRanges.name]["EMu"]["UncertaintyUp"],shelvesTrigger["inclusive"][runRanges.name]["EMu"]["UncertaintyDown"]))



	tableMC += lineTemplate%("ee",shelvesTriggerMC["inclusive"][runRanges.name]["EE"]["Nominator"],shelvesTriggerMC["inclusive"][runRanges.name]["EE"]["Denominator"],shelvesTriggerMC["inclusive"][runRanges.name]["EE"]["Efficiency"],max(shelvesTriggerMC["inclusive"][runRanges.name]["EE"]["UncertaintyUp"],shelvesTriggerMC["inclusive"][runRanges.name]["EE"]["UncertaintyDown"]))	
	tableMC += lineTemplate%("$\mu\mu$",shelvesTriggerMC["inclusive"][runRanges.name]["MuMu"]["Nominator"],shelvesTriggerMC["inclusive"][runRanges.name]["MuMu"]["Denominator"],shelvesTriggerMC["inclusive"][runRanges.name]["MuMu"]["Efficiency"],max(shelvesTriggerMC["inclusive"][runRanges.name]["MuMu"]["UncertaintyUp"],shelvesTriggerMC["inclusive"][runRanges.name]["MuMu"]["UncertaintyDown"]))	
	tableMC += lineTemplate%("e$\mu$",shelvesTriggerMC["inclusive"][runRanges.name]["EMu"]["Nominator"],shelvesTriggerMC["inclusive"][runRanges.name]["EMu"]["Denominator"],shelvesTriggerMC["inclusive"][runRanges.name]["EMu"]["Efficiency"],max(shelvesTriggerMC["inclusive"][runRanges.name]["EMu"]["UncertaintyUp"],shelvesTriggerMC["inclusive"][runRanges.name]["EMu"]["UncertaintyDown"]))	


		
	saveTable(tableTemplate%(tableData,tableMC), "TriggerEffsExclusive_Inclusive")


# Table with Barrel and Endcap seperated


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
 


& \multicolumn{6}{c}{MC} \\
\hline
&  \multicolumn{3}{c|}{Central } & \multicolumn{3}{|c}{ Forward } \\
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


	tableMC += lineTemplateMC%("ee",shelvesTriggerMC["central"][runRanges.name]["EE"]["Nominator"],shelvesTriggerMC["central"][runRanges.name]["EE"]["Denominator"],shelvesTriggerMC["central"][runRanges.name]["EE"]["Efficiency"],max(shelvesTriggerMC["central"][runRanges.name]["EE"]["UncertaintyUp"],shelvesTriggerMC["central"][runRanges.name]["EE"]["UncertaintyDown"]),shelvesTriggerMC["forward"][runRanges.name]["EE"]["Nominator"],shelvesTriggerMC["forward"][runRanges.name]["EE"]["Denominator"],shelvesTriggerMC["forward"][runRanges.name]["EE"]["Efficiency"],max(shelvesTriggerMC["forward"][runRanges.name]["EE"]["UncertaintyUp"],shelvesTriggerMC["forward"][runRanges.name]["EE"]["UncertaintyDown"]))	
	tableMC += lineTemplateMC%("$\mu\mu$",shelvesTriggerMC["central"][runRanges.name]["MuMu"]["Nominator"],shelvesTriggerMC["central"][runRanges.name]["MuMu"]["Denominator"],shelvesTriggerMC["central"][runRanges.name]["MuMu"]["Efficiency"],max(shelvesTriggerMC["central"][runRanges.name]["MuMu"]["UncertaintyUp"],shelvesTriggerMC["central"][runRanges.name]["MuMu"]["UncertaintyDown"]),shelvesTriggerMC["forward"][runRanges.name]["MuMu"]["Nominator"],shelvesTriggerMC["forward"][runRanges.name]["MuMu"]["Denominator"],shelvesTriggerMC["forward"][runRanges.name]["MuMu"]["Efficiency"],max(shelvesTriggerMC["forward"][runRanges.name]["MuMu"]["UncertaintyUp"],shelvesTriggerMC["forward"][runRanges.name]["MuMu"]["UncertaintyDown"]))	
	tableMC += lineTemplateMC%("e$\mu$",shelvesTriggerMC["central"][runRanges.name]["EMu"]["Nominator"],shelvesTriggerMC["central"][runRanges.name]["EMu"]["Denominator"],shelvesTriggerMC["central"][runRanges.name]["EMu"]["Efficiency"],max(shelvesTriggerMC["central"][runRanges.name]["EMu"]["UncertaintyUp"],shelvesTriggerMC["central"][runRanges.name]["EMu"]["UncertaintyDown"]),shelvesTriggerMC["forward"][runRanges.name]["EMu"]["Nominator"],shelvesTriggerMC["forward"][runRanges.name]["EMu"]["Denominator"],shelvesTriggerMC["forward"][runRanges.name]["EMu"]["Efficiency"],max(shelvesTriggerMC["forward"][runRanges.name]["EMu"]["UncertaintyUp"],shelvesTriggerMC["forward"][runRanges.name]["EMu"]["UncertaintyDown"]))	


	saveTable(tableTemplate%(tableData,tableMC), "TriggerEffsExclusive_Seperated")	

	
def main():

	produceRMuETable()
	produceRSFOFTable()
	produceTriggerEffTables()
	produceFactorizationTable()
	produceCombinedRSFOFTable()
	produceROutInTable()

main()

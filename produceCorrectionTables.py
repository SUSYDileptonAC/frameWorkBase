import pickle
import os
import sys


#~ from corrections import rSFOF, rEEOF, rMMOF, rOutIn, rOutInEE, rOutInMM, rMuE, rSFOFTrig, rSFOFFactOld
from corrections import rSFOF, rEEOF, rMMOF, rOutIn, rMuE, rSFOFTrig, rSFOFFactOld
from centralConfig import zPredictions, regionsToUse, runRanges, baselineTrigger,systematics
from helpers import ensurePathExists
import argparse 
import subprocess

massRanges = {
                        "mass20To60":"20-60",
                        "mass60To86":"60-86",
                        "mass96To150":"96-150",
                        "mass150To200":"150-200",
                        "mass200To300":"200-300",
                        "mass300To400":"300-400",
                        "mass400":"$>$400",
                        "edgeMass":"20-70",
                        "lowMass":"20-86",
                        "highMass":"$>$96",
                        "highMassOld":"$>$101",
                        }

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
        


        shelvesRSFOF = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRange),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRange), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRange)}
        shelvesRSFOFMC = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRange,MC=True),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRange,MC=True), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRange,MC=True)}       





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


        
        saveTable(tableTemplate%(tableCentral,tableForward), "Rsfof_seperated_%s"%(runRange))


        tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
 \caption{Observed event yields in the control region and the resulting values of \Rsfof, \Reeof, and \Rmmof. 
 The results are shown separately for the central and forward lepton selection and the same quantities derived on simulation are shown for comparison.}
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


        
        saveTable(tableTemplate%(tableCentral,tableForward,tableCentralEE,tableForwardEE,tableCentralMM,tableForwardMM), "Rsfof_full_seperated_%s"%(runRange))

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
 and $R_{\mu\mu/OF}$ for both data and MC. The transfer factor is defined as the ratio of $R_{SF/OF}$
 in the signal region devided by $R_{SF/OF}$ in the control region.}
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
        

        
        saveTable(tableTemplate%(table,tableEE,tableMM,), "Rsfof_full_%s"%(runRange))


def produceRMuETable():


        template = r"        %s       &  %d                   & %d              &  %.3f$\pm$%.3f$\pm$%.3f    \\" +"\n"
        
        shelvesRMuE = {"inclusive":readPickle("rMuE",regionsToUse.rMuE.inclusive.name , runRange),"central": readPickle("rMuE",regionsToUse.rMuE.central.name,runRange), "forward":readPickle("rMuE",regionsToUse.rMuE.forward.name,runRange)}
        shelvesRMuEMC = {"inclusive":readPickle("rMuE",regionsToUse.rMuE.inclusive.name , runRange,MC=True),"central": readPickle("rMuE",regionsToUse.rMuE.central.name,runRange,MC=True), "forward":readPickle("rMuE",regionsToUse.rMuE.forward.name,runRange,MC=True)}

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
        
        dataCentral = template%("Data",shelvesRMuE["central"]["nMM"],shelvesRMuE["central"]["nEE"],shelvesRMuE["central"]["rMuE"],shelvesRMuE["central"]["rMuEStatErr"],shelvesRMuE["central"]["rMuESystErrOld"])
        dataForward = template%("Data",shelvesRMuE["forward"]["nMM"],shelvesRMuE["forward"]["nEE"],shelvesRMuE["forward"]["rMuE"],shelvesRMuE["forward"]["rMuEStatErr"],shelvesRMuE["forward"]["rMuESystErrOld"])
        mcCentral = template%("MC",shelvesRMuEMC["central"]["nMM"],shelvesRMuEMC["central"]["nEE"],shelvesRMuEMC["central"]["rMuE"],shelvesRMuEMC["central"]["rMuEStatErr"],shelvesRMuEMC["central"]["rMuESystErrOld"])
        mcForward = template%("MC",shelvesRMuEMC["forward"]["nMM"],shelvesRMuEMC["forward"]["nEE"],shelvesRMuEMC["forward"]["rMuE"],shelvesRMuEMC["forward"]["rMuEStatErr"],shelvesRMuEMC["forward"]["rMuESystErrOld"])
        table = tableTemplate%(dataCentral,mcCentral,dataForward,mcForward)
        
        saveTable(table,"rMuE_result_seperated_%s"%(runRange))

        tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \centering
 \caption{Result of the calculation of \rmue. Shown are the observed event yields in the Drell-Yan control region
 in the $e^{+}e^{-}$ and $\mu^{+}\mu^{-}$ channels and the resulting values for \rmue. The same quantities derived
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
        
        data = template%("Data",shelvesRMuE["inclusive"]["nMM"],shelvesRMuE["inclusive"]["nEE"],shelvesRMuE["inclusive"]["rMuE"],shelvesRMuE["inclusive"]["rMuEStatErr"],shelvesRMuE["inclusive"]["rMuESystErrOld"])
        mc = template%("MC",shelvesRMuEMC["inclusive"]["nMM"],shelvesRMuEMC["inclusive"]["nEE"],shelvesRMuEMC["inclusive"]["rMuE"],shelvesRMuEMC["inclusive"]["rMuEStatErr"],shelvesRMuEMC["inclusive"]["rMuESystErrOld"])
        table = tableTemplate%(data,mc)
        
        saveTable(table,"rMuE_result_%s"%(runRange))
        
        
        templateFitParameters = r"        %s       &  %.3f$\pm$%.3f  &  %.2f$\pm$%.2f    \\" +"\n"
        
        shelvesRMuEFitParameters = {"inclusive":readPickle("rMuE_correctionParameters",regionsToUse.rMuE.inclusive.name , runRange),"central": readPickle("rMuE_correctionParameters",regionsToUse.rMuE.central.name,runRange), "forward":readPickle("rMuE_correctionParameters",regionsToUse.rMuE.forward.name,runRange)}
        shelvesRMuEFitParametersMC = {"inclusive":readPickle("rMuE_correctionParameters",regionsToUse.rMuE.inclusive.name , runRange,MC=True),"central": readPickle("rMuE_correctionParameters",regionsToUse.rMuE.central.name,runRange,MC=True), "forward":readPickle("rMuE_correctionParameters",regionsToUse.rMuE.forward.name,runRange,MC=True)}

        
        
        tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \centering
 \caption{Result of the fit of \\rmue as a function of the \pt of the trailing lepton in the Drell--Yan control region for the central and forward lepton selection. 
 The same quantaties derived from simulation are shown for comparison. Only statistical uncertainties are given.}
  \label{tab:rMuEFitParameters}
  \\begin{tabular}{l| cc }

                                                        & $a$ & $b$ \\\\ \n    
    \hline
                                                        & \multicolumn{2}{c}{Central}  \\\\ \n
    \hline
%s
%s
\hline
                                                        & \multicolumn{2}{c}{Forward}  \\\\ \n
    \hline
%s
%s
  \end{tabular}
\end{table}


"""
        
        dataCentral = templateFitParameters%("Data",shelvesRMuEFitParameters["central"]["offset"],shelvesRMuEFitParameters["central"]["offsetErr"],shelvesRMuEFitParameters["central"]["falling"],shelvesRMuEFitParameters["central"]["fallingErr"])
        dataForward = templateFitParameters%("Data",shelvesRMuEFitParameters["forward"]["offset"],shelvesRMuEFitParameters["forward"]["offsetErr"],shelvesRMuEFitParameters["forward"]["falling"],shelvesRMuEFitParameters["forward"]["fallingErr"])
        mcCentral = templateFitParameters%("MC",shelvesRMuEFitParametersMC["central"]["offset"],shelvesRMuEFitParametersMC["central"]["offsetErr"],shelvesRMuEFitParametersMC["central"]["falling"],shelvesRMuEFitParametersMC["central"]["fallingErr"])
        mcForward = templateFitParameters%("MC",shelvesRMuEFitParametersMC["forward"]["offset"],shelvesRMuEFitParametersMC["forward"]["offsetErr"],shelvesRMuEFitParametersMC["forward"]["falling"],shelvesRMuEFitParametersMC["forward"]["fallingErr"])
        table = tableTemplate%(dataCentral,mcCentral,dataForward,mcForward)
        
        saveTable(table,"rMuE_fitParameters_seperated_%s"%(runRange))

        tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \centering
 \caption{Result of the fit of \\rmue as a function of the \pt of the trailing lepton in the Drell--Yan control region. 
 The same quantaties derived from simulation are shown for comparison. Only statistical uncertainties are given.}
   \label{tab:rMuEFitParameters}
  \\begin{tabular}{l| cc }

                                                        & $a$ & $b$ \\\\ \n    
    \hline
%s
%s
  \end{tabular}
\end{table}


"""
        
        data = templateFitParameters%("Data",shelvesRMuEFitParameters["inclusive"]["offset"],shelvesRMuEFitParameters["inclusive"]["offsetErr"],shelvesRMuEFitParameters["inclusive"]["falling"],shelvesRMuEFitParameters["inclusive"]["fallingErr"])
        mc = templateFitParameters%("MC",shelvesRMuEFitParametersMC["inclusive"]["offset"],shelvesRMuEFitParametersMC["inclusive"]["offsetErr"],shelvesRMuEFitParametersMC["inclusive"]["falling"],shelvesRMuEFitParametersMC["inclusive"]["fallingErr"])
        
        table = tableTemplate%(data,mc)
        
        saveTable(table,"rMuE_fitParameters_%s"%(runRange))



def produceROutInTable():




        shelvesROutIn = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRange),"central": readPickle("rOutIn",regionsToUse.rOutIn.central.name,runRange), "forward":readPickle("rOutIn",regionsToUse.rOutIn.forward.name,runRange)}
        shelvesROutInMC = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRange,MC=True),"central": readPickle("rOutIn",regionsToUse.rOutIn.central.name,runRange,MC=True), "forward":readPickle("rOutIn",regionsToUse.rOutIn.forward.name,runRange,MC=True)}


        tableTemplate =r"""
\begin{table}[hbtp]
 \renewcommand{\arraystretch}{1.3}
 \setlength{\belowcaptionskip}{6pt}
 \centering
 \caption{ Measured values for \rinout for data and MC in the different signal regions of the off-Z analysis. The uncertainty is dominated by
  the assigned systematic uncertainty.
     }
  \label{tab:rOutIn}
\begin{tabular}{c|c|c|c|c}
 & \multicolumn{2}{c|}{Data} & \multicolumn{2}{c}{MC}    \\ 
%s
mass range [GeV] & $N_{out}$ & $R_{out/in}$ & $N_{out}$ & $R_{out/in}$ \\    
\hline 
 %s
 %s
 %s
 %s
 %s
 %s
 %s
 \hline 
 \multicolumn{5}{c}{No MT2 cut} \\
 \hline 
 %s
 \hline 
 %s
 %s
 
  
\end{tabular}  
\end{table}
"""

        
        #~ lineTemplate = r" %s & %d$\pm$%d & %.3f$\pm$%.3f$\pm$%.3f & %d$\pm$%d & %.3f$\pm$%.3f$\pm$%.3f \\"+"\n"
        lineTemplate = r" %s & %d$\pm$%d & %.3f$\pm$%.3f & %d$\pm$%d & %.3f$\pm$%.3f \\"+"\n"
        
        peakEventLine = "& \multicolumn{2}{c|}{ $N_{in}$ %d$\pm$%d} & \multicolumn{2}{c}{ $N_{in}$ %d$\pm$%d}    \\\\"%(shelvesROutIn["inclusive"]["corrected_peak_SF"],shelvesROutIn["inclusive"]["peak_ErrorSF"],shelvesROutInMC["inclusive"]["corrected_peak_SF"],shelvesROutInMC["inclusive"]["peak_ErrorSF"])
        peakEventLineNoMT2Cut = "& \multicolumn{2}{c|}{ $N_{in}$ %d$\pm$%d} & \multicolumn{2}{c}{ $N_{in}$ %d$\pm$%d}    \\\\"%(shelvesROutIn["inclusive"]["corrected_peak_NoMT2Cut_SF"],shelvesROutIn["inclusive"]["peak_NoMT2Cut_ErrorSF"],shelvesROutInMC["inclusive"]["corrected_peak_NoMT2Cut_SF"],shelvesROutInMC["inclusive"]["peak_NoMT2Cut_ErrorSF"])
        
        lines = {}
        
        massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400","edgeMass","highMassOld"]    
        
        for massBin in massBins:        

                lines[massBin] = lineTemplate%(massRanges[massBin],
                                                                                shelvesROutIn["inclusive"]["corrected_%s_SF"%massBin],shelvesROutIn["inclusive"]["%s_ErrorSF"%massBin],                                                                         
                                                                                #~ shelvesROutIn["inclusive"]["rOutIn_%s_SF"%massBin],shelvesROutIn["inclusive"]["rOutIn_%s_ErrSF"%massBin],shelvesROutIn["inclusive"]["rOutIn_%s_SystSF"%massBin],     
                                                                                shelvesROutIn["inclusive"]["rOutIn_%s_SF"%massBin],(shelvesROutIn["inclusive"]["rOutIn_%s_SystSF"%massBin]**2 + shelvesROutIn["inclusive"]["rOutIn_%s_ErrSF"%massBin]**2)**0.5, 
                                                                                shelvesROutInMC["inclusive"]["corrected_%s_SF"%massBin],shelvesROutInMC["inclusive"]["%s_ErrorSF"%massBin],                                                                             
                                                                                #~ shelvesROutInMC["inclusive"]["rOutIn_%s_SF"%massBin],shelvesROutInMC["inclusive"]["rOutIn_%s_ErrSF"%massBin],shelvesROutInMC["inclusive"]["rOutIn_%s_SystSF"%massBin])       
                                                                                shelvesROutInMC["inclusive"]["rOutIn_%s_SF"%massBin],(shelvesROutInMC["inclusive"]["rOutIn_%s_SystSF"%massBin]**2 + shelvesROutInMC["inclusive"]["rOutIn_%s_ErrSF"%massBin]**2)**0.5)   
                                                                                
                lineEdge = lineTemplate%(massRanges["edgeMass"],
                                                                                shelvesROutIn["inclusive"]["corrected_edgeMass_NoMT2Cut_SF"],shelvesROutIn["inclusive"]["edgeMass_NoMT2Cut_ErrorSF"],                                                                           
                                                                                #~ shelvesROutIn["inclusive"]["rOutIn_edgeMass_NoMT2Cut_SF"],shelvesROutIn["inclusive"]["rOutIn_edgeMass_NoMT2Cut_ErrSF"],shelvesROutIn["inclusive"]["rOutIn_edgeMass_NoMT2Cut_SystSF"],        
                                                                                shelvesROutIn["inclusive"]["rOutIn_edgeMass_NoMT2Cut_SF"],(shelvesROutIn["inclusive"]["rOutIn_edgeMass_NoMT2Cut_SystSF"]**2 + shelvesROutIn["inclusive"]["rOutIn_edgeMass_NoMT2Cut_ErrSF"]**2)**0.5,    
                                                                                shelvesROutInMC["inclusive"]["corrected_edgeMass_NoMT2Cut_SF"],shelvesROutInMC["inclusive"]["edgeMass_NoMT2Cut_ErrorSF"],                                                                               
                                                                                #~ shelvesROutInMC["inclusive"]["rOutIn_edgeMass_NoMT2Cut_SF"],shelvesROutInMC["inclusive"]["rOutIn_edgeMass_NoMT2Cut_ErrSF"],shelvesROutInMC["inclusive"]["rOutIn_edgeMass_NoMT2Cut_SystSF"])  
                                                                                shelvesROutInMC["inclusive"]["rOutIn_edgeMass_NoMT2Cut_SF"],(shelvesROutInMC["inclusive"]["rOutIn_edgeMass_NoMT2Cut_SystSF"]**2 + shelvesROutInMC["inclusive"]["rOutIn_edgeMass_NoMT2Cut_ErrSF"]**2)**0.5)
        
                lineHighMass = lineTemplate%(massRanges["highMassOld"],
                                                                                shelvesROutIn["inclusive"]["corrected_highMassOld_NoMT2Cut_SF"],shelvesROutIn["inclusive"]["highMassOld_NoMT2Cut_ErrorSF"],                                                                             
                                                                                #~ shelvesROutIn["inclusive"]["rOutIn_highMassOld_NoMT2Cut_SF"],shelvesROutIn["inclusive"]["rOutIn_highMassOld_NoMT2Cut_ErrSF"],shelvesROutIn["inclusive"]["rOutIn_highMassOld_NoMT2Cut_SystSF"],       
                                                                                shelvesROutIn["inclusive"]["rOutIn_highMassOld_NoMT2Cut_SF"],(shelvesROutIn["inclusive"]["rOutIn_highMassOld_NoMT2Cut_SystSF"]**2 + shelvesROutIn["inclusive"]["rOutIn_highMassOld_NoMT2Cut_ErrSF"]**2)**0.5,   
                                                                                shelvesROutInMC["inclusive"]["corrected_highMassOld_NoMT2Cut_SF"],shelvesROutInMC["inclusive"]["highMassOld_NoMT2Cut_ErrorSF"],                                                                         
                                                                                #~ shelvesROutInMC["inclusive"]["rOutIn_highMassOld_NoMT2Cut_SF"],shelvesROutInMC["inclusive"]["rOutIn_highMassOld_NoMT2Cut_ErrSF"],shelvesROutInMC["inclusive"]["rOutIn_highMassOld_NoMT2Cut_SystSF"]) 
                                                                                shelvesROutInMC["inclusive"]["rOutIn_highMassOld_NoMT2Cut_SF"],(shelvesROutInMC["inclusive"]["rOutIn_highMassOld_NoMT2Cut_SystSF"]**2 + shelvesROutInMC["inclusive"]["rOutIn_highMassOld_NoMT2Cut_ErrSF"]**2)**0.5)     
        
        
        saveTable(tableTemplate%(peakEventLine,lines["mass20To60"],lines["mass60To86"],lines["mass96To150"],lines["mass150To200"],lines["mass200To300"],lines["mass300To400"],lines["mass400"],peakEventLineNoMT2Cut,lineEdge,lineHighMass), "ROutIn_%s"%(runRange))

        


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

        
        tableResult += template%("\Rsfof",rSFOFFactOld.central.SF.val,rSFOFFactOld.central.SF.err,rSFOFFactOld.central.SF.valMC,rSFOFFactOld.central.SF.errMC,rSFOFFactOld.forward.SF.val,rSFOFFactOld.forward.SF.err,rSFOFFactOld.forward.SF.valMC,rSFOFFactOld.forward.SF.errMC)      
        tableResult += template%("\Reeof",rSFOFFactOld.central.EE.val,rSFOFFactOld.central.EE.err,rSFOFFactOld.central.EE.valMC,rSFOFFactOld.central.EE.errMC,rSFOFFactOld.forward.EE.val,rSFOFFactOld.forward.EE.err,rSFOFFactOld.forward.EE.valMC,rSFOFFactOld.forward.EE.errMC)      
        tableResult += template%("\Rmmof",rSFOFFactOld.central.MM.val,rSFOFFactOld.central.MM.err,rSFOFFactOld.central.MM.valMC,rSFOFFactOld.central.MM.errMC,rSFOFFactOld.forward.MM.val,rSFOFFactOld.forward.MM.err,rSFOFFactOld.forward.MM.valMC,rSFOFFactOld.forward.MM.errMC)      



        table = tableTemplate%(tableIngredients,tableResult)
        
        saveTable(table,"factorization_result_seperated_%s"%(runRange))
        
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
        tableIngredients += template%("$\\frac{1}{2}$( \rmue + \rmue$^{-1})$",0.5*(rMuE.inclusive.val+1./rMuE.inclusive.val),0.5*(1. - (1./(rMuE.inclusive.val**2)))*rMuE.inclusive.err,0.5*(rMuE.inclusive.valMC+1./rMuE.inclusive.valMC),0.5*(1. - (1./(rMuE.inclusive.valMC**2)))*rMuE.inclusive.errMC)       
        #~ tableIngredients += template%("$R_{T}$",rSFOFTrig.inclusive.val,rSFOFTrig.inclusive.err,rSFOFTrig.inclusive.valMC,rSFOFTrig.inclusive.errMC,rSFOFTrig.forward.val,rSFOFTrig.forward.err,rSFOFTrig.forward.valMC,rSFOFTrig.forward.errMC)     
        tableIngredients += templateTrigger%("$R_{T}$",rSFOFTrig.inclusive.val,rSFOFTrig.inclusive.err) 

        
        tableResult += template%("$R_{SF/OF}$",rSFOFFactOld.inclusive.SF.val,rSFOFFactOld.inclusive.SF.err,rSFOFFactOld.inclusive.SF.valMC,rSFOFFactOld.inclusive.SF.errMC,)    
        tableResult += template%("$R_{ee/OF}$",rSFOFFactOld.inclusive.EE.val,rSFOFFactOld.inclusive.EE.err,rSFOFFactOld.inclusive.EE.valMC,rSFOFFactOld.inclusive.EE.errMC,)    
        tableResult += template%("$R_{\mu\mu/OF}$",rSFOFFactOld.inclusive.MM.val,rSFOFFactOld.inclusive.MM.err,rSFOFFactOld.inclusive.MM.valMC,rSFOFFactOld.inclusive.MM.errMC,)        



        table = tableTemplate%(tableIngredients,tableResult)
        
        saveTable(table,"factorization_result_%s"%(runRange))

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



        shelvesRSFOF = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRange),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRange), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRange)}
        shelvesRSFOFMC = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRange,MC=True),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRange,MC=True), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRange,MC=True)}       



        tableResultSF =""
        tableResultEE =""
        tableResultMM =""

        
                
        tableResultSF += template%("from factorization method",rSFOFFactOld.central.SF.val,rSFOFFactOld.central.SF.err,rSFOFFactOld.central.SF.valMC,rSFOFFactOld.central.SF.errMC,rSFOFFactOld.forward.SF.val,rSFOFFactOld.forward.SF.err,rSFOFFactOld.forward.SF.valMC,rSFOFFactOld.forward.SF.errMC) 
        tableResultSF += template%("from direct measurement",shelvesRSFOF["central"]["rSFOF"],(shelvesRSFOF["central"]["rSFOFErr"]**2+(shelvesRSFOF["central"]["rSFOF"]*systematics.rSFOF.central.val)**2)**0.5,shelvesRSFOFMC["central"]["rSFOF"],(shelvesRSFOFMC["central"]["rSFOFErr"]**2+(shelvesRSFOFMC["central"]["rSFOF"]*systematics.rSFOF.central.val)**2)**0.5,shelvesRSFOF["forward"]["rSFOF"],(shelvesRSFOF["forward"]["rSFOFErr"]**2+(shelvesRSFOF["forward"]["rSFOF"]*systematics.rSFOF.forward.val)**2)**0.5,shelvesRSFOFMC["forward"]["rSFOF"],(shelvesRSFOFMC["forward"]["rSFOFErr"]**2+(shelvesRSFOFMC["forward"]["rSFOF"]*systematics.rSFOF.forward.val)**2)**0.5)   
        tableResultSF += template%("weighted avarage",rSFOF.central.val,rSFOF.central.err,rSFOF.central.valMC,rSFOF.central.errMC,rSFOF.forward.val,rSFOF.forward.err,rSFOF.forward.valMC,rSFOF.forward.errMC)  

        
        tableResultEE += template%("from factorization method",rSFOFFactOld.central.EE.val,rSFOFFactOld.central.EE.err,rSFOFFactOld.central.EE.valMC,rSFOFFactOld.central.EE.errMC,rSFOFFactOld.forward.EE.val,rSFOFFactOld.forward.EE.err,rSFOFFactOld.forward.EE.valMC,rSFOFFactOld.forward.EE.errMC) 
        tableResultEE += template%("from direct measurement",shelvesRSFOF["central"]["rEEOF"],(shelvesRSFOF["central"]["rEEOFErr"]**2+(shelvesRSFOF["central"]["rEEOF"]*systematics.rSFOF.central.val)**2)**0.5,shelvesRSFOFMC["central"]["rEEOF"],(shelvesRSFOFMC["central"]["rEEOFErr"]**2+(shelvesRSFOFMC["central"]["rEEOF"]*systematics.rSFOF.central.val)**2)**0.5,shelvesRSFOF["forward"]["rEEOF"],(shelvesRSFOF["forward"]["rEEOFErr"]**2+(shelvesRSFOF["forward"]["rEEOF"]*systematics.rSFOF.forward.val)**2)**0.5,shelvesRSFOFMC["forward"]["rEEOF"],(shelvesRSFOFMC["forward"]["rEEOFErr"]**2+(shelvesRSFOFMC["forward"]["rEEOF"]*systematics.rSFOF.forward.val)**2)**0.5)   
        tableResultEE += template%("weighted avarage",rEEOF.central.val,rEEOF.central.err,rEEOF.central.valMC,rEEOF.central.errMC,rEEOF.forward.val,rEEOF.forward.err,rEEOF.forward.valMC,rEEOF.forward.errMC)  

        
        tableResultMM += template%("from factorization method",rSFOFFactOld.central.MM.val,rSFOFFactOld.central.MM.err,rSFOFFactOld.central.MM.valMC,rSFOFFactOld.central.MM.errMC,rSFOFFactOld.forward.MM.val,rSFOFFactOld.forward.MM.err,rSFOFFactOld.forward.MM.valMC,rSFOFFactOld.forward.MM.errMC) 
        tableResultMM += template%("from direct measurement",shelvesRSFOF["central"]["rMMOF"],(shelvesRSFOF["central"]["rMMOFErr"]**2+(shelvesRSFOF["central"]["rMMOF"]*systematics.rSFOF.central.val)**2)**0.5,shelvesRSFOFMC["central"]["rMMOF"],(shelvesRSFOFMC["central"]["rMMOFErr"]**2+(shelvesRSFOFMC["central"]["rMMOF"]*systematics.rSFOF.central.val)**2)**0.5,shelvesRSFOF["forward"]["rMMOF"],(shelvesRSFOF["forward"]["rMMOFErr"]**2+(shelvesRSFOF["forward"]["rMMOF"]*systematics.rSFOF.forward.val)**2)**0.5,shelvesRSFOFMC["forward"]["rMMOF"],(shelvesRSFOFMC["forward"]["rMMOFErr"]**2+(shelvesRSFOFMC["forward"]["rMMOF"]*systematics.rSFOF.forward.val)**2)**0.5)   
        tableResultMM += template%("weighted avarage",rMMOF.central.val,rMMOF.central.err,rMMOF.central.valMC,rMMOF.central.errMC,rMMOF.forward.val,rMMOF.forward.err,rMMOF.forward.valMC,rMMOF.forward.errMC)  



        table = tableTemplate%(tableResultSF,tableResultEE,tableResultMM)
        
        saveTable(table,"rSFOF_combinationOld_result_seperated")

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

        tableResultSF += template%("from factorization method",rSFOFFactOld.inclusive.SF.val,rSFOFFactOld.inclusive.SF.err,rSFOFFactOld.inclusive.SF.valMC,rSFOFFactOld.inclusive.SF.errMC,)    
        tableResultSF += template%("from direct measurement",shelvesRSFOF["inclusive"]["rSFOF"],(shelvesRSFOF["inclusive"]["rSFOFErr"]**2+(shelvesRSFOF["inclusive"]["rSFOF"]*systematics.rSFOF.inclusive.val)**2)**0.5,shelvesRSFOFMC["inclusive"]["rSFOF"],(shelvesRSFOFMC["inclusive"]["rSFOFErr"]**2+(shelvesRSFOFMC["inclusive"]["rSFOF"]*systematics.rSFOF.inclusive.val)**2)**0.5)       
        tableResultSF += template%("weighted avarage",rSFOF.inclusive.val,rSFOF.inclusive.err,rSFOF.inclusive.valMC,rSFOF.inclusive.errMC)      

        
        tableResultEE += template%("from factorization method",rSFOFFactOld.inclusive.EE.val,rSFOFFactOld.inclusive.EE.err,rSFOFFactOld.inclusive.EE.valMC,rSFOFFactOld.inclusive.EE.errMC,)    
        tableResultEE += template%("from direct measurement",shelvesRSFOF["inclusive"]["rEEOF"],(shelvesRSFOF["inclusive"]["rEEOFErr"]**2+(shelvesRSFOF["inclusive"]["rEEOF"]*systematics.rSFOF.inclusive.val)**2)**0.5,shelvesRSFOFMC["inclusive"]["rEEOF"],(shelvesRSFOFMC["inclusive"]["rEEOFErr"]**2+(shelvesRSFOFMC["inclusive"]["rEEOF"]*systematics.rSFOF.inclusive.val)**2)**0.5)       
        tableResultEE += template%("weighted avarage",rEEOF.inclusive.val,rEEOF.inclusive.err,rEEOF.inclusive.valMC,rEEOF.inclusive.errMC)      

        
        tableResultMM += template%("from factorization method",rSFOFFactOld.inclusive.MM.val,rSFOFFactOld.inclusive.MM.err,rSFOFFactOld.inclusive.MM.valMC,rSFOFFactOld.inclusive.MM.errMC)     
        tableResultMM += template%("from direct measurement",shelvesRSFOF["inclusive"]["rMMOF"],(shelvesRSFOF["inclusive"]["rMMOFErr"]**2+(shelvesRSFOF["inclusive"]["rMMOF"]*systematics.rSFOF.inclusive.val)**2)**0.5,shelvesRSFOFMC["inclusive"]["rMMOF"],(shelvesRSFOFMC["inclusive"]["rMMOFErr"]**2+(shelvesRSFOFMC["inclusive"]["rMMOF"]*systematics.rSFOF.inclusive.val)**2)**0.5)       
        tableResultMM += template%("weighted avarage",rMMOF.inclusive.val,rMMOF.inclusive.err,rMMOF.inclusive.valMC,rMMOF.inclusive.errMC)      



        table = tableTemplate%(tableResultSF,tableResultEE,tableResultMM)
        
        saveTable(table,"rSFOF_combinationOld_result")


def produceTriggerEffTables():


        shelvesTrigger = {"inclusive":readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.inclusive.name , runRange, baselineTrigger.name),"central": readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.central.name,runRange, baselineTrigger.name), "forward":readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.forward.name,runRange, baselineTrigger.name)}
        shelvesTriggerMC = {"inclusive":readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.inclusive.name , runRange, baselineTrigger.name,MC=True),"central": readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.central.name,runRange, baselineTrigger.name,MC=True), "forward":readTriggerPickle("triggerEff",regionsToUse.triggerEfficiencies.forward.name,runRange, baselineTrigger.name,MC=True)}     



        tableTemplate =r"""
\begin{table}[hbp] \caption{Trigger efficiency values for data and MC with OS, $p_T>25(20)\,\GeV$ and $H_T>200\,\GeV$.} 
\centering 
\renewcommand{\arraystretch}{1.2} 
\begin{tabular}{l|c|c|c|c|c|c}  

&\multicolumn{3}{c|}{Data} &\multicolumn{3}{c}{MC} \\   

 & nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$ & nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$ \\    
\hline
%s 
\hline
%s 

 
\end{tabular}  
\label{tab:TriggerEffValues}
\end{table}

"""
        lineTemplate = r"%s & %d & %d & %.3f$\pm$%.3f & %d & %d & %.3f$\pm$%.3f \\"+"\n"
        lineTemplateRT = r"$R_{T}$ & \multicolumn{3}{c|}{%.3f$\pm$%.3f}  & \multicolumn{3}{c}{%.3f$\pm$%.3f}  \\"+"\n"


        table =""
        #~ tableData =""

        
        table += lineTemplate%("ee",
                                                                shelvesTrigger["inclusive"][runRange]["EE"]["Nominator"],
                                                                shelvesTrigger["inclusive"][runRange]["EE"]["Denominator"],
                                                                shelvesTrigger["inclusive"][runRange]["EE"]["Efficiency"],
                                                                max(shelvesTrigger["inclusive"][runRange]["EE"]["UncertaintyUp"],shelvesTrigger["inclusive"][runRange]["EE"]["UncertaintyDown"]),
                                                                shelvesTriggerMC["inclusive"][runRange]["EE"]["Nominator"],
                                                                shelvesTriggerMC["inclusive"][runRange]["EE"]["Denominator"],
                                                                shelvesTriggerMC["inclusive"][runRange]["EE"]["Efficiency"],
                                                                max(shelvesTriggerMC["inclusive"][runRange]["EE"]["UncertaintyUp"],shelvesTriggerMC["inclusive"][runRange]["EE"]["UncertaintyDown"])
                                                                )       
        table += lineTemplate%("$\mu\mu$",
                                                                shelvesTrigger["inclusive"][runRange]["MuMu"]["Nominator"],
                                                                shelvesTrigger["inclusive"][runRange]["MuMu"]["Denominator"],
                                                                shelvesTrigger["inclusive"][runRange]["MuMu"]["Efficiency"],
                                                                max(shelvesTrigger["inclusive"][runRange]["MuMu"]["UncertaintyUp"],shelvesTrigger["inclusive"][runRange]["MuMu"]["UncertaintyDown"]),
                                                                shelvesTriggerMC["inclusive"][runRange]["MuMu"]["Nominator"],
                                                                shelvesTriggerMC["inclusive"][runRange]["MuMu"]["Denominator"],
                                                                shelvesTriggerMC["inclusive"][runRange]["MuMu"]["Efficiency"],
                                                                max(shelvesTriggerMC["inclusive"][runRange]["MuMu"]["UncertaintyUp"],shelvesTriggerMC["inclusive"][runRange]["MuMu"]["UncertaintyDown"])
                                                                )       
        table += lineTemplate%("e$\mu$",
                                                                shelvesTrigger["inclusive"][runRange]["EMu"]["Nominator"],
                                                                shelvesTrigger["inclusive"][runRange]["EMu"]["Denominator"],
                                                                shelvesTrigger["inclusive"][runRange]["EMu"]["Efficiency"],
                                                                max(shelvesTrigger["inclusive"][runRange]["EMu"]["UncertaintyUp"],shelvesTrigger["inclusive"][runRange]["EMu"]["UncertaintyDown"]),
                                                                shelvesTriggerMC["inclusive"][runRange]["EMu"]["Nominator"],
                                                                shelvesTriggerMC["inclusive"][runRange]["EMu"]["Denominator"],
                                                                shelvesTriggerMC["inclusive"][runRange]["EMu"]["Efficiency"],
                                                                max(shelvesTriggerMC["inclusive"][runRange]["EMu"]["UncertaintyUp"],shelvesTriggerMC["inclusive"][runRange]["EMu"]["UncertaintyDown"])
                                                                )

        RTLine = lineTemplateRT%(
                                                                shelvesTrigger["inclusive"][runRange]["RT"],
                                                                (shelvesTrigger["inclusive"][runRange]["RTErrStat"]**2+shelvesTrigger["inclusive"][runRange]["RTErrSyst"]**2)**0.5,
                                                                shelvesTriggerMC["inclusive"][runRange]["RT"],
                                                                (shelvesTriggerMC["inclusive"][runRange]["RTErrStat"]**2+shelvesTriggerMC["inclusive"][runRange]["RTErrSyst"]**2)**0.5
                                                                )


        saveTable(tableTemplate%(table,RTLine), "TriggerEffsExclusive_Inclusive")


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
    #~ \hline 
#~ \end{tabular}  
#~ \label{tab:EffValues_Seperated}
#~ \end{table}  
#~ """
        lineTemplate = r"%s & %d & %d & %.3f$\pm$%.3f & %d & %d & %.3f$\pm$%.3f \\"+"\n"
        lineTemplateMC = r"%s & %.1f & %.1f & %.3f$\pm$%.3f & %.1f & %.1f & %.3f$\pm$%.3f \\"+"\n"
        tableMC =""
        tableData =""

        tableData += lineTemplate%("ee",shelvesTrigger["central"][runRange]["EE"]["Nominator"],shelvesTrigger["central"][runRange]["EE"]["Denominator"],shelvesTrigger["central"][runRange]["EE"]["Efficiency"],max(shelvesTrigger["central"][runRange]["EE"]["UncertaintyUp"],shelvesTrigger["central"][runRange]["EE"]["UncertaintyDown"]),shelvesTrigger["forward"][runRange]["EE"]["Nominator"],shelvesTrigger["forward"][runRange]["EE"]["Denominator"],shelvesTrigger["forward"][runRange]["EE"]["Efficiency"],max(shelvesTrigger["forward"][runRange]["EE"]["UncertaintyUp"],shelvesTrigger["forward"][runRange]["EE"]["UncertaintyDown"]))  
        tableData += lineTemplate%("$\mu\mu$",shelvesTrigger["central"][runRange]["MuMu"]["Nominator"],shelvesTrigger["central"][runRange]["MuMu"]["Denominator"],shelvesTrigger["central"][runRange]["MuMu"]["Efficiency"],max(shelvesTrigger["central"][runRange]["MuMu"]["UncertaintyUp"],shelvesTrigger["central"][runRange]["MuMu"]["UncertaintyDown"]),shelvesTrigger["forward"][runRange]["MuMu"]["Nominator"],shelvesTrigger["forward"][runRange]["MuMu"]["Denominator"],shelvesTrigger["forward"][runRange]["MuMu"]["Efficiency"],max(shelvesTrigger["forward"][runRange]["MuMu"]["UncertaintyUp"],shelvesTrigger["forward"][runRange]["MuMu"]["UncertaintyDown"]))        
        tableData += lineTemplate%("e$\mu$",shelvesTrigger["central"][runRange]["EMu"]["Nominator"],shelvesTrigger["central"][runRange]["EMu"]["Denominator"],shelvesTrigger["central"][runRange]["EMu"]["Efficiency"],max(shelvesTrigger["central"][runRange]["EMu"]["UncertaintyUp"],shelvesTrigger["central"][runRange]["EMu"]["UncertaintyDown"]),shelvesTrigger["forward"][runRange]["EMu"]["Nominator"],shelvesTrigger["forward"][runRange]["EMu"]["Denominator"],shelvesTrigger["forward"][runRange]["EMu"]["Efficiency"],max(shelvesTrigger["forward"][runRange]["EMu"]["UncertaintyUp"],shelvesTrigger["forward"][runRange]["EMu"]["UncertaintyDown"]))


        tableMC += lineTemplateMC%("ee",shelvesTriggerMC["central"][runRange]["EE"]["Nominator"],shelvesTriggerMC["central"][runRange]["EE"]["Denominator"],shelvesTriggerMC["central"][runRange]["EE"]["Efficiency"],max(shelvesTriggerMC["central"][runRange]["EE"]["UncertaintyUp"],shelvesTriggerMC["central"][runRange]["EE"]["UncertaintyDown"]),shelvesTriggerMC["forward"][runRange]["EE"]["Nominator"],shelvesTriggerMC["forward"][runRange]["EE"]["Denominator"],shelvesTriggerMC["forward"][runRange]["EE"]["Efficiency"],max(shelvesTriggerMC["forward"][runRange]["EE"]["UncertaintyUp"],shelvesTriggerMC["forward"][runRange]["EE"]["UncertaintyDown"]))      
        tableMC += lineTemplateMC%("$\mu\mu$",shelvesTriggerMC["central"][runRange]["MuMu"]["Nominator"],shelvesTriggerMC["central"][runRange]["MuMu"]["Denominator"],shelvesTriggerMC["central"][runRange]["MuMu"]["Efficiency"],max(shelvesTriggerMC["central"][runRange]["MuMu"]["UncertaintyUp"],shelvesTriggerMC["central"][runRange]["MuMu"]["UncertaintyDown"]),shelvesTriggerMC["forward"][runRange]["MuMu"]["Nominator"],shelvesTriggerMC["forward"][runRange]["MuMu"]["Denominator"],shelvesTriggerMC["forward"][runRange]["MuMu"]["Efficiency"],max(shelvesTriggerMC["forward"][runRange]["MuMu"]["UncertaintyUp"],shelvesTriggerMC["forward"][runRange]["MuMu"]["UncertaintyDown"]))    
        tableMC += lineTemplateMC%("e$\mu$",shelvesTriggerMC["central"][runRange]["EMu"]["Nominator"],shelvesTriggerMC["central"][runRange]["EMu"]["Denominator"],shelvesTriggerMC["central"][runRange]["EMu"]["Efficiency"],max(shelvesTriggerMC["central"][runRange]["EMu"]["UncertaintyUp"],shelvesTriggerMC["central"][runRange]["EMu"]["UncertaintyDown"]),shelvesTriggerMC["forward"][runRange]["EMu"]["Nominator"],shelvesTriggerMC["forward"][runRange]["EMu"]["Denominator"],shelvesTriggerMC["forward"][runRange]["EMu"]["Efficiency"],max(shelvesTriggerMC["forward"][runRange]["EMu"]["UncertaintyUp"],shelvesTriggerMC["forward"][runRange]["EMu"]["UncertaintyDown"]))        


        saveTable(tableTemplate%(tableData,tableMC), "TriggerEffsExclusive_Seperated")  
        #~ saveTable(tableTemplate%(tableData), "TriggerEffsExclusive_Seperated")       

        
def main():
        
        parser = argparse.ArgumentParser(description='Correction tables')
        
        parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
                                                  help="write tables to thesis repo.")

        parser.add_argument("-r", "--runRange", action="store", dest="runRange", default=runRanges.name,
                                                  help="which runRange to use")
        

        args = parser.parse_args()      
        global runRange 
        runRange = args.runRange
        ensurePathExists("tab/")
        if args.write:
                import os
                for table in os.listdir("tab/"): 
                        bashCommand = "cp tab/%s /home/jan/Doktorarbeit/Thesis/tab/"%table
                        process = subprocess.Popen(bashCommand.split())         
        else:   
                #produceRMuETable()
                produceRSFOFTable()
                #produceTriggerEffTables()
                produceFactorizationTable()
                #produceCombinedRSFOFTable()
                #produceROutInTable()

main()

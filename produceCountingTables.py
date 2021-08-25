import pickle
import os
import sys


from setTDRStyle import setTDRStyle

#from corrections import rSFOF, rEEOF, rMMOF, rOutIn, rSFOFDirect,rSFOFTrig
from centralConfig import zPredictions,OnlyZPredictions, OtherPredictions, regionsToUse, runRanges,systematics
from defs import theCuts, getRunRange
from corrections import corrections

import ROOT
from ROOT import TCanvas

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
        
### load pickles for the systematics
def loadPickles(path):
        from glob import glob
        result = {}
        for pklPath in glob(path):
                pklFile = open(pklPath, "r")
                result.update(pickle.load(pklFile))
        return result

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
    
def getWeightedAverage(val1,err1,val2,err2):
        
        weightedAverage = (val1/(err1**2) +val2/(err2**2))/(1./err1**2+1./err2**2)
        weightedAverageErr = 1./(1./err1**2+1./err2**2)**0.5
        
        return weightedAverage, weightedAverageErr

            
def getResultsNLL(shelves, signalRegion):
       
        NLLRegions = ["lowNLL","highNLL",]
        massRegions = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]       
        nBJetsRegions = [ "zeroBJets","oneOrMoreBJets",]
        MT2Regions = ["highMT2"]
        result = {}
        
        region = "inclusive"
        
        result["onZPrediction_highNLL_highMT2_zeroBJets"] = OnlyZPredictions.MT2.SF.zeroB.highNLL.val
        result["onZPrediction_lowNLL_highMT2_zeroBJets"] = OnlyZPredictions.MT2.SF.zeroB.lowNLL.val
        result["onZPrediction_highNLL_highMT2_zeroBJets_Err"] = OnlyZPredictions.MT2.SF.zeroB.highNLL.err
        result["onZPrediction_lowNLL_highMT2_zeroBJets_Err"] = OnlyZPredictions.MT2.SF.zeroB.lowNLL.err
        
        result["onZPrediction_highNLL_highMT2_oneOrMoreBJets"] = OnlyZPredictions.MT2.SF.oneB.highNLL.val
        result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets"] = OnlyZPredictions.MT2.SF.oneB.lowNLL.val
        result["onZPrediction_highNLL_highMT2_oneOrMoreBJets_Err"] = OnlyZPredictions.MT2.SF.oneB.highNLL.err
        result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets_Err"] = OnlyZPredictions.MT2.SF.oneB.lowNLL.err
        
        runRanges = shelves.keys()
        
        
        for selection in NLLRegions:
                result[selection] = {}
                for MT2Region in MT2Regions:
                        for nBJetsRegion in nBJetsRegions:
                                for massRegion in massRegions: 
                                        
                                        
                                        currentBin = getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.nBJetsCuts,nBJetsRegion).name+"_"+getattr(theCuts.massCuts,massRegion).name
                                        resultsBinName = "%s_%s_%s"%(MT2Region,nBJetsRegion,massRegion)
                                        
                                        print resultsBinName
                                        print currentBin
                                        result[selection]["%s_EE"%(resultsBinName)] = 0.0
                                        result[selection]["%s_MM"%(resultsBinName)] = 0.0
                                        result[selection]["%s_SF"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OF"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaled"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)] = 0.0
                                        
                                        
                                        for runRangeName in runRanges:
                                                shelve = shelves[runRangeName]
                                                
                                                
                                                result[selection]["%s_EE"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EE"]
                                                result[selection]["%s_MM"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["MM"]
                                                result[selection]["%s_SF"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EE"] + shelve[signalRegion][selection][currentBin]["MM"]
                                                result[selection]["%s_OF"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EM"]
                                                result[selection]["%s_OFRMuEScaled"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EMRMuEScaled"]
                                                
                                                
                                                runRange = getRunRange(runRangeName)
                                                RT = corrections[runRange.era].rSFOFTrig.inclusive.val
                                                RTErr = corrections[runRange.era].rSFOFTrig.inclusive.err

                                                rmuepred = shelve[signalRegion][selection][currentBin]["EMRMuEScaled"]
                                                OFRMuEScaledErrRT = shelve[signalRegion][selection][currentBin]["EMRMuEScaled"]*RTErr/RT
                                                OFRMuEScaledErrFlat = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpFlat"]-rmuepred), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownFlat"]-rmuepred))
                                                OFRMuEScaledErrPt = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpPt"]-rmuepred), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownPt"]-rmuepred))
                                                OFRMuEScaledErrEta = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpEta"]-rmuepred), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownEta"]-rmuepred))
                                                
                                                result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)] + OFRMuEScaledErrRT**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)]**2 + OFRMuEScaledErrFlat**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)]**2 + OFRMuEScaledErrPt**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)]**2 + OFRMuEScaledErrEta**2)**0.5
                                        
                                        shelve=None # safety so it is not used outside the loop
                                        
                                        yield_up = ROOT.Double(1.)
                                        yield_down = ROOT.Double(1.)
                                
                                        
                                        ## calculate poisson error for FS prediction
                                        ROOT.RooHistError.instance().getPoissonInterval(int(result[selection]["%s_OF"%(resultsBinName)]),yield_down,yield_up,1.)
                                        
                                        ## calculate poisson error for observed data
                                        yieldSF_up = ROOT.Double(1.)
                                        yieldSF_down = ROOT.Double(1.)
                                        ROOT.RooHistError.instance().getPoissonInterval(int(result[selection]["%s_SF"%(resultsBinName)]),yieldSF_down,yieldSF_up,1.)
                                        result[selection]["%s_SFUp"%(resultsBinName)] = yieldSF_up - result[selection]["%s_SF"%(resultsBinName)]
                                        result[selection]["%s_SFDown"%(resultsBinName)] = result[selection]["%s_SF"%(resultsBinName)] - yieldSF_down
                                        
                                        # fs backgrounds
                                        result[selection]["%s_PredFactSF"%(resultsBinName)] = result[selection]["%s_OFRMuEScaled"%(resultsBinName)]
                                        if result[selection]["%s_OF"%(resultsBinName)] > 0:
                                                eff_rsfof = result[selection]["%s_PredFactSF"%(resultsBinName)]/result[selection]["%s_OF"%(resultsBinName)]
                                                
                                                result[selection]["%s_PredFactStatUpSF"%(resultsBinName)] = yield_up*eff_rsfof - result[selection]["%s_PredFactSF"%(resultsBinName)]
                                                result[selection]["%s_PredFactStatDownSF"%(resultsBinName)] = result[selection]["%s_PredFactSF"%(resultsBinName)] - yield_down*eff_rsfof
                                                systErrFact = (result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)]**2)**0.5
                                                result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] = systErrFact
                                        else:
                                                result[selection]["%s_PredFactStatUpSF"%(resultsBinName)] = 1.8
                                                result[selection]["%s_PredFactStatDownSF"%(resultsBinName)] = yield_down
                                                result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] = 0
                                        
                                        if result[selection]["%s_OF"%(resultsBinName)] > 0:
                                                result[selection]["%s_RSFOF_Fact"%(resultsBinName)] = result[selection]["%s_PredFactSF"%(resultsBinName)] / result[selection]["%s_OF"%(resultsBinName)]
                                                result[selection]["%s_RSFOF_Fact_Err"%(resultsBinName)] = result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] / result[selection]["%s_OF"%(resultsBinName)]
                                        else:
                                                result[selection]["%s_RSFOF_Fact"%(resultsBinName)] = 0.
                                                result[selection]["%s_RSFOF_Fact_Err"%(resultsBinName)] = 0.
                                        
                                        result[selection]["%s_PredSF"%(resultsBinName)] = result[selection]["%s_PredFactSF"%(resultsBinName)]
                                        if result[selection]["%s_PredSF"%(resultsBinName)] > 0:
                                                result[selection]["%s_PredStatUpSF"%(resultsBinName)] = result[selection]["%s_PredFactStatUpSF"%(resultsBinName)]
                                        else:
                                                result[selection]["%s_PredStatUpSF"%(resultsBinName)] = 1.8
                                                
                                        result[selection]["%s_PredStatDownSF"%(resultsBinName)] = result[selection]["%s_PredFactStatDownSF"%(resultsBinName)] 
                                        result[selection]["%s_PredSystErrSF"%(resultsBinName)] = result[selection]["%s_PredFactSystErrSF"%(resultsBinName)]
                                        
                                        
                                        # Drell-Yan
                                        rOutIn = corrections["Combined"].rOutIn
                                        onZPredName = "onZPrediction_%s_%s_%s"%(selection,MT2Region,nBJetsRegion)
                                        onZPredErrName = "onZPrediction_%s_%s_%s_Err"%(selection,MT2Region,nBJetsRegion)
                                        
                                        result[selection]["%s_ZPredSF"%(resultsBinName)] = result[onZPredName]*getattr(getattr(rOutIn,massRegion),region).val
                                        result[selection]["%s_ZPredErrSF"%(resultsBinName)] = ((result[onZPredName]*getattr(getattr(rOutIn,massRegion),region).err)**2 + (result[onZPredErrName] * getattr(getattr(rOutIn,massRegion),region).val)**2 )**0.5

                                        # ttz,wz,zz
                                        
                                        
                                        result[selection]["%s_RarePredSF"%(resultsBinName)] = 0.0
                                        result[selection]["%s_RarePredErrSF"%(resultsBinName)] = 0.0
                                        
                                        rarePredName ="%s_%s_%s_%s"%(massRegion,selection,MT2Region,nBJetsRegion)
                                        
                                        for runRangeName in runRanges:
                                                shelve = shelves[runRangeName]
                                        
                                                rarePred = shelve["Rares"]["%s_SF"%(rarePredName)] - shelve["Rares"]["%s_OF"%(rarePredName)]
                                                rareUp = shelve["Rares"]["%s_SF_Up"%(rarePredName)] - shelve["Rares"]["%s_OF_Up"%(rarePredName)]
                                                rareDown = shelve["Rares"]["%s_SF_Down"%(rarePredName)] - shelve["Rares"]["%s_OF_Down"%(rarePredName)]
                                                
                                                result[selection]["%s_RarePredSF"%(resultsBinName)] += rarePred
                                                
                                                errRare = max(abs(rareUp-rarePred), abs(rarePred-rareDown))
                                                statErrRare = shelve["Rares"]["%s_SF_Stat"%(rarePredName)]
                                                result[selection]["%s_RarePredErrSF"%(resultsBinName)] = (result[selection]["%s_RarePredErrSF"%(resultsBinName)]**2 + errRare**2 + statErrRare**2)**0.5
                                                
                        

                                        result[selection]["%s_TotalPredSF"%(resultsBinName)] = result[selection]["%s_PredSF"%(resultsBinName)] + result[selection]["%s_ZPredSF"%(resultsBinName)] + result[selection]["%s_RarePredSF"%(resultsBinName)]
                                        result[selection]["%s_TotalPredErrUpSF"%(resultsBinName)]   = ( result[selection]["%s_PredStatUpSF"%(resultsBinName)]**2   +  result[selection]["%s_PredSystErrSF"%(resultsBinName)]**2 + result[selection]["%s_ZPredErrSF"%(resultsBinName)]**2 + result[selection]["%s_RarePredErrSF"%(resultsBinName)]**2)**0.5
                                        result[selection]["%s_TotalPredErrDownSF"%(resultsBinName)] = ( result[selection]["%s_PredStatDownSF"%(resultsBinName)]**2 +  result[selection]["%s_PredSystErrSF"%(resultsBinName)]**2 + result[selection]["%s_ZPredErrSF"%(resultsBinName)]**2 + result[selection]["%s_RarePredErrSF"%(resultsBinName)]**2)**0.5

        return result
     
     
def produceFinalTableOld(shelves):
        
        
        
        
        tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Results of the edge-search counting experiment for event yields in the signal regions.
     The statistical and systematic uncertainties are added in quadrature, except for the flavor-symmetric backgrounds.
     Low-mass refers to 20 $<$ \mll $<$ 81\GeV, high-mass to \mll $>$ 101\GeV, ttbar like to \nll < 21, non-ttbar like to \nll $geq$ 21.
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

        flavSysmTemplate = r"        Flavor-symmetric    & $%.1f\pm%.1f\pm%.1f$        & $%.1f\pm%.1f\pm%.1f$   &  $%.1f\pm%.1f\pm%.1f$  & $%.1f\pm%.1f\pm%.1f$  & $%.1f\pm%.1f\pm%.1f$  \\"+"\n"

        dyTemplate = r"            Drell--Yan          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$  \\"+"\n"
        
        totalTemplate = r"            Total estimated          & $%.1f\pm%.1f$            & $%.1f\pm%.1f$      & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ \\"+"\n"
        
        resultsNLL = getResultsNLL(shelves,"NLL")
        resultsLegacy = getResultsLegacy(shelves,"legacy")
                

        observed = observedTemplate%(resultsNLL["lowNLL"]["lowMassSF"],resultsNLL["highNLL"]["lowMassSF"],resultsNLL["lowNLL"]["highMassSF"],resultsNLL["highNLL"]["highMassSF"],resultsLegacy["edgeMassSF"])
                
        flavSym = flavSysmTemplate%(resultsNLL["lowNLL"]["lowMassPredSF"],resultsNLL["lowNLL"]["lowMassPredStatErrSF"],resultsNLL["lowNLL"]["lowMassPredSystErrSF"],resultsNLL["highNLL"]["lowMassPredSF"],resultsNLL["highNLL"]["lowMassPredStatErrSF"],resultsNLL["highNLL"]["lowMassPredSystErrSF"],resultsNLL["lowNLL"]["highMassPredSF"],resultsNLL["lowNLL"]["highMassPredStatErrSF"],resultsNLL["lowNLL"]["highMassPredSystErrSF"],resultsNLL["highNLL"]["highMassPredSF"],resultsNLL["highNLL"]["highMassPredStatErrSF"],resultsNLL["highNLL"]["highMassPredSystErrSF"],resultsLegacy["edgeMassPredSF"],resultsLegacy["edgeMassPredStatErrSF"],resultsLegacy["edgeMassPredSystErrSF"])
        
        dy = dyTemplate%(resultsNLL["lowNLL"]["lowMassZPredSF"],resultsNLL["lowNLL"]["lowMassZPredErrSF"],resultsNLL["highNLL"]["lowMassZPredSF"],resultsNLL["highNLL"]["lowMassZPredErrSF"],resultsNLL["lowNLL"]["highMassZPredSF"],resultsNLL["lowNLL"]["highMassZPredErrSF"],resultsNLL["highNLL"]["highMassZPredSF"],resultsNLL["highNLL"]["highMassZPredErrSF"],resultsLegacy["edgeMassZPredSF"],resultsLegacy["edgeMassZPredErrSF"])
                
        totalPrediction = totalTemplate%(resultsNLL["lowNLL"]["lowMassTotalPredSF"],resultsNLL["lowNLL"]["lowMassTotalPredErrSF"],resultsNLL["highNLL"]["lowMassTotalPredSF"],resultsNLL["highNLL"]["lowMassTotalPredErrSF"],resultsNLL["lowNLL"]["highMassTotalPredSF"],resultsNLL["lowNLL"]["highMassTotalPredErrSF"],resultsNLL["highNLL"]["highMassTotalPredSF"],resultsNLL["highNLL"]["highMassTotalPredErrSF"],resultsLegacy["edgeMassTotalPredSF"],resultsLegacy["edgeMassTotalPredErrSF"])


                
        table = tableTemplate%(observed,flavSym,dy,totalPrediction)
        saveTable(table,"cutNCount_Result_SF")

def produceFinalTable(shelves, blinded=False):
        
        tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Results of the edge-search counting experiment for event yields in the signal regions.
     The statistical and systematic uncertainties are added in quadrature.
     ttbar like refers to $NLL<$ 21, non-ttbar like to $NLL\geq$ 21.
     }
  \label{tab:edgeResults}
  \\begin{tabular}{c | c | c | c | c | c| c}
    \hline

$N_\\text{b-tags}$ & $m_{\\ell\\ell}$ range [GeV] & FS & DY+jets & $\mathrm{Z}+\\nu$ & Total background & Observed \\\\ \n

    \hline
\multirow{8}{*}{} & \multicolumn{6}{c}{ttbar like}  \\\\ \cline{2-7}
    
 & %s
 & %s
 & %s
 & %s
 & %s
 & %s
 & %s
\cline{2-7}
$=0$ &  \multicolumn{6}{c}{non ttbar like}   \\\\\cline{2-7}
\multirow{7}{*}{} & %s
 & %s
 & %s
 & %s
 & %s
 & %s
 & %s
\hline\hline
\multirow{8}{*}{} & \multicolumn{6}{c}{ttbar like}  \\\\ \cline{2-7}
    
 & %s
 & %s
 & %s
 & %s
 & %s
 & %s
 & %s
\cline{2-7}
$\\geq 1$ & \multicolumn{6}{c}{non ttbar like}   \\\\ \cline{2-7}

\multirow{7}{*}{} & %s
 & %s
 & %s
 & %s
 & %s
 & %s
 & %s
\hline\hline

  \end{tabular}
\end{table}


"""
        

        lineTemplate = r" %s   &  %.1f$^{+%.1f}_{-%.1f}$    & %.1f$\pm$%.1f   & %.1f$\pm$%.1f  &  %.1f$^{+%.1f}_{-%.1f}$ & %d \\"+"\n"
                
        resultsNLL = getResultsNLL(shelves,"NLL")
                
        massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
        
        lines = {}
        
        
        for massBin in massBins:
                lines["lowNLL_zeroBJets_"+massBin] = lineTemplate%(massRanges[massBin],
                                                                                                        #~ resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_PredSF"%massBin],resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_PredStatUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_PredStatDownSF"%massBin],resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_PredSystErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_PredSF"%massBin],(resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_PredStatUpSF"%massBin]**2 + resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_PredSystErrSF"%massBin]**2)**0.5,(resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_PredStatDownSF"%massBin]**2 + resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_PredSystErrSF"%massBin]**2)**0.5,
                                                                                                        resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_ZPredSF"%massBin],resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_ZPredErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_RarePredSF"%massBin],resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_RarePredErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_TotalPredSF"%massBin],resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_TotalPredErrUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_TotalPredErrDownSF"%massBin],
                                                                                                        (resultsNLL["lowNLL"]["highMT2_zeroBJets_%s_SF"%massBin] if not blinded else 0))
                
                lines["highNLL_zeroBJets_"+massBin] = lineTemplate%(massRanges[massBin],
                                                                                                        #~ resultsNLL["highNLL"]["highMT2_zeroBJets_%s_PredSF"%massBin],resultsNLL["highNLL"]["highMT2_zeroBJets_%s_PredStatUpSF"%massBin],resultsNLL["highNLL"]["highMT2_zeroBJets_%s_PredStatDownSF"%massBin],resultsNLL["highNLL"]["highMT2_zeroBJets_%s_PredSystErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_zeroBJets_%s_PredSF"%massBin],(resultsNLL["highNLL"]["highMT2_zeroBJets_%s_PredStatUpSF"%massBin]**2 + resultsNLL["highNLL"]["highMT2_zeroBJets_%s_PredSystErrSF"%massBin]**2)**0.5,(resultsNLL["highNLL"]["highMT2_zeroBJets_%s_PredStatDownSF"%massBin]**2 + resultsNLL["highNLL"]["highMT2_zeroBJets_%s_PredSystErrSF"%massBin]**2)**0.5,
                                                                                                        resultsNLL["highNLL"]["highMT2_zeroBJets_%s_ZPredSF"%massBin],resultsNLL["highNLL"]["highMT2_zeroBJets_%s_ZPredErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_zeroBJets_%s_RarePredSF"%massBin],resultsNLL["highNLL"]["highMT2_zeroBJets_%s_RarePredErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_zeroBJets_%s_TotalPredSF"%massBin],resultsNLL["highNLL"]["highMT2_zeroBJets_%s_TotalPredErrUpSF"%massBin],resultsNLL["highNLL"]["highMT2_zeroBJets_%s_TotalPredErrDownSF"%massBin],
                                                                                                        (resultsNLL["highNLL"]["highMT2_zeroBJets_%s_SF"%massBin] if not blinded else 0))
        
                lines["lowNLL_oneOrMoreBJets_"+massBin] = lineTemplate%(massRanges[massBin],
                                                                                                        #~ resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_PredSF"%massBin],resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_PredStatUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_PredStatDownSF"%massBin],resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_PredSystErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_PredSF"%massBin],(resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_PredStatUpSF"%massBin]**2 + resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_PredSystErrSF"%massBin]**2)**0.5,(resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_PredStatDownSF"%massBin]**2 + resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_PredSystErrSF"%massBin]**2)**0.5,
                                                                                                        resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_ZPredSF"%massBin],resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_ZPredErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_RarePredSF"%massBin],resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_RarePredErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_TotalPredSF"%massBin],resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_TotalPredErrUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_TotalPredErrDownSF"%massBin],
                                                                                                        (resultsNLL["lowNLL"]["highMT2_oneOrMoreBJets_%s_SF"%massBin] if not blinded else 0))
                
                lines["highNLL_oneOrMoreBJets_"+massBin] = lineTemplate%(massRanges[massBin],
                                                                                                        #~ resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_PredSF"%massBin],resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_PredStatUpSF"%massBin],resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_PredStatDownSF"%massBin],resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_PredSystErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_PredSF"%massBin],(resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_PredStatUpSF"%massBin]**2 + resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_PredSystErrSF"%massBin]**2)**0.5,(resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_PredStatDownSF"%massBin]**2 + resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_PredSystErrSF"%massBin]**2)**0.5,
                                                                                                        resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_ZPredSF"%massBin],resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_ZPredErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_RarePredSF"%massBin],resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_RarePredErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_TotalPredSF"%massBin],resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_TotalPredErrUpSF"%massBin],resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_TotalPredErrDownSF"%massBin],
                                                                                                        (resultsNLL["highNLL"]["highMT2_oneOrMoreBJets_%s_SF"%massBin] if not blinded else 0))
        
        
        
        table = tableTemplate%(
                                                        lines["lowNLL_zeroBJets_mass20To60"],lines["lowNLL_zeroBJets_mass60To86"],lines["lowNLL_zeroBJets_mass96To150"],lines["lowNLL_zeroBJets_mass150To200"],lines["lowNLL_zeroBJets_mass200To300"],lines["lowNLL_zeroBJets_mass300To400"],lines["lowNLL_zeroBJets_mass400"],
                                                        lines["highNLL_zeroBJets_mass20To60"],lines["highNLL_zeroBJets_mass60To86"],lines["highNLL_zeroBJets_mass96To150"],lines["highNLL_zeroBJets_mass150To200"],lines["highNLL_zeroBJets_mass200To300"],lines["highNLL_zeroBJets_mass300To400"],lines["highNLL_zeroBJets_mass400"],
                                                        lines["lowNLL_oneOrMoreBJets_mass20To60"],lines["lowNLL_oneOrMoreBJets_mass60To86"],lines["lowNLL_oneOrMoreBJets_mass96To150"],lines["lowNLL_oneOrMoreBJets_mass150To200"],lines["lowNLL_oneOrMoreBJets_mass200To300"],lines["lowNLL_oneOrMoreBJets_mass300To400"],lines["lowNLL_oneOrMoreBJets_mass400"],
                                                        lines["highNLL_oneOrMoreBJets_mass20To60"],lines["highNLL_oneOrMoreBJets_mass60To86"],lines["highNLL_oneOrMoreBJets_mass96To150"],lines["highNLL_oneOrMoreBJets_mass150To200"],lines["highNLL_oneOrMoreBJets_mass200To300"],lines["highNLL_oneOrMoreBJets_mass300To400"],lines["highNLL_oneOrMoreBJets_mass400"],
                                                        )
                                                        
        saveTable(table,"cutNCount_Result_SF")  

def produceROutInStudyTable(shelves):
        
        
        
        
        tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Background prediction of the edge-search counting experiment for event yields in the signal regions.
     The statistical and systematic uncertainties are added in quadrature, except for the flavor-symmetric backgrounds.
     ttbar like refers to \nll $<$ 21, non-ttbar like to \nll $\geq$ 21.
     }
  \label{tab:edgeResults}
  \\begin{tabular}{ c | c | c | c | c}
    \hline

mass range [GeV] & Flavor-symmetric & DY (template) & Rare*r$_{out/in}$ & Rare direct & tot. est. r$_{out/in}$ & tot. direct \\\\ \n

    \hline
 \multicolumn{7}{c}{ttbar like}  \\\\ \n
    \hline
%s
%s
%s
%s
%s
%s
%s
\hline
  \multicolumn{7}{c}{non ttbar like}   \\\\ \n
\hline
%s
%s
%s
%s
%s
%s
%s



  \end{tabular}
\end{table}


"""

        lineTemplate = r" %s   &  %.1f$^{+%.1f}_{-%.1f}\pm$%.1f    & %.2f$\pm$%.2f & %.2f$\pm$%.2f   & %.2f$\pm$%.2f  &  %.1f$^{+%.1f}_{-%.1f}$ &  %.1f$^{+%.1f}_{-%.1f}$ \\"+"\n"

                
        resultsNLL = getResultsNLL(shelves,"NLL")
        resultsLegacy = getResultsLegacy(shelves,"legacy")
                
        massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
        
        lines = {}
        
        
        for massBin in massBins:
                lines["lowNLL_"+massBin] = lineTemplate%(massRanges[massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_PredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredStatUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredStatDownSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredSystErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_ZPredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_ZPredErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_RarePredROutInSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_RarePredROutInErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_RarePredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_RarePredErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_TotalPredROutInSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_TotalPredROutInErrUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_TotalPredROutInErrDownSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_TotalPredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_TotalPredErrUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_TotalPredErrDownSF"%massBin]
                                                                                                        )
                
                lines["highNLL_"+massBin] = lineTemplate%(massRanges[massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_PredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredStatUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredStatDownSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredSystErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_ZPredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_ZPredErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_RarePredROutInSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_RarePredROutInErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_RarePredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_RarePredErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_TotalPredROutInSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_TotalPredROutInErrUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_TotalPredROutInErrDownSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_TotalPredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_TotalPredErrUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_TotalPredErrDownSF"%massBin]
                                                                                                        )
        
        
        
        table = tableTemplate%(
                                                        lines["lowNLL_mass20To60"],lines["lowNLL_mass60To86"],lines["lowNLL_mass96To150"],lines["lowNLL_mass150To200"],lines["lowNLL_mass200To300"],lines["lowNLL_mass300To400"],lines["lowNLL_mass400"],
                                                        lines["highNLL_mass20To60"],lines["highNLL_mass60To86"],lines["highNLL_mass96To150"],lines["highNLL_mass150To200"],lines["highNLL_mass200To300"],lines["highNLL_mass300To400"],lines["highNLL_mass400"],
                                                        
                                                        )
                                                        
        saveTable(table,"cutNCount_RareStudy_SF")       
        
        
        


def produceFlavSymTable(shelves):
        
        tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Resulting estimates for flavour-symmetric backgrounds. Given is the observed event yield in \EM events,
 the estimate in the SF channel using the event-by-event reweighting of the factorization method,  
 R$_{SF/OF}$ for the factorization method, R$_{SF/OF}$ when combining this value with the constant R$_{SF/OF}$ from
   direct measurement,  and the combined final prediction. 
   Statistical and systematic uncertainties are given separately.
     }
  \label{tab:FlavSymBackgrounds}
  \\begin{tabular}{ c | c | c | c | c | c}
    \hline

Mass range [GeV] & OF events & pred. fact. method & R$_{SF/OF}$ fact. method & comb. R$_{SF/OF}$ & pred. \\\\ \n

    \hline
 \multicolumn{6}{c}{ttbar like} \\\\ \n
    \hline
%s
%s
%s
%s
%s
%s
%s
\hline
  \multicolumn{6}{c}{non ttbar like}  \\\\ \n
\hline
%s
%s
%s
%s
%s
%s
%s
\hline
  \multicolumn{6}{c}{ICHEP legacy region}  \\\\ \n
\hline
%s
\hline
  \multicolumn{6}{c}{8 TeV legacy region}  \\\\ \n 
\hline
%s


  \end{tabular}
\end{table}


"""

        flavSysmTemplate = r" %s   & %d    & %.1f$^{+%.1f}_{-%.1f}\pm$%.1f  &  %.2f$\pm$%.2f & %.2f$\pm$%.2f & %.1f$^{+%.1f}_{-%.1f}\pm$%.1f \\"+"\n"

                
        resultsNLL = getResultsNLL(shelves,"NLL")
        resultsLegacy = getResultsLegacy(shelves,"legacy")
                
        massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
        
        lines = {}
        
        for massBin in massBins:
                lines["lowNLL_"+massBin] = flavSysmTemplate%(massRanges[massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_OF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_PredFactSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredFactStatUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredFactStatDownSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredFactSystErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_RSFOF_Fact"%massBin],resultsNLL["lowNLL"]["highMT2_%s_RSFOF_Fact_Err"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_RSFOF_Combined"%massBin],resultsNLL["lowNLL"]["highMT2_%s_RSFOF_Combined_Err"%massBin],
                                                                                                        resultsNLL["lowNLL"]["highMT2_%s_PredSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredStatUpSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredStatDownSF"%massBin],resultsNLL["lowNLL"]["highMT2_%s_PredSystErrSF"%massBin])
                
                lines["highNLL_"+massBin] = flavSysmTemplate%(massRanges[massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_OF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_PredFactSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredFactStatUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredFactStatDownSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredFactSystErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_RSFOF_Fact"%massBin],resultsNLL["highNLL"]["highMT2_%s_RSFOF_Fact_Err"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_RSFOF_Combined"%massBin],resultsNLL["highNLL"]["highMT2_%s_RSFOF_Combined_Err"%massBin],
                                                                                                        resultsNLL["highNLL"]["highMT2_%s_PredSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredStatUpSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredStatDownSF"%massBin],resultsNLL["highNLL"]["highMT2_%s_PredSystErrSF"%massBin])
                
        lines["highNLLHighMass"] = flavSysmTemplate%(massRanges["highMassOld"],
                                                                                                resultsNLL["highNLL"]["highMassOld_OF"],
                                                                                                resultsNLL["highNLL"]["highMassOld_PredFactSF"],resultsNLL["highNLL"]["highMassOld_PredFactStatUpSF"],resultsNLL["highNLL"]["highMassOld_PredFactStatDownSF"],resultsNLL["highNLL"]["highMassOld_PredFactSystErrSF"],
                                                                                                resultsNLL["highNLL"]["highMassOld_RSFOF_Fact"],resultsNLL["highNLL"]["highMassOld_RSFOF_Fact_Err"],
                                                                                                resultsNLL["highNLL"]["highMassOld_RSFOF_Combined"],resultsNLL["highNLL"]["highMassOld_RSFOF_Combined_Err"],
                                                                                                resultsNLL["highNLL"]["highMassOld_PredSF"],resultsNLL["highNLL"]["highMassOld_PredStatUpSF"],resultsNLL["highNLL"]["highMassOld_PredStatDownSF"],resultsNLL["highNLL"]["highMassOld_PredSystErrSF"])
                
        lines["EdgeMass"] = flavSysmTemplate%(massRanges["edgeMass"],
                                                                                                resultsLegacy["EdgeMassOF"],
                                                                                                resultsLegacy["EdgeMassPredFactSF"],resultsLegacy["EdgeMassPredFactStatUpSF"],resultsLegacy["EdgeMassPredFactStatDownSF"],resultsLegacy["EdgeMassPredFactSystErrSF"],
                                                                                                resultsLegacy["EdgeMassRSFOFFact"],resultsLegacy["EdgeMassRSFOFFactErr"],
                                                                                                resultsLegacy["EdgeMassRSFOFCombined"],resultsLegacy["EdgeMassRSFOFCombinedErr"],
                                                                                                resultsLegacy["EdgeMassPredSF"],resultsLegacy["EdgeMassPredStatUpSF"],resultsLegacy["EdgeMassPredStatDownSF"],resultsLegacy["EdgeMassPredSystErrSF"])
                
        table = tableTemplate%(
                                                        lines["lowNLL_mass20To60"],lines["lowNLL_mass60To86"],lines["lowNLL_mass96To150"],lines["lowNLL_mass150To200"],lines["lowNLL_mass200To300"],lines["lowNLL_mass300To400"],lines["lowNLL_mass400"],
                                                        lines["highNLL_mass20To60"],lines["highNLL_mass60To86"],lines["highNLL_mass96To150"],lines["highNLL_mass150To200"],lines["highNLL_mass200To300"],lines["highNLL_mass300To400"],lines["highNLL_mass400"],
                                                        lines["highNLLHighMass"],lines["EdgeMass"]
                                                        )
                
        saveTable(table,"cutNCount_FlavSymBkgs")        
        
def produceFlavSymTableLowMT2(shelves):
        
        tableTemplate = """
\\begin{table}[hbtp]
 \\renewcommand{\\arraystretch}{1.3}
 \setlength{\\belowcaptionskip}{6pt}
 \\small
 \centering
 \caption{Resulting estimates for flavour-symmetric backgrounds. Given is the observed event yield in \EM events and the resulting estimate in the SF channel using the factorization method,
   the control region method and the combination of both methods. 
   Statistical and systematic uncertainties are given separately.
     }
  \label{tab:FlavSymBackgrounds}
  \\begin{tabular}{ c | c | c | c | c | c | c}
    \hline

mass range [GeV] & OF events & pred. fact. method & R$_{SF/OF}$ fact. method & comb. R$_{SF/OF}$ & pred. & SF yield \\\\ \n

    \hline
 \multicolumn{7}{c}{ttbar like}  \\\\ \n
    \hline
%s
%s
%s
%s
%s
%s
%s
\hline
  \multicolumn{7}{c}{non ttbar like} \\\\ \n
\hline
%s
%s
%s
%s
%s
%s
%s



  \end{tabular}
\end{table}


"""

        flavSysmTemplate = r" %s   & %d    & %.1f$^{+%.1f}_{-%.1f}\pm$%.1f  &  %.2f$\pm$%.2f & %.2f$\pm$%.2f & %.1f$^{+%.1f}_{-%.1f}\pm$%.1f & %d \\"+"\n"

                
        resultsNLL = getResultsNLL(shelves,"NLL")
                
        massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
        
        lines = {}
        
        for massBin in massBins:
                lines["lowNLL_"+massBin] = flavSysmTemplate%(massRanges[massBin],
                                                                                                        resultsNLL["lowNLL"]["lowMT2_%s_OF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["lowMT2_%s_PredFactSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredFactStatUpSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredFactStatDownSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredFactSystErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["lowMT2_%s_RSFOF_Fact"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_RSFOF_Fact_Err"%massBin],
                                                                                                        resultsNLL["lowNLL"]["lowMT2_%s_RSFOF_Combined"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_RSFOF_Combined_Err"%massBin],
                                                                                                        resultsNLL["lowNLL"]["lowMT2_%s_PredSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredStatUpSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredStatDownSF"%massBin],resultsNLL["lowNLL"]["lowMT2_%s_PredSystErrSF"%massBin],
                                                                                                        resultsNLL["lowNLL"]["lowMT2_%s_SF"%massBin])
                
                lines["highNLL_"+massBin] = flavSysmTemplate%(massRanges[massBin],
                                                                                                        resultsNLL["highNLL"]["lowMT2_%s_OF"%massBin],
                                                                                                        resultsNLL["highNLL"]["lowMT2_%s_PredFactSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredFactStatUpSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredFactStatDownSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredFactSystErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["lowMT2_%s_RSFOF_Fact"%massBin],resultsNLL["highNLL"]["lowMT2_%s_RSFOF_Fact_Err"%massBin],
                                                                                                        resultsNLL["highNLL"]["lowMT2_%s_RSFOF_Combined"%massBin],resultsNLL["highNLL"]["lowMT2_%s_RSFOF_Combined_Err"%massBin],
                                                                                                        resultsNLL["highNLL"]["lowMT2_%s_PredSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredStatUpSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredStatDownSF"%massBin],resultsNLL["highNLL"]["lowMT2_%s_PredSystErrSF"%massBin],
                                                                                                        resultsNLL["highNLL"]["lowMT2_%s_SF"%massBin])
                
                
        table = tableTemplate%(
                                                        lines["lowNLL_mass20To60"],lines["lowNLL_mass60To86"],lines["lowNLL_mass96To150"],lines["lowNLL_mass150To200"],lines["lowNLL_mass200To300"],lines["lowNLL_mass300To400"],lines["lowNLL_mass400"],
                                                        lines["highNLL_mass20To60"],lines["highNLL_mass60To86"],lines["highNLL_mass96To150"],lines["highNLL_mass150To200"],lines["highNLL_mass200To300"],lines["highNLL_mass300To400"],lines["highNLL_mass400"],
                                                        )
                
        saveTable(table,"cutNCount_FlavSymBkgs_LowMT2") 
        
        
def main():
        
        RaresPickle2016 = loadPickles("shelves/RareOnZBG_Run2016_36fb.pkl")
        RaresPickle2017 = loadPickles("shelves/RareOnZBG_Run2017_42fb.pkl")
        RaresPickle2018 = loadPickles("shelves/RareOnZBG_Run2018_60fb.pkl")
        #RaresPickle = loadPickles("shelves/RareOnZBG_8TeVLegacy_36fb.pkl")
        
        
        name = "cutAndCount"
        countingShelves2016= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , "Run2016_36fb"),"Rares":RaresPickle2016}      
        countingShelves2017= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , "Run2017_42fb"),"Rares":RaresPickle2017}      
        countingShelves2018= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , "Run2018_60fb"),"Rares":RaresPickle2018}      
        
        countingShelves = {"Run2016_36fb": countingShelves2016,"Run2017_42fb": countingShelves2017,"Run2018_60fb": countingShelves2018}
        
        
        #produceFlavSymTable(countingShelves)
        #~ produceFlavSymTableLowMT2(countingShelves)
        produceFinalTable(countingShelves, blinded=False)
        #~ produceROutInStudyTable(countingShelves)
        
main()

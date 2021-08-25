import pickle
import os
import sys


from setTDRStyle import setTDRStyle

from corrections import corrections
#from corrections import rSFOF,rSFOFDirect,rSFOFTrig, rEEOF, rMMOF, rOutIn
from centralConfig import zPredictions, regionsToUse, runRanges, OtherPredictions, OnlyZPredictions,systematics
from helpers import createMyColors
from defs import myColors,thePlots,getPlot,theCuts,getRunRange

import ratios

from array import array

import ROOT
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphErrors, TF1, gStyle, TGraphAsymmErrors, TFile, TH2F


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
        
### load pickles for the systematics
def loadPickles(path):
        from glob import glob
        result = {}
        for pklPath in glob(path):
                pklFile = open(pklPath, "r")
                result.update(pickle.load(pklFile))
        return result

                        
def getResultsNLL(shelves, signalRegion):
       
        NLLRegions = ["lowNLL","highNLL",]
        massRegions = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]       
        nBJetsRegions = [ "zeroBJets","oneOrMoreBJets",]
        MT2Regions = ["highMT2"]
        result = {}
        
        region = "inclusive"
        
        
        runRanges = shelves.keys()
        
        for selection in NLLRegions:
                result[selection] = {}
                for MT2Region in MT2Regions:
                        for nBJetsRegion in nBJetsRegions:
                                for massRegion in massRegions: 
                                        
                                        
                                        currentBin = getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.nBJetsCuts,nBJetsRegion).name+"_"+getattr(theCuts.massCuts,massRegion).name
                                        resultsBinName = "%s_%s_%s"%(MT2Region,nBJetsRegion,massRegion)

                                        # ttz,wz,zz,rare
                                        
                                        for proc in ["TTZ", "WZ", "ZZ", "Rare"]:
                                                result[selection]["%s_Pred_%s"%(resultsBinName, proc)] = 0.0
                                                
                                                rarePredName ="%s_%s_%s_%s"%(massRegion,selection,MT2Region,nBJetsRegion)
                                                
                                                for runRangeName in runRanges:
                                                        shelve = shelves[runRangeName]
                                                        
                                                        rarePred = shelve["Rares"]["%s_bySample"%rarePredName][proc]
                                                        result[selection]["%s_Pred_%s"%(resultsBinName, proc)] += rarePred

        return result
        

        
def makeOverviewPlot(shelves, nBJetsRegion, blind = False, ratio=True): 
        resultsNLL = getResultsNLL(shelves,"NLL")
        
        hCanvas = TCanvas("hCanvas%s%s"%(ratio, nBJetsRegion), "Distribution", 1000,1000)
        
        plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
        style=setTDRStyle()
        style.SetPadBottomMargin(0.28)
        style.SetPadLeftMargin(0.13)
        style.SetTitleYOffset(0.9)
        plotPad.UseCurrentStyle()
        plotPad.Draw()  
        plotPad.cd()
        # plotPad.SetLogy()       
                
        hist = {}
        histObs = ROOT.TH1F("dummy%s"%( nBJetsRegion),"dummy",14,0,14)
        hist["TTZ"] = ROOT.TH1F("histTTZ%s"%( nBJetsRegion),"histTTZ",14,0,14)
        hist["WZ"] = ROOT.TH1F("histWZ%s"%( nBJetsRegion),"histWZ",14,0,14)
        hist["ZZ"] = ROOT.TH1F("histZZ%s"%(nBJetsRegion),"histZZ",14,0,14)
        hist["Rare"] = ROOT.TH1F("histRare%s"%(nBJetsRegion),"histRare",14,0,14)
        
        hist["TTZ"].SetFillColor(ROOT.kCyan-6)
        hist["WZ"].SetFillColor(ROOT.kGreen+2)
        hist["ZZ"].SetFillColor(ROOT.kYellow+3)
        hist["Rare"].SetFillColor(630)
        
        
        names = ["m_{ll}: 20-60 GeV","m_{ll}: 60-86 GeV","m_{ll}: 96-150 GeV","m_{ll}: 150-200 GeV","m_{ll}: 200-300 GeV","m_{ll}: 300-400 GeV","m_{ll}: > 400 GeV","m_{ll}: 20-60 GeV","m_{ll}: 60-86 GeV","m_{ll}: 96-150 GeV","m_{ll}: 150-200 GeV","m_{ll}: 200-300 GeV","m_{ll}: 300-400 GeV","m_{ll}: > 400 GeV"]
        
        for index, name in enumerate(names):
                histObs.GetXaxis().SetBinLabel(index+1,name)
                
        
        for proc in ["TTZ", "WZ", "ZZ", "Rare"]:
                hist[proc].SetFillStyle(1001)
                hist[proc].SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_Pred_%s"%(nBJetsRegion, proc)])     
                
                hist[proc].SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_Pred_%s"%(nBJetsRegion, proc)])
                hist[proc].SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_Pred_%s"%(nBJetsRegion, proc)])   

        
        from ROOT import THStack
        
        stack = THStack()
        stack.Add(hist["Rare"])       
        stack.Add(hist["TTZ"])             
        stack.Add(hist["ZZ"])       
        stack.Add(hist["WZ"]) 

        
        if "zeroBJets" in nBJetsRegion:
                histObs.GetYaxis().SetRangeUser(0,60)
        else:
                histObs.GetYaxis().SetRangeUser(0,20)
        histObs.GetYaxis().SetTitle("Events")
        histObs.SetTitleOffset(0.7, "Y")
        histObs.GetYaxis().SetTitleSize(0.1)
        histObs.LabelsOption("v")
        
        histObs.UseCurrentStyle()
        histObs.GetXaxis().SetLabelSize(0.035)
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
        latexCMSExtra.SetTextSize(0.03)
        latexCMSExtra.SetNDC(True)              
        


        intlumi = ROOT.TLatex()
        intlumi.SetTextAlign(12)
        intlumi.SetTextSize(0.03)
        intlumi.SetNDC(True)            

        latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%"137.2")
        
        cmsExtra = "#splitline{Preliminary}{Simulation}"
        #cmsExtra = ""
        latexCMS.DrawLatex(0.17,0.88,"CMS")


    

        latexCMSExtra.DrawLatex(0.17,0.84,"%s"%(cmsExtra))

        leg = ROOT.TLegend(0.37, 0.85, 0.89, 0.95,"","brNDC")
        leg.SetNColumns(4)
        leg.SetFillColor(10)
        leg.SetLineColor(10)
        leg.SetShadowColor(0)
        leg.SetBorderSize(1)
        
        for proc in ["TTZ", "WZ", "ZZ", "Rare"]:
                leg.AddEntry(hist[proc], proc,"f")
        
        
        stack.Draw("samehist")  
        

        leg.Draw("same")

        
        
        line1 = ROOT.TLine(0.54,0.28,0.54,0.7)
        line1.SetLineColor(ROOT.kBlack)
        line1.SetLineWidth(2)
        line1.SetNDC(True)
        line1.Draw("same")


        label = ROOT.TLatex()
        label.SetTextAlign(12)
        label.SetTextSize(0.06)
        label.SetTextColor(ROOT.kBlack) 
        label.SetTextAlign(22)  
        #~ label.SetTextAngle(-45)      
        label.SetNDC(True)
        label.DrawLatex(0.4,0.6,"t#bar{t} like")
        label.DrawLatex(0.7,0.6,"non t#bar{t} like")
        
        
        label.SetTextAlign(32) 
        if nBJetsRegion == "oneOrMoreBJets":
                label.DrawLatex(0.9,0.75,"n_{b} #geq 1")
        else:
                label.DrawLatex(0.9,0.75,"n_{b} = 0")

        plotPad.RedrawAxis()
        

        

        hCanvas.Print("rareOverview_%s.pdf"%(nBJetsRegion))
                
        ROOT.gROOT.Clear()
  

        
def main():
        
        #OnZPickleICHEP = loadPickles("shelves/OnZBG_ICHEPLegacy_36fb.pkl")
        #RaresPickle8TeVLegacy = loadPickles("shelves/RareOnZBG_8TeVLegacy_36fb.pkl")
        RaresPickle2016 = loadPickles("shelves/RareOnZBG_Run2016_36fb.pkl")
        RaresPickle2017 = loadPickles("shelves/RareOnZBG_Run2017_42fb.pkl")
        RaresPickle2018 = loadPickles("shelves/RareOnZBG_Run2018_60fb.pkl")
        #RaresPickle = loadPickles("shelves/RareOnZBG_8TeVLegacy_36fb.pkl")
        
        
        name = "cutAndCount"
        countingShelves2016= {"Rares":RaresPickle2016}      
        countingShelves2017= {"Rares":RaresPickle2017}      
        countingShelves2018= {"Rares":RaresPickle2018}      
        
        countingShelves = {"Run2016_36fb": countingShelves2016,"Run2017_42fb": countingShelves2017,"Run2018_60fb": countingShelves2018}
        setTDRStyle()
        makeOverviewPlot(countingShelves, "zeroBJets")
        makeOverviewPlot(countingShelves, "oneOrMoreBJets")
        
main()

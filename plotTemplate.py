import sys
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)

import ROOT
import ratios

from setTDRStyle import setTDRStyle
from helpers import *    

################## SUMMARY OF CLASS plotTemplate #######################
## Constructors:
# * plotTemplate()
#
## Methods:
# * setPrimaryPlot(plot, drawOption)
#       Plot (histogram, graph) to be drawn first with drawOption, 
#       defining the axes and boundaries, redrawn 
#       after secondary plots by default so it will be on top
#
# * addSecondaryPlot(plot, drawOption)
#       Adds plot (anything with Draw(drawOption) method in root) to 
#       list of secondary plots
#
# * clearSecondaryPlots()
#       Resets list of secondary plots
#
# * addRatioErrorByHist(self,title, histUp, histDown, color, fillStyle)
#       See the RatioGraph class
#
# * addRatioErrorBySize(self,title, size, color, fillStyle, add)
#       See the RatioGraph class
#
# * addRatioPair(nominator, denominator, color)
#       Add a pair of histograms to be drawn in the ratioGraph. Will 
#       also be used for efficiency plots.
#
# * addResidualPlot(h1, h2, range=None, color=ROOT.kBlack, markerStyle=20, markerSize=1, fillColor=ROOT.kWhite, errList=None, options="")
#       Add a residual plot to be drawn with h1 and h2. h1 can be TH1 or 
#       TGraphErrors, while h2 can also be TF1. errList can be used to 
#       apply custom errors, each entry in the list being the error to be 
#       used. A range can be defined in the format (min, max), where min 
#       max are included.
#       options:    "-" to multiply residuals by -1.
#                   "P" to create a pull plot (divide by uncertainties)
#                   "H" to draw as a histogram (without errors). fillColor 
#                       is used as the histogram bar color
#
# * clearRatioPairs()
#       Empty list of ratioPairs
#
# * draw()
#       Draw full canvas
#
# * drawCanvas()
#       Draws canvas and pads in case one does not want to use draw()
#
# * drawLatexLabels()
#       If any of the labels were changed after calling draw() or one 
#       does not want to use draw(), this can be called to (re)draw all 
#       the labels
#
# * drawRatioPlot()
#       Draws all ratio or efficiency plots that were added as ratio 
#       pairs
#
# * drawLegend()
#       Draws legend of all plots with specified labels if hasLegend is True
#
# * setFolderPath(folderName)
#       Set Name of folder in fig/ to store output
#
# * saveAs(fileName)
#       Print canvas to fileName in folder that was defined earlier, 
#       prints with all defined filetypes, so fileName should not contain 
#       file ending
#
# * clean()
#       Resets the plotTemplate, this is sometimes neccessary to clear 
#       all objects before exiting a function
#
# * addLabel(label)
#       Adds a LatexLabel to the plotTemplate. This label is accessible 
#       through the name defined for it, the name cannot be a duplicate
#       of any class member or of another label that is currently added.
#       If name is "", a default unique name is given.
#           The label will be accessible via plotTemplate.name where name
#           is the label's specified name
#
# * removeLabel(name)
#       Removes the label with the specified name from the plotTemplate.
#       It will no longer be accessible by plotTemplate.name or any other
#       plotTemplate function
#
# * getLabelNames()
#       Returns a list of all label names currently included in the 
#       plotTemplate
#
# * getLabelAttr(name, attr)
#       returns specified attribute of label with specified name.
#       Can be used instead of direct access to label object
#
# * getLabelAttr(name, attr, value)
#       sets specified attribute of label with specified name to value.
#       Can be used instead of direct access to label object
#
#
## Members for options:
# -logX,logY,logZ(bools): 
#       Draw axis with logarithmic scale, false by default
# -nDivX, nDivY (ints):
#       Set number of divisions on axes, elsewise just take from primary plot
# -maximumScale(float):
#       Maximum of plot scaled by maximum value of primary plot. Default: 1.8
# -minimumScale(float):
#       Minimum of plot scaled by minimum value of primary plot. Default: 1.0
# -minimumX/Y/Z, maximumX/Y/Z(floats):
#       Overwrites maximum scale, set minimum and maximum x/y-value 
# -labelX,labelY,labelZ(strings): 
#       Set axis title of primary plot, None (default) will not change titles of primary plot
# -marginTop, marginBottom, marginLeft, marginRight(floats): 
#       Pad outer margins
# -personalWork, preliminary, forTWIKI, plotData(bools): 
#       For text below CMS logo. Default: True, False, False, False
# -hasRatio, hasEfficiency, hasBottomWindow, hasRatio(bools): 
#       Draw ratio/efficiency/residual graph, if all are true, only ratio graph is drawn. hasBottomWindow only creates lower pad. 
#       Default: False
# -hasLegend (bool):
#       Automatically draw legend of all added plots that have specified labels
# -ratioLabel, efficiencyLabel(strings): 
#       Y-axis label of ratio/efficiency graph
# -ratioMin, ratioMax(floats):
#       Min/Max values in ratio graph
# -ratioPairs (list of tuples of histogram, histogram, color):
#       If not equal to [], will add ratios of the given pairs to the ratioPlot. Will also be used for efficiency plots.
# -redrawPrimary(bool):
#       Should primary plot be redrawn to be on top of other plots. On by default, not recommended for 2D plots
# -dilepton (string): // For legacy reasons only
#       Used dilepton combination in plot. "SF", "EE", "EMu", "MuMu" will result in predefined dilepton strings.
#       If dilepton is set to a different string, this will be used directly.
# -fileTypes (list of strings):
#       List of file endings to print the canvas into. Default: ["pdf"]
#  -cutsText(string): // For legacy reasons only
#       Text to describe cuts, for latexCuts; if not set, the label will not be drawn
#  -regionName(string): // For legacy reasons only
#       Text for label latexRegion
#  -lumiInt, (float):
#       Integrated luminosity [fb^-1]
#  ---
# Following members are for specifications about the residual plot
#  -residualLabel (string):
#       Y-axis title of residual graph
#  -residualRangeUp (float):
#       Upper bound for residual plot if set manually
#  -residualRangeLow (float):
#       Lower bound for residual plot if set manually. Default "None", so
#       -residualRangeUp will be used
#  -residualRangeMode (string):
#       "MANUAL", "AUTO" or "AUTOASYMM". If AUTO is used, the maximum 
#       values of residuals will be used (scaled by residualRangeScale [float])
#       "AUTOASYMM" allows for residual plot not centered around 0 if the 
#       distribution is asymmetric around 0. Default: "AUTO"
#  -residualZeroLineDo (bool):
#       draw line through 0. Default: True
#  -residualZeroLineWidth (float):
#       width of zero line. Default: 2.0
#  -residualZeroLineStyle (float):
#       line style of zero line. Default: 2.0
#  -residualZeroLineColor (int):
#       color of zero line. Default: ROOT.kBlack

################### SUMMARY OF CLASS LatexLabel ########################
#
# This class has the following member attributes to customize:
# -name, text, posX, posY, size, font, align, angle, color
#
# Each of these variables has a getter function with the prefix get_ which
# is used in the method draw(), which draws the LatexLabel with all defined
# options. By default, every method returns just the related attribute, but
# the functions can be overloaded by custom classes which inherit from the
# LatexLabel class. Other functions that can be overloaded are draw() and
# is_drawn() (which returns True by default)
#
# When calling the constructor, an arbitrary number of arguments with 
# specified names can be given, these arguments are then added to the object
# as attributes.
# For example, label = LatexLabel(var=1, posX = 0.5) will set label.var = 1
# and label.posX = 0.5
#
# ! When added to a plotTemplate by addLabel(), it is useful to have a unique
# name for the label in order for it to be added. If no such name is defined,
# a name is automatically generated and written to label.name. 
# ! A label which is added to plotTemplate by addLabel() also sets the value of
# self.template to the current plotTemplate, so adding the same label to 
# different plotTemplates can lead to unexpected behavior if custom functions that
# use label.template are defined.
# 
# After being added to a plotTemplate, the LatexLabel object is also accessible as
# an attribute of the plotTemplate, as long as one knows its name
#
# Existing custom LatexLabels are CMSLabel, CMSExtraLabel, CutsLabel, DileptonLabel,
# RegionLabel and LumiLabel. All of these but the first by default access members 
# of plotTemplate to define the position or text which is to be drawn, but this 
# behavior of the get_ functions is usually overwritten when setting the relevant
# variable to a custom value.
#

def countNumbersUp():
    countNumbersUp.counter += 1
    return countNumbersUp.counter
countNumbersUp.counter = 0    

#TODO implement way for more than one bottom panel
#TODO implement axis label/title size/font configuration 

class LatexLabel:
    name = ""
    latex = None
    text = ""
    posX = 0
    posY = 0
    size = 0.04
    font = 42
    align = 11
    angle = 0
    color = ROOT.kBlack
    drawn = True
    template = None
    
    def __init__(self, **kwargs):
        self.latex = ROOT.TLatex()
        for varname, value in kwargs.iteritems():
            setattr(self, varname, value)
    def get_text(self):
        return self.text
    def get_posX(self):
        return self.posX
    def get_posY(self):
        return self.posY
    def get_size(self):
        return self.size
    def get_font(self):
        return self.font
    def get_align(self):
        return self.align
    def get_color(self):
        return self.color
    def get_angle(self):
        return self.angle
    def is_drawn(self):
        return self.drawn
    def draw(self):
        if self.is_drawn():
            self.latex.SetTextSize(self.get_size())
            self.latex.SetTextFont(self.get_font())
            self.latex.SetTextColor(self.get_color())
            self.latex.SetTextAlign(self.get_align())
            self.latex.SetTextAngle(self.get_angle())
            self.latex.SetNDC(True)
            self.latex.DrawLatex(self.get_posX(), self.get_posY(), self.get_text())
        
class CMSLabel(LatexLabel):
    name = "latexCMS"
    text = "CMS"
    posX = 0.19 
    posY = 0.89
    size = 0.06
    font = 61
    
class CMSExtraLabel(LatexLabel):
    name = "latexCMSExtra"
    text = None
    posX = 0.19
    posY = 0.85
    simPosY = 0.82
    #size = 0.045
    size = 0.035
    font = 52
    
    def get_text(self):
        if self.text != None:
            return self.text
        text = ""
        if self.template.personalWork:
            #text = "Work in Progress"
            text = "Private Work"
            if not self.template.plotData:
                #text = "#splitline{Work in Progress}{Simulation}"
                text = "#splitline{Private Work}{Simulation}"
        elif not self.template.plotData:
            text = "Simulation" 
        elif self.template.preliminary:
            text = "Preliminary"
        elif self.template.forTWIKI:
            text = "Unpublished"    
        return text
    def get_posY(self):
        if self.template.personalWork and not self.template.plotData:
            return self.simPosY
        else:
            return self.posY
    def is_drawn(self):
        return self.template.personalWork or not self.template.plotData or self.template.preliminary or self.template.forTWIKI

class LumiLabel(LatexLabel):
    name = "latexLumi"
    text = None
    posX = None
    posY = 0.96
    align = 31
    
    def get_text(self):
        if self.text != None:
            return self.text
        if self.template.lumiInt == None:
            return "13 TeV"
        else:
            return "%s fb^{-1} (13 TeV)"%(self.template.lumiInt)
    
    def get_posX(self):
        if self.posX == None:
            return 1 - self.template.marginRight
        else:
            return self.posX
    
class CutsLabel(LatexLabel):
    name = "latexCuts"
    text = None
    posX = 0.92
    posY = 0.81
    size = 0.03
    align = 32
    
    def get_text(self):
        if self.text != None:
            return self.text
        if self.template.cutsText == None:
            return ""
        else:
            return self.template.cutsText
    
class RegionLabel(LatexLabel):
    name = "latexRegion"
    text = None
    posX = 0.92
    posY = 0.905
    size = 0.03
    align = 32
    
    def get_text(self):
        if self.text != None:
            return self.text
        if self.template.regionName == None:
            return ""
        else:
            return self.template.regionName
    
class DileptonLabel(LatexLabel):
    text = None
    name = "latexDilepton"
    posX = 0.92
    posY = 0.875
    size = 0.03
    align = 32
    
    def get_text(self):
        if self.text != None:
            return self.text
        if self.template.dilepton == "EE":
            return "ee"
        elif self.template.dilepton == "EMu" or self.template.dilepton == "DF" or self.template.dilepton == "OF":
            return "e#mu"
        elif self.template.dilepton == "MuMu":
            return "#mu#mu"
        elif self.template.dilepton == "SF":
            return "ee+#mu#mu"
        return ""
    

            
class plotTemplate:   
    
    def __init__(self):   
        self.pathName = "fig/"
        self.folderName = ""
        self.fileTypes = ["pdf"]
        self.dilepton = None
        
        self.logX = False
        self.logY = False
        self.logZ = False
        self.redrawPrimary = True
        self.maximumScale = 1.3
        self.minimumScale = 1.0
        self.maximumX = None
        self.minimumX = None
        self.maximumY = None
        self.minimumY = None
        self.maximumZ = None
        self.minimumZ = None
        
        self.marginLeft = 0.15
        self.marginRight = 0.05
        self.marginTop = 0.05
        self.marginBottom = 0.14
        
        self.labels = {}
        self.lumiInt = None
        self.regionName = ""
        self.cutsText = None
        ##############
        self.hasLegend = False
        self.legend = None
        self.legendColumns = 1
        self.legendPosX1 = 0.55
        self.legendPosX2 = 0.90
        self.legendPosY1 = 0.55
        self.legendPosY2 = 0.70
        self.legendFont = 42
        self.legendTextSize = 0.03
        self.legendTextColor = 1
        self.legendBorderSize = 0
        self.legendFillColor = 0
        self.legendFillStyle = 0
        ##############    
        
        self.labelX = None
        self.labelY = None
        self.labelZ = None 
        
        self.ratioLabel = "ratio"    
        self.efficiencyLabel = "efficiency"
        self.ratioMin = 0
        self.ratioMax = 2
        self.efficiencyMin = 0
        self.efficiencyMax = 1.2
        self.ratioErrsSize = []
        self.ratioErrsHist = []
        self.ratioPairs = []
        self.ratioPadHeight = 0.3
        self.hasEfficiency = False
        self.efficiencyOption = "cp"
        self.hasRatio = False
        self.hasBottomWindow = False
        self.hasResidual = False
        self.nDivX = None
        self.nDivY = None
        self.is2D = False
        
        self.residualPlots = []
        self.residualGraphs = []
        self.residualLabel = ""
        self.residualRangeUp =  3
        self.residualRangeLow = None
        self.residualRangeMode = "AUTO" # MANUAL, AUTO, AUTOASYMM
        self.residualRangeScale = 1.1 
        self.residualZeroLineDo = True
        self.residualZeroLine = None
        self.residualZeroLineWidth = 2
        self.residualZeroLineStyle = 2
        self.residualZeroLineColor = ROOT.kBlack
        
        self.forTWIKI = False
        self.preliminary = False
        self.personalWork = True
        self.plotData = False

        self.canvas = None
        self.plotPad = None
        self.ratioPad = None
        
        self.primaryPlot = None
        self.secondaryPlots = []
        
        self.ratioErrsSize = []
        self.ratioErrsHist = []
        
        self.ratioPairs = []
        setTDRStyle() 
        
        self.labels = {}
        self.addLabel(CMSLabel      ())
        self.addLabel(CMSExtraLabel ())
        self.addLabel(RegionLabel   ())
        self.addLabel(CutsLabel     ())
        self.addLabel(LumiLabel     ())
        self.addLabel(DileptonLabel ())
        
    def addRatioPair(self, nominator, denominator, color=ROOT.kBlack, markerstyle=20):
        self.ratioPairs.append((nominator, denominator, color, markerstyle))
        
    def clearRatioPairs(self):
        self.ratioPairs = []
    
    def addRatioErrorBySize(self,title, size, color, fillStyle, add,number=0):
        self.ratioErrsSize.append((title,size,color,fillStyle,add,number))

    def addRatioErrorByHist(self,title, histUp, histDown, color, fillStyle,number=0):
        self.ratioErrsHist.append((title,histUp,histDown,color,fillStyle,number))
        
    def setFolderName(self,name):
        self.folderName = name
        if name != "":
            self.pathName = "fig/%s/"%(name)
        else:
            self.pathName = "fig/"
        
    def setLabelAttr(self, name, attr, value):
        setattr(self.labels[name], attr, value)
    
    def getLabelAttr(self, name, attr):
        return getattr(self.labels[name], attr)

    def addLabel(self, label):
        label.template = self
        if label.name == "":
            label.name = "Label%s"%(countNumbersUp())
        if not hasattr(self, label.name):
            self.labels[label.name] = label
            setattr(self, label.name, label)
        else:
            print "plotTemplate Error: Label name %s is either plotTemplate attribute name or name of existing label"%(label.name)
            exit()
    
    def getLabelNames(self):
        return self.labels.keys()
    
    def removeLabel(self, name):
        if name in self.labels:
            self.labels[name].template = None
            del self.labels[name]
            delattr(self, name)
        else:
            print "plotTemplate Error: Label name to delete was not found"
            exit()
           
    def saveAs(self,fileName):
        ensurePathExists(self.pathName)
        for typ in self.fileTypes:
            self.canvas.Print(self.pathName+fileName+"."+typ)
    
    def setPrimaryPlot(self,hist, drawOption, label=None):
        self.primaryPlot = (hist, drawOption, label)
    
    def addSecondaryPlot(self,hist, drawOption="", label = None):
        self.secondaryPlots.append((hist, drawOption, label))
        
    def addResidualPlot(self, h1, h2, resRange=None, color=ROOT.kBlack, markerStyle=20, markerSize=1, fillColor=ROOT.kWhite, errList=None, options=""):
        self.residualPlots.append((h1, h2, resRange, color, markerStyle, markerSize, fillColor, errList, options))
      
    def clearSecondaryPlots(self):
        self.secondaryPlots = []
    
    def drawCanvas(self):
        self.canvas = ROOT.TCanvas("hCanvas%d"%(countNumbersUp()), "", 800,800)
        
        doRatioPad = any((self.hasRatio, self.hasEfficiency, self.hasResidual, self.hasBottomWindow))
        
        if doRatioPad:
            self.plotPad = ROOT.TPad("plotPad","plotPad",0,self.ratioPadHeight,1,1)
        else:
            self.plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
        self.plotPad.UseCurrentStyle()
        self.plotPad.Draw()  
        
        if doRatioPad:
            self.ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0,1,self.ratioPadHeight)
            self.ratioPad.UseCurrentStyle()
            self.ratioPad.Draw()
         
        if doRatioPad:
            self.plotPad.SetTopMargin    (self.marginTop)
            self.plotPad.SetLeftMargin   (self.marginLeft)
            self.plotPad.SetRightMargin  (self.marginRight)
            self.ratioPad.SetBottomMargin(self.marginBottom)
            self.ratioPad.SetLeftMargin  (self.marginLeft)
            self.ratioPad.SetRightMargin (self.marginRight)
        else:
            self.plotPad.SetTopMargin   (self.marginTop)
            self.plotPad.SetLeftMargin  (self.marginLeft)
            self.plotPad.SetRightMargin (self.marginRight)
            self.plotPad.SetBottomMargin(self.marginBottom)
            
        self.plotPad.cd()  
        
        if self.logX:
            self.plotPad.SetLogx()
            if doRatioPad:
                self.ratioPad.SetLogx()
        if self.logY:
            self.plotPad.SetLogy()
        if self.logZ:
            self.plotPad.SetLogz()
    
    def drawLatexLabels(self):
        for name, label in self.labels.iteritems():
            label.draw()
            
    def clean(self):
        for key in self.labels.keys():
            self.removeLabel(key)
        self.__init__()       
        
        #self.addLabel(CMSLabel      ())
        #self.addLabel(CMSExtraLabel ())
        #self.addLabel(RegionLabel   ())
        #self.addLabel(CutsLabel     ())
        #self.addLabel(LumiLabel     ())
        #self.addLabel(DileptonLabel ())
        
        #self.primaryPlot    = None
        #self.legend         = None
        #self.secondaryPlots = []
        #self.ratioGraphs    = []
        #self.residualGraphs  = []
        #self.residualPlots   = []
        #self.residualZeroLine= None
        #self.ratioPairs     = []
        #self.pathName       = "fig/"
        #self.folderName     = ""
        #self.canvas         = None
        #self.plotPad        = None
        #self.ratioPad       = None
        #self.hAxis          = None
        #self.axisField      = None
    
    def drawRatioPlots(self):
        if self.hasRatio or self.hasEfficiency or self.hasResidual:
            self.ratioPad.cd()
            
        if self.hasRatio:
            self.ratioGraphs = []
            self.plotPad.Update() # So that Uxmin and Uxmax are retrievable
            for nominator, denominator, color, markerstyle in self.ratioPairs:
                self.ratioGraphs.append(ratios.RatioGraph(nominator, denominator, xMin=self.plotPad.GetUxmin(), xMax=self.plotPad.GetUxmax(),title=self.ratioLabel,yMin=self.ratioMin,yMax=self.ratioMax,ndivisions=10,color=color,  adaptiveBinning=1000 ))
            for err in self.ratioErrsSize:
                self.ratioGraphs[err[5]].addErrorBySize(err[0],err[1],err[2],err[3],err[4])
            for err in self.ratioErrsHist:
                self.ratioGraphs[err[5]].addErrorByHistograms(err[0],err[1],err[2],err[3],err[4])
            for number,graph in enumerate(self.ratioGraphs):
                if number == 0:
                    graph.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
                    if self.nDivX == None:
                        graph.hAxis.GetXaxis().SetNdivisions(self.primaryPlot[0].GetXaxis().GetNdivisions())
                    else:
                        graph.hAxis.GetXaxis().SetNdivisions(self.nDivX)
                else:
                    graph.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)
                graph.graph.SetMarkerStyle(markerstyle)
                
        elif self.hasEfficiency:
            self.ratioGraphs = []
            
            self.plotPad.Update() # So that Uxmin and Uxmax are retrievable
            
            self.hAxis = ROOT.TH2F("hAxis%d"%(countNumbersUp()), "", 20, self.plotPad.GetUxmin(), self.plotPad.GetUxmax(), 10, self.efficiencyMin, self.efficiencyMax)    
            self.hAxis.GetYaxis().SetNdivisions(408)
            self.hAxis.GetYaxis().SetTitleOffset(0.4)
            self.hAxis.GetYaxis().SetTitleSize(0.15)
            self.hAxis.GetXaxis().SetLabelSize(0.0)
            self.hAxis.GetYaxis().SetLabelSize(0.15)
            if self.nDivX == None:
                self.hAxis.GetXaxis().SetNdivisions(self.primaryPlot[0].GetXaxis().GetNdivisions())
            else:
                self.hAxis.GetXaxis().SetNdivisions(self.nDivX)
            self.hAxis.GetYaxis().SetTitle(self.efficiencyLabel)
            self.hAxis.Draw("AXIS")
            for nominator, denominator, color, markerstyle in self.ratioPairs:
                tmp = ROOT.TGraphAsymmErrors(nominator,denominator, self.efficiencyOption)
                tmp.SetMarkerColor(color)
                tmp.SetLineColor(color)
                tmp.SetMarkerStyle(markerstyle)
                self.ratioGraphs.append(tmp)
                self.ratioGraphs[len(self.ratioGraphs)-1].Draw("same P")
                
        elif self.hasResidual:
            low = self.residualRangeLow if (self.residualRangeLow != None) else -self.residualRangeUp
            up  = self.residualRangeUp
            
            minRes =  100000000000.0
            maxRes = -100000000000.0
            
            self.plotPad.Update() # So that Uxmin and Uxmax are retrievable
            self.hAxis = ROOT.TH2F("hAxis%d"%(countNumbersUp()), "", 20, self.plotPad.GetUxmin(), self.plotPad.GetUxmax(), 10, low, up)    
            self.hAxis.GetYaxis().SetNdivisions(408)
            self.hAxis.GetYaxis().SetTitleOffset(0.4)
            self.hAxis.GetYaxis().SetTitleSize(0.15)
            self.hAxis.GetXaxis().SetLabelSize(0.0)
            self.hAxis.GetYaxis().SetLabelSize(0.15)
            if self.nDivX == None:
                self.hAxis.GetXaxis().SetNdivisions(self.primaryPlot[0].GetXaxis().GetNdivisions())
            else:
                self.hAxis.GetXaxis().SetNdivisions(self.nDivX)
            self.hAxis.GetYaxis().SetTitle(self.residualLabel)
            self.hAxis.Draw("AXIS")
            
            if self.residualZeroLineDo:
                self.residualZeroLine = ROOT.TLine(self.plotPad.GetUxmin(),0,self.plotPad.GetUxmax(),0)
                self.residualZeroLine.SetLineColor(self.residualZeroLineColor)
                self.residualZeroLine.SetLineWidth(self.residualZeroLineWidth)
                self.residualZeroLine.SetLineStyle(self.residualZeroLineStyle)
                self.residualZeroLine.Draw("same")
            
            self.residualGraphs = []
            
            for h1, h2, resRange, color, markerstyle, markersize, fillcolor, errList, options in self.residualPlots:
                
                tmp = ROOT.TGraphAsymmErrors()
                tmp.SetMarkerColor(color)
                tmp.SetMarkerSize(markersize)
                tmp.SetLineColor(color)
                tmp.SetFillColor(fillcolor)
                tmp.SetMarkerStyle(markerstyle)
                self.residualGraphs.append(tmp)
                
                xpos = []
                minu = []
                subt = []
                minu_err = []
                subt_err = []
                
                if h1.InheritsFrom(ROOT.TH1.Class()):
                    slope = 0
                    for i in range(1, h1.GetNbinsX()+1):
                        xPos = h1.GetBinCenter(i)
                        if resRange != None:
                            if xPos > resRange[1] or xPos < resRange[0]:
                                #tmp.SetPoint(i, xPos, 0)
                                #tmp.SetPointError(i, 0, 0, 0, 0)
                                continue
                        
                        minuent = h1.GetBinContent(i)
                        minuent_err = (h1.GetBinErrorLow(i), h1.GetBinErrorUp(i))
                        
                        if h2.InheritsFrom(ROOT.TH1.Class()):
                            subtrahent = h2.GetBinContent(h2.FindBin(xPos))
                            subtrahent_err = (h2.GetBinErrorLow(h2.FindBin(xPos)), h2.GetBinErrorUp(h2.FindBin(xPos)))
                        elif h2.InheritsFrom(ROOT.TF1.Class()):
                            subtrahent = h2.Eval(xPos)
                            slope = h2.Derivative(xPos)
                            subtrahent_err = (0,0)
                        else: 
                            print "Error in drawResiduals: Invalid type of subtrahent", h1
                            exit()
                        
                        xpos.append(xPos)
                        minu.append(minuent)
                        subt.append(subtrahent)
                        minu_err.append(minuent_err)
                        subt_err.append(subtrahent_err)
                            
                elif h1.InheritsFrom(ROOT.TGraphErrors.Class()):
                    for i in range(h1.GetN()):
                        xPos = h1.GetX()[i]
                        if resRange != None:
                            if xPos > resRange[1] or xPos < resRange[0]:
                                #tmp.SetPoint(i, xPos, 0)
                                #tmp.SetPointError(i, 0, 0, 0, 0)
                                continue

                        
                        minuent = h1.GetY()[i]
                        if h1.InheritsFrom(ROOT.TGraphAsymmErrors.Class()):
                                minuent_err = (h1.GetEYlow()[i], h1.GetEYhigh()[i])
                        else:
                                minuent_err = (h1.GetEY()[i], h1.GetEY()[i])
                                
                        if h2.InheritsFrom(ROOT.TH1.Class()):
                            subtrahent = h2.GetBinContent(h2.FindBin(xPos))
                            subtrahent_err = h2.GetBinError(h2.FindBin(xPos))
                        elif h2.InheritsFrom(ROOT.TGraphErrors.Class()):
                            subtrahent = h2.GetY()[i]
                            if h2.InheritsFrom(ROOT.TGraphAsymmErrors.Class()):
                                subtrahent_err = (h2.GetEYlow()[i], h2.GetEYhigh()[i])
                            else:
                                subtrahent_err = (h2.GetEY()[i], h2.GetEY()[i])
                        elif h2.InheritsFrom(ROOT.TF1.Class()):
                            subtrahent = h2.Eval(xPos)
                            subtrahent_err = (0,0)
                        
                        xpos.append(xPos)
                        minu.append(minuent)
                        subt.append(subtrahent)
                        minu_err.append(minuent_err)
                        subt_err.append(subtrahent_err)
                        
                
                
                else:
                    print "plotTemplate Error: in drawResiduals: Invalid type of minuent ", h2
                    exit()
                
                
                for i, (xPos, minuent, subtrahent, minuent_err, subtrahent_err) in enumerate(zip(xpos, minu, subt, minu_err, subt_err)):
                    residual = minuent - subtrahent
                    if residual >= 0:
                        i_m = 0
                        i_s = 1
                    else:
                        i_m = 1
                        i_s = 0
                        
                    residual_err = (minuent_err[i_m]**2 + subtrahent_err[i_s]**2 )**0.5
                    if errList != None:
                        residual_err = errList[i]
                    
                    if "P" in options:
                        if residual_err > 0:
                            residual /= residual_err
                            residual_err = 1
                        else:
                            residual = 0
                            residual_err = 0
                    if "-" in options:
                        residual = -residual
                    
                    if residual < minRes:
                        minRes = residual
                    if residual > maxRes:
                        maxRes = residual
                    
                    tmp.SetPoint(i, xPos, residual)
                    tmp.SetPointError(i, 0, 0, residual_err, residual_err)
                
                
                if "H" in options:
                    tmp.Draw("same BX")
                else:
                    tmp.Draw("same P")
            
            if self.residualRangeMode.upper() == "AUTO":
                boundaries = max(abs(minRes), maxRes)
                boundLow = -boundaries * self.residualRangeScale
                boundUp = boundaries * self.residualRangeScale      
                self.hAxis.GetYaxis().SetLimits(boundLow, boundUp)              
            elif self.residualRangeMode.upper() == "AUTOASYMM":
                boundLow = minRes * self.residualRangeScale
                boundUp = maxRes * self.residualRangeScale
                self.hAxis.GetYaxis().SetLimits(boundLow, boundUp)     
        
                
    
    def draw(self):
        self.drawCanvas()
        self.primaryPlot[0].Draw(self.primaryPlot[1]) # just so a THStack would have defined axes (which is not the case before drawing), will be overdrawn by axisField
        #self.is2D = self.primaryPlot[0].InheritsFrom(ROOT.TH2.Class()) 
        
        if self.minimumY == None:
            if self.is2D:
                minimumY = (self.primaryPlot[0].GetYaxis().GetBinLowEdge(1))
            else:
                minimumY = self.primaryPlot[0].GetMinimum()*self.minimumScale
        else:
            minimumY = (self.minimumY)
        
        if self.maximumY == None:
            if self.is2D:
                maximumY = (self.primaryPlot[0].GetYaxis().GetBinUpEdge(self.primaryPlot[0].GetYaxis().GetNbins()))
            else:
                maximumY = self.primaryPlot[0].GetMaximum()*self.maximumScale
        else:
            maximumY = (self.maximumY)
    
        if self.minimumX == None:
            minimumX = (self.primaryPlot[0].GetXaxis().GetBinLowEdge(1))
        else:
            minimumX = (self.minimumX)
            
        if self.maximumX == None:
            maximumX = (self.primaryPlot[0].GetXaxis().GetBinUpEdge(self.primaryPlot[0].GetXaxis().GetNbins()))
        else:
            maximumX =  (self.maximumX)
            
        if self.is2D:
            if self.minimumZ == None:
                minimumZ = (self.primaryPlot[0].GetMinimum()*self.minimumScale)
            else:
                minimumZ = (self.minimumZ)
                
            if self.maximumZ == None:
                maximumZ = (self.primaryPlot[0].GetMaximum()*self.maximumScale)
            else:
                maximumZ = (self.maximumZ)
                
        self.axisField = ROOT.TH2F("hAxis%d"%(countNumbersUp()), ";x;y;z", 20, minimumX, maximumX, 10, minimumY, maximumY)    
        
        if self.labelX != None:
            self.axisField.GetXaxis().SetTitle(self.labelX)
        else:
            self.axisField.GetXaxis().SetTitle(self.primaryPlot[0].GetXaxis().GetTitle())
        if self.labelY != None:
            self.axisField.GetYaxis().SetTitle(self.labelY)
        else:
            self.axisField.GetYaxis().SetTitle(self.primaryPlot[0].GetYaxis().GetTitle())
        if self.is2D:
            if self.labelZ != None:
                self.axisField.GetZaxis().SetTitle(self.labelZ) 
                self.primaryPlot[0].GetZaxis().SetTitle(self.labelZ) # needed because axisField does not have a z-axis
            else:
                
                self.axisField.GetZaxis().SetTitle(self.primaryPlot[0].GetZaxis().GetTitle())
            
        if self.nDivX == None:
            self.axisField.GetXaxis().SetNdivisions(self.primaryPlot[0].GetXaxis().GetNdivisions())
        else:
            self.axisField.GetXaxis().SetNdivisions(self.nDivX) 
            
        if self.nDivY == None:
            self.axisField.GetYaxis().SetNdivisions(self.primaryPlot[0].GetYaxis().GetNdivisions())
        else:
            self.axisField.GetYaxis().SetNdivisions(self.nDivY)    
        
        
        self.axisField.Draw("AXIS")
        
        self.primaryPlot[0].Draw(self.primaryPlot[1]+"same")
       
        for plot, drawStyle, label in self.secondaryPlots:
            plot.Draw(drawStyle+"same")
         
        if self.redrawPrimary:
            self.primaryPlot[0].Draw(self.primaryPlot[1]+"same")
        
        if self.is2D:
            self.axisField.GetZaxis().SetRangeUser(minimumZ,maximumZ) # This line is only needed for older ROOT versions
            self.primaryPlot[0].GetZaxis().SetRangeUser(minimumZ,maximumZ)
        else:
            self.primaryPlot[0].GetYaxis().SetRangeUser(minimumY,maximumY)
        
        self.canvas.Update()
        self.drawLatexLabels()
        
        self.drawLegend()
        
        self.plotPad.RedrawAxis()
        
        self.drawRatioPlots()
        
    
    def drawLegend(self):
        if self.hasLegend:
            if self.legend == None:
                self.legend = ROOT.TLegend(self.legendPosX1, self.legendPosY1, self.legendPosX2, self.legendPosY2)
            self.legend.SetTextSize(self.legendTextSize)
            self.legend.SetTextFont(self.legendFont)
            self.legend.SetTextColor(self.legendTextColor)
            self.legend.SetBorderSize(self.legendBorderSize)
            self.legend.SetNColumns(self.legendColumns)
            self.legend.SetFillStyle(self.legendFillStyle)
            self.legend.SetFillColor(self.legendFillColor)
            
            for plot, drawOption, label in [self.primaryPlot]+self.secondaryPlots:
                if label != None:
                    drawOpt = drawOption.replace("hist","l")
                    self.legend.AddEntry(plot, label, drawOpt)
            
            self.legend.Draw("same")
            

customColors = [(178,61,18), (178,255,26), (0,82,204), (178,0,71), (255,162,128), (102,204,129), (64,81,128), (255,128,179), (255,136,0), (46,217,230), (27,0,204), (255,26,56), (153,107,15), (64,123,128), (102,51,128), (178,170,54), (128,196,255), (217,46,230)]            
colorPosition = 0
switch = False
colors = []

def getNewColor():
    global colorPosition
    global customColors
    global colors
    global switch
    if colorPosition >= len(customColors):
        colorPosition = 0
        switch = True
    
    if not switch:
        tempColor = ROOT.TColor(2100+colorPosition, float(customColors[colorPosition][0]) / 255, float(customColors[colorPosition][1]) / 255, float(customColors[colorPosition][2]) / 255)        
        colors.append(tempColor)
        
    pos = 2100+colorPosition
    colorPosition += 1
    if colorPosition > 9:
        return colorPosition+30
    return colorPosition
    return pos
    
         
# simple example on how to create a custom template
class plotTemplate2D(plotTemplate):
    
    
    
    def __init__(self):
        plotTemplate.__init__(self)
        self.is2D = True
        self.setLabelAttr("latexRegion", "posX", 0.78)
        self.setLabelAttr("latexCuts", "posX", 0.78)
        self.setLabelAttr("latexDilepton", "posX", 0.78)
        self.marginRight = 0.2
        self.redrawPrimary = False
        self.maximumScale = 1.1
        self.minimumScale = 1.0
    

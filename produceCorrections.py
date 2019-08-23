
import pickle
import os
import sys
from centralConfig import regionsToUse, baselineTrigger, runRanges, systematics, triggerRegionNamesLists

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

def getROutInClass(classTemplate,shelve,shelveMC,massRange,combination,label):
        return classTemplate%(label,shelve[label]["rOutIn_%s_%s"%(massRange,combination)],( shelve[label]["rOutIn_%s_Syst%s"%(massRange,combination)]**2 + shelve[label]["rOutIn_%s_Err%s"%(massRange,combination)]**2 )**0.5 , shelveMC[label]["rOutIn_%s_%s"%(massRange,combination)],( shelveMC[label]["rOutIn_%s_Syst%s"%(massRange,combination)]**2 + shelveMC[label]["rOutIn_%s_Err%s"%(massRange,combination)]**2 )**0.5)        


def getTriggerClass(classTemplate,shelve,shelveMC,combination,label,year):
#~ def getTriggerClass(classTemplate,shelve,combination,label):
        
        
        if combination == "EE":
                otherLabel = "effEE"
        elif combination == "MuMu":
                otherLabel = "effMM"
        else:
                otherLabel = "effEM"
        return classTemplate%(otherLabel,shelve[label][runRanges[year].name][combination]["Efficiency"] , (systematics.trigger[year].central.val**2 + max(shelve[label][runRanges[year].name][combination]["UncertaintyUp"] , shelve[label][runRanges[year].name][combination]["UncertaintyDown"]  )**2)**0.5 ,shelveMC[label][runRanges[year].name][combination]["Efficiency"] , (systematics.trigger[year].central.val**2 + max(shelveMC[label][runRanges[year].name][combination]["UncertaintyUp"] , shelveMC[label][runRanges[year].name][combination]["UncertaintyDown"]  )**2)**0.5)
        #~ return classTemplate%(otherLabel,shelve[label][runRanges.name][combination]["Efficiency"] , (systematics.trigger[year].central.val**2 + max(shelve[label][runRanges.name][combination]["UncertaintyUp"] , shelve[label][runRanges.name][combination]["UncertaintyDown"]  )**2)**0.5 )


def getRSFOFTrigClass(classTemplate,shelve,shelveMC,label,returnNumbers=False,year=2016):
#~ def getRSFOFTrigClass(classTemplate,shelve,label,returnNumbers=False):
        
        
                effEE = shelve[label][runRanges[year].name]["EE"]["Efficiency"] 
                effMM = shelve[label][runRanges[year].name]["MuMu"]["Efficiency"] 
                effEM = shelve[label][runRanges[year].name]["EMu"]["Efficiency"] 
                errEE = (systematics.trigger[year].central.val**2 + max(shelve[label][runRanges[year].name]["EE"]["UncertaintyUp"] , shelve[label][runRanges[year].name]["EE"]["UncertaintyDown"]  )**2)**0.5
                errMM = (systematics.trigger[year].central.val**2 + max(shelve[label][runRanges[year].name]["MuMu"]["UncertaintyUp"] , shelve[label][runRanges[year].name]["MuMu"]["UncertaintyDown"]  )**2)**0.5
                errEM = (systematics.trigger[year].central.val**2 + max(shelve[label][runRanges[year].name]["EMu"]["UncertaintyUp"] , shelve[label][runRanges[year].name]["EMu"]["UncertaintyDown"]  )**2)**0.5
        
                err = (errEE**2/(2*effEE*effMM)**2+ errMM**2/(2*effEE*effMM)**2 + errEM**2/(effEM)**2)**0.5
                val = (effEE*effMM)**0.5/effEM
        
                effEEMC = shelveMC[label][runRanges[year].name]["EE"]["Efficiency"] 
                effMMMC = shelveMC[label][runRanges[year].name]["MuMu"]["Efficiency"] 
                effEMMC = shelveMC[label][runRanges[year].name]["EMu"]["Efficiency"] 
                errEEMC = (systematics.trigger[year].central.val**2 + max(shelveMC[label][runRanges[year].name]["EE"]["UncertaintyUp"] , shelveMC[label][runRanges[year].name]["EE"]["UncertaintyDown"]  )**2)**0.5
                errMMMC = (systematics.trigger[year].central.val**2 + max(shelveMC[label][runRanges[year].name]["MuMu"]["UncertaintyUp"] , shelveMC[label][runRanges[year].name]["MuMu"]["UncertaintyDown"]  )**2)**0.5
                errEMMC = (systematics.trigger[year].central.val**2 + max(shelveMC[label][runRanges[year].name]["EMu"]["UncertaintyUp"] , shelveMC[label][runRanges[year].name]["EMu"]["UncertaintyDown"]  )**2)**0.5
        
                errMC = val*(errEEMC**2/(2*effMMMC)**2+ errMMMC**2/(2*effMMMC)**2 + errEMMC**2/(effEMMC)**2)**0.5
                valMC = (effEEMC*effMMMC)**0.5/effEMMC
                
                if returnNumbers:
                        return val,err,valMC,errMC
                else:
                        return classTemplate%(label, val, err, valMC, errMC )
                #~ if returnNumbers:
                        #~ return val,err
                #~ else:
                        #~ return classTemplate%(label, val, err)

### Old factoritation method using constant rMuE                        
def getRSFOFFactClassOld(classTemplate,shelve,shelveMC,shelvesRMuE,shelvesRMuEMC,label,combination,returnNumbers=False,year=2016):
#~ def getRSFOFFactClassOld(classTemplate,shelve,shelvesRMuE,shelvesRMuEMC,label,combination,returnNumbers=False):
        inputs = {}
        inputs["rMuE"] = shelvesRMuE[label]["rMuE"]
        inputs["rMuEErr"] = (shelvesRMuE[label]["rMuEStatErr"]**2 + shelvesRMuE[label]["rMuESystErrOld"]**2)**0.5
        inputs["rMuEMC"] = shelvesRMuEMC[label]["rMuE"]
        inputs["rMuEErrMC"] = (shelvesRMuEMC[label]["rMuEStatErr"]**2 + shelvesRMuEMC[label]["rMuESystErrOld"]**2)**0.5 
        
        result = {}
        ### error propagation deluxe! 
        if combination == "SF":
                result["fromRMuE"] = 0.5*(inputs["rMuE"]+1./inputs["rMuE"])
                result["fromRMuEErr"] = 0.5*(1. - (1./(inputs["rMuE"]**2)))*inputs["rMuEErr"]
                result["fromRMuEMC"] = 0.5*(inputs["rMuEMC"]+1./inputs["rMuEMC"])
                result["fromRMuEErrMC"] = 0.5*(1. - (1./(inputs["rMuEMC"]**2)))*inputs["rMuEErrMC"]
        elif combination == "MM":
                result["fromRMuE"] = 0.5*(inputs["rMuE"])
                result["fromRMuEErr"] = inputs["rMuEErr"]
                result["fromRMuEMC"] = 0.5*(inputs["rMuEMC"])
                result["fromRMuEErrMC"] = inputs["rMuEErrMC"]

        elif combination == "EE":
                result["fromRMuE"] = 0.5*(1./inputs["rMuE"])
                result["fromRMuEErr"] = inputs["rMuEErr"]
                result["fromRMuEMC"] = 0.5*(1./inputs["rMuEMC"])
                result["fromRMuEErrMC"] = inputs["rMuEErrMC"]

        result["fromTrigger"], result["fromTriggerErr"] , result["fromTriggerMC"], result["fromTriggerErrMC"] = getRSFOFTrigClass(classTemplate,shelve,shelveMC,label,returnNumbers=True, year=year)
        #~ result["fromTrigger"], result["fromTriggerErr"] = getRSFOFTrigClass(classTemplate,shelve,label,returnNumbers=True)


        result["fromAC"] = result["fromRMuE"]*result["fromTrigger"]
        result["fromACErr"] = result["fromAC"]*((result["fromRMuEErr"]/result["fromRMuE"])**2 + (result["fromTriggerErr"]/result["fromTrigger"])**2)**0.5
        result["fromACMC"] = result["fromRMuEMC"]*result["fromTriggerMC"]
        result["fromACErrMC"] = result["fromACMC"]*((result["fromRMuEErrMC"]/result["fromRMuEMC"])**2 + (result["fromTriggerErrMC"]/result["fromTriggerMC"])**2)**0.5
        #~ result["fromACMC"] = result["fromRMuEMC"]*result["fromTrigger"]
        #~ result["fromACErrMC"] = result["fromACMC"]*((result["fromRMuEErrMC"]/result["fromRMuEMC"])**2 + (result["fromTriggerErr"]/result["fromTrigger"])**2)**0.5
                

        return classTemplate%(combination, result["fromAC"], result["fromACErr"], result["fromACMC"], result["fromACErrMC"] )
        

def getRSFOFClass(classTemplate,shelve,shelveMC,shelveTrigger,shelveTriggerMC,shelvesRMuE,shelvesRMuEMC,label,combination,year):
#~ def getRSFOFClass(classTemplate,shelve,shelveMC,shelveTrigger,shelvesRMuE,shelvesRMuEMC,label,combination):

        inputs = {}
        inputs["rMuE"] = shelvesRMuE[label]["rMuE"]
        inputs["rMuEErr"] = (shelvesRMuE[label]["rMuEStatErr"]**2 + shelvesRMuE[label]["rMuESystErrOld"]**2)**0.5
        inputs["rMuEMC"] = shelvesRMuEMC[label]["rMuE"]
        inputs["rMuEErrMC"] = (shelvesRMuEMC[label]["rMuEStatErr"]**2 + shelvesRMuEMC[label]["rMuESystErrOld"]**2)**0.5
        

        inputs["RSFOF"] = shelve[label]["r%sOF"%combination]
        inputs["RSFOFMC"] = shelveMC[label]["r%sOF"%combination]
        
        if combination == "SF":
                systErr = max(shelveMC[label]["transferErr"],abs(1.-shelveMC[label]["transfer"]))
        else:
                systErr = max(shelveMC[label]["transfer%sErr"%combination],abs(1.-shelveMC[label]["transfer%s"%combination]))

        inputs["RSFOFErr"] = (shelve[label]["r%sOFErr"%combination]**2 + inputs["RSFOF"]*systErr**2)**0.5
        inputs["RSFOFErrMC"] = shelveMC[label]["r%sOFErr"%combination]
        
        
        result = {}
        ### error propagation deluxe! 
        if combination == "SF":
                result["fromRMuE"] = 0.5*(inputs["rMuE"]+1./inputs["rMuE"])
                result["fromRMuEErr"] = 0.5*(1. - (1./(inputs["rMuE"]**2)))*inputs["rMuEErr"]
                result["fromRMuEMC"] = 0.5*(inputs["rMuEMC"]+1./inputs["rMuEMC"])
                result["fromRMuEErrMC"] = 0.5*(1. - (1./(inputs["rMuEMC"]**2)))*inputs["rMuEErrMC"]
        elif combination == "MM":
                result["fromRMuE"] = 0.5*(inputs["rMuE"])
                result["fromRMuEErr"] = inputs["rMuEErr"]
                result["fromRMuEMC"] = 0.5*(inputs["rMuEMC"])
                result["fromRMuEErrMC"] = inputs["rMuEErrMC"]

        elif combination == "EE":
                result["fromRMuE"] = 0.5*(1./inputs["rMuE"])
                result["fromRMuEErr"] = inputs["rMuEErr"]
                result["fromRMuEMC"] = 0.5*(1./inputs["rMuEMC"])
                result["fromRMuEErrMC"] = inputs["rMuEErrMC"]

        result["fromTrigger"], result["fromTriggerErr"] , result["fromTriggerMC"], result["fromTriggerErrMC"] = getRSFOFTrigClass(classTemplate,shelveTrigger,shelveTriggerMC,label,returnNumbers=True,year=year)
        #~ result["fromTrigger"], result["fromTriggerErr"] = getRSFOFTrigClass(classTemplate,shelveTrigger,label,returnNumbers=True)


        result["fromAC"] = result["fromRMuE"]*result["fromTrigger"]
        result["fromACErr"] = result["fromAC"]*((result["fromRMuEErr"]/result["fromRMuE"])**2 + (result["fromTriggerErr"]/result["fromTrigger"])**2)**0.5
        result["fromACMC"] = result["fromRMuEMC"]*result["fromTriggerMC"]
        result["fromACErrMC"] = result["fromACMC"]*((result["fromRMuEErrMC"]/result["fromRMuEMC"])**2 + (result["fromTriggerErrMC"]/result["fromTriggerMC"])**2)**0.5

        
        
        
        result["fromETH"] = inputs["RSFOF"]
        result["fromETHErr"] = (inputs["RSFOFErr"]**2 + (getattr(systematics.rSFOF[year],label).val * inputs["RSFOF"]) **2 )**0.5
        result["fromETHMC"] = inputs["RSFOFMC"]
        result["fromETHErrMC"] = (inputs["RSFOFErrMC"]**2 + (getattr(systematics.rSFOF[year],label).val * inputs["RSFOFMC"]) **2 )**0.5
        
                
        
        result["combination"] = (result["fromAC"]/result["fromACErr"]**2 + result["fromETH"]/result["fromETHErr"]**2) / (1./result["fromACErr"]**2 + 1./result["fromETHErr"]**2)
        result["combinationErr"] = (1./(1./result["fromACErr"]**2 + 1./result["fromETHErr"]**2))**0.5
        
        result["combinationMC"] = (result["fromACMC"]/result["fromACErrMC"]**2 + result["fromETHMC"]/result["fromETHErrMC"]**2) / (1./result["fromACErrMC"]**2 + 1./result["fromETHErrMC"]**2)
        result["combinationErrMC"] = (1./(1./result["fromACErrMC"]**2 + 1./result["fromETHErrMC"]**2))**0.5

        
        return classTemplate%(label, result["combination"], result["combinationErr"], result["combinationMC"], result["combinationErrMC"] )
        
                
def main():
        import sys
        from ConfigParser import ConfigParser
        import argparse 
        
        parser = argparse.ArgumentParser(description='Produce correction file')
        parser.add_argument("-y", "--year", dest="year", action="store", default="2016",
                                                  help="Corrections from which year to save")
        parser.add_argument("-C", "--combine", action="store_true", dest="combine", default=False,
                                                  help="Write corrections from combination of multiple years")
        args = parser.parse_args()
        
        if not args.combine:
                year = args.year
                runRangeName = runRanges[year].name
        else:
                year = "Combined"
                runRangeName = "Combined"
        
        
        classTemplate = """
                class %s:
                        val = %f
                        err = %f
                        valMC = %f
                        errMC = %f
"""
        classTemplateRMuELeptonPt = """
                class %s:
                        offset = %f
                        offsetErr = %f
                        falling = %f
                        fallingErr = %f
                        
                        offsetMC = %f
                        offsetErrMC = %f
                        fallingMC = %f
                        fallingErrMC = %f
"""
        classTemplateTrigger = """
                class %s:
                        val = %f
                        err = %f
"""
        if not args.combine:
                r = """
### central config file for all correction factors used in the dilepton edge search. This file was autogenerated.

%s
        
%s
        
%s
        
%s
        
%s
        
%s

%s
                                        
%s      

%s              

%s              

"""
        else:
                r = """
### central config file for all correction factors used in the dilepton edge search. This file was autogenerated.

%s
"""

        rOutInPart = """

class rOutIn:
        class mass20To60:
                %s
        
        class mass60To86:
                %s
     
        class mass96To150:
                %s
                
        class mass150To200:
                %s
        
        class mass200To300:
                %s
        
        class mass300To400:
                %s
        
        class mass400:
                %s
        
      
"""     


        shelvesROutIn = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRangeName)}
        shelvesROutInMC = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRangeName,MC=True)}

        
        rOutInTuple = []
        for combination in ["SF"]:
                for massRange in ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]:
                        for label in ["inclusive",]: #"central","forward"
                                rOutInTuple.append(getROutInClass(classTemplate,shelvesROutIn,shelvesROutInMC,massRange,combination,label))

        rOutInPartFinal = rOutInPart%tuple(rOutInTuple)
        
        if not args.combine:
                
                rSFOFDirectPart = """

### Direct measurement of RSFOF 
class rSFOFDirect:
%s      
              
"""     
                shelvesRSFOF = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRangeName)}
                shelvesRSFOFMC = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRangeName,MC=True)}
                

                classRSFOFDirectInclusive = classTemplate%("inclusive",shelvesRSFOF["inclusive"]["rSFOF"] , (shelvesRSFOF["inclusive"]["rSFOFErr"]**2 +(shelvesRSFOF["inclusive"]["rSFOF"]*systematics.rSFOF[year].inclusive.val)**2)**0.5 ,shelvesRSFOFMC["inclusive"]["rSFOF"] ,(shelvesRSFOFMC["inclusive"]["rSFOFErr"]**2 +(shelvesRSFOFMC["inclusive"]["rSFOF"]*systematics.rSFOF[year].inclusive.val)**2)**0.5)
                #classRSFOFDirectCentral = classTemplate%("central",shelvesRSFOF["central"]["rSFOF"] , (shelvesRSFOF["central"]["rSFOFErr"]**2 +(shelvesRSFOF["central"]["rSFOF"]*systematics.rSFOF[year].central.val)**2)**0.5 ,shelvesRSFOFMC["central"]["rSFOF"] ,(shelvesRSFOFMC["central"]["rSFOFErr"]**2 +(shelvesRSFOFMC["central"]["rSFOF"]*systematics.rSFOF[year].central.val)**2)**0.5)
                #classRSFOFDirectForward = classTemplate%("forward",shelvesRSFOF["forward"]["rSFOF"] , (shelvesRSFOF["forward"]["rSFOFErr"]**2 +(shelvesRSFOF["forward"]["rSFOF"]*systematics.rSFOF[year].forward.val)**2)**0.5 ,shelvesRSFOFMC["forward"]["rSFOF"] ,(shelvesRSFOFMC["forward"]["rSFOFErr"]**2 +(shelvesRSFOFMC["forward"]["rSFOF"]*systematics.rSFOF[year].forward.val)**2)**0.5)
                
                
                rSFOFDirectPartFinal = rSFOFDirectPart%(classRSFOFDirectInclusive)   
                
                
                
                rMuELeptonPtPart = """
        
### New rMuE factorization

class rMuELeptonPt:
%s          


"""     
                shelvesRMuELeptonPt = {"inclusive":readPickle("rMuE_correctionParameters",regionsToUse.rMuE.inclusive.name , runRangeName)}
                shelvesRMuELeptonPtMC = {"inclusive":readPickle("rMuE_correctionParameters",regionsToUse.rMuE.inclusive.name , runRangeName,MC=True)}
                        
                classRMuELeptonPtInclusive = classTemplateRMuELeptonPt%("inclusive",shelvesRMuELeptonPt["inclusive"]["offset"], shelvesRMuELeptonPt["inclusive"]["offsetErr"], shelvesRMuELeptonPt["inclusive"]["falling"], shelvesRMuELeptonPt["inclusive"]["fallingErr"], shelvesRMuELeptonPtMC["inclusive"]["offset"], shelvesRMuELeptonPtMC["inclusive"]["offsetErr"], shelvesRMuELeptonPtMC["inclusive"]["falling"], shelvesRMuELeptonPtMC["inclusive"]["fallingErr"])
                #classRMuELeptonPtCentral = classTemplateRMuELeptonPt%("central",shelvesRMuELeptonPt["central"]["offset"], shelvesRMuELeptonPt["central"]["offsetErr"], shelvesRMuELeptonPt["central"]["falling"], shelvesRMuELeptonPt["central"]["fallingErr"], shelvesRMuELeptonPtMC["central"]["offset"], shelvesRMuELeptonPtMC["central"]["offsetErr"], shelvesRMuELeptonPtMC["central"]["falling"], shelvesRMuELeptonPtMC["central"]["fallingErr"])
                #classRMuELeptonPtForward = classTemplateRMuELeptonPt%("forward",shelvesRMuELeptonPt["forward"]["offset"], shelvesRMuELeptonPt["forward"]["offsetErr"], shelvesRMuELeptonPt["forward"]["falling"], shelvesRMuELeptonPt["forward"]["fallingErr"], shelvesRMuELeptonPtMC["forward"]["offset"], shelvesRMuELeptonPtMC["forward"]["offsetErr"], shelvesRMuELeptonPtMC["forward"]["falling"], shelvesRMuELeptonPtMC["forward"]["fallingErr"])
                
                
                rMuELeptonPtPartFinal = rMuELeptonPtPart%(classRMuELeptonPtInclusive)
                        
                rMuEPart = """
### rMuE for the old factorization method

class rMuE:
%s         


"""     
                shelvesRMuE = {"inclusive":readPickle("rMuE",regionsToUse.rMuE.inclusive.name , runRangeName)}
                shelvesRMuEMC = {"inclusive":readPickle("rMuE",regionsToUse.rMuE.inclusive.name , runRangeName,MC=True)}
                        
                classRMuEInclusive = classTemplate%("inclusive",shelvesRMuE["inclusive"]["rMuE"] , (shelvesRMuE["inclusive"]["rMuEStatErr"]**2 + shelvesRMuE["inclusive"]["rMuESystErrOld"]**2)**0.5 ,shelvesRMuEMC["inclusive"]["rMuE"] , (shelvesRMuEMC["inclusive"]["rMuEStatErr"]**2 + shelvesRMuEMC["inclusive"]["rMuESystErrOld"]**2)**0.5)
                #classRMuECentral = classTemplate%("central",shelvesRMuE["central"]["rMuE"] , (shelvesRMuE["central"]["rMuEStatErr"]**2 + shelvesRMuE["central"]["rMuESystErrOld"]**2)**0.5 ,shelvesRMuEMC["central"]["rMuE"] , (shelvesRMuEMC["central"]["rMuEStatErr"]**2 + shelvesRMuEMC["central"]["rMuESystErrOld"]**2)**0.5)
                #classRMuEForward = classTemplate%("forward",shelvesRMuE["forward"]["rMuE"] , (shelvesRMuE["forward"]["rMuEStatErr"]**2 + shelvesRMuE["forward"]["rMuESystErrOld"]**2)**0.5 ,shelvesRMuEMC["forward"]["rMuE"] , (shelvesRMuEMC["forward"]["rMuEStatErr"]**2 + shelvesRMuEMC["forward"]["rMuESystErrOld"]**2)**0.5)
                
                
                rMuEPartFinal = rMuEPart%(classRMuEInclusive)
                

                shelvesTrigger = {"inclusive":readTriggerPickle("triggerEff",triggerRegionNamesLists[year].inclusive.name , runRangeName, baselineTrigger.name)}
                shelvesTriggerMC = {"inclusive":readTriggerPickle("triggerEff",triggerRegionNamesLists[year].inclusive.name , runRangeName, baselineTrigger.name,MC=True)}
                
                triggerPart = """

class triggerEffs:                                  
        class inclusive:
                %s      
                %s
                %s              
        
        
"""     
                triggerEffList = []
                for label in ["inclusive",]: # "central","forward",
                        for combination in ["EE","MuMu","EMu"]:
                                triggerEffList.append(getTriggerClass(classTemplate,shelvesTrigger,shelvesTriggerMC,combination,label,year))
                                #~ triggerEffList.append(getTriggerClass(classTemplateTrigger,shelvesTrigger,combination,label))
                                
                triggerPartFinal = triggerPart%tuple(triggerEffList)            
                
                rSFOFTrigPart = """
        
class rSFOFTrig:
%s      
        
        
"""     

                rSFOFTrigList = []
                for label in ["inclusive",]: # "central","forward",
                                rSFOFTrigList.append(getRSFOFTrigClass(classTemplate,shelvesTrigger,shelvesTriggerMC,label, year=year))
                                #~ rSFOFTrigList.append(getRSFOFTrigClass(classTemplateTrigger,shelvesTrigger,label))
                                
                rSFOFTrigPartFinal = rSFOFTrigPart%tuple(rSFOFTrigList)         

                rSFOFFactOldPart = """
        
### R_SFOF using the old factorization method
        
class rSFOFFactOld:                                   
        class inclusive:
                %s      
                %s
                %s      
        
"""     

                rSFOFFactList = []
                for label in ["inclusive",]:
                                for combination in ["SF","EE","MM"]:
                                        rSFOFFactList.append(getRSFOFFactClassOld(classTemplate,shelvesTrigger,shelvesTriggerMC,shelvesRMuE,shelvesRMuEMC,label,combination,year=year))
                                        #~ rSFOFFactList.append(getRSFOFFactClassOld(classTemplate,shelvesTrigger,shelvesRMuE,shelvesRMuEMC,label,combination))
                                
                rSFOFFactOldPartFinal = rSFOFFactOldPart%tuple(rSFOFFactList)           
                

                shelvesRSFOF = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRangeName)}
                shelvesRSFOFMC = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRangeName,MC=True)}
                
                rSFOFList = []
                for label in ["inclusive",]: # "central","forward",
                                rSFOFList.append(getRSFOFClass(classTemplate,shelvesRSFOF,shelvesRSFOFMC,shelvesTrigger,shelvesTriggerMC,shelvesRMuE,shelvesRMuEMC,label,"SF",year))
                                #~ rSFOFList.append(getRSFOFClass(classTemplate,shelvesRSFOF,shelvesRSFOFMC,shelvesTrigger,shelvesRMuE,shelvesRMuEMC,label,"SF"))
                
                rSFOFPart  = """
        
### R_SFOF combination using the old factorization method

class rSFOF:
%s           
"""     
                rSFOFPartFinal = rSFOFPart%tuple(rSFOFList)
                
                rEEOFList = []
                for label in ["inclusive",]: # "central","forward",
                                rEEOFList.append(getRSFOFClass(classTemplate,shelvesRSFOF,shelvesRSFOFMC,shelvesTrigger,shelvesTriggerMC,shelvesRMuE,shelvesRMuEMC,label,"EE",year))
                                #~ rEEOFList.append(getRSFOFClass(classTemplate,shelvesRSFOF,shelvesRSFOFMC,shelvesTrigger,shelvesRMuE,shelvesRMuEMC,label,"EE"))
                
                rEEOFPart  = """
class rEEOF:
%s          
"""     
                rEEOFPartFinal = rEEOFPart%tuple(rEEOFList)
                
                rMMOFList = []
                for label in ["inclusive",]: # "central","forward",
                                rMMOFList.append(getRSFOFClass(classTemplate,shelvesRSFOF,shelvesRSFOFMC,shelvesTrigger,shelvesTriggerMC,shelvesRMuE,shelvesRMuEMC,label,"MM",year))
                                #~ rMMOFList.append(getRSFOFClass(classTemplate,shelvesRSFOF,shelvesRSFOFMC,shelvesTrigger,shelvesRMuE,shelvesRMuEMC,label,"MM"))
                
                rMMOFPart  = """
class rMMOF:
%s           
"""     
                rMMOFPartFinal = rMMOFPart%tuple(rMMOFList)

                finalFile = r%(rOutInPartFinal,rSFOFDirectPartFinal,rMuELeptonPtPartFinal,rMuEPartFinal,rSFOFTrigPartFinal,rSFOFFactOldPartFinal,rSFOFPartFinal,rEEOFPartFinal,rMMOFPartFinal,triggerPartFinal)
        
        else:
                finalFile = r%(rOutInPartFinal)
        
        corrFile = open("corrections%s.py"%(year), "w")
        corrFile.write(finalFile)
        corrFile.close()        
        
main()

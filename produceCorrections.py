### Script to produce corrections.py that holds all the relevant information
### for the background prediction
### For each component of the background prediction there is a certain template
### and a routine to fill it

import pickle
import os
import sys
from centralConfig import regionsToUse, runRanges, systematics

def readPickle(name,regionName,runName,MC=False):
	### read .pkl files from shelves
	
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

def getROutInClass(classTemplate,shelve,shelveMC,massRange,combination,label):
	### R_Out/In values
	
	### fetch value from pkl and combine stat and syst uncertainty
	### done for both data and MC
	
	val = shelve[label]["rOutIn%s%s"%(massRange,combination)]
	err = ( shelve[label]["rOutIn%sSyst%s"%(massRange,combination)]**2 + shelve[label]["rOutIn%sErr%s"%(massRange,combination)]**2 )**0.5
	
	valMC = shelveMC[label]["rOutIn%s%s"%(massRange,combination)]
	errMC = ( shelveMC[label]["rOutIn%sSyst%s"%(massRange,combination)]**2 + shelveMC[label]["rOutIn%sErr%s"%(massRange,combination)]**2 )**0.5

	return classTemplate%(label,val, err , valMC, errMC)	


def getTriggerClass(classTemplate,shelve,shelveMC,combination,label):
	### trigger efficiencies
	
	### fetch value from pkl and combine stat and syst uncertainty
	### done for both data and MC for a certain dilepton combination
	
	if combination == "EE":
		otherLabel = "effEE"
	elif combination == "MuMu":
		otherLabel = "effMM"
	else:
		otherLabel = "effEM"
		
	val = shelve[label][runRanges.name][combination]["Efficiency"]
	err = (systematics.trigger.central.val**2 + max(shelve[label][runRanges.name][combination]["UncertaintyUp"] , shelve[label][runRanges.name][combination]["UncertaintyDown"]  )**2)**0.5
	
	valMC = shelveMC[label][runRanges.name][combination]["Efficiency"] 
	errMC = (systematics.trigger.central.val**2 + max(shelveMC[label][runRanges.name][combination]["UncertaintyUp"] , shelveMC[label][runRanges.name][combination]["UncertaintyDown"]  )**2)**0.5
	
	return classTemplate%(otherLabel, val, err , valMC, errMC)


def getRSFOFTrigClass(classTemplate,shelve,shelveMC,label,returnNumbers=False):
	### R_T from trigger efficiencies to use in the factorization method
	
	### fetch efficiencies from pkl and combine stat and syst uncertainty
	### done for both data and MC for a certain dilepton combination
	
	effEE = shelve[label][runRanges.name]["EE"]["Efficiency"] 
	effMM = shelve[label][runRanges.name]["MuMu"]["Efficiency"] 
	effEM = shelve[label][runRanges.name]["EMu"]["Efficiency"] 
	errEE = (systematics.trigger.central.val**2 + max(shelve[label][runRanges.name]["EE"]["UncertaintyUp"] , shelve[label][runRanges.name]["EE"]["UncertaintyDown"]  )**2)**0.5
	errMM = (systematics.trigger.central.val**2 + max(shelve[label][runRanges.name]["MuMu"]["UncertaintyUp"] , shelve[label][runRanges.name]["MuMu"]["UncertaintyDown"]  )**2)**0.5
	errEM = (systematics.trigger.central.val**2 + max(shelve[label][runRanges.name]["EMu"]["UncertaintyUp"] , shelve[label][runRanges.name]["EMu"]["UncertaintyDown"]  )**2)**0.5

	### make the combinations that go into the calculation of R_SF/OF
	err = (errEE**2/(2*effEE*effMM)**2+ errMM**2/(2*effEE*effMM)**2 + errEM**2/(effEM)**2)**0.5
	val = (effEE*effMM)**0.5/effEM

	effEEMC = shelveMC[label][runRanges.name]["EE"]["Efficiency"] 
	effMMMC = shelveMC[label][runRanges.name]["MuMu"]["Efficiency"] 
	effEMMC = shelveMC[label][runRanges.name]["EMu"]["Efficiency"] 
	errEEMC = (systematics.trigger.central.val**2 + max(shelveMC[label][runRanges.name]["EE"]["UncertaintyUp"] , shelveMC[label][runRanges.name]["EE"]["UncertaintyDown"]  )**2)**0.5
	errMMMC = (systematics.trigger.central.val**2 + max(shelveMC[label][runRanges.name]["MuMu"]["UncertaintyUp"] , shelveMC[label][runRanges.name]["MuMu"]["UncertaintyDown"]  )**2)**0.5
	errEMMC = (systematics.trigger.central.val**2 + max(shelveMC[label][runRanges.name]["EMu"]["UncertaintyUp"] , shelveMC[label][runRanges.name]["EMu"]["UncertaintyDown"]  )**2)**0.5

	errMC = val*(errEEMC**2/(2*effMMMC)**2+ errMMMC**2/(2*effMMMC)**2 + errEMMC**2/(effEMMC)**2)**0.5
	valMC = (effEEMC*effMMMC)**0.5/effEMMC
	
	if returnNumbers:
		return val,err,valMC,errMC
	else:
		return classTemplate%(label, val, err, valMC, errMC )
		
def getRSFOFFactClass(classTemplate,shelve,shelveMC,shelvesRMuE,shelvesRMuEMC,label,combination,returnNumbers=False):
	### Full factorization method for R_SF/OF
	
	### first fetch r_mu/e
	inputs = {}
	inputs["rMuE"] = shelvesRMuE[label]["rMuE"]
	inputs["rMuEErr"] = (shelvesRMuE[label]["rMuEStatErr"]**2 + shelvesRMuE[label]["rMuESystErr"]**2)**0.5
	inputs["rMuEMC"] = shelvesRMuEMC[label]["rMuE"]
	inputs["rMuEErrMC"] = (shelvesRMuEMC[label]["rMuEStatErr"]**2 + shelvesRMuEMC[label]["rMuESystErr"]**2)**0.5	
	
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

	### now the triggers, use routine from above
	result["fromTrigger"], result["fromTriggerErr"] , result["fromTriggerMC"], result["fromTriggerErrMC"] = getRSFOFTrigClass(classTemplate,shelve,shelveMC,label,returnNumbers=True)

	### combine both
	result["fromFactorization"] = result["fromRMuE"]*result["fromTrigger"]
	result["fromFactorizationErr"] = result["fromFactorization"]*((result["fromRMuEErr"]/result["fromRMuE"])**2 + (result["fromTriggerErr"]/result["fromTrigger"])**2)**0.5
	result["fromFactorizationMC"] = result["fromRMuEMC"]*result["fromTriggerMC"]
	result["fromFactorizationErrMC"] = result["fromFactorizationMC"]*((result["fromRMuEErrMC"]/result["fromRMuEMC"])**2 + (result["fromTriggerErrMC"]/result["fromTriggerMC"])**2)**0.5
		

	return classTemplate%(combination, result["fromFactorization"], result["fromFactorizationErr"], result["fromFactorizationMC"], result["fromFactorizationErrMC"] )
	

def getRSFOFClass(classTemplate,shelve,shelveMC,shelveTrigger,shelveTriggerMC,shelvesRMuE,shelvesRMuEMC,label,combination):
	### Combination of both factorization method and direct measurement

	### first fetch r_mu/e
	inputs = {}
	inputs["rMuE"] = shelvesRMuE[label]["rMuE"]
	inputs["rMuEErr"] = (shelvesRMuE[label]["rMuEStatErr"]**2 + shelvesRMuE[label]["rMuESystErr"]**2)**0.5
	inputs["rMuEMC"] = shelvesRMuEMC[label]["rMuE"]
	inputs["rMuEErrMC"] = (shelvesRMuEMC[label]["rMuEStatErr"]**2 + shelvesRMuEMC[label]["rMuESystErr"]**2)**0.5
	
	### Input from the direct measurement
	inputs["RSFOF"] = shelve[label]["r%sOF"%combination]
	inputs["RSFOFMC"] = shelveMC[label]["r%sOF"%combination]
	
	if combination == "SF":
		inputs["RSFOFErr"] = (shelve[label]["r%sOFErr"%combination]**2 + inputs["RSFOF"]*shelveMC[label]["transferErr"]**2)**0.5
	else:
		inputs["RSFOFErr"] = (shelve[label]["r%sOFErr"%combination]**2 + inputs["RSFOF"]*shelveMC[label]["transfer%sErr"%combination]**2)**0.5

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

	### now the triggers, use routine from above
	result["fromTrigger"], result["fromTriggerErr"] , result["fromTriggerMC"], result["fromTriggerErrMC"] = getRSFOFTrigClass(classTemplate,shelveTrigger,shelveTriggerMC,label,returnNumbers=True)


	### full factorization method
	result["fromFactorization"] = result["fromRMuE"]*result["fromTrigger"]
	result["fromFactorizationErr"] = result["fromFactorization"]*((result["fromRMuEErr"]/result["fromRMuE"])**2 + (result["fromTriggerErr"]/result["fromTrigger"])**2)**0.5
	result["fromFactorizationMC"] = result["fromRMuEMC"]*result["fromTriggerMC"]
	result["fromFactorizationErrMC"] = result["fromFactorizationMC"]*((result["fromRMuEErrMC"]/result["fromRMuEMC"])**2 + (result["fromTriggerErrMC"]/result["fromTriggerMC"])**2)**0.5

	
	
	### direct measurement
	result["fromDirectMeasurement"] = inputs["RSFOF"]
	result["fromDirectMeasurementErr"] = inputs["RSFOFErr"]
	result["fromDirectMeasurementMC"] = inputs["RSFOFMC"]
	result["fromDirectMeasurementErrMC"] = inputs["RSFOFErrMC"]
	
		
	### combination of both methaods using the weighted average
	result["combination"] = (result["fromFactorization"]/result["fromFactorizationErr"]**2 + result["fromDirectMeasurement"]/result["fromDirectMeasurementErr"]**2) / (1./result["fromFactorizationErr"]**2 + 1./result["fromDirectMeasurementErr"]**2)
	result["combinationErr"] = (1./(1./result["fromFactorizationErr"]**2 + 1./result["fromDirectMeasurementErr"]**2))**0.5
	
	result["combinationMC"] = (result["fromFactorizationMC"]/result["fromFactorizationErrMC"]**2 + result["fromDirectMeasurementMC"]/result["fromDirectMeasurementErrMC"]**2) / (1./result["fromFactorizationErrMC"]**2 + 1./result["fromDirectMeasurementErrMC"]**2)
	result["combinationErrMC"] = (1./(1./result["fromFactorizationErrMC"]**2 + 1./result["fromDirectMeasurementErrMC"]**2))**0.5

	
	return classTemplate%(label, result["combination"], result["combinationErr"], result["combinationMC"], result["combinationErrMC"] )
	
		
def main():

### Use a general template and templates for each part

	classTemplate = """
		class %s:
			val = %f
			err = %f
			valMC = %f
			errMC = %f
"""

### general template
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

"""

### R_Out/In template

### ADD OTHER REGIONS HERE AFTER ADDING THEM TO countsAndCorrections/rOutIn/rOutIn.py!!!
	rOutInPart = """

class rOutIn:
	class lowMass:
	%s
	%s
	%s
class rOutInEE:
	class lowMass:
	%s
	%s
	%s
class rOutInMM:
	class lowMass:
	%s
	%s
	%s
	

"""	


	### read in .pkl files 
	shelvesROutIn = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRanges.name),"central": readPickle("rOutIn",regionsToUse.rOutIn.central.name,runRanges.name), "forward":readPickle("rOutIn",regionsToUse.rOutIn.forward.name,runRanges.name)}
	shelvesROutInMC = {"inclusive":readPickle("rOutIn",regionsToUse.rOutIn.inclusive.name , runRanges.name,MC=True),"central": readPickle("rOutIn",regionsToUse.rOutIn.central.name,runRanges.name,MC=True), "forward":readPickle("rOutIn",regionsToUse.rOutIn.forward.name,runRanges.name,MC=True)}

	### get all the values from the pkls
	rOutInTuple = []
	for combination in ["SF","EE","MM"]:
		### ADD OTHER REGIONS HERE !!!!
		for massRange in ["LowMass"]:
			for label in ["inclusive","central","forward"]:
				rOutInTuple.append(getROutInClass(classTemplate,shelvesROutIn,shelvesROutInMC,massRange,combination,label))

	rOutInPartFinal = rOutInPart%tuple(rOutInTuple)

### r_Mu/E 
	rMuEPart = """
class rMuE:
%s	
%s
%s	


"""	
	shelvesRMuE = {"inclusive":readPickle("rMuE",regionsToUse.rMuE.inclusive.name , runRanges.name),"central": readPickle("rMuE",regionsToUse.rMuE.central.name,runRanges.name), "forward":readPickle("rMuE",regionsToUse.rMuE.forward.name,runRanges.name)}
	shelvesRMuEMC = {"inclusive":readPickle("rMuE",regionsToUse.rMuE.inclusive.name , runRanges.name,MC=True),"central": readPickle("rMuE",regionsToUse.rMuE.central.name,runRanges.name,MC=True), "forward":readPickle("rMuE",regionsToUse.rMuE.forward.name,runRanges.name,MC=True)}
		
	classRMuEInclusive = classTemplate%("inclusive",shelvesRMuE["inclusive"]["rMuE"] , (shelvesRMuE["inclusive"]["rMuEStatErr"]**2 + shelvesRMuE["inclusive"]["rMuESystErr"]**2)**0.5 ,shelvesRMuEMC["inclusive"]["rMuE"] , (shelvesRMuEMC["inclusive"]["rMuEStatErr"]**2 + shelvesRMuEMC["inclusive"]["rMuESystErr"]**2)**0.5)
	classRMuECentral = classTemplate%("central",shelvesRMuE["central"]["rMuE"] , (shelvesRMuE["central"]["rMuEStatErr"]**2 + shelvesRMuE["central"]["rMuESystErr"]**2)**0.5 ,shelvesRMuEMC["central"]["rMuE"] , (shelvesRMuEMC["central"]["rMuEStatErr"]**2 + shelvesRMuEMC["central"]["rMuESystErr"]**2)**0.5)
	classRMuEForward = classTemplate%("forward",shelvesRMuE["forward"]["rMuE"] , (shelvesRMuE["forward"]["rMuEStatErr"]**2 + shelvesRMuE["forward"]["rMuESystErr"]**2)**0.5 ,shelvesRMuEMC["forward"]["rMuE"] , (shelvesRMuEMC["forward"]["rMuEStatErr"]**2 + shelvesRMuEMC["forward"]["rMuESystErr"]**2)**0.5)
	
	
	rMuEPartFinal = rMuEPart%(classRMuEInclusive , classRMuECentral, classRMuEForward)
	

	shelvesTrigger = {"inclusive":readPickle("triggerEff",regionsToUse.triggerEfficiencies.inclusive.name , runRanges.name),"central": readPickle("triggerEff",regionsToUse.triggerEfficiencies.central.name,runRanges.name), "forward":readPickle("triggerEff",regionsToUse.triggerEfficiencies.forward.name,runRanges.name)}
	shelvesTriggerMC = {"inclusive":readPickle("triggerEff",regionsToUse.triggerEfficiencies.inclusive.name , runRanges.name,MC=True),"central": readPickle("triggerEff",regionsToUse.triggerEfficiencies.central.name,runRanges.name, MC=True), "forward":readPickle("triggerEff",regionsToUse.triggerEfficiencies.forward.name,runRanges.name,MC=True)}

### Trigger efficiencies	
	triggerPart = """

class triggerEffs:
	class central:
		%s	
		%s
		%s		
	class forward:
		%s	
		%s
		%s					
	class inclusive:
		%s	
		%s
		%s		
	
	
"""	
	triggerEffList = []
	for label in ["central","forward","inclusive"]:
		for combination in ["EE","MuMu","EMu"]:
			triggerEffList.append(getTriggerClass(classTemplate,shelvesTrigger,shelvesTriggerMC,combination,label))
			
	triggerPartFinal = triggerPart%tuple(triggerEffList)		

### R_T	
	rSFOFTrigPart = """
	
class rSFOFTrig:
%s	
%s
%s
	
	
"""	

	rSFOFTrigList = []
	for label in ["central","forward","inclusive"]:
			rSFOFTrigList.append(getRSFOFTrigClass(classTemplate,shelvesTrigger,shelvesTriggerMC,label))
			
	rSFOFTrigPartFinal = rSFOFTrigPart%tuple(rSFOFTrigList)		
	


### Factorization method
	rSFOFFactPart = """
	
class rSFOFFact:
	class central:
		%s	
		%s
		%s		
	class forward:
		%s	
		%s
		%s					
	class inclusive:
		%s	
		%s
		%s	
	
"""	

	rSFOFFactList = []
	for label in ["central","forward","inclusive"]:
			for combination in ["SF","EE","MM"]:
				rSFOFFactList.append(getRSFOFFactClass(classTemplate,shelvesTrigger,shelvesTriggerMC,shelvesRMuE,shelvesRMuEMC,label,combination))
			
	rSFOFFactPartFinal = rSFOFFactPart%tuple(rSFOFFactList)		
	

	### Input from direct measurement	
	shelvesRSFOF = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRanges.name),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRanges.name), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRanges.name)}
	shelvesRSFOFMC = {"inclusive":readPickle("rSFOF",regionsToUse.rSFOF.inclusive.name , runRanges.name,MC=True),"central": readPickle("rSFOF",regionsToUse.rSFOF.central.name,runRanges.name,MC=True), "forward":readPickle("rSFOF",regionsToUse.rSFOF.forward.name,runRanges.name,MC=True)}
	
	rSFOFList = []
	for label in ["central","forward","inclusive"]:
			rSFOFList.append(getRSFOFClass(classTemplate,shelvesRSFOF,shelvesRSFOFMC,shelvesTrigger,shelvesTriggerMC,shelvesRMuE,shelvesRMuEMC,label,"SF"))

### Combination of both methods for R_SF/OF	
	rSFOFPart  = """
class rSFOF:
%s	
%s
%s	
"""	
	rSFOFPartFinal = rSFOFPart%tuple(rSFOFList)
	
	rEEOFList = []
	for label in ["central","forward","inclusive"]:
			rEEOFList.append(getRSFOFClass(classTemplate,shelvesRSFOF,shelvesRSFOFMC,shelvesTrigger,shelvesTriggerMC,shelvesRMuE,shelvesRMuEMC,label,"EE"))
	
	rEEOFPart  = """
class rEEOF:
%s	
%s
%s	
"""	
	rEEOFPartFinal = rEEOFPart%tuple(rEEOFList)
	
	rMMOFList = []
	for label in ["central","forward","inclusive"]:
			rMMOFList.append(getRSFOFClass(classTemplate,shelvesRSFOF,shelvesRSFOFMC,shelvesTrigger,shelvesTriggerMC,shelvesRMuE,shelvesRMuEMC,label,"MM"))
	
	rMMOFPart  = """
class rMMOF:
%s	
%s
%s	
"""	
	rMMOFPartFinal = rMMOFPart%tuple(rMMOFList)



	finalFile = r%(rOutInPartFinal,rMuEPartFinal,rSFOFTrigPartFinal,rSFOFFactPartFinal,rSFOFPartFinal,rEEOFPartFinal,rMMOFPartFinal,triggerPartFinal)

	corrFile = open("corrections.py", "w")
	corrFile.write(finalFile)
	corrFile.close()	
	
main()

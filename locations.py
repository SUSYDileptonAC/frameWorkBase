from baseClasses import maplike


class locations2016(maplike):
        dataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2016v1019/" 
        dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw2016v1019_NLL/"
        
        dataSetPathSignalDenominator = "/net/data_cms1b/user/teroerde/trees/SignalDenominator_2016"
        fileNameDenominator_T6bbllslepton = "T6bbllsleptonDenominatorHisto.root"
        fileNameDenominator_T6qqllslepton = "T6qqllsleptonDenominatorHisto.root"
        
        dataSetPathSignalT6bbllslepton = "/net/data_cms1b/user/teroerde/trees/sw2016v1019_T6bbllslepton/"
        dataSetPathSignalT6qqllslepton = "/net/data_cms1b/user/teroerde/trees/sw2016v1019_T6qqllslepton/"
        
        dataSetPathSignalNLLT6bbllslepton = "/net/data_cms1b/user/teroerde/trees/sw2016v1019_T6bbllslepton_NLL/"
        dataSetPathSignalNLLT6qqllslepton = "/net/data_cms1b/user/teroerde/trees/sw2016v1019_T6qqllslepton_NLL/"
        
        dataSetPathNonIso = "/net/data_cms1b/user/teroerde/trees/sw2016vNoIso/"
        dataSetPathMC = "/net/data_cms1b/user/teroerde/trees/sw2016v1019/" 
        triggerDataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2016v1017_MET/"
        denominator_T6bbllslepton_SourcePath = "/net/data_cms1b/user/teroerde/trees/sw2016v1019_SignalNominator_T6bbllslepton"
        denominator_T6qqllslepton_SourcePath = "/net/data_cms1b/user/teroerde/trees/sw2016v1019_SignalNominator_T6qqllslepton"
        
class locations2017(maplike): 
        dataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2017v1019/"   
        dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw2017v1019_NLL/"
        
        dataSetPathSignalDenominator = "/net/data_cms1b/user/teroerde/trees/SignalDenominator_2017"
        fileNameDenominator_T6bbllslepton = "T6bbllsleptonDenominatorHisto.root"
        fileNameDenominator_T6qqllslepton = "T6qqllsleptonDenominatorHisto.root"
        
        dataSetPathSignalT6bbllslepton = "/net/data_cms1b/user/teroerde/trees/sw2017v1018_T6bbllslepton/"
        dataSetPathSignalT6qqllslepton = "/net/data_cms1b/user/teroerde/trees/sw2017v1018_T6qqllslepton/"
        
        dataSetPathSignalNLLT6bbllslepton = "/net/data_cms1b/user/teroerde/trees/sw2017v1018_T6bbllslepton_NLL/"
        dataSetPathSignalNLLT6qqllslepton = "/net/data_cms1b/user/teroerde/trees/sw2017v1018_T6qqllslepton_NLL/"
        
        dataSetPathNonIso = "/net/data_cms1b/user/teroerde/trees/sw2017vNoIso/"
        dataSetPathMC = "/net/data_cms1b/user/teroerde/trees/sw2017v1019/"
        triggerDataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2017v1017_MET/"
        denominator_T6bbllslepton_SourcePath = "/net/data_cms1b/user/teroerde/trees/sw2017v1015_SignalNominator_T6bbllslepton"
        denominator_T6qqllslepton_SourcePath = "/net/data_cms1b/user/teroerde/trees/sw2017v1015_SignalNominator_T6qqllslepton"

class locations2018(maplike): 
        dataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2018v1021/"   
        dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw2018v1021_NLL/"
        
        dataSetPathSignalDenominator = "/net/data_cms1b/user/teroerde/trees/SignalDenominator_2018"
        fileNameDenominator_T6bbllslepton = "T6bbllsleptonDenominatorHisto.root"
        fileNameDenominator_T6qqllslepton = "T6qqllsleptonDenominatorHisto.root"
        
        dataSetPathSignalT6bbllslepton = "/net/data_cms1b/user/teroerde/trees/sw2018v1021_T6bbllslepton/"
        dataSetPathSignalT6qqllslepton = "/net/data_cms1b/user/teroerde/trees/sw2018v1021_T6qqllslepton/"
        
        dataSetPathSignalNLLT6bbllslepton = "/net/data_cms1b/user/teroerde/trees/sw2018v1021_T6bbllslepton_NLL/"
        dataSetPathSignalNLLT6qqllslepton = "/net/data_cms1b/user/teroerde/trees/sw2018v1021_T6qqllslepton_NLL/"
        
        dataSetPathNonIso = "/net/data_cms1b/user/teroerde/trees/sw2018vNoIso/"
        dataSetPathMC = "/net/data_cms1b/user/teroerde/trees/sw2018v1018/"
        triggerDataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2018v1017_MET/"
        denominator_T6bbllslepton_SourcePath = "/net/data_cms1b/user/teroerde/trees/sw2018v1015_SignalNominator_T6bbllslepton"
        denominator_T6qqllslepton_SourcePath = "/net/data_cms1b/user/teroerde/trees/sw2018v1015_SignalNominator_T6qqllslepton"

class locations(maplike):
        masterListPath = "/home/home4/institut_1b/teroerde/Doktorand/SUSYFramework/SubmitScripts/Input"
        epsToPdfPath = "perl /home/home4/institut_1b/teroerde/Doktorand/epstopdf/epstopdf/epstopdf.pl --gsopt=-dCompatibilityLevel=1.5" # could just be "epstopdf, but pdflatex will output a version warning"

locations["2016"] = locations2016
locations["2017"] = locations2017
locations["2018"] = locations2018

# temporary default ################################
for key,entry in locations2016.__dict__.iteritems():
        if not "__" in key:
                setattr(locations, key, entry)
####################################################

from baseClasses import maplike

class locations2016:
        
        #dataSetPath = "/net/data_cms1b/user/teroerde/trees/sw8026v3015/"  
        dataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2016v1007/"  
        dataSetPathSignal = "/net/data_cms1b/user/teroerde/trees/sw8026v3016_Signal/"
        dataSetPathSignalDenominator = "/net/data_cms1b/user/teroerde/trees/sw8026v3015_Signal_counts/T6bbllsleptonDenominatorHisto.root"
        #dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw8026v3015_NLL/"
        #dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw8026v3015_NLL2/"
        dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw2016v1007_NLL/"
        dataSetPathSignalNLL = "/net/data_cms1b/user/teroerde/trees/sw8026v3016_Signal_NLL/"

        #dataSetPathMC = "/net/data_cms1b/user/teroerde/trees/sw8026v3015/"
        dataSetPathMC = "/net/data_cms1b/user/teroerde/trees/sw2016v1007/" 
        triggerDataSetPath = "/net/data_cms1b/user/teroerde/trees/sw8026v3015_HT/"

class locations2017: 
        dataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2017v1008/"   
        dataSetPathSignal = "/net/data_cms1b/user/teroerde/trees/sw9409v1003_Signal"
        #dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw2017v1005_NLL"
        dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw2017v1008_NLL/"
        dataSetPathSignalNLL = "/net/data_cms1b/user/teroerde/trees/sw9409v1003_Signal_NLL/"

        dataSetPathMC = "/net/data_cms1b/user/teroerde/trees/sw2017v1008/"
        triggerDataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2017v1005_MET/"


class locations2018: 
        dataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2018v1008/"   
        #dataSetPathSignal = "/net/data_cms1b/user/teroerde/trees/sw9409v1003_Signal"
        #dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw2018v1001_NLL/"
        dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw2018v1008_NLL/"
        #dataSetPathSignalNLL = "/net/data_cms1b/user/teroerde/trees/sw9409v1003_Signal_NLL/"

        dataSetPathMC = "/net/data_cms1b/user/teroerde/trees/sw2018v1008/"
        triggerDataSetPath = "/net/data_cms1b/user/teroerde/trees/sw2018v1001_MET/"



class locations(maplike):
        masterListPath = "/home/home4/institut_1b/teroerde/Doktorand/SUSYFramework/SubmitScripts/Input"


locations["2016"] = locations2016
locations["2017"] = locations2017
locations["2018"] = locations2018

# temporary ########################################
for key,entry in locations2016.__dict__.iteritems():
        if not "__" in key:
                setattr(locations, key, entry)
####################################################

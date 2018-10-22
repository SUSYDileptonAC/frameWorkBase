class LOCATIONS2016:
        
        dataSetPath = "/net/data_cms1b/user/teroerde/trees/sw8026v3014/"  
        dataSetPathSignal = "/net/data_cms1b/user/teroerde/trees/sw8026v3014_Signal"
        dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw8026v3014_NLL"
        dataSetPathSignalNLL = "/net/data_cms1b/user/teroerde/trees/sw8026v3014_Signal_NLL/"

        dataSetPathMC = "/net/data_cms1b/user/teroerde/trees/sw8026v3014/"
        triggerDataSetPath = "/net/data_cms1b/user/teroerde/trees/HTTrees_80X/"

class LOCATIONS2017: 
        dataSetPath = "/net/data_cms1b/user/teroerde/trees/sw9409v1004/"   
        dataSetPathSignal = "/net/data_cms1b/user/teroerde/trees/sw9409v1003_Signal"
        dataSetPathNLL = "/net/data_cms1b/user/teroerde/trees/sw9409v1003_NLL"
        dataSetPathSignalNLL = "/net/data_cms1b/user/teroerde/trees/sw9409v1003_Signal_NLL/"

        dataSetPathMC = "/net/data_cms1b/user/teroerde/trees/sw9409v1004/"
        triggerDataSetPath = "/net/data_cms1b/user/teroerde/trees/sw9409v1004_HT/"



class LOCATIONS:
        masterListPath = "/home/home4/institut_1b/teroerde/Doktorand/SUSYFramework/SubmitScripts/Input"

        def __getitem__(self, key):
                return getattr(self, "for"+key)


locations = LOCATIONS()

setattr(locations, "for2017", LOCATIONS2017)
setattr(locations, "for2016", LOCATIONS2016)

# temporary ########################################
for key,entry in LOCATIONS2016.__dict__.iteritems():
        if not "__" in key:
                setattr(locations, key, entry)
####################################################

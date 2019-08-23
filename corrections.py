
### this file loads all the correction classes from all eras (2016-2018)
### they are accessible through corrections[era] and readable in the different files
from baseClasses import maplike

class corrections(maplike):
        pass

import corrections2016
import corrections2017
import corrections2018
import correctionsCombined

corrections["2016"] = corrections2016
corrections["2017"] = corrections2017
corrections["2018"] = corrections2018
corrections["Combined"] = correctionsCombined



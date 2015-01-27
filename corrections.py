

class zPredictions:
	class central:
		value = 100
		err = 10
	class forward:
		value = 50
		err = 5
		

class rOutIn:
	class central:
		val = 0.07
		err = 0.25*0.07
	class forward:
		val = 0.07
		err = 0.25*0.07
class rMuE:
	class central:
		val = 1.088
		err = 0.1*1.088
	class forward:
		val = 1.183
		err = 1.183*0.2
class rSFOFTrig:
	class central:
		val = 1.02
		err = 0.064
	class forward:
		val = 1.02
		err = 0.064
class rSFOF:
	class central:
		val = 1.0
		err = 0.04
	class forward:
		val = 1.10
		err = 0.08
	
class rEEOF:
	class central:
		val = 1.0
		err = 0.04
	class forward:
		val = 1.10
		err = 0.08
class rMMOF:
	class central:
		val = 1.0
		err = 0.04
	class forward:
		val = 1.10
		err = 0.08
		
			
class triggerEffs:
	class central:
		class effEE:
			val = 1.0
			err = 0.05			
		class effMM:
			val = 1.0
			err = 0.05			
		class effEM:
			val = 1.0
			err = 0.05			
	class forward:
		class effEE:
			val = 1.0
			err = 0.05			
		class effMM:
			val = 1.0
			err = 0.05			
		class effEM:
			val = 1.0
			err = 0.05			
	class inclusive:
		class effEE:
			val = 1.0
			err = 0.05			
		class effMM:
			val = 1.0
			err = 0.05			
		class effEM:
			val = 1.0
			err = 0.05			


class systematics:
	class rMuE:
		class central:
			val = 0.1
		class forward:
			val = 0.2	
	class trigger:
		class central:
			val = 0.05
		class forward:
			val = 0.05
	class rOutIn:
		class central:
			val = 0.25
		class forward:
			val = 0.25		
			
class mllBins:
	class lowMass:
		low = 20
		high = 70
	class onZ:
		low = 81
		high = 101
	class highMass:
		low = 120
		high = 1000


### central config file for all correction factors used in the dilepton edge search. This file was autogenerated.



class rOutIn:
        class mass20To60:
                
                class inclusive:
                        val = 0.055144
                        err = 0.027773
                        valMC = 0.053458
                        errMC = 0.026925

        
        class mass60To86:
                
                class inclusive:
                        val = 0.111515
                        err = 0.055962
                        valMC = 0.114949
                        errMC = 0.057673

     
        class mass96To150:
                
                class inclusive:
                        val = 0.168578
                        err = 0.084502
                        valMC = 0.150817
                        errMC = 0.075615

                
        class mass150To200:
                
                class inclusive:
                        val = 0.014297
                        err = 0.014419
                        valMC = 0.013955
                        errMC = 0.014077

        
        class mass200To300:
                
                class inclusive:
                        val = 0.012797
                        err = 0.012906
                        valMC = 0.013706
                        errMC = 0.013835

        
        class mass300To400:
                
                class inclusive:
                        val = 0.003268
                        err = 0.003418
                        valMC = 0.005334
                        errMC = 0.005447

        
        class mass400:
                
                class inclusive:
                        val = 0.003813
                        err = 0.003946
                        valMC = 0.006513
                        errMC = 0.006623

        
      

        


### Direct measurement of RSFOF 
class rSFOFDirect:

                class inclusive:
                        val = 1.123671
                        err = 0.046522
                        valMC = 1.090902
                        errMC = 0.044270
      
              

        

        
### New rMuE factorization

class rMuELeptonPt:

                class inclusive:
                        offset = 1.166156
                        offsetErr = 0.003083
                        falling = 2.702703
                        fallingErr = 0.130622
                        
                        offsetMC = 1.162048
                        offsetErrMC = 0.006914
                        fallingMC = 1.833668
                        fallingErrMC = 0.290102
          



        

### rMuE for the old factorization method

class rMuE:

                class inclusive:
                        val = 1.224875
                        err = 0.122495
                        valMC = 1.200151
                        errMC = 0.120023
         



        

        
class rSFOFTrig:

                class inclusive:
                        val = 1.037309
                        err = 0.044300
                        valMC = 1.028570
                        errMC = 0.040851
      
        
        

        

        
### R_SFOF using the old factorization method
        
class rSFOFFactOld:                                   
        class inclusive:
                
                class SF:
                        val = 1.058721
                        err = 0.049932
                        valMC = 1.045737
                        errMC = 0.045619
      
                
                class EE:
                        val = 0.423435
                        err = 0.128345
                        valMC = 0.428517
                        errMC = 0.124620

                
                class MM:
                        val = 0.635287
                        err = 0.129929
                        valMC = 0.617220
                        errMC = 0.125862
      
        



        
### R_SFOF combination using the old factorization method

class rSFOF:

                class inclusive:
                        val = 1.085686
                        err = 0.038186
                        valMC = 1.068997
                        errMC = 0.031770
           

                                        

class rEEOF:

                class inclusive:
                        val = 0.450551
                        err = 0.022985
                        valMC = 0.439891
                        errMC = 0.017946
          
      


class rMMOF:

                class inclusive:
                        val = 0.668093
                        err = 0.043445
                        valMC = 0.649335
                        errMC = 0.026030
           
              



class triggerEffs:                                  
        class inclusive:
                
                class effEE:
                        val = 0.906570
                        err = 0.030186
                        valMC = 0.955457
                        errMC = 0.030024
      
                
                class effMM:
                        val = 0.873007
                        err = 0.030218
                        valMC = 0.949475
                        errMC = 0.030033

                
                class effEM:
                        val = 0.857633
                        err = 0.030132
                        valMC = 0.926005
                        errMC = 0.030018
              
        
        
              

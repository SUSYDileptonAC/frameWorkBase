#!/bin/bash

TEMPVAR=`pwd`
cd ../
git clone https://github.com/SUSYDileptonAC/DataMC.git
git clone https://github.com/SUSYDileptonAC/countsAndCorrections.git
git clone https://github.com/SUSYDileptonAC/Triggerefficiencies.git
git clone https://github.com/SUSYDileptonAC/edgeFitRunII.git
git clone https://github.com/SUSYDileptonAC/SubmitScripts.git

cd $TEMPVAR

#!/bin/bash

TEMPVAR=`pwd`
mkdir shelves
cd ../
git clone -b CMSDAS https://github.com/SUSYDileptonAC/DataMC.git
git clone -b CMSDAS https://github.com/SUSYDileptonAC/countsAndCorrections.git
git clone -b CMSDAS https://github.com/SUSYDileptonAC/edgeFitRunII.git
git clone -b CMSDAS https://github.com/SUSYDileptonAC/SignalScan.git

### make folders for figures, tables etc

cd frameWorkBase
mkdir shelves
mkdir tab

cd ../DataMC
mkdir fig
mkdir shelves

cd ../countsAndCorrections
mkdir fig
mkdir shelves

cd rMuE
mkdir fig
mkdir shelves

cd ../rOutIn
mkdir fig
mkdir shelves

cd ../rSFOF
mkdir fig
mkdir tab
mkdir shelves

cd ../TriggerEfficiencies
mkdir fig
mkdir shelves
mkdir tab

cd ../../edgeFitRunII
mkdir fig
mkdir figToys
mkdir shelves
mkdir shelves/dicts
mkdir workspaces

cd ../SignalScan
bash setup.sh

cd $TEMPVAR

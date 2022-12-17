# HSCPLimit

### Setup(once)

```bash
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.1.0
scramv1 b clean; scramv1 b # always make a clean build
cd ../
git clone git@github.com:Christinaw97/HSCPLimit.git
cd HSCPLimit
```

### datacards
datacards are created using the code: ```scripts/create_datacard_mass.py```
* need input ROOT file that contains mass distribution for signal and bkg

### produce limit trees
run ```run_datacards_mass.py``` to produce limit trees from datacards


### limit plots
limit plots are created using the code: ./scripts/MuonSystem_plots-limitPlot_cleaned.ipynb 

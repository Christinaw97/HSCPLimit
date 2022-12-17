"""
Code to combine the datacard of 3 categories in 2tag and produce limits for 2tag limits
"""
import numpy as np
import os
import sys

def readNorm(f_cscCard):
    f = open(f_cscCard,"r")
    norm = float(f.readline().split()[3])
    return norm

def insert(originalfile,string):
    with open(originalfile,'r') as f:
        with open('newfile.txt','w') as f2:
            f2.write(string)
            f2.write(f.read())
    os.rename('newfile.txt',originalfile)
if __name__ == '__main__':

	input_dir=os.getenv('CMSSW_BASE')+'/src/HiggsAnalysis/HSCPLimit/combine/datacards/mass/v2//histoMass_region_999'
	tree_dir=os.getenv('CMSSW_BASE')+'/src/HiggsAnalysis/HSCPLimit/combine/limitTrees/mass/v2//histoMass_region_999'
	os.system("mkdir -p {0}/".format(input_dir))
	os.system("mkdir -p {0}/".format(tree_dir))
    	samples = [
	'Gluino1800',
        'Gluino1600',
        'Gluino2000',
        'Gluino2200',
        'Gluino2400',
        'Gluino2600',]
	for sample in samples:
		name=sample
		run_combine = "combine -M AsymptoticLimits --run blind -n.{} {}/{}_nominal.txt".format(name, input_dir, name)
		os.system(run_combine)
		os.system("mv higgsCombine.{0}.AsymptoticLimits.mH120.root {1}/".format(name, tree_dir))

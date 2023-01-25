"""
Code to combine the datacard of 3 categories in 2tag and produce limits for 2tag limits
"""
import numpy as np
import os
import sys

def readNorm(f_cscCard):
    f = open(f_cscCard,"r")
    norm = float(f.readline().split()[-1])
    return norm

def insert(originalfile,string):
    with open(originalfile,'r') as f:
        with open('newfile.txt','w') as f2:
            f2.write(string)
            f2.write(f.read())
    os.rename('newfile.txt',originalfile)
if __name__ == '__main__':

	input_dir=os.getenv('CMSSW_BASE')+'/src/HiggsAnalysis/HSCPLimit/combine/datacards/test_Ias_probQ/v4/'
	tree_dir = input_dir.replace('datacards','limitTrees')
	os.system("mkdir -p {0}/all_cat".format(input_dir))
	os.system("mkdir -p {0}/all_cat".format(tree_dir))
    	samples = [
	'HSCPgluino_M-1800',
        'HSCPgluino_M-1000',
        'HSCPgluino_M-1400',
        'HSCPgluino_M-1600',
        'HSCPgluino_M-1800',
        'HSCPgluino_M-2000',
        'HSCPgluino_M-200',
        'HSCPgluino_M-2200',
        'HSCPgluino_M-2400',
        'HSCPgluino_M-2600',
        'HSCPgluino_M-400',
        'HSCPgluino_M-500',
        'HSCPgluino_M-800',
        #'HSCPgmsbStau_M-1029',
        #'HSCPgmsbStau_M-1409',
        #'HSCPgmsbStau_M-200',
        #'HSCPgmsbStau_M-247',
        #'HSCPgmsbStau_M-432',
        #'HSCPgmsbStau_M-651',
        #'HSCPgmsbStau_M-871',
	'HSCPpairStau_M-1218',
        'HSCPpairStau_M-1029',
        'HSCPpairStau_M-1599',
        'HSCPpairStau_M-1409',
        'HSCPpairStau_M-200',
        'HSCPpairStau_M-247',
        'HSCPpairStau_M-308',
        'HSCPpairStau_M-432',
        'HSCPpairStau_M-557',
        'HSCPpairStau_M-651',
        'HSCPpairStau_M-745',
        'HSCPpairStau_M-871',
	]
	#samples = ['HSCPgluinoOnlyNeutral_M-200', 'HSCPgluinoOnlyNeutral_M-400', 'HSCPgluinoOnlyNeutral_M-800', 'HSCPgluinoOnlyNeutral_M-1000', 'HSCPgluinoOnlyNeutral_M-1200', 'HSCPgluinoOnlyNeutral_M-1400', 'HSCPgluinoOnlyNeutral_M-1600', 'HSCPgluinoOnlyNeutral_M-1800', 'HSCPgluinoOnlyNeutral_M-2000', 'HSCPgluinoOnlyNeutral_M-2200', 'HSCPgluinoOnlyNeutral_M-2400', 'HSCPgluinoOnlyNeutral_M-2600', 'HSCPgluino_M-200', 'HSCPgluino_M-400', 'HSCPgluino_M-500', 'HSCPgluino_M-800', 'HSCPgluino_M-1000', 'HSCPgluino_M-1400', 'HSCPgluino_M-1600', 'HSCPgluino_M-1800', 'HSCPgluino_M-2000', 'HSCPgluino_M-2200', 'HSCPgluino_M-2400', 'HSCPgluino_M-2600', 'HSCPgmsbStau_M-1029', 'HSCPgmsbStau_M-1218', 'HSCPgmsbStau_M-1409', 'HSCPgmsbStau_M-1599', 'HSCPgmsbStau_M-200', 'HSCPgmsbStau_M-247', 'HSCPgmsbStau_M-308', 'HSCPgmsbStau_M-432', 'HSCPgmsbStau_M-557', 'HSCPgmsbStau_M-651', 'HSCPgmsbStau_M-745', 'HSCPgmsbStau_M-871', 'HSCPpairStau_M-1029', 'HSCPpairStau_M-1218', 'HSCPpairStau_M-1409', 'HSCPpairStau_M-1599', 'HSCPpairStau_M-200', 'HSCPpairStau_M-247', 'HSCPpairStau_M-308', 'HSCPpairStau_M-432', 'HSCPpairStau_M-557', 'HSCPpairStau_M-651', 'HSCPpairStau_M-745', 'HSCPpairStau_M-871', 'HSCPstopOnlyNeutral_M-1000', 'HSCPstopOnlyNeutral_M-100', 'HSCPstopOnlyNeutral_M-1200', 'HSCPstopOnlyNeutral_M-1400', 'HSCPstopOnlyNeutral_M-1600', 'HSCPstopOnlyNeutral_M-1800', 'HSCPstopOnlyNeutral_M-2000', 'HSCPstopOnlyNeutral_M-200', 'HSCPstopOnlyNeutral_M-2200', 'HSCPstopOnlyNeutral_M-2400', 'HSCPstopOnlyNeutral_M-2600', 'HSCPstopOnlyNeutral_M-400', 'HSCPstopOnlyNeutral_M-500', 'HSCPstopOnlyNeutral_M-800', 'HSCPstop_M-1000', 'HSCPstop_M-100', 'HSCPstop_M-1200', 'HSCPstop_M-1400', 'HSCPstop_M-1600', 'HSCPstop_M-1800', 'HSCPstop_M-2000', 'HSCPstop_M-200', 'HSCPstop_M-2200', 'HSCPstop_M-2400', 'HSCPstop_M-2600', 'HSCPstop_M-400', 'HSCPstop_M-500', 'HSCPstop_M-800', 'HSCPtauPrimeCharge1e_M-1000', 'HSCPtauPrimeCharge1e_M-100', 'HSCPtauPrimeCharge1e_M-1400', 'HSCPtauPrimeCharge1e_M-1800', 'HSCPtauPrimeCharge1e_M-200', 'HSCPtauPrimeCharge1e_M-2200', 'HSCPtauPrimeCharge1e_M-2600', 'HSCPtauPrimeCharge1e_M-400', 'HSCPtauPrimeCharge1e_M-500', 'HSCPtauPrimeCharge1e_M-800', 'HSCPtauPrimeCharge2e_M-1000', 'HSCPtauPrimeCharge2e_M-100', 'HSCPtauPrimeCharge2e_M-1400', 'HSCPtauPrimeCharge2e_M-1800', 'HSCPtauPrimeCharge2e_M-200', 'HSCPtauPrimeCharge2e_M-2200', 'HSCPtauPrimeCharge2e_M-2600', 'HSCPtauPrimeCharge2e_M-400', 'HSCPtauPrimeCharge2e_M-500']
	for ias in list(np.arange(0.3,0.7,0.05)):
    		for probq in list(np.arange(0.1,0.2,0.05)):
			ias = np.round(ias,2)
			probq = np.round(probq,2)
			if not (ias == 0.5 and probq == 0.1):continue
			for sample in samples:
				print("mode is {}, ias is {}, probQ is {}".format(sample, ias, probq))
				name="%(sample)s_ias%(ias)s_probq%(probq)s"%{
        	                    "sample":sample,"ias": str(ias).replace('.','p'), "probq": str(probq).replace('.','p')}
                		norm = readNorm("{0}/{1}.txt".format(input_dir, name))
                		if norm == 0.0:continue
				run_combine = "combine -M AsymptoticLimits --run blind -n.{0} {1}/{0}.txt --setParameters norm={2} --freezeParameter norm ".format(name, input_dir, 1./norm)
				print(run_combine)
				os.system(run_combine)
				os.system("mv higgsCombine.{0}.AsymptoticLimits.mH120.root {1}/".format(name, tree_dir))

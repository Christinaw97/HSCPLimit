"""

2022/10/03
create datacard from the mass distributions of signal and data in region D
using distributions that are already normalized from Dylan

"""

import ROOT as rt
import csv
import re
import sys
import collections
import os

from collections import OrderedDict
import uproot

import scipy
import awkward
import numpy as np
import time



def make_datacard_hscp(outDataCardsDir,  modelName, signal, bkg, observation, sig_unc, bkg_unc):

    text_file = open(outDataCardsDir+modelName+".txt", "w")

    text_file.write('imax {0} \n'.format(1))
    text_file.write('jmax {0} \n'.format(1))
    text_file.write('kmax * \n')
    text_file.write('shapes * * FAKE \n')



    text_file.write('--------------- \n')
    text_file.write('--------------- \n')
    text_file.write('bin \t  chD \n')
    text_file.write('observation \t {0:6.2f} \n'.format(observation))
    text_file.write('------------------------------ \n')
    text_file.write('bin \t chD \t chD \n')
    text_file.write('process \t signal \t bkg \n')
    text_file.write('process \t 0 \t 1 \t \n')
    text_file.write('rate \t {} \t {} \n'.format(signal, bkg))
    text_file.write('------------------------------ \n')

#   #### uncertainties ####
    for k,v in sig_unc.items():
        text_file.write('{} \t lnN \t {} \t - \n'.format(k, 1+v))

    for k,v in bkg_unc.items():
        if len(v)==2:text_file.write('{} \t lnN \t -  \t {}/{} \n'.format(k, v[0],v[1]))
        else:text_file.write('{} \t lnN \t -  \t {} \n'.format(k, v[0]))


    text_file.close()

if __name__ == '__main__':

# # load mass distributions
    fpath =OrderedDict()
    mass = OrderedDict()
    mass_plot = OrderedDict()

    # load root file
    path = "/storage/af/user/christiw/login-1/christiw/LLP/dedx/Dylan_histograms/v2/"
    fpath['test'] = path + 'histoMass_region_999.root'

    # load histograms
    file = rt.TFile.Open(fpath['test'], 'READ')
    mass_plot['predNominal'] = file.Get('predNominal')
    mass_plot['predUp'] = file.Get('predUp')
    mass_plot['predDown'] = file.Get('predDown')
    mass_plot['Gluino1600_nominal'] = file.Get('Gluino1600_nominal')
    mass_plot['Gluino1800_nominal'] = file.Get('Gluino1800_nominal')
    mass_plot['Gluino2000_nominal'] = file.Get('Gluino2000_nominal')
    mass_plot['Gluino2200_nominal'] = file.Get('Gluino2200_nominal')
    mass_plot['Gluino2400_nominal'] = file.Get('Gluino2400_nominal')
    mass_plot['Gluino2600_nominal'] = file.Get('Gluino2600_nominal')
    mass_plot['Gluino2600_nominal'].SetDirectory(0)

    # set mass cut for each signal sample
    cut={
       'Gluino1600_nominal': 600,
       'Gluino1800_nominal': 600,
       'Gluino2000_nominal': 670,
        'Gluino2200_nominal': 730,
        'Gluino2400_nominal': 800,
    }

    # set signal/bkg systematics
    sig_unc = {
        'lumi': 0.2,
    }
    bkg_unc = {
        'bkg_est': 0.0,
    }

    # output path for output datacard  directory
    outDataCardsDir = '/storage/af/user/christiw/login-1/christiw/LLP/dedx/CMSSW_10_2_13/src/HiggsAnalysis/HSCPLimit/combine/datacards/test_mass/v2/' + fpath['test'].replace('.root','/')[fpath['test'].find('histoMass'):]
    os.system("mkdir -p {0}".format(outDataCardsDir))


    signal_keys = []
    for s in mass_plot.keys():
        if not 'pred' in s: signal_keys.append(s)
    for s in signal_keys:
        signal_yield = 0
        bkg_nominal = 0
        bkg_up = 0
        bkg_down = 0

        for bin_i in range(mass_plot[s].GetNbinsX()):
            if mass_plot[s].GetBinLowEdge(bin_i+1) >= cut[s]:
                signal_yield+=mass_plot[s].GetBinContent(bin_i+1)
                bkg_nominal+=mass_plot['predNominal'].GetBinContent(bin_i+1)
                bkg_up+=mass_plot['predUp'].GetBinContent(bin_i+1)
                bkg_down+=mass_plot['predDown'].GetBinContent(bin_i+1)
        bkg_up/=bkg_nominal
        bkg_down /= bkg_nominal
        bkg_unc = {
            'bkg_est': [bkg_down, bkg_up]
        }
        print(s, signal_yield, bkg_nominal)
        make_datacard_hscp(outDataCardsDir, s, signal_yield*101/51.2, bkg_nominal*101/51.2 , bkg_nominal*101/51.2, sig_unc, bkg_unc)
        # hard coded input lumi of 51.2 and scaled lumi of 101/fb

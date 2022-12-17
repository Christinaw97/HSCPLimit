

import ROOT as rt
# import root_numpy as rtnp
import csv
import re
import sys
import collections
import os

from collections import OrderedDict
import uproot
import pandas as pd
import math
import scipy
import awkward
import numpy as np
import time
sys.path.append('/storage/af/user/christiw/gpu/christiw/llp/delayed_jet_analyzer/lib/')
from histo_utilities import std_color_list, create_TGraph, find_intersect


import CMS_lumi, tdrstyle
a = tdrstyle.setTDRStyle()
CMS_lumi.writeExtraText = 0



print(sys.version)




xsec_list = '/storage/af/user/christiw/login-1/christiw/LLP/dedx/CMSSW_10_6_30/src/llp_analyzer/data/xSections.dat'
models = ['HSCPgluinoOnlyNeutral', 'gluino', 'gmsbStau', 'pairStau', 'stopOnlyNeutral', 'stop', 'tauPrimeCharge1e', 'tauPrimeCharge2e']
models = [ 'gluino', ]


data = np.loadtxt(xsec_list, dtype=str)
xsec_hscp = {}
sample_names = []
for i in range(len(data)):
    if 'HSCP' in data[i,0]:
        name = data[i,0][:data[i,0].find('_TuneCP5')]
        xsec_hscp[name] = float(data[i, 1])
        flag = 0
        for m in models:
            if m in name:flag = 1
        if flag == 0:continue
        sample_names.append(name)

signal_names = {}
for m in models:
    mass = []
    signal_names[m] = []
    for s in sample_names:
        if m+'_' in s:
            signal_names[m].append(s)
            mass.append(int(s[s.find('M-')+2:]))
    mass = np.array(mass)
    inds = mass.argsort()
    signal_names[m] = list(np.array(signal_names[m])[inds])




signal = []
for k,v in signal_names.items():signal += v
print(signal)



limitTrees_90 =OrderedDict()
dataCards_90 = OrderedDict()
limits_90 = OrderedDict()

limitTrees_99 =OrderedDict()
dataCards_99 = OrderedDict()
limits_99 = OrderedDict()

limitTrees_999 =OrderedDict()
dataCards_999 = OrderedDict()
limits_999 = OrderedDict()


dataCardDir = '/storage/af/user/christiw/login-1/christiw/LLP/dedx/CMSSW_10_2_13/src/HiggsAnalysis/HSCPLimit/combine/datacards/test_mass/v2//histoMass_region_90/'
limitDir = dataCardDir.replace('datacards', 'limitTrees')

for s in signal:
    limitTrees_90[s] = {}
    dataCards_90[s] = {}
    name = s.replace('HSCPg', 'G')
    name = name.replace('_M-', '')
    dataCards_90[s] = dataCardDir + '{}_nominal.txt'.format(name)
    limitTrees_90[s] = limitDir + 'higgsCombine.{}'.format(name) + '.AsymptoticLimits.mH120.root'

for i,m in enumerate(limitTrees_90.keys()):
    if not os.path.isfile(dataCards_90[m]):
        continue
    if len(uproot.open(limitTrees_90[m]).keys()) == 2:
        T = uproot.open(limitTrees_90[m])['limit']
        limits_90[m] = np.array(T.array('limit'))

############################################


dataCardDir = '/storage/af/user/christiw/login-1/christiw/LLP/dedx/CMSSW_10_2_13/src/HiggsAnalysis/HSCPLimit/combine/datacards/test_mass/v2//histoMass_region_99/'
limitDir = dataCardDir.replace('datacards', 'limitTrees')

for s in signal:
    limitTrees_99[s] = {}
    dataCards_99[s] = {}
    name = s.replace('HSCPg', 'G')
    name = name.replace('_M-', '')
    dataCards_99[s] = dataCardDir + '{}_nominal.txt'.format(name)
    limitTrees_99[s] = limitDir + 'higgsCombine.{}'.format(name) + '.AsymptoticLimits.mH120.root'

for i,m in enumerate(limitTrees_99.keys()):
    if not os.path.isfile(dataCards_99[m]):
        continue
    if len(uproot.open(limitTrees_99[m]).keys()) == 2:
        T = uproot.open(limitTrees_99[m])['limit']
        limits_99[m] = np.array(T.array('limit'))

############################################
dataCardDir = '/storage/af/user/christiw/login-1/christiw/LLP/dedx/CMSSW_10_2_13/src/HiggsAnalysis/HSCPLimit/combine/datacards/test_mass/v2//histoMass_region_999/'
limitDir = dataCardDir.replace('datacards', 'limitTrees')

for s in signal:
    limitTrees_999[s] = {}
    dataCards_999[s] = {}
    name = s.replace('HSCPg', 'G')
    name = name.replace('_M-', '')
    dataCards_999[s] = dataCardDir + '{}_nominal.txt'.format(name)
    limitTrees_999[s] = limitDir + 'higgsCombine.{}'.format(name) + '.AsymptoticLimits.mH120.root'

for i,m in enumerate(limitTrees_999.keys()):
    if not os.path.isfile(dataCards_999[m]):
        continue
    if len(uproot.open(limitTrees_999[m]).keys()) == 2:
        T = uproot.open(limitTrees_999[m])['limit']
        limits_999[m] = np.array(T.array('limit'))




# load theoretical xsec
import json
path = '/storage/af/user/christiw/login-1/christiw/LLP/dedx/CMSSW_10_6_30/src/llp_analyzer/data/xsec/json/'
filenames = {
   'gluino': 'pp13_gluino_NNLO+NNLL.json',
#     'pp13_slep_LR_NLO+NLL_PDF4LHC.json',
#     'stop':'pp13_squark_NNLO+NNLL.json',
#     'chargino':'pp13_wino_C1C1_NLO+NLL.json',
#     'stau': 'pp13_stau_LR_NLO+NLL_PDF4LHC.json',
}
mass = {}
theoretical_xsec = {}
for f, file in filenames.items():
    data = json.load(open( path + file))
    mass[f] = []
    theoretical_xsec[f] = []
    for k,v in data['data'].items():
        mass[f].append(int(k))
        theoretical_xsec[f].append(float(v['xsec_pb']))
    mass[f] = np.array(mass[f])
    theoretical_xsec[f] = np.array(theoretical_xsec[f])
    inds = mass[f].argsort()
    mass[f] = mass[f][inds]
    theoretical_xsec[f] = theoretical_xsec[f][inds]


# make plots

leg = rt.TLegend(0.6,0.7,0.9,0.92)
leg.SetTextSize(0.03)
leg.SetBorderSize(0)
leg.SetEntrySeparation(0.01)

c = rt.TCanvas('c','c', 800, 800)
c.SetRightMargin(0.04)


rt.gStyle.SetOptFit(1011)

h = {}
h_exp1sig = {}
h_exp2sig = {}
h_obs = {}
h_others = {}
for i, k in enumerate(mass.keys()):
    h[k+'theoretical'] = create_TGraph(mass[k],theoretical_xsec[k],  axis_title=['mass [GeV]', '95% CL Limit on #sigma [pb]'])
#     leg.AddEntry(h[k+'theoretical'], 'theoretical_'+k)
    h[k+'theoretical'].SetLineColor(std_color_list[i])

for i, m in enumerate(signal_names.keys()):
    x = []
    y = []
    y_up = []
    y_down = []
    for key in limits_90.keys():
        if m in key and len(limits_90[key])>0:
            if 'gluino' in key:
                y.append(limits_90[key][2]*xsec_hscp[key])
                y_up.append(limits_90[key][3]*xsec_hscp[key])
                y_down.append(limits_90[key][1]*xsec_hscp[key])
            x.append(int(key[key.find('M-')+2:]))

    if len(x) ==0 :continue
    h[m+'_Ias90'] = create_TGraph(x,y_down,  axis_title=['mass [GeV]', '95% CL Limit on #sigma [pb]'])
    h_exp1sig[m + '_Ias90'] = create_TGraph(np.hstack((x, np.flip(x))), np.hstack((y_down, np.flip(y_up))))



    ######

    x = []
    y = []
    y_up = []
    y_down = []
    for key in limits_99.keys():
        if m in key and len(limits_99[key])>0:
            if 'gluino' in key:
                y.append(limits_99[key][2]*xsec_hscp[key])
                y_up.append(limits_99[key][3]*xsec_hscp[key])
                y_down.append(limits_99[key][1]*xsec_hscp[key])
            else: y.append(limits_99[key][2])
            x.append(int(key[key.find('M-')+2:]))
    if len(x) ==0 :continue
    h[m+'_Ias99'] = create_TGraph(x,y_down,  axis_title=['mass [GeV]', '95% CL Limit on #sigma [pb]'])
    h_exp1sig[m + '_Ias99'] = create_TGraph(np.hstack((x, np.flip(x))), np.hstack((y_down, np.flip(y_up))))


    ###
    x = []
    y = []
    y_up = []
    y_down = []
    for key in limits_999.keys():
        if m in key and len(limits_999[key])>0:
            if 'gluino' in key:
                y.append(limits_999[key][2]*xsec_hscp[key])
                y_up.append(limits_999[key][3]*xsec_hscp[key])
                y_down.append(limits_999[key][1]*xsec_hscp[key])
            else: y.append(limits_999[key][2])
            x.append(int(key[key.find('M-')+2:]))
    if len(x) ==0 :continue
    h[m+'_Ias99.9'] = create_TGraph(x,y_down,  axis_title=['mass [GeV]', '95% CL Limit on #sigma [pb]'])
    h_exp1sig[m + '_Ias99.9'] = create_TGraph(np.hstack((x, np.flip(x))), np.hstack((y_down, np.flip(y_up))))

for i, m in enumerate(h.keys()):
    leg.AddEntry(h[m],m, "L")
    h[m].SetLineColor(std_color_list[i])

    h[m].SetLineWidth(3)

#     h[m].SetLineStyle(2)
    h[m].SetLineWidth(3)


    h[m].GetXaxis().SetTitleOffset(1)
    h[m].GetYaxis().SetTitleSize(0.05)
    h[m].GetYaxis().SetTitleOffset(1.5)


for i,m in enumerate(h.keys()):
    h[m].GetXaxis().SetLimits(1500,3000.0)
    h[m].GetYaxis().SetRangeUser(1e-4,1)
    h[m].Draw('LA' if i == 0 else 'Lsame')
    if 'theoretical' in m:continue
    h_exp1sig[m].SetFillColorAlpha(std_color_list[i],0.5)
    h_exp1sig[m].Draw('Fsame')


tdrstyle.setTDRStyle()
CMS_lumi.cmsText     = "CMS"
iPos = 0
CMS_lumi.writeExtraText = 0

if( iPos==0 ): CMS_lumi.relPosX = 0.12
# CMS_lumi.CMS_lumi(c, 4, 0)
CMS_lumi.lumi_13TeV  = "101 fb^{-1}"
CMS_lumi.CMS_lumi(c, 4, iPos)


print('gluino', find_intersect(h['gluino_Ias90'],h['gluinotheoretical']))
print('gluino', find_intersect(h['gluino_Ias99'],h['gluinotheoretical']))
print('gluino', find_intersect(h['gluino_Ias99.9'],h['gluinotheoretical']))



leg.Draw()
c.SetLogy()
c.SetTicky(1)
c.SetTickx(1)


tdrstyle.setTDRStyle()
c.Draw()

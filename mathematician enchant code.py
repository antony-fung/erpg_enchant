# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 21:13:55 2025

@author: Antony
"""

# written by mathematician2075

import random
import statistics
import heapq
import numpy as np
import time
import math

from plotly.offline import plot
import pandas as pd
import plotly.express as px

x,y=np.ogrid[:11,:101]
A=np.array([0,40,20,15,12.5,10,7.5,6,5,4,3])
B=np.array([0,0.08,0.1,0.11,0.12,0.125,0.15,0.2,0.25,0.3,0.35])
C=np.array([0,0,0,95,90,80,70,65,60,55,50])
D=np.array([0,0,0,0.25,0.15,0.05,0.018,0.011,0.0069,0.00445,0.00265])
E=np.array([0,0.04,0.02,0.01,0.004,0.002,0,0,0,0,0])
F=np.array([0,0.001,0.0006,0.0002,0.00005,0.00001,0,0,0,0,0])
levelup=A[x]/(1+B[x]*y)
leveldown=np.maximum(0,D[x]*(y-C[x]))
reset=np.maximum(0,0.00005*(2*x+y-110))
tierup=E[x]+F[x]*y
stay=100-levelup-leveldown-reset-tierup

x,y,z=np.ogrid[:11,:102,:102]
levelup_transition=(z==y+1)*levelup[x,np.minimum(y,100)]
leveldown_transition=(z==y-1)*leveldown[x,np.minimum(y,100)]
levelreset_transition=(z==1)*reset[x,np.minimum(y,100)]
tierup_transition=(z==101)*tierup[x,np.minimum(y,100)]
stay_transition=(z==y)*stay[x,np.minimum(y,100)]

transition=levelup_transition+leveldown_transition+levelreset_transition+tierup_transition+stay_transition
transition=transition/100

for i in range(11):
    transition[i][0]=np.zeros(102)
    transition[i][0][0]=1
    transition[i][101]=np.zeros(102)
    transition[i][101][101]=1
transition[10][100]=np.zeros(102)
transition[10][100][100]=1

def info(tier,starting_level,end_flame,step,plot_it=True):
    if tier==10:
        end_level=100
    else:
        end_level=101
    # flame per enchant
    fpe=(tier-0.5)*step
    flame=0
    flame_count=[]
    chance_density=[]
    previous_prop=0
    step_transition=np.linalg.matrix_power(transition[tier],step)
    current_trans=step_transition
    while flame<end_flame:
        flame+=fpe
        flame_count.append(flame)
        current_prop=current_trans[starting_level][end_level]
        chance_density.append((current_prop-previous_prop)/fpe)
        previous_prop=current_prop
        current_trans=np.matmul(current_trans,step_transition)
    df=pd.DataFrame({'flame':flame_count,'probability density':chance_density})
    df['cum prob']=df['flame'][0]*df['probability density'].cumsum()
    mode=round(df['flame'][list(df['probability density']).index(max(df['probability density']))])
    df['new col']=df['cum prob'].map(lambda x:abs(x-0.5))
    median=round(df['flame'][list(df['new col']).index(min(df['new col']))])
    df['xfx']=df['flame'][0]*df['probability density']*df['flame']
    mean=round(sum(df['xfx']))
    print('mode: '+str(mode))
    print('median: '+str(median))
    print('mean: '+str(mean))
    df['new col 1']=df['cum prob'].map(lambda x:abs(x-0.025))
    df['new col 2']=df['cum prob'].map(lambda x:abs(x-0.975))
    low=round(df['flame'][list(df['new col 1']).index(min(df['new col 1']))])
    high=round(df['flame'][list(df['new col 2']).index(min(df['new col 2']))])
    print('95% CI: ['+str(low)+','+str(high)+']')
    if plot_it:
        plot(px.line(df,x='flame',y='probability density'))

def chances(tier,starting_level,flames):
    enchants=math.floor(flames/(tier-0.5))
    print('On average, '+f'{flames:,}'+' flames gives around '+f'{enchants:,}'+' enchants at tier '+str(tier))
    print('Exact chances of each ending level with '+f'{enchants:,}'+' enchants, starting at tier '+str(tier)+' level '+str(starting_level)+':')
    probabilities=np.linalg.matrix_power(transition[tier],enchants)
    if tier<10:
        for i in range(1,101):
            print('T'+str(tier)+'L'+str(i)+': '+f"{100*probabilities[starting_level][i]:.4f}"+'%')
        print('Tier '+str(tier+1)+' or above: '+f"{100*probabilities[starting_level][101]:.4f}"+'%')
    if tier==10:
        for i in range(1,100):
            print('T10L'+str(i)+': '+f"{100*probabilities[starting_level][i]:.4f}"+'%')
        print('T10L100: '+f"{100*(probabilities[starting_level][100]+probabilities[starting_level][101]):.4f}"+'%')
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydmr
import miblab

resultspath = os.path.join(os.getcwd(), 'build')
figpath = os.path.join(resultspath, 'Figs')
if not os.path.exists(figpath):
    os.makedirs(figpath)
tablespath = os.path.join(resultspath, 'Tables')
datapath = os.path.join(resultspath, 'Data')



def lines():

    studies = [
        'study_05_single_asunaprevir',
        'study_06_single_pioglitazone',
        'study_07_single_ketoconazole',
        'study_08_single_cyclosporine',
        'study_10_single_bosentan',
        'study_12_single_rifampicin',
        'study_09_single_placebo',
    ]

    # Set up the figure
    clr = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
        'tab:brown']
    fs = 10
    fig, ax = plt.subplots(2, len(studies), figsize=(len(studies)*1.5, 8))
    fig.subplots_adjust(wspace=0.2, hspace=0.1)

    for i, study in enumerate(studies):

        drug = study[16:]

        # Set up subfigures for the study
        ax[0,i].set_title(drug, fontsize=fs, pad=10)
        ax[0,i].set_ylim(0, 300)
        ax[0,i].set_xticklabels([])
        ax[1,i].set_ylim(0, 30)
        ax[1,i].set_xticklabels([])
        if i==0:
            ax[0,i].set_ylabel('khe (mL/min/100mL)', fontsize=fs)
            ax[0,i].tick_params(axis='y', labelsize=fs)
            ax[1,i].set_ylabel('kbh (mL/min/100mL)', fontsize=fs)
            ax[1,i].tick_params(axis='y', labelsize=fs)
        else:
            ax[0,i].set_yticklabels([])
            ax[1,i].set_yticklabels([])

        file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')
        dmr = pydmr.read(file, 'nest')

        # Plot the rate constants in units of mL/min/100mL
        for s in dmr['pars'].keys():
            studies = list(dmr['pars'][s].keys())
            x = [1]
            khe = [6000*dmr['pars'][s][studies[0]]['khe']]
            kbh = [6000*dmr['pars'][s][studies[0]]['kbh']] 
            if len(studies)==2:
                x += [2]
                khe += [6000*dmr['pars'][s][studies[1]]['khe']]
                kbh += [6000*dmr['pars'][s][studies[1]]['kbh']] 
            color = clr[int(s[-2:])-1]
            ax[0,i].plot(x, khe, '-', label=s, marker='o', markersize=6, 
                        color=color)
            ax[1,i].plot(x, kbh, '-', label=s, marker='o', markersize=6, 
                        color=color)

    plt.savefig(fname=os.path.join(figpath, 'six_compounds_lineplot'))



def averages():

    studies = [
        'study_05_single_asunaprevir',
        'study_06_single_pioglitazone',
        'study_07_single_ketoconazole',
        'study_08_single_cyclosporine',
        'study_10_single_bosentan',
        'study_12_single_rifampicin',
        'study_09_single_placebo',
    ]

    # Set up figure
    fs = 10
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(len(studies), 5))
    fig.subplots_adjust(left=0.3, right=0.7, wspace=0.25)

    ax0.set_title('khe effect (%)', fontsize=fs, pad=10)
    ax1.set_title('kbh effect (%)', fontsize=fs, pad=10)
    ax0.set_xlim(-100, 50)
    ax1.set_xlim(-100, 50)
    ax0.grid(which='major', axis='x', linestyle='-')
    ax1.grid(which='major', axis='x', linestyle='-')
    ax1.set_yticklabels([])

    # Loop over all studies
    for i, study in enumerate(studies):

        drug = study[16:]

        stats = pd.read_csv(os.path.join(tablespath, f'{study}_effect.csv'))
        stats = stats.set_index('parameter')

        # Calculate mean effect sizes and 59% CI on the mean.
        khe_eff = stats.at['mean','khe']
        kbh_eff = stats.at['mean','kbh']
        khe_eff_err = 1.96*stats.at['std','khe']/np.sqrt(stats.at['count','khe'])
        kbh_eff_err = 1.96*stats.at['std','kbh']/np.sqrt(stats.at['count','kbh'])

        # Plot mean effect size for khe along with 95% CI
        # Choose color based on magnitude of effect
        if khe_eff + khe_eff_err < -20:
            clr = 'tab:red'
        elif khe_eff + khe_eff_err < 0:
            clr = 'tab:orange'
        else:
            clr = 'tab:green'
        ax0.errorbar(khe_eff, drug, xerr=khe_eff_err, fmt='o', color=clr)

        # Plot mean effect size for kbh along with 95% CI
        # Choose color based on magnitude of effect
        if kbh_eff + kbh_eff_err < -20:
            clr = 'tab:red'
        elif kbh_eff + kbh_eff_err < 0:
            clr = 'tab:orange'
        else:
            clr = 'tab:green'
        ax1.errorbar(kbh_eff, drug, xerr=kbh_eff_err, fmt='o', color=clr)

    # Plot dummy values out of range to show a legend
    ax1.errorbar(-200, drug, 
                marker='o', 
                color='tab:red', 
                label='inhibition > 20%')
    ax1.errorbar(-200, drug, 
                marker='o', 
                color='tab:orange', 
                label='inhibition')
    ax1.errorbar(-200, drug, 
                marker='o', 
                color='tab:green', 
                label='no inhibition')
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.savefig(fname=os.path.join(figpath, 'six_compounds_averages'))


def chronic_cyclosporine_effect():

    fs = 10
    fig, ax = plt.subplots(2, 2, figsize=(2*2.5, 2*2.5))
    fig.subplots_adjust(left=0.15, wspace=0.25, hspace=0.25)

    # high dose khe
    groups = ['Cyclosporine (clinical dose)', 'Cyclosporine (placebo)']
    clr = {groups[0]:'b', groups[1]:'g'}
    for j, group in enumerate(groups):
        ax[0,j].set_title(group, fontsize=fs, pad=10)
        ax[1,j].set_xlabel('Day')
    for i, parameter in enumerate(['khe', 'kbh']):
        ax[i,0].set_ylabel(parameter + ' effect (%)')
    for i, parameter in enumerate(['khe', 'kbh']):
        for j, group in enumerate(groups):
            df = pd.read_csv(os.path.join(tablespath, f'study_01_effect_{group}.csv'))
            avr = df[f'{parameter} avr']
            err = df[f'{parameter} err']
            days = range(len(avr))
            ax[i,j].set_xticks(days)
            ax[i,j].set_ylim(-100,50)
            ax[i,j].plot(days, avr, '-', label=group, 
                         marker='o', markersize=6, color=clr[group])
            ax[i,j].errorbar(days, avr, yerr=err, fmt='o', color=clr[group])

    plt.savefig(fname=os.path.join(figpath, 'chronic_cyclosporine_effect'))



def chronic_cyclosporine_absolute():

    fs = 10
    fig, ax = plt.subplots(2, 2, figsize=(2*2.5, 2*2.5))
    fig.subplots_adjust(wspace=0.25, hspace=0.25)

    # high dose khe
    groups = ['Cyclosporine (clinical dose)', 'Cyclosporine (placebo)']
    clr = {groups[0]:'b', groups[1]:'g'}
    for j, group in enumerate(groups):
        ax[0,j].set_title(group, fontsize=fs, pad=10)
        ax[1,j].set_xlabel('Day')
    for i, parameter in enumerate(['khe', 'kbh']):
        ax[i,0].set_ylabel(parameter + ' (mL/min/100cm3)')
    #ylim = {'khe': (0,0.02), 'kbh':(0,0.003)}
    ylim = {'khe': (0,250), 'kbh':(0,25)}
    for i, parameter in enumerate(['khe', 'kbh']):
        for j, group in enumerate(groups):
            df = pd.read_csv(os.path.join(tablespath, f'study_01_{group}.csv'))
            avr = df[f'{parameter} avr']
            err = df[f'{parameter} err']
            days = range(len(avr))
            ax[i,j].set_xticks(days)
            ax[i,j].set_ylim(ylim[parameter])
            ax[i,j].plot(days, 6000*avr, '-', label=group, 
                         marker='o', markersize=6, color=clr[group])
            ax[i,j].errorbar(days, 6000*avr, yerr=6000*err, fmt='o', color=clr[group])

    plt.savefig(fname=os.path.join(figpath, 'chronic_cyclosporine_absolute'))




def chronic_rifampicin_absolute():

    fs = 10
    fig, ax = plt.subplots(2, 3, figsize=(3*2.5, 2*2.5))
    fig.subplots_adjust(wspace=0.25, hspace=0.25)

    # high dose khe
    groups = ['Rifampicin (high dose)', 'Rifampicin (clinical dose)', 'Rifampicin (placebo)']
    clr = {groups[0]:'r', groups[1]:'b', groups[2]:'g'}
    for j, group in enumerate(groups):
        ax[0,j].set_title(group, fontsize=fs, pad=10)
        ax[1,j].set_xlabel('Day')
    for i, parameter in enumerate(['khe', 'kbh']):
        ax[i,0].set_ylabel(parameter + ' (mL/min/100cm3)')
    #ylim = {'khe': (0,0.02), 'kbh':(0,0.003)}
    ylim = {'khe': (0,6000*0.02), 'kbh':(0,6000*0.003)}
    for i, parameter in enumerate(['khe', 'kbh']):
        for j, group in enumerate(groups):
            df = pd.read_csv(os.path.join(tablespath, f'study_01_{group}.csv'))
            avr = df[f'{parameter} avr']
            err = df[f'{parameter} err']
            days = range(len(avr))
            ax[i,j].set_xticks(days)
            ax[i,j].set_ylim(ylim[parameter])
            ax[i,j].plot(days, 6000*avr, '-', label=group, 
                         marker='o', markersize=6, color=clr[group])
            ax[i,j].errorbar(days, 6000*avr, yerr=6000*err, fmt='o', color=clr[group])

    plt.savefig(fname=os.path.join(figpath, 'chronic_rifampicin_absolute'))


def chronic_rifampicin_effect():

    fs = 10
    fig, ax = plt.subplots(2, 3, figsize=(3*2.5, 2*2.5))
    fig.subplots_adjust(wspace=0.25, hspace=0.25)

    # high dose khe
    groups = ['Rifampicin (high dose)', 'Rifampicin (clinical dose)', 'Rifampicin (placebo)']
    clr = {groups[0]:'r', groups[1]:'b', groups[2]:'g'}
    for j, group in enumerate(groups):
        ax[0,j].set_title(group, fontsize=fs, pad=10)
        ax[1,j].set_xlabel('Day')
    for i, parameter in enumerate(['khe', 'kbh']):
        ax[i,0].set_ylabel(parameter + ' effect (%)')
    for i, parameter in enumerate(['khe', 'kbh']):
        for j, group in enumerate(groups):
            df = pd.read_csv(os.path.join(tablespath, f'study_01_effect_{group}.csv'))
            avr = df[f'{parameter} avr']
            err = df[f'{parameter} err']
            days = range(len(avr))
            ax[i,j].set_xticks(days)
            ax[i,j].set_ylim(-100,100)
            ax[i,j].plot(days, avr, '-', label=group, 
                         marker='o', markersize=6, color=clr[group])
            ax[i,j].errorbar(days, avr, yerr=err, fmt='o', color=clr[group])

    plt.savefig(fname=os.path.join(figpath, 'chronic_rifampicin_effect'))


def reproducibility():

    df = pd.read_csv(os.path.join(tablespath, 'reproducibility.csv'))

    fs = 10
    fig, ax = plt.subplots(1, 2, figsize=(2*4, 1*3))
    fig.subplots_adjust(wspace=0.25, hspace=0.25, bottom=0.2)
    studies = 1 + np.arange(len(df))
    ylim = {'khe': (0,250), 'kbh':(0,30)}
    for i, parameter in enumerate(['khe', 'kbh']):
        avr = df[f'{parameter} avr']
        err = df[f'{parameter} err']
        ax[i].set_xticks(studies)
        ax[i].set_ylim(ylim[parameter])
        ax[i].plot(studies, avr, linestyle='none', marker='o', markersize=6, color='r')
        ax[i].errorbar(studies, avr, yerr=err, fmt='o', color='r')
        avr = np.mean(avr)
        err = 1.96*np.std(avr)/np.sqrt(len(studies))
        ax[i].plot(studies, 0*studies + avr, linestyle='-', color='k')
        ax[i].plot(studies, 0*studies + avr - err, linestyle='--', color='grey')
        ax[i].plot(studies, 0*studies + avr + err, linestyle='--', color='grey')
        ax[i].set_xlabel('Study')
        ax[i].set_ylabel(parameter + ' (mL/min/100cm3)')

    plt.savefig(fname=os.path.join(figpath, 'reproducibility'))


def all():
    lines()
    averages()
    chronic_rifampicin_absolute()
    chronic_rifampicin_effect()
    chronic_cyclosporine_absolute()
    chronic_cyclosporine_effect()
    reproducibility()   


if __name__ == '__main__':
    # lines()
    averages()
    # chronic_rifampicin_absolute()
    # chronic_rifampicin_effect()
    # chronic_cyclosporine_absolute()
    # chronic_cyclosporine_effect()
    # reproducibility()

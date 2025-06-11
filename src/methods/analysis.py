import os

import numpy as np
import pandas as pd
import pydmr
import miblab


resultspath = os.path.join(os.getcwd(), 'build')
datapath = os.path.join(resultspath, 'Data')
if not os.path.exists(datapath):
    os.makedirs(datapath)
tablespath = os.path.join(resultspath, 'Tables')
if not os.path.exists(tablespath):
    os.makedirs(tablespath)



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

    # Loop over all studies
    for i, study in enumerate(studies):

        file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')

        # Pivot data for both visits of the study for easy access:
        dmr = pydmr.read(file, 'pandas', study='Day_1')
        params = dmr['pars'].query("parameter not in ['center','substance']")
        params = params.copy()
        params['value'] = pd.to_numeric(params['value'], errors='coerce')
        v1 = pd.pivot_table(params, values='value', 
                            columns='parameter', index='subject')
        dmr = pydmr.read(file, 'pandas', study='Day_2')
        params = dmr['pars'].query("parameter not in ['center','substance']")
        params = params.copy()
        params['value'] = pd.to_numeric(params['value'], errors='coerce')
        v2 = pd.pivot_table(params, values='value', 
                            columns='parameter', index='subject')
        
        # Calculate effect size for the drug in %
        effect = 100*(v2-v1)/v1

        # Get descriptive statistics
        stats = effect.describe()

        # Save as csv
        stats.index.name = 'parameter'
        stats.reset_index()
        stats.to_csv(os.path.join(tablespath, f'{study}_effect.csv'))



def chronic_cyclosporine_effect():

    # Read data
    study = 'study_02_chronic_cyclosporine_placebo'
    file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')

    # high dose khe
    groups = ['Cyclosporine (clinical dose)', 'Placebo']
    pars = pydmr.read(file, 'nest')['pars']
    avr = np.zeros((2, 3))
    err = np.zeros((2, 3))# paramter, study, avr/err
    for j, group in enumerate(groups):
        data = {}
        for i, parameter in enumerate(['khe', 'kbh']):
            vals = []
            for subj in pars.keys():
                subj_vals = []
                for study in pars[subj].keys():
                    if pars[subj][study]['substance'] == group:
                        subj_vals.append(pars[subj][study][parameter])
                if subj_vals != []:
                    subj_vals += [np.nan] * (3 - len(subj_vals))
                    vals.append(subj_vals)
            vals = np.array(vals) # (subjects, days)
            vals = 100 *( (vals / vals[:, [0]]) - 1 ) # effect size
            avr = np.nanmean(vals, axis=0)
            err = 1.96*np.nanstd(vals, axis=0)/np.sqrt(vals.shape[0])
            data[f'{parameter} avr'] = avr
            data[f'{parameter} err'] = err
        data['Day'] = 1 + np.arange(len(data['khe avr']))
        df = pd.DataFrame(data)
        name = group.replace('Placebo', 'Cyclosporine (placebo)')
        df.to_csv(os.path.join(tablespath, f'study_01_effect_{name}.csv'), index=None)


def chronic_cyclosporine_absolute():

    # Read data
    study = 'study_02_chronic_cyclosporine_placebo'
    file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')

    # high dose khe
    groups = ['Cyclosporine (clinical dose)', 'Placebo']
    pars = pydmr.read(file, 'nest')['pars']
    avr = np.zeros((2, 3))
    err = np.zeros((2, 3))# paramter, study, avr/err
    for j, group in enumerate(groups):
        data = {}
        for i, parameter in enumerate(['khe', 'kbh']):
            vals = []
            for subj in pars.keys():
                subj_vals = []
                for study in pars[subj].keys():
                    if pars[subj][study]['substance'] == group:
                        subj_vals.append(pars[subj][study][parameter])
                if subj_vals != []:
                    subj_vals += [np.nan] * (3 - len(subj_vals))
                    vals.append(subj_vals)
            vals = np.array(vals) # (subjects, days)
            avr = np.nanmean(vals, axis=0)
            err = 1.96*np.nanstd(vals, axis=0)/np.sqrt(vals.shape[0])
            data[f'{parameter} avr'] = avr
            data[f'{parameter} err'] = err
        data['Day'] = 1 + np.arange(len(data['khe avr']))
        df = pd.DataFrame(data)
        name = group.replace('Placebo', 'Cyclosporine (placebo)')
        df.to_csv(os.path.join(tablespath, f'study_01_{name}.csv'), index=None)




def chronic_rifampicin_absolute():

    # Read data
    study = 'study_01_chronic_rifampicin_placebo'
    file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')

    # high dose khe
    groups = ['Rifampicin (high dose)', 'Rifampicin (clinical dose)', 'Placebo']
    pars = pydmr.read(file, 'nest')['pars']
    avr = np.zeros((2, 3))
    err = np.zeros((2, 3))# paramter, study, avr/err
    for j, group in enumerate(groups):
        data = {}
        for i, parameter in enumerate(['khe', 'kbh']):
            vals = []
            for subj in pars.keys():
                subj_vals = []
                for study in pars[subj].keys():
                    if pars[subj][study]['substance'] == group:
                        subj_vals.append(pars[subj][study][parameter])
                if subj_vals != []:
                    subj_vals += [np.nan] * (4 - len(subj_vals))
                    vals.append(subj_vals)
            vals = np.array(vals) # (subjects, days)
            avr = np.nanmean(vals, axis=0)
            err = 1.96*np.nanstd(vals, axis=0)/np.sqrt(vals.shape[0])
            data[f'{parameter} avr'] = avr
            data[f'{parameter} err'] = err
        data['Day'] = 1 + np.arange(len(data['khe avr']))
        df = pd.DataFrame(data)
        name = group.replace('Placebo', 'Rifampicin (placebo)')
        df.to_csv(os.path.join(tablespath, f'study_01_{name}.csv'), index=None)


def chronic_rifampicin_effect():

    # Read data
    study = 'study_01_chronic_rifampicin_placebo'
    file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')

    # high dose khe
    groups = ['Rifampicin (high dose)', 'Rifampicin (clinical dose)', 'Placebo']
    pars = pydmr.read(file, 'nest')['pars']
    avr = np.zeros((2, 3))
    err = np.zeros((2, 3))# paramter, study, avr/err
    for j, group in enumerate(groups):
        data = {}
        for i, parameter in enumerate(['khe', 'kbh']):
            vals = []
            for subj in pars.keys():
                subj_vals = []
                for study in pars[subj].keys():
                    if pars[subj][study]['substance'] == group:
                        subj_vals.append(pars[subj][study][parameter])
                if subj_vals != []:
                    subj_vals += [np.nan] * (4 - len(subj_vals))
                    vals.append(subj_vals)
            vals = np.array(vals) # (subjects, days)
            vals = 100 *( (vals / vals[:, [0]]) - 1 ) # effect size
            avr = np.nanmean(vals, axis=0)
            err = 1.96*np.nanstd(vals, axis=0)/np.sqrt(vals.shape[0])
            data[f'{parameter} avr'] = avr
            data[f'{parameter} err'] = err
        data['Day'] = 1 + np.arange(len(data['khe avr']))
        df = pd.DataFrame(data)
        name = group.replace('Placebo', 'Rifampicin (placebo)')
        df.to_csv(os.path.join(tablespath, f'study_01_effect_{name}.csv'), index=None)



def reproducibility():

    studies = [
        'study_01_chronic_rifampicin_placebo',
        'study_02_chronic_cyclosporine_placebo',
        'study_03_single_bosentan',
        'study_04_placebo_rifampicin',
        'study_05_single_asunaprevir',
        'study_06_single_pioglitazone',
        'study_07_single_ketoconazole',
        'study_08_single_cyclosporine',
        'study_09_single_placebo',
        'study_10_single_bosentan',
        'study_11_control',
        'study_12_single_rifampicin',
        'study_13_field_strength',
    ]
    k_avr = np.zeros((2, 13))
    k_err = np.zeros((2, 13))# paramter, study, avr/err
    for j, study in enumerate(studies):
        file = miblab.zenodo_fetch(f'tristan_rats_{study}.dmr.zip', datapath, '15644248')
        pars = pydmr.read(file, 'nest', study='Day_1')['pars']
        for i, parameter in enumerate(['khe', 'kbh']):
            vals = [pars[subj]['Day_1'][parameter] for subj in pars.keys()]
            k_avr[i,j] = 6000*np.mean(vals)
            k_err[i,j] = 6000*1.96*np.std(vals)/np.sqrt(len(vals))

    data = {
        'study': studies,
        'khe avr': k_avr[0,:],
        'khe err': k_err[0,:],
        'kbh avr': k_avr[1,:],
        'kbh err': k_err[1,:],
    }
    df = pd.DataFrame(data, index=studies)
    df.to_csv(os.path.join(tablespath, 'reproducibility.csv'), index=None)

def all():
    averages()
    chronic_rifampicin_absolute()
    chronic_rifampicin_effect()
    chronic_cyclosporine_absolute()
    chronic_cyclosporine_effect()
    reproducibility()

if __name__ == '__main__':
    # averages()
    # chronic_rifampicin_absolute()
    # chronic_rifampicin_effect()
    # chronic_cyclosporine_absolute()
    # chronic_cyclosporine_effect()
    reproducibility()

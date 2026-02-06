# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:02:27 2019

@author: Jacob
"""
import numpy as np
import os
import logging

MODELS_ALLOWED = ['prolate','oblate', 'cylinder']

def initiator(dictionary_of_samples):
    #dictionary_of_samples = FileReader()
    
    possible_names = dictionary_of_samples.keys()
    print("The possible names are: \n")
    for name in possible_names:
       print(name)
    sampleName = str(input('STEP 3: Enter the desired sample name exactly as shown above (this is required to load your experimental data from the dictionary for aspect ratio models): '))
    
    loop_or_not = str(input('STEP 4: If you would like to loop over ALL data rows in the dataset (for batch fitting), enter exactly \'1\' and press enter. Otherwise (for single sample analysis), type any other key.\n'))
    if loop_or_not != '1':
        
        print('Available samples are below.\n')
         #{[tuple([1,len(j)]) for j in FileReader().values()]}
        
        counter = 1
        for title in np.transpose(dictionary_of_samples[sampleName])[0]:
            print(f'Sample number {counter}: {title}')
            counter+=1
            
        sampleNum = int(input(f'STEP 4 continued: Enter the sample number to analyze (must be a valid integer from the list above): '))
        model = str(input('STEP 5: Enter the model to be used for aspect ratio fitting (must be exactly one of: prolate, oblate, or cylinder): '))
        assert model in MODELS_ALLOWED, f'User entry \"{model}\" is not a valid model.\nPlease enter a valid model: {MODELS_ALLOWED}.'

        solver_choice = input('STEP 5.5: Choose solver method for root optimization (default "hybr" from scipy.optimize.root; enter "hybr", "lm", "broyden1", or "compare" to run all 3 and compare solutions): ') or "hybr"
        plot_type = input('STEP 6: For the plotting step, enter exactly "html" to write figure to HTML (and auto-open in browser) OR "png" to save as PNG image in working dir (default) or your specified location: ')
        if plot_type == 'png':
            save_loc = input('STEP 6 continued (PNG only): Enter full path for PNG save location, or press enter to use default (current working directory): ') or os.getcwd()
        else:
            save_loc = None

        try:
            sample = dictionary_of_samples[sampleName][sampleNum - 1]
        except KeyError:
            logging.error("Incorrect sample name entered.")
            print("Incorrect name entered.")
            exit()
        
        name,T,D_tr,D_rot = sample
    
        return False, [model, T, D_tr, D_rot, plot_type, save_loc, solver_choice]
        
    if loop_or_not == '1':
        model = str(input('STEP 5: Enter the model to be used for aspect ratio fitting (must be exactly one of: prolate, oblate, or cylinder): '))
        assert model in MODELS_ALLOWED, f'User entry \"{model}\" is not a valid model.\nPlease enter a valid model: {MODELS_ALLOWED}.'

        solver_choice = input('STEP 5.5: Choose solver method for root optimization (default "hybr" from scipy.optimize.root; enter "hybr", "lm", "broyden1", or "compare" to run all 3 and compare solutions): ') or "hybr"
        plot_type = input('STEP 6: For the plotting step, enter exactly "html" to write figure to HTML (and auto-open in browser) OR "png" to save as PNG image in working dir (default) or your specified location: ')
        if plot_type == 'png':
            save_loc = input('STEP 6 continued (PNG only): Enter full path for PNG save location, or press enter to use default (current working directory): ') or os.getcwd()
        else:
            save_loc = None

        temp_dic = dictionary_of_samples[sampleName]
        for j in temp_dic:
            j[0] = model
            j.extend([plot_type, save_loc, solver_choice])
            # replacement to fit the return scheme

        return True, temp_dic 
        
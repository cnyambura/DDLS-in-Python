# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 18:09:39 2020

@author: Jacob
"""

import logging

def _catchable_input(input_type):
    try:
        x=input(f"STEP: Now enter your experimental data value in the required format below (see example printed earlier). For ({input_type}):\t")
        if input_type != "D_tr":
            return x
        else:
            return x + " * (1e-9)**2/(1e-6)"

    except KeyboardInterrupt:
        logging.error("Keyboard interrupt during data input")
        print("Exiting...")
        
        

def AddMoreData():
    data_array = []
    dataset_string=""
    stock_name = input("STEP 2: Please type the name of the new dataset (e.g. your nanoparticle sample like \"stocksAndrew\" or \"prolate_test\") and press Enter. This will be the key in the data dictionary.\n")
    
    print("""STEP 2 continued: The dataset MUST follow this exact format for parsing into the dictionary used for the 3 aspect ratio models (prolate/oblate/cylinder). Enter one row per sample (title + 3 values). Example:
          \n(title)\t(temp.[K])\t(D_translation [nm^2/us])\t(D_rotational [10^-4/us])
          \nno.5\t 298.15\t\t 3.07 \t\t 111\n\n""")
    
    exit_word=""
    while exit_word != "stop":
        try:
            for keyword in ["title", "temp.", "D_tr", "D_rot"]:
                dataset_string += _catchable_input(keyword) + ", "
            exit_word = input("STEP 2 continued: Type exactly \"stop\" (lowercase) if you have reached the end of your dataset. Otherwise, press any other key to add another data row.\n")
        except KeyboardInterrupt:
            logging.error("Keyboard interrupt in data loop")
            print("broke out of loop")
            break
        
        data_array.append(dataset_string[:-2])
        dataset_string = ""
    return stock_name, data_array

        
        
def WriteToFile(name,data_array):
    fo = open("sample_data.txt", "a+") # a+ necc to append data
    fo.write(f"\n===\n{name}\n")
    for dataset_string in data_array:
        fo.write(f"{dataset_string}\n")
    fo.write('...\n')
    
def writer():
    WriteToFile(*AddMoreData())
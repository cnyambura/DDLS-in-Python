# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:54:21 2020

@author: Jacob
"""

import sys
sys.path.insert(0, 'src')  # for src layout

from ddls.data_file_writer import writer
from ddls.data_file_reader import FileReader
from ddls.Calculations import runner
from ddls.sample_initializer import initiator
import logging
import warnings

# minimal setup for error tracking and warnings
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ddls_errors.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
warnings.simplefilter("always")
logging.captureWarnings(True)
# warnings to own file too
warnings_logger = logging.getLogger("py.warnings")
warnings_logger.addHandler(logging.FileHandler("ddls_warnings.log"))
warnings_logger.setLevel(logging.WARNING)

sample_dictionary = FileReader()
newdata = input("STEP 1: If you would like to add a new dataset (e.g. to include your experimental nanoparticle data for aspect ratio fitting), type exactly \"yes\" and press enter. Otherwise, press any other key to proceed directly to analysis using existing data in sample_data.txt.\n")

if newdata == 'yes':
    # Proceed to add new data:
    try:
        writer()
    except Exception as err:
        logger.error(f'Error adding experimental data: {err}')
        print("Data addition failed. Check ddls_errors.log. Exiting...")
        exit()
    print("Data added. Re-run file to analyze this data. Exiting...")

else:
    # Let the user select the model on dataset(s) of choice:
    is_looped, model = initiator(sample_dictionary)
    try:
        if is_looped:
            for model_params in model:
                print(model_params)

                runner(*model_params)
        else:
            runner(*model)

    except Exception as err:
        logger.error(f'Model analysis error: {err}')
        print("Model analysis failed. Check ddls_errors.log. Exiting...")


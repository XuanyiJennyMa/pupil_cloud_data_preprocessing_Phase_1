import numpy as np
import pandas as pd
import glob

def label_gaze(list_of_pic):
    for pic in list_of_pic:
        foldername = glob.glob('*' + pic + '_csv')
        path_to_gaze_data = foldername[0]
        gaze = pd.read_csv(f"{path_to_gaze_data}/fixations.csv")
        #import the section information for participant order
        path_to_gaze_info = foldername[0]
        section = pd.read_csv(f"{path_to_gaze_info}/sections.csv")
        gaze["Participant"] = None
        for order in range(len(section)):
            participant_match = gaze[gaze["section id"] == section['section id'][order]]
            filted_index = participant_match.index.to_list()
            gaze.loc[filted_index, 'Participant'] = section['wearer name'][order]
        save_file_name = 'labelled_gaze.csv'
        gaze.to_csv(f"{path_to_gaze_data}/{save_file_name}", index=False) 
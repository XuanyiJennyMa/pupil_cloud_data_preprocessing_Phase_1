"""
This script is used for labelling the gaze data with the wearer name (or participant number in the example)
Please note, folders that contain enrichment data should be saved within the same directory with this script.

"""

# Import libraries
import pandas as pd
import glob


def label_gaze(list_of_pic):
    for pic in list_of_pic:
        # Import the gaze data
        # If you have changed the folder name to be the same as the picture name
        path_to_gaze_data = "./" + pic
        # If you keep the folder name as how it was downloaded from Pupil Cloud, comment the line above and uncomment the two lines below:
        # foldername = glob.glob('*' + pic + '_csv')
        # path_to_gaze_data = foldername[0]
        gaze = pd.read_csv(f"{path_to_gaze_data}/gaze.csv")

        # Import the section file for the wearer information
        # Label the gaze data 
        section = pd.read_csv(f"{path_to_gaze_data}/sections.csv")
        gaze["Participant"] = None
        for order in range(len(section)):
            participant_match = gaze[gaze["section id"] == section['section id'][order]]
            filted_index = participant_match.index.to_list()
            gaze.loc[filted_index, 'Participant'] = section['wearer name'][order]
        save_file_name = 'labelled_gaze.csv'
        gaze.to_csv(f"{path_to_gaze_data}/{save_file_name}", index=False) 


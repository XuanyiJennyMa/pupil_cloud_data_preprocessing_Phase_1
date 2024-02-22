# This script is used for labelling the fixations data with the AOIs and wearer name (or participant number in the example)
# It is a modified version of some codes in Pupil Labs' gallery_demo_analysis:
#       https://github.com/pupil-labs/gallery_demo_analysis/blob/main/1_Defining%20Nested%20AOIs.ipynb
# Please note, folders that contain enrichment data should be saved within the same directory with this script.

# Import libraries
import numpy as np
import pandas as pd
import glob

# This function is for the detection of fixations inside AOIs
# Original code can be found in Pupil Labs' script as indicated above.
def check_in_rect(fixation_data, rectangle_coordinates):
    """
    returns an array with the length of fixation_data, which is True, when the entry in fixation_data
    was inside rectangle_coordinates and False otherwise.
    """

    # unpack the rectangle coordinates
    rect_x, rect_y, rect_width, rect_height = rectangle_coordinates

    # check if the fixation was within the x- and y-borders
    x_hit = fixation_data["fixation x [px]"].between(rect_x, rect_x + rect_width)
    y_hit = fixation_data["fixation y [px]"].between(rect_y, rect_y + rect_height)

    in_rect_idx = x_hit & y_hit

    return in_rect_idx
# The function above will be called in the functions below.

def label_aoi_diff_pic(list_of_pics):
    for pic in list_of_pics:
        # Import the saved AOI information
        aoi_filepath = "./AOI_information/" + pic + '_AOIs.csv'
        aois = pd.read_csv(aoi_filepath, sep=',')
        aois = aois.to_numpy()
        paintings = [idx for idx in range(len(aois))]
        
        # Import the fixation data
        # If you have changed the folder name to be the same as the picture name
        data_folder = "./" + pic
        # If you keep the folder name as how it was downloaded from Pupil Cloud, comment the line above and uncomment the two lines below:
        # foldername = glob.glob('*' + pic + '_csv')
        # data_folder = "./" + foldername
        fixations = pd.read_csv(f"{data_folder}/fixations.csv")
        fixations = fixations[fixations["fixation detected in reference image"]]
        
        # Import the section file for the wearer information
        section = pd.read_csv(f"{data_folder}/sections.csv")
        fixations["Participant"] = None
        for order in range(len(section)):
            participant_match = fixations[fixations["section id"] == section['section id'][order]]
            filted_index = participant_match.index.to_list()
            fixations.loc[filted_index, 'Participant'] = section['wearer name'][order]
        
        # Create a new column in the fixations dataframe
        fixations["AOI"] = None

        # Assign the AOI ID to those fixations that were inside the AOI
        for aoi_id, aoi in enumerate(aois):
            fixations.loc[check_in_rect(fixations, aoi), "AOI"] = paintings[aoi_id]

        # Save the labelled file
        save_file_name = 'labelled_fixations.csv'
        fixations.to_csv(f"{data_folder}/{save_file_name}", index=False)  

def label_aoi_same_pic(pic, versions):
    #import the fixation data
    # If you have changed the folder name to be the same as the picture name
    data_folder = "./" + pic
    # If you keep the folder name as how it was downloaded from Pupil Cloud, comment the line above and uncomment the two lines below:
    # foldername = glob.glob('*' + pic + '_csv')
    # data_folder = "./" + foldername
    fixations = pd.read_csv(f"{data_folder}/fixations.csv")
    fixations = fixations[fixations["fixation detected in reference image"]]
    
    for version in range(versions):
        # Import the saved AOI information
        aoi_filepath = "./AOI_information/" + pic+'_'+str(version)+'_AOIs.csv'
        aois = pd.read_csv(aoi_filepath, sep=',')
        aois = aois.to_numpy()
        paintings = [idx for idx in range(len(aois))]
        
        # Import the section file for the wearer information
        section = pd.read_csv(f"{data_folder}/sections.csv")
        fixations["Participant"] = None
        for order in range(len(section)):
            participant_match = fixations[fixations["section id"] == section['section id'][order]]
            filted_index = participant_match.index.to_list()
            fixations.loc[filted_index, 'Participant'] = section['wearer name'][order]
        
        # Create a new column in the fixations dataframe
        column_name = 'AOI_' + str(version)
        fixations[column_name] = None

        # Assign the AOI ID to those fixations that were inside the AOI
        for aoi_id, aoi in enumerate(aois):
            fixations.loc[check_in_rect(fixations, aoi), column_name] = paintings[aoi_id]
    
    # Save the labelled file
    save_file_name = 'labelled_fixations_diff_version.csv'
    fixations.to_csv(f"{data_folder}/{save_file_name}", index=False) 
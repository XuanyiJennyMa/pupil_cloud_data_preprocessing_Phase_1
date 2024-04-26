"""
This script is used for label the raw pupil diameter data with event information (timestamps from PupilCloud) and AOIs (timeestamps from previous steps). 
Please note, the "Timeseries data" folder should be saved within the same directory with this script.
Please make sure that you have ran the script "Change_foldername_timeseries.py". 

"""

# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import glob

# Read the information of wearers
section_info_df = pd.read_csv("Timeseries Data/sections.csv")

# Filter out the information of scanning recordings
# Change the keyword "scanning" if you label your scanning videos differently
wearer_name = [participant for index, participant in enumerate(section_info_df['wearer name']) if 'scanning' not in participant]

# Label each wearer' raw pupil diameter data with event information (timestamps from PupilCloud)
for wearer in wearer_name:
    # Read the pupil diameter data
    data_folder = glob.glob('./Timeseries Data/'+ "*" + wearer)
    pupil_df = pd.read_csv(f"{data_folder[0]}/3d_eye_states.csv") 

    # Read the event information
    pupil_event = pd.read_csv(f"{data_folder[0]}/events.csv")
    # Filter out the beginning and the ending of the recording as there are useless data before the partipant starting reading the first manuscript and after the participant finishing reading the last manuscript
    valid_event = [event for index, event in enumerate(pupil_event['name']) if 'recording' not in event]
    
    # Make a list of the numbers of the manuscripts that the participant has read
    manu_number = []
    for event in valid_event:
        number = event.split(".")[0].split("_")[-1]
        manu_number.append(number)
    single_manu = np.unique(manu_number)

    # Label participant's raw pupil diameter data with event information
    for manu in single_manu:
        # Read the timestamps of the starting and ending of the manuscript
        start_event_name = "Manu_" + manu + ".start"
        end_event_name = "Manu_" + manu + ".end"
        start_index = pupil_event['name'].to_list().index(start_event_name)
        end_index = pupil_event['name'].to_list().index(end_event_name)
        start_time = pupil_event['timestamp [ns]'][start_index]
        end_time = pupil_event['timestamp [ns]'][end_index]

        # Assign the manuscript number to thoes pupil diameter data that were collected while reading this manuscript
        subset = pupil_df[(pupil_df['timestamp [ns]'] >= start_time) & (pupil_df['timestamp [ns]'] <= end_time)]
        index_list = subset.index
        pupil_df.loc[index_list, 'Manuscript'] = manu
    
    # Save the labelled file
    pupil_df.to_csv(f"{data_folder[0]}/labelled_pupil.csv", index=False)

# Assign the AOIs information to the pupil diameter data according to the timestamps from fixation data
# And save each participant's fixation data for checking the accuracy of the labelling process
def label_pupil_with_aoi(pic, multi_version_check, overlapped_aois, version):
    if multi_version_check == True:
        aoi_version = version
        aoi_column = 'AOI_' + str(version)
        if overlapped_aois == True:
            csv_file = 'final_labelled_fixations_diff_version.csv'
        else:
            csv_file = 'labelled_fixations_diff_version.csv'
    else:
        aoi_column = 'AOI' 
        csv_file = 'labelled_fixations.csv'
   
    # Import the fixation data
    # If you have changed the folder name to be the same as the picture name
    # data_folder = "./" + pic
    # If you keep the folder name as how it was downloaded from Pupil Cloud, comment the line above and uncomment the two lines below:
    foldername = glob.glob('*' + pic + '_csv')
    data_folder = "./" + foldername[0]
    aoi_labelled_fixations = pd.read_csv(f"{data_folder}/{csv_file}")

    fixation_participant_dict = {}
    for wearer in wearer_name:
        # Read the pupil diameter data of each participant from Timeseries Data folder
        pupil_data_folder = glob.glob('./Timeseries Data/'+ "*" + wearer)
        pupil_diameter = pd.read_csv(f"{pupil_data_folder[0]}/labelled_pupil.csv")

        start_time_list = []
        end_time_list = []
        selected_participant = aoi_labelled_fixations[aoi_labelled_fixations['Participant'] == int(wearer)]
        valid_fixations = [fixation for index, fixation in enumerate(selected_participant[aoi_column]) if not pd.isna(fixation)]
        fixation_list = np.unique(valid_fixations) # Even for the same reference picture, some participants may not have looked at all area of interests. 
        
        for fix in fixation_list:
            selected_fixation = selected_participant[selected_participant[aoi_column] == fix]
            list_of_index = selected_fixation.index.to_list()

            # There may be multiple lists of continuous fixations in one AOI
            # Read all lists of continuous fixations in one AOI
            list_fixation = []
            list_of_list_fixation = []
            for index_no in list_of_index:
                if list_of_index.index(index_no) != len(list_of_index)-1:
                    if list_of_index[list_of_index.index(index_no)+1] - index_no == 1:
                        list_fixation.append(index_no)
                    else:
                        list_fixation.append(index_no)
                        list_of_list_fixation.append(list_fixation)
                        list_fixation=[]
                else:
                    list_fixation.append(index_no)     
                    
            # Save the lists into another list
            list_of_list_fixation.append(list_fixation)
            # Save the list into the dictionary with the key name indicating the participant and AOI information
            key_name = 'participant_' + wearer + '_fixation_' + str(int(fix))
            fixation_participant_dict[key_name] = list_of_list_fixation
            
            # Find the start time and the end time of each list of continuous fixations
            # Save the timestamps
            start_time = []
            end_time=[]
            for i in range(0, len(list_of_list_fixation)):
                start_time.append(aoi_labelled_fixations['start timestamp [ns]'][list_of_list_fixation[i][0]])
                end_time.append(aoi_labelled_fixations['end timestamp [ns]'][list_of_list_fixation[i][-1]])
            start_time_list.append(start_time)  
            end_time_list.append(end_time)  
            
        # Assign the pupil diameter data that are between the start and end timestamps of the continuous fixations within the AOI to the AOI number   
        for i, fix in enumerate(fixation_list):
            for j in range(0, len(start_time_list[i])):
                subset = pupil_diameter[(pupil_diameter['timestamp [ns]'] >= start_time_list[i][j]) & (pupil_diameter['timestamp [ns]'] <= end_time_list[i][j])]
                #fix -- AOI, j -- fixation group
                index_list = subset.index
                pupil_diameter.loc[index_list, 'aoi_column'] = str(int(fix))+ '_' + str(j)

        # Save the labelled pupil diameter data file
        pupil_diameter.to_csv(f"{pupil_data_folder[0]}/labelled_pupil.csv", index=False)
                
    # Save the dictionary containing each participant's fixation data into .csv file
    csv_filename = pic + '_' + aoi_column + '_fixation_dict.csv'
    with open(csv_filename, 'w') as f:  
        w = csv.DictWriter(f, fixation_participant_dict.keys())
        w.writeheader()
        w.writerow(fixation_participant_dict)            
    return fixation_participant_dict

# Take manuscript 1 as an example:
label_pupil_with_aoi('Manuscript_1', false, false, 0)
# There is only one version of AOIs for manuscript one, so both multi_version_check and overlapped_aois are set to false.
# In this case, version can be set to any number as it won't affect the result. And I set it to 0. 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import glob

section_info_df = pd.read_csv("Timeseries Data/sections.csv")
wearer_name = [participant for index, participant in enumerate(section_info_df['wearer name']) if 'scanning' not in participant]

for wearer in wearer_name:
    data_folder = glob.glob('./Timeseries Data/'+ "*" + wearer)
    pupil_df = pd.read_csv(f"{data_folder[0]}/3d_eye_states.csv")
    pupil_df['aoi_column'] = None
    pupil_df.to_csv(f"{data_folder[0]}/labelled_pupil.csv", index=False)

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
        pupil_data_folder = glob.glob('./Timeseries Data/'+ "*" + wearer)
        pupil_diameter = pd.read_csv(f"{pupil_data_folder[0]}/labelled_pupil.csv")

        start_time_list = []
        end_time_list = []
        selected_participant = aoi_labelled_fixations[aoi_labelled_fixations['Participant'] == int(wearer)]
        valid_fixations = [fixation for index, fixation in enumerate(selected_participant[aoi_column]) if not pd.isna(fixation)]
        fixation_list = np.unique(valid_fixations)
        
        for fix in fixation_list:
            selected_fixation = selected_participant[selected_participant[aoi_column] == fix]
            list_of_index = selected_fixation.index.to_list()
            
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
                    
                    
            list_of_list_fixation.append(list_fixation)
            key_name = 'participant_' + wearer + '_fixation_' + str(int(fix))
            fixation_participant_dict[key_name] = list_of_list_fixation
            
            start_time = []
            end_time=[]
            for i in range(0, len(list_of_list_fixation)):
                start_time.append(aoi_labelled_fixations['start timestamp [ns]'][list_of_list_fixation[i][0]])
                end_time.append(aoi_labelled_fixations['end timestamp [ns]'][list_of_list_fixation[i][-1]])
            start_time_list.append(start_time)  
            end_time_list.append(end_time)  
            

        for i, fix in enumerate(fixation_list):
            for j in range(0, len(start_time_list[i])):
                subset = pupil_diameter[(pupil_diameter['timestamp [ns]'] >= start_time_list[i][j]) & (pupil_diameter['timestamp [ns]'] <= end_time_list[i][j])]
                #fix -- AOI, j -- fixation group
                index_list = subset.index
                pupil_diameter.loc[index_list, 'aoi_column'] = str(int(fix))+ '_' + str(j)
        
        pupil_diameter.to_csv(f"{pupil_data_folder[0]}/labelled_pupil.csv", index=False)
                
    
    csv_filename = pic + '_' + aoi_column + '_fixation_dict.csv'
    with open(csv_filename, 'w') as f:  
        w = csv.DictWriter(f, fixation_participant_dict.keys())
        w.writeheader()
        w.writerow(fixation_participant_dict)            
    return fixation_participant_dict



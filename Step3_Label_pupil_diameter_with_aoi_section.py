import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

def extract_fixation_info(pic, multi_version_check, overlapped_aois, version):
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
   
    filepath = "./" + pic
    aoi_labelled_fixations = pd.read_csv(f"{filepath}/{csv_file}")
    
    number_of_fixations = np.unique(aoi_labelled_fixations[aoi_column])
    number_of_participants = np.unique(aoi_labelled_fixations['Participant'])
    
    fixation_participant_dict = {}
    for participant in range(max(number_of_participants)):
        for idx in range(len(number_of_fixations)-1):
            selected_participant = aoi_labelled_fixations[aoi_labelled_fixations['Participant'] == (participant + 1)]
            selected_fixation = selected_participant[selected_participant[aoi_column] == idx]
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
            key_name = 'participant_' + str(participant +1) + '_fixation_' + str(idx)
            fixation_participant_dict[key_name] = list_of_list_fixation
    
    csv_filename = pic + '_' + aoi_column + '_fixation_dict.csv'
    with open(csv_filename, 'w') as f:  
        w = csv.DictWriter(f, fixation_participant_dict.keys())
        w.writeheader()
        w.writerow(fixation_participant_dict)            
    return fixation_participant_dict


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
   
    labelled_fixations_filepath = "./" + pic
    aoi_labelled_fixations = pd.read_csv(f"{labelled_fixations_filepath}/{csv_file}")
    
    number_of_fixations = np.unique(aoi_labelled_fixations[aoi_column])
    number_of_participants = np.unique(aoi_labelled_fixations['Participant'])
    
    
    fixation_participant_dict = {}
    for participant in range(max(number_of_participants)):
        pupil_filepath = "./Timeseries_Data/" + pic + "_" + str(participant+1).zfill(3)
        pupil_diameter = pd.read_csv(f"{pupil_filepath}/3d_eye_states.csv")

        start_time_list = []
        end_time_list = []
        for idx in range(len(number_of_fixations)-1):
            selected_participant = aoi_labelled_fixations[aoi_labelled_fixations['Participant'] == (participant + 1)]
            selected_fixation = selected_participant[selected_participant[aoi_column] == idx]
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
            key_name = 'participant_' + str(participant +1) + '_fixation_' + str(idx)
            fixation_participant_dict[key_name] = list_of_list_fixation
            
            start_time = []
            end_time=[]
            for i in range(0, len(list_of_list_fixation)):
                start_time.append(aoi_labelled_fixations['start timestamp [ns]'][list_of_list_fixation[i][0]])
                end_time.append(aoi_labelled_fixations['end timestamp [ns]'][list_of_list_fixation[i][-1]])
            start_time_list.append(start_time)  
            end_time_list.append(end_time)  
            
        pupil_diameter[aoi_column] = None
        

        for i in range(0, len(start_time_list)):
            for j in range(0, len(start_time_list[i])):
                print(i, j)
                subset = pupil_diameter[(pupil_diameter['timestamp [ns]'] >= start_time_list[i][j]) & (pupil_diameter['timestamp [ns]'] <= end_time_list[i][j])]
                #i -- AOI, j -- fixation group
                index_list = subset.index
                pupil_diameter.loc[index_list, aoi_column] = str(i)+str(j)
        
        pupil_filename = pic + '_labelled_pupil_' + str(participant+1).zfill(3) + '.csv'
        pupil_diameter.to_csv(pupil_filename, index=False)
                
    
    csv_filename = pic + '_' + aoi_column + '_fixation_dict.csv'
    with open(csv_filename, 'w') as f:  
        w = csv.DictWriter(f, fixation_participant_dict.keys())
        w.writeheader()
        w.writerow(fixation_participant_dict)            
    return fixation_participant_dict

pupil_filepath = "./Timeseries_Data/" + 'Manuscript_1' + "_" + str(1).zfill(3)
pupil_diameter = pd.read_csv(f"{pupil_filepath}/3d_eye_states.csv")
print(pupil_diameter)
pupil_diameter['test'] = None
pupil_filename = 'Manuscript_1' + '_labelled_pupil_test_' + str(1).zfill(3) + '.csv'
        
pupil_diameter.to_csv(pupil_filename, index=False)
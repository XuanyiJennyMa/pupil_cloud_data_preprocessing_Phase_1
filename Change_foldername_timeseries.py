"""
This script is used for changing the names of the folders that contain raw pupil diameter data for each participant. 
Please note, the "Timeseries data" folder that contain all these folders should be saved within the same directory with this script.

"""

# Import libraries
import glob
import os

# label the pupil data with manuscript information
section_info_df = pd.read_csv("Timeseries Data/sections.csv")
wearer_name = [participant for index, participant in enumerate(section_info_df['wearer name']) if 'scanning' not in participant]
wearer_index = [index for index, participant in enumerate(section_info_df['wearer name']) if 'scanning' not in participant]
print(wearer_name,wearer_index)

for idx, wearer_idx in enumerate(wearer_index):
    recording_id = section_info_df['recording id'][wearer_idx]
    recording_id_abbr = recording_id.split("-")[0] 
    recording_id_abbr = str(recording_id_abbr)
    current_folder_name = glob.glob('./Timeseries Data/'+ "*" + recording_id_abbr)
    new_folder_name = './Timeseries Data/'+ recording_id_abbr + '_' + wearer_name[idx]
    print(new_folder_name)
    os.rename(current_folder_name[0], new_folder_name)


""" 
This script is used for 1) the extraction of nested area(s) of interests; 
                        2) saving the defined AOIs of each reference picture in an independant .csv file.
It is a modified version of some codes in Pupil Labs' gallery_demo_analysis:
       https://github.com/pupil-labs/gallery_demo_analysis/blob/main/1_Defining%20Nested%20AOIs.ipynb
Please note, "Reference_pic" folder should be saved within the same directory with this script.

"""

# Import libraries
import cv2
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd
import os

# Set the directory of the folder containing reference pictures.
path_to_reference_image_single_aoi = ("./Reference_pic/Single_aoi") 
path_to_reference_image_complex_aoi = ("./Reference_pic/Complex_aoi")

# Create a new directory to save AOI information for each reference picture
save_aoi_path = "./AOI_information"
os.mkdir(save_aoi_path)

# This function is for reading the reference picture name. 
# Original code can be found in Pupil Labs' script as indicated above.
# Change the file extension within the quotation mark if your picures are in different format.
extract_name = lambda name: name.split(".png")[0] 

# This function is to extract the information of each referencec picture and then save it in a dictionary with the reference picure name as the key. 
def extract_ref_pics(path):
    all_ref_pic = os.listdir(path) # Get all the referenece files in the folder
    ref_pic_dict = {} # create an empty dictionary
    
    # Read and extract the information of each referencec picture
    for pic in all_ref_pic: 
        # Original code can be found in Pupil Labs' script as indicated above.
        reference_image = cv2.imread(f"{path}/{pic}") 
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB) 
        
        # Save the information of each referencec picture in a dictionary with the reference picure name as the key
        ref_pic_dict[extract_name(pic)] = reference_image 
    return ref_pic_dict

# Run the above function with the reference pictures in the set-up folders
reference_picture_single_aoi = extract_ref_pics(path_to_reference_image_single_aoi) 
reference_picture_complex_aoi = extract_ref_pics(path_to_reference_image_complex_aoi)

# This function is for extracting the AOIs once for each picture in the "Single_aoi" folder
def extract_aoi_info_diff_pic(ref_pic_list):
    for pic in ref_pic_list:
        scaling_factor = 0.3  # Change it according to the size of your reference picture(s)
        picture = reference_picture_single_aoi.get(pic) # Read the information from dictionary

        # Original code can be found in Pupil Labs' script as indicated above.
        # Selecting AOIs
        scaled_image = picture.copy() 
        scaled_image = cv2.resize(scaled_image, dsize=None, fx=scaling_factor, fy=scaling_factor) 
        scaled_aois = cv2.selectROIs("AOI Annotation", scaled_image) 
        cv2.destroyAllWindows() 
        aois = scaled_aois / scaling_factor 
        
        # Save the information of the AOIs of each picture in an individual .csv file
        aoi_df = pd.DataFrame(aois) 
        filename = pic+"_AOIs.csv"
        aoi_df.to_csv(f"{save_aoi_path}/{filename}", index=False)

# Call the function to process all the reference pictures in "Single_aoi" folder.
extract_aoi_info_diff_pic(reference_picture_single_aoi)
# Make your own list if you only want to run it for some of the reference picutres in "Single_aoi" folder.

# This function is for extracting the AOIs for each picture in the "Complex_aoi" folder.
# Run this function with only one set of AOIs and one reference picture at once.
def extract_aoi_info_same_pic(ref_pic, aoi_versions):
    for version in range(aoi_versions):
        scaling_factor = 0.3 # Change it according to the size of your reference picture(s)
        picture = reference_picture_complex_aoi.get(ref_pic) # Read the information from dictionary

        # Original code can be found in Pupil Labs' script as indicated above.
        # Selecting AOIs
        scaled_image = picture.copy() 
        scaled_image = cv2.resize(scaled_image, dsize=None, fx=scaling_factor, fy=scaling_factor) 
        scaled_aois = cv2.selectROIs("AOI Annotation", scaled_image) 
        cv2.destroyAllWindows() 
        aois = scaled_aois / scaling_factor
        
        # Save the information of this set of AOIs of the picture in an individual .csv file
        aoi_df = pd.DataFrame(aois)
        filename = ref_pic +'_'+str(version)+"_AOIs.csv"
        aoi_df.to_csv(f"{save_aoi_path}/{filename}", index=False)

# For example:
# If you want to run the function for reference picture "Manuscript_1.png" 4 times because there are 4 sets of AOIs that you are interested in,
# You can run the function with the proper arguments as shown below:
extract_aoi_info_same_pic('Manuscript_1', 4)
# Please be aware, the input of 'ref_pic' should always be a string while the input of 'aoi_version' should always be a positive integer. 

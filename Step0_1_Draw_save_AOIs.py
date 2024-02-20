# After the successful extraction (Knock!Knock!Knock!) of the information of AOIs of each reference pictures, it is time to visualise them on the reference pictures and save the visualisation. 
# It is a modified version of some codes in Pupil Labs' gallery_demo_analysis:
#       https://github.com/pupil-labs/gallery_demo_analysis/blob/main/1_Defining%20Nested%20AOIs.ipynb
# Please note, "Reference_pic" folder should be saved within the same directory with this script.


# Import libraries
import cv2
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd
import math 

# This is to set the size of the labels of AOIs in the pictures.
# Original code can be found in Pupil Labs' script as indicated above.
plt.rcParams.update({"font.size": 18})

# This function is for overlaying the AOIs on the reference pictures.
# Original code can be found in Pupil Labs' script as indicated above.
def plot_aoi_patches(aois, ax, aoi_colors, n_colorsteps):
    for idx, aoi in enumerate(aois):
        ax.add_patch(
            patches.Rectangle(
                aoi, *aoi[2:], alpha=0.2, color=aoi_colors(idx / n_colorsteps)
            )
        )
        ax.text(aoi[0] + 20, aoi[1] + 120, f"{idx}", color="black")
# The function above will be called in the functions below.


# This function is for plotting the AOIs on each manuscript that has only one set of AOIs (from "Single_aoi" folder) with the preprocessed AOI information from the previous script.
def paint_save_aoi_diff_picture(list_of_pics):
    for pic in list_of_pics:  
        aoi_file = pic+'_AOIs.csv' # Full filename of AOI information
        path_to_reference_image = ("./Reference_pic/Single_aoi") # Path to the reference picture
        reference_image_file = pic+'.png' # Full filename of the reference picture

        # Original code can be found in Pupil Labs' script as indicated above.
        reference_image = cv2.imread(f"{path_to_reference_image}/{reference_image_file}") 
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)

        # Read the file of AOIs information
        aois = pd.read_csv(aoi_file, sep=',')
        aois = aois.to_numpy() # Convert Pandas dataframe to Numpy array

        # Original code can be found in Pupil Labs' script as indicated above.
        # Define a colormap
        aoi_colors = matplotlib.cm.get_cmap("plasma")
        n_colorsteps = len(aois) - 1

        # Some referencec pictures are in portrait orientation while the others are in landscape orientation. 
        # Set the figure size of reference picture accroding to the orientation of the reference picture.
        height, width, channel = reference_image.shape
        ratio = width/height
        if ratio <= 1:
            marked_ref_fig = plt.figure(figsize=(math.trunc(ratio*20), 20))
        else:
            marked_ref_fig = plt.figure(figsize=(20, math.trunc(20/ratio)))
        plt.imshow(np.asarray(reference_image))

        # Original code can be found in Pupil Labs' script as indicated above.
        # Plot the AOIs on the reference picture
        plot_aoi_patches(aois, plt.gca(),aoi_colors, n_colorsteps)
        plt.gca().set_axis_off()
        
        # Save the referemce picture with AOIs marked 
        save_file_name = pic + '_aois.png'
        marked_ref_fig.savefig(save_file_name)

def paint_save_aoi_same_picture(pic, versions):
    for version in range(versions):  
        aoi_file = pic+'_'+str(version)+'_AOIs.csv'
        path_to_reference_image = ("./Reference_pic")
        reference_image_file = pic+'.jpeg'
        reference_image = cv2.imread(f"{path_to_reference_image}/{reference_image_file}")
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        
        aois = pd.read_csv(aoi_file, sep=',')
        aois = aois.to_numpy()
        aoi_colors = matplotlib.cm.get_cmap("plasma")
        n_colorsteps = len(aois) - 1
        
        h_1, w_1, c_1 = reference_image.shape
        ratio = w_1/h_1
        if ratio <= 1:
            marked_ref_fig = plt.figure(figsize=(math.trunc(ratio*20), 20))
        else:
            marked_ref_fig = plt.figure(figsize=(20, math.trunc(20/ratio)))

        plt.imshow(np.asarray(reference_image))
        
        plot_aoi_patches(aois, plt.gca(),aoi_colors, n_colorsteps)
        plt.gca().set_axis_off()
        save_file_name = pic + '_' + str(version) + '_aois.png'

        marked_ref_fig.savefig(save_file_name)

import cv2
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

path_to_reference_image = ("./Reference_pic")

extract_name = lambda name: name.split(".jpeg")[0]
def extract_ref_pics(path):
    all_ref_pic = os.listdir(path)
    ref_pic_dict = {}
    for pic in all_ref_pic:
        reference_image = cv2.imread(f"{path}/{pic}")
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        ref_pic_dict[extract_name(pic)] = reference_image
        #globals()[extract_name(pic)] = reference_image
    return ref_pic_dict

reference_picture = extract_ref_pics(path_to_reference_image)     

# this function is for extracting the AOIs once for each picture
# for different versions of AOIs from the same picture, see the function below

def extract_aoi_info_diff_pic(ref_pic_list):
    for pic in ref_pic_list:
        scaling_factor = 0.25
        picture = reference_picture.get(pic)
        scaled_image = picture.copy()
        scaled_image = cv2.resize(scaled_image, dsize=None, fx=scaling_factor, fy=scaling_factor)
        scaled_aois = cv2.selectROIs("AOI Annotation", scaled_image)
        cv2.destroyAllWindows()
        aois = scaled_aois / scaling_factor
        aoi_df = pd.DataFrame(aois)
        filename = pic+"_AOIs.csv"
        aoi_df.to_csv(filename, index=False)

def extract_aoi_info_same_pic(ref_pic, aoi_versions):
    for version in range(aoi_versions):
        reference_image = cv2.imread(f"{path_to_reference_image}/{ref_pic}")
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        scaling_factor = 0.5
        scaled_image = reference_image.copy()
        scaled_image = cv2.resize(scaled_image, dsize=None, fx=scaling_factor, fy=scaling_factor)
        scaled_aois = cv2.selectROIs("AOI Annotation", scaled_image)
        cv2.destroyAllWindows()
        aois = scaled_aois / scaling_factor
        aoi_df = pd.DataFrame(aois)
        filename = ref_pic.split(".jpeg")[0]+'_'+str(version)+"_AOIs.csv"
        aoi_df.to_csv(filename, index=False)


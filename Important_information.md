# Aims and the built-up of scripts

## A little background information and the set-up of working space

In our project, we are very interested in the fixations in different parts of a manuscript and the saccades between each parts. We have various kinds of manuscripts: 
+  pictures
+  pictures with description
+  texts with illustration
+  texts with paratexts

AOIs of each manuscript need to be defined. However, AOIs are easier to capture in some manuscripts than the others and sometimes there are multiple sets of AOIs that we are interested in for one single manuscript. 

In this case, manuscripts (also as reference pictures for enrichment in [Pupil Cloud][1]) are saved in different folders with folder named "Reference_pic": 

![Different folders for reference pictures](Screenshot%202024-02-15%20153113.png)

[1]: https://pupil-labs.com/products/cloud

Folder "Complex_aoi" contains the manuscirpts that have multiple sets of AOIs or/and overlapped selection of AOIs (which will be explained with more details in the .py file).
Folder "Single_aoi" contains the manuscripts that have only one set of AOIs and they are not overlapped (I wish all reference pictures went to this folder but not the other......). 

Before you run the scripts, please make sure that the scripts are downloaded and saved in the same folder with the other folders including the raw timeseries data, the data from enrichment and reference pictures (as shown below):

![Original folder names](Screenshot%202024-02-14%20153212.png)












After downloading and extracting the data from the successful enrichment process of each reference picture, the original folder names are like this:



I personally prefer a shorter folder name which still reminds me what this folder is about, so I changed the folder names into this:

![New folder names](Screenshot%202024-02-14%20153329.png)

However, this process is completely optional. You don't have to change your folder name as there are also codes prepared to the original long folder names. 


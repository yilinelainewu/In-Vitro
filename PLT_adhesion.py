#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 16:53:17 2025

@author: elaine
Analyze sheep PLT adhesion data for collagen and vwf output files

"""

import os
import pandas as pd


#enter details of experiment
date = input('Enter experiment date [YYYY+MM+DD]:')
sheep_num = input('Enter sheep number [###]:')
mark = input('Enter sheep schedule [BL/PI/1H/POD+DD]:')

#input and output files
data_folder = '/Volumes/EWu LaCie/Sheep/Sheep 308/POD 14/25-08-12/Adhesion'
output_file = f"/Users/elaine/Desktop/PLT_adhesion_summary_sheep{sheep_num}_{mark}_{date}.csv"

#date = 20250812
#mark = "POD14"

###################################### COLLAGEN ###########################################
print("COLLAGEN#####################################################")

#FRAME 300 AREA
collagen_data_file = None
for file in os.listdir(data_folder):
    if file.endswith(f"{date}_data.csv") and "Collagen" in file:
        collagen_data_file = os.path.join(data_folder, file)
        print("👀Reading collagen f300 file:", collagen_data_file)
        break

if collagen_data_file is None:
    print("No collagen f300 file found for this date")
else:
    # Read while skipping metadata until the real table starts
    df = pd.read_csv(collagen_data_file, skiprows=10)  # adjust number if needed

    if df.shape[1] > 1:  # ensure at least 2 columns exist
        collagen_f300_area = df.iloc[-1, 1]
        print("Frame 300 area is:", collagen_f300_area)
    else:
        print("Only one column detected. Check skiprows value or file format.")
        
#10 IMAGE AVG AREA
collagen_image_file = None
for file in os.listdir(data_folder):
    if file.endswith("output_data.csv") and "Collagen" in file:
        collagen_image_file = os.path.join(data_folder, file)
        print("\n👀Reading collagen image file:", collagen_image_file)
        break
    
if collagen_image_file is None:
    print("No collagen image file found for this date")
else:
    df = pd.read_csv(collagen_image_file, skiprows=1)
    
    if df.shape[1] > 1:
        collagen_image_area_mean = df.iloc[-2,1]
        collagen_image_area_std = df.iloc[-1,1]
        print("Image area mean is:", collagen_image_area_mean)
        print("Image area std is:", collagen_image_area_std)
    else:
        print("Only one column detected. Check skiprows value or file format.")
        
#FRAME 300 SPOTS
collagen_spot_file = os.path.join(data_folder, "Summary.csv")
print("\n👀Reading collagen spot file:", collagen_spot_file)
df = pd.read_csv(collagen_spot_file)

collagen_spot_count = df["Count"].iloc[0]
print("Spot count:", collagen_spot_count)
collagen_spot_size_mean = df["Average Size"].iloc[0]
print("Mean spot size is:", collagen_spot_size_mean)
collagen_percent_area = df["%Area"].iloc[0]
print("Mean %Area is:", collagen_percent_area)
collagen_intensity_mean = df["Mean"].iloc[0]
print("Mean grayscale intensity is:", collagen_intensity_mean)



###################################### VWF ################################################
print("\nVWF#########################################################")
#FRAME 300 AREA
vwf_data_file = None
for file in os.listdir(data_folder):
    if file.endswith(f"{date}_data.csv") and "VWF" in file:
        vwf_data_file = os.path.join(data_folder, file)
        print("👀Reading VWF f300 file:", vwf_data_file)
        break

if vwf_data_file is None:
    print("No VWF f300 file found for this date")
else:
    # Read while skipping metadata until the real table starts
    df = pd.read_csv(vwf_data_file, skiprows=10)  # adjust number if needed

    if df.shape[1] > 1:  # ensure at least 2 columns exist
        vwf_f300_area = df.iloc[-1, 1]
        print("Frame 300 area is:", vwf_f300_area)
    else:
        print("Only one column detected. Check skiprows value or file format.")
        
#10 IMAGE AVG AREA
vwf_image_file = None
for file in os.listdir(data_folder):
    if file.endswith("output_data.csv") and "VWF" in file:
        vwf_image_file = os.path.join(data_folder, file)
        print("\n👀Reading VWF image file:", vwf_image_file)
        break
    
if vwf_image_file is None:
    print("No VWF image file found for this date")
else:
    df = pd.read_csv(vwf_image_file, skiprows=1)
    
    if df.shape[1] > 1:
        vwf_image_area_mean = df.iloc[-2,1]
        vwf_image_area_std = df.iloc[-1,1]
        print("Image area mean is:", vwf_image_area_mean)
        print("Image area std is:", vwf_image_area_std)
    else:
        print("Only one column detected. Check skiprows value or file format.")

#50 FRAME VIDEO ANALYZED
vwf_50f_file = None
for file in os.listdir(data_folder):
    if file.endswith("analyzed.csv"):
        vwf_50f_file = os.path.join(data_folder, file)
        print("\n👀Reading VWF 50f analyzed file:", vwf_50f_file)
        break
    
if vwf_data_file is None:
    print("No VWF 50f file found for this date")
else:
    df = pd.read_csv(vwf_50f_file, skiprows=9)
    
    #new column for speed 60X
    df["60X Mean Speed"] = df.iloc[:,7] * 0.171
    
    vwf_total_count = len(df)
    print("Total spot count is:", vwf_total_count)
    
    G1_count = (df.iloc[:, 12] == 1).sum()
    print("G1 count is:", G1_count)
    G2_count = (df.iloc[:, 12] == 2).sum()
    print("G2 count is:", G2_count)
    G3_count = (df.iloc[:, 12] == 3).sum()
    print("G3 count is:", G3_count)
    G4_count = (df.iloc[:, 12] == 3).sum()
    print("G4 count is:", G4_count)
    G5_count = (df.iloc[:, 12] == 3).sum()
    print("G5 count is:", G5_count)
    G6_count = (df.iloc[:, 12] == 6).sum()
    print("G6 count is:", G6_count)
    
    percent_rolling = (G2_count + G3_count + G4_count + G5_count)/vwf_total_count *100
    print("%Rolling spots is:", "{:.3f}".format(percent_rolling))
    
    
    G_filter = df.iloc[:, 12].isin([2,3,4,5])
    G2_G5_speed = df.loc[G_filter, "60X Mean Speed"].mean()
    print("G2-G5 Mean speed is:", "{:.3f}".format(G2_G5_speed))
    
    max_speed = df.loc[G_filter, "60X Mean Speed"].max()
    print("Max speed is:", "{:.3f}".format(max_speed))



############################################################################## OUTPUT FILE
# Collagen block
collagen_df = pd.DataFrame({
    "Metric": [
        "F300 Area",
        "Image Area Mean",
        "Image Area STD",
        "Spot Count",
        "Mean Spot Size",
        "Mean %Area",
        "Mean Intensity"
    ],
    "Value": [
        collagen_f300_area,
        collagen_image_area_mean,
        collagen_image_area_std,
        collagen_spot_count,
        collagen_spot_size_mean,
        collagen_percent_area,
        collagen_intensity_mean
    ]
})

# VWF block
vwf_df = pd.DataFrame({
    "Metric": [
        "F300 Area",
        "Image Area Mean",
        "Image Area STD",
        "Total Spot Count",
        "G1 Count",
        "G2 Count",
        "G3 Count",
        "G4 Count",
        "G5 Count",
        "G6 Count",
        "%Rolling",
        "G2-G5 Speed (um/s)",
        "Max Speed (um/s)"
    ],
    "Value": [
        vwf_f300_area,
        vwf_image_area_mean,
        vwf_image_area_std,
        vwf_total_count,
        G1_count,
        G2_count,
        G3_count,
        G4_count,
        G5_count,
        G6_count,
        percent_rolling,
        G2_G5_speed,
        max_speed
    ]
})

# Add headers as separator rows
collagen_header = pd.DataFrame([["Collagen", ""]], columns=["Metric", "Value"])
vwf_header = pd.DataFrame([["VWF", ""]], columns=["Metric", "Value"])
blank_row = pd.DataFrame([["", ""]], columns=["Metric", "Value"])

# Stack them in one table
summary_df = pd.concat([collagen_header, collagen_df, vwf_header, vwf_df], ignore_index=True)

# Save to Excel

summary_df.to_csv(output_file, index=False, header=False)

print("\n✅ CSV file saved:", output_file)
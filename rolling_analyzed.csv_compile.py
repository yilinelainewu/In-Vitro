#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 10:46:12 2025

@author: elaine
created to compile all analyzed csv into one file
"""

import os
import pandas as pd

csv_folder = '/Users/elaine/Desktop/2025-06-03_WBC_Rolling_Analyzed'
output_path = '/Users/elaine/Desktop/combined.csv'

# Sorted CSV filenames
csv_files = sorted([f for f in os.listdir(csv_folder) if f.endswith('.csv')])

# Get headers from the first file (assumes first 2 rows are header + units)
header_df = pd.read_csv(os.path.join(csv_folder, csv_files[0]), nrows=2)
column_names = ['Source'] + header_df.columns.tolist()

# Collect all data
all_data = []

for filename in csv_files:
    filepath = os.path.join(csv_folder, filename)
    
    # Skip header and unit rows
    df = pd.read_csv(filepath, skiprows=2, header=None)
    
    # Insert filename as first column
    df.insert(0, 'Source', filename)
    
    all_data.append(df)

# Concatenate all data
combined_df = pd.concat(all_data, ignore_index=True)

# Set final column names
combined_df.columns = column_names

# Save to file
combined_df.to_csv(output_path, index=False)

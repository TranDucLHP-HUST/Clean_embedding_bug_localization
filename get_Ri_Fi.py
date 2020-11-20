import pandas as pd
import numpy as np
import csv

# define link file
BUG_REPORT = 'data/AspectJ_csv_not_trace.csv'
CONNECT = 'data/data_connect.csv'
OUTPUT = 'data/R_F.csv'


input = pd.read_csv(BUG_REPORT)
bug_time = input['report_timestamp'].values
source_time = input['commit_timestamp'].values
sources = input['files'].values

input = pd.read_csv(CONNECT)
sources_connect_0 = input['source_label_0'].values
sources_connect_1 = input['source_label_1'].values

with open(OUTPUT, 'w') as csv_file:
    fieldnames = ['id', 'bug_id', 'commit', 'commit_timestamp', 'files', 'Unnamed: 10']  # Định dạng cột
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()





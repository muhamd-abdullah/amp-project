import os
import sys
import json
from statsmodels.distributions.empirical_distribution import ECDF
import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.interpolate import interp1d as spline
import csaps
import pandas as pd 


def get_stat_list(stat_name, file_name):
    csv_file = open(file_name)
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    stat_list = []

    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        line_count += 1
        if not row[stat_name] or float(row[stat_name]) <=0 :
            continue
        stat_list.append(row[stat_name])

    stat_list_numeric = [float(i) for i in stat_list]
    stat_list_numeric.sort()
    
    summary_file = open(stat_name[3:]+".txt",'a')
    print(file_name[6:-4]," - " ,stat_name[3:])
    df = pd.DataFrame(stat_list_numeric) 
    summary_file.write(file_name+" - "+stat_name+str(df.describe())[19:]+"\n\n")

    return stat_list_numeric, str(df.describe())[19:]


def get_cdf(stat_list, stat_name=""):
    ecdf = ECDF(stat_list)    
    return stat_name, ecdf.x, ecdf.y


def plot(stat_name, ecdf_x, ecdf_y, axes):
    # CUSHION
    cushion = 500000000
    ecdf_x = list(ecdf_x)
    ecdf_y = list(ecdf_y)
    ecdf_x.append(int(max(ecdf_x))+cushion)
    ecdf_y.append(1)

    axes.plot(ecdf_x, ecdf_y)
    
    if stat_name not in ["FV Bytes In (Doc) Median", "FV Requests (Doc) Median","FV Speed Index Median"]:
        plt.setp(axes, xlabel= stat_name[3:-7]+" (ms)")
    else:
        plt.setp(axes, xlabel= stat_name[3:-7])
    
    plt.setp(axes, ylabel='CDF')



def get_summary(summary):
    summary = summary.split("\n")
    mean = int(float(summary[-7].split(" ")[-1]))
    std = int(float(summary[-6].split(" ")[-1]))
    min_val = int(float(summary[-5].split(" ")[-1]))
    ci_25 = int(float(summary[-4].split(" ")[-1]))
    ci_50 = int(float(summary[-3].split(" ")[-1]))
    ci_75 = int(float(summary[-2].split(" ")[-1]))
    max_val = int(float(summary[-1].split(" ")[-1]))
    return [mean, std, min_val, ci_25, ci_50, ci_75, max_val]

improvements= []

def main(test_number, stat_name, axes):
    open(stat_name[3:]+".txt",'w')

    onload_normal, summary_normal = get_stat_list(stat_name, "test"+test_number+"_normal.csv")
    onload_amp, summary_amp = get_stat_list(stat_name, "test"+test_number+"_amp.csv")
    
    plot(*get_cdf(onload_normal,stat_name), axes)
    plot(*get_cdf(onload_amp,stat_name), axes)

    _, x_amp, _ = get_cdf(onload_amp, stat_name)
    _, x_normal, _ = get_cdf(onload_normal, stat_name)

    limit = max(float(x_amp[-1]), float(x_normal[-1]))

    axes.set_xlim(0, limit+x_normal[1])
    axes.set_ylim(0,1.01)

    axes.legend(["Normal","AMP"])
    
    # TABLE
    summary_list_normal = get_summary(summary_normal)
    summary_list_amp = get_summary(summary_amp)
    total_summary = [summary_list_normal, summary_list_amp]

    median_amp = summary_list_amp[4]
    median_normal = summary_list_normal[4]
    
    print(median_amp, median_normal)

    improvement_for_amp = round(((median_normal - median_amp)/median_normal)*100,2)
    print("improvement: ",round(improvement_for_amp,2),"\n\n")
    improvements.append(improvement_for_amp)

    plt.figure()
    plt.title(stat_name[3:])
    clust_data = total_summary

    collabel=("Mean", "S.D", "Min", "25% C.I", "50% C.I", "75 C.I", "Max")
    row_labels= ("Normal","AMP")
    plt.axis('off')
    plt.table(cellText=clust_data,colLabels=collabel,loc='center', rowLabels=row_labels, bbox = [0, 0.75, 1, 0.15], cellLoc='center', rowLoc='center')
    plt.savefig(stat_name[3:]+"_TABLE.png")
    

# JUST PLACE THE SCRIPT IN THE TEST FOLDER AND RUN IT 
if __name__ == "__main__":  
    test_number = 0

    cwd = os.getcwd()
    current_dir = cwd.split("\\")[-1]
    current_dir = current_dir.lower().split()[0]

    fig = plt.figure()
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    
    for i in range(10):
        if str(i) in current_dir and "test" in current_dir:
            test_number = i
            break
    if test_number == 0:
        print("failed")
        exit()

    stats = ["FV Document Complete Median","FV Fully Loaded Median", "FV First Byte Median", "FV Start Render Median", "FV Requests (Doc) Median","FV Load Event Start Median", "FV Speed Index Median", "FV Last Visual Change Median", "FV Visually Complete Median"]

    for i, s in enumerate(stats):
        ax = fig.add_subplot(3, 3, i+1)
        main(str(test_number), s, ax)

    fig.set_size_inches(15,11) 
    fig.savefig("ALL_CDFs.png",dpi=150)

    print(improvements)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 11:36:57 2018

@author: student
"""

import os
import numpy as np
import csv

for i in range(1,31):
    myDict = {}
    newfile = open("Audio_data_f/"+str(i)+".txt","w")
    mydata_dir = os.listdir("Sound_Analysis/"+str(i))
    j = 1
    with open("Audio_data_f/"+str(i)+".txt", "w") as output:
        stimulitypes = ["V","S","C"]
        features= ["Laughs","%Duration","meanDuration", "meanIntensity","medianIntensity", "medianDuration"]
        header = []
        for stimtype in stimulitypes:
            for feat in features:
                header.append(stimtype+"_"+feat)
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(header)
        for file in mydata_dir:
            if not file.startswith('.'):
                mydata = open("Sound_Analysis/"+str(i)+"/"+file,"r")
                arr = []
                k = 1
                
                for line in mydata:
                    line = str(line).strip().split(',')
                    if k ==1:
                        for val in line:
                           arr.append(val)
                    if k > 1:
                        med =np.median(np.array(line).astype(np.float))
                        arr.append(str(med))
                    k+=1
                k=1
                if file[5:7] not in myDict:
                    myDict[file[5:7]] = arr
                else:
                    for e in arr:
                        myDict[file[5:7]].append(e)
            j+=1
            if j%3 == 0:
                arr = []
        for key in sorted(myDict.keys()):
           writer.writerows([myDict[key]])
    
    newfile.close()

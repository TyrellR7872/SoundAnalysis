#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 13:08:45 2018

@author: student
"""
import os

path = "Raw_data/"
participant_data = os.listdir(path)
for file in participant_data:
    new_name = os.path.splitext(path+file)[0]
    participantno = new_name[len(new_name)-2:len(new_name)]
    if participantno[len(participantno)-2] == "_":
        participantno = participantno[len(participantno)-1]
    os.rename(path+file, path+participantno+".txt")
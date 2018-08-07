"""
File Name:      sound_analysis.py

Author Name:    Tyrell Roberts

Last Updated:   7/30/18

Description:    This script will perform a full sound analysis based on audio captured during participant recording and data
                outputted from the software iMotions. It will first extract timestamps from the data output in order to split
                each participant audio (.wav) into segments: video (V),survey (S), and captcha(C), for each stimuli, while also renaming them
                (Participant#_{Humorous,Non-humorous}_Video#_Position#_StimuliType). Then it will perform
                sound analysis by calling the software Praat, which will export specific data that will be inserted into the final data
                output.

"""

import os
import subprocess
import warnings
import numpy as np
import csv
import pandas as pd
import sys as platform

warnings.filterwarnings("ignore")  # Suppresses a warning thrown by the pydub package

from pydub import AudioSegment

class Splitter:

    def __init__(self, name):
        self.name = name
    '''
    Retrieves renamed stimuli name for simpler data manipulation
    '''
    def stimuliDict(self):
        readfile = open("stimuliRename.txt", "r") # Maps original stimuli name to numeral (E.g. A1 -> 1)
        newDict = {}

        for line in readfile:
            line = line.strip().split(",")
            newDict[line[0]] = line[1].strip()

        return newDict

    '''
    Renames each splitted audio to the appropriate format
    Note: This function may need to be modified depending on how your stimuli is
    '''
    def renameFile(self, stimuli, pos):
        stimuliRename = self.stimuliDict()
        humor_stim = ['A','C','E','G','I','K']
        stimulino = int(stimuliRename[stimuli[0:2]])
        stimtype = "V"
        positstr = str(pos)
        new_name = str(self.name)
        stimstr = str(stimulino)

        if pos < 10:
            positstr = "00"+positstr
        elif pos > 9 and pos < 100:
            positstr = "0"+positstr

        if stimulino < 10:
            stimstr = "0"+stimstr

        if int(self.name) < 10:
            new_name = "0"+new_name

        if "Survey" in stimuli:
            stimtype = "S"
        elif "Captcha" in stimuli:
            stimtype = "C"

        if stimuli[0] in funny:
            new_name = new_name+"_"+positstr+"_H_"+stimstr+"_"+str(stimtype)
        else:
           new_name = new_name+"_"+positstr+"_N_"+stimstr+"_"+str(stimtype)

        return new_name

    # Splits a large WAV file into smaller WAV files based on timestamps as input
    def split_wav(self, tfile):
        os.makedirs(r'Split_Audio/')
        wav_path = "Audio/Participant " + str(self.name) + ".wav"
        new_wav_path = "Split_Audio/" + str(self.name)
        original_audio = AudioSegment.from_file(wav_path, "wav")

        readfile = open("Timestamps/"+tfile)
        stimulis = []
        timestamps = []

        for line in readfile:
            line = line.split(",")
            stimulis.append(line[0])
            timestamps.append(int(line[1]))

        j=3
        i=1
        count = 0

        # Multiply by 1000 to convert from milliseconds to seconds
        for j in range(3,len(timestamps)-1):

            # This "splits" the WAV file based on two indices
            small_wav = original_audio[timestamps[j]+1:timestamps[j+1]]

            # File names continually increment upwards
            new_wav_name = self.renameFile(stimulis[j],i)
            i+=1

            # Makes a new folder for each subjects' split WAV files
            if not os.path.exists(new_wav_path):
                os.makedirs(new_wav_path)

            new_wav_file = new_wav_path + "/" + new_wav_name + ".wav"
            small_wav.export(new_wav_file, format="wav")
            count+=1

        small_wav = original_audio[timestamps[len(timestamps)-1]+1:len(original_audio)-1]
        new_wav_name = self.renameFile(stimulis[len(timestamps)-1],i)
        new_wav_file = new_wav_path + "/" + new_wav_name + ".wav"
        small_wav.export(new_wav_file, format="wav")

def header():
    stimulitypes = ["V","S","C"]
    features= ["Laughs","%Duration","meanDuration", "meanIntensity","medianIntensity", "medianDuration"]
    header = []
    for stimtype in stimulitypes:
        for feat in features:
            header.append(stimtype+"_"+feat)
    return header

def sound_to_csv(participantno):
    myDict = {}
    newfile = open("Audio_data/"+str(participantno)+".txt","w") # Desired output
    mydata_dir = os.listdir("Sound_Analysis/"+str(participantno))
    j = 1

    with open("Audio_data/"+str(participantno)+".txt", "w") as output:
        header = header()
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(header)

        # Traverse through each file for participant and insert data in sets of three (S,V,C) into newfile
        for file in mydata_dir:
            if not file.startswith('.'):
                mydata = open("Sound_Analysis/"+str(participantno)+"/"+file,"r")
                stimuli_arr = []
                k = 1

                for line in mydata:
                    line = str(line).strip().split(',')
                    for i in range(len(line)):
                        if line[i] == "":
                            del(line[i])
                        elif str(line[i]).strip() =='--undefined--':
                            line[i] = 0s
                        else:
                            line[i] = float(line[i].strip())
                    if k ==1:
                        if int(line[0]) == 0:
                            for i in range(6):
                                stimuli_arr.append(0)
                            break
                        stimuli_arr.append(int(line[0]))
                        for j in range(1,len(line)):
                           stimuli_arr.append(float(line[j]))
                    elif k > 1:
                        med =np.median(np.array(line).astype(np.float))
                        stimuli_arr.append(med)
                    k+=1
                k=1
                if file[9:11] not in myDict:
                    myDict[file[9:11]] = stimuli_arr
                else:
                    for e in stimuli_arr:
                        myDict[file[9:11]].append(e)
            j+=1
            if j%3 == 0:
                stimuli_arr = []
        for key in sorted(myDict.keys()):
           writer.writerows([myDict[key]])

    newfile.close()


def concfiles():
    filenames = []
    for i in range(1,31):
        filenames.append(str(i)+".txt")

    with open('final_output_sound.csv', 'w') as outfile:
        header = ""
        stimulitypes = ["V","S","C"]
        features= ["Laughs","%Duration","meanDuration", "meanIntensity","medianIntensity", "medianDuration"]
        for stimtype in stimulitypes:
            for feat in features:
                header = header+stimtype+"_"+feat+","
        header = header[0:len(header)-1]
        outfile.write(header+"\n")
        for fname in filenames:
            with open("Audio_data_f/"+fname) as infile:
                for line in infile:
                    outfile.write(line)

# Copies sound data into overall data output spreadsheet
def csv_to_final_output():
    stimulitypes = ["V","S","C"]
    features= ["Laughs","%Duration","meanDuration", "meanIntensity","medianIntensity", "medianDuration"]

    csv_input = pd.read_csv('final_output_sound.csv')
    csv_output = pd.read_csv('Project_Data_Output.csv')
    for stimtype in stimulitypes:
        for feat in features:
            csv_output[stimtype+"_"+feat]=csv_input[stimtype+"_"+feat]
    csv_output.to_csv('Project_Data_Output.csv', index=False)


# Retrieves Stimuli names and timestamps while ignoring unused lines
def timestamp_maker(participantno):
    readfile = open('Raw_data/'+str(participantno)+".txt")
    newfile = open("Timestamps/"+str(participantno)+".txt","w")

    i = 0
    array = []
    for line in readfile:
        if i < 5:
            i+=1
            continue
        if  i > 6:
            myarray = np.asarray(line.strip().split("\t"))
            if myarray[5] not in array:
                array.append(myarray[5])
                newfile.write(myarray[5]+","+myarray[8]+"\n")
        i+=1

    newfile.close()




if __name__ == "__main__":
    timestampspath = r'Timestamps/'
    if not os.path.exists(timestampspath):
        os.makedirs(timestampspath)

    x = int(raw_input("How many subjects do you have? (Please enter an integer) "))
    for i in range(1,x):
        timestamp_maker(i)
        txtfile = str(i)+".txt"
        splitter = Splitter(i)
        splitter.split_wav(txtfile)

    sound_analysispath = r'Sound_Analysis/'
    if not os.path.exists(sound_analysispath):
        os.makedirs(sound_analysispath)
    Calls the software Praat to retrieve and export specific sound data relating to laughter
    if platform == "darwin":
        subprocess.call("PATH/TO/PRAAT/APP --run laughter_analysis.praat", shell=True)
    elif platform == "win32":
        os.system ('"PATH/TO/PRAAT/APP" --open sound_analysis.praat')


    for i in range(1,x):
        sound_to_csv(i)
    concfiles()
    csv_to_final_output()

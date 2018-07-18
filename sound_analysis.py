"""
File Name:      sound_analysis.py

Author Name:    Tyrell Roberts

Last Updated:   7/17/18

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

warnings.filterwarnings("ignore")  # Suppresses a warning thrown by the pydub package

from pydub import AudioSegment

class Splitter:

    def __init__(self, name):
        self.name = name
        
    # Retrieves renamed stimuli name for simpler data manipulation
    def stimuliDict(self):
        readfile = open("stimuliRename.txt", "r") # Maps original stimuli name to numeral (E.g. A1 -> 1)
        newDict = {}
        
        for line in readfile:
            line = line.strip().split(",")
            newDict[line[0]] = line[1].strip()
            
        return newDict
    
    # Renames each splitted audio to the appropriate format
    def renameFile(self, stimuli,pos):
        stimuliRename = self.stimuliDict()
        funny = {'A','C','E','G','I','K'}
        stimulino = stimuliRename[stimuli]
        stimtype = "V"
        
        if "Survey" in stimuli:
            stimtype = "S"
        elif "Captcha" in stimuli:
            stimtype = "C"
        
        if stimuli[0] in funny:
            new_name = self.name+"_H_"+stimulino+"_"+pos+"_"+stimtype
        else:
           new_name = self.name+"_N_"+stimulino+"_"+pos+"_"+stimtype
        
        return new_name
        
        
        
        

    # Splits a large WAV file into smaller WAV files based on timestamps as input

    def split_wav(self,tfile):
        wav_path = "Audio/Participant_" + self.name + ".wav"
        new_wav_path = "Split_Audio/" + self.name 
        original_audio = AudioSegment.from_file(wav_path, "wav")

        readfile = open("Timestamps/"+tfile)
        stimulis = []
        timestamps = []
        
        for line in readfile:
            line = line.split(",")
            stimulis.append(int(line[1]))
            timestamps.append(int(line[2]))
 
        j=3
        i=1
        # Multiply by 1000 to convert from milliseconds to seconds
        while j < len(timestamps)-1:

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
            j+=1
            
def sound_to_csv(participantno):
    myDict = {} 
    newfile = open("Audio_data_f/"+str(participantno)+".txt","w") # Desired output 
    mydata_dir = os.listdir("Sound_Analysis/"+str(participantno))
    j = 1

    with open("Audio_data_f/"+str(participantno)+".txt", "w") as output:
        stimulitypes = ["V","S","C"]
        features= ["Laughs","%Duration","meanDuration", "meanIntensity","medianIntensity", "medianDuration"]
        header = []
        for stimtype in stimulitypes:
            for feat in features:
                header.append(stimtype+"_"+feat)
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(header)
        
        # Traverse through each file for participant and insert data in sets of three (S,V,C) into newfile
        for file in mydata_dir:
            if not file.startswith('.'):
                mydata = open("Sound_Analysis/"+str(participantno)+"/"+file,"r")
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

# Retrieves Stimulu names and timestamps while ignoring unused lines
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
    newpath = r'Timestamps/' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for i in range(1,31):
        timestamp_maker()
        txtfile = str(i)+".txt"
        splitter = Splitter(i)
        splitter.split_wav(txtfile)
        
    # Calls the software Praat to retrieve and export specific sound data relating to laughter
    subprocess.call("/Applications/Praat.app/Contents/MacOS/Praat --run laughter_analysis.praat", shell=True)
    for i in range(1,31):
        sound_to_csv(i)
            
              

# SoundAnalysis
A script that performs sound analysis with respect to laughter given data output from iMotions and audio wavs

The following explains how to use the following files:
1.sound_analysis.py 

To run: python sound_analysis.py

Input Files:
Folder: Raw_data (Contains spreadsheets of data in .csv extracted from iMotions for each participant)
Folder: Audio (Contains .wav files for every participant’s recording)
Folder: Sound_Analysis (Output of sound_analysis.praat)
Folder: Participant#
Subject#_Position#_Humorous/Non-Humorous_Stimuli#_Video/Survey/Captcha.txt (Contains laughter data)
Output Files:
Folder: Timestamps 
Participant#.txt (Contains timestamps extracted from Participant data in Raw_data folder)
Folder: Split_Audio
Folder: Participant #
Subject#_Position#_Humorous/Non-Humorous_Stimuli#_Video/Survey/Captcha.wav
Folder: Audio_data_f
Participant#.txt (Contains all subsegments’ laughter data concatenated into one file)



Notes:
Coding System used (Odd letters [A,C,E,G,I,K] = Humorous, Even Letters [B,D,F,H,J] = Non-Humorous)
A1, 1
A2, 2
A3, 3
A4, 4
B1, 5
B2, 6
B3, 7
B4, 8
B5, 9
C1, 10
C2, 11
C3, 12
C4, 13
C5, 14
D1, 15
D2, 16
D3, 17
D4, 18
D5, 19
E3, 20
E5, 21
F1, 22
F2, 23
F3, 24
F5, 25
G1, 26
G2, 27
G3, 28
G4, 29
G5, 30
H1, 31
H2, 32
H3, 33
H4, 34
H5, 35
I2, 36
I3, 37
I5, 38
J1, 39
J2, 40
J3, 41
J4, 42
K1, 43
K2, 44
K3, 45
K4, 46
K5, 47

If using Windows, in main function on line that reads:
os.system ('"PATH/TO/PRAAT/APP" --open sound_analysis.praat')
Replace PATH/TO/PRAAT/APP with the path to Praat.exe
If using macOS, in main function on line that reads:
subprocess.call("PATH/TO/PRAAT/APP --run laughter_analysis.praat", shell=True)
Replace PATH/TO/PRAAT/APP with the path to Praat application


2. sound_analysis.praat
	
	To Run: Opens from sound_analysis.py. Ctrl+R to Run.

	Input Files: 
Folder: Split_Audio

	Output Files: 
Folder: Sound_Analysis
Folder: Participant#
Subject#_Position#_Humorous/Non-Humorous_Stimuli#_Video/Survey/Captcha.txt (Contains laughter data)

	Notes:
Does not save TextGrids as of 8/1/18
Uncomment the following lines to perform automatic + post-correction analysis:
        #	selectObject: soundfile ,textgrid
       	# View & Edit
    
       	 #beginPause: "Annotation"
        #    	comment: "Press OK when done to save."
    
        #	endPause: "OK", 0
Recommend lines above to perform automatic only analysis
Laughter data format (by line):
1. Laugh Count, Proportion segment that is laughter, MeanDuration of laughter, Total Mean Intensity of Laughter
2. Median Intensity (array of intensities that are calculated in sound_analysis.py),
3. Median Duration (array of durations that are calculated in sound_analysis.py)
If segment has no laughter, then txt file contains:
0, --undefined—, --undefined--

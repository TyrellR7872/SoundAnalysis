pitch_min = 50
time_step = 0.3
silence_threshold = -35
min_pause = 0.1
min_voiced = 0.1
tier = 1


createDirectory: "Sound_Analysis"


for participant from 1 to 30
	directory$ = "Split_Audio/Participant_'participant'" 
    
    tier = 1
    Create Strings as file list... list 'directory$'*'.wav'
    number_files = Get number of strings

    for ifile to number_files
    	
    	select Strings list
    	sound$ = Get string... ifile
    	reportname$ = replace$: sound$, ".wav", "", 1
    	soundfile = Read from file... 'directory$''sound$'
    	objectname$ = selected$ ("Sound")
    	lengthSound = length (objectname$)
    	
    	textgrid = To TextGrid (silences)...  100 0.01 -45 0.05 0.1 silence laughter
    	# pop-up of sound and textgrid to manually confirm intervals
        	selectObject: soundfile ,textgrid
       	 View & Edit
    
       	 beginPause: "Annotation"
            	comment: "Press OK when done to save."
    
        	endPause: "OK", 0
    
    
    	selectObject: textgrid
    	# check how many intervals there are in the selected tier:
    	numberOfIntervals = Get number of intervals... tier
    
    	soundfile = Read from file... 'directory$''sound$'
    	objectname$ = selected$ ("Sound")
    	To Intensity... 100 0 
    	# loop through all the intervals
    	totalIntensity = 0
    	laughCount = 0 
    	totalLaughDuration = 0
    	totalDuration = 0 
    	medianIntensity$ = ""
    	medianDuration$ = ""	
    	for interval from 1 to numberOfIntervals
    		selectObject: textgrid 
    		label$ = Get label of interval... tier interval
    
    		# Calculates the duration + start&end points of one interval
    			start = Get starting point... tier interval
    			end = Get end point... tier interval
    			duration = end - start
    			totalDuration = totalDuration + duration
    
    		
    		# if the interval has some text as a label, then calculate.
    		laugh  = index_regex(label$, "laughter")
    		if laugh > 0
    			laughCount = laughCount + 1
    			totalLaughDuration = totalLaughDuration + duration
    			#calculates the intensity values
    			select Intensity 'objectname$'
    			meanIntensity = Get mean... start end dB
    			totalIntensity = totalIntensity + meanIntensity
    			medianIntensity$ = "'medianIntensity$''meanIntensity', "
    			medianDuration$ = "'medianDuration$''duration', "
    		endif
    directory$ = "Split_Audio" + "/" 
    		
    			
    	endfor
    	totalMeanIntensity = totalIntensity / laughCount
    	percentageDuration = ('totalLaughDuration' / 'totalDuration') *100
    	meanDuration = totalLaughDuration/ laughCount
    	medianDuration$ = left$ (medianDuration$ ,length (medianDuration$)-2)
    	resultline$ = "'laughCount', 'percentageDuration', 'meanDuration', 'totalMeanIntensity''newline$''medianIntensity$''newline$''medianDuration$'" 
    	appendFileLine: "Sound_Analysis/'reportname$'.txt", "'resultline$'"
    
    	select all
    	minus Strings list
    	Remove
    
    endfor
endfor
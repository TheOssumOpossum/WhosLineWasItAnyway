import os, librosa, scipy, numpy as np
from scipy.io import wavfile as wavf

def split_audio(file_name,AudioChanges=None,ExportName='test',parameter='log',split='neighbor'):
    rate, sci_music = wavf.read(file_name)
    music, sr = librosa.load(file_name)
    #print("Sample Rate Detected: ",sr)
    hop_length = 1024
    n_fft = 2048

    #mfcc - we think this should work but it doesnt
    if parameter == 'mfcc':
        mfcc = librosa.feature.mfcc(y=music, sr=sr)
        mfcc_short = mfcc[1:12,:]
        mfcc_diff = np.vstack((mfcc_short[:,:-1],np.diff(mfcc_short)))
        mat = sim_matrix(np.diff(mfcc_short).T)

    #chroma - this doesnt work
    if parameter == 'chroma':
        chroma = librosa.feature.chroma_stft(y=music, sr=sr, S=None,hop_length=hop_length)
        mat = sim_matrix(chroma.T)

    #log_spectrogram - this works really well
    if parameter == 'log':
        stft = librosa.stft(music, hop_length = hop_length, n_fft = n_fft)	
        log_spectrogram = librosa.logamplitude(np.abs(stft**2), ref_power=np.max)
        mat = sim_matrix(log_spectrogram.T)

    #trying to get some sort of measure for silence
    nrgs = None
    # print(log_spectrogram.T[0])
    # features = range(len(log_spectrogram.T))
    # nrgs = []
    # for i in features:
    # 	nrg = 0
    # 	for feature in log_spectrogram.T[i]:
    # 		if feature > -80.0:
    # 			nrg += feature*feature
    # 	nrg/= len(log_spectrogram.T[i])
    # 	nrgs += [nrg]
	   	#print("Energy for feature #",i,": ",nrg)

    #Normalizing vector
    # print(log_spectrogram.T[0])
    # for feature_vector in range(len(log_spectrogram.T)):
    # 	maxval = 0
    # 	for feature in range(len(log_spectrogram.T[feature_vector])):
    # 		log_spectrogram.T[feature_vector][feature] = log_spectrogram.T[feature_vector][feature]**2
    # 		if log_spectrogram.T[feature_vector][feature] > maxval:
    # 			maxval = log_spectrogram.T[feature_vector][feature] 
    # 	for feature in range(len(log_spectrogram.T[feature_vector])):
    # 		log_spectrogram.T[feature_vector][feature] /= float(maxval)
    # print(log_spectrogram.T[0])


    sections = group_sections(mat,AudioChanges,nrgs=nrgs,splitby = split)
    #print("Section Labels: ",sections)	
    write_audio(sci_music,sections,mat,sr=rate,audio_name = ExportName)
    return len(sections)-1


def sim_matrix(feature_vectors, distance_metric = 'cosine'):
    Y = scipy.spatial.distance.pdist(feature_vectors, distance_metric)
    matrix = scipy.spatial.distance.squareform(Y)
    return matrix

def group_sections(matrix,estimated_sections = None, threshold_start = 0.07, threshold_increment = 0.00005,nrgs=None,splitby='neighbor'):
	#matrix - similarity matrix
	#estimated_sections - group_sections tries to split the audio by number of sections, if None, use old code and ignore rest of args
	#threshold_start - first threshold for splitting
	#threshold_increment - threshold increment if previous threshold produced too many audio splits
    current_feature_vector = 1
    min_length = 30
    section_starts = [0]
    start_of_section = 0
    threshold = threshold_start
    number_of_feature_vectors = matrix.shape[0]
    if estimated_sections is not None:
        estimated_sections += 1

    #split the audio with threshold_start
    while (current_feature_vector < number_of_feature_vectors):
        comparing_vector = 0
        if splitby == 'neighbor':
            comparing_vector = current_feature_vector-1
        else:
            #splitby start
            comparing_vector = start_of_section
        #if(matrix[start_of_section][current_feature_vector] > threshold and abs(start_of_section-current_feature_vector)>min_length): #split the audio when similarity matrix exceeds threshold
        if(matrix[comparing_vector][current_feature_vector] > threshold and abs(start_of_section-current_feature_vector)>min_length): #split the audio when similarity matrix exceeds threshold

            #print("Splitting from feature #",start_of_section," to feature #",current_feature_vector-1)
            current_feature_vector -= 1
            section_starts += [current_feature_vector]
            start_of_section = section_starts[-1]
        current_feature_vector += 1
    section_starts += [number_of_feature_vectors]#add the last feature vector to audio splits
    if estimated_sections is None or len(section_starts) == estimated_sections:
        #print("Split into ",len(section_starts)-1," sections")
        return section_starts

    #used when a jump of threshold_increment goes from too many to too few splits (or vice versa)
    toosmall = False
    toobig = False
    if len(section_starts) > estimated_sections:
    	toobig = True
    if len(section_starts) < estimated_sections:
    	toosmall = True

    while len(section_starts) != estimated_sections:
        old_sections = section_starts
        section_starts = [0]
        current_feature_vector = 1
        start_of_section = 0
        if len(old_sections) < estimated_sections:
        	threshold -= threshold_increment
        else:
        	threshold += threshold_increment
        #print("new threshold: ", threshold)
        while (current_feature_vector < number_of_feature_vectors):
            comparing_vector = 0
            if splitby == 'neighbor':
                comparing_vector = current_feature_vector-1
            else:
                #splitby start
                comparing_vector = start_of_section
            #if(matrix[start_of_section][current_feature_vector] > threshold and abs(start_of_section-current_feature_vector)>min_length): #split the audio when similarity matrix exceeds threshold
            if(matrix[comparing_vector][current_feature_vector] > threshold and abs(start_of_section-current_feature_vector)>min_length): #split the audio when similarity matrix exceeds threshold
                #print("Splitting from feature #",start_of_section," to feature #",current_feature_vector-1)
                current_feature_vector -= 1
                section_starts += [current_feature_vector]
                start_of_section = section_starts[-1]
            current_feature_vector += 1
        section_starts += [number_of_feature_vectors]#add the last feature vector to audio splits

        #print(len(section_starts)-1)
        if len(section_starts) == estimated_sections:
        	#print("old splitting: ",len(old_sections)-1," new splitting: ",len(section_starts)-1," estimated splits: ",estimated_sections-1, " final_thresh: ", threshold)
        	return section_starts
        if len(section_starts) > estimated_sections:
        	toobig = True
        if len(section_starts) < estimated_sections:
        	toosmall = True
        if toosmall and toobig:
        	#print("old splitting: ",len(old_sections)-1," new splitting: ",len(section_starts)-1," estimated splits: ",estimated_sections-1, " final_thresh: ", threshold)
        	if len(section_starts) == 2:
        		return old_sections
        	if len(old_sections) == 2:
        		return section_starts
        	if abs(len(old_sections) -estimated_sections) < abs(len(section_starts) - estimated_sections):
        		#print("returning old")
        		return old_sections
        	else:
        		#print("returning new")
        		return section_starts


def write_audio(music,section_starts,matrix,audio_name = 'test', sr=16000):
	#given an audio file and an array of splits, exports the split audio files
    i = 0
    beat_length = music.size/matrix.shape[0]
    for start_feature in section_starts:
        if i == 0:
            i += 1
            continue
        start = section_starts[i-1]*beat_length
        end = section_starts[i]*beat_length
        section = music[int(start):int(end)]
        #print "Audio from section: ", start/beat_length, " to ", end/beat_length
        #audio(section,sr)
        output_sr = sr
        file_path = os.getcwd() + '\\AudioSegments\\' + audio_name + '_segment_' + str(i) + '.wav'
        #librosa.output.write_wav(file_path,section,output_sr)
        wavf.write(file_path,output_sr,section)
        i+= 1
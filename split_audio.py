import os, librosa, scipy, numpy as np

def split_audio(file_name,AudioChanges=None,ExportName='test'):
	music, sr = librosa.load(file_name)
	hop_length = 1024
	n_fft = 2048
	stft = librosa.stft(music, hop_length = hop_length, n_fft = n_fft)
	log_spectrogram = librosa.logamplitude(np.abs(stft**2), ref_power=np.max)
	mat = sim_matrix(log_spectrogram.T)
	sections = group_sections(mat,AudioChanges)
	write_audio(music,sections,mat,sr=sr,audio_name = ExportName)


def sim_matrix(feature_vectors, distance_metric = 'cosine'):
    Y = scipy.spatial.distance.pdist(feature_vectors, distance_metric)
    matrix = scipy.spatial.distance.squareform(Y)
    return matrix

def group_sections(matrix,estimated_sections = None, threshold_start = 0.075, threshold_increment = 0.001):
	#matrix - similarity matrix
	#estimated_sections - group_sections tries to split the audio by number of sections, if None, use old code and ignore rest of args
	#threshold_start - first threshold for splitting
	#threshold_increment - threshold increment if previous threshold produced too many audio splits
    current_feature_vector = 1
    section_starts = [0]
    start_of_section = 0
    threshold = threshold_start
    number_of_feature_vectors = matrix.shape[0]
    if estimated_sections is not None:
        estimated_sections += 1

    #split the audio with threshold_start
    while (current_feature_vector < number_of_feature_vectors):
        if(matrix[start_of_section][current_feature_vector] > threshold): #split the audio when similarity matrix exceeds threshold
            section_starts += [current_feature_vector]
            start_of_section = section_starts[-1]
        current_feature_vector += 1
    section_starts += [number_of_feature_vectors]#add the last feature vector to audio splits
    if estimated_sections is None or len(section_starts) == estimated_sections:
        print(len(section_starts))
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
        while (current_feature_vector < number_of_feature_vectors):
            if(matrix[start_of_section][current_feature_vector] > threshold): #split the audio when similarity matrix exceeds threshold
                section_starts += [current_feature_vector]
            	start_of_section = section_starts[-1]
            current_feature_vector += 1
        section_starts += [number_of_feature_vectors]#add the last feature vector to audio splits

        if len(section_starts) == estimated_sections:
        	print("old: ",len(old_sections)," new: ",len(section_starts)," est: ",estimated_sections, " final_thresh: ", threshold)
        	return section_starts
        if len(section_starts) > estimated_sections:
        	toobig = True
        if len(section_starts) < estimated_sections:
        	toosmall = True
        if toosmall and toobig:
        	print("old: ",len(old_sections)," new: ",len(section_starts)," est: ",estimated_sections, " final_thresh: ", threshold)
        	if abs(len(old_sections) -estimated_sections) < abs(len(section_starts) - estimated_sections):
        		return old_sections
        	else:
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
        librosa.output.write_wav(file_path,section,output_sr)
        i+= 1
__author__ = 'rose'
#all imports
import pandas as pd
import pickle as pkl

#path to the csv files, ie the db
path = '/home/rose/UMass/Courses/F15/BINDS/db/neurosynth-db/'

def readDB() :
    #read the files. they are tab separated
    features_tbl = pd.read_csv(path+'features.txt', sep="\t")
    #this file has pmids and activation info, 
    data_tbl = pd.read_csv(path+'database.txt',index_col='id', sep="\t")
    return data_tbl, features_tbl

def extract_xyz_from_data_tbl(data_tbl, columns_of_interest=['x','y','z']) :
    #num_of_cols = len(columns_of_interest)
    activation_info_tbl = data_tbl.reindex(columns=columns_of_interest)
    return activation_info_tbl

def fetch_pmids_above_threshold_for_word(features_tbl, word, threshold) :
    pmid_col = 'pmid'
    #create table from features table - with pmid as col1 and frequency of 'word' as col2
    pmids_word_freq = features_tbl.reindex(columns=[pmid_col, word])
    #fetch all those pmids whose frequency is above 'threshold'
    pmids_above_threshold = pmids_word_freq[pmids_word_freq[word]>threshold]
    return pmids_above_threshold

##
##Note : This method will be used with get_dict_activations_for_words() - to
##return a dictionary with pmids also
##
def get_activation_xys_for_word_dict(pmids_above_threshold,activation_info_tbl):
    pmid_col = 'pmid'
    #make a list of all the pmids and their threshold, from the dataframe of pandas
    #pmids_word_freq_list = pmids_above_threshold.values.tolist()
    pmids_list = pmids_above_threshold[pmid_col].tolist()
    #freq_list = pmids_above_threshold[word].tolist()

    #this is the activation dictionary being returned
    #keys are pmid, values are list of dictionary of x,y,z
    pmid_activation_dict = {}
    for i in pmids_list :
        activation_info = activation_info_tbl.loc[i]
        activation_list_for_pmid = []
        num_of_activations = activation_info.shape[0]
        for j in range(num_of_activations) :
        #for j in range(1) :
            act_info = activation_info.iloc[j]
            temp_dict = {}
            if(isinstance( act_info, pd.core.series.Series) == True) :
                temp_dict['x'] = act_info['x']
                temp_dict['y'] = act_info['y']
                temp_dict['z'] = act_info['z']
                '''temp_dict['space'] = act_info['space']
                temp_dict['peak_id'] = act_info['peak_id']'''
            elif(isinstance(act_info, (int, long, float, complex, str))== False) : 
                data_list = act_info.tolist()
                if(len(data_list) == 3) :
                    temp_dict['x'] = data_list[0]
                    temp_dict['y'] = data_list[1]
                    temp_dict['z'] = data_list[2]
                    '''temp_dict['space'] = data_list[3]
                    temp_dict['peak_id'] = data_list[4]'''
            activation_list_for_pmid.append(temp_dict)
        pmid_activation_dict[i] = activation_list_for_pmid
    return pmid_activation_dict

##
##NOTE : Use this, only if you require pmids also 
##this method still returns a dictionary. of .
##word = { pmid1 = [{x,y,z},{x,y,z}....], pmid2 = [{x,y,z},{x,y,z}....]...}; ie - a list of activation coordinates as x,y,z for every word
##
def get_dict_activations_for_words(words, threshold=0.0) :
    (data_tbl, features_tbl) = readDB()
    activation_info_tbl = extract_xyz_from_data_tbl(data_tbl)
    all_words_data_activations = {}
    for word in words:
        pmids_above_threshold = fetch_pmids_above_threshold_for_word(features_tbl, word, threshold)
        activation_dict = get_activation_xys_for_word_dict(pmids_above_threshold,activation_info_tbl)
		#print ("No of pmids for word: ", word, "above threshold: ",len(activation_dict.keys()))
        all_words_data_activations[word] = activation_dict
    return all_words_data_activations

##
##Note : This method will be used with get_list_activations_for_words() - to
##return a list of activations, pmids are not saved
##
def get_activation_xys_for_word_list(pmids_above_threshold,activation_info_tbl):
    pmid_col = 'pmid'
    #make a list of all the pmids and their threshold, from the dataframe of pandas
    pmids_list = pmids_above_threshold[pmid_col].tolist()

    #this is the activation list, being returned
    #list of dictionary of x,y,z
    activation_list = []
    for i in pmids_list :
        activation_info = activation_info_tbl.loc[i]
        num_of_activations = activation_info.shape[0]
        for j in range(num_of_activations) :
            act_info = activation_info.iloc[j]
            temp_dict = {}
            if(isinstance( act_info, pd.core.series.Series) == True) :
                temp_dict['x'] = act_info['x']
                temp_dict['y'] = act_info['y']
                temp_dict['z'] = act_info['z']
            elif(isinstance(act_info, (int, long, float, complex, str))== False) : 
                data_list = act_info.tolist()
                if(len(data_list) == 3) :
                    temp_dict['x'] = data_list[0]
                    temp_dict['y'] = data_list[1]
                    temp_dict['z'] = data_list[2]
            if(len(temp_dict)>0):
	            activation_list.append(temp_dict)
	#remove duplicate activations that might exist for the word
	if(len(activation_list)>0):
		unique_activation_list = {(v['x'],v['y'],v['z']):v for v in activation_list}.values()
    #UNCOMMENT FOR CHECKING DUPLICATE REMOVAL
	#print ("dup list len: ", len(activation_list))
	#print ("Non dup list len: ",len(unique_activation_list))
    return unique_activation_list

    
##
##NOTE : Better to use this, as only the activation co-ordinates matter, not the pmids
##this method still returns a dictionary. of .
##word = [{x,y,z},{x,y,z}....] ; ie - a list of activation coordinates as x,y,z for every word
##
def get_list_activations_for_words(words, threshold=0.0) :
    (data_tbl, features_tbl) = readDB()
    activation_info_tbl = extract_xyz_from_data_tbl(data_tbl)
    all_words_data_activations = {}
    for word in words:
        pmids_above_threshold = fetch_pmids_above_threshold_for_word(features_tbl, word, threshold)
        activation_list = get_activation_xys_for_word_list(pmids_above_threshold,activation_info_tbl)
        ###UNCOMMENT FOR DEBUGGING PICKLING
        #print ("No of activations for word: ", word, "above threshold: ",len(activation_list))
        all_words_data_activations[word] = activation_list
    return all_words_data_activations

##
##Use this method in case you want to pickle the data and store it. 
##With more words, the run time is huge. better to pickle the dict and keep it
##
def save_activations(words, store_as, filename):
    if(store_as=="list"):
        all_words_data_activations = get_list_activations_for_words(words)
    else:
    	all_words_data_activations = get_dict_activations_for_words(words)
    with open(filename, 'wb') as f:
        pkl.dump(all_words_data_activations, f)
    print ''
    print "Data has been pickled to file - "+filename
    print ''

if __name__=='__main__':
    #uncomment below block for simple testing
    '''words_list = ['emotion','accurate']
    acts_of_words_dict=get_dict_activations_for_words(words_list)
    acts_of_words_list=get_list_activations_for_words(words_list)
    print ''
    print 'TESTING WITH DICTIONARY OF PMIDS'
    print len(acts_of_words_dict[words_list[0]].keys())
    print len(acts_of_words_dict[words_list[1]].keys())
    print ''
    print ''
    print 'TESTING WITH LIST OF ACTIVATIONS'
    print len(acts_of_words_list[words_list[0]])
    print len(acts_of_words_list[words_list[1]])'''

    words_inputfile= '/home/rose/UMass/Courses/F15/BINDS/output/words_file'
    with open(words_inputfile, 'rb') as f:
        words_list = pkl.load(f)

    outputfile = '/home/rose/UMass/Courses/F15/BINDS/output/word_activation_list.pkl'

    save_activations(words_list, 'list', outputfile)

    words_activation_list = {}
    print ''
    print 'Loading from pickled file'
    with open(outputfile, 'rb') as f:
        words_activation_list = pkl.load(f)
    print ("No of activations for word: "+ words_list[0] +" is ",len(words_activation_list[words_list[0]]))
    print ("No of activations for word: "+ words_list[1]+" is ",len(words_activation_list[words_list[1]]))

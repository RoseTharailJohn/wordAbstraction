#all imports
import pandas as pd

#path to the csv files, ie the db
path = '/home/rose/UMass/Courses/F15/BINDS/neurosynth/data/'

def readDB() :
    #read the files. they are tab separated
    features_tbl = pd.read_csv(path+'features.txt', sep="\t")
    #this file has pmids and activation info, 
    data_tbl = pd.read_csv(path+'database.txt',index_col='id', sep="\t")
    return data_tbl, features_tbl

def extract_xyz_from_data_tbl(data_tbl, columns_of_interest)
    num_of_cols = len(columns_of_interest)
    activation_info_tbl = data_tbl.reindex(columns=columns_of_interest)
    return activation_info_tbl

def fetch_pmids_above_threshold_for_word(features_tbl, word, threshold) :
    #create table from features table - with pmid as col1 and frequency of 'word' as col2
    pmids_word_freq = features_tbl.reindex(columns=[pmid_col, word])
    #fetch all those pmids whose frequency is above 'threshold'
    pmids_above_threshold = pmids_word_freq[pmids_word_freq[word]>threshold]
    return pmids_above_threshold

def get_activation_xys_for_word(pmids_above_threshold,activation_info_tbl):
    #make a list of all the pmids and their threshold, from the dataframe of pandas
    pmids_word_freq_list = pmids_above_threshold.values.tolist()
    pmids_list = pmids_above_threshold[pmid_col].tolist()
    #freq_list = pmids_above_threshold[word].tolist()

    #this is the activation dictionary being returned
    #keys are pmid, values are list of dictionary of x,y,z, and all other columns of interest
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
                temp_dict['space'] = act_info['space']
                temp_dict['peak_id'] = act_info['peak_id']
            elif(isinstance(data_list, (int, long, float, complex))== False) : 
                data_list = act_info.tolist()
                if(len(data_list) == num_of_cols) :
                    temp_dict['x'] = data_list[0]
                    temp_dict['y'] = data_list[1]
                    temp_dict['z'] = data_list[2]
                    temp_dict['space'] = data_list[3]
                    temp_dict['peak_id'] = data_list[4] 
            activation_list_for_pmid.append(temp_dict)
        pmid_activation_dict[i] = activation_list_for_pmid
    return pmid_activation_dict

if __name__=='__main__':
    (data_tbl, features_tbl) = readDB()
    #extract required columns from data table
    columns_of_interest = ['x','y','z','space', 'peak_id']
    activation_info_tbl = extract_xyz_from_data_tbl(data_tbl, columns_of_interest)

    #later this has to be repeated for every word. for now testing on one word
    word = 'emotion'
    threshold = 0.0
    pmid_col = 'pmid'
    #get all pmids whose frequency for the 'word' is above 'threshold'
    pmids_above_threshold = fetch_pmids_above_threshold_for_word(features_tbl, word, threshold)
    #get activation xyz dictionary for each pmid as key in dict, for given word
    get_activation_xys_for_word(pmids_above_threshold,activation_info_tbl)
        

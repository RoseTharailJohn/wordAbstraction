__author__ = 'rose'
#all imports
import pandas as pd
import pickle as pkl

#path to the csv files, ie the db
path_to_neurosynth = '/home/rose/UMass/Courses/F15/BINDS/db/neurosynth-db/'
path_to_words_50k = '/home/rose/UMass/Courses/F15/BINDS/db/concreteness_ratings-db/'
neurosynth_words = pd.read_csv(path_to_neurosynth+'features.txt', sep="\t").columns.tolist()
words_50k = pd.read_csv(path_to_words_50k+'50k_word_concreteness_ratings.csv')['Word'].tolist()
words = list(set(words_50k) & set(neurosynth_words))
outputfile = '/home/rose/UMass/Courses/F15/BINDS/output/words_file'
print "Words can be found in path - "+outputfile
with open(outputfile, 'wb') as f:
        pkl.dump(words, f)
#uncomment following to test
'''with open(outputfile, 'rb') as f:
        words_list = pkl.load(f)
print "First 10 words are: ",words_list[0:10]'''
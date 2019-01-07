import os
import numpy as np
from collections import Counter


def make_Dictionary(root_dir):
    #Input is a directory path
    all_words = []
    emails = [os.path.join(root_dir,f) for f in os.listdir(root_dir)]
    for mail in emails:
        with open(mail) as m:
            for line in m:
                words = line.split()
                all_words += words
    dictionary = Counter(all_words)
    list_to_remove = dictionary.keys()

    for item in list_to_remove:
        if item.isalpha() == False:
            del dictionary[item]
        elif len(item) == 1:
            del dictionary[item]
    dictionary = dictionary.most_common(3000)

    return dictionary



def extract_features(mail_dir, dictionary):
    #Input is a directory path
    #Other input is the created dictionary
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files),3000))
    train_labels = np.zeros(len(files))
    count = 0;
    docID = 0;
    for fil in files:
      with open(fil) as fi:
        for i,line in enumerate(fi):
          if i == 2:
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                  wordID = i
                  features_matrix[docID,wordID] = words.count(word)
        train_labels[docID] = 0;
        filepathTokens = fil.split('/')
        lastToken = filepathTokens[len(filepathTokens) - 1]
        if lastToken.startswith("spmsg"):
            train_labels[docID] = 1;
            count = count + 1
        docID = docID + 1
    return features_matrix, train_labels



TRAIN_DIR = "../train-mails"
TEST_DIR = "../test-mails"


'''
Use these functions and these paths to create and organize the dictionary of features
'''
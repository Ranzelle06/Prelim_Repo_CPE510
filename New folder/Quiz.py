import os
import numpy as np
from collections import Counter
from sklearn import tree
from sklearn.metrics import accuracy_score
import graphviz

'''
PYTHON 3 CODE(WINDOWS)
IN VISUALIZING THE MODEL, INSTALL FIRST ON CONDA
COPY THIS TO ANACONDA PROMPT:

conda install -c anaconda graphviz

AFTER INSTALLING, RUN THE CODE.
AFTER RUNNING THE CODE, RUN THIS ON THE ANACONDA PROMPT

dot -Tpdf model.dot -o model.pdf

FIND THE PDF IN YOUR CURRENT WORKING DIRECTORY.
'''
#python decision_trees/code/decision_tree.py
print("START")
def make_Dictionary(root_dir,size):
    all_words = []
    emails = [os.path.join(root_dir,f) for f in os.listdir(root_dir)]
    for mail in emails:
        with open(mail) as m:
            for line in m:
                words = line.split()
                all_words += words
    dictionary = Counter(all_words)

    list_to_remove = list(dictionary)

    for item in list_to_remove:
        if item.isalpha() == False:
            del dictionary[item]
        elif len(item) == 1:
            del dictionary[item]

    dictionary = dictionary.most_common(size)
    return dictionary

def extract_features(mail_dir,size):
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files),size))
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


TRAIN_DIR = "decision_trees/train-mails/"
TEST_DIR = "decision_trees/test-mails/"
value=3000
dictionary=make_Dictionary(TRAIN_DIR,value)
'''
START 
'''
print("rsni")

features_matrix, labels = extract_features(TRAIN_DIR,value)
test_feature_matrix, test_labels = extract_features(TEST_DIR,value)

model=tree.DecisionTreeClassifier(criterion="entropy")

print("Training Model")

model.fit(features_matrix,labels)

predicted_labels=model.predict(test_feature_matrix)

print("FINISHED classifying accuracy score: ")
print(accuracy_score(test_labels,predicted_labels))

print(model)

with open("model.dot", "w") as f:
    f = tree.export_graphviz(model, out_file=f)
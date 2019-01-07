import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

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

score_Gaussian=[]
score_Bernoulli=[]
TRAIN_DIR = "C:/Users/RM A-225/Ricohermozo/Prelim_Repo_CPE510/New folder/train-mails/"
TEST_DIR = "C:/Users/RM A-225/Ricohermozo/Prelim_Repo_CPE510/New folder/test-mails/"
for flag_model in range (1,3,1):
    for i in range(100,1100,100):
        dictionary = make_Dictionary(TRAIN_DIR,i)
        print("Reading and processing emails from file...")
        features_matrix, labels = extract_features(TRAIN_DIR,i)
        test_feature_matrix, test_labels = extract_features(TEST_DIR,i)
        
        if flag_model==1:
            print("Training model: Gaussian")
            model = GaussianNB()
        else:
            print("Training model: Bernoulli")
            model = BernoulliNB()

        #train model
        model.fit(features_matrix, labels)
        predicted_labels = model.predict(test_feature_matrix)
        
        if flag_model==1:
            score_Gaussian.append(accuracy_score(test_labels, predicted_labels))
        else:
            score_Bernoulli.append(accuracy_score(test_labels, predicted_labels))
    

x = np.arange(100., 1100., 100)
plot=plt.figure()
plt.scatter(x,score_Gaussian,color='red')
plt.scatter(x,score_Bernoulli,color='blue')
plt.xlabel("Most Common Words")
plt.ylabel("Accuracy Score")
plt.legend(["Gaussian","Bernoulli"])
plt.title("Gaussian vs. Bernoulli Accuracy Scores")
plt.show()
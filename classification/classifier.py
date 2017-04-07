import itertools
import numpy as np
import pandas as pd
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from matplotlib import pyplot as plt

import nltk
nltk_data_folder = os.path.join(os.path.join(os.getcwd(), 'query_optimization'), 'nltk_data')
nltk.data.path.append(nltk_data_folder)

folder_path = os.path.join(os.getcwd(), 'classification')

def build_classifier():
    global folder_path
    if not (os.path.isfile(os.path.join(folder_path, 'train_data.csv')) and os.path.isfile(
            os.path.join(folder_path, 'test_data.csv'))):
        report = 'Error... Train and test data are not found. Please import and preprocess them first.'
        return report
    # read training data from csv files
    hotel_training_set = pd.read_csv(os.path.join(folder_path, 'train_data.csv'))
    # try this two lines to see which category is not good
    # hotel_training_set = hotel_training_set[hotel_training_set.targetName!="General"]
    # hotel_training_set = hotel_training_set[hotel_training_set.targetName!="Location"]
    train = {}
    train["targetNames"] = hotel_training_set['label']
    train["data"] = hotel_training_set['content'].values.astype('U')
    # remove stopwords, but seems nothing happened, why?
    train["data"] = preprocess(train['data'])

    hotel_test_set = pd.read_csv(os.path.join(folder_path, 'test_data.csv'))

    text_clf = Pipeline([('vect', CountVectorizer(decode_error='ignore')),
                         ('tfidf', TfidfTransformer()),
                         # ('clf', MultinomialNB()),
                         ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                               alpha=1e-3, n_iter=1000, random_state=42)),
                        ])

    # can declare more rules to remove trash
    exclusionList = ['\#',
                     '  +',
                     '\@\S+']
    exclusionList = '|'.join(exclusionList)

    newtraindata = []

    for x in train['data']:
        x = re.sub(exclusionList, '', str(x))
        if(len(x)<2):
            x = ""
        newtraindata.append(x)
    train['data'] = newtraindata

    text_clf = text_clf.fit(train["data"], train["targetNames"])

    newtestdata = []
    hotel_test_set["data"] = preprocess(hotel_test_set['content'])
    for x in hotel_test_set['data']:
        x = re.sub(exclusionList, '', str(x))
        newtestdata.append(x)
    hotel_test_set['data'] = newtestdata

    docs_test = hotel_test_set['data']
    predicted = text_clf.predict(docs_test)

    # show predict
    accuracy = np.mean(predicted == hotel_test_set['label'])
    print(accuracy)
    print(classification_report(hotel_test_set['label'], predicted))

    # Prepare confusion matrix for visualisation
    cnf_matrix = confusion_matrix(hotel_test_set['label'], predicted)
    np.set_printoptions(precision=2)
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=list(set(hotel_test_set['label'])),
                          title='Confusion matrix, without normalization')

    hotel_test_set['predicted'] = predicted
    hotel_test_set.to_csv(os.path.join(folder_path, "prediction.csv"), index=False)

    # Save models
    with open(os.path.join(folder_path, 'classifier.pickle'), mode='wb') as classifier_file:
        pickle.dump(text_clf, classifier_file)

    report = 'Classifier was built with accuracy of ' + str(accuracy) + '.'
    return report


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(os.path.join(folder_path, 'plot.png'), format='png')


def get_classifier():
    global folder_path
    if not os.path.isfile(os.path.join(folder_path, 'classifier.pickle')):
        return None
    with open(os.path.join(folder_path, 'classifier.pickle'), mode='rb') as classifier_file:
        classifier = pickle.load(classifier_file)
    return classifier


def preprocess(data):
    for i in range(len(data)):
        try:
            sentence = data[i]
            # sentence_token = tokenize(sentence)
            # sentence_token = remove_stopwords(sentence_token)
            # sentence = ' '.join(sentence_token)
            data[i] = sentence
        except TypeError as err:
            print(err)
    return data


def tokenize(sentence):
    return word_tokenize(sentence, language='english')


def remove_stopwords(tokens):
    cleaned_tokens = [token for token in tokens if token not in stopwords.words('english')]
    return cleaned_tokens


def stem_words(tokens):
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

if __name__ == '__main__':
    build_classifier()

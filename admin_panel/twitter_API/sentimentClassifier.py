import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# read training data from csv files
# rename the tweet_601_800.csv to labeled_tweetlist.csv
# rename the column names to below names
# put in model and train
tweet_list = pd.read_csv('labeled_tweetlist.csv');
train = {}
train["targetNames"] = tweet_list['target_name']
train["targetValue"] = tweet_list['target_value']
train["data"] = tweet_list['status']
# read test data
test_tweets = pd.read_csv('tweet_list_401_600.csv');
test = {}
test["data"] = test_tweets['data']
test["targetNames"] = test_tweets['targetNames']
test["targetValues"] = test_tweets['targetValues']
#
#
# count_vect = CountVectorizer(decode_error='ignore')
# X_train_counts = count_vect.fit_transform(train.data)
# X_train_counts.shape
#
# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# X_train_tfidf.shape
#
#
# clf = MultinomialNB().fit(X_train_tfidf, train.targetNames)
#
#
#
# # In[97]:
#
# X_new_counts = count_vect.transform(docs_new)
#


# pipeline

text_clf = Pipeline([('vect', CountVectorizer(decode_error='ignore')),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
                    ])

text_clf = text_clf.fit(train["data"], train["targetNames"])



docs_test = test["data"]
predicted = text_clf.predict(docs_test)
result = {}
result['predicted'] = np.asarray(predicted)
# result['status'] = test_tweets['data']
# result['targetName'] = test_tweets['targetNames']
# np.savetxt('test.txt', np.asarray(predicted), delimiter=" ", fmt="%s")
# np.savetxt("prediced.csv", array(result).reshape(1,), delimiter=",", fmt="%s")
print(np.mean(predicted == test["targetNames"]))


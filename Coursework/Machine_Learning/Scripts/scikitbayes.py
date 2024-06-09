import numpy as np
import time, re
from scipy.sparse import lil_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn import metrics

def scikitbayes(data):
  """The scikitbayes() function prepares data to be used by the Scikit-learn
  library's diverse classifiers. It automatically outputs time statistics,
  accuracy measurements, and the classification report from Scikit-learn. The
  function returns the accuracy scores for both the Gaussian and Multinomial
  classifiers.

  The function takes one argument:
  (1) data : the dataset as a list of tuples with the first element containing
  the textual data and the second element its classification"""

  start = time.time()
  print('Training...')

  ## creates the vocabulary ##
  vocab = {}
  for tup in data:
    text = re.sub('[\"\'’‘”“,.?!;:*()><&|»«]', '', tup[0])
    text = re.sub('[-/—[]–]', ' ', text)
    for token in text.split():
        token = token.lower().strip()
        if token not in vocab:
          vocab[token] = 1
        else:
          vocab[token] += 1

  ## defines the dimensions of the matrix ##
  matrix = lil_matrix((len(data), len(vocab)))

  ## assigns ids to each token and article ##
  token_ids = {token : i for i, token in enumerate(vocab)}

  ## populates a matrix ##
  classifications = []
  for i, tup in enumerate(data):
    text = re.sub('[\"\'’‘”“,.?!;:*()><&|»«]', '', tup[0])
    text = re.sub('[-/—[]–]', ' ', text)

    classifications.append(tup[1])

    for token in text.split():
      token = token.lower().strip()
      matrix[i, token_ids[token]] += 1

  ## assigns content to variables for scikit-learn's classifiers ##
  X = matrix.toarray()
  y = np.array(classifications)

  ## clean up ##
  del vocab
  del matrix
  del token_ids
  del classifications

  ## splits and prepares the data ##
  X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = y, random_state = 0, train_size = 0.9)

  mid = time.time()
  print(f'     Data preparation elapsed {round(mid - start, 2)} seconds.\n')

  print('Testing Accuracy...')
  ## Gaussian Naiive Bayes Classifier ##
  gnb = GaussianNB()
  y_pred_gnb = gnb.fit(X_train, y_train).predict(X_test)
  print(f"     Scikit-Learn's Gaussian Naiive Bayes Classifier's accuracy is {round(((y_test == y_pred_gnb).sum() / X_test.shape[0]) * 100, 2)}% with {X_test.shape[0]} test cases.")
  accuracy_gnb = ((y_test == y_pred_gnb).sum() / X_test.shape[0])
  endG = time.time()

  ## Multinomial Naiive Bayes Classifier ##
  mnb = MultinomialNB()
  y_pred_mnb = mnb.fit(X_train, y_train).predict(X_test)
  print(f"     Scikit-Learn's Multinomial Naiive Bayes Classifier's accuracy is {round(((y_test == y_pred_mnb).sum() / X_test.shape[0]) * 100, 2)}% with {X_test.shape[0]} test cases.\n")
  accuracy_mnb = ((y_test == y_pred_mnb).sum() / X_test.shape[0])
  end = time.time()

  print('Metrics...')
  print('     Gaussian Naiive Bayes:\n', metrics.classification_report(y_test, y_pred_gnb, zero_division = 0))
  print('     Multinomial Naiive Bayes:\n', metrics.classification_report(y_test, y_pred_mnb, zero_division = 0))

  print('Time Statistics...')
  print(f'     Gaussian classification elapsed {round(endG - mid, 2)} seconds.')
  print(f'     Multinomial classification elapsed {round(end - endG, 2)} seconds.\n')
  print(f'     Total operation elapsed {round(end - start, 2)} seconds.\n')

  return accuracy_gnb, accuracy_mnb

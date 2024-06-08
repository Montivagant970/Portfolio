from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from scipy.sparse import lil_matrix
from sklearn import metrics
import time, re
import numpy as np

def scikitkNN(data, neighbors, metric):
  """The scikitkNN() is a function that prepares data to be used by the Scikit-learn
  library's k-Nearest Neighbor classifier. It automatically outputs time statistics,
  accuracy measurements, and the classification report from Scikit-learn.

  The function takes three arguments:
  (1) data : the dataset as a list of tuples with the first element containing
  the textual data and the second element its classification
  (2) neighbors : an integer for the number of neighboring points to be taken
  into consideration when classifying
  (3) metric : a string with the heuristic to be used in classifying. Viable
  heuristics can be found on the Scikit-learn's website"""

  start = time.time()
  print('Training...')

  ## create the vocabulary following the classifier's same procedure ##
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

  ## define the dimensions of the matrix ##
  matrix = lil_matrix((len(data), len(vocab)))

  ## assign ids to each token and article ##
  token_ids = {token : i for i, token in enumerate(vocab)}

  ## populate the matrix ##
  classifications = []
  for i, tup in enumerate(data):
    text = re.sub('[\"\'’‘”“,.?!;:*()><&|»«]', '', tup[0])
    text = re.sub('[-/—[]–]', ' ', text)

    classifications.append(tup[1])

    for token in text.split():
      token = token.lower().strip()
      matrix[i, token_ids[token]] += 1

  ## assigning variables for scikit-learn's classifiers ##
  X = matrix.toarray()
  y = np.array(classifications)

  ## clean up ##
  del vocab
  del matrix
  del token_ids
  del classifications

  ## data splitting ##
  X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = y, random_state = 0, train_size = 0.9)

  ## data preparation and normalization ##
  pipe_knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors = neighbors, metric = metric))

  mid = time.time()
  print(f'     Data preparation elapsed {round(mid - start, 2)} seconds.\n')

  print('Testing Accuracy...')
  ## k-Nearest Neighbor Classifier ##
  pipe_knn.fit(X_train, y_train)
  y_pred = pipe_knn.predict(X_test)
  print(f"     Scikit-Learn's k-Nearest Neighbor Classifier's accuracy using the {metric.upper()} distance metric is {round(pipe_knn.score(X_test, y_test) * 100, 2)}% with {X_test.shape[0]} test cases.\n")
  accuracy = pipe_knn.score(X_test, y_test) * 100
  end = time.time()

  print('Metrics...')
  print('     k-Nearest Neighbor:\n', metrics.classification_report(y_test, y_pred, zero_division = 0))

  print('Time Statistics...')
  print(f'     k-Nearest Neighbor classification elapsed {round(end - mid, 2)} seconds.\n')
  print(f'     Total operation elapsed {round(end - start, 2)} seconds.\n')

  return accuracy

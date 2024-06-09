import re, math, time
import matplotlib.pyplot as plt
from sklearn import metrics

class FakeNewsClassifier:
  """The FakeNewsClassifier class applies a Multinomial Naiive Bayes classification
  on text data.

  To instantiate the class, five arguments must be passed:
  (1) data : the dataset as a list of tuples with the first element containing
  the textual data and the second element its classification
  (2) stopwords : a list of stopwords to be used to remove semantically vacant
  words from the vocabulary
  (3) skipbucket : the number of the bucket to be skipped in training and testing
  (4) datasize : an integer representing the decimal fraction of the dataset
  desired. For example if only 20% of the data is wanted, '.2' would be written
  for this argument. The default is '1,' i.e. all the data.
  (5) test : a Boolean value, which when set to true tests the accuracy of the
  classifier on the given dataset. Otherwise, the classifier is only trained,
  but not tested"""

  def __init__(self, data, stopwords, skipbucket, datasize = 1, test = False):
    start = time.time()
    print('Training...')

    self.vocabulary = {}
    self.prob = {}
    self.totals = {}
    self.stopwords = {}
    self.categories = []

    ## reduces the dataset ##
    data = self.reducedata(data, datasize)

    ## instantiates the buckets ##
    buckets = self.makebuckets(data)

    ## defines the categories ##
    for tup in data:
      try:
        int(tup[1])
        self.categories.append(tup[1])
      except:
        pass

    self.categories = set(self.categories)

    ## sets the stopwords ##
    for word in stopwords:
      self.stopwords[word] = 1

    ## counts token frequency and token totals for each category ##
    for category in self.categories:
      (self.prob[category], self.totals[category]) = self.train(buckets, category, skipbucket, stopwords)

    ## simplifies the vocabulary ##
    tbdeleted = []
    for word in self.vocabulary:
      if self.vocabulary[word] < 3:
        tbdeleted.append(word)

    for word in tbdeleted:
      del self.vocabulary[word]

    ## computes the probabilities ##
    lenvocab = len(self.vocabulary)
    for category in self.categories:
      denominator = self.totals[category] + lenvocab
      for word in self.vocabulary:
        if word in self.prob[category]:
          count = self.prob[category][word]
        else:
          count = 1
        self.prob[category][word] = (float(count + 1) / denominator)

    mid = time.time()
    print(f'     Data preparation elapsed {round(mid - start, 2)} seconds.')

    ## tests accuracy ##
    if test == True:
      print('\nTesting Accuracy...')
      self.test(buckets, skipbucket, output = True, mets = True)

    end = time.time()
    print('Time Statistics...')
    print(f'     Classification elapsed {round(end - mid, 2)} seconds.')
    print(f'     Total operation elapsed {round(end - start, 2)} seconds.')


  ## methods ##
  def train(self, buckets, category, skipbucket, stopwords):
    """The train() method does three tasks: (1) creates a vocabulary of all tokens
    and maintains a token count, (2) counts the frequency of every token, and (3)
    counts the total tokens (to be later used as a total count for each category).

    The method takes four arguments:
    (1) buckets : the training data divided previously into buckets
    (2) category : the current category being trained upon
    (3) skipbucket : the bucket number to be skipped to be used as a test set
    (4) stopwords : the list of stopwords to be excluded"""

    counts = {}
    total = 0
    for bucket, content in buckets.items():
      if bucket != skipbucket:
        for tup in content:
          text = re.sub('[\"\'’‘”“,.?!;:*()><&|»«]', '', tup[0])
          text = re.sub('[-/—[]–]', ' ', text)
          if tup[1] == category:
            tokens = text.split()

            for token in tokens:
              token = token.strip()
              token = token.lower()

              if token not in stopwords:
                self.vocabulary.setdefault(token, 0)
                self.vocabulary[token] += 1
                counts.setdefault(token, 0)
                counts[token] += 1
                total += 1

    return (counts, total)


  def makebuckets(self, data):
    """The makebuckets() method divides the dataset into 10 equally sized buckets.

    The method takes one argument:
    (1) data : the dataset in the form of a tuple with the first element containing
    the text data and the second element the classification"""

    divider = int(len(data) / 10)
    buckets = {}
    for i in range(0, 10):
      buckets[i + 1] = data[i * divider : (i * divider) + divider]

    return buckets


  def reducedata(self, data, datasize = 1):
    """The reducedata() method reduces the size of the dataset in order to test
    upon only a subsection of the data.

    The method takes two arguments:
    (1) data : the dataset
    (2) datasize : an integer representing the decimal fraction of the dataset
    desired. For example if only 20% of the data is wanted, '.2' would be written
    for this argument. The default is '1,' i.e. all the data."""

    bound = round(len(data) * datasize)

    return data[: bound]


  def classify(self, testcase):
    """The classify() method takes a single data element (one text), cleans its
    contents, and calculates the log probability of an individual token belonging
    to a specific class. It then adds that probability to a running total, which
    gets sorted to return the most likely class to which the text belongs.

    The method takes one argument:
    (1) testcase : the single text being considered for classification."""

    results = {}
    for category in self.categories:
      results[category] = 0

    text = re.sub('[\"\'’‘”“,.?!;:*()><&|»«]', '', testcase)
    text = re.sub('[-/—[]–]', ' ', text)
    tokens = text.split()

    for token in tokens:
      token = token.strip().lower()

      if token in self.vocabulary:
        for category in self.categories:
          try:
            results[category] += math.log(self.prob[category][token])
          except:
            self.prob[category].setdefault(token, 0)
            self.prob[category][token] += 1
            results[category] += math.log(self.prob[category][token])

    results = list(results.items())
    results.sort(key = lambda tuple: tuple[1], reverse = True)

    return results[0][0]


  def test(self, buckets, skipbucket, output = False, mets = False):
    """The test() method takes the test set, iterates through each text, and
    applies the classify() method to derive its predicted class. It counts the
    total cases and the total correct predictions to calculate the accuracy of
    the classifier on the given dataset.

    The method takes four arguments:
    (1) buckets : the training data divided previously into buckets
    (2) skipbucket : the bucket number previously skipped to be used here as a
    test set
    (3) output : a Boolean value, which when set to True outputs the accuracy of
    the classifier on the amount of test cases present in the bucket
    (4) mets : a Boolean value, which when set to True outputs the classification
    report from Scikit-Learn"""

    total = 0
    correct = 0
    y_test = []
    y_pred = []
    for bucket, content in buckets.items():
      if bucket == skipbucket:
        for tup in content:
          result = self.classify(tup[0])
          if result != None:
            total += 1
            y_test.append(tup[1])
            y_pred.append(result)

            if result == tup[1]:
              correct += 1

    if output == True:
      print(f'     Accuracy is {round(((float(correct) / total) * 100), 2)}% with {total} test cases.\n')

    if mets == True:
      print('Metrics...')
      print(metrics.classification_report(y_test, y_pred, zero_division = 0))

    return float(correct) / total

import csv, random, nltk
from FakeNewsClassifier import FakeNewsClassifier
from NewsClassifier import NewsClassifier
from scikitbayes import scikitbayes
from scikitkNN import scikitkNN


## Inputs ##
data = []
with open('fakenews.csv', encoding='ISO-8859-1') as filein: #reads in the csv file
  reader = csv.reader(filein)
  for i, row in enumerate(reader):
    if i != 0: #skips the first row, i.e. header
      data.append((row[0], row[1]))
random.shuffle(data) #shuffles the data

data1 = []
with open('Articles.csv', 'r', encoding='ISO-8859-1') as filein:
  reader = csv.reader(filein)
  for row in reader:
    data1.append((row[0], row[1]))
random.shuffle(data1)

stopwords = nltk.corpus.stopwords.words('english')


## FakeNewsClassifier ##
print('FakeNewsClassifier:')
fnc = FakeNewsClassifier(data, stopwords, 5, test = True)
print('\n', '-' * 70, '\n')


## Scikit-learn's Gaussian and Multinomial Classifiers ##
print("Scikit-learn's Gaussian and Multinomial Classifiers:")
accuracy_gnb, accuracy_mnb = scikitbayes(data)
print('-' * 70, '\n')


## Scikit-learn's k-Nearest Neighbor Classifier ##
print("Scikit-learn's k-Nearest Neighbor Classifier:")
accuracy = scikitkNN(data, 3, 'cosine')
print('-' * 70, '\n')


## NewsClassifier ##
print('NewsClassifier:')
nc = NewsClassifier(data1, stopwords, 5, test = True)

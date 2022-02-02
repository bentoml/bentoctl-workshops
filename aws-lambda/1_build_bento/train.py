from sklearn import svm
from sklearn import datasets

import bentoml


# Load training data
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Model Training
clf = svm.SVC(gamma='scale')
clf.fit(X, y)

bentoml.sklearn.save("iris_clf", clf)

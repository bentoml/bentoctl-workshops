import numpy as np

import bentoml

from bentoml.io import NumpyNdarray

iris_clf_runner = bentoml.sklearn.load_runner('iris_clf:latest')

svc = bentoml.Service('iris_classifier', runners=[iris_clf_runner])

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def predict(input_ndarray: np.ndarray) -> np.ndarray:
    result = iris_clf_runner.run(input_ndarray)
    return result

from typing import Dict

import bentoml
from bentoml.io import JSON, Text

# create a runner with the sentiment_clf model
sentiment_clf_runner = bentoml.transformers.load_runner(
    "sentiment_clf:latest", tasks="sentiment-analysis", lm_head="classifier"
)

# create a new bentoml service and the sentiment_clf_runner to it
svc = bentoml.Service("sentiment_analysis", runners=[sentiment_clf_runner])

# dict to convert Lable from model -> Human readable label
keys = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE",
}


# define the /predict endpoint that is used for inference
@svc.api(input=Text(), output=JSON())
def predict(input_text: str) -> Dict:
    """
    /predict endpoint

    This endpoint takes a Text input, runs the inference with the runner
    and returns the result as JSON.
    """
    # run inference with the input_text that is received to the endpoint
    result = sentiment_clf_runner.run(input_text)

    # post-processing
    if result["label"] in keys:
        result["label"] = keys[result["label"]]

    # return the result as response
    return result

import bentoml
from bentoml.io import JSON, Text

sentiment_clf_runner = bentoml.transformers.load_runner(
    "sentiment_clf:latest", tasks="sentiment-analysis", lm_head="classifier"
)

svc = bentoml.Service("sentiment_analysis", runners=[sentiment_clf_runner])

keys = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE",
}


@svc.api(input=Text(), output=JSON())
def predict(input_text):
    result = sentiment_clf_runner.run(input_text)

    if result["label"] in keys:
        result["label"] = keys[result["label"]]
    return result

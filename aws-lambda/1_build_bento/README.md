# Build ML server with BentoML

Time to complete: 10 minutes.

## What are we building?

We are going to build a ML server with BentoML. First we will create an
[sentiment analysis](https://en.wikipedia.org/wiki/Sentiment_analysis) model with 
the [Hugging Face transformers library](https://huggingface.co/docs/transformers/index). 
This model, given a text input, will
infer how positive or negative the sentiment of the input text is. We will be
using a pre-trained model and we will build a Bento server with it. After
testing, we will build it and save to the local system.


## Build Bento server

### 1. Create the model

We going to use a pre-trained model from the Hugging Face. There is `train.py` file
in this folder that has 3 models already configured that are ready for you to be used.

- `cardiffnlp/twitter-roberta-base-sentiment` - a very popular model that is
  used for sentiment analysis tasks. Model size is ~500Mb.
- `bhadresh-savani/distilbert-base-uncased-sentiment-sst2` - this model is 
  based on distill bert and is ~250Mb in size.
- `dhpollack/distilbert-dummy-sentiment` - this is a dummy model that outputs
  random results for any inference string.
  
You are free to choose any of these 3 models as you see fit. If you choose a 
larger model it might take you longer to complete the workshop based on your 
internet speed but will give better results after inferenence. 

To choose the model, open the `train.py` 
file and uncomment the `MODEL` name that you want to use and then run
```
python train.py
```
This will download the model and save it into the BentoML local model store.

### 2. Test and debug Bento Server

The BentoML service has been created for you in the `./bento.py` file. Lets take
a look at that file

```python
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
```

This service takes in Text input and return a JSON with the result.
Let's serve it and test the API out.
```
bentoml serve ./bento.py:svc --reload
```

Once the server has started up successfully, send test request in another terminal

```
curl \
-X POST \
-H "content-type: application/json" \
--data "This is a test." \
http://127.0.0.1:5000/predict

# sample output
{"label":"NEUTRAL","score":0.612240731716156}% 
```

Go ahead and sent different texts to the endpoint and see what the responses are.
Note: if you are using the dummy model then the result will be always `{"label":"NEGATIVE","score":0.5%`.

### 3. Build Bento 

Now that we have tested the service and made sure everything is working let's build
the bento and save it to the local bento store.
```
bentoml build

# sample output
[07:49:56 PM ] INFO     Building BentoML service "sentiment_analysis:azyrubeiega4mk5z" from
                        build context "/home/username/username/bentoml/bentoctl-workshops/aws
                        -lambda/1_build_bento"
               INFO     Packing model "sentiment_clf:r573sheh6wbdgh6p" from
                        "/home/username/bentoml/models/sentiment_clf/r573sheh6wbdgh6p"
               INFO     Locking PyPI package versions..
[07:50:02 PM ] INFO
                        ██████╗░███████╗███╗░░██╗████████╗░█████╗░███╗░░░███╗██╗░░░░░
                        ██╔══██╗██╔════╝████╗░██║╚══██╔══╝██╔══██╗████╗░████║██║░░░░░
                        ██████╦╝█████╗░░██╔██╗██║░░░██║░░░██║░░██║██╔████╔██║██║░░░░░
                        ██╔══██╗██╔══╝░░██║╚████║░░░██║░░░██║░░██║██║╚██╔╝██║██║░░░░░
                        ██████╦╝███████╗██║░╚███║░░░██║░░░╚█████╔╝██║░╚═╝░██║███████╗
                        ╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░░╚════╝░╚═╝░░░░░╚═╝╚══════╝

               INFO     Successfully built Bento(tag="sentiment_analysis:azyrubeiega4mk5z")
                        at
                        "/home/username/bentoml/bentos/sentiment_analysis/azyrubeiega4mk5z/"
```

### 4. Validate build result

List out the bentos using the `bentoml list` command and see if the bento
`sentiment_clf` that we just created is there.
```
> bentoml list
# sample output
Tag                                  Service      Path                                                               Size        Creation Time
sentiment_analysis:uja63oeh6wbdgh6p  bento:svc    ~/bentoml/bentos/sentiment_analysis/uja63oeh6wbdgh6p  478.79 MiB  2022-02-07 09:09:26
```

If it is, the congrations, you have successfully created the bentoml service for 
sentiment analysis using a pretrained model from Hugging Face. Now lets 
deploy this into AWS Lambda.

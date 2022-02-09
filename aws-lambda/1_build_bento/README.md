# Build ML server with BentoML

Time to complete: 10 minutes.

## What are we building?

We are going to build a ML server with BentoML. First we will create an
sentiment analysis model with the Hugging Face transformers library. We will be
using a pre-trained model and then we will build a Bento server with it. After
testing, we will build it and save to the local system.


## Build Bento server

### 1. Create the model

We going to use a pre-trained model from the Hugging Face. You are free another
other model you preffer too. Currently we have 2 models that we can use in the
train.py script

- `cardiffnlp/twitter-roberta-base-sentiment` - a very popular model that is
  used for sentiment analysis tasks. Model size is ~500Mb.
- `dhpollack/distilbert-dummy-sentiment` - this is a dummy model that can be
  used if you want to create a lighter bento service that consumes the lowest
  bandwith possible.

Open the `train.py` file uncomment the `MODEL` name that you want to use and
then run
```
python train.py
```
This will download the model and save it into the BentoML Local Model Store.

### 2. Test and debug Bento Server

The BentoML service has been created for you in the `./bento.py` file. Lets take
a look at that file

```python
# ./bento.py
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
```

As you can see the service takes in Text input and return a JSON with the result.
Let run serve this service and test the API out.
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
Note: if you are using the dummy model then the result will be always consant.

### 3. Build Bento 

Now that we have tested the service and made sure everything is working lets build
the bento save it to the local bento store.
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

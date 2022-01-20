## Build ML server with BentoML

Time to complete: 10 minutes.

### What are we building?

We are going to build a ML server with BentoML. First we will train an iris flower classifier model with SKlearn and then we will build a Bento server. After testing, we will build it and save to the local system.


### Build Bento server

1. Train the model

```
python train.py
```

2. Test and debug Bento Server

```
bentoml serve ./bento.py:svc --reload
```

Send test request in another terminal

```
curl \
-X POST \
-H "content-type: application/json" \
--data "[[5, 4, 3, 2]]" \
http://127.0.0.1:5000/predict
```


3. Build Bento 

```
bentoml build
```

4. Validate build result

```
bentoml list
```

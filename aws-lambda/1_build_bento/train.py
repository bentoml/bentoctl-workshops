from transformers import AutoTokenizer, AutoModelForSequenceClassification
import bentoml


# PLEASE UNCOMMENT THE MODEL YOU WANT TO USE
# MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
# MODEL = "bhadresh-savani/distilbert-base-uncased-sentiment-sst2"
# MODEL = "dhpollack/distilbert-dummy-sentiment"


# load the model and tokenizer for the MODEL selected
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# save the model into bentoml's model store
bentoml.transformers.save("sentiment_clf", model=model, tokenizer=tokenizer)

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import bentoml


# PLEASE UNCOMMENT THE MODEL YOU WANT TO USE
# MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
# MODEL = "dhpollack/distilbert-dummy-sentiment"
# MODEL = "bhadresh-savani/distilbert-base-uncased-sentiment-sst2"


tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

bentoml.transformers.save("sentiment_clf", model=model, tokenizer=tokenizer)

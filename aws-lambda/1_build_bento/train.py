from transformers import AutoTokenizer, AutoModelForSequenceClassification
import bentoml


MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
# if you want a smaller model, use this (~200M)
# MODEL = "bhadresh-savani/distilbert-base-uncased-sentiment-sst2"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

bentoml.transformers.save("sentiment_clf", model=model, tokenizer=tokenizer)

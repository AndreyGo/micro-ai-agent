import os
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from deeppavlov import build_model, configs
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet", quiet=True)

MODEL_NAME = os.getenv("MODEL_NAME", "sberbank-ai/sbert_large_nlu_ru")

embedding_model = SentenceTransformer(MODEL_NAME, device="cpu")

try:
    spell_model = build_model(
        configs.spelling_correction.en_ru_spell_corrector, download=True
    )
except Exception:
    spell_model = None

try:
    ru_lemmatizer = build_model(configs.morpho_tagger.lemma_ru, download=True)
except Exception:
    ru_lemmatizer = None

en_lemmatizer = WordNetLemmatizer()

app = FastAPI()


class TextRequest(BaseModel):
    text: str


@app.post("/embed")
async def generate_embedding(req: TextRequest):
    embedding = embedding_model.encode(req.text).tolist()
    return {"embedding": embedding}


@app.post("/correct")
async def correct_text(req: TextRequest):
    corrected = req.text
    if spell_model:
        try:
            corrected = spell_model([req.text])[0]
        except Exception:
            corrected = req.text
    lemmas = []
    if ru_lemmatizer:
        try:
            lemmas = ru_lemmatizer([corrected])[0]
        except Exception:
            lemmas = []
    if not lemmas:
        # Fallback to simple English lemmatizer
        lemmas = [en_lemmatizer.lemmatize(word) for word in corrected.split()]
    return {"corrected": corrected, "lemmas": lemmas}

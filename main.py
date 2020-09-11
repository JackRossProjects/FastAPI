from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from joblib import load

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Verifies the API is deployed, and links to the docs
    """
    return HTMLResponse("""
    <h1>Fake News Detector API</h1>
    <p>Go to <a href="/docs">/docs</a> for documentation.</p>
    """)

pipeline = load('fakenewsmodel.joblib')

class Story(BaseModel):
  title: str



@app.post('/predict')
async def predict(story: Story):
    """
    Predict whether a news article is real or fake news, 
    based on its title & text

    Naive baseline: Always predicts 'fake'
    """

    # verifies we can read request body
    print(story)
    X = pd.DataFrame([dict(story)])
    print(X.to_markdown())

    # use pickled pipeline to predict
    prediction = pipeline.predict(X)[0]
    probability = pipeline.predict_proba(X).max()

    return {
        'prediction': prediction, 
        'proobability': probability
    }
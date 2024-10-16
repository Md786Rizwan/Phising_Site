import uvicorn
from fastapi import FastAPI, Request, Form
import joblib
import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

# Load the phishing model
try:
    phish_model = open("phishing.pkl", 'rb')
    phish_model_ls = joblib.load(phish_model)
except FileNotFoundError:
    print("Phishing model file not found.")

# ML Aspect
class URL(BaseModel):
    website: str

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={'request': request})

@app.post('/predict')
async def predict(request: Request, url: str = Form(...)):
    features = url

    X_predict = []
    X_predict.append(str(features))
    
    # Perform the prediction
    try:
        y_Predict = phish_model_ls.predict(X_predict)[0]
    except Exception as e:
        result = f"Error in prediction: {str(e)}"
        return templates.TemplateResponse("index.html", context={'request': request, 'result': result, 'url': url, 'error': True})

    if y_Predict == 'bad':
        result = "This is a Phishing Site"
    else:
        result = "This is not a Phishing Site"
    
    return templates.TemplateResponse("index.html", context={'request': request, 'result': result, 'url': url, 'error': False})

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)

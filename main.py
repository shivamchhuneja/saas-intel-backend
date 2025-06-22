from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from analyzer.scrape import scrape_homepage
from analyzer.prompts import run_analysis
import asyncio

app = FastAPI()

# Allow frontend (Streamlit) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/scrape")
async def scrape_endpoint(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return {"error": "Missing URL"}

    try:
        text = await scrape_homepage(url)
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze")
async def analyze_endpoint(request: Request):
    data = await request.json()
    text = data.get("text")
    mode = data.get("mode")
    api_key = data.get("api_key")

    if not all([text, mode, api_key]):
        return {"error": "Missing one or more fields: text, mode, api_key"}

    try:
        result = await run_analysis(text, mode, api_key)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

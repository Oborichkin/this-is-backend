import aiohttp
from RfcParser import RFC
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

with open("data/rfc3261.txt", "r") as f:
    rfc = RFC(f.read())

app = FastAPI()

coreference_endpoint = "http://localhost:8001/"

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return rfc.json


@app.get("/resolved")
async def root():
    result = []
    async with aiohttp.ClientSession() as session:
        for ch in rfc.json["chapters"]:
            for i, sec in enumerate(ch["sections"]):
                if sec["type"] == "text":
                    async with session.post(coreference_endpoint, json={"text": sec["text"]}) as resp:
                        text = await resp.json()
                        result.append({
                            "chapter": ch["title"],
                            "section": i,
                            "text": text
                        })
    return result

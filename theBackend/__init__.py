import aiohttp
from RfcParser import RFC
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .crud import get_all_entity_names, search_entity

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


@app.get("/entities")
async def entities():
    return get_all_entity_names()


@app.get("/entity")
async def entity(name: str):
    return search_entity(name)


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

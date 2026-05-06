from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import os
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
import chromadb
from google import genai

#we're using a private ai bc the documents we're looking at are private
#i never got this working but like. its probably close enough

load_dotenv()

#make connections to the db and the gemini ai
chroma_client = chromadb.PersistentClient("./chroma_db")
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


#put each colelction into the dictionary
collections = {}
for name in ["opponents_2026","roster_2026","scouting_2027"]:
    collections[name] = chroma_client.get_collection(name)

#similar to sql model classes, just not connected to a db
#makes sure everything is in teh right format/datatype
class Question(BaseModel):
    #when data comes in, itll have a question, and which report they want to work with (they pick)
    question: str
    collection: Literal["opponents_2026","roster_2026","scouting_2027"]


app = FastAPI()

@app.post("/ask")
def ask(payload: Question):
    collection = collections[payload.collection]
    results = collection.query(query_texts=[payload.question], n_results = 8)
    chunks = results["documents"][0] #bc queries return as dictionaries w/ arrays

    context = "\n\n".join(chunks) #bc the llm only takes in strings
    prompt = f"""Answer the coach's question using only the context below.
    If the answer is not in the context, say so politely.

    Context:
    {context}

    Question: {payload.question}"""

    response = gemini_client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    #return {"answer": response.text, "chunks": chunks} #included to see the response vs chunks, but unnecessicary
    return {"answer":response.text}



app.mount("/", StaticFiles(directory="static", html=True), name="static")
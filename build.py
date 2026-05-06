import chromadb

#for files: each section is broken up by 70 "-" between each one
SEPARATOR = "-" * 70
#gonna treat each section as a document

#funtion for splitting the document into chunks
def load_chunks(filename):
    with open(filename) as f:
        text = f.read()
    sections = text.split(SEPARATOR)
    #could do more text editing/formatting, if needed or wanted
    return sections


#creates persistent database (folder w sqlite db)
client = chromadb.PersistentClient("./chroma_db")

#the files, and what we're gonna refer to them as (for simplicity)
files_and_collections = [
    ("opponents_2026.txt","opponents_2026"),
    ("roster_2026.txt","roster_2026"),
    ("scouting_2027.txt","scouting_2027")
]

#iterate through all the files in files_and_collections, get and save the chunks and assign them to their respective collection
for filename, collection_name in files_and_collections:
    chunks = load_chunks(filename)
    collection = client.get_or_create_collection(collection_name)

    ids = []
    for i in range(len(chunks)):
        ids.append(f"chunk_{i}")

    collection.add(documents=chunks, ids=ids)


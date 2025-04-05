import chromadb

# Create or connect to the persistent DB
client = chromadb.PersistentClient(path="./db/chroma_dbs")

def get_collection(username: str):
    return client.get_or_create_collection(name=f"{username}_memory")

def list_collections():
    return [col.name for col in client.list_collections()]
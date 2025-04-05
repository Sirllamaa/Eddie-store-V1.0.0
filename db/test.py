import chromadb
from memory_add import add_memory
from memory_query import query_memories

# Add memory
add_memory("bob", "Eddie should track CPU load", [0.1, 0.2, 0.3])

# Query memory
results = query_memories("alice", [0.1, 0.2, 0.3])
print(results)

# Get collections
client = chromadb.PersistentClient(path="./db/chroma_dbs")
print(client.list_collections())

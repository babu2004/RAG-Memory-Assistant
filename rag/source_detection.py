from pathlib import Path


"""
Retrieve all unique document sources stored in ChromaDB.
"""

def get_available_sources(collection)->list[str]:

    results = collection.get(include = ["metadatas"])

    metadatas = results.get("metadatas",[])

    sources = sorted({
        metadata['source']
        for metadata in metadatas
        if metadata and "source" in metadata
    })

    return sources



def detect_source(query:str, collection) -> str | None :

    query = query.lower()

    sources = get_available_sources(collection)

    for source in sources:
        document_name = Path(source).stem.lower()
        if document_name in query :
            return source
    
    return None



from pathlib import Path


"""
Retrieve all unique document sources stored in ChromaDB.
"""


def detect_source(query:str, registry):

    query = query.lower()

    for source in registry.get_sources():

        document_name = Path(source).stem.lower()
        
        if document_name in query :
            return source
    
    return None



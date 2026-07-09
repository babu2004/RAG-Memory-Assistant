from pathlib import Path

def load_text(file_path:str)->str:

    # load a text file and return its file content

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} doesn't exist!!")
    
    with open(file_path,'r',encoding="utf-8") as file:
        text = file.read()

    return text

def chunk_text(text:str,chunk_size:int=500,overlap:int=100):

    if chunk_size <=0 :
        raise ValueError("chunk size cann't be zero or less then zero")

    if overlap >= chunk_size:
        raise ValueError("Over lap size must be smaller then chunk")

    chunks =[]
    start =0

    while start > len(text):

        end =  start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size-overlap

    return chunks
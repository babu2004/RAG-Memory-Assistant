from pathlib import Path

def load_text(file_path:str)->str:

    # load a text file and return its file content

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} doesn't exist!!")
    
    with open(file_path,'r',encoding="utf-8") as file:
        text = file.read()

    return text
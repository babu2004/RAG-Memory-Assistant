from pathlib import Path
from pypdf import PdfReader
def load_text(file_path:str)->str:

    # load a text file and return its file content

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} doesn't exist!!")
    
    with open(file_path,'r',encoding="utf-8") as file:
        text = file.read()

    return text


def load_pdf(file_path:str)->str:

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text+=page_text+ "\n"

    return text



def load_document(file_path:str)->str:

    extention = Path(file_path).suffix.lower()

    if extention == ".txt":
        return load_text(file_path)
    
    elif extention == ".pdf":
        return load_pdf(file_path)

    raise ValueError(f"Unsupported file format: {extention}")
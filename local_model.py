from sentence_transformers import SentenceTransformer

# This downloads the model files from the web
model = SentenceTransformer("all-MiniLM-L6-v2")

# This saves the physical files into a folder in your current directory
model.save("./my_local_model")
print("Model successfully saved to ./my_local_model")

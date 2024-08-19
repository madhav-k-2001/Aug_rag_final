from langchain_community.vectorstores import FAISS
import pandas as pd
from langchain.schema import Document
from langchain_cohere import CohereEmbeddings
from config_pg import * 
from dotenv import load_dotenv

def faiss_vector_db():
    load_dotenv()
    df = pd.read_csv(r"C:\Users\Lenovo\PycharmProjects\boomlive\theDataset.csv", encoding='utf-8')
    print("file Loaded")
    
    # Create a list of LangChain documents
    documents = []
    for _, row in df.iterrows():
        doc = Document(
            page_content=row['text'],
            metadata={'source': row['url']}
        )
        documents.append(doc)

    embedding_model = CohereEmbeddings(
                            model=EMBEDDER
                        )

    db = FAISS.from_documents(documents, embedding_model)
    db.save_local(r"D:\jupyter projects\FaissLocalEmbedding")
    print("Vector Store Creation Completed")

if __name__ == "__main__":
    
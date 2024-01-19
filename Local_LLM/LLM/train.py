import box
import yaml
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

# Import config vars
with open('func.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def run_ingest():
    # loader = DirectoryLoader(cfg.DATA_PATH,
    #                          glob='*.pdf',
    #                          loader_cls=PyPDFLoader)

    #loader = TextLoader("data\sample_doctors.txt")
    loader = TextLoader("data\sample_packages.txt")

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.CHUNK_SIZE,
                                                   chunk_overlap=cfg.CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=cfg.EMBEDDINGS,
                                       model_kwargs={'device': 'cpu'})

    vector = FAISS.from_documents(texts, embeddings)
    vector.save_local(cfg.DB_FAISS_PATH)

if __name__ == "__main__":
    run_ingest()

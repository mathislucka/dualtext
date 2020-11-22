from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

class SentenceEmbedding():
    def __init__(self):
        self.model = model
    
    def process_documents(self, documents):
            
        #Our sentences we like to encode
        sentences = [document.content for document in documents.all()]
        ids = [document.id for document in documents.all()]

        #Sentences are encoded by calling model.encode()
        embeddings = self.model.encode(sentences, convert_to_tensor=True)
        embeddings = [pickle.dumps(ndarray, protocol=None, fix_imports=True, buffer_callback=None) for ndarray in embeddings]


        return zip(ids, embeddings)

    def process_query(self, query):
        embeddings = self.model.encode([query])
        return embeddings[0]


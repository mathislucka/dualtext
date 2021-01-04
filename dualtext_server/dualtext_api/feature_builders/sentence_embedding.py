from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer('distilbert-multilingual-nli-stsb-quora-ranking')

class SentenceEmbedding():
    def __init__(self):
        self.model = model
    
    def process_documents(self, documents):
            
        sentences = [document.content for document in documents.all()]
        ids = [document.id for document in documents.all()]
        sentences = self.split_list(sentences, 250)

        to_store = []
        for lst in sentences:
            embeddings = self.model.encode(lst, convert_to_tensor=True)
            to_store.extend([pickle.dumps(ndarray, protocol=None, fix_imports=True, buffer_callback=None) for ndarray in embeddings])
        
        return zip(ids, to_store)

    def process_query(self, query):
        embeddings = self.model.encode([query])
        return embeddings[0]
    
    def split_list(self, lst, chunk_size):
        return [lst[i * chunk_size:(i + 1) * chunk_size] for i in range((len(lst) + chunk_size - 1) // chunk_size )]



import ollama
import scipy.spatial.distance as dst

def create_vector_store(file_name,model_name):
    documents=list()
    vector_store=dict()
    file=open(file_name,'r')
    for chunk in file:
        if chunk!='\n':
            documents.append(chunk)
    for index,chunk in enumerate(documents):
        vector=ollama.embeddings(model=model_name,prompt=chunk)
        vector_store.update({index:vector['embedding']})
    return vector_store,documents

def query_engine(vector_store,documents,model_name,query):
    vector_query=ollama.embeddings(model=model_name,prompt=query)
    distances={index:dst.cosine(vector_query['embedding'],db_vector) for index,db_vector in vector_store.items()}
    min_index=min(distances, key=distances.get)
    return documents[min_index]

if __name__ == "__main__":
    model_name='all-minilm'
    vector_store,document=create_vector_store('data/Textos_de_Entrenamientos.txt',model_name) #Aqui puedes colocarle el texto el cual quieres que la IA responda tus querys o preguntas. El archivo de entrenamiento debe estar en la carpeta Data del proyecto.
    while True:
        query = input('My query: ')
        if query=='exit':
            break 
        else:
            response=query_engine(vector_store,document,model_name,query)
            print(response)

#Puedes usar muchos modelos, con mucha mas capacidad de procesamiento :D

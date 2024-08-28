from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from typing import List
import matplotlib
matplotlib.use('Agg')  # Define o backend para Agg
import matplotlib.pyplot as plt

from features.slant import slant
from svm.main import train_and_test_svm

app = FastAPI()

@app.post("/manuscripts")
async def train_data_and_return(training_images : List[UploadFile] = File(...), test_image : UploadFile = File(...), labels: int = Query(..., alias="labels")):
    """
    Recebe as imagens de treino e teste, treina o SVM e realiza a predição.
    """
    
    if len(training_images) != 2:
        raise HTTPException(status_code=400, detail="Exatamente duas imagens de treino são necessárias.")
    
    train_data = []
    test_data = []
    
    for i, image in enumerate(training_images):
        contents = await image.read()
        result = slant(contents)
        train_data.append(result)
        
        # Criar e salvar gráfico do histograma de treino
        plt.figure()
        plt.bar(range(17), result)
        plt.title(f"Histograma Imagem de Treino {i+1}")
        plt.xlabel("Ângulo")
        plt.ylabel("Frequência Normalizada")
        plt.savefig(f"histograma_treino_{i+1}.png")
        plt.close()  # Fechar a figura para liberar memória

    contents = await test_image.read()
    result = slant(contents)
    test_data.append(result)
    
     # Criar e salvar gráfico do histograma de teste
    plt.figure()
    plt.bar(range(17), result)
    plt.title("Histograma Imagem de Teste")
    plt.xlabel("Ângulo")
    plt.ylabel("Frequência Normalizada")
    plt.savefig("histograma_teste.png")
    plt.close()  # Fechar a figura para liberar memória

    accuracy = train_and_test_svm(labels, train_data, test_data)

    return {"accuracy": accuracy}

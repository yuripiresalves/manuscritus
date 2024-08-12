from fastapi import FastAPI, File, UploadFile, Query
from typing import List

from features.slant import slant
from svm.main import train_and_test_svm

app = FastAPI()

train_data = [] 
test_data = []   #

@app.post("/manuscripts/training") 
async def read_manus(images: List[UploadFile] = File(...)):
    """
    Recebe uma lista de imagens de manuscritos para treino.
    """
    
    for image in images:
        contents = await image.read()
        result = slant(contents)
        train_data.append((result))

    return {"message": f"Imagens de treino adicionadas com sucesso!"}

@app.post("/manuscripts/test")
async def test_manus(image: UploadFile = File(...)):
    """
    Recebe uma imagem de manuscrito para teste.
    """
    contents = await image.read()
    result = slant(contents)
    test_data.append(result)
    return {"message": "Imagem de teste adicionada com sucesso!"}

@app.get("/manuscripts/predict") 
async def predict_manuscript(labels: int = Query(..., alias="labels")):
    """
    Treina o SVM e realiza a predição na imagem de teste.
    """
    if not train_data or not test_data:
        return {"error": "Dados de treino ou teste não encontrados!"}


    accuracy = train_and_test_svm(labels, train_data, test_data) 

    return {"accuracy": accuracy} 

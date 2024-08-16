from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from typing import List

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
    
    for image in training_images:
        contents = await image.read()
        result = slant(contents)
        train_data.append(result)

    contents = await test_image.read()
    result = slant(contents)
    test_data.append(result)

    accuracy = train_and_test_svm(labels, train_data, test_data)

    return {"accuracy": accuracy}

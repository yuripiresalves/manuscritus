from fastapi import FastAPI, File, UploadFile
from typing import List

from features.slant import slant 

app = FastAPI()

@app.post("/manuscripts")
async def read_manus(images: List[UploadFile] = File(...)):
    """
    Recebe uma lista de imagens de manuscritos e as processa.

    Args:
        images: Lista de arquivos de imagem do tipo UploadFile.

    Returns:
        Um dicionário com o resultado do processamento de cada imagem.
    """
    results = {}
    for image in images:
        # Lê o conteúdo do arquivo de imagem.
        contents = await image.read() 
        
        # Chama a função slant para processar a imagem.
        result = slant(contents) 
        
        # Adiciona o resultado ao dicionário de resultados.
        results[image.filename] = result 
    return results
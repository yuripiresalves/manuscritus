from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from models.main import init


# Classe para validar o corpo da requisição
class ModelRequest(BaseModel):
    num_authors: int
    models: List[str]


app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/results")
async def get_results(request: ModelRequest):
    """
    Realiza a carga dos dados, seleção de autores aleatórios, normalização das características e
    testes de modelos de aprendizado de máquina (SVM e Random Forest).

    Args:
        request (ModelRequest): Um objeto contendo os parâmetros da requisição.
            - num_authors (int): Número de autores aleatórios a serem selecionados para o teste.
            - models (List[str]): Lista de modelos a serem testados. Os modelos podem incluir:
                - "svm": para executar o modelo SVM.
                - "random_forest": para executar o modelo Random Forest.

    Returns:
        dict: Um dicionário com as acurácias dos modelos testados. O dicionário pode conter:
            - "accuracy_svm": Acurácia do modelo SVM (em percentual).
            - "accuracy_svm_grid_search": Acurácia do modelo SVM com Grid Search (em percentual).
            - "best_params_svm": Melhores parâmetros encontrados para o modelo SVM.
            - "accuracy_rf": Acurácia do modelo Random Forest (em percentual).

        Caso nenhum modelo reconhecido seja solicitado, o retorno será:
            - "error": Mensagem indicando que nenhum modelo foi reconhecido.
    """
    num_authors = request.num_authors
    models = request.models

    # Inicializa o teste com os autores e modelos fornecidos
    results = init(num_authors, models)

    return results

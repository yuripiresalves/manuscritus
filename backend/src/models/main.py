import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

from .svm import train_and_test_svm
from .random_forest import train_and_test_random_forest


def select_random_authors(train_df, test_df, num_authors):
    """
    Seleciona um número especificado de autores aleatórios e filtra os
    dados de treino e teste para incluir apenas esses autores.

    Args:
        train_df (pd.DataFrame): DataFrame contendo os dados de treino com
        as inclinações e o autor.
        test_df (pd.DataFrame): DataFrame contendo os dados de teste com
        as inclinações e o autor.
        num_authors (int): Número de autores a serem selecionados aleatoriamente.

    Returns:
        pd.DataFrame, pd.DataFrame: DataFrames de treino e teste filtrados com
        os autores selecionados.

    Raises:
        ValueError: Se o número de autores solicitado for maior que o número
        de autores disponíveis nos dados de treino.
    """

    # Obter os autores únicos no conjunto de treino
    unique_authors = train_df["autor"].unique()

    # Verificar se o número de autores solicitados é menor ou igual ao número total de autores
    if num_authors > len(unique_authors):
        raise ValueError(
            "O número solicitado de autores excede o número de autores disponíveis."
        )

    # Sortear os autores aleatoriamente
    selected_authors = np.random.choice(unique_authors, size=num_authors, replace=False)

    # Filtrar os dados de treino e teste com base nos autores selecionados
    selected_train = train_df[train_df["autor"].isin(selected_authors)]
    selected_test = test_df[test_df["autor"].isin(selected_authors)]

    return selected_train, selected_test


def init(num_authors, models):
    """
    Função principal para carregar dados, selecionar autores aleatórios,
    normalizar as características e realizar testes com SVM e Random Forest.

    Args:
        num_authors (int): Número de autores aleatórios a serem selecionados.
        models (list): Lista de modelos a serem testados. Pode incluir "svm" e/ou "random_forest".

    Returns:
        dict: Um dicionário contendo a acurácia dos modelos testados.
    """
    # Carregar os dados de treino e teste
    train_df = pd.read_csv("../treino.csv")
    test_df = pd.read_csv("../teste.csv")

    # Selecionar autores aleatórios
    train_df, test_df = select_random_authors(train_df, test_df, num_authors)

    # Separar as características (inclinacoes) e a classe (autor)
    X_train = train_df.iloc[:, 1:].values
    y_train = train_df["autor"].values

    X_test = test_df.iloc[:, 1:].values
    y_test = test_df["autor"].values

    # Normalização dos dados
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    results = {}

    # Testar modelos
    if "svm" in models:
        accuracy_svm, accuracy_svm_grid_search, best_params_svm = train_and_test_svm(
            X_train, y_train, X_test, y_test
        )
        results["accuracy_svm"] = accuracy_svm * 100
        results["accuracy_svm_grid_search"] = accuracy_svm_grid_search * 100
        results["best_params_svm"] = best_params_svm

    if "random_forest" in models:
        accuracy_rf = train_and_test_random_forest(X_train, y_train, X_test, y_test)
        results["accuracy_rf"] = accuracy_rf * 100

    # Verificação caso nenhum modelo válido tenha sido selecionado
    if not results:
        return {"error": "Nenhum modelo reconhecido."}

    return results

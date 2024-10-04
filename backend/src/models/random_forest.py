from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def train_and_test_random_forest(X_train, y_train, X_test, y_test):
    """
    Treina um modelo Random Forest com os dados fornecidos, avalia o desempenho no conjunto de teste
    e retorna a acurácia do modelo.

    Args:
        X_train (np.array): Conjunto de dados de treino contendo as características (features).
        y_train (np.array): Conjunto de rótulos de treino (autores).
        X_test (np.array): Conjunto de dados de teste contendo as características (features).
        y_test (np.array): Conjunto de rótulos de teste (autores).

    Returns:
        float: Acurácia do modelo Random Forest no conjunto de teste.

    Detalhes:
        1. O modelo Random Forest é configurado com 100 estimadores (árvores de decisão) e uma semente aleatória fixa para reprodutibilidade.
        2. O modelo é treinado com os dados de treino e em seguida faz previsões no conjunto de teste.
        3. A acurácia do modelo é calculada usando a métrica `accuracy_score` e é exibida no console.
    """

    # Inicializar o modelo Random Forest com 100 árvores de decisão
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Treinar o modelo com os dados de treino
    rf_model.fit(X_train, y_train)

    # Fazer previsões no conjunto de teste
    y_pred = rf_model.predict(X_test)

    # Avaliar a acurácia do modelo
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do Random Forest: {accuracy * 100:.2f}%")

    # Retornar a acurácia
    return accuracy

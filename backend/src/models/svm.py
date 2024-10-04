from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV, LeaveOneOut
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


def plot_confusion_matrix(y_true, y_pred, classes, save_path):
    """
    Plota e salva a matriz de confusão.

    Args:
        y_true (array-like): Verdadeiros rótulos.
        y_pred (array-like): Rótulos preditos pelo modelo.
        classes (list): Nomes das classes.
        save_path (str): Caminho onde a matriz de confusão será salva.
    """
    conf_matrix = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        conf_matrix,
        annot=True,
        cmap="Blues",
        xticklabels=classes,
        yticklabels=classes,
        cbar=False,
    )

    plt.xlabel("Predição")
    plt.ylabel("Real")
    plt.title("Matriz de Confusão")
    plt.tight_layout()

    plt.savefig(save_path)
    plt.close()


def train_and_test_svm(X_train, y_train, X_test, y_test):
    """
    Treina um modelo SVM com os dados fornecidos, realiza uma busca de hiperparâmetros
    utilizando GridSearchCV e LeaveOneOut, avalia o desempenho no conjunto de teste
    e salva uma matriz de confusão.

    Args:
        X_train (np.array): Conjunto de dados de treino contendo as características (features).
        y_train (np.array): Conjunto de rótulos de treino (autores).
        X_test (np.array): Conjunto de dados de teste contendo as características (features).
        y_test (np.array): Conjunto de rótulos de teste (autores).

    Returns:
        tuple: Retorna uma tupla contendo duas acurácias:
            - accuracy_svm: Acurácia do modelo SVM treinado sem otimização de hiperparâmetros.
            - accuracy_svm_grid_search: Acurácia do modelo SVM otimizado usando GridSearchCV.
    """
    # Treinar o modelo SVM sem otimização de hiperparâmetros
    svm_model = SVC()
    svm_model.fit(X_train, y_train)

    # Fazer previsões e calcular a acurácia
    y_pred = svm_model.predict(X_test)
    accuracy_svm = accuracy_score(y_test, y_pred)
    print(f"Acurácia do SVM: {accuracy_svm * 100:.2f}%")

    # Definir LeaveOneOut para validação cruzada
    cv = LeaveOneOut()

    # Definir o grid de parâmetros para múltiplos kernels
    param_grid = [
        {"kernel": ["linear"], "C": [0.1, 1, 10, 100]},
        {
            "kernel": ["poly"],
            "C": [0.1, 1, 10],
            "degree": [2, 3, 4],
            "gamma": ["scale", "auto"],
        },
        {"kernel": ["rbf"], "C": [0.1, 1, 10], "gamma": ["scale", "auto"]},
    ]

    # Realizar busca de hiperparâmetros usando GridSearchCV
    svm_model = GridSearchCV(SVC(), param_grid, cv=cv)

    # Treinar o modelo otimizado
    svm_model.fit(X_train, y_train)

    # Fazer previsões no conjunto de teste otimizado
    y_pred = svm_model.predict(X_test)

    # Avaliar a acurácia após a otimização dos hiperparâmetros
    accuracy_svm_grid_search = accuracy_score(y_test, y_pred)
    print(f"Acurácia do SVM Grid Search: {accuracy_svm_grid_search * 100:.2f}%")

    # Exibir os melhores parâmetros encontrados
    print(f"Melhores parâmetros: {svm_model.best_params_}")

    # Plotar e salvar a matriz de confusão
    save_path = "../confusion_matrix.png"
    plot_confusion_matrix(
        y_test, y_pred, classes=svm_model.classes_, save_path=save_path
    )

    return accuracy_svm, accuracy_svm_grid_search

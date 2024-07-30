import io
import cv2
import numpy as np
from PIL import Image

def normaliza_histograma(vetangulo):
    """
    Normaliza o histograma de ângulos.

    Args:
      vetangulo: Vetor com a contagem de ângulos.

    Returns:
      vetangulonormal: Vetor com a distribuição de ângulos normalizada.
    """

    vetangulonormal = np.zeros(17)
    x = np.sum(vetangulo)
    for cont in range(17):
        vetangulonormal[cont] = vetangulo[cont] / x
    return vetangulonormal

def elemento_estruturante_cinco(img):
    """
    Calcula o histograma de ângulos de inclinação da escrita usando um elemento estruturante 5x5.

    Args:
      img: Imagem binarizada.

    Returns:
      vetangulo: Vetor com a contagem de ângulos.
    """

    vetangulo = np.zeros(17, dtype=int)
    h, w = img.shape
    for i in range(4, h):
        for j in range(4, w - 4):
            pixcentral = img[i, j]
            if pixcentral == 0:
                # Posição 0
                if (img[i, j + 1] == 0) and (img[i, j + 2] == 0) and (img[i, j + 3] == 0) and (img[i, j + 4] == 0):
                    vetangulo[0] += 1
                # Posição 1
                if (img[i, j + 1] == 0) and (img[i - 1, j + 2] == 0) and (img[i - 1, j + 3] == 0) and (img[i - 1, j + 4] == 0):
                    vetangulo[1] += 1
                # Posição 2
                if (img[i - 1, j + 1] == 0) and (img[i - 1, j + 2] == 0) and (img[i - 2, j + 3] == 0) and (img[i - 2, j + 4] == 0):
                    vetangulo[2] += 1
                # Posição 3
                if (img[i - 1, j + 1] == 0) and (img[i - 2, j + 2] == 0) and (img[i - 2, j + 3] == 0) and (img[i - 3, j + 4] == 0):
                    vetangulo[3] += 1
                # Posição 4
                if (img[i - 1, j + 1] == 0) and (img[i - 2, j + 2] == 0) and (img[i - 3, j + 3] == 0) and (img[i - 4, j + 4] == 0):
                    vetangulo[4] += 1
                # Posição 5
                if (img[i - 1, j + 1] == 0) and (img[i - 2, j + 2] == 0) and (img[i - 3, j + 2] == 0) and (img[i - 4, j + 3] == 0):
                    vetangulo[5] += 1
                # Posição 6
                if (img[i - 1, j + 1] == 0) and (img[i - 2, j + 1] == 0) and (img[i - 3, j + 2] == 0) and (img[i - 4, j + 2] == 0):
                    vetangulo[6] += 1
                # Posição 7
                if (img[i - 1, j] == 0) and (img[i - 2, j + 1] == 0) and (img[i - 3, j + 1] == 0) and (img[i - 4, j + 1] == 0):
                    vetangulo[7] += 1
                # Posição 8
                if (img[i - 1, j] == 0) and (img[i - 2, j] == 0) and (img[i - 3, j] == 0) and (img[i - 4, j] == 0):
                    vetangulo[8] += 1
                # Posição 9
                if (img[i - 1, j] == 0) and (img[i - 2, j - 1] == 0) and (img[i - 3, j - 1] == 0) and (img[i - 4, j - 1] == 0):
                    vetangulo[9] += 1
                # Posição 10
                if (img[i - 1, j - 1] == 0) and (img[i - 2, j - 1] == 0) and (img[i - 3, j - 2] == 0) and (img[i - 4, j - 2] == 0):
                    vetangulo[10] += 1
                # Posição 11
                if (img[i - 1, j - 1] == 0) and (img[i - 2, j - 2] == 0) and (img[i - 3, j - 3] == 0) and (img[i - 4, j - 3] == 0):
                    vetangulo[11] += 1
                # Posição 12
                if (img[i - 1, j - 1] == 0) and (img[i - 2, j - 2] == 0) and (img[i - 3, j - 3] == 0) and (img[i - 4, j - 4] == 0):
                    vetangulo[12] += 1
                # Posição 13
                if (img[i - 1, j - 1] == 0) and (img[i - 2, j - 2] == 0) and (img[i - 3, j - 2] == 0) and (img[i - 4, j - 3] == 0):
                    vetangulo[13] += 1
                # Posição 14
                if (img[i - 1, j - 1] == 0) and (img[i - 2, j - 1] == 0) and (img[i - 3, j - 2] == 0) and (img[i - 4, j - 2] == 0):
                    vetangulo[14] += 1
                # Posição 15
                if (img[i - 1, j] == 0) and (img[i - 2, j - 1] == 0) and (img[i - 3, j - 1] == 0) and (img[i - 4, j - 1] == 0):
                    vetangulo[15] += 1
                # Posição 16
                if (img[i, j - 1] == 0) and (img[i, j - 2] == 0) and (img[i, j - 3] == 0) and (img[i, j - 4] == 0):
                    vetangulo[16] += 1

    return vetangulo

def slant(image_data):
    """
    Processa uma única imagem e retorna o vetor de características.

    Args:
        image_data: Dados da imagem no formato bytes.

    Returns:
        list: Vetor de características (histograma de 17 posições normalizado).
    """
    
    print("Processando imagem...")
    
    # Converte os dados da imagem para um objeto PIL Image
    img = Image.open(io.BytesIO(image_data)).convert('L')  # Converte para escala de cinza

    # Converte o objeto PIL Image para um array NumPy
    img = np.array(img)

    # Binariza a imagem
    _, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Calcula o histograma de 17 posições
    histograma = elemento_estruturante_cinco(img_bin)

    # Normaliza o histograma
    vetor_caracteristicas = normaliza_histograma(histograma)

    return vetor_caracteristicas.tolist()  # Converte para lista para ser serializável pelo FastAPI
  

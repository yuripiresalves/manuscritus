import time
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
    Calcula o histograma de ângulos de inclinação da escrita usando um elemento estruturante 5x5
    e desenha marcações na imagem para destacar as áreas de interesse.

    Args:
      img: Imagem binarizada.

    Returns:
      tuple: Vetor com a contagem de ângulos e a imagem com as marcações.
    """

    vetangulo = np.zeros(17, dtype=int)
    h, w = img.shape
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for i in range(4, h):
        for j in range(4, w - 4):
            pixcentral = img[i, j]
            if pixcentral == 0:
                # Posição 0
                if (img[i, j + 1] == 0) and (img[i, j + 2] == 0) and (img[i, j + 3] == 0) and (img[i, j + 4] == 0):
                    vetangulo[0] += 1
                    cv2.rectangle(img_color, (j, i), (j + 4, i), (0, 255, 0), 1)
                # Posição 1
                if (img[i, j + 1] == 0) and (img[i - 1, j + 2] == 0) and (img[i - 1, j + 3] == 0) and (img[i - 1, j + 4] == 0):
                    vetangulo[1] += 1
                    cv2.line(img_color, (j, i), (j + 4, i - 4), (255, 0, 0), 1)
                # Posição 2
                if (img[i - 1, j + 1] == 0) and (img[i - 1, j + 2] == 0) and (img[i - 2, j + 3] == 0) and (img[i - 2, j + 4] == 0):
                    vetangulo[2] += 1
                    cv2.line(img_color, (j, i), (j + 4, i - 4), (255, 0, 0), 1)
                # Posição 3
                if (img[i - 1, j + 1] == 0) and (img[i - 2, j + 2] == 0) and (img[i - 2, j + 3] == 0) and (img[i - 3, j + 4] == 0):
                    vetangulo[3] += 1
                    cv2.line(img_color, (j, i), (j + 4, i - 4), (255, 0, 0), 1)
                # Posição 4
                if (img[i - 1, j + 1] == 0) and (img[i - 2, j + 2] == 0) and (img[i - 3, j + 3] == 0) and (img[i - 4, j + 4] == 0):
                    vetangulo[4] += 1
                    cv2.line(img_color, (j, i), (j + 4, i - 4), (255, 0, 0), 1)
                # Posição 5
                if (img[i - 1, j + 1] == 0) and (img[i - 2, j + 2] == 0) and (img[i - 3, j + 2] == 0) and (img[i - 4, j + 3] == 0):
                    vetangulo[5] += 1
                    cv2.line(img_color, (j, i), (j + 4, i - 4), (255, 0, 0), 1)
                # Posição 6
                if (img[i - 1, j + 1] == 0) and (img[i - 2, j + 1] == 0) and (img[i - 3, j + 2] == 0) and (img[i - 4, j + 2] == 0):
                    vetangulo[6] += 1
                    cv2.line(img_color, (j, i), (j + 4, i - 4), (255, 0, 0), 1)
                # Posição 7
                if (img[i - 1, j] == 0) and (img[i - 2, j + 1] == 0) and (img[i - 3, j + 1] == 0) and (img[i - 4, j + 1] == 0):
                    vetangulo[7] += 1
                    cv2.line(img_color, (j, i), (j + 4, i - 4), (255, 0, 0), 1)
                # Posição 8
                if (img[i - 1, j] == 0) and (img[i - 2, j] == 0) and (img[i - 3, j] == 0) and (img[i - 4, j] == 0):
                    vetangulo[8] += 1
                    cv2.rectangle(img_color, (j - 4, i - 4), (j, i), (0, 255, 0), 1)
                # Posição 9
                if (img[i - 1, j] == 0) and (img[i - 2, j - 1] == 0) and (img[i - 3, j - 1] == 0) and (img[i - 4, j - 1] == 0):
                    vetangulo[9] += 1
                    cv2.line(img_color, (j, i), (j - 4, i - 4), (255, 0, 0), 1)
                # Posição 10
                if (img[i - 1, j - 1] == 0) and (img[i - 2, j - 1] == 0) and (img[i - 3, j - 2] == 0) and (img[i - 4, j - 2] == 0):
                    vetangulo[10] += 1
                    cv2.line(img_color, (j, i), (j - 4, i - 4), (255, 0, 0), 1)
                # Posição 11
                if (img[i - 1, j - 1] == 0) and (img[i - 2, j - 2] == 0) and (img[i - 3, j - 3] == 0) and (img[i - 4, j - 3] == 0):
                    vetangulo[11] += 1
                    cv2.line(img_color, (j, i), (j - 4, i - 4), (255, 0, 0), 1)
                # Posição 12
                if (img[i - 1, j - 1] == 0) and (img[i - 2, j - 2] == 0) and (img[i - 3, j - 3] == 0) and (img[i - 4, j - 4] == 0):
                    vetangulo[12] += 1
                    cv2.line(img_color, (j, i), (j - 4, i - 4), (255, 0, 0), 1)
                # Posição 13
                if (img[i - 1, j - 1] == 0) and (img[i - 2, j - 2] == 0) and (img[i - 3, j - 2] == 0) and (img[i - 4, j - 3] == 0):
                    vetangulo[13] += 1
                    cv2.line(img_color, (j, i), (j - 4, i - 4), (255, 0, 0), 1)
                # Posição 14
                if (img[i - 1, j - 1] == 0) and (img[i - 2, j - 1] == 0) and (img[i - 3, j - 2] == 0) and (img[i - 4, j - 2] == 0):
                    vetangulo[14] += 1
                    cv2.line(img_color, (j, i), (j - 4, i - 4), (255, 0, 0), 1)
                # Posição 15
                if (img[i - 1, j] == 0) and (img[i - 2, j - 1] == 0) and (img[i - 3, j - 1] == 0) and (img[i - 4, j - 1] == 0):
                    vetangulo[15] += 1
                    cv2.line(img_color, (j, i), (j - 4, i - 4), (255, 0, 0), 1)
                # Posição 16
                if (img[i - 1, j] == 0) and (img[i - 2, j] == 0) and (img[i - 3, j] == 0) and (img[i - 4, j] == 0):
                    vetangulo[16] += 1
                    cv2.rectangle(img_color, (j, i - 4), (j + 4, i), (0, 255, 0), 1)

    return vetangulo, img_color

def slant(image_data):
    """
    Processa uma única imagem e retorna o vetor de características.

    Args:
        image_data: Dados da imagem no formato bytes.

    Returns:
        list: Vetor de características (histograma de 17 posições normalizado).
    """
    
    print("Processando imagem...")
       
    file_bytes = np.frombuffer(image_data, dtype=np.uint8)
    
    img_original = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

    img_suavizada = cv2.medianBlur(img_original, 5)

    img_bin = cv2.adaptiveThreshold(img_suavizada, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    millis = int(round(time.time() * 1000))
    cv2.imwrite(f"img_bin_{millis}.png", img_bin)    
    
    histograma, img_annotated = elemento_estruturante_cinco(img_bin)

    vetor_caracteristicas = normaliza_histograma(histograma)

    img_annotated = Image.fromarray(cv2.cvtColor(img_annotated, cv2.COLOR_BGR2RGB))

    millis = int(round(time.time() * 1000))
    img_annotated.save(f"imagem_anotada_{millis}.png")
    
    print(vetor_caracteristicas.tolist()) 
    
    print("Imagem processada.") 

    return vetor_caracteristicas.tolist()
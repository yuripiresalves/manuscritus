import os
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

def normalize_histogram(angle_vector):
    """
    Normaliza o histograma de ângulos utilizando a técnica min-max.

    Args:
      angle_vector: Vetor com a contagem de ângulos.

    Returns:
      normalized_angle_vector: Vetor com a distribuição de ângulos normalizada.
    """
    
    # Encontra o valor mínimo e máximo do vetor
    min_val = np.min(angle_vector)
    max_val = np.max(angle_vector)
    
    # Aplica a normalização min-max
    normalized_angle_vector = (angle_vector - min_val) / (max_val - min_val)

    return normalized_angle_vector

def slant(fragment, filename, output_dir, fragment_index=1):
    """
    Extrai a inclinação axial de um fragmento utilizando a técnica de 
    distribuição de borda direcional.

    Args:
        fragment (numpy.ndarray): Fragmento da imagem com as bordas da escrita.
        output_dir (str): Diretório para salvar as imagens.
        fragment_index (int): Índice do fragmento.

    Returns:
        numpy.ndarray: Vetor de características da inclinação axial.
    """
    output_dir = f"{output_dir}/{filename[:-4]}/histograms"
    os.makedirs(output_dir, exist_ok=True)
    
    height, width = fragment.shape
    
    # Inicializa o vetor de características com 17 posições
    axial_slant = np.zeros(17, dtype=int)
    
    # Itera sobre os pixels do fragmento, considerando o elemento estruturante 5x5
    for i in range(4, height - 4):
        for j in range(4, width - 4):
            central_pixel = fragment[i, j]
            if central_pixel == 0:
                if (fragment[i, j + 1] == 0) and (fragment[i, j + 2] == 0) and (fragment[i, j + 3] == 0) and (fragment[i, j + 4] == 0):
                    axial_slant[16] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-2, j + 2] == 0) and (fragment[i-3, j + 3] == 0) and (fragment[i-4, j + 4] == 0):
                    axial_slant[15] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-1, j + 2] == 0) and (fragment[i-2, j + 3] == 0) and (fragment[i-2, j + 4] == 0):
                    axial_slant[14] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-2, j + 2] == 0) and (fragment[i-2, j + 3] == 0) and (fragment[i-3, j + 4] == 0):
                    axial_slant[13] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-2, j + 2] == 0) and (fragment[i-3, j + 3] == 0) and (fragment[i-4, j + 4] == 0):
                    axial_slant[12] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-2, j + 2] == 0) and (fragment[i-3, j + 2] == 0) and (fragment[i-4, j + 3] == 0):
                    axial_slant[11] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-2, j + 1] == 0) and (fragment[i-3, j + 2] == 0) and (fragment[i-4, j + 2] == 0):
                    axial_slant[10] += 1
                if (fragment[i-1, j] == 0) and (fragment[i-2, j + 1] == 0) and (fragment[i-3, j + 1] == 0) and (fragment[i-4, j + 1] == 0):
                    axial_slant[9] += 1
                if (fragment[i-1, j] == 0) and (fragment[i-2, j] == 0) and (fragment[i-3, j] == 0) and (fragment[i-4, j] == 0):
                    axial_slant[8] += 1
                if (fragment[i-1, j] == 0) and (fragment[i-2, j - 1] == 0) and (fragment[i-3, j - 1] == 0) and (fragment[i-4, j - 1] == 0):
                    axial_slant[7] += 1
                if (fragment[i-1, j - 1] == 0) and (fragment[i-2, j - 1] == 0) and (fragment[i-3, j - 2] == 0) and (fragment[i-4, j - 2] == 0):
                    axial_slant[6] += 1
                if (fragment[i-1, j - 1] == 0) and (fragment[i-2, j - 2] == 0) and (fragment[i-3, j - 3] == 0) and (fragment[i-4, j - 3] == 0):
                    axial_slant[5] += 1
                if (fragment[i-1, j - 1] == 0) and (fragment[i-2, j - 2] == 0) and (fragment[i-3, j - 3] == 0) and (fragment[i-4, j - 4] == 0):
                    axial_slant[4] += 1
                if (fragment[i-1, j - 1] == 0) and (fragment[i-2, j - 2] == 0) and (fragment[i-3, j - 2] == 0) and (fragment[i-4, j - 3] == 0):
                    axial_slant[3] += 1
                if (fragment[i-1, j - 1] == 0) and (fragment[i-2, j - 1] == 0) and (fragment[i-3, j - 2] == 0) and (fragment[i-4, j - 2] == 0):
                    axial_slant[2] += 1
                if (fragment[i-1, j] == 0) and (fragment[i-2, j - 1] == 0) and (fragment[i-3, j - 1] == 0) and (fragment[i-4, j - 1] == 0):
                    axial_slant[1] += 1
                if (fragment[i, j - 1] == 0) and (fragment[i, j - 2] == 0) and (fragment[i, j - 3] == 0) and (fragment[i, j - 4] == 0):
                    axial_slant[0] += 1
                

    # Normaliza o vetor de características
    axial_slant = normalize_histogram(axial_slant)

    # Gera e salva o histograma da inclinação axial
    angles = np.linspace(0, 180, 17, endpoint=False)
    plt.bar(angles, axial_slant)
    plt.xlabel("Ângulo (graus)")
    plt.ylabel("Frequência")
    plt.title(f"Histograma da Inclinação Axial - Fragment {fragment_index}")
    plt.xlim(0, 180)
    plt.savefig(os.path.join(output_dir, f"8_histograma_fragmento_{fragment_index}.png"))
    plt.clf()

    return axial_slant

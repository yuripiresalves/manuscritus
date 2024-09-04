import cv2
import numpy as np
import os
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import csv

def preprocess_image(image_path, filename, output_dir):
    """
    Pré-processa a imagem do manuscrito e salva as imagens intermediárias.

    Args:
        image_path (str): Caminho para a imagem do manuscrito.
        output_dir (str): Diretório para salvar as imagens.
    Returns:
        numpy.ndarray: Imagem pré-processada (bordas da escrita).
    """
    output_dir = f"{output_dir}/{filename[:-4]}"
    os.makedirs(output_dir, exist_ok=True)

    # Carrega a imagem em escala de cinza
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(os.path.join(output_dir, "1_grayscale.png"), img)

    # Binariza a imagem usando o método de Abutaleb
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite(os.path.join(output_dir, "2_binarizada.png"), thresh)

    # Cria uma máscara com a escrita em branco e o fundo em preto (NOVO)
    mask = thresh.copy()

    # Aplica dilatação e erosão apenas na máscara (NOVO)
    kernel = np.ones((5, 5), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel, iterations=1)
    cv2.imwrite(os.path.join(output_dir, "3_dilatada.png"), dilated_mask)

    eroded_mask = cv2.erode(mask, kernel, iterations=1)
    cv2.imwrite(os.path.join(output_dir, "4_erodida.png"), eroded_mask)
    edges_mask = dilated_mask - eroded_mask

    # Combina as bordas da máscara com a imagem binarizada original (NOVO)
    edges = cv2.bitwise_and(thresh, edges_mask)
    cv2.imwrite(os.path.join(output_dir, "5_bordas.png"), edges)

    return edges

def segment_image(image, filename, output_dir):
    """
    Segmenta a imagem em 24 fragmentos e salva as imagens dos fragmentos e da imagem
    com linhas de segmentação.

    Args:
        image (numpy.ndarray): Imagem pré-processada (bordas).
        output_dir (str): Diretório para salvar as imagens.

    Returns:
        list: Lista de fragmentos da imagem.
    """
    output_dir = f"{output_dir}/{filename[:-4]}"
    fragments_output_dir = f"{output_dir}/fragmentos"
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(fragments_output_dir, exist_ok=True)
    
    
    # Divide a imagem em fragmentos
    height, width = image.shape
    fragment_height = height // 6
    fragment_width = width // 4
    fragments = []

    # Imagem com linhas de segmentação
    segmented_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Converte para colorida para as linhas
    for i in range(6):
        cv2.line(segmented_image, (0, i*fragment_height), (width, i*fragment_height), (255, 255, 255), 2)  # Linhas horizontais
        for j in range(4):
            fragment = image[i*fragment_height:(i+1)*fragment_height, j*fragment_width:(j+1)*fragment_width]
            fragments.append(fragment)
            cv2.imwrite(os.path.join(fragments_output_dir, f"7_fragmento_{i}_{j}.png"), fragment)
            cv2.line(segmented_image, (j*fragment_width, 0), (j*fragment_width, height), (255, 255, 255), 2)  # Linhas verticais

    cv2.imwrite(os.path.join(output_dir, "6_segmentacao.png"), segmented_image)

    # Descarta fragmentos com pouca informação (CORRIGIDO)
    filtered_fragments = []
    for fragment in fragments:
        black_pixels = np.sum(fragment == 0)
        white_pixels = np.sum(fragment == 255)  # Adiciona contagem de pixels brancos
        total_pixels = fragment.size
        # Verifica se há mais de 1% de pixels pretos e mais de 1% de pixels brancos
        if black_pixels > 0.01 * total_pixels and white_pixels > 0.01 * total_pixels:
            filtered_fragments.append(fragment)
        

    # Seleciona 3 fragmentos de forma aleatória (NOVO)
    np.random.shuffle(filtered_fragments)
    random_fragments = filtered_fragments[:3]
    for i, fragment in enumerate(random_fragments):
        cv2.imwrite(os.path.join(fragments_output_dir, f"8_fragmento_{i}_aleatorio.png"), fragment)

    return random_fragments

def normaliza_histograma(vetangulo):
    """
    Normaliza o histograma de ângulos utilizando a técnica min-max.

    Args:
      vetangulo: Vetor com a contagem de ângulos.

    Returns:
      vetangulonormal: Vetor com a distribuição de ângulos normalizada.
    """
    
    # Encontra o valor mínimo e máximo do vetor
    min_val = np.min(vetangulo)
    max_val = np.max(vetangulo)
    
    # Aplica a normalização min-max
    vetangulonormal = (vetangulo - min_val) / (max_val - min_val)

    return vetangulonormal

def extract_axial_inclination(fragment, filename, output_dir, fragment_index=1):
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
    output_dir = f"{output_dir}/{filename[:-4]}/histogramas"
    os.makedirs(output_dir, exist_ok=True)
    
    height, width = fragment.shape
    
    # Inicializa o vetor de características com 17 posições
    inclinacao_axial = np.zeros(17, dtype=int)
    
    # Itera sobre os pixels do fragmento, considerando o elemento estruturante 5x5
    for i in range(4, height - 4):
        for j in range(4, width - 4):
            pixcentral = fragment[i, j]
            if pixcentral == 0:
                if (fragment[i, j + 1] == 0) and (fragment[i, j + 2] == 0) and (fragment[i, j + 3] == 0) and (fragment[i, j + 4] == 0):
                    inclinacao_axial[16] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-2, j + 2] == 0) and (fragment[i-3, j + 3] == 0) and (fragment[i-4, j + 4] == 0):
                    inclinacao_axial[15] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-1, j + 2] == 0) and (fragment[i-2, j + 3] == 0) and (fragment[i-2, j + 4] == 0):
                    inclinacao_axial[14] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-2, j + 2] == 0) and (fragment[i-2, j + 3] == 0) and (fragment[i-3, j + 4] == 0):
                    inclinacao_axial[13] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-2, j + 2] == 0) and (fragment[i-3, j + 3] == 0) and (fragment[i-4, j + 4] == 0):
                    inclinacao_axial[12] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-2, j + 2] == 0) and (fragment[i-3, j + 2] == 0) and (fragment[i-4, j + 3] == 0):
                    inclinacao_axial[11] += 1
                if (fragment[i-1, j + 1] == 0) and (fragment[i-2, j + 1] == 0) and (fragment[i-3, j + 2] == 0) and (fragment[i-4, j + 2] == 0):
                    inclinacao_axial[10] += 1
                if (fragment[i-1, j] == 0) and (fragment[i-2, j + 1] == 0) and (fragment[i-3, j + 1] == 0) and (fragment[i-4, j + 1] == 0):
                    inclinacao_axial[9] += 1
                if (fragment[i-1, j] == 0) and (fragment[i-2, j] == 0) and (fragment[i-3, j] == 0) and (fragment[i-4, j] == 0):
                    inclinacao_axial[8] += 1
                if (fragment[i-1, j] == 0) and (fragment[i-2, j - 1] == 0) and (fragment[i-3, j - 1] == 0) and (fragment[i-4, j - 1] == 0):
                    inclinacao_axial[7] += 1
                if (fragment[i-1, j - 1] == 0) and (fragment[i-2, j - 1] == 0) and (fragment[i-3, j - 2] == 0) and (fragment[i-4, j - 2] == 0):
                    inclinacao_axial[6] += 1
                if (fragment[i-1, j - 1] == 0) and (fragment[i-2, j - 2] == 0) and (fragment[i-3, j - 3] == 0) and (fragment[i-4, j - 3] == 0):
                    inclinacao_axial[5] += 1
                if (fragment[i-1, j - 1] == 0) and (fragment[i-2, j - 2] == 0) and (fragment[i-3, j - 3] == 0) and (fragment[i-4, j - 4] == 0):
                    inclinacao_axial[4] += 1
                if (fragment[i-1, j - 1] == 0) and (fragment[i-2, j - 2] == 0) and (fragment[i-3, j - 2] == 0) and (fragment[i-4, j - 3] == 0):
                    inclinacao_axial[3] += 1
                if (fragment[i-1, j - 1] == 0) and (fragment[i-2, j - 1] == 0) and (fragment[i-3, j - 2] == 0) and (fragment[i-4, j - 2] == 0):
                    inclinacao_axial[2] += 1
                if (fragment[i-1, j] == 0) and (fragment[i-2, j - 1] == 0) and (fragment[i-3, j - 1] == 0) and (fragment[i-4, j - 1] == 0):
                    inclinacao_axial[1] += 1
                if (fragment[i, j - 1] == 0) and (fragment[i, j - 2] == 0) and (fragment[i, j - 3] == 0) and (fragment[i, j - 4] == 0):
                    inclinacao_axial[0] += 1
                

    # Normaliza o vetor de características
    inclinacao_axial = normaliza_histograma(inclinacao_axial)

    # Gera e salva o histograma da inclinação axial (opcional)
    angulos = np.linspace(0, 180, 17, endpoint=False)
    plt.bar(angulos, inclinacao_axial)
    plt.xlabel("Ângulo (graus)")
    plt.ylabel("Frequência")
    plt.title(f"Histograma da Inclinação Axial - Fragmento {fragment_index}")
    # plt.xticks(angulos)
    plt.xlim(0, 180)
    plt.savefig(os.path.join(output_dir, f"8_histograma_fragmento_{fragment_index}.png"))
    plt.clf()

    return inclinacao_axial

def process_dataset(dataset_dir, output_csv_path):
    """
    Processa um conjunto de dados de manuscritos, extraindo a inclinação axial
    de cada imagem e salvando os resultados em um arquivo CSV.

    Args:
        dataset_dir (str): Caminho para o diretório do conjunto de dados.
        output_csv_path (str): Caminho para o arquivo CSV de saída.
    """
    with open(output_csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['autor'] + [f'inclinacao_{i}' for i in range(17)])  # Cabeçalho do CSV

        if os.path.isdir(dataset_dir):
            for idx, filename in enumerate(sorted(os.listdir(dataset_dir))):
                # if dataset_dir == "/home/yuri/www/manuscritus/backend/training_manuscripts":
                #     if idx > 3:
                #         break
                # else:
                #     if idx > 1:
                #         break
                
                if filename.endswith(".bmp"):
                    image_path = os.path.join(dataset_dir, filename)
                    author_id = filename[-10:-7]
                    print(f"---------- Processando imagem: {filename} ----------")
                    preprocessed_image = preprocess_image(image_path, filename, "output_images")
                    fragments = segment_image(preprocessed_image, filename, "output_images")
                    for i, fragment in enumerate(fragments):
                        axial_inclination = extract_axial_inclination(fragment, filename, "output_images", i)
                        print(f"\nFragmento {i}:\n{axial_inclination}\n")
                        
                        csv_writer.writerow([f"a{author_id}"] + list(axial_inclination))

# Exemplo de uso:
train_dir = "/home/yuri/www/manuscritus/backend/training_manuscripts"  # Diretório das imagens de treino
test_dir = "/home/yuri/www/manuscritus/backend/test_manuscripts"  # Diretório das imagens de teste
train_csv_path = "treino.csv"
test_csv_path = "teste.csv"

process_dataset(train_dir, train_csv_path)
process_dataset(test_dir, test_csv_path)

print(f"Resultados do treino salvos em: {train_csv_path}")
print(f"Resultados do teste salvos em: {test_csv_path}")
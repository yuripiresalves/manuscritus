import os
import cv2
import csv
import numpy as np
from features.slant import slant

def preprocess_image(image_path, filename, output_dir):
    """
    Pré-processa a imagem do manuscrito e salva as imagens intermediárias.

    Args:
        image_path (str): Caminho para a imagem do manuscrito.
        filename (str): Nome do arquivo da imagem.
        output_dir (str): Diretório para salvar as imagens processadas.

    Returns:
        numpy.ndarray: Imagem pré-processada (bordas da escrita).
    """
    output_dir = f"{output_dir}/{filename[:-4]}"
    os.makedirs(output_dir, exist_ok=True)

    # Carrega a imagem em escala de cinza
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(os.path.join(output_dir, "1_grayscale.png"), img)

    # Binariza a imagem usando o método de Otsu
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite(os.path.join(output_dir, "2_binarizada.png"), thresh)

    # Aplica dilatação e erosão
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    cv2.imwrite(os.path.join(output_dir, "3_dilatada.png"), dilated)

    eroded = cv2.erode(thresh, kernel, iterations=1)
    cv2.imwrite(os.path.join(output_dir, "4_erodida.png"), eroded)
    edges = dilated - eroded

    # Combina as bordas da máscara com a imagem binarizada original
    edges = cv2.bitwise_and(thresh, edges)
    
    # Inverte a imagem para que o fundo fique branco e as bordas pretas
    inverted_edges = cv2.bitwise_not(edges)
    cv2.imwrite(os.path.join(output_dir, "5_bordas.png"), inverted_edges)

    return inverted_edges

# def segment_image(image, filename, output_dir):
#     """
#     Segmenta a imagem em 24 fragmentos e salva as imagens dos fragmentos e da imagem
#     com linhas de segmentação.

#     Args:
#         image (numpy.ndarray): Imagem pré-processada (bordas).
#         filename (str): Nome do arquivo da imagem.
#         output_dir (str): Diretório para salvar as imagens.

#     Returns:
#         list: Lista de fragmentos da imagem.
#     """
#     output_dir = f"{output_dir}/{filename[:-4]}"
#     fragments_output_dir = f"{output_dir}/fragmentos"
    
#     os.makedirs(output_dir, exist_ok=True)
#     os.makedirs(fragments_output_dir, exist_ok=True)
    
#     # Divide a imagem em fragmentos
#     height, width = image.shape
#     fragment_height = height // 6
#     fragment_width = width // 4
#     fragments = []

#     # Imagem com linhas de segmentação
#     segmented_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Converte para colorida para as linhas
#     for i in range(6):
#         cv2.line(segmented_image, (0, i*fragment_height), (width, i*fragment_height), (0, 0, 255), 2)  # Linhas horizontais
#         for j in range(4):
#             fragment = image[i*fragment_height:(i+1)*fragment_height, j*fragment_width:(j+1)*fragment_width]
#             fragments.append(fragment)
#             cv2.imwrite(os.path.join(fragments_output_dir, f"7_fragmento_{i}_{j}.png"), fragment)
#             cv2.line(segmented_image, (j*fragment_width, 0), (j*fragment_width, height), (0, 0, 255), 2)  # Linhas verticais

#     cv2.imwrite(os.path.join(output_dir, "6_segmentacao.png"), segmented_image)

#     # Descarta fragmentos com pouca informação
#     filtered_fragments = []
#     for fragment in fragments:
#         black_pixels = np.sum(fragment == 0)
#         white_pixels = np.sum(fragment == 255)  # Adiciona contagem de pixels brancos
#         total_pixels = fragment.size
#         # Verifica se há mais de 1% de pixels pretos e mais de 1% de pixels brancos
#         if black_pixels > 0.01 * total_pixels and white_pixels > 0.01 * total_pixels:
#             filtered_fragments.append(fragment)
        
#     # Seleciona 5 fragmentos de forma aleatória
#     np.random.shuffle(filtered_fragments)
#     random_fragments = filtered_fragments[:5]
#     for i, fragment in enumerate(random_fragments):
#         cv2.imwrite(os.path.join(fragments_output_dir, f"8_fragmento_{i}_aleatorio.png"), fragment)

#     return random_fragments

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
              if dataset_dir == train_dir:
                if idx > 3:
                  break
              else:
                if idx > 1:
                  break
                  
              if filename.endswith(".bmp"):
                  image_path = os.path.join(dataset_dir, filename)
                  author_id = filename[-10:-7]
                  print(f"---------- Processando imagem: {filename} ----------")
                  preprocessed_image = preprocess_image(image_path, filename, "output_images")
                  slant_result = slant(preprocessed_image, filename, "output_images")
                  csv_writer.writerow([f"a{author_id}"] + list(slant_result))

# Exemplo de uso:
train_dir = "/home/yuri/www/manuscritus/backend/training_manuscripts"  # Diretório das imagens de treino
test_dir = "/home/yuri/www/manuscritus/backend/test_manuscripts"  # Diretório das imagens de teste
train_csv_path = "treino.csv"
test_csv_path = "teste.csv"

process_dataset(train_dir, train_csv_path)
process_dataset(test_dir, test_csv_path)

print(f"Resultados do treino salvos em: {train_csv_path}")
print(f"Resultados do teste salvos em: {test_csv_path}")

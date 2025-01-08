# Manuscritus

Ferramenta para Identificação de Autoria de Manuscritos utilizando características grafométricas.

## Descrição do Projeto

Este projeto foi desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) apresentado à Universidade Estadual de Maringá (UEM). A ferramenta propõe um método computacional para identificar a autoria de manuscritos, utilizando técnicas de aprendizado de máquina e características grafométricas extraídas de cartas manuscritas.

## Funcionalidades

- **Pré-processamento de imagens:** Binarização, dilatação, erosão e extração de bordas.
- **Extração de características:** Foco na característica de inclinação axial para análise grafométrica.
- **Treinamento e avaliação de modelos:** Utilização de algoritmos SVM e Random Forest.
- **Interface web:** Permite configurações de parâmetros e visualização dos resultados.

## Tecnologias Utilizadas

### Backend:

- **Linguagem:** Python
- **Bibliotecas:**
  - OpenCV: Processamento de imagens.
  - Scikit-learn: Treinamento de modelos de aprendizado de máquina.
  - FastAPI: Criação da API para comunicação entre frontend e backend.

### Frontend:

- **Linguagem:** TypeScript
- **Frameworks:**
  - ReactJS: Construção da interface.
  - Next.js: Estruturação do frontend.

### Ferramentas Adicionais:

- Prototipação da interface com Figma.
- Organização de dados com arquivos CSV.

## Estrutura do Repositório

- `backend/`: Contém o código relacionado ao processamento de imagens, extração de características e treinamento dos modelos.
- `frontend/`: Inclui o código da interface web para interação com a ferramenta.

## Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- Pip
- Node.js 18 ou superior

### Configuração do Backend

1. Clone o repositório:
   ```bash
   git clone https://github.com/yuripiresalves/manuscritus.git
   ```
2. Acesse o diretório do backend:
   ```bash
   cd manuscritus/backend
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o servidor FastAPI:
   ```bash
   uvicorn src.server:app --reload
   ```

### Configuração do Frontend

1. Acesse o diretório do frontend:
   ```bash
   cd manuscritus/frontend
   ```
2. Crie um arquivo `.env` na raiz do projeto e adicione a seguinte variável de ambiente:
    ```bash
    NEXT_PUBLIC_API_URL="http://localhost:8000"
    ```
3. Instale as dependências:
   ```bash
   npm install
   ```
4. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

### Uso da Ferramenta

1. Acesse a interface web no navegador, disponível em `http://localhost:3000`.
2. Configure os parâmetros desejados, como número de autores e algoritmos de classificação.
3. Execute os experimentos e visualize os resultados.

## Resultados dos Experimentos

Os experimentos realizados mostraram que o SVM otimizado por Grid Search apresentou o melhor desempenho, com acurácia de até 95% para conjuntos menores de autores. Mais detalhes podem ser encontrados na seção de resultados do TCC.

## Autor

**Yuri Pires Alves**  
Orientadora: Profª. Drª. Aline Maria Malachini Miotto Amaral

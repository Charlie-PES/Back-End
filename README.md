# Back-End

Este é um projeto de back-end utilizando **FastAPI** e **Uvicorn**.

## Pré-requisitos

Certifique-se de ter o seguinte instalado em sua máquina:

- Python 3.8 ou superior
- Gerenciador de pacotes `pip`

## Instalação

1. Clone este repositório:

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd charlie-backend
   ```
2. Crie um ambiente virtual (opcional, mas recomendado):

   **python3** **-m** **venv** **venv**

   **source** **venv/bin/activate**  **# No Windows: venv\Scripts\activate**
3. Instale as dependências:

   **pip** **install** **-r** **requirements.txt**

## Executando o Servidor

1. Navegue até o diretório `src/charlie-backend`:

   **cd** **src/charlie-backend**
2. Inicie o servidor FastAPI com o Uvicorn:

   **python** **main.py**
3. O servidor estará disponível em: [http://127.0.0.1:8080](vscode-file://vscode-app/Applications/Visual%20Studio%20Code.app/Contents/Resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)

## Endpoints Disponíveis

* **GET /** : Retorna uma mensagem de boas-vindas.
* **GET /v1/test** : Retorna uma mensagem de teste.

## Testando os Endpoints

Você pode testar os endpoints utilizando o arquivo `request.rest` com a extensão [REST Client](vscode-file://vscode-app/Applications/Visual%20Studio%20Code.app/Contents/Resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) no VS Code. Basta abrir o arquivo e clicar em "Send Request" nos endpoints.

## Contribuição

Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias.

## Licença

Este projeto está sob a licença [MIT](vscode-file://vscode-app/Applications/Visual%20Studio%20Code.app/Contents/Resources/app/out/vs/code/electron-sandbox/workbench/workbench.html).

**Substitua `<URL_DO_REPOSITORIO>` pelo link do **repositório Git, caso aplicável.

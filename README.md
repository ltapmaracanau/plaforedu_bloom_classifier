# API de Classificação de Cursos
Este é um modelo de API de classificação de cursos, que retorna as probabilidades para cada classe da taxonomia de Bloom.

## Instalação
Antes de usar a API, você precisará instalar as dependências. Para isso, você pode usar o seguinte comando no terminal:

```bash
pip install -r requirements.txt
```

Alternativamente, você pode construir e rodar a aplicação usando Docker. Para isso, utilize os comandos disponíveis no Makefile:

```bash
make build # Constrói a imagem Docker
make run # Inicia a aplicação em um container Docker
```

## Execução
Para iniciar a API, execute:

```bash
python api.py
```

Se estiver usando Docker, após construir a imagem, você pode iniciar a API com:

```bash
make run
```

## Endpoint
A API possui apenas um endpoint, o POST /predict, que recebe um corpo com um campo chamado `description`. Este campo representa a descrição de um curso. A resposta da API é um JSON com as probabilidades para cada uma das 6 classes da taxonomia de Bloom.

Exemplo de requisição:

```bash
curl -X POST \
  http://localhost:5000/predict \
  -H 'Content-Type: application/json' \
  -d '{"description": "Este é um curso sobre inteligência artificial."}'
```

Exemplo de resposta:

```json
{
    "Analisar": 0.05,
    "Aplicar": 0.10,
    "Compreender": 0.20,
    "Criar": 0.30,
    "Avaliar": 0.25,
    "Lembrar": 0.10
}
```

## Comandos Docker (via Makefile)
Além de iniciar a API com `make run`, você pode utilizar os seguintes comandos disponíveis no Makefile:

- `make build`: Constrói a imagem Docker da API.
- `make stop`: Para o container Docker que está rodando a API.
- `make clean`: Remove o container Docker que rodava a API.
- `make logs`: Exibe os logs do container Docker da API.

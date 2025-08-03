master_transformers
==============================

This project is study and experimentations for master

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>


uvicorn app.main:app --reload para rodar
---


#  Uber Sim API — Simulador de Corridas em Tempo Real

Simulador de mobilidade urbana estilo Uber, com:
- WebSocket de movimentação
- Cálculo de distâncias e tempos
- Integração com Redis
- Foco geográfico na Grande Vitória (ES)

---

##  Requisitos

- Python 3.10+
- Redis (via Docker)
- Node.js (opcional, para usar `wscat`)
- Docker (opcional, mas recomendado)

---

##  Instalação

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/uber-sim-api.git
cd uber-sim-api
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
venv\\Scripts\\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

##  Rodar Redis com Docker

```bash
docker run -d --name redis -p 6379:6379 redis
```

---

## Rodar a API

Na raiz do projeto:

```bash
uvicorn app.main:app --reload
```

Acesse:
- Swagger UI: http://localhost:8000/docs

---

## 🧪 Testar o WebSocket

Instale `wscat` (se ainda não tiver):

```bash
npm install -g wscat
```

Conecte:

```bash
wscat -c "ws://localhost:8000/ws/motorista/teste123?lat_origem=-20.315&lon_origem=-40.305&lat_destino=-20.320&lon_destino=-40.295"
```

---

## 🔁 Simular Jornada Completa

```http
POST /corrida/jornada
```

Payload:

```json
{
  "motorista_id": "teste123",
  "posicao_motorista": [-20.312, -40.310],
  "origem_cliente": [-20.315, -40.305],
  "destino_cliente": [-20.320, -40.295]
}
```

Isso registra no Redis:
- Distância e tempo de pickup
- Da viagem
- Do retorno
- Status da jornada

---

## 🗂️ Histórico

Consultar histórico de jornadas:
```http
GET /corrida/historico/{user_id}
```

---

##  Área de cobertura

Todas as simulações são geograficamente restritas à **Grande Vitória (ES)**:
- Vitória
- Vila Velha
- Serra
- Cariacica
- Viana

---

## Estrutura

```
uber-sim/
├── app/
│   ├── routers/
│   ├── services/
│   ├── websocket.py
│   └── main.py
├── requirements.txt
└── README.md
```

---

## Futuro

- Docker Compose com Redis + API
- Frontend com mapa em tempo real
- Suporte a múltiplos motoristas simultâneos


# Backend - Sistema de Compras Online

API REST construída com **FastAPI** e **SQLite**, utilizando SQLAlchemy como ORM e Alembic para migrations.

## 📋 Sobre

Este backend fornece uma API completa para gerenciar:
- **Produtos** e categorias
- **Pedidos** e itens de pedidos
- **Consumidores** (clientes)
- **Vendedores**
- **Avaliações** de pedidos
- **Proxy de imagens** para contornar CORS

## ✅ Requisitos

- **Python 3.11+**
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório)

## 🚀 Como Rodar

### 1️⃣ Criar e Ativar Ambiente Virtual

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**No macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

Isso instalará:
- **fastapi** - Framework web moderno
- **uvicorn** - Servidor ASGI
- **sqlalchemy** - ORM para banco de dados
- **alembic** - Versionamento de schema
- **pydantic** - Validação de dados
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **pytest** - Framework de testes
- **httpx** - Cliente HTTP

### 3️⃣ Configurar Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` na raiz do backend (opcional, usa SQLite por padrão):

```env
DATABASE_URL=sqlite:///./database.db
```

### 4️⃣ Inicializar o Banco de Dados

```bash
alembic upgrade head
```

Isso aplicará todas as migrations e criará as tabelas necessárias.

### 5️⃣ Rodar o Servidor

```bash
python -m uvicorn app.main:app --reload
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

O servidor estará disponível em **http://localhost:8000**

## 📚 Documentação da API

Após iniciar o servidor, acesse a documentação interativa gerada automaticamente:

- **Swagger UI**: http://localhost:8000/docs

Aqui você pode:
- Ver todos os endpoints disponíveis
- Testar os endpoints de forma interativa
- Ver os modelos de dados esperados

## 🔗 Endpoints Disponíveis

### Produtos
```
GET    /api/produtos             # Listar todos os produtos
POST   /api/produtos             # Criar novo produto
GET    /api/produtos/{id}        # Obter produto por ID
PUT    /api/produtos/{id}        # Atualizar produto
DELETE /api/produtos/{id}        # Deletar produto
```

### Pedidos
```
GET    /api/pedidos              # Listar todos os pedidos
POST   /api/pedidos              # Criar novo pedido
GET    /api/pedidos/{id}         # Obter pedido por ID
PUT    /api/pedidos/{id}         # Atualizar pedido
DELETE /api/pedidos/{id}         # Deletar pedido
```

### Consumidores
```
GET    /api/consumidores         # Listar todos os consumidores
POST   /api/consumidores         # Criar novo consumidor
GET    /api/consumidores/{id}    # Obter consumidor por ID
PUT    /api/consumidores/{id}    # Atualizar consumidor
DELETE /api/consumidores/{id}    # Deletar consumidor
```

### Vendedores
```
GET    /api/vendedores           # Listar todos os vendedores
POST   /api/vendedores           # Criar novo vendedor
GET    /api/vendedores/{id}      # Obter vendedor por ID
PUT    /api/vendedores/{id}      # Atualizar vendedor
DELETE /api/vendedores/{id}      # Deletar vendedor
```

### Itens de Pedido
```
GET    /api/itens-pedido         # Listar itens de pedido
POST   /api/itens-pedido         # Criar item de pedido
GET    /api/itens-pedido/{id}    # Obter item por ID
PUT    /api/itens-pedido/{id}    # Atualizar item
DELETE /api/itens-pedido/{id}    # Deletar item
```

### Avaliações
```
GET    /api/avaliacoes           # Listar avaliações
POST   /api/avaliacoes           # Criar nova avaliação
GET    /api/avaliacoes/{id}      # Obter avaliação por ID
PUT    /api/avaliacoes/{id}      # Atualizar avaliação
DELETE /api/avaliacoes/{id}      # Deletar avaliação
```

### Proxy de Imagens
```
GET    /images/proxy?url=...     # Fazer proxy de imagem de uma URL
```

## 🏗️ Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação FastAPI principal
│   ├── config.py               # Configurações (DATABASE_URL, etc)
│   ├── database.py             # Conexão e sessão do banco de dados
│   ├── models/                 # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── consumidor.py
│   │   ├── vendedor.py
│   │   ├── produto.py
│   │   ├── pedido.py
│   │   ├── item_pedido.py
│   │   └── avaliacao_pedido.py
│   ├── routers/                # Endpoints da API
│   │   ├── __init__.py
│   │   ├── consumidor_router.py
│   │   ├── vendedor_router.py
│   │   ├── produto_router.py
│   │   ├── pedido_routers.py
│   │   ├── item_pedido_router.py
│   │   └── avaliacao_pedido_router.py
│   ├── schema/                 # Schemas Pydantic (validação)
│   │   ├── __init__.py
│   │   ├── consumidor_schema.py
│   │   ├── vendedor_schema.py
│   │   ├── produto_schema.py
│   │   ├── pedido_schema.py
│   │   ├── item_pedido_schema.py
│   │   ├── avaliacao_pedido_schema.py
│   │   └── pagination_schema.py
│   ├── service/                # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── ingest.py           # Funções de importação de dados
│   │   └── utils.py            # Utilitários
│   └── data/                   # Dados CSV para seed
│       ├── dim_consumidores.csv
│       ├── dim_vendedores.csv
│       ├── dim_produtos.csv
│       ├── dim_categoria_imagens.csv
│       ├── fat_pedidos.csv
│       ├── fat_itens_pedidos.csv
│       └── fat_avaliacoes_pedidos.csv
├── alembic/                    # Controle de versão do banco
│   ├── env.py
│   ├── script.py.mako
│   └── versions/               # Scripts de migration
│       ├── 001_initial_schema.py
│       └── 002_add_imagem_and_media_to_pedidos.py
├── testes/                     # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_consumidor_router.py
│   ├── test_vendedor_router.py
│   ├── test_produto_router.py
│   ├── test_pedido_router.py
│   ├── test_item_pedido_router.py
│   └── test_avaliacao_pedido_router.py
├── requirements.txt            # Dependências Python
├── pytest.ini                  # Configuração do Pytest
├── alembic.ini                 # Configuração do Alembic
└── README.md                   # Este arquivo
```

## 🧪 Executar Testes

Para rodar todos os testes:

```bash
pytest
```

Para rodar testes de um arquivo específico:

```bash
pytest testes/test_produto_router.py -v
```

Para ver cobertura de testes:

```bash
pytest --cov=app
```

## 📊 Modelos de Dados

### Consumidor
- `id` - Identificador único
- `nome` - Nome do consumidor
- `email` - Email
- `cpf` - CPF
- `telefone` - Telefone
- `endereco` - Endereço

### Vendedor
- `id` - Identificador único
- `nome_vendedor` - Nome do vendedor
- `email_vendedor` - Email
- `telefone_vendedor` - Telefone
- `endereco_vendedor` - Endereço

### Produto
- `id` - Identificador único
- `nome_produto` - Nome
- `descricao` - Descrição
- `preco` - Preço
- `estoque` - Quantidade em estoque
- `categoria` - Categoria do produto
- `vendedor_id` - Referência ao vendedor
- `imagem_url` - URL da imagem
- `media_rating` - Avaliação média

### Pedido
- `id` - Identificador único
- `numero_pedido` - Número do pedido
- `data_pedido` - Data do pedido
- `consumidor_id` - Referência ao consumidor
- `status` - Status do pedido
- `valor_total` - Valor total
- `imagem` - Imagem do pedido (opcional)
- `media_imagem` - Mídia do pedido (opcional)

### Item Pedido
- `id` - Identificador único
- `pedido_id` - Referência ao pedido
- `produto_id` - Referência ao produto
- `quantidade` - Quantidade de itens
- `preco_unitario` - Preço unitário

### Avaliação Pedido
- `id` - Identificador único
- `pedido_id` - Referência ao pedido
- `nota` - Nota (0-5 estrelas)
- `comentario` - Comentário do cliente
- `data_avaliacao` - Data da avaliação

## 🔄 Trabalhar com Migrations

### Ver status das migrations
```bash
alembic current
```

### Criar nova migration
```bash
alembic revision --autogenerate -m "Descrição da mudança"
```

### Atualizar banco de dados
```bash
alembic upgrade head
```

### Reverter última migration
```bash
alembic downgrade -1
```

## 🔗 Voltar ao Projeto Principal

Veja [README Principal](../README.md) para instruções do projeto completo e documentação do frontend.

---

**Última atualização**: Abril 2026

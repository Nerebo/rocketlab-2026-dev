# Rocket Ship - Sistema de E-commerce

Um sistema completo de e-commerce desenvolvido com tecnologias modernas, oferecendo uma API robusta no backend e uma interface intuitiva no frontend.

## 📋 Sobre o Projeto

O **Rocket Ship** é um sistema de compras online que permite:

- **Gerenciamento de Produtos**: Cadastro, atualização e listagem de produtos com categorias
- **Gestão de Pedidos**: Criação, acompanhamento e pagamento de pedidos
- **Sistema de Consumidores**: Registro e autenticação de clientes
- **Avaliações e Feedback**: Clientes podem avaliar produtos e pedidos
- **Múltiplos Vendedores**: Suporte para vendedores independentes
- **Proxy de Imagens**: Sistema de proxy para contornar restrições CORS

## 🏗️ Arquitetura

O projeto é dividido em duas grandes partes:

### **Backend**
API REST construída com **FastAPI** e **SQLite**, utilizando:
- **SQLAlchemy**: ORM para interação com banco de dados
- **Alembic**: Controle de versão de schema do banco de dados
- **Pydantic**: Validação de dados e schemas
- **Pytest**: Testes automatizados

### **Frontend**
Interface web moderna construída com:
- **React 19** com TypeScript
- **Vite**: Build tool rápido para desenvolvimento
- **Tailwind CSS**: Utilitários de estilo
- **ESLint**: Análise estática de código

## 📁 Estrutura do Projeto

```
rocketlab-2026-dev/
├── backend/                          # API REST (FastAPI)
│   ├── app/
│   │   ├── main.py                  # Aplicação principal
│   │   ├── config.py                # Configurações
│   │   ├── database.py              # Configuração do banco de dados
│   │   ├── models/                  # Modelos SQLAlchemy
│   │   ├── routers/                 # Endpoints da API
│   │   ├── schema/                  # Schemas Pydantic
│   │   ├── service/                 # Lógica de negócio
│   │   └── data/                    # Dados CSV para seed
│   ├── alembic/                     # Migrations do banco de dados
│   ├── testes/                      # Testes automatizados
│   ├── requirements.txt             # Dependências Python
│   ├── pytest.ini                   # Configuração do Pytest
│   └── README.md                    # Documentação do backend
│
└── frontend/                         # Interface web (React)
    └── rocket_ecommerce/
        ├── src/
        │   ├── components/          # Componentes React reutilizáveis
        │   ├── services/            # Serviços de integração com API
        │   ├── App.tsx              # Componente principal
        │   └── main.tsx             # Entry point
        ├── public/                  # Arquivos estáticos
        ├── package.json             # Dependências Node.js
        ├── vite.config.ts           # Configuração do Vite
        ├── tailwind.config.js       # Configuração Tailwind CSS
        └── README.md                # Documentação do frontend
```

## 🚀 Como Comece

### Pré-requisitos

- **Python 3.11+** (para o backend)
- **Node.js 18+** e **pnpm** (para o frontend)

### Quick Start

**1. Clone ou extraia o projeto**

```bash
cd rocketlab-2026-dev
```

**2. Configure e inicie o Backend**

Veja [Backend README](./backend/README.md) para instruções detalhadas.

```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**3. Configure e inicie o Frontend**

Veja [Frontend README](./frontend/rocket_ecommerce/README.md) para instruções detalhadas.

```bash
cd frontend/rocket_ecommerce
pnpm install
pnpm run dev
```

## 📚 Documentação Completa

- **[Backend - Como Rodar](./backend/README.md)**: Instruções detalhadas para configuração, instalação e execução do backend
- **[Frontend - Como Rodar](./frontend/rocket_ecommerce/README.md)**: Instruções detalhadas para configuração, instalação e execução do frontend

## 🔗 Endpoints Principais da API

O backend disponibiliza os seguintes endpoints:

- **Produtos**: `/api/produtos` - Listar, criar, atualizar produtos
- **Pedidos**: `/api/pedidos` - Gerenciar pedidos
- **Consumidores**: `/api/consumidores` - Gerenciar usuários
- **Vendedores**: `/api/vendedores` - Gerenciar vendedores
- **Itens Pedido**: `/api/itens-pedido` - Gerenciar itens dos pedidos
- **Avaliações**: `/api/avaliacoes-pedido` - Adicionar avaliações
- **Proxy de Imagens**: `/images/proxy` - Fazer proxy de imagens

Para documentação interativa, acesse [http://localhost:8000/docs](http://localhost:8000/docs) após iniciar o backend.

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** 0.115.6
- **SQLAlchemy** 2.0.36
- **Alembic** 1.14.0
- **Pydantic** 2.10.3
- **Pytest** 8.3.4

### Frontend
- **React** 19.2.4
- **TypeScript** 6.0.2
- **Vite** 8.0.4
- **Tailwind CSS** 3.4.1

## 📝 Notas de Desenvolvimento

- O CORS está configurado para aceitar requisições de qualquer origem em desenvolvimento
- Em produção, configure a lista de domínios permitidos em `backend/app/main.py`
- O banco de dados utiliza SQLite por padrão
- Migrations são gerenciadas via Alembic na pasta `alembic/`

## 📄 Licença

Projeto desenvolvido para fins de aprendizado e desenvolvimento.

---

**Última atualização**: Abril 2026

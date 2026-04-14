# Frontend - Rocket E-commerce

Interface web moderna para o sistema de e-commerce, desenvolvida com **React 19**, **TypeScript** e **Tailwind CSS**.

## 📋 Sobre

Este frontend fornece uma interface completa para:
- **Listar e visualizar produtos** com categorias e imagens
- **Buscar produtos** por seu nome
- **Detalhes do produto** com informações completas
- **Integração com API** do backend

## ✅ Requisitos

- **Node.js 18+**
- **pnpm**

## 🚀 Como Rodar

### 1️⃣ Instalar Node Package Manager (pnpm)

Se ainda não tem pnpm instalado:

```bash
npm install -g pnpm
```

Ou, se usa Homebrew no macOS:
```bash
brew install pnpm
```

### 2️⃣ Instalar Dependências

```bash
pnpm install
```

Isso instalará todos os pacotes necessários listados em `package.json`.

### 3️⃣ Rodar em Modo de Desenvolvimento

```bash
pnpm run dev
```

**Saída esperada:**
```
  VITE v8.0.4  ready in 123 ms

  ➜  Local:   http://127.0.0.1:5173/
  ➜  press h to show help
```

O frontend estará disponível em **http://localhost:5173** (ou uma porta similar, veja o terminal).

## 🏗️ Estrutura do Projeto

```
rocket_ecommerce/
├── src/
│   ├── components/              # Componentes React
│   │   ├── ProdutoCard.tsx      # Card individual de produto
│   │   ├── ProdutoLista.tsx     # Lista de produtos
│   │   ├── ProdutoDetalhe.tsx   # Página de detalhes do produto
│   │   ├── SearchBar.tsx        # Barra de busca
│   │   ├── atoms/               # Componentes reutilizáveis pequenos
│   │   │   ├── Button.tsx       # Botão genérico
│   │   │   ├── Input.tsx        # Campo de entrada
│   │   │   ├── Card.tsx         # Container genérico
│   │   │   ├── Badge.tsx        # Tag/badge
│   │   │   ├── Modal.tsx        # Modal genérico
│   │   │   ├── LoadingSpinner.tsx # Indicador de carregamento
│   │   │   ├── ErrorMessage.tsx # Mensagem de erro
│   │   │   └── index.ts         # Exportações
│   │   ├── molecules/           # Componentes médios (combinações de atoms)
│   │   └── organisms/           # Componentes grandes (layout completo)
│   ├── services/                # Serviços de integração
│   │   ├── produtoService.ts    # Requisições relacionadas a produtos
│   │   └── imagemService.ts     # Requisições relacionadas a imagens
│   ├── styles/                  # Estilos globais e por componente
│   │   ├── ProdutoCard.css
│   │   ├── ProdutoLista.css
│   │   ├── ProdutoDetalhe.css
│   │   └── SearchBar.css
│   ├── App.tsx                  # Componente raiz da aplicação
│   ├── App.css                  # Estilos do App
│   ├── main.tsx                 # Entry point
│   ├── index.css                # Estilos globais
│   ├── assets/                  # Imagens e recursos estáticos
│   └── vite-env.d.ts            # Tipos do Vite
├── public/                      # Arquivos estáticos públicos
├── index.html                   # HTML principal
├── vite.config.ts               # Configuração do Vite
├── tailwind.config.js           # Configuração do Tailwind CSS
├── postcss.config.js            # Configuração do PostCSS
├── tsconfig.json                # Configuração do TypeScript
├── eslint.config.js             # Configuração do ESLint
├── package.json                 # Dependências do projeto
├── pnpm-lock.yaml              # Lock file do pnpm
└── README.md                    # Este arquivo
```

## 🎨 Arquitetura de Componentes

O projeto segue a arquitetura **Atomic Design**:

### **Atoms** (Componentes Básicos)
- `Button` - Botão genérico
- `Input` - Campo de entrada
- `Badge` - Tag/etiqueta
- `Card` - Container genérico
- `Modal` - Modal genérico
- `LoadingSpinner` - Indicador de carregamento
- `ErrorMessage` - Mensagem de erro

### **Molecules** (Combinações de Atoms)
- Componentes que combinam atoms para criar componentes mais complexos

### **Organisms** (Componentes Completos)
- `ProdutoCard` - Card de exibição do produto
- `ProdutoLista` - Lista de produtos com paginação
- `SearchBar` - Barra de busca com filtros
- `ProdutoDetalhe` - Página completa de detalhes do produto

## 🛠️ Stack Tecnológico

| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| React | 19.2.4 | Framework UI |
| TypeScript | 6.0.2 | Type-safety |
| Vite | 8.0.4 | Build tool |
| Tailwind CSS | 3.4.1 | Estilização |
| ESLint | 9.39.4 | Linting |
| Babel | 7.29.0 | Transpilação |

## 📦 Dependências Principais

### Runtime
- **react** - Library de UI
- **react-dom** - Renderização do React no DOM

### Dev Dependencies
- **@vitejs/plugin-react** - Plugin React para Vite
- **@types/react** - Types para React
- **@types/react-dom** - Types para React DOM
- **typescript** - Linguagem TypeScript
- **tailwindcss** - Framework CSS utilitário
- **eslint** - Linter de código
- **postcss** - Processador CSS
- **autoprefixer** - Adiciona prefixos CSS automáticamente

## ⚙️ Configurações Importantes

### Vite (`vite.config.ts`)
- Configuração de build
- Plugin React
- Paths para imports

### Tailwind CSS (`tailwind.config.js`)
- Tema customizado
- Plugins adicionais (@tailwindcss/forms)
- Extensões de cores e tipografia

### TypeScript (`tsconfig.json`)
- Strictness settings
- Target ES2020
- Paths customizadas

### ESLint (`eslint.config.js`)
- Regras de linting
- Plugins React
- React Hooks rules


## 🔗 Voltar ao Projeto Principal

Veja [README Principal](../../README.md) para instruções do projeto completo e documentação do backend.

---

**Última atualização**: Abril 2026

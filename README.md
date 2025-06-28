# STRIDE-CAPEC-CWE_DB

Este repositório contém os arquivos, scripts e dados necessários para a construção de um banco de dados de conhecimento em segurança cibernética, integrando três bases fundamentais: **STRIDE**, **CAPEC** e **CWE**.

---

## 📚 Objetivo

Construir um banco de dados unificado que relacione ameaças (STRIDE), padrões de ataque (CAPEC) e fraquezas comuns (CWE), permitindo:

- Consulta cruzada entre as bases.
- Apoio à modelagem de ameaças.
- Aplicação em análise de risco automatizada.
- Reprodutibilidade por outros pesquisadores.

---

## 🧠 Sobre as Fontes de Dados

STRIDE: Modelo de ameaça proposto pela Microsoft.

CAPEC: Common Attack Pattern Enumeration and Classification (MITRE).

CWE: Common Weakness Enumeration (MITRE).

As fontes originais são públicas e estão referenciadas na documentação técnica do projeto.

---

## 🗃️ Estrutura do Repositório

    STRIDE-CAPEC-CWE_DB/
    ├── converter/      # Scripts para converter o formato dos dados
    ├── data/           # Dados obtidos em fontes públicas
    ├── scripts/        # Scripts de importação, transformação e análise
    ├── queries/        # Exemplos de consultas no MongoDB
    └── README.md       # Documentação do projeto

---

## ⚙️ Como Reproduzir

1. **Pré-requisitos:**
   - Python 3.8+
   - MongoDB local ou MongoDB Atlas
   - Pip ou Conda para instalar as dependências

2. **Instale os pacotes necessários:**
   ```bash
   pip install pymongo
   pip install bson

---

## 📌 Referência

Se este repositório for útil para sua pesquisa, por favor cite ou referencie conforme apropriado. Para mais informações, entre em contato: eduardo.santos.oli.mar@gmail.com

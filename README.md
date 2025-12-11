# ESPECIFICAÇÃO TÉCNICA DETALHADA — SISTEMA SKY ALP

**Versão:** 1.0.0  
**Data:** 10 de Dezembro de 2025  
**Classificação:** Documentação Técnica Oficial  

---

## SUMÁRIO

1. [Dados de Autoria e Desenvolvimento](#1-dados-de-autoria-e-desenvolvimento)
2. [Visão Geral do Sistema](#2-visão-geral-do-sistema)
3. [Arquitetura de Software](#3-arquitetura-de-software)
4. [Tecnologias Utilizadas](#4-tecnologias-utilizadas)
5. [Modelagem de Dados (Dicionário Detalhado)](#5-modelagem-de-dados-dicionário-detalhado)
6. [APIs e Endpoints (Especificação Formal)](#6-api-e-endpoints-especificação-formal)
7. [Lógica Funcional Detalhada](#7-lógica-funcional-detalhada)
8. [Regras de Negócio (Modelo Formal)](#8-regras-de-negócio-formalização)
9. [Segurança e Compliance](#9-segurança-e-compliance)
10. [Infraestrutura e DevOps](#10-infraestrutura-e-devops)
11. [Requisitos de Sistema e Limites](#11-requisitos-de-sistema-e-limites)
12. [Manual Operacional (Visão por Perfil)](#12-manual-operacional-visão-por-perfil)
13. [Módulos de Exportação e Backup](#13-módulos-de-exportação-e-backup)
14. [Considerações Finais](#14-considerações-finais)

---

## 1. DADOS DE AUTORIA E DESENVOLVIMENTO

* **Responsável Técnico:** Rodrigo Gandarela Soares de Farias Duca
* **Formação:** Desenvolvedor Full Stack / Engenheiro da Computação
* **Versão da Build:** 1.0.0
* **Contato:** `rodrigosfduca@gmail.com`
* **LinkedIn:** `/rodrigo-gandarela-02473434b`
* **Github:** `/RodrigoDuca`

**Responsável pelo ciclo de vida completo:**
* Planejamento
* Desenvolvimento backend e frontend
* Arquitetura de dados
* Deploy
* Segurança
* Testes funcionais

---

## 2. VISÃO GERAL DO SISTEMA

O **Sky ALP** é uma plataforma inteligente para gestão de obras, integrando:

* ✔ Diário de Obra
* ✔ Gestão de Etapas
* ✔ Dashboard Analítico
* ✔ Módulos administrativos
* ✔ Exportação de dados
* ✔ Coleta de leads e comunicação

> **Nota:** O sistema segue uma filosofia de confiabilidade, rastreabilidade, segurança e mobilidade, garantindo operação a campo, mesmo com operadores de baixa familiaridade tecnológica.

---

## 3. ARQUITETURA DE SOFTWARE

### 3.1 Arquitetura Geral
O sistema utiliza uma **Arquitetura Monolítica Modular**, composta por:
1.  **Camada de Apresentação:** Jinja2 + Tailwind
2.  **Camada de Lógica de Negócio:** Flask Controllers
3.  **Camada de Serviços:** Analytics, Autenticação, Exportação
4.  **Camada de Persistência:** SQLAlchemy ORM

**Vantagens:**
* Manutenção centralizada
* Menor latência
* Deploy mais simples
* Menos pontos de falha

### 3.2 Componentes Internos
* `/controllers/` → Endpoints e rotas
* `/services/` → Módulos independentes (analytics, exportação, segurança)
* `/models/` → Classes ORM
* `/static/` → Tailwind, ícones
* `/templates/` → Interfaces Jinja2
* `/utils/` → Funções auxiliares (data/hora, validações)

### 3.3 Padrões de Projeto Aplicados
* **Factory Pattern:** Criação da instância da aplicação Flask.
* **MVC Parcial:** Usado de forma pragmática.
* **Repository Pattern:** Implementado via SQLAlchemy.
* **Adapter Pattern:** Abstração para exportações.
* **Service Layer:** Lógica encapsulada fora dos controladores.

### 3.4 Fluxo de Dados (Resumo Formal)
1.  Usuário realiza requisição (HTTP).
2.  Camada de Roteamento direciona ao Controller.
3.  Controller aciona a Camada de Serviços.
4.  Serviços acessam o ORM.
5.  ORM traduz para SQL e consulta o Banco.
6.  Resposta é processada e devolvida ao template Jinja2.
7.  HTML final é entregue ao cliente.

---

## 4. TECNOLOGIAS UTILIZADAS

### 4.1 Backend
* **Linguagem:** Python 3.10+
* **Framework:** Flask
* **Gestão de Sessão:** Flask-Session
* **ORM:** SQLAlchemy
* **Analytics:** Matplotlib (modo Agg backend)

### 4.2 Frontend
* **Template Engine:** Jinja2
* **Estilização:** Tailwind CSS CDN
* **Ícones:** Google Material Symbols

### 4.3 Terceiros e Bibliotecas Conectadas
* Interpretador Base64 para gráficos
* Mecanismo de horário sincronizado (UTC-3)

---

## 5. MODELAGEM DE DADOS (DICIONÁRIO DETALHADO)

Abaixo está o modelo de dados, com explicações aprofundadas das entidades principais.

### 5.1 Entidade: Obra
*Unidade central do sistema.*

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | PK | Identificador único |
| `nome` | Texto | Nome da obra |
| `status` | Texto | “Em andamento”, “Pendente”, “Concluída” |
| `cor_primaria` | Hex | Cor identificadora |
| `equipe` | Rel. M:N | Funcionários associados |

**Funções críticas:** Define permissões, impacta dashboard, identidade visual e controla o ciclo de vida.

### 5.2 Entidade: Registro Diário
*Contém fatos operacionais.*

**Campos importantes:**
* `data_hora`: Usado para exibição visual.
* `data_iso`: Usado para ordenação lógica.
* `autor_nome`: Nome do responsável.
* `foto`: Arquivo ou string Base64.
* `status_novo`: Flag de estado.

*Inclui rastreabilidade histórica completa.*

### 5.3 Entidade: Etapa
*Controla cronogramas.*

**Campos:**
* `prioridade` (Afeta layout e dashboards)
* `data_inicio_prevista`
* `data_fim_prevista`
* `status`

### 5.4 Entidades Complementares
* Funcionário
* Solicitação (Leads)
* Usuário Interno

### 5.5 Esquema ER (Descrito)
* **Obra** 1 — N **Etapas**
* **Obra** 1 — N **Registros**
* **Funcionário** M — N **Ob

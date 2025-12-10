# 🏗️ Sky ALP - Sistema de Gestão de Engenharia e Obras

> Plataforma integrada para gestão de construções civis, conectando o escritório administrativo ao canteiro de obras em tempo real.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![Status](https://img.shields.io/badge/Status-%20Concluído-green)

## 📌 Sobre o Projeto

O **Sky ALP** é um sistema Full Stack desenvolvido para resolver o problema de comunicação entre a gestão e a operação em obras. O sistema opera em arquitetura cliente-servidor e divide-se em duas interfaces principais:

1.  **Portal Administrativo (Web Desktop):** Para diretores e engenheiros gerenciarem cronogramas, equipes, clientes e leads.
2.  **App do Operador (Mobile Web):** Interface simplificada e focada em UX para mestres de obras registrarem o diário de obra com fotos e status diretamente do celular.

## 🚀 Funcionalidades Principais

### 🏢 Portal Administrativo (Gestores)
* **Dashboard de Leads:** Recebimento e gestão de solicitações de orçamento via Landing Page.
* **Gestão de Carteira:** Cadastro de Clientes e Múltiplas Obras por cliente.
* **Controle de Equipe:** Cadastro global de funcionários com níveis de acesso (Admin vs Operador).
* **Painel da Obra:**
    * Criação de Cronogramas e Etapas.
    * Visualização da Linha do Tempo (Diário de Obra).
    * Gráficos de progresso (gerados via Matplotlib).
    * Exportação de dados (CSV, SQL, JSON).

### 👷 App do Operador (Campo)
* **Interface Mobile-First:** Design responsivo otimizado para smartphones.
* **Diário de Obra:** Registro de atividades com upload de fotos (Base64).
* **Status em Tempo Real:** Atualização de etapas (Em andamento, Bloqueada, Concluída).
* **Timeline:** Visualização do histórico recente da obra.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, Flask.
* **Banco de Dados:** SQLite (com SQLAlchemy ORM).
* **Frontend:** HTML5, Jinja2, Tailwind CSS (CDN).
* **Visualização de Dados:** Matplotlib.
* **Ícones e Fontes:** Google Fonts, Material Symbols.

## ⚙️ Como Executar Localmente

### Pré-requisitos
* Python 3.8 ou superior.

### Instalação

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/SEU-USUARIO/skyalp-construction-manager.git](https://github.com/SEU-USUARIO/skyalp-construction-manager.git)
    cd skyalp-construction-manager
    ```

2.  Crie um ambiente virtual e instale as dependências:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install flask flask_sqlalchemy matplotlib
    ```

3.  Execute a aplicação:
    ```bash
    python app.py
    ```

4.  Acesse no navegador:
    * Landing Page: `http://127.0.0.1:5000/`
    * **Login Admin Padrão:** Usuário: `admin` | Senha: `admin`

## 🔒 Segurança e Implantação

Este projeto foi entregue com código aberto para hospedagem própria.
* **Infraestrutura:** Recomenda-se uso de Gunicorn + Nginx para produção.
* **Segurança:** É mandatório alterar a `SECRET_KEY` no arquivo `app.py` antes do deploy.
* **HTTPS:** O uso de SSL é obrigatório para funcionamento correto da câmera em dispositivos móveis.

## 👨‍💻 Desenvolvedor

* **RODRIGO GANDARELA SOARES DE FARIAS DUCA** - *Desenvolvedor Full Stack*
* [LinkedIn](https://www.linkedin.com/in/rodrigo-gandarela-02473434b/) | [Email](rodrigogsfduca@gmail.com)

---
*© 2025 Sky ALP Engineering. Todos os direitos reservados.*

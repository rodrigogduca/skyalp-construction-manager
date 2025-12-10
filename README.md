Aqui está o arquivo `README.md` completo, formatado para o GitHub. O conteúdo mantém o tom estritamente profissional, sem emojis e com o guia técnico detalhado para infraestrutura própria (VPS Linux), conforme solicitado.

-----

````markdown
# SkyALP - Sistema Integrado de Gestão de Obras Civis

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask Version](https://img.shields.io/badge/flask-2.0%2B-green)
![Status](https://img.shields.io/badge/status-stable%20v1.0.0-success)

## Visão Geral

O **SkyALP** é uma solução de software Full Stack desenvolvida para a administração centralizada de projetos de engenharia civil. [cite_start]O sistema soluciona o problema de desintegração de dados entre o escritório e o canteiro de obras, operando em uma arquitetura cliente-servidor robusta[cite: 7, 8].

O projeto está dividido em dois módulos funcionais distintos:
1.  [cite_start]**Portal Administrativo (Desktop):** Interface de gestão para engenheiros e diretores[cite: 9].
2.  [cite_start]**Módulo Operacional (Mobile):** Aplicação web otimizada para dispositivos móveis, destinada ao registro de diário de obra por mestres e encarregados[cite: 10].

---

## Funcionalidades

### Módulo Administrativo (Web Desktop)
* [cite_start]**Gestão de Leads:** Centralização de solicitações de orçamento via Landing Page integrada[cite: 42, 43].
* [cite_start]**Gestão de Contratos:** Cadastro de múltiplos clientes e obras [cite: 46-49].
* [cite_start]**Cronograma de Engenharia:** Definição de etapas construtivas (Gantt simplificado) e prioridades[cite: 59, 60].
* [cite_start]**Controle de Equipe:** Gestão de usuários e níveis de acesso (Gestor vs. Operador) [cite: 52-55].
* [cite_start]**Monitoramento:** Painel com indicadores de progresso visual (Matplotlib) e linha do tempo de registros[cite: 66, 67].
* [cite_start]**Exportação de Dados:** Relatórios em CSV, JSON e Dump SQL[cite: 68].

### Módulo Operacional (Web Mobile)
* **Interface Responsiva:** Design Mobile-First utilizando Tailwind CSS.
* [cite_start]**Diário de Obra Digital:** Registro de atividades com suporte a upload de imagens (armazenamento em Base64)[cite: 10, 77, 78].
* [cite_start]**Status em Tempo Real:** Atualização de etapas (Em Andamento, Bloqueada, Concluída)[cite: 80].
* **Funcionamento em Campo:** Otimizado para redes móveis (4G/5G).

---

## Stack Tecnológico

* [cite_start]**Linguagem:** Python 3.8+[cite: 14].
* [cite_start]**Framework Web:** Flask[cite: 7, 17].
* [cite_start]**Banco de Dados:** SQLite (SQLAlchemy ORM)[cite: 15, 17].
* **Frontend:** HTML5, Jinja2, Tailwind CSS (CDN).
* [cite_start]**Visualização de Dados:** Matplotlib[cite: 17].

---

## Guia de Infraestrutura e Implantação (Produção)

Este sistema foi projetado para ser hospedado em infraestrutura própria ou VPS (Virtual Private Server) rodando Linux (Ubuntu 20.04 ou superior). [cite_start]A configuração recomendada utiliza **Nginx** como proxy reverso e **Gunicorn** como servidor de aplicação WSGI[cite: 27, 32].

### 1. Preparação do Ambiente
No servidor Linux, instale as dependências do sistema:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx -y
````

### 2\. Instalação da Aplicação

Clone o repositório e configure o ambiente virtual:

```bash
cd /var/www/skyalp
python3 -m venv venv
source venv/bin/activate
pip install flask flask_sqlalchemy matplotlib gunicorn
```

### 3\. Configuração do Serviço (Systemd)

Para garantir a disponibilidade contínua, configure o serviço no Systemd. Crie o arquivo `/etc/systemd/system/skyalp.service`:

```ini
[Unit]
Description=Gunicorn instance to serve SkyALP
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/skyalp
Environment="PATH=/var/www/skyalp/venv/bin"
# Timeout definido para 120s para permitir uploads de imagens grandes em conexões lentas
ExecStart=/var/www/skyalp/venv/bin/gunicorn --workers 3 --bind unix:skyalp.sock --timeout 120 app:app

[Install]
WantedBy=multi-user.target
```

### 4\. Configuração do Proxy Reverso (Nginx)

A configuração do Nginx é crítica para permitir o upload de evidências fotográficas. No arquivo `/etc/nginx/sites-available/skyalp`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com.br;

    # OBRIGATÓRIO: Ajuste para aceitar payloads de até 32MB
    client_max_body_size 32M;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/skyalp/skyalp.sock;
    }
}
```

### 5\. Requisitos de Segurança

  * [cite_start]**SSL/HTTPS:** É mandatório o uso de certificado SSL (ex: Let's Encrypt) para que os navegadores móveis permitam o acesso à câmera no módulo operacional[cite: 30, 31].
  * [cite_start]**Variáveis de Ambiente:** Configure a `SECRET_KEY` via arquivo `.env` no servidor de produção[cite: 34, 35].
  * [cite_start]**Backup:** Configure rotinas diárias de backup do arquivo `skyalp_production.db`[cite: 37, 38].

-----

## Acesso Inicial

[cite_start]Ao realizar a primeira execução, o sistema cria automaticamente um superusuário para configuração inicial[cite: 20].

**Credenciais Padrão:**

  * [cite_start]**Login:** `admin` [cite: 21]
  * [cite_start]**Senha:** `admin` [cite: 22]

> **Nota:** Recomenda-se a alteração imediata destas credenciais após o primeiro login.

-----

## Autor

**Rodrigo Gandarela Soares de Farias Duca**
[cite_start]*Desenvolvedor Full Stack / Engenheiro da Computação* [cite: 5]

  * [cite_start]**Email:** rodrigogsfduca@gmail.com [cite: 5]
  * [cite_start]**LinkedIn:** [Perfil Profissional](https://www.linkedin.com/in/rodrigo-gandarela-02473434b/) [cite: 5]
  * [cite_start]**GitHub:** [@RodrigoDuca](https://github.com/RodrigoDuca) [cite: 5]

-----

© 2025 SkyALP. Todos os direitos reservados.

```
```

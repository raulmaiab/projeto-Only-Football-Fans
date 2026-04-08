# 🏆 FootballFans 
<p align="center"> <img src="https://img.shields.io/badge/Python-blue?style=for-the-badge"/> <img src="https://img.shields.io/badge/Django-success?style=for-the-badge"/> <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge"/> <img src="https://img.shields.io/badge/Deploy-Azure-blue?style=for-the-badge"/> </p>

## 📌 Visão Geral

O **FootballFans** é um aplicativo web desenvolvido em **Django** que funciona como um diário digital das experiências de cada torcedor.  
  
O objetivo é transformar cada ida ao estádio, cada gol, cada emoção, cada caos na arquibancada, em memórias organizadas, fáceis de buscar, comparar e reviver.

Aqui o torcedor pode:

**- Registrar partidas que assistiu ao vivo**

**- Avaliar estádios e torcidas**

**- Acompanhar tudo em uma linha do tempo**

**- Criar sua própria identidade futebolística ao longo dos jogos**

_Um app que eterniza momentos que o futebol entrega e o tempo não devolve._


---

## 📑 Funcionalidades  
- ⚽ **Registro de Jogos**: registre jogos na sua agenda.  
- 📖 **Histórico de Jogos**: visualize uma lista de todos os jogos que já assistiu.  
- ⭐ **Avaliações Personalizadas**: avalie torcidas, estádios, jogadores e experiências.  
- 🖼️ **Galeria de Mídia**: adicione fotos e comentários pessoais.  
- 🎥 **Links de Replay**: acesse os melhores momentos dos jogos.  

---

## 👥 Time de Desenvolvimento  

- **Artur Moury** – [amfgs@cesar.school](mailto:amfgs@cesar.school)  
  🟢 *Agile Coach – Time de Desenvolvimento*  

- **Diego Magnata** – [dfm@cesar.school](mailto:dfm@cesar.school)  
  🟢 *Scrum Master – Time de Desenvolvimento*  

- **Guilherme Silvestre** – [lgsgs@cesar.school](mailto:lgsgs@cesar.school)  
  🟢 *Engenheiro de QA – Time de Desenvolvimento*  

- **Matheus Fialho** – [mgfm@cesar.school](mailto:mgfm@cesar.school)  
  🟢 *Líder Técnico – Time de Desenvolvimento*  

- **Pablo** – [pcgar@cesar.school](mailto:pcgar@cesar.school)  
  🟢 *Engenheiro de QA – Time de Desenvolvimento*  

- **Raul Maia** – [rmb2@cesar.school](mailto:rmb2@cesar.school)  
  🟢 *Engenheiro de QA – Time de Desenvolvimento*  

- **Vitor Gadelha** – [vrlbga@cesar.school](mailto:vrlbga@cesar.school)  
  🟢 *Engenheiro de QA – Time de Desenvolvimento*  

---

## 🔗 Links Importantes  
- 📌 **Jira (Gestão do Projeto)** → [Acessar](https://fds-cesar-school.atlassian.net/jira/software/projects/PGF/boards/1?atlOrigin=eyJpIjoiNWUxNGI5MDY2OGM1NDhiYWJiMjg5ZjliMWU0M2E3ZTMiLCJwIjoiaiJ9)  
- 🎨 **Figma (Protótipo de Design)** → [Acessar](https://www.figma.com/design/CXlarW1bJs3u1XKdIYB1Q0/ProjetoFDS?node-id=0-1&p=f&t=6GuU3fSHRvxqUSVA-0)  
- 📄 **Google Docs (Documentação)** → [Acessar](https://docs.google.com/document/d/1KJ7e-UgdJZPT6Hks4MEKToqq0ciq734pU-kY532tJzU/edit?usp=sharing)
- 📽️ **Canva (Apresentação Do Projeto)** → [Acessar](https://www.canva.com/design/DAG451OIFY4/_TWTgrChyf5cAFsolQoQCw/edit?ui=e30)  

---

## 🤝 Como Contribuir com o projeto--Football-Fans

Ficamos muito felizes pelo seu interesse em contribuir! Este projeto é construído pela comunidade, e toda ajuda é bem-vinda.

Para garantir que o processo seja simples e eficiente para todos, por favor, siga este guia.

### 🚀 Configurando o Ambiente (Obrigatório)

Para garantir que seu código seja compatível e que tudo funcione, é *essencial* configurar seu ambiente local corretamente *antes* de começar a codificar.

Este projeto utiliza *Django* e requer um *ambiente virtual*.

---

#### 1. Preparação (Git)

Primeiro, prepare o repositório em sua máquina.

1.  **Fork:** Faça um "fork" deste repositório (raulmaiab/projeto--Football-Fans) para sua própria conta no GitHub.

2.  **Clone:** Clone o seu fork (substitua SEU-USUARIO):
    ```bash
    git clone https://github.com/SEU-USUARIO/projeto--Football-Fans.git
    cd projeto--Football-Fans
    ```

3.  **Crie uma Branch:** Nunca trabalhe diretamente na branch main ou master. Crie uma nova branch descritiva para sua mudança:
    ```bash
    git checkout -b minha-nova-funcionalidade
    ```
    (Ex: `git checkout -b fix/bug-login` ou `git checkout -b feature/pagina-estatisticas`)

---

#### 2. Configuração do Projeto (Django)

Agora, vamos instalar e rodar o projeto.

1.  **Crie o Ambiente Virtual (venv):**
    Dentro da pasta do projeto, crie um ambiente virtual.

    ```bash
    # No macOS/Linux
    python3 -m venv venv

    # No Windows
    python -m venv venv
    ```

2.  **Ative o Ambiente Virtual:**
    Você *precisa* ativar o ambiente antes de instalar qualquer coisa.

    ```bash
    # No macOS/Linux
    source venv/bin/activate

    # No Windows (PowerShell/CMD)
    .\venv\Scripts\activate
    ```
    (Seu terminal deve agora mostrar `(venv)` no início da linha).

3.  **Instale as Dependências:**
    Com o ambiente virtual ativo, instale todos os pacotes necessários:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados e Rode o Servidor:**
    (Adicione aqui quaisquer passos extras, como criar um .env, mas o básico é):
    ```bash
    # Aplica as migrações do banco de dados
    python manage.py migrate

    # Inicia o servidor de desenvolvimento
    python manage.py runserver
    ```

5.  **Verifique:**
    Acesse http://127.0.0.1:8000 no seu navegador. Se o projeto carregar sem erros, você está pronto para contribuir!

---

### 🧠 Padrões de Código

Não temos um Código de Conduta formal ou um guia de estilo (style guide) rígido. Pedimos apenas uma coisa:

**Mantenha a lógica do código.**

Antes de enviar, pergunte-se:
* Meu código segue os padrões já usados no restante do projeto?
* Minha lógica está clara e legível?
* Estou reutilizando funções ou classes que já existem, em vez de reescrever?

Se você seguir a estrutura e a lógica existentes, sua contribuição será facilmente integrada.

### 📥 Enviando sua Contribuição

Depois que seu ambiente estiver configurado e suas alterações estiverem prontas:

1.  **Faça o Commit:** Adicione e faça o commit das suas mudanças com uma mensagem clara.
    ```bash
    git add .
    git commit -m "Feat: Adiciona funcionalidade X"
    ```

2.  **Envie para seu Fork:**
    Envie a sua branch para o seu repositório (fork) no GitHub.
    ```bash
    git push origin minha-nova-funcionalidade
    ```

3.  **Abra um Pull Request (PR):**
    * Vá até a página do seu fork no GitHub.
    * Clique no botão "Compare & pull request".
    * Verifique se a base é a branch main (ou master) do repositório raulmaiab/projeto--Football-Fans e o head é a sua branch.
    * Na descrição, explique *o que* você fez e *por que*. Se sua alteração corrige uma "Issue" aberta, mencione o número dela (ex: Resolve #42).

**Obrigado por ajudar a construir o -Football-Fans!**

---

## 📦 Entregáveis  
<details>
  
  <summary>Entrega 1 ✅</summary>
  
  [Screencast Figma](https://youtu.be/sAhcepC54wo?si=GCJNAyZaQ7O_8hI4)
  
  [Histórias de Usuário](https://docs.google.com/document/d/1KJ7e-UgdJZPT6Hks4MEKToqq0ciq734pU-kY532tJzU/edit?usp=sharing )
  
  [BackLog Jira](images/backlog1.png)
  
  [Quadro Jira](images/quadrojira1.png)

</details>
<details>
  
  <summary>Entrega 2 ✅</summary>

  [Sessão de Programação em Dupla](images/programacao_dupla.png)
  
  [Print do BackLog Jira da Semana 2](images/backlog2.png) 
  
  [Link do primeiro Deploy](https://-football-fans.azurewebsites.net/login/)
  
  [Screencast do Deploy](https://youtu.be/sAhcepC54wo?si=GCJNAyZaQ7O_8hI4)
   
  [Issue/Bug Tracker](images/bug_tracker1.png)
  
  [Quadro Jira Entrega 2](images/quadrojira2.png)

</details>
<details>
  <summary>Entrega 3 ✅</summary>

  [BackLog Jira da Entrega 3](images/backlog3.png)
  
  [Quadro Jira da Entrega 3](images/quadrojira3.png)
  
  [Issue/ BugTracker - Open](images/bug_tracker2_open.png)
  
  [Issue/ Bug Tracker - Closed](images/bug_tracker2_closed.png)

  [Screencast dos Testes](https://youtu.be/c-wovCPDYfY?si=dTk3_qhHd_bDsY7F)

  [Screencast do CI/CD](https://youtu.be/XMa_inb8q7g?si=d223A3XJ7rpS5TtO)

  [Screencast do Deploy](https://youtu.be/3ujceBWA1Cs?si=PcHjT4azrKEH4oLb)

  [Sessão de Programação em Dupla](images/programacao_dupla2.png)
  
</details>
<details>

  <summary>Entrega 4 ✅</summary>

  [Print do BackLog Jira da Entrega 4](images/backlog4.png)
  
  [Quadro Jira da Entrega 4](images/quadrojira4.png)  

  [Issue/ Bug Tracker - Open](images/bugtracker3_open.png)
  
  [Issue/ Bug Tracker - Closed](images/bugtracker3_closed.png)

  [Screencast dos Testes](https://youtu.be/OZvVUhpt0sE)

  [Screencast do CI/CD](https://youtu.be/LvGSSg8vy8s?si=9LDbbrBAAshH6EtW)

  [Screencast do Deployment das Novas Histórias](https://youtu.be/eBS04oMwzm8)
  
  [Print da Sessão de Programação em Dupla](images/duplas.png)

  [Print da Sessão de Programação em Trio](images/trio.png)
  
</details>

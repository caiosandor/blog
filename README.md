# Portal Editorial Multi-Tenant (Django Full Stack + API REST)

Sistema web desenvolvido para a disciplina de **Laboratório de Programação Full Stack** (Universidade de Vassouras), estruturado em arquitetura multi-tenant para suportar múltiplas revistas, blogs e portais editoriais utilizando a mesma base de dados com isolamento lógico rigoroso.

## Sobre o Projeto

A plataforma permite que diferentes organizações (revistas digitais, portais de notícias ou blogs independentes) operem sobre uma única infraestrutura de banco de dados, garantindo que cada redação acesse, edite, analise e exporte exclusivamente os seus próprios conteúdos, colaboradores e métricas.

---

## Evolução e Funcionalidades

### Etapa 1 — Base do Sistema (CRUD e Regras de Negócio)
* **CRUD Completo de Matérias:** Criação, listagem, leitura detalhada, edição e exclusão de publicações, além de área dedicada para gestão de rascunhos.
* **Validação de Conteúdo:** Exigência de tamanho mínimo (pelo menos 50 caracteres) para postagens com status `Publicado`.
* **Busca e Filtro Editorial:** Filtragem por palavra-chave (buscando em título e conteúdo via `Q`) e por status de publicação (`Publicado` ou `Rascunho`).

### Etapa 2 — Isolamento Multi-Tenant e API REST (DRF)
* **Isolamento por Coluna Discriminadora:** Criação do app `core` contendo o modelo abstrato `DaOrganizacao` e o modelo `PerfilFuncionario`, vinculando cada usuário à sua respectiva `Pagina` e cargo (`Dono` ou `Editor`).
* **Migração de Dados Legados:** Uso de migrações personalizadas com `RunPython` para associar registros antigos às organizações sem perda de dados.
* **Blindagem da API REST (Django REST Framework):**
  * `get_queryset`: Filtra requisições `GET` para retornar exclusivamente os registros pertencentes à organização do usuário autenticado.
  * `perform_create`: Injeta automaticamente o `autor` e a `pagina` no backend durante o `POST`, impedindo manipulação indevida via payload JSON.
  * **Segurança de Acesso por ID:** Uso de `get_object_or_404` restrito ao tenant atual, retornando `404 Not Found` em tentativas de acesso a dados de outras organizações.

### Etapa 3 — Dashboard Gerencial, Segurança e Performance
* **Indicadores e Agregações no Banco:** Cálculo de KPIs (total de matérias, publicadas, rascunhos e autores ativos) usando `Count` com filtros condicionais (`filter=Q(...)`), ranking de autores mais ativos com `annotate` e série temporal mensal com `TruncMonth` ordenada cronologicamente.
* **Visualização Dinâmica:** Gráficos interativos com **Chart.js** e tratamento visual para estados vazios (quando não há dados no período).
* **Filtro por Período Validado:** Filtragem por intervalo de datas (`inicio` e `fim`) via `PeriodoForm`, prevenindo erros 500 em URLs malformadas.
* **Controle de Acesso por Papel (`Dono` vs `Editor`):**
  * **Dono:** Acesso completo ao dashboard, série histórica mensal, gestão de equipe e exportação de relatórios CSV.
  * **Editor:** Acesso à publicação de matérias e KPIs gerais, com bloqueio (`403 Forbidden`) na exportação de relatórios CSV e na gestão da equipe.
* **Relatório CSV Seguro:** Exportação de matérias filtradas por organização e período com proteção contra *CSV Injection* (escapando caracteres especiais no início de células).
* **Otimização de Consultas (Zero N+1):** Uso estratégico de `select_related('autor')` nas listagens e índices compostos no banco de dados para evitar consultas redundantes.

### Etapa 4 — Experiência Editorial, Onboarding e Gestão de Equipe
* **Interface Editorial Responsiva:** Design unificado com tipografia dedicada para leitura (`Inter` e `Merriweather`), destaque de capa, grade responsiva de artigos e indicador de revista e cargo na barra superior.
* **Autenticação e Onboarding Self-Service:** Telas próprias de login (`/entrar/`), logout seguro (`/sair/`) e criação de novas revistas (`/cadastrar/`), onde o usuário já cria sua organização e inicia automaticamente como `Dono`.
* **Gestão de Equipe (`/equipe/`):** Painel exclusivo para o `Dono` cadastrar novos colaboradores (`Editor` ou `Dono`) diretamente para a sua redação pela interface web.

---

## Roteiro de Demonstração e Perfis de Teste

Ao carregar o arquivo `dados_iniciais.json`, o sistema já dispõe de organizações e usuários prontos para validar o isolamento multi-tenant:

* **Revista Tech (`@usuario1` — Cargo: Dono):** Exibe apenas as matérias técnicas da Revista Tech, libera acesso completo ao gráfico mensal, à gestão de equipe e à exportação CSV.
* **Blog de Games (`@usuario2` — Cargo: Dono):** Isola completamente os artigos de jogos, mantendo dashboard, ranking e exportação independentes da Revista Tech.
* **Laboratório de Programação Full Stack (`@usuario3` — Cargo: Dono):** Organização dedicada à disciplina, contendo o artigo retrospectivo sobre toda a arquitetura construída.

---

## Testes Automatizados e Validação

O projeto possui suíte de testes automatizados (`python manage.py test`) cobrindo:
* Isolamento multi-tenant entre organizações no frontend e na API REST.
* Restrições de permissão por cargo (`Dono` vs `Editor` e bloqueio `403 Forbidden`).
* Integridade dos filtros de período e exportação CSV.
* Eficiência de consultas ao banco de dados utilizando `assertNumQueries`.

---

## Como Executar o Projeto

1. **Clone o repositório e acesse a pasta raiz do projeto:**
   ```bash
   git clone <url-do-seu-repositorio>
   cd blog
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   # No Linux/macOS:
   source venv/bin/activate
   # No Windows (PowerShell):
   venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Acesse a pasta `portal`, aplique as migrações e carregue os dados iniciais:**
   ```bash
   cd portal
   python manage.py migrate
   python manage.py loaddata dados_iniciais.json
   ```

5. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

6. **Acesse a aplicação no navegador:**
   * **Portal Editorial (Capa):** `http://127.0.0.1:8000/`
   * **Criar Nova Revista:** `http://127.0.0.1:8000/cadastrar/`
   * **Login da Redação:** `http://127.0.0.1:8000/entrar/`
   * **Dashboard Gerencial:** `http://127.0.0.1:8000/dashboard/`
   * **Gestão de Equipe:** `http://127.0.0.1:8000/equipe/`
   * **Painel Administrativo Django:** `http://127.0.0.1:8000/admin/`

---

## Rodando a Suíte de Testes

Dentro da pasta `portal/`, execute:
```bash
python manage.py test
```
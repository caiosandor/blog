Sistema de Blog Multi-Tenant (Django Full Stack + API REST)

Sistema web desenvolvido para a disciplina de Laboratório de Programação Full Stack (Universidade de Vassouras), estruturado em arquitetura multi-tenant para suportar múltiplos clientes/organizações utilizando a mesma base de dados.

🚀 Sobre o Projeto

O projeto consiste em uma plataforma de gerenciamento de postagens de blog onde diferentes organizações (como empresas, revistas ou blogs independentes) compartilham a mesma infraestrutura de banco de dados, mas com os seus dados rigorosamente isolados.

🛠️ Evolução e Funcionalidades

📌 P1 (Base do Sistema)

CRUD Completo de Posts: Criação, listagem, detalhamento, edição e exclusão de publicações (via Views HTML baseadas em funções e formulários Django).

Regras de Negócio: Validação de tamanho mínimo (exigindo pelo menos 50 caracteres para posts com status "publicado").

Busca e Filtro: Suporte a parâmetros na URL para filtragem por título e status de publicação.

🛡️ P2 (Isolamento Multi-Tenant e API REST)

Isolamento por Coluna Discriminadora: Criação do app core contendo o model abstrato DaOrganizacao e o PerfilFuncionario para vincular cada usuário à sua respectiva página/organização.

Migração de Dados Legados: Uso de migrações personalizadas com RunPython para popular registros antigos sem perda de dados.

Blindagem da API REST (DRF):

get_queryset: Filtra as requisições GET para que os usuários visualizem apenas os registros pertencentes à sua organização.

perform_create: Injeta automaticamente o autor e a página no backend durante o POST, impedindo manipulação indevida via JSON.

Segurança de Acesso por ID: Uso de get_object_or_404 restrito à organização atual, retornando 404 Not Found caso haja tentativa de acesso a dados alheios.

🧪 Roteiro de Testes e Validação

O sistema foi testado e validado utilizando dois perfis de usuários distintos:

Usuário 1 (Revista Tech):

Ao criar postagens, o sistema injeta automaticamente a autoria e a página "Revista Tech".

A consulta à API e ao frontend exibe unicamente os posts da Revista Tech, ocultando dados de outras tenants.

Usuário 2 (Blog de Games):

Ao alternar a sessão para este usuário, o sistema isola completamente o ambiente. As listagens retornam apenas as publicações do Blog de Games.

Tentativas de alteração direta de IDs na URL geram bloqueios de segurança (404).

⚙️ Como Executar o Projeto

Clone o repositório e acesse a pasta do projeto.

Crie e ative o ambiente virtual:

python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate


Instale as dependências:

pip install -r requirements.txt


Aplique as migrações no banco de dados:

python manage.py migrate


Inicie o servidor de desenvolvimento:

python manage.py runserver


Acesse http://127.0.0.1:8000/admin para gerenciar organizações, perfis e usuários de teste.
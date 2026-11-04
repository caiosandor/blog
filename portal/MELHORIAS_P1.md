# Melhorias P1 (Preparação para o DRF)

Como foi avisado no slide: se o model for frágil, a API herda a fragilidade[cite: 1]. Por isso, vou arrumar a base do projeto para não limitar a saída de dados da minha API. Aqui estão os pontos que vou corrigir:

1. **Modelagem (Autor como ForeignKey):** 
   O campo `autor` hoje é um texto simples. Se eu mantiver isso, a API vai entregar um JSON pobre (ex: `"autor": "João"`), sem o ID ou e-mail da pessoa. Vou alterar para uma `ForeignKey` ligada ao modelo `User`. Assim, o DRF consegue puxar os dados completos do usuário e validar corretamente quem está fazendo o POST.

2. **Modelagem (Datas de Criação e Atualização):** 
   O meu modelo `Post` não registra quando a notícia foi criada. Sem essas datas, o sistema de ordenação nativo do DRF não tem como funcionar. Vou adicionar os campos `criado_em` e `atualizado_em` para que a API consiga filtrar e entregar "as notícias mais recentes".

3. **Validação (Regras presas no forms.py):** 
   A minha regra que exige 50 caracteres está no `forms.py`. Como o DRF usa *Serializers* e ignora formulários HTML, a API acabaria aceitando envios inválidos. Vou jogar essa validação para dentro do modelo (ou prepará-la para o Serializer) para garantir que a API também barre dados ruins, e aproveitar para colocar avisos na tela (`messages`) do frontend atual.

4. **Dívida Técnica (Rotas repetidas para Rascunhos):** 
   Criei rotas e views separadas só para rascunhos, o que vai contra a ideia de uma API RESTful. No DRF, vou precisar de um *endpoint* único (`/api/posts/`) e usar parâmetros de busca (`?status=rascunho`). Vou limpar essas views duplicadas agora para já deixar a arquitetura no padrão correto.

5. **Dívida Técnica (Banco de Dados):** 
   Ainda estou usando o `db.sqlite3` em arquivo. Para garantir que a base de dados aguente as requisições da API e tenha integridade real nos relacionamentos, vou migrar para um PostgreSQL rodando em um contêiner Docker.
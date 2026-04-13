# LS_Management
Plataforma digital para gestão de rebanho bovino: controle de produção de leite, vacinas, evolução de peso e relatórios estratégicos para o produtor rural.

Como Executar:

Crie um ambiente virtual: python -m venv venv.
Ative o venv: venv\Scripts\activate (Windows).
Instale o Django e o DRF: pip install django djangorestframework.
Rode as migrações: python manage.py migrate.
Inicie o servidor: python manage.py runserver.

Rotas da API:

GET /api/bovinos/ Lista todos os bovinos cadastrados.
POST /api/bovinos/ Cria um novo registro de bovino.

GET /api/bovinos/<rfid>/ Detalha um bovino específico pelo RFID.
PUT /api/bovinos/<rfid>/ Atualiza todos os dados de um bovino.
PATCH /api/bovinos/<rfid>/ Atualiza parcialmente os dados.
DELETE /api/bovinos/<rfid>/ Exclui um bovino do sistema.

Criar Registro POST /api/historicos/ Adiciona um novo evento ao histórico de um animal.

Corpo da requisição bovinos (POST):

{
    "rfid_tag": "1",
    "nome": "Mimosa 1",
    "raca": "Holandesa",
    "status": "Ativo"
}

Corpo da requisição historicos (POST):

{
    "animal": 10, - Usar ID do boi e não o RFID_Tag.
    "tipo": "PESO",
    "valor": 450.0,
    "sintomas": "Animal saudável e em engorda",
    "data": "2026-04-13T20:30:00Z"
}
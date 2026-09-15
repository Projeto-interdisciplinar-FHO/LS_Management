# LS Management

Plataforma web para gestão de rebanho bovino, com foco em controle sanitário, movimentações, alimentação, produção, peso e autenticação via JWT.

## Visão Geral

O projeto está organizado em apps Django/DRF por domínio de negócio, o que facilita manter cada recurso isolado e evoluir a API sem perder clareza.

### Tecnologias

- Django
- Django REST Framework
- Simple JWT
- SQLite
- CORS Headers

## Como Executar

### 1. Entrar no backend

```powershell
cd backend
```

### 2. Ativar o ambiente virtual

```powershell
.\venv\Scripts\Activate.ps1
```

Se preferir usar o executável diretamente, também funciona:

```powershell
.\venv\Scripts\python.exe --version
```

### 3. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 4. Aplicar migrações

```powershell
python manage.py migrate
```

### 5. Subir o servidor

```powershell
python manage.py runserver
```

## Autenticação

O backend usa JWT. As rotas de autenticação ficam em `authentication/token/`.

### Rotas de autenticação

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/authentication/token/` | Gera access e refresh token |
| POST | `/authentication/token/refresh/` | Renova o access token |
| POST | `/authentication/token/verify/` | Valida um token |

## Rotas da API

As rotas abaixo estão definidas em [backend/core/urls.py](backend/core/urls.py).

### Admin

| Método | Rota |
| --- | --- |
| GET | `/admin/` |

### Especies

| Método | Rota |
| --- | --- |
| GET, POST | `/species/` |
| GET, PUT, PATCH, DELETE | `/species/<int:pk>` |

### Quadrants

| Método | Rota |
| --- | --- |
| GET, POST | `/quadrants/` |
| GET, PUT, PATCH, DELETE | `/quadrants/<int:pk>` |

### Purpose Types

| Método | Rota |
| --- | --- |
| GET, POST | `/purpose_types/` |
| GET, PUT, PATCH, DELETE | `/purpose_types/<int:pk>` |

### Animals

| Método | Rota |
| --- | --- |
| GET, POST | `/animals/` |
| GET, PUT, PATCH, DELETE | `/animals/<int:pk>` |

### Breeds

| Método | Rota |
| --- | --- |
| GET, POST | `/breeds/` |
| GET, PUT, PATCH, DELETE | `/breeds/<int:pk>` |

### Weight History

| Método | Rota |
| --- | --- |
| GET, POST | `/weight_history/` |
| GET, PUT, PATCH, DELETE | `/weight_history/<int:pk>` |

### Milk Production History

| Método | Rota |
| --- | --- |
| GET, POST | `/milk_production_history/` |
| GET, PUT, PATCH, DELETE | `/milk_production_history/<int:pk>` |

### Vaccines

| Método | Rota |
| --- | --- |
| GET, POST | `/vaccines/` |
| GET, PUT, PATCH, DELETE | `/vaccines/<int:pk>` |

### Vaccination Plans

| Método | Rota |
| --- | --- |
| GET, POST | `/vaccination_plans/` |
| GET, PUT, PATCH, DELETE | `/vaccination_plans/<int:pk>` |

### Vaccinations

| Método | Rota |
| --- | --- |
| GET, POST | `/vaccinations/` |
| GET, PUT, PATCH, DELETE | `/vaccinations/<int:pk>` |

### Foods

| Método | Rota |
| --- | --- |
| GET, POST | `/foods/` |
| GET, PUT, PATCH, DELETE | `/foods/<int:pk>` |

### Feedings

| Método | Rota |
| --- | --- |
| GET, POST | `/feedings/` |
| GET, PUT, PATCH, DELETE | `/feedings/<int:pk>` |

### Feeding Plans

| Método | Rota |
| --- | --- |
| GET, POST | `/feeding_plans/` |
| GET, PUT, PATCH, DELETE | `/feeding_plans/<int:pk>` |

### Movement Types

| Método | Rota |
| --- | --- |
| GET, POST | `/movement_types/` |
| GET, PUT, PATCH, DELETE | `/movement_types/<int:pk>` |

### Animal Movements

| Método | Rota |
| --- | --- |
| GET, POST | `/animal_movements/` |
| GET, PUT, PATCH, DELETE | `/animal_movements/<int:pk>` |

### Animal Health

| Método | Rota |
| --- | --- |
| GET, POST | `/animal_health/` |
| GET, PUT, PATCH, DELETE | `/animal_health/<int:pk>` |

## Documentação da API

A documentação completa das rotas, autenticação e exemplos de respostas está em [docs/api.md](docs/api.md).

## Frontend

A interface é um app Vue 3 + Vite em [frontend/](frontend). O mapa das pastas está em [frontend/README.md](frontend/README.md).

## Estrutura do Projeto

```
LS_Management/
├── docs/                  documentação da API
├── frontend/              app Vue (ver frontend/README.md)
└── backend/
    ├── manage.py
    ├── requirements.txt
    ├── core/              settings, urls, wsgi/asgi e permissões compartilhadas
    ├── apps/              apps Django agrupados em módulos por área
    │   ├── accounts/      authentication                                  (contas)
    │   ├── herd/          animals, species, breeds, purpose_types, quadrants  (rebanho)
    │   ├── production/    weight_history, milk_production_history         (produção)
    │   ├── health/        vaccines, vaccination_plans, vaccinations, animal_health, animal_biometrics*  (sanidade)
    │   ├── nutrition/     foods, feedings, feeding_plans                  (alimentação)
    │   ├── movements/     movement_types, animal_movements                (movimentação)
    │   ├── operations/    tasks, notifications                            (operação)
    │   └── reports/       statistics_api*                                 (relatórios)
    ├── integrations/
    │   └── gemini_api/    cliente da API do Gemini
    └── scripts/           scripts avulsos de carga de dados de teste
```

\* existem, mas não estão no `INSTALLED_APPS`.

Cada módulo e cada app seguem a mesma anatomia:

```
apps/<modulo>/
├── __init__.py          o que o módulo cobre
├── urls.py              prefixos dos apps do módulo (species/, animals/...)
└── <app>/
    ├── apps.py          configuração do app (name = 'apps.<modulo>.<app>')
    ├── models.py        tabelas
    ├── serializers.py   entrada/saída da API
    ├── views.py         endpoints
    ├── urls.py          rotas do app
    ├── admin.py         registro no /admin, quando houver
    └── migrations/
```

- Cada app continua sendo um app Django independente: o rótulo usado nas migrations e nas tabelas é só o nome final (ex.: `animals`), então agrupar em módulos não mexe no banco.
- Imports usam sempre o caminho completo, inclusive dentro do próprio app: `from apps.herd.animals.models import Animal`.
- Rotas em três níveis: [core/urls.py](backend/core/urls.py) liga os módulos → `apps/<modulo>/urls.py` define o prefixo de cada app → `apps/<modulo>/<app>/urls.py` define as rotas.
- Para criar um app novo: coloque-o no módulo da área, com `name = 'apps.<modulo>.<app>'` no `apps.py`; registre no `INSTALLED_APPS` e no `urls.py` do módulo.
- [core/settings.py](backend/core/settings.py) tem primeiro a configuração do Django e, no fim, a das bibliotecas (DRF e CORS).
- A autenticação JWT está concentrada no fluxo de `authentication/token/`.
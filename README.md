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

## Frontend

Os arquivos de interface ficam em [frontend/](frontend). Atualmente existem as telas:

- [frontend/index.html](frontend/index.html)
- [frontend/login.html](frontend/login.html)
- [frontend/user_selection.html](frontend/user_selection.html)

## Estrutura do Projeto

- [backend/core/](backend/core) contém configurações globais e URLs principais.
- Os apps de domínio ficam separados por responsabilidade, como animals, vaccines, feedings e outros.
- A autenticação JWT está concentrada no fluxo de `authentication/token/`.

## Sugestão de Organização das Rotas

Para manter o README limpo quando a API crescer, o ideal é:

1. Manter aqui uma visão geral das rotas mais importantes.
2. Criar um arquivo dedicado em `docs/api.md` para a documentação completa da API.
3. Se quiser algo ainda melhor no futuro, gerar documentação automática com schema OpenAPI/Swagger.

## Exemplo de Payload

### Animal

```json
{
    "rfid_tag": "1",
    "nome": "Mimosa 1",
    "raca": "Holandesa",
    "status": "Ativo"
}
```

### Histórico

```json
{
    "animal": 1,
    "tipo": "PESO",
    "valor": 420.5,
    "sintomas": "Nenhum",
    "data": "2026-04-13T20:30:00Z"
}
```
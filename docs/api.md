# API do LS Management

API REST em Django REST Framework com autenticação JWT. Todas as rotas exigem token, exceto as de login.

Base local: `http://127.0.0.1:8000/`

## Autenticação

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/api/token/` (ou `/authentication/token/`) | Gera `access` e `refresh` |
| POST | `/api/token/refresh/` | Renova o `access` |
| POST | `/api/token/verify/` | Valida um token |

Resposta do login:

```json
{
  "refresh": "eyJ...",
  "access": "eyJ...",
  "is_superuser": true,
  "papel": "Administrador",
  "username": "admin",
  "nome": "Admin"
}
```

Nas demais rotas, envie:

```http
Authorization: Bearer SEU_TOKEN_AQUI
```

## Usuários (somente Administrador)

| Método | Rota |
| --- | --- |
| GET, POST | `/users/` (POST também em `/users/register/`) |
| GET, PUT, PATCH | `/users/<id>/` |

Não há exclusão: para desativar um usuário use `PATCH {"is_active": false}`.

## Recursos (CRUD)

Todos ficam em [backend/apps/api/urls.py](../backend/apps/api/urls.py) e seguem o padrão do router do DRF:

- `GET, POST /<recurso>/`
- `GET, PUT, PATCH, DELETE /<recurso>/<id>/`

| Recurso | Modelo | Observação |
| --- | --- | --- |
| `cows/` | `cattle.Cow` | vacas |
| `animals/` | `cattle.Cow` | apelido de `cows/`, usado pelo frontend |
| `bulls/` | `cattle.Bull` | touros |
| `classes/` | `cattle.CattleClass` | categorias do rebanho |
| `breeds/` | `breeds.Breed` | raças |
| `quadrants/` | `quadrants.Quadrant` | estábulos / piquetes |
| `movement_types/` | `movement_types.MovementType` | |
| `animal_movements/` | `animal_movements.AnimalMovement` | filtra por `?animal_id=` |
| `inseminations/` | `reproduction.Insemination` | |
| `births/` | `reproduction.Birth` | |
| `birth_occurrences/` | `reproduction.BirthOccurrence` | |
| `vaccines/` | `vaccines.Vaccine` | |
| `vaccination_groups/` | `vaccination_groups.VaccinationGroup` | filtra por `?animal_id=` |
| `vaccination_plans/` | `vaccination_plans.VaccinationPlan` | |
| `vaccinations/` | `vaccinations.Vaccination` | `?animal_id=` e `?upcoming=true` (próxima dose a partir de hoje) |
| `veterinary_occurrences/` | `animal_health.VeterinaryOccurrence` | |
| `animal_health/` | `animal_health.AnimalHealth` | filtra por `?animal_id=` |
| `foods/` | `foods.Food` | |
| `feedings/` | `feedings.Feeding` | filtra por `?animal_id=` |
| `feeding_plans/` | `feeding_plans.FeedingPlan` | |
| `milking/` | `milk_production_history.Milking` | filtra por `?animal_id=` |
| `milk_production_history/` | `milk_production_history.Milking` | apelido de `milking/` |
| `weight_history/` | `weight_history.WeightHistory` | filtra por `?animal_id=` |

O filtro `?animal_id=` é ignorado em recursos que não têm o campo `animal`.

Exemplo de vaca (`GET /animals/1/`):

```json
{
  "id": 1,
  "name": "Mimosa",
  "register_number": 1001,
  "status": "active",
  "score": "3.50",
  "reproductive_status": true,
  "breed": 2,
  "birth": null
}
```

`status` aceita `active`, `inactive`, `sold` e `deceased`. `register_number` é único.

### Exportação CSV de animais

| Método | Rota |
| --- | --- |
| GET | `/animals/export-fields/` |
| GET | `/animals/export/` |

Sem parâmetros, exporta todos os animais com todos os campos. Para um estábulo, informe `quadrant_id` (ou `estabulo_id`); `quadrant_id=all` exporta todos. Campos são escolhidos pela chave devolvida em `export-fields`, separados por vírgula:

```text
/animals/export/?quadrant_id=3&fields=register_number,name,current_quadrant_name,last_weight
```

O estábulo atual de cada animal é o do último movimento registrado. Campos históricos saem agregados (ex.: quantidade de vacinações), sem repetir o animal.

## Importação por planilha (XLSX)

Disponível em `/api/importacao/` e `/importacao/`:

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `vacas/` | baixa o modelo (`?exportar=true` exporta os dados) |
| POST | `vacas/` | importa vacas |
| GET | `ordenhas/` | baixa o modelo (`?exportar=true` exporta os dados) |
| POST | `ordenhas/` | importa ordenhas |

## IA: validação genealógica

`GET /api/reproducao/validar-genealogia/?cow_id=2&bull_id=1` ou `POST` com `{"cow_id": 2, "bull_id": 1}`.
Também responde em `/reproducao/validar-genealogia/`. Depende de `API_KEY` (Gemini) no `backend/.env`.

## Admin

`/admin/`: Django Admin.

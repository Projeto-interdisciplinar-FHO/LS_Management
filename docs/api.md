# API do LS Management

Documentação prévia da API REST do projeto LS Management.

## Visão geral

A API é organizada por apps Django/DRF e usa JWT para autenticação. Por padrão, as rotas exigem token válido no header `Authorization`.

## Base local

Durante o desenvolvimento, a API costuma ficar disponível em:

```text
http://127.0.0.1:8000/
```

## Autenticação

### POST /authentication/token/

Gera os tokens `access` e `refresh`.

#### Exemplo de resposta

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### POST /authentication/token/refresh/

Renova o token de acesso.

#### Exemplo de resposta

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### POST /authentication/token/verify/

Valida um token JWT.

#### Exemplo de resposta

```json
{}
```

## Cabeçalho de autenticação

Para as rotas protegidas, envie o token assim:

```http
Authorization: Bearer SEU_TOKEN_AQUI
```

## Rotas por recurso

### Admin

| Método | Rota |
| --- | --- |
| GET | `/admin/` |

### Species

| Método | Rota |
| --- | --- |
| GET, POST | `/species/` |
| GET, PUT, PATCH, DELETE | `/species/<int:pk>` |

#### Exemplo de resposta

```json
{
  "id": 1,
  "name": "Bovino"
}
```

### Quadrants

| Método | Rota |
| --- | --- |
| GET, POST | `/quadrants/` |
| GET, PUT, PATCH, DELETE | `/quadrants/<int:pk>` |

#### Exemplo de resposta

```json
{
  "id": 1,
  "name": "Piquete A",
  "description": "Área principal de pastejo",
  "area": "12.50",
  "max_animals": 40
}
```

### Purpose Types

| Método | Rota |
| --- | --- |
| GET, POST | `/purpose_types/` |
| GET, PUT, PATCH, DELETE | `/purpose_types/<int:pk>` |

#### Exemplo de resposta

```json
{
  "id": 1,
  "name": "Leite"
}
```

### Animals

| Método | Rota |
| --- | --- |
| GET, POST | `/animals/` |
| GET, PUT, PATCH, DELETE | `/animals/<int:pk>` |

#### Exemplo de resposta

```json
{
  "id": 1,
  "name": "Mimosa 1",
  "birth_date": "2022-08-15",
  "register_number": 1001,
  "weight": "420.50",
  "active": true,
  "sex": "F",
  "specie": 1,
  "breed": 2,
  "quadrant": 1,
  "purpose": 1
}
```

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

#### Exemplo de resposta

```json
{
  "id": 1,
  "name": "Clostridial"
}
```

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

## Exemplo de lista

Quando o endpoint retorna uma coleção, a resposta normalmente vem em formato de lista:

```json
[
  {
    "id": 1,
    "name": "Bovino"
  },
  {
    "id": 2,
    "name": "Bufalino"
  }
]
```

## Dicas rápidas

- As respostas usam o formato padrão do Django REST Framework.
- Campos de relacionamento aparecem como IDs, salvo se a view/serializer for alterado para expandir os dados.
- Como a permissão padrão é `IsAuthenticated`, a maioria das rotas exige token JWT válido.

## Próximo passo recomendado

Se quiser documentar melhor ainda, o ideal é adicionar para cada recurso:

- exemplo de payload de criação
- exemplo de resposta de detalhe
- exemplo de erro de validação
- status HTTP esperados

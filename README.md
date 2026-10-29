# API de Gerenciamento de Eventos Acadêmicos (APS 3)

API RESTful feita com FastAPI para gerenciar eventos acadêmicos (palestras, workshops,
minicursos, seminários, competições), participantes e inscrições.

Esta versão evolui a API da APS 2: os dados deixam de ficar em listas na memória e passam a
ser salvos em um banco **SQLite** usando **SQLAlchemy ORM**. Também foram criados três
relatórios que consolidam as informações do banco (ocupação, categorias e cursos).

## Instalação

```bash
git clone <link-do-repositorio>
cd projeto

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
```

## Execução

```bash
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## Estrutura do projeto

```
projeto/
├── main.py
├── database.py
├── requirements.txt
├── README.md
│
├── controller/
│   ├── evento_controller.py
│   ├── participante_controller.py
│   ├── inscricao_controller.py
│   └── relatorio_controller.py
│
├── model/
│   ├── evento.py
│   ├── participante.py
│   └── inscricao.py
│
├── schema/
│   ├── evento_schema.py
│   ├── participante_schema.py
│   ├── inscricao_schema.py
│   └── relatorio_schema.py
│
└── service/
    ├── evento_service.py
    ├── participante_service.py
    ├── inscricao_service.py
    └── relatorio_service.py
```

- **controller**: rotas e recebimento das requisições HTTP.
- **model**: tabelas e relacionamentos do banco (SQLAlchemy).
- **schema**: validação da entrada e formato das respostas (Pydantic).
- **service**: regras de negócio, acesso ao banco e consultas dos relatórios.
- **database.py**: conexão, sessões e criação das tabelas.

## Configuração do banco de dados

- O banco é um arquivo SQLite chamado **`eventos.db`**, criado automaticamente na pasta do
  projeto (ao lado do `main.py`) na primeira vez que a aplicação é executada.
- O `database.py` cria o `engine`, a `SessionLocal` e a `Base` dos models.
- A função `get_db()` abre uma sessão para cada requisição e fecha ao final (usada com
  `Depends` nos controllers).
- As tabelas (`eventos`, `participantes` e `inscricoes`) são criadas a partir dos models com
  `Base.metadata.create_all()` quando a aplicação inicia.
- As chaves estrangeiras do SQLite são ativadas a cada conexão (`PRAGMA foreign_keys=ON`).
- Para zerar os dados, basta parar a aplicação e apagar o arquivo `eventos.db`.

### Relacionamentos e integridade

- `Evento` 1 — N `Inscricao`
- `Participante` 1 — N `Inscricao`
- A tabela `inscricoes` tem uma restrição única em (`evento_id`, `participante_id`), então o
  mesmo participante não consegue se inscrever duas vezes no mesmo evento.
- O e-mail do participante é único (e salvo em minúsculo).
- **Exclusão:** ao excluir um evento ou um participante, as inscrições ligadas a ele também
  são excluídas (cascade), para não sobrar registros órfãos.
- Não é possível reduzir a capacidade de um evento para um valor menor que o número de
  inscritos (retorna 409).
- Erros inesperados do banco retornam uma mensagem genérica (500), sem detalhes técnicos.

## Principais rotas

### Eventos

| Método | Rota           | Descrição                     |
|--------|----------------|-------------------------------|
| POST   | /eventos       | Cadastra um evento            |
| GET    | /eventos       | Lista os eventos              |
| GET    | /eventos/{id}  | Consulta um evento            |
| PUT    | /eventos/{id}  | Atualiza um evento            |
| DELETE | /eventos/{id}  | Exclui um evento              |

### Participantes

| Método | Rota                | Descrição                     |
|--------|---------------------|-------------------------------|
| POST   | /participantes      | Cadastra um participante      |
| GET    | /participantes      | Lista os participantes        |
| GET    | /participantes/{id} | Consulta um participante      |
| PUT    | /participantes/{id} | Atualiza um participante      |
| DELETE | /participantes/{id} | Exclui um participante        |

### Inscrições

| Método | Rota                                              | Descrição                              |
|--------|---------------------------------------------------|----------------------------------------|
| POST   | /eventos/{evento_id}/inscricoes/{participante_id} | Inscreve um participante em um evento  |
| GET    | /eventos/{evento_id}/inscricoes                   | Lista os participantes inscritos       |

### Relatórios

| Método | Rota                            | Descrição                          |
|--------|---------------------------------|------------------------------------|
| GET    | /relatorios/eventos/ocupacao    | Ocupação de cada evento            |
| GET    | /relatorios/eventos/categorias  | Consolidação de eventos por categoria |
| GET    | /relatorios/participantes/cursos| Participação por curso             |

## Códigos de erro

| Situação                           | Código |
|------------------------------------|--------|
| Evento ou participante inexistente | 404    |
| Participante já inscrito           | 409    |
| Evento sem vagas                   | 409    |
| E-mail já cadastrado               | 409    |
| Capacidade menor que os inscritos  | 409    |
| Dados inválidos                    | 422    |
| Falha inesperada no banco          | 500    |

## Relatórios

Todos os valores são calculados na hora, com consultas SQLAlchemy (`join`, `group_by`,
`count`, `sum`), e não existe nenhum valor fixo no código. Se não houver registros, a rota
retorna uma lista vazia (`[]`).

**Ocupação dos eventos** — `GET /relatorios/eventos/ocupacao`

Para cada evento: id, título, capacidade, total de inscritos, vagas disponíveis e percentual
de ocupação. Eventos sem inscrições aparecem com 0 inscritos e 0.0% (usa `outerjoin`).

```json
[
  {
    "evento_id": 1,
    "titulo": "Introdução à Inteligência Artificial",
    "capacidade": 100,
    "total_inscritos": 75,
    "vagas_disponiveis": 25,
    "percentual_ocupacao": 75.0
  }
]
```

**Eventos por categoria** — `GET /relatorios/eventos/categorias`

Para cada categoria: quantidade de eventos, soma das capacidades e total de inscrições.

```json
[
  {
    "categoria": "Palestra",
    "total_eventos": 5,
    "capacidade_total": 500,
    "total_inscricoes": 320
  }
]
```

**Participação por curso** — `GET /relatorios/participantes/cursos`

Para cada curso: quantidade de participantes (cada participante é contado uma vez, mesmo com
várias inscrições) e total de inscrições feitas por eles.

```json
[
  {
    "curso": "Engenharia de Software",
    "total_participantes": 80,
    "total_inscricoes": 150
  }
]
```

## Exemplos de utilização

Cadastrar evento — `POST /eventos`

```json
{
  "titulo": "Workshop de Python",
  "descricao": "Introdução à linguagem Python",
  "data": "2026-11-20",
  "horario": "19:00",
  "local": "Laboratório 3",
  "capacidade": 40,
  "categoria": "Workshop"
}
```

Resposta (201):

```json
{
  "id": 1,
  "titulo": "Workshop de Python",
  "descricao": "Introdução à linguagem Python",
  "data": "2026-11-20",
  "horario": "19:00:00",
  "local": "Laboratório 3",
  "capacidade": 40,
  "categoria": "Workshop"
}
```

Cadastrar participante — `POST /participantes`

```json
{
  "nome": "Maria Silva",
  "email": "maria@email.com",
  "curso": "Engenharia de Software"
}
```

Inscrever — `POST /eventos/1/inscricoes/1` — resposta (201):

```json
{
  "id": 1,
  "evento_id": 1,
  "participante_id": 1,
  "data_inscricao": "2026-10-28"
}
```

Inscrição duplicada (409):

```json
{
  "detail": "Participante já está inscrito neste evento."
}
```

## Como reproduzir os testes (Swagger)

Abra http://127.0.0.1:8000/docs e siga a ordem abaixo.

1. **Eventos:** `POST /eventos` para criar 2 ou 3 eventos (use categorias diferentes e
   capacidade 1 em um deles) e confira com `GET /eventos` e `GET /eventos/{id}`.
2. **Participantes:** `POST /participantes` para criar 3 participantes (dois no mesmo curso)
   e confira com `GET /participantes`.
3. **Atualização e exclusão:** use `PUT` e `DELETE` em um evento e em um participante.
4. **Inscrição:** `POST /eventos/1/inscricoes/1`, depois confira em `GET /eventos/1/inscricoes`.
5. **Inscrição duplicada:** repita o passo 4 e verifique o 409.
6. **Evento inexistente:** `POST /eventos/999/inscricoes/1` e verifique o 404.
7. **Sem vagas:** inscreva um segundo participante no evento de capacidade 1 e verifique o 409.
8. **Persistência:** pare o servidor (Ctrl+C), rode `uvicorn main:app --reload` de novo e
   consulte `GET /eventos` e `GET /participantes`. Os dados continuam lá.
9. **Ocupação:** `GET /relatorios/eventos/ocupacao`.
10. **Categorias:** `GET /relatorios/eventos/categorias`.
11. **Cursos:** `GET /relatorios/participantes/cursos`.
12. **Relatórios atualizando:** faça novas inscrições, altere a capacidade de um evento,
    exclua um evento ou um participante e consulte os três relatórios de novo. Os números
    mudam conforme os dados do banco.
13. **Validações:** envie título vazio, capacidade 0 ou negativa, e-mail inválido, horário
    inválido (ex: `25:99`) e e-mail repetido, e confira os erros 422 e 409.

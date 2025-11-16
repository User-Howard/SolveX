# SolveX API Documentation

**Base URL:** `http://<host>:8000`

All responses are JSON. Timestamps use ISO 8601. Errors follow FastAPI’s default shape `{"detail": "...message..."}` unless stated otherwise.

---

## 1. Users

| Method & Path | Description |
| --- | --- |
| `POST /users` | Create a user. Body: `{ username, email, password, first_name?, last_name? }`. Returns `201` with created user. |
| `GET /users/{user_id}` | Fetch a user record. |
| `PATCH /users/{user_id}` | Partially update (username/email remain unique). |
| `GET /users/{user_id}/problems` | Problems authored by the user, newest first. |
| `GET /users/{user_id}/resources` | Resources created by the user, sorted by last visit time. |

---

## 2. Problems

| Method & Path | Description |
| --- | --- |
| `POST /problems` | Body: `{ user_id, title, description?, problem_type?, tags?: [tag_id] }`. Returns the created problem. Tags must exist. |
| `GET /problems/{problem_id}` | Problem plus author info. |
| `PATCH /problems/{problem_id}` | Update `title`, `description`, `problem_type`, or `resolved`. |
| `DELETE /problems/{problem_id}` | Returns `{ "deleted": true }`. |
| `GET /problems` | Query params: `keyword`, `type`, `tag` (optional, case-insensitive). Returns matching problems ordered by `created_at`. |
| `POST /problems/{problem_id}/resolve` | Sets `resolved = true`. |
| `GET /problems/{problem_id}/full` | Returns `{ problem, solutions[], tags[], linked_resources[], relations_out[], relations_in[] }`. Useful for detail pages. |

---

## 3. Solutions

| Method & Path | Description |
| --- | --- |
| `POST /problems/{problem_id}/solutions` | Body: `{ problem_id (must match path), code_snippet, explanation?, approach_type?, parent_solution_id?, improvement_description?, success_rate?, branch_type? }`. |
| `GET /solutions/{solution_id}` | Returns `SolutionDetail` including parent info and child count. |
| `PATCH /solutions/{solution_id}` | Edits any mutable field (validates parent/problem). |
| `DELETE /solutions/{solution_id}` | `{ "deleted": true }`. |
| `GET /problems/{problem_id}/solutions` | Solutions for a problem (descending `created_at`). |
| `GET /solutions/{solution_id}/children` | Version tree branch below the given solution. |

---

## 4. Resources

| Method & Path | Description |
| --- | --- |
| `POST /resources` | Body: `{ user_id, url, title?, source_platform?, content_summary?, usefulness_score? }`. Sets visit timestamps to now. |
| `GET /resources/{resource_id}` | Returns `ResourceDetail` (linked problems, solutions, tags). |
| `PATCH /resources/{resource_id}` | Update title, summary, or usefulness. |
| `POST /resources/{resource_id}/visit` | Refreshes visit timestamps. |
| `GET /resources` | Query params: `tag`, `min_score`, `keyword`. Returns matches ordered by last visit. |

---

## 5. Tags

| Method & Path | Description |
| --- | --- |
| `POST /tags` | Create `{ tag_name, category?, description? }` (unique name). |
| `GET /tags` | List all tags alphabetically. |
| `POST /problems/{problem_id}/tags` | Assign tag `{ tag_id }` to a problem. |
| `DELETE /problems/{problem_id}/tags/{tag_id}` | Remove tag from problem. |
| `POST /resources/{resource_id}/tags` | Assign tag `{ tag_id, confidence? }` to resource (updates confidence if exists). |
| `DELETE /resources/{resource_id}/tags/{tag_id}` | Remove tag from resource. |

---

## 6. Relations & Attachments

| Method & Path | Description |
| --- | --- |
| `POST /problems/{problem_id}/relations` | Body: `{ to_problem_id, relation_type?, strength? }` (0–1 strength, no duplicates). |
| `DELETE /problems/{problem_id}/relations/{to_problem_id}` | Remove relation. |
| `GET /problems/{problem_id}/relations/out` | Outgoing relations. |
| `GET /problems/{problem_id}/relations/in` | Incoming relations. |
| `POST /problems/{problem_id}/resources` | Attach resource `{ resource_id, relevance_score?, contribution_type? }`. Returns full problem payload. |
| `DELETE /problems/{problem_id}/resources/{resource_id}` | Detach resource (full problem payload). |
| `POST /solutions/{solution_id}/resources` | Attach resource to solution. |
| `DELETE /solutions/{solution_id}/resources/{resource_id}` | Detach resource from solution. |

---

## 7. Dashboard & Health

| Method & Path | Description |
| --- | --- |
| `GET /dashboard/{user_id}` | Returns `{ recent_problems[], recent_solutions[], top_tags[], top_resources[] }`. Lists limited to 10/top 5. |
| `GET /health` | `{ "status": "ok" }`. |
| `GET /` | `{ "message": "Hello" }`. |

---

## Schemas & Validation Notes

- All response bodies come from Pydantic models defined in `src/api/schemas`. They enforce numeric ranges (`success_rate` 0–100, `usefulness_score` 0–5, relation strength 0–1).
- Nested responses (e.g., `ProblemFull`, `ResourceDetail`) include related entities and their metadata.
- Standard FastAPI error responses (`404` for missing resources, `400` for constraint violations) are returned automatically.

---

## Environment

- Default DB: Postgres (`DATABASE_URL` env variable). Compose file also wires `LOAD_FAKE_DATA=true` when desired.
- Authentication is not yet implemented; add middleware before exposing publicly.


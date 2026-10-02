# AGENTS.md — Protocolo de trabajo

Este documento es la fuente de verdad para cualquier agente (Claude, Codex, Copilot, etc.) o persona que trabaje en **my-project**. Si una instrucción puntual del usuario contradice este archivo, manda la del usuario; si el cambio es permanente, actualiza este archivo en el mismo PR.

---

## 1. Principios

1. **Nada entra en `main` sin PR.** `main` siempre compila y pasa los tests.
2. **Una tarea = un issue = una rama = un PR.** Si el trabajo crece, se divide en issues nuevos.
3. **Cambios pequeños y revisables.** Objetivo: PR de < 400 líneas cambiadas (sin contar lockfiles/generados).
4. **El estado vive en GitHub, no en la cabeza del agente.** Decisiones, bloqueos y avances se escriben en el issue o el PR.
5. **Ante la duda, pregunta antes de actuar** en acciones irreversibles (force-push, borrar ramas ajenas, cerrar issues de otros, cambiar settings del repo).

---

## 2. Flujo de trabajo (GitHub Flow)

```
issue ──► rama ──► commits ──► PR (draft) ──► CI verde ──► review ──► squash merge ──► borrar rama
```

### 2.1 Antes de empezar
- Busca si ya existe un issue: `gh issue list --search "<palabras>"`.
- Si no existe, créalo con la plantilla adecuada (`gh issue create`). Todo issue lleva:
  - **Tipo** (label): `type:feature`, `type:bug`, `type:refactor`, `type:docs`, `type:chore`.
  - **Área** (label, opcional): `area:core`, `area:ui`, `area:infra`...
  - **Criterios de aceptación** verificables (checklist).
- Asígnate el issue (`gh issue edit <n> --add-assignee @me`) para evitar trabajo duplicado entre agentes.

### 2.2 Ramas
- Siempre desde `main` actualizado: `git switch main && git pull --ff-only`.
- Nombre: `<tipo>/<n-issue>-<descripcion-corta-kebab>`
  - `feat/12-exportar-csv`
  - `fix/34-fecha-invalida`
  - `refactor/40-separar-capa-datos`
  - `docs/5-protocolo-agentes`
  - `chore/8-configurar-ci`
- Una rama por issue. No reutilizar ramas mergeadas.
- **Varios agentes en paralelo:** cada uno en su propia rama (o `git worktree`). Nunca dos agentes en la misma rama.

### 2.3 Commits — Conventional Commits
Formato: `<tipo>(<ámbito opcional>): <resumen en imperativo>`

```
feat(export): añadir exportación a CSV
fix(parser): evitar división por cero con entrada vacía
refactor(core): extraer validación a un módulo propio
test(export): cubrir caso de lista vacía
docs: documentar estructura de carpetas
chore(ci): cachear dependencias
```

- Tipos permitidos: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `style`, `build`, `ci`, `chore`, `revert`.
- Resumen ≤ 72 caracteres, sin punto final, en español.
- Cuerpo (opcional) explica el **por qué**, no el qué.
- Cambio incompatible: `feat!:` y una línea `BREAKING CHANGE: ...` en el cuerpo.
- Commits atómicos: cada commit compila. Nada de "wip", "fix typo 3".
- Commits hechos por un agente terminan con su línea `Co-Authored-By:` correspondiente.

### 2.4 Pull Requests
- Abre el PR pronto como **draft**: `gh pr create --draft --fill`.
- Título = mismo formato que un commit (será el mensaje del squash).
- Cuerpo según [.github/pull_request_template.md](.github/pull_request_template.md). Debe incluir `Closes #<n>`.
- Antes de marcarlo *ready for review*:
  - [ ] Rebase sobre `main` (`git fetch && git rebase origin/main`), sin conflictos.
  - [ ] Lint, formato y tests pasan en local.
  - [ ] Tests nuevos para lógica nueva o bugs corregidos.
  - [ ] Docs actualizadas si cambia comportamiento, estructura o comandos.
  - [ ] Entrada en `CHANGELOG.md` → `[Unreleased]` si cambia algo visible para el usuario.
  - [ ] El diff no incluye ficheros ajenos a la tarea, secretos ni artefactos generados.
- Estrategia de merge: **squash and merge** únicamente. Borrar la rama tras el merge.

### 2.5 Revisión
- Un agente **no aprueba ni mergea su propio PR** salvo que el usuario lo autorice explícitamente.
- Los comentarios de review se resuelven con commits nuevos (no force-push durante la review, salvo rebase pedido).
- Quien revisa marca hallazgos como: `bloqueante`, `sugerencia` o `pregunta`.

### 2.6 Releases
**Proceso completo: [docs/versioning.md](docs/versioning.md).** Resumen:

- **SemVer** (`MAJOR.MINOR.PATCH`). En `0.x`, lo incompatible sube MINOR.
- Única fuente de la versión: `version` en `pyproject.toml`. El tag `vX.Y.Z` debe coincidir.
- Nunca carpetas ni copias por versión: las versiones son tags de Git.
- Release = PR `chore(release): vX.Y.Z` (sube versión + cierra `[Unreleased]` del CHANGELOG) → merge → tag anotado → `gh release create`.
- Los tags publicados no se mueven ni se borran.

---

## 3. Prohibido (sin permiso explícito del usuario)

- `git push --force` a `main` o a ramas de otros. En tu propia rama, solo `--force-with-lease`.
- Commit directo a `main`.
- Commitear secretos, `.env`, credenciales o datos personales.
- Desactivar tests, lint o checks de CI para "que pase".
- Cambiar la configuración del repositorio (branch protection, secrets, colaboradores).
- Añadir dependencias pesadas sin justificarlo en el PR.

---

## 4. Estructura del proyecto

Python ≥ 3.11, *src layout*. **Guía completa: [docs/project-structure.md](docs/project-structure.md)**. Léela antes de crear archivos o carpetas.

Resumen:
- Código en `src/my_project/{core,persistence,ui}/`. Cada `__init__.py` declara la responsabilidad del subpaquete y de quién puede depender.
- Tests en `tests/`, misma estructura que `src/my_project/`.
- Utilidades de desarrollo en `scripts/`; documentación en `docs/`.
- Dependencias: `core` no depende de nadie, `persistence` solo de `core`, y nadie importa `ui`. Lo comprueba `tests/test_architecture.py`: si falla, se corrige el import, no el test.
- Una carpeta o subpaquete de primer nivel nuevo requiere issue + ADR antes de crearse.
- Identificadores en inglés; docstrings, comentarios y documentación en español.

---

## 5. Comandos

Ejecútalos antes de abrir o actualizar un PR.

| Acción       | Comando |
|--------------|---------|
| Entorno      | `python3 -m venv .venv && source .venv/bin/activate` |
| Instalar     | `pip install -e ".[dev]"` |
| Ejecutar     | `my-project` (o `python -m my_project`) |
| Tests        | `pytest` |
| Lint         | `ruff check .` |
| Formato      | `ruff format .` (CI comprueba con `ruff format --check .`) |

---

## 6. Checklist rápido para agentes

1. Leer este archivo y el issue asignado.
2. `git switch main && git pull --ff-only && git switch -c <tipo>/<n>-<desc>`
3. Implementar en commits pequeños y convencionales.
4. Ejecutar tests + lint.
5. `git push -u origin HEAD && gh pr create --draft --fill` (con `Closes #<n>`).
6. Completar la plantilla del PR, marcar *ready*, esperar review.
7. Informar al usuario: enlace al PR, qué se hizo, qué queda pendiente.

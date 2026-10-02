# Mapa del proyecto: dónde está y dónde va cada cosa

Antes de crear un archivo, consulta esta guía. Si algo no encaja en ningún sitio, **no inventes una carpeta**: abre un issue y propón el cambio con un ADR (ver [adr/](adr/)).

---

## 1. Vista general

```
my-project/
├── AGENTS.md                  # Protocolo de trabajo (GitHub, ramas, commits, PRs)
├── CLAUDE.md                  # Importa AGENTS.md para Claude Code
├── README.md                  # Qué es el proyecto y cómo arrancarlo
├── CHANGELOG.md               # Historial de cambios por versión
├── pyproject.toml             # Metadatos, VERSIÓN, dependencias y config de herramientas
├── .editorconfig              # Estilo básico común a todos los editores
├── .gitignore                 # Lo que Git nunca debe guardar
│
├── .github/
│   ├── workflows/             # CI: lint, tipos y tests (ci.yml); convenciones del PR (pr.yml)
│   ├── dependabot.yml         # Actualización automática de dependencias y acciones
│   ├── ISSUE_TEMPLATE/        # Plantillas de issues (feature, bug, tarea)
│   └── pull_request_template.md
│
├── docs/
│   ├── project-structure.md   # ← este archivo
│   ├── architecture.md        # Cómo funciona el sistema por dentro
│   ├── versioning.md          # Cómo se versiona y se publica una release
│   └── adr/                   # Registro de decisiones de arquitectura
│
├── src/my_project/            # CÓDIGO DEL PROYECTO (el paquete Python)
│   ├── __init__.py            # Expone __version__
│   └── __main__.py            # Punto de entrada (python -m my_project)
│
├── tests/                     # Pruebas: misma estructura que src/my_project/
│   └── test_package.py
│
└── scripts/                   # Utilidades de desarrollo (no forman parte del paquete)
```

---

## 2. Qué va en cada carpeta

### `src/my_project/`: el producto
Todo el código que se instala con el paquete. Usamos el *src layout*: así los tests se ejecutan siempre contra el paquete instalado, nunca contra archivos sueltos.

Cuando el código crezca, se divide en subpaquetes. Cada subpaquete describe en su `__init__.py` su responsabilidad y de qué puede depender. **Léelo antes de añadir código ahí.**

| Subpaquete | Contiene | Ejemplos de archivos |
|------------|----------|----------------------|
|            |          |                      |

### `tests/`: las pruebas
- **Espejo de `src/`**: el test de `src/my_project/export/csv.py` va en `tests/export/test_csv.py`.
- Archivos `test_<modulo>.py`, funciones `test_<comportamiento>()`.
- Fixtures compartidas en `conftest.py`, en la carpeta del nivel más bajo donde se usen.
- Si un test necesita aleatoriedad, **fija la semilla**.

### `docs/`: documentación para humanos
- `architecture.md`: visión técnica general. Se actualiza cuando cambia un módulo o una relación entre módulos.
- `adr/`: una decisión importante = un archivo numerado. Ver [adr/0000-template.md](adr/0000-template.md).
- `versioning.md`: proceso de versiones y releases.

### `scripts/`: herramientas auxiliares
Scripts de desarrollo: generar datos de prueba, perfilar rendimiento, etc. **No** se importan desde `src/`. Si un script se vuelve útil para el usuario final, se convierte en un comando del paquete.

### `.github/`: automatización del proceso
CI y plantillas. Se modifica solo con un PR de tipo `ci:` o `chore:`.

---

## 3. Reglas de dependencia entre módulos

Las dependencias entre subpaquetes van en **una sola dirección**: lo más estable abajo, lo más cambiante arriba. Nunca en círculo.

<!-- Dibuja aquí el diagrama cuando haya más de un subpaquete. Las flechas apuntan hacia lo que se puede importar. -->

Reglas de partida:
- El núcleo del dominio no depende de nadie.
- La lógica del dominio no importa la entrada/salida (archivos, red, base de datos) ni la interfaz.
- Nadie importa la interfaz (CLI, web).

---

## 4. Decidir dónde va algo nuevo

| Si vas a…                                  | Va en                                   |
|--------------------------------------------|-----------------------------------------|
| Añadir lógica del proyecto                 | `src/my_project/`                       |
| Añadir un test                             | `tests/`, en la ruta espejo             |
| Añadir un script de desarrollo             | `scripts/`                              |
| Añadir una dependencia                     | `pyproject.toml` (justifícalo en el PR) |
| Tomar una decisión de diseño no trivial    | `docs/adr/NNNN-titulo.md`               |
| Crear un subpaquete nuevo de primer nivel  | Issue + ADR **antes** de crearlo        |

**Cuándo dividir un archivo:** si un módulo supera unas 300-400 líneas o mezcla dos responsabilidades, se convierte en un subpaquete (`export.py` → `export/__init__.py`, `export/csv.py`...).

---

## 5. Convenciones de nombres

| Elemento         | Convención              | Ejemplo                     |
|------------------|-------------------------|-----------------------------|
| Paquetes/módulos | `snake_case`, singular  | `export/csv.py`             |
| Clases           | `PascalCase`            | `class Report`              |
| Funciones/vars   | `snake_case`            | `compute_total()`           |
| Constantes       | `UPPER_SNAKE_CASE`      | `MAX_RETRIES`               |
| Privado          | prefijo `_`             | `_update_cache()`           |
| Tests            | `test_<qué>.py`         | `tests/export/test_csv.py`  |
| ADRs             | `NNNN-titulo-kebab.md`  | `0003-formato-de-datos.md`  |

El código (identificadores) se escribe en **inglés**. Docstrings, comentarios y documentación, en **español**.

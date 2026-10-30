# Semana08 — API de cuestionarios con Django REST Framework

Implementación de los once requisitos del laboratorio: exámenes, preguntas y opciones,
API navegable, cliente HTTP JSON, validaciones, filtros, búsqueda y paginación.

- [Entregable y tabla de la API](docs/ENTREGABLE.md)
- [Recorrido real en navegador](docs/evidencias/navegador.md)
- [Peticiones y respuestas del cliente HTTP](docs/evidencias/http.json)
- [Laboratorio adicional de cliente y agente](docs/LAB_EXTRA.md)

## Instalación y ejecución (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre http://127.0.0.1:8000/api/ e inicia sesión con el superusuario creado.
La sesión permite usar los formularios de DRF y protege las escrituras con CSRF.
Para preguntas usa **Raw data**, `application/json` y las opciones anidadas.
En los detalles Raw data ofrece **PATCH**. DELETE abre una confirmación.
OpenAPI: `/api/docs/`; esquema: `/api/schema/`.

## Datos de muestra en una base aislada

`seed_quiz` carga 2 exámenes y 8 preguntas y muestra tokens de profe y agente.
**Reemplaza los exámenes existentes y sus preguntas/opciones.** Usa una base
de prácticas que puedas reemplazar. Para aislarla:

```powershell
New-Item -ItemType Directory -Force work | Out-Null
$env:QUIZ_DB = "$PWD\work\practica.sqlite3"
python manage.py migrate
python manage.py seed_quiz
python manage.py createsuperuser
python manage.py runserver
```

## Cliente HTTP externo y evidencias

En otra terminal, usando un token de usuario staff de esa misma base:

```powershell
$env:QUIZ_TOKEN = "TOKEN_MOSTRADO_POR_SEED"
python scripts/verificar_http.py --url http://127.0.0.1:8000
```

Realiza 32 peticiones reales con requests, envía JSON y comprueba estados,
contenido, errores y dos páginas. Solo elimina los registros que él crea.
Guarda las respuestas en `docs/evidencias/http.json`, sin guardar el token.
Para un superusuario propio también puedes obtener su token con
`python manage.py drf_create_token NOMBRE_DE_USUARIO`.

## Pruebas

```powershell
python manage.py test
python manage.py check
```

En entornos que restringen la carpeta temporal del sistema:

```powershell
New-Item -ItemType Directory -Force work\tmp | Out-Null
$env:TEMP = "$PWD\work\tmp"
$env:TMP = $env:TEMP
python manage.py test
```

No se necesitan claves de IA ni un modelo local para comprobar este laboratorio.

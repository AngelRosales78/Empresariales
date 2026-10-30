# Laboratorio Semana08 — API de cuestionarios

Fecha de verificación: 30 de octubre de 2026 (America/Lima).

## 1. Instalación, estructura y configuración

Proyecto Django con `manage.py`, `config/` y aplicación `quiz/`. Las dependencias
están declaradas en `requirements.txt`: Django, djangorestframework,
drf-spectacular y requests. Se comprobó su instalación.

`INSTALLED_APPS` incluye `rest_framework`, `quiz`, autenticación, tokens,
sesiones y archivos estáticos. `TEMPLATES` utiliza APP_DIRS para cargar los
formularios de DRF. Los middlewares habilitan sesiones, autenticación y CSRF.

`REST_FRAMEWORK` establece PageNumberPagination, PAGE_SIZE=5,
IsAuthenticated y AgentPermission. Se acepta token y sesión. Usuario staff:
CRUD completo; grupo agente: consultar, crear y editar, sin eliminar;
otros usuarios autenticados: lectura. Sin identidad válida: 401.

## 2. Serializadores y relaciones

ExamSerializer, QuestionSerializer y ChoiceSerializer usan ModelSerializer.
Examen: id, title, created_at y question_count. Pregunta: id, exam, text,
choices y created_at. Opción independiente: id, question, text, is_correct.
Los identificadores y fechas son de solo lectura; question_count también.

Decisión: `exam` es un identificador de un examen existente. Las opciones
viajan anidadas en `choices` para crear una pregunta válida de forma atómica.
La representación anidada omite question porque el padre ya está determinado.
En `/api/choices/`, question se envía por identificador y es obligatorio.
Una opción existente no puede trasladarse a otra pregunta.

POST de pregunta crea padre e hijos en una transacción. En PATCH, omitir
choices conserva las opciones. Enviar choices reemplaza todas las anteriores,
incluidos sus identificadores. Se requieren al menos dos opciones y exactamente
una correcta. Para cambiar cuál es correcta se envía el conjunto completo en
PATCH de la pregunta. Las escrituras individuales de opciones también protegen
estas condiciones; no se puede borrar la única correcta ni el último distractor.

## 3. Vistas y rutas

Los tres recursos utilizan ModelViewSet y DefaultRouter en `quiz/urls.py`.
`config/urls.py` incluye estas rutas bajo `/api/`. Inicio de sesión:
`/api-auth/login/`; esquema: `/api/schema/`; Swagger: `/api/docs/`.
La API navegable de DRF y Swagger son interfaces distintas.

## 4. Tabla de la API

Base habitual: `http://127.0.0.1:8000`. Los identificadores de ejemplo deben
reemplazarse por los devueltos en POST. Los cuerpos se envían como JSON.

| Recurso | Dirección | Método | Cuerpo de ejemplo | Respuesta esperada |
|---|---|---|---|---|
| Examen | `/api/exams/` | GET | — | 200, count/next/previous/results |
| Examen | `/api/exams/1/` | GET | — | 200, examen con question_count |
| Examen | `/api/exams/` | POST | `{"title":"Examen REST"}` | 201, id/title/created_at |
| Examen | `/api/exams/1/` | PUT | `{"title":"Examen completo"}` | 200, examen actualizado |
| Examen | `/api/exams/1/` | PATCH | `{"title":"Nuevo título"}` | 200, examen actualizado |
| Examen | `/api/exams/1/` | DELETE | — | 204 sin cuerpo; elimina preguntas y opciones en cascada |
| Pregunta | `/api/questions/` | GET | — | 200, lista paginada con choices anidadas |
| Pregunta | `/api/questions/1/` | GET | — | 200, pregunta y sus opciones |
| Pregunta | `/api/questions/` | POST | Cuerpo A, abajo | 201, pregunta y opciones con id |
| Pregunta | `/api/questions/1/` | PUT | Cuerpo A, abajo | 200, reemplazo de datos y opciones |
| Pregunta | `/api/questions/1/` | PATCH | `{"text":"Enunciado corregido"}` | 200, conserva examen y opciones |
| Pregunta | `/api/questions/1/` | DELETE | — | 204 sin cuerpo; elimina sus opciones |
| Opción | `/api/choices/` | GET | — | 200, lista paginada |
| Opción | `/api/choices/1/` | GET | — | 200, opción y question |
| Opción | `/api/choices/` | POST | `{"question":1,"text":"Distractor adicional","is_correct":false}` | 201, opción con id |
| Opción | `/api/choices/1/` | PUT | `{"question":1,"text":"Texto completo","is_correct":false}` | 200 si mantiene la regla |
| Opción | `/api/choices/1/` | PATCH | `{"text":"Distractor corregido"}` | 200, opción actualizada |
| Opción | `/api/choices/1/` | DELETE | — | 204 si quedan al menos dos opciones y una correcta; en otro caso 400 |

Cuerpo A:

```json
{
  "exam": 1,
  "text": "¿Qué es REST?",
  "choices": [
    {"text": "Estilo de arquitectura", "is_correct": true},
    {"text": "Lenguaje", "is_correct": false}
  ]
}
```

Ejemplo de respuesta de pregunta (las fechas e identificadores son ilustrativos):

```json
{
  "id": 9,
  "exam": 1,
  "text": "¿Qué es REST?",
  "choices": [
    {"id": 33, "text": "Estilo de arquitectura", "is_correct": true},
    {"id": 34, "text": "Lenguaje", "is_correct": false}
  ],
  "created_at": "2026-10-30T14:00:00-05:00"
}
```

GET de un id inexistente devuelve 404. JSON inválido o campos inválidos: 400.
Usuario autenticado sin permiso de escritura: 403. Sesión sin CSRF en una
escritura: 403. Token: cabecera `Authorization: Token TOKEN`; JSON:
`Content-Type: application/json` y `Accept: application/json`.

## 5. Recorrido en navegador y cliente HTTP externo

Se levantó un servidor real en `127.0.0.1:8018`, con base SQLite independiente,
sin reemplazar `db.sqlite3` del laboratorio. Se inició sesión en DRF y se
realizaron listar, detalle, POST, PATCH y DELETE en los tres recursos.
El registro de estados está en [navegador.md](evidencias/navegador.md).

Se repitieron las operaciones mediante `requests` con cuerpos JSON, usando
`scripts/verificar_http.py`. El cliente efectuó 32 peticiones y comprobó tanto
los códigos como los campos actualizados y los listados. Las respuestas
completas están en [http.json](evidencias/http.json), sin guardar credenciales.
En ambos canales se obtuvo 200 para listado/detalle/PATCH, 201 para POST y
204 para DELETE. Las diferencias de id, fecha y datos iniciales son esperadas:
son registros distintos de prueba. En ambos se conservó la relación padre-hijos.

En DELETE, 204 es el código de la operación que muestra el panel de DRF y
el que recibe el cliente JSON. El renderer navegable cambia el transporte de
su página HTML a 200 para mostrar la confirmación visual; se registró esta
distinción en navegador.md. La eliminación y los demás resultados coinciden.

## 6. Errores deliberados

Los tres casos se ejecutaron por POST de pregunta con dos opciones:
omitir text; exam con cadena no numérica; y dos opciones correctas.
Los mensajes exactos y estados observados se registran al final de este informe,
extraídos de http.json. También se comprobó cero opciones correctas (400).

## 7. Filtrado, búsqueda y paginación

`GET /api/questions/?exam=1` filtra por examen.
`GET /api/questions/?search=select_related` busca en el enunciado.
Se pueden combinar: `?exam=1&search=select_related` devolvió una pregunta
en el navegador (200). El cliente verificó filtro y búsqueda sobre su examen.

Con las ocho preguntas de muestra, el navegador mostró cinco en la primera
página y tres en `?page=2`; next fue null en la segunda. El cliente generó siete
preguntas en un examen propio y comprobó cinco y dos en páginas consecutivas,
con next/previous correctos. El tamaño de página es 5 para los tres recursos.

## 8. Reproducción

Sigue la instalación de README.md. Para el navegador, crea un superusuario,
inicia sesión, usa Raw data con application/json y pulsa POST o PATCH.
DELETE solicita confirmación. El cuerpo de una pregunta debe incluir choices.

En otra terminal:

```powershell
$env:QUIZ_TOKEN = "TOKEN_DE_UN_USUARIO_STAFF"
python scripts/verificar_http.py --url http://127.0.0.1:8000
python manage.py test
python manage.py check
```

El script crea sus propios datos y los elimina al terminar correctamente.
No ejecutes seed_quiz sobre datos que quieras conservar: ese comando reemplaza
los exámenes y sus relaciones. QUIZ_DB permite elegir una base de prácticas.


## 9. Mensajes exactos y resultado final

| Caso ejecutado | Estado HTTP | Respuesta JSON real |
|---|---|---|
| Falta text | 400 | `{"text": ["Este campo es requerido."]}` |
| exam con tipo incorrecto | 400 | `{"exam": ["Tipo incorrecto. Se esperaba valor de clave primaria y se recibió str."]}` |
| Dos opciones correctas | 400 | `{"choices": ["Debe haber exactamente una opción correcta."]}` |
| Ninguna opción correcta | 400 | `{"choices": ["Debe haber exactamente una opción correcta."]}` |

Validación final: **70 pruebas aprobadas**, sin fallos. El registro está en
`evidencias/pruebas.txt`. `manage.py check` no detectó problemas;
`makemigrations --check --dry-run` no detectó cambios de modelos y el esquema
OpenAPI se generó y validó en `openapi.yml`.

| Requisito | Evidencia entregada |
|---|---|
| 1. Proyecto, instalación y apps | requirements.txt; config/settings.py; README |
| 2. REST_FRAMEWORK | settings.py: permisos, autenticación y página de 5 |
| 3. ModelSerializer | quiz/serializers.py; campos y solo lectura explícitos |
| 4. Relaciones | Sección 2 de este documento |
| 5. Validación propia | validate_choices y pruebas; se protegen también opciones independientes |
| 6. ViewSets y router | quiz/views.py, quiz/urls.py y config/urls.py |
| 7. Servidor y API navegable | evidencias/navegador.md y capturas JPG |
| 8. Cliente HTTP externo JSON | scripts/verificar_http.py; 32 peticiones en evidencias/http.json |
| 9. Tres errores | Tabla de mensajes reales anterior y http.json |
| 10. Filtro, búsqueda y dos páginas | Sección 7; pruebas y capturas |
| 11. Tabla de API | Sección 4 con direcciones, métodos, cuerpos y respuestas |

Las pruebas se hicieron sobre datos aislados. La base original se conservó;
solo se aplicó la migración necesaria para sesiones. El servidor de verificación
se utiliza únicamente para desarrollo local.

# Registro de la API navegable

30/10/2026, America/Lima. Servidor real: http://127.0.0.1:8018.
Base aislada de verificación; se conservaron los datos originales del laboratorio.
Interfaz: Django REST Framework, autenticación por sesión con usuario staff profe.
POST y PATCH mediante formularios/Raw data; DELETE mediante su confirmación.

| Recurso | Operación | Dirección | Estado observado |
|---|---|---|---|
| Examen | Listar GET | `/api/exams/` | 200 |
| Examen | Crear POST | `/api/exams/` | 201, id=3 |
| Examen | Detalle GET | `/api/exams/3/` | 200 |
| Examen | Parcial PATCH | `/api/exams/3/` | 200 |
| Examen | Eliminar DELETE | `/api/exams/3/` | 204 |
| Pregunta | Listar GET | `/api/questions/` | 200, 8 resultados en total, 5 en página 1 |
| Pregunta | Crear POST | `/api/questions/` | 201, id=9, dos opciones |
| Pregunta | Detalle GET | `/api/questions/9/` | 200 |
| Pregunta | Parcial PATCH | `/api/questions/9/` | 200, conserva opciones |
| Pregunta | Eliminar DELETE | `/api/questions/9/` | 204 |
| Opción | Listar GET | `/api/choices/?question=9` | 200 |
| Opción | Crear POST | `/api/choices/?question=9` | 201, id=50 |
| Opción | Detalle GET | `/api/choices/50/` | 200 |
| Opción | Parcial PATCH | `/api/choices/50/` | 200 |
| Opción | Eliminar DELETE | `/api/choices/50/` | 204 |
| Pregunta | Página 2 GET | `/api/questions/?page=2` | 200, 3 resultados, next=null |
| Pregunta | Filtro y búsqueda GET | `/api/questions/?exam=1&search=select_related` | 200, count=1 |

Examen POST: `{"title":"Verificación navegador Semana08"}`.
PATCH: `{"title":"Examen navegador modificado"}`.

Pregunta POST:

```json
{"exam":3,"text":"¿Qué es REST?","choices":[{"text":"Estilo de arquitectura","is_correct":true},{"text":"Lenguaje","is_correct":false}]}
```

Pregunta PATCH: `{"text":"¿Qué significa REST?"}`.

Opción POST: `{"question":9,"text":"Distractor adicional","is_correct":false}`.
Opción PATCH: `{"text":"Distractor modificado"}`.

Las eliminaciones se realizaron en orden opción, pregunta, examen.
Solo se eliminaron los datos temporales creados para este recorrido.
Antes de iniciar sesión, GET de exámenes devolvió 401.

Nota sobre DELETE: el panel de DRF muestra el estado de la operación **204**.
BrowsableAPIRenderer entrega la página HTML contenedora con **200** para poder
mostrar ese resultado en el navegador. El cliente JSON recibe **204** real,
sin cuerpo. Es el comportamiento de presentación de DRF, no una diferencia
en la eliminación. Los códigos de la tabla corresponden al panel de la API;
el transporte HTML de las tres eliminaciones fue 200.

Las mismas operaciones desde requests están registradas en `http.json`:
listado/detalle/PATCH=200, POST=201 y DELETE=204 en los tres recursos.
Las capturas de eliminación, paginación y búsqueda están en esta carpeta.

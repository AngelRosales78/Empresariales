# Tres errores de React provocados y corregidos

Fecha: 30 de octubre de 2026, America/Lima.
Entorno real: Node 22.23.3, npm 10.9.9, React 19.3.1, Vite 8.3.5.
Se abrió `/laboratorio-errores.html` en el servidor Vite y se cambió un ejemplo
aislado. La aplicación principal no se modificó para provocar los errores.

## 1. Usar class en lugar de className

Código erróneo ejecutado:

```jsx
export default function Example() {
  return <div class="demo">Error deliberado: class en vez de className</div>
}
```

Mensaje observado en el servidor y la consola de desarrollo de React:

```text
Invalid DOM property `class`. Did you mean `className`?
```

Es una advertencia de desarrollo registrada con console.error: en esta versión
el elemento sigue apareciendo en pantalla. No equivale a un fallo de compilación.
El registro sin formatear conserva los placeholders `%s`, que el navegador
sustituye por `class` y `className`.

Corrección: `<div className="demo">...</div>`.
Evidencia: [error-class.json](evidencias/error-class.json).

## 2. Devolver dos nodos raíz

Código erróneo ejecutado:

```jsx
export default function Example() {
  return (
    <h1>Primer nodo</h1>
    <p>Segundo nodo sin fragmento</p>
  )
}
```

Mensaje real de Vite/Oxc:

```text
[PARSE_ERROR] Adjacent JSX elements must be wrapped in an enclosing tag.
Help: Did you want a JSX fragment `<>...</>`?
```

Ubicación: `experiments/Example.jsx:3:3`. El módulo respondió HTTP 500 y
la página de pruebas no pudo dibujarse. La consola también registró:

```text
[vite] Failed to reload /experiments/Example.jsx. This could be due to syntax errors or importing non-existent modules. (see errors above)
```

Corrección: envolver ambos nodos en un fragmento:

```jsx
return (
  <>
    <h1>Primer nodo</h1>
    <p>Segundo nodo con fragmento</p>
  </>
)
```

Evidencia: [respuesta HTTP del módulo](evidencias/error-roots.txt) y
[consola del navegador](evidencias/error-roots-console.json).

## 3. Olvidar key en map

Código erróneo ejecutado:

```jsx
export default function Example() {
  return <ul>{['Órbita', 'Medianoche'].map((title) => <li>{title}</li>)}</ul>
}
```

Mensaje real de React:

```text
Each child in a list should have a unique "key" prop.
Check the render method of `Example`.
```

La lista aparece, pero React advierte porque no puede identificar establemente
sus elementos entre actualizaciones. En el ejemplo, los títulos son únicos y
se corrige con `<li key={title}>{title}</li>`. En la aplicación real se usan los
identificadores estables de las películas:

```jsx
filteredMovies.map((movie) => <MovieCard key={movie.id} movie={movie} />)
```

Evidencia: [error-key.json](evidencias/error-key.json).

## Repetir la práctica

Con `npm run dev` activo, ejecutar uno por uno:

```powershell
node scripts/error-demo.mjs class
node scripts/error-demo.mjs roots
node scripts/error-demo.mjs key
node scripts/error-demo.mjs reset
```

Después de cada comando, abrir o recargar `/laboratorio-errores.html` y revisar
la consola del navegador. Ejecutar siempre `reset` al terminar.
El script solo modifica `experiments/Example.jsx`; los ejemplos no forman parte
de la cartelera. Estado final entregado: **restaurado**, con un único nodo raíz
y sin los errores provocados. La consola de la aplicación principal quedó vacía
de advertencias y errores durante la revisión final.

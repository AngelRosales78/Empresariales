# Cinéclub · Semana09

Cartelera de ocho películas con React y Vite. Componentes Header, Footer, Hero,
MovieCard y MovieList; datos locales, estilos separados por responsabilidad,
filtros de género, búsqueda y horarios seleccionables de demostración.

## Ejecutar

Entorno comprobado: Node **22.23.3** y npm **10.9.9**.

```powershell
cd C:\Users\ADMIN\Ciclo4\Empresariales\Semana09
npm install
npm run dev
```

Abrir la URL Local que muestra Vite. Para una instalación idéntica a la probada,
usar `npm ci` en lugar de `npm install`.

```powershell
npm run build
npm run preview
```

## Entregables

- [Informe con los once puntos y comprobaciones](docs/ENTREGABLE.md)
- [Tres errores provocados y correcciones](docs/ERRORES.md)
- [Header comprobado antes de continuar](docs/evidencias/01-header.jpg)
- [Cartelera completa en navegador](docs/evidencias/02-cartelera-completa.jpg)
- [Compilación correcta](docs/evidencias/build.txt)

Los datos están en `src/data/movies.js`; los componentes en `src/components/`;
los estilos en `src/styles/`; las imágenes originales en `public/images/`.
La arquitectura CSS adoptada está explicada en el informe, porque no se adjuntó
la guía específica del curso.

## Repetir los errores de React

Con el servidor activo, abrir `/laboratorio-errores.html`. Ejecutar cada caso
y recargar esa página, mirando la consola del navegador:

```powershell
node scripts/error-demo.mjs class
node scripts/error-demo.mjs roots
node scripts/error-demo.mjs key
node scripts/error-demo.mjs reset
```

El ejemplo es independiente de la cartelera. Ejecutar **reset** al terminar.
El proyecto se entrega restaurado y compila correctamente.

Las películas, valoraciones, datos de contacto y funciones son ficticios.
No hay reservas ni compras reales. No se necesitan claves ni servicios externos.

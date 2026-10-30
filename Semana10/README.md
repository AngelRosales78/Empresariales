# Cinéclub · Semana10

Continuación del laboratorio de cartelera de Semana09: Button reutilizable,
favoritas con useState y localStorage, búsqueda controlada desde el banner,
retardo de 400 ms, filtros y estado vacío.

## Ejecutar

Entorno utilizado: Node 22.23.3, npm 10.9.9, React 19.3.1 y Vite 8.3.5.

```powershell
cd C:\Users\ADMIN\Ciclo4\Empresariales\Semana10
npm ci
npm run dev
```

Abrir la dirección Local que muestra Vite. Las favoritas se guardan para ese
origen del navegador: usar la misma dirección y puerto al comprobar una recarga.

```powershell
npm test
npm run build
npm run preview
```

## Comprobar la práctica

1. Escribir `orbita` en el buscador del banner. El texto se actualiza al instante;
   la cartelera muestra Órbita tras una pausa de 400 ms.
2. Abrir la consola de desarrollo: aparecen `[entrada inmediata]` por cada cambio,
   `[búsqueda aplicada]` al vencer el retardo y `[filtro ejecutado]` al filtrar.
3. Pulsar el corazón de Órbita, recargar y comprobar que sigue marcado.
4. Activar Mis favoritas para ver solo la colección. Quitarla y recargar para
   comprobar también que la eliminación persiste.
5. Buscar `pelicula inexistente` y pulsar Buscar: aparece el estado vacío.
6. Pulsar Ver todas las películas para limpiar búsqueda, género y filtro de favoritas.

Los registros de búsqueda solo aparecen en desarrollo, no en la compilación de
producción. React StrictMode puede repetir registros iniciales de desarrollo.

## Entregable

- [Informe de los once puntos y tabla de decisiones de estado](docs/ENTREGABLE.md)
- [Captura obligatoria del estado vacío](docs/evidencias/03-estado-vacio.jpg)
- [Registros reales del retardo](docs/evidencias/debounce.json)
- [Favoritas recuperadas después de recargar](docs/evidencias/02-favoritas-recuperadas.jpg)
- [Ocho pruebas de almacenamiento aprobadas](docs/evidencias/pruebas.txt)

Solo las favoritas se conservan entre visitas. Búsqueda, filtros y horarios
seleccionados son temporales. Los datos de las ocho películas y sus imágenes
locales se mantienen desde Semana09. Películas, horarios y contacto son ficticios;
la selección de funciones no realiza reservas ni compras.

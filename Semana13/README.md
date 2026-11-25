# Laboratorio 12 · React y Django REST Framework

Desde PowerShell, en la carpeta Semana12, ejecuta:

```powershell
powershell -ExecutionPolicy Bypass -File .\preparar.ps1
```

La preparación instala las dependencias, aplica las migraciones, carga los datos iniciales y configura la credencial local de React. La base de datos pertenece a Semana12. El token del usuario de prácticas permite borrar y queda en `react/.env.local`, excluido de Git. Úsalo solo en este entorno local.

Abre dos terminales en Semana12 y ejecuta un bloque en cada una.

```powershell
cd api
python manage.py runserver 127.0.0.1:8000
```

```powershell
cd react
npm.cmd run dev
```

Abre [React](http://127.0.0.1:5173/) y la [API de Django](http://127.0.0.1:8000/api/). La API requiere autenticación. El [entregable](docs/ENTREGABLE.md) registra las direcciones, los estados de pantalla y las pruebas del navegador.

La aplicación usa el proyecto disponible de Semana10. Las carpetas de Semana11 encontradas solo contenían `.gitkeep`. La cartelera original está en `/cartelera`.

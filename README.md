# VENTANILLA — Sistema de Gestión de Solicitudes Estudiantiles

Adaptación del MVP especificado en el documento del proyecto: backend en **Flask** (en lugar de FastAPI),
frontend en **Angular 17 (standalone)** y base de datos **PostgreSQL**.

## Estructura

```
ventanilla/
├── backend/            # API REST con Flask
│   ├── app/
│   │   ├── models.py        # Usuario, TipoSolicitud, Solicitud
│   │   ├── routers/         # auth, tipos, solicitudes
│   │   ├── services/        # email_service, pdf_service
│   │   └── core/security.py # decorador requiere_rol
│   ├── seed.py          # datos de prueba (usuarios + tipos)
│   └── run.py
├── frontend/            # SPA Angular 17
│   └── src/app/
│       ├── core/             # AuthService, SolicitudService, guards, interceptor
│       ├── features/         # login, solicitud-form, mis-solicitudes, panel-funcionario
│       └── shared/           # modelo Solicitud, EstadoBadgeComponent
└── docker-compose.yml
```

## Cómo correrlo en desarrollo

### 1. Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://ventanilla:ventanilla@localhost:5432/ventanilla
python seed.py        # crea tablas + datos de prueba
python run.py          # http://localhost:8000
```

### 2. Frontend
```bash
cd frontend
npm install
ng serve               # http://localhost:4200
```

### 3. Usuarios de prueba (creados por seed.py)
| Rol | Email | Password |
|---|---|---|
| Estudiante | estudiante@uni.edu | estudiante123 |
| Funcionario | funcionario@uni.edu | funcionario123 |

## Con Docker Compose

```bash
docker compose up --build
```
- API: http://localhost:8000
- Web: http://localhost:80
- DB: PostgreSQL en el puerto 5432

## Lo que cubre esta primera vista

- Login con JWT y roles (estudiante / funcionario).
- Creación de solicitudes con tipo, motivo y archivo adjunto opcional.
- Vista "Mis solicitudes" con filtro por estado y descarga de PDF.
- Panel del funcionario: tomar, aprobar (genera PDF) o rechazar (motivo obligatorio) con notificación por email.
- Guards de Angular por rol + verificación autoritativa en el backend.

## Pendiente para siguientes iteraciones (fuera del MVP, según el documento)
Historial de cambios de estado, asignación manual de solicitudes, panel de estadísticas, firma digital,
integración con sistemas académicos, app móvil.

## Despliegue
e
git clone (https://github.com/Kazuke23/ventanilla-backend.git)
cd backend

docker compose up -d db

python seed.py

python run.py
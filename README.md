# Proyecto Apache Airflow

Este proyecto contiene una implementación de Apache Airflow 3.0 con múltiples DAGs de ejemplo y un SDK personalizado para extender la funcionalidad de Airflow.

## Descripción

El proyecto incluye varios DAGs que demuestran diferentes características de Airflow:

- **user_processing**: Pipeline completo de ETL que extrae datos de una API, los procesa y los almacena en PostgreSQL
- **branching_dag**: Ejemplo de branching condicional en workflows
- **sql_dag**: Ejecución de consultas SQL usando el decorador personalizado
- **task_groups**: Organización de tareas en grupos y grupos anidados
- **xcom_dag**: Comunicación entre tareas usando XCom
- **delete_table_user**: Operaciones de limpieza de base de datos
- **user_asset**: Manejo de assets y scheduling basado en datos

## Requisitos Previos

- Docker y Docker Compose instalados
- Python 3.10 o superior (para desarrollo local)
- Al menos 4GB de RAM disponible
- Al menos 2 CPUs

## Instalación y Configuración

### Opción 1: Usando Docker (Recomendado)

1. Clona el repositorio:
```bash
git clone <tu-repositorio>
cd <nombre-del-proyecto>
```

2. Construye las imágenes de Docker:
```bash
docker-compose build
```

3. Inicia los servicios de Airflow:
```bash
docker-compose up -d
```

4. Espera a que todos los servicios estén listos (puede tomar unos minutos la primera vez)

5. Accede a la interfaz web de Airflow:
```
URL: http://localhost:8080
Usuario: airflow
Contraseña: airflow
```

### Opción 2: Instalación Local

1. Crea un entorno virtual:
```bash
python -m venv airflowenv
source airflowenv/bin/activate  # En Windows: airflowenv\Scripts\activate
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Instala el SDK personalizado:
```bash
pip install -e ./my-sdk
```

4. Configura la base de datos y crea un usuario administrador:
```bash
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

5. Inicia el webserver y scheduler:
```bash
airflow webserver --port 8080
airflow scheduler  # En otra terminal
```

## Configuración de Conexiones

Antes de ejecutar los DAGs, configura la conexión a PostgreSQL en la interfaz de Airflow:

1. Ve a Admin > Connections
2. Crea una nueva conexión con los siguientes datos:
   - Connection Id: `postgres`
   - Connection Type: `Postgres`
   - Host: `postgres` (o `localhost` si usas instalación local)
   - Schema: `airflow`
   - Login: `airflow`
   - Password: `airflow`
   - Port: `5432`

## Estructura del Proyecto

```
.
├── dags/                    # DAGs de Airflow
│   ├── user_processing.py   # Pipeline ETL completo
│   ├── branching.py         # Ejemplo de branching
│   ├── sql.py              # Uso del decorador SQL
│   ├── task_groups.py      # Grupos de tareas
│   ├── xcom.py             # Comunicación entre tareas
│   ├── delete_table_user.py # Limpieza de datos
│   └── user_asset.py       # Manejo de assets
├── my-sdk/                 # SDK personalizado
│   └── my_sdk/
│       ├── decorators/     # Decoradores personalizados
│       └── __init__.py
├── config/                 # Configuración de Airflow
├── logs/                   # Logs de ejecución
├── plugins/                # Plugins personalizados
├── docker-compose.yml      # Configuración de Docker
├── dockerfile             # Imagen personalizada
└── requirements.txt       # Dependencias Python
```

## Uso

### Ejecutar un DAG

1. Accede a la interfaz web de Airflow
2. Activa el DAG que deseas ejecutar usando el toggle
3. Haz clic en el botón "Play" para ejecutarlo manualmente
4. Monitorea el progreso en la vista de Graph o Grid

### Detener los Servicios

```bash
docker-compose down
```

Para eliminar también los volúmenes (base de datos):
```bash
docker-compose down -v
```

## Desarrollo

### Agregar un Nuevo DAG

1. Crea un nuevo archivo Python en la carpeta `dags/`
2. Define tu DAG usando el decorador `@dag`
3. El DAG aparecerá automáticamente en la interfaz web

### Modificar el SDK

El SDK personalizado se encuentra en `my-sdk/` y proporciona decoradores adicionales para Airflow. Consulta el README del SDK para más detalles.

## Troubleshooting

### Los DAGs no aparecen en la interfaz

- Verifica que no haya errores de sintaxis en tus archivos Python
- Revisa los logs del dag-processor: `docker-compose logs airflow-dag-processor`

### Error de conexión a la base de datos

- Asegúrate de que el servicio de PostgreSQL esté corriendo: `docker-compose ps`
- Verifica la configuración de la conexión en Airflow

### Problemas de permisos

- En Linux, asegúrate de configurar la variable `AIRFLOW_UID` en un archivo `.env`:
```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```

## Tecnologías Utilizadas

- Apache Airflow 3.0.0
- PostgreSQL 13
- Docker & Docker Compose
- Python 3.10+

## Licencia

Este proyecto está bajo la Licencia Apache 2.0

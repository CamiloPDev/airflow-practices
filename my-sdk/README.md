# My SDK - Custom Airflow Task Decorators

SDK personalizado para Apache Airflow que proporciona decoradores de tareas adicionales para extender la funcionalidad nativa de Airflow.

## Descripción

Este SDK implementa decoradores personalizados que simplifican la creación de tareas en Airflow. Actualmente incluye el decorador `@task.sql` que permite ejecutar consultas SQL de manera más intuitiva y pythonic.

## Características

### Decorador @task.sql

El decorador `@task.sql` permite definir tareas SQL usando funciones Python que retornan consultas SQL como strings. Esto proporciona:

- **Sintaxis más limpia**: Define consultas SQL dentro de funciones Python
- **Validación automática**: Verifica que la función retorne una consulta SQL válida
- **Integración con XCom**: Soporta el paso de datos entre tareas
- **Template rendering**: Soporta Jinja templating en las consultas SQL

## Instalación

### Desde el código fuente

```bash
pip install -e /path/to/my-sdk
```

### En Docker (ya incluido en el proyecto)

El SDK se instala automáticamente al construir la imagen Docker del proyecto principal:

```dockerfile
COPY my-sdk /opt/airflow/my-sdk
RUN pip install -e /opt/airflow/my-sdk
```

## Uso

### Ejemplo Básico

```python
from airflow.sdk import dag, task

@dag
def sql_dag():
    @task.sql(conn_id="postgres")
    def get_user_count():
        return "SELECT COUNT(*) FROM users"
    
    get_user_count()

sql_dag()
```

### Ejemplo con Parámetros

```python
from airflow.sdk import dag, task

@dag
def dynamic_sql_dag():
    @task.sql(
        conn_id="postgres",
        autocommit=True
    )
    def create_table():
        return """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            price DECIMAL(10, 2)
        )
        """
    
    @task.sql(conn_id="postgres")
    def get_product_stats():
        return """
        SELECT 
            COUNT(*) as total_products,
            AVG(price) as avg_price
        FROM products
        """
    
    create_table() >> get_product_stats()

dynamic_sql_dag()
```

### Ejemplo con Templating

```python
from airflow.sdk import dag, task
from datetime import datetime

@dag
def templated_sql_dag():
    @task.sql(
        conn_id="postgres",
        parameters={"table_name": "orders"}
    )
    def get_daily_orders():
        return """
        SELECT * FROM {{ params.table_name }}
        WHERE date = '{{ ds }}'
        """
    
    get_daily_orders()

templated_sql_dag()
```

## Arquitectura

### Estructura del Proyecto

```
my-sdk/
├── my_sdk/
│   ├── __init__.py           # Información del provider
│   └── decorators/
│       └── sql.py            # Implementación del decorador SQL
├── pyproject.toml            # Configuración del paquete
└── README.md                 # Esta documentación
```

### Componentes Principales

#### 1. Provider Info (`__init__.py`)

Define la información del provider para que Airflow pueda descubrir y registrar los decoradores personalizados:

```python
def get_provider_info() -> dict[str, Any]:
    return {
        "package-name": "my-sdk",
        "name": "My SDK",
        "description": "A sample SDK for demonstration purposes.",
        "version": [__version__],
        "task-decorators": [
            {
                "name": "sql",
                "class-name": "my_sdk.decorators.sql.sql_task",
            }
        ],
    }
```

#### 2. SQL Decorator (`decorators/sql.py`)

Implementa el decorador `@task.sql` que:

- Extiende `DecoratedOperator` y `SQLExecuteQueryOperator`
- Ejecuta la función Python para obtener la consulta SQL
- Valida que el resultado sea un string SQL no vacío
- Renderiza templates antes de ejecutar la consulta
- Ejecuta la consulta usando el operador SQL de Airflow

### Flujo de Ejecución

1. El decorador `@task.sql` envuelve la función Python
2. Durante la ejecución, se llama a la función para obtener la consulta SQL
3. Se valida que el resultado sea un string SQL válido
4. Se renderizan los templates Jinja si existen
5. Se ejecuta la consulta usando `SQLExecuteQueryOperator`
6. Se retorna el resultado de la consulta

## Parámetros del Decorador

El decorador `@task.sql` acepta todos los parámetros de `SQLExecuteQueryOperator`:

- `conn_id` (str): ID de la conexión a la base de datos
- `autocommit` (bool): Si se debe hacer commit automático
- `parameters` (dict): Parámetros para la consulta SQL
- `handler` (callable): Función para procesar los resultados
- `split_statements` (bool): Si se deben dividir múltiples statements
- `return_last` (bool): Si se debe retornar solo el último resultado

## Validaciones

El decorador realiza las siguientes validaciones:

1. **Tipo de retorno**: La función debe retornar un string
2. **SQL no vacío**: El string no puede estar vacío o contener solo espacios
3. **No soporta multiple_outputs**: Se ignora este parámetro con un warning

## Desarrollo

### Agregar un Nuevo Decorador

1. Crea un nuevo archivo en `my_sdk/decorators/`
2. Implementa la clase del operador decorado
3. Crea la función factory del decorador
4. Registra el decorador en `__init__.py`

Ejemplo:

```python
# my_sdk/decorators/custom.py
from airflow.sdk.bases.decorator import DecoratedOperator, task_decorator_factory

class _CustomDecoratedOperator(DecoratedOperator):
    custom_operator_name: str = "@task.custom"
    
    def execute(self, context):
        # Tu lógica aquí
        pass

def custom_task(python_callable=None, **kwargs):
    return task_decorator_factory(
        python_callable=python_callable,
        decorated_operator_class=_CustomDecoratedOperator,
        **kwargs
    )
```

### Testing

Para probar el SDK localmente:

```bash
# Instalar en modo desarrollo
pip install -e .

# Usar en un DAG de prueba
python dags/sql.py
```

## Requisitos

- Python >= 3.10
- apache-airflow >= 2.7.0
- typing-extensions >= 4.0.0

## Compatibilidad

- Apache Airflow 3.0.0+
- Python 3.10+

## Contribuir

Para contribuir al SDK:

1. Crea una nueva rama para tu feature
2. Implementa tu decorador siguiendo el patrón existente
3. Actualiza la documentación
4. Asegúrate de que el código siga las convenciones de Airflow

## Limitaciones Conocidas

- El decorador `@task.sql` no soporta `multiple_outputs`
- Solo funciona con bases de datos soportadas por Airflow providers

## Roadmap

Posibles mejoras futuras:

- [ ] Decorador para APIs REST
- [ ] Decorador para operaciones de archivos
- [ ] Decorador para transformaciones de datos
- [ ] Soporte para async/await
- [ ] Tests unitarios

## Licencia

Apache License 2.0

## Soporte

Para reportar bugs o solicitar features, crea un issue en el repositorio del proyecto.

# finance-proyect
# Control de Gastos y Planes de Ahorro


Este proyecto es un gestor de finanzas personales desarrollado en Python con una interfaz gráfica moderna basada en `customtkinter`. Permite crear, editar y eliminar planes de ahorro, registrar gastos asociados a estos planes, y generar reportes detallados. Además, incluye un sistema de monitoreo en segundo plano que alerta cuando un plan está próximo a vencer o ha alcanzado su objetivo.

---

## Requisitos Previos

- **Python**: Versión 3.7 o superior instalada en tu sistema.
- **Pip**: Administrador de paquetes de Python (incluido con Python).
- **Conexión a Internet**: Para instalar las dependencias necesarias.

---

## Configuración del Entorno

### 1. Crear un Entorno Virtual
1. Abre una terminal o línea de comandos.
2. Navega al directorio donde se encuentra el archivo `app.py`.
3. Ejecuta el siguiente comando para crear un entorno virtual:
```
python -m venv env
```

### 2. Ejecutar el Entorno Virtual
Linux Run env
```
source env/bin/activate
```

Windows Run env
```
env\Scripts\activate
```

## 3. Instalar las Dependencias
Ejecuta el siguiente comando para instalar las bibliotecas necesarias:
```
pip install customtkinter
```

---

## Uso del Software

### 1. Ejecutar la Aplicación
1. Asegúrate de que el entorno virtual esté activado.
2. Ejecuta el archivo principal:
```
python app.py
```

### 2. Funcionalidades Principales

- **Crear Plan de Ahorro:**
    Haz clic en el botón "Crear Plan de Ahorro".
    Completa los campos requeridos: nombre del plan, objetivo monetario y fecha de fin.
    Haz clic en "Guardar Plan" para añadir el plan.

- **Añadir Ahorro a un Plan:**
    Haz clic en el botón "Añadir Ahorro" junto al plan deseado.
    Ingresa el monto a añadir y haz clic en "Guardar".

- **Editar Plan:**
    Haz clic en el botón "Editar" junto al plan que deseas modificar.
    Cambia los datos en los campos y haz clic en "Guardar Cambios".

- **Eliminar Plan:**
    Haz clic en el botón "Eliminar" junto al plan que deseas borrar.

- **Registrar Gasto:**
    Haz clic en el botón "Registrar Gasto".
    Selecciona un plan, ingresa la descripción y el monto del gasto.
    Haz clic en "Guardar Gasto" para registrar el gasto y descontarlo del plan seleccionado.

- **Ver Reportes:**
    Haz clic en el botón "Ver Reportes" para visualizar un resumen de los gastos por plan.

- **Filtrar Planes:**
    Usa el menú desplegable en el panel derecho para mostrar todos los planes o solo los próximos a vencer.

- **Guardar Datos:**
    Haz clic en el botón "Guardar Datos" para guardar toda la información en el archivo `finanzas.json`.

---

## Características Adicionales

- **Monitoreo en Segundo Plano:** El sistema verifica automáticamente si algún plan ha alcanzado su fecha de fin o su objetivo, mostrando alertas cuando sea necesario.
- **Interfaz Intuitiva:** Diseño oscuro y moderno con `customtkinter` para una mejor experiencia de usuario.
- **Persistencia de Datos:** Todos los planes y gastos se guardan en un archivo JSON para su recuperación en futuras sesiones.

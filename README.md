# Sistema de Triaje Hospitalario

Un sistema moderno, modular y completamente funcional para la gestión hospitalaria de ingresos urgentes. Desarrollado con **Python/Flask** para la lógica del servidor, **Tailwind CSS** para un diseño vanguardista de la interfaz (UI), y almacenamiento local en **JSON** para persistencia de datos.

## 🚀 Funcionalidades Principales

El sistema está diseñado para cumplir con el flujo completo de atención a pacientes:

1. **Registro Automático y Triaje:** Interfaz amigable para ingresar datos personales y signos vitales. Un algoritmo evalúa en milisegundos las palabras clave en síntomas y las anomalías en signos vitales para asignar automáticamente uno de los 5 niveles de triaje (I al V).
2. **Cola de Espera Dinámica:** Los pacientes que ingresan se ordenan en la sala de espera basándose primero en su Prioridad Médica y, en caso de empate, por hora de llegada.
3. **Asignación a Camas:** El personal médico puede "Atender" a un paciente de la cola, transfiriéndolo inmediatamente a la primera cama disponible del hospital.
4. **Dashboard Interactivo de Camas:** Muestra visualmente las camas libres y ocupadas. Las camas ocupadas muestran el color de triaje correspondiente al paciente para facilitar el reconocimiento rápido en piso. 
5. **Historial Clínico por Cédula:** Un motor de búsqueda que devuelve la línea de tiempo de atenciones históricas de cualquier paciente basado en su identificación.
6. **Alta Médica:** Botón en el mapa de camas que finaliza el encuentro, desocupa la cama y deja registro de la atención finalizada.
7. **Persistencia Transparente:** La base de datos reposa internamente en archivos `.json` (Ubicados en la carpeta `/data`). Al reiniciar el servidor en días posteriores, nadie pierde su lugar, su cama ni su historia.

---

## 📁 Estructura del Proyecto

El proyecto está diseñado bajo un modelo de arquitectura **Limpia y Modular** usando `Blueprints` en Flask para extrema escalabilidad:

```text
triage-hospitalario/
│
├── app/
│   ├── __init__.py           # Inicializador principal (hace que 'app' sea un módulo)
│   ├── models/
│   │   └── data_store.py     # Capa abstracta: Lee/Escribe JSON y administra los modelos (Paciente, Encuentro, Cama)
│   ├── routes/
│   │   ├── beds_routes.py    # Controlador Flask: Gestión de Camas y Altas
│   │   ├── history_routes.py # Controlador Flask: Búsqueda del historial clínico
│   │   ├── queue_routes.py   # Controlador Flask: Consulta de Espera y Admisión
│   │   └── registration.py   # Controlador Flask: Ingreso y Registro
│   ├── services/
│   │   └── triage.py         # Lógica pura del Negocio: El algoritmo de triaje
│   ├── static/               # CSS personalizados, Imágenes o JS local
│   └── templates/            # Vistas en HTML+Tailwind
│       ├── base.html         # Plantilla maestra, barra de navegación, importación de Tailwind UI.
│       ├── beds.html         # Mapa en malla de las camas.
│       ├── history.html      # Buscador con línea de tiempo visual.
│       ├── queue.html        # Tarjetas de turnos coloreadas y jerarquizadas.
│       └── register.html     # Formulario integral del paciente.
│
├── data/                     # (Se auto-crea) Contiene los JSONs que suplen la base de datos (PostgreSQL ready-architecture)
│
├── run.py                    # Script de entrada para encender el servidor y ensamblar la app
└── requirements.txt          # Dependencias de Python
```

---

## 💻 Instalación y Uso

**1. Requisitos Previos:**
*   Asegúrate de tener instalado Python 3.10 o superior (`python --version`).
*   Tener acceso a tu terminal (Linux, WSL, GitBash, CMD o PowerShell).

**2. Instalación:**

Abre tu terminal y clona el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd triage-hospitalario
```

Crea y activa un entorno virtual (venv) para aislar las dependencias:
```bash
# En Windows (CMD/PowerShell):
python -m venv venv
venv\Scripts\activate

# En Linux/Mac/WSL:
python3 -m venv venv
source venv/bin/activate
```

Finalmente, instala las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```

**3. Ejecutar el Servidor Web:**
Enciende la aplicación escribiendo en tu terminal:
```bash
python run.py
```
*(Se verá un mensaje en la terminal indicando que Flask está encendido con Debug Mode: ON)*

**4. Uso Final:**
Abre tu navegador de preferencia (Chrome, Firefox, Safari) e ingresa a:
👉 `http://127.0.0.1:5000`
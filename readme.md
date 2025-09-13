Mini RAG - Historia Argentina (ES / EN) 🇦🇷


Un sistema RAG (Retrieval-Augmented Generation) diseñado para actuar como un asistente experto en la historia de Argentina. La aplicación utiliza un modelo de lenguaje avanzado para responder preguntas basándose en un conjunto curado de fuentes documentales, emulando la personalidad de un catedrático universitario con más de 30 años de experiencia.

Características Principales ✨
Backend Robusto: Construido con FastAPI, proporciona una API rápida y eficiente para procesar las consultas.

Pipeline RAG Avanzado:

Recuperación de Información: Utiliza scikit-learn y embeddings de última generación (Gemini text-embedding-004) para encontrar los fragmentos de texto más relevantes.

Expansión de Consulta: Emplea a Gemini 1.5 Flash para enriquecer y re-contextualizar las preguntas del usuario, mejorando drásticamente la precisión de la búsqueda.

Generación Aumentada: El mismo modelo Gemini 1.5 Flash sintetiza la información recuperada para generar respuestas coherentes, citando sus fuentes.

Personalidad Definida: El prompt está cuidadosamente diseñado para que el asistente responda con el tono y la cadencia de un profesor de historia argentino experimentado.

Interfaz Académica: Un frontend limpio y profesional construido con HTML, CSS y JavaScript puros, con un diseño que evoca un entorno universitario.

Demo de la Aplicación 🚀
Aquí podés insertar una captura de pantalla de tu aplicación funcionando, como la última que me enviaste.

Instalación y Puesta en Marcha 🛠️
Sigue estos pasos para ejecutar el proyecto en tu máquina local.

1. Prerrequisitos
Python 3.9+

Git

2. Clonar el Repositorio
Abre tu terminal y clona este repositorio:

Bash

git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
3. Configurar el Entorno
Crea y activa un entorno virtual de Python:

Bash

# En Windows
python -m venv .venv
.\.venv\Scripts\activate

# En macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
4. Instalar Dependencias
Instala todas las librerías necesarias con pip:

Bash

pip install -r requirements.txt
5. Configurar las Claves de API
Este proyecto requiere una clave de API de Google (Gemini).

Crea una copia del archivo de ejemplo .env.example y renómbralo a .env.

Abre el archivo .env y pega tu clave de API de Google:

GEMINI_API_KEY="AIzaSy...tu...clave...secreta"
Cómo Usar la Aplicación 🚀
El proceso se divide en dos etapas: la ingesta de datos (se hace una sola vez) y la ejecución de la aplicación.

1. Ingesta de Datos (Creación del Índice)
Este paso procesa las fuentes de información, las divide en fragmentos (chunks) y genera los embeddings para la base de datos vectorial.

Bash

python -m app.ingest
Verás barras de progreso mientras se procesan las URLs. Este proceso puede tardar varios minutos dependiendo de la cantidad de fuentes.

2. Iniciar el Servidor de la API
Una vez que la ingesta ha finalizado, inicia el servidor backend:

Bash

python -m app.api
El servidor estará corriendo en http://127.0.0.1:8000. ¡Dejá esta terminal abierta!

3. Abrir la Interfaz de Usuario
Abre el archivo index.html en tu navegador web. La forma más fácil es usar la extensión Live Server en VS Code (clic derecho sobre el archivo > "Open with Live Server").

¡Listo! Ya podés empezar a hacerle preguntas a tu asistente de historia.

Estructura del Proyecto 📂
.
├── app/                # Lógica principal del backend
│   ├── api.py          # Servidor FastAPI y endpoints
│   ├── generator.py    # Lógica de generación de respuestas (LLM)
│   ├── ingest.py       # Script para la ingesta y embedding de datos
│   ├── rag_pipeline.py # Orquestador principal del proceso RAG
│   ├── retriever.py    # Lógica de búsqueda y recuperación de documentos
│   └── settings.py     # Carga de configuraciones y secretos
├── data/               # (Generada por ingest.py) Contiene el índice
├── .env                # (Local) Archivo con tus claves de API
├── .env.example        # Plantilla para el archivo .env
├── .gitignore          # Archivos a ignorar por Git
├── index.html          # Interfaz de usuario (Frontend)
├── README.md           # Este archivo
└── requirements.txt    # Dependencias de Python
<br>
<hr>
<br>

Mini RAG - Argentinian History 📜🇦🇷
A RAG (Retrieval-Augmented Generation) system designed to act as an expert assistant on the history of Argentina. The application uses an advanced language model to answer questions based on a curated set of documentary sources, emulating the persona of a university professor with over 30 years of experience.

Key Features ✨
Robust Backend: Built with FastAPI, it provides a fast and efficient API to process queries.

Advanced RAG Pipeline:

Information Retrieval: Uses scikit-learn and state-of-the-art embeddings (Gemini text-embedding-004) to find the most relevant text fragments.

Query Expansion: Employs Gemini 1.5 Flash to enrich and re-contextualize user questions, drastically improving search accuracy.

Augmented Generation: The same Gemini 1.5 Flash model synthesizes the retrieved information to generate coherent answers, citing its sources.

Defined Persona: The prompt is carefully crafted for the assistant to respond with the tone and cadence of an experienced Argentinian history professor.

Academic Interface: A clean and professional frontend built with pure HTML, CSS, and JavaScript, featuring a design that evokes a university environment.

Application Demo 🚀
You can insert a screenshot of your running application here, like the last one you sent me.

Installation and Setup 🛠️
Follow these steps to run the project on your local machine.

1. Prerequisites
Python 3.9+

Git

2. Clone the Repository
Open your terminal and clone this repository:

Bash

git clone https://github.com/your-username/your-repository.git
cd your-repository
3. Set Up the Environment
Create and activate a Python virtual environment:

Bash

# On Windows
python -m venv .venv
.\.venv\Scripts\activate

# On macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
4. Install Dependencies
Install all required libraries using pip:

Bash

pip install -r requirements.txt
5. Configure API Keys
This project requires a Google API Key (Gemini).

Create a copy of the .env.example file and rename it to .env.

Open the .env file and paste your Google API key:

GEMINI_API_KEY="AIzaSy...your...secret...key"
How to Use the Application 🚀
The process is divided into two stages: data ingestion (done only once) and running the application.

1. Data Ingestion (Index Creation)
This step processes the information sources, splits them into chunks, and generates the embeddings for the vector database.

Bash

python -m app.ingest
You will see progress bars as the URLs are processed. This may take several minutes depending on the number of sources.

2. Start the API Server
Once the ingestion is complete, start the backend server:

Bash

python -m app.api
The server will be running at http://127.0.0.1:8000. Keep this terminal open!

3. Open the User Interface
Open the index.html file in your web browser. The easiest way is to use the Live Server extension in VS Code (right-click on the file > "Open with Live Server").

That's it! You can now start asking questions to your history assistant.

Project Structure 📂
.
├── app/                # Main backend logic
│   ├── api.py          # FastAPI server and endpoints
│   ├── generator.py    # Response generation logic (LLM)
│   ├── ingest.py       # Script for data ingestion and embedding
│   ├── rag_pipeline.py # Main RAG process orchestrator
│   ├── retriever.py    # Document search and retrieval logic
│   └── settings.py     # Loads configurations and secrets
├── data/               # (Generated by ingest.py) Contains the index
├── .env                # (Local) File with your API keys
├── .env.example        # Template for the .env file
├── .gitignore          # Files to be ignored by Git
├── index.html          # User Interface (Frontend)
├── README.md           # This file
└── requirements.txt    # Python dependencies
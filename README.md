========================== PathExplorer AI Backend ==========================

Este proyecto es el backend de PathExplorer, una plataforma de desarrollo profesional que genera automaticamente:

- Resumenes de perfil de usuario  
- Embeddings vectoriales para matching semantico  
- Recomendaciones de crecimiento (keypoints)  
- Roles sugeridos a partir de RFPs  

Todo esto esta construido con FastAPI, Cohere, Supabase y Transformers.

------------ Tecnologias Usadas ------------

- FastAPI – Framework web moderno y asincrono para APIs  
- Supabase – Backend como servicio (DB + Auth + Storage)  
- Cohere API – IA para generacion de texto y embeddings  
- Transformers (HuggingFace) – Para tokenizacion inteligente  
- PyMuPDF (fitz) – Para extraer texto desde PDFs  
- Dotenv – Manejo de variables de entorno  

------------ Estructura del Proyecto ------------
.
├── app/
│   ├── main.py → Entrypoint FastAPI + routers
│   ├── api/endpoints.py → Endpoints agrupados
│   ├── models/request_models.py → Pydantic models
│
├── services/
│   ├── generate_user_summary.py → Resumen de perfil y embedding
│   ├── generate_keypoints.py → Micro-recomendaciones personalizadas
│   ├── generate_roles_from_rfp.py → Extraccion de roles desde RFP
│   ├── embedding_utils.py → Logica general de embedding
│
├── cohere_summarizer.py → Prompting para resumen
├── cohere_roles.py → Prompting para extraccion de roles
├── cohere_keypoints.py → Prompting para keypoints
│
├── requirements.txt → Dependencias
├── .env → Variables de entorno
└── README.md

------------ Instalacion Local ------------

1. Clonar el repositorio:
git clone https://github.com/tu-usuario/path-explorer-backend.git
cd path-explorer-backend

2. Crear un entorno virtual
python -m venv env
source env/bin/activate → Mac/Linux
env\\Scripts\\activate → Windows

3. Instalcion de las dependencias
pip install -r requirements.txt

4. Configura el .env
VITE_SUPABASE_URL=url-de-supabase
VITE_SUPABASE_ANON_KEY=clave-anon
COHERE_API_KEY=api-key-de-cohere

------------ Ejecutar el Servidor ------------

uvicorn app.main:app --reload

Ir a: http://localhost:8000/docs para usar Swagger UI.

------------ Endpoints Principales ------------

GET / → Verifica que el backend esta activo  
POST /generate-summary → Genera resumen y embedding del usuario  
POST /generate-keypoints → Genera recomendaciones personalizadas  
POST /generate-roles → Extrae roles desde un archivo RFP PDF  

------------ Descripcion Funcional ------------

generate-summary:
- Extrae el CV PDF desde Supabase  
- Usa IA para generar un resumen profesional  
- Genera embedding semantico  
- Guarda todo en la tabla User

generate-keypoints:
- Lee el resumen AI y metas del usuario  
- Genera 4 micro-habitos personalizados  
- Guarda en la tabla Grow

generate-roles:
- Descarga un archivo RFP del proyecto  
- Extrae multiples roles con IA  
- Genera embeddings y guarda en la tabla Role

------------ Dependencias Clave ------------

fastapi  
uvicorn  
python-dotenv  
cohere  
requests  
pymupdf  
transformers  
supabase  

Instalacion rapida:

pip install fastapi uvicorn python-dotenv cohere requests pymupdf transformers supabase

------------ Creditos ------------

Desarrollado por Ana Aramoni del equipo TheBytles para la plataforma PathExplorer.

------------ Nota ------------

Este backend esta preparado para integrarse con un frontend en Vite + React desplegado en Vercel.

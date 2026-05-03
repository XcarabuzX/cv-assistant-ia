# 📄 CV Assistant IA

Asistente inteligente que utiliza IA para optimizar CVs y generar cartas de presentación personalizadas según una oferta laboral específica.

**Proyecto Final** - Curso de *Prompt Engineering para Programadores* · Coderhouse

---

## 🎯 ¿Qué hace la app?

CV Assistant IA recibe dos entradas (tu CV actual + una oferta laboral) y, mediante un prompt con salida dirigida, devuelve:

- Un **CV optimizado** adaptado a esa oferta específica.
- Una **carta de presentación personalizada** de máximo 300 palabras.
- Una lista de **mejoras concretas y accionables** para fortalecer la candidatura.
- Un **score de compatibilidad** del 1 al 10 entre tu perfil y el puesto.

## 🧠 Problemática que resuelve

Una de las principales razones por las que candidatos calificados quedan fuera de procesos de selección es que envían el mismo CV genérico a todas las ofertas. Los reclutadores y filtros automáticos (ATS) priorizan candidatos cuyo CV está alineado con las palabras clave y requisitos del puesto. Adaptar manualmente cada CV es un proceso tedioso que la mayoría termina evitando.

## ✨ Solución

CV Assistant IA automatiza esa adaptación en segundos usando Google Gemini API. El usuario pega su CV una sola vez, pega la oferta a la que quiere aplicar, y obtiene material listo para enviar.

---

## 🛠️ Tecnologías

- **Python 3.10+**
- **Streamlit** — framework para apps web de datos
- **Google Gemini API** (gemini-1.5-flash / gemini-1.5-pro) — tier gratuito 1.500 req/día
- **HTML/CSS** personalizado para la identidad visual

---

## 🚀 Cómo correrlo localmente

```bash
# 1. Cloná el repo
git clone https://github.com/XcarabuzX/cv-assistant-ia.git
cd cv-assistant-ia

# 2. Creá un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

# 3. Instalá las dependencias
pip install -r requirements.txt

# 4. Corré la app
streamlit run app.py
```

La app se abrirá automáticamente en `http://localhost:8501`.

### Configuración de la API Key (Google AI)

Generá tu API Key gratis en 👉 https://aistudio.google.com/app/apikey (no requiere tarjeta de crédito).

Tenés dos opciones para usarla:

**Opción A (recomendada para uso local):** ingresá la API Key directamente en el sidebar de la app.

**Opción B (para deploy):** creá el archivo `.streamlit/secrets.toml` con:
```toml
GOOGLE_API_KEY = "tu-api-key-aqui"
```

---

## ☁️ Deploy en Streamlit Community Cloud

1. Subí este repositorio a GitHub.
2. Ingresá a [share.streamlit.io](https://share.streamlit.io) y conectá tu cuenta de GitHub.
3. Hacé clic en *New app*, elegí el repo y el archivo `app.py`.
4. En *Settings > Secrets*, pegá tu `GOOGLE_API_KEY`.
5. *Deploy* — la app queda online en una URL pública.

---

## 📂 Estructura del proyecto

```
cv-assistant-ia/
├── app.py                  # Aplicación principal Streamlit
├── requirements.txt        # Dependencias Python
├── .gitignore              # Archivos ignorados por Git
├── secrets.toml.example    # Plantilla para la API Key
└── README.md               # Este archivo
```

---

## 💰 Factibilidad económica

Se evaluaron varias opciones de proveedores de LLMs y se eligió **Google Gemini 1.5 Flash** por su excelente relación calidad-precio:

| Proveedor | Modelo | Costo / 1.000 consultas |
|---|---|---|
| **Google Gemini** ⭐ | gemini-1.5-flash | **USD 0,00** (Free tier hasta 1.500/día) |
| OpenAI | gpt-4o-mini | USD 1,00 |
| OpenAI | gpt-4o | USD 15,00 |
| OpenAI | gpt-3.5-turbo | USD 3,00 |

Con Gemini en su tier gratuito, el proyecto tiene **costo operativo cero** para uso personal y para los primeros usuarios de un MVP.

---

## ⚠️ Limitaciones

- La IA trabaja únicamente con la información que se le provee. No inventa experiencias ni habilidades.
- Los modelos de lenguaje pueden tener alucinaciones ocasionales (mitigadas con prompt de salida dirigida).
- Requiere conexión a internet y una API Key de Google AI (gratuita).

---

## 👤 Autor

**Felipe Gutierrez Reuss**
Comisión 86240 · Coderhouse 2026
GitHub: [@XcarabuzX](https://github.com/XcarabuzX)

---

## 📜 Licencia

Proyecto académico. Uso libre con atribución.

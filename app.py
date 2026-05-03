"""
CV Assistant IA - Asistente inteligente para optimizar CVs y generar
cartas de presentación personalizadas.

Proyecto Final - Prompt Engineering para Programadores
Autor: Felipe Gutierrez Reuss
Comisión: 86240
Coderhouse - 2026

Implementación con Google Gemini API (Tier gratuito).
Decisión técnica: tras evaluar costos entre OpenAI (gpt-4o-mini, gpt-4o)
y Google Gemini (1.5-flash), se eligió Gemini por su tier gratuito
que cubre hasta 1.500 consultas por día sin costo operativo.
"""

import streamlit as st
import google.generativeai as genai

# ----------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ----------------------------------------------------------------------
# Define el título que aparece en la pestaña del navegador, el ícono
# y el layout. "wide" usa todo el ancho disponible de la pantalla.
st.set_page_config(
    page_title="CV Assistant IA",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Header, Footer, paleta de colores)
# ----------------------------------------------------------------------
# Inyectamos CSS para darle identidad visual a la app: colores, header
# y footer fijo. Esto cumple con el contenido adicional sugerido por
# la consigna (estructura visual con paleta de colores).
st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(90deg, #1E2761 0%, #408EC6 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { color: white; margin: 0; font-size: 2.2rem; }
    .main-header p { color: #CADCFC; margin: 0.3rem 0 0 0; }
    .footer {
        text-align: center;
        padding: 1rem;
        color: #888;
        font-size: 0.85rem;
        border-top: 1px solid #eee;
        margin-top: 2rem;
    }
    .stButton > button {
        background-color: #1E2761;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
    }
    .stButton > button:hover {
        background-color: #408EC6;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# HEADER VISUAL
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <h1>📄 CV Assistant IA</h1>
        <p>Optimizá tu CV y generá cartas de presentación con Inteligencia Artificial</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# DESCRIPCIÓN DE LA APP
# ----------------------------------------------------------------------
st.markdown(
    """
    ### Bienvenido/a 👋
    **CV Assistant IA** es una aplicación que utiliza inteligencia artificial
    (Google Gemini) para ayudarte a maximizar tus chances de conseguir
    entrevistas laborales. Pegá tu CV actual y la descripción del puesto
    al que querés aplicar, y la IA te devolverá tres salidas estructuradas:
    un **CV optimizado**, una **carta de presentación personalizada** y
    una lista de **mejoras concretas** que podés implementar.
    """
)

# ----------------------------------------------------------------------
# SIDEBAR - CONFIGURACIÓN
# ----------------------------------------------------------------------
# La API Key se lee primero desde st.secrets (Streamlit Cloud) y, si
# no está, se le pide al usuario por el sidebar. Esto permite probar
# la app localmente sin commitear credenciales.
with st.sidebar:
    st.header("⚙️ Configuración")

    # Intentamos leer la API Key desde los secrets de Streamlit Cloud
    api_key = st.secrets.get("GOOGLE_API_KEY", "") if hasattr(st, "secrets") else ""

    # Si no está en secrets, dejamos que el usuario la ingrese manualmente
    if not api_key:
        api_key = st.text_input(
            "🔑 Google AI API Key",
            type="password",
            help=(
                "Generá tu API Key gratis en aistudio.google.com/app/apikey "
                "(no requiere tarjeta de crédito)."
            ),
        )

    # Selector de modelo de Gemini disponible en el tier gratuito
    modelo = st.selectbox(
        "🤖 Modelo de IA",
        options=[
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-1.5-pro",
        ],
        index=0,
        help=(
            "gemini-1.5-flash es el recomendado: rápido, gratuito y de "
            "calidad alta para tareas de texto."
        ),
    )

    # Selector de idioma de salida
    idioma = st.selectbox(
        "🌎 Idioma de salida",
        options=["Español", "Inglés", "Portugués"],
        index=0,
    )

    st.markdown("---")
    st.markdown(
        """
        **💡 Tip:** Tu API Key se usa solo durante la sesión y no se guarda
        en ningún servidor.

        **🆓 Costo cero:** Gemini ofrece hasta 1.500 consultas por día gratis.
        """
    )

# ----------------------------------------------------------------------
# SECCIÓN: ENTRADAS DEL USUARIO
# ----------------------------------------------------------------------
st.markdown("---")
st.subheader("📝 Ingresá tu información")

# Usamos dos columnas para el CV y la oferta para mejor distribución visual
col1, col2 = st.columns(2)

with col1:
    cv_actual = st.text_area(
        "📄 Tu CV actual",
        height=300,
        placeholder=(
            "Pegá acá el contenido de tu CV: experiencia laboral, "
            "estudios, habilidades, etc."
        ),
        help="Copiá y pegá el texto completo de tu CV",
    )

with col2:
    oferta_laboral = st.text_area(
        "💼 Descripción del puesto al que aplicás",
        height=300,
        placeholder=(
            "Pegá acá la descripción del puesto: requisitos, "
            "responsabilidades, tecnologías, etc."
        ),
        help="Copiá la oferta completa de LinkedIn, Computrabajo, etc.",
    )

# Tipo de tarea que se quiere realizar
tarea = st.radio(
    "🎯 ¿Qué querés generar?",
    options=[
        "CV optimizado para esta oferta",
        "Carta de presentación personalizada",
        "Análisis completo (CV + Carta + Mejoras)",
    ],
    horizontal=True,
)

# ----------------------------------------------------------------------
# FUNCIÓN PRINCIPAL: CONSTRUCCIÓN DEL PROMPT CON SALIDA DIRIGIDA
# ----------------------------------------------------------------------
def construir_prompt(cv: str, oferta: str, tipo: str, idioma_out: str) -> str:
    """
    Construye un prompt con salida dirigida según la tarea elegida.

    "Salida dirigida" significa que le indicamos al modelo el formato
    EXACTO en el que debe responder, evitando alucinaciones y respuestas
    inconsistentes. Así garantizamos que la salida sea siempre útil y
    parseable.
    """
    instrucciones_base = f"""
Sos un experto en Recursos Humanos y reclutamiento técnico con más de
15 años de experiencia. Tu tarea es ayudar a un candidato a maximizar
sus chances de ser seleccionado para una oferta laboral.

IDIOMA DE LA RESPUESTA: {idioma_out}

CV DEL CANDIDATO:
\"\"\"
{cv}
\"\"\"

OFERTA LABORAL:
\"\"\"
{oferta}
\"\"\"

REGLAS IMPORTANTES:
1. Trabajá EXCLUSIVAMENTE con la información del CV. NO inventes datos,
   experiencias ni habilidades que no estén explícitas.
2. Si falta información clave, indicalo claramente como "[FALTA: ...]"
   en lugar de inventar.
3. Sé concreto, profesional y orientado a resultados.
"""

    if tipo == "CV optimizado para esta oferta":
        formato = """
FORMATO DE SALIDA (respetar exactamente):

## 🎯 CV OPTIMIZADO

### Resumen profesional (3-4 líneas adaptadas a la oferta)
[texto]

### Experiencia laboral (reordenada y reescrita destacando lo relevante)
[texto]

### Habilidades clave (priorizando las que pide la oferta)
[lista]

### Educación
[texto]

### 💡 Cambios principales que hice
[lista breve de los 3-5 cambios más importantes y por qué]
"""

    elif tipo == "Carta de presentación personalizada":
        formato = """
FORMATO DE SALIDA (respetar exactamente):

## ✉️ CARTA DE PRESENTACIÓN

[Carta de máximo 300 palabras, tono profesional pero cercano, con esta
estructura:
- Saludo
- Por qué te interesa la posición y la empresa
- Match entre tu experiencia y los requisitos clave (con ejemplos concretos)
- Cierre con llamada a la acción
- Despedida formal]

### 💡 Por qué funciona esta carta
[3-4 puntos breves explicando por qué esta carta es efectiva para esta oferta]
"""

    else:  # Análisis completo
        formato = """
FORMATO DE SALIDA (respetar exactamente):

## 🎯 1. CV OPTIMIZADO
[Versión mejorada del CV adaptada a la oferta, con secciones: Resumen,
Experiencia, Habilidades, Educación]

## ✉️ 2. CARTA DE PRESENTACIÓN
[Carta personalizada de máximo 300 palabras]

## 🚀 3. MEJORAS CONCRETAS
[5-7 sugerencias específicas y accionables para fortalecer la candidatura.
Cada mejora debe incluir: qué cambiar, por qué y un ejemplo.]

## 📊 4. SCORE DE COMPATIBILIDAD
Puntaje del 1 al 10 indicando qué tan bien encaja el CV con la oferta,
con justificación breve.
"""

    return instrucciones_base + formato

# ----------------------------------------------------------------------
# BOTÓN DE ACCIÓN PARA LA TAREA ESPECÍFICA
# ----------------------------------------------------------------------
st.markdown("---")
boton_generar = st.button(
    "🚀 Generar con IA",
    type="primary",
    use_container_width=True,
)

# ----------------------------------------------------------------------
# LÓGICA DE EJECUCIÓN
# ----------------------------------------------------------------------
if boton_generar:
    # Validaciones previas para evitar requests inútiles
    if not api_key:
        st.error("⚠️ Por favor ingresá tu API Key de Google AI en el sidebar.")
    elif not cv_actual.strip():
        st.error("⚠️ Por favor pegá tu CV en el campo correspondiente.")
    elif not oferta_laboral.strip():
        st.error("⚠️ Por favor pegá la descripción de la oferta laboral.")
    else:
        # Si todo está OK, construimos el prompt y llamamos a la API
        prompt = construir_prompt(cv_actual, oferta_laboral, tarea, idioma)

        try:
            # Mostramos un spinner mientras la API procesa
            with st.spinner("🧠 La IA está analizando tu CV..."):
                # Configuración de Gemini con la API Key
                genai.configure(api_key=api_key)

                # Configuración del modelo: usamos un system prompt para
                # asignar el rol y reglas de comportamiento
                modelo_gemini = genai.GenerativeModel(
                    model_name=modelo,
                    system_instruction=(
                        "Sos un asistente experto en Recursos Humanos "
                        "que ayuda a candidatos a optimizar su CV y "
                        "cartas de presentación. Siempre seguís el "
                        "formato exacto que se te pide y nunca inventás "
                        "información que no esté en el CV."
                    ),
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,    # creatividad moderada
                        max_output_tokens=2500,
                    ),
                )

                # Llamada al modelo
                respuesta = modelo_gemini.generate_content(prompt)
                resultado = respuesta.text

                # Métricas de uso (útiles para evaluar factibilidad económica)
                metadata = respuesta.usage_metadata
                tokens_input = metadata.prompt_token_count
                tokens_output = metadata.candidates_token_count
                tokens_usados = metadata.total_token_count

            # Mostrar el resultado en un contenedor destacado
            st.success("✅ ¡Listo! Acá está tu resultado:")
            st.markdown("---")
            st.markdown(resultado)

            # Mostrar métricas y botón de descarga
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Tokens totales", tokens_usados)
            with col_b:
                # Costo aprox: gratis hasta 1.500 req/día con gemini-1.5-flash
                st.metric("Costo (USD)", "$0.00 (Free)")
            with col_c:
                st.download_button(
                    label="📥 Descargar resultado",
                    data=resultado,
                    file_name="resultado_cv_assistant.md",
                    mime="text/markdown",
                )

        except Exception as e:
            st.error(f"❌ Ocurrió un error al consultar la IA: {e}")
            st.info(
                "Verificá que tu API Key sea válida. Podés generar una "
                "gratis en https://aistudio.google.com/app/apikey"
            )

# ----------------------------------------------------------------------
# SECCIÓN: ¿CÓMO FUNCIONA?
# ----------------------------------------------------------------------
st.markdown("---")
with st.expander("ℹ️ ¿Cómo funciona CV Assistant IA?", expanded=False):
    st.markdown(
        """
        ### 🔍 Características clave

        - **Optimización dirigida**: la IA adapta tu CV a cada oferta específica,
          destacando las habilidades y experiencias más relevantes para ese puesto.
        - **Carta personalizada**: genera cartas de presentación únicas para cada
          aplicación, no plantillas genéricas.
        - **Sugerencias accionables**: te indica exactamente qué mejorar y por qué.
        - **Score de compatibilidad**: te dice qué tan bien encaja tu perfil con
          el puesto antes de aplicar.
        - **Costo cero**: usa Google Gemini en su tier gratuito (1.500 req/día).

        ### 📋 Cómo realizar una solicitud

        1. **Generá tu API Key gratis** en [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
           — solo necesitás una cuenta de Google.
        2. **Ingresá la API Key** en el sidebar de la app.
        3. **Pegá tu CV actual** en el campo de la izquierda. Cuanta más
           información, mejor el resultado.
        4. **Pegá la oferta laboral** en el campo de la derecha. Copiala
           directamente desde LinkedIn, Computrabajo, etc.
        5. **Elegí qué querés generar**: CV optimizado, carta de presentación
           o el análisis completo.
        6. **Hacé clic en "Generar con IA"** y esperá unos segundos.

        ### 🎯 Qué esperar como resultado

        Dependiendo de la opción que elijas:
        - **CV optimizado**: una versión reescrita de tu CV adaptada a la oferta,
          con un resumen del cambio principal.
        - **Carta de presentación**: una carta de máximo 300 palabras lista para
          enviar.
        - **Análisis completo**: las dos cosas anteriores + lista de mejoras
          concretas + score de compatibilidad del 1 al 10.

        ### ⚠️ Limitaciones a tener en cuenta

        - La IA trabaja **solo con la información que le des**. Si tu CV está
          incompleto, el resultado también lo estará.
        - Si bien usamos prompts con salida dirigida para minimizarlas, los
          modelos de lenguaje pueden tener **alucinaciones** ocasionales.
          Siempre revisá la salida antes de usarla.
        - El **tier gratuito de Gemini** permite 1.500 consultas por día, lo
          cual es más que suficiente para uso personal.

        ### 🔒 Privacidad

        Tu CV y datos personales **no se almacenan** en ningún servidor.
        Cada consulta se procesa en tiempo real y se descarta al cerrar
        la sesión.
        """
    )

# ----------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        <p>
            CV Assistant IA · Proyecto Final - Prompt Engineering para Programadores<br>
            Desarrollado por <b>Felipe Gutierrez Reuss</b> · Comisión 86240 · Coderhouse 2026
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

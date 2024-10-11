import streamlit as st
from openai import OpenAI
import time
import re
import os
from streamlit_navigation_bar import st_navbar

st.set_page_config(layout="wide")

parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "logo.svg")


styles = {
    "nav": {
        "background-color": "#387FC6",
        "justify-content": "left",
        "height": "60px",
        "position": "sticky",
    },

    "img": {
        "padding-right": "14px",
        "width": "150px",
        "height": "500px" 
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "0px",
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    [""],
    logo_path=logo_path,
#    urls=urls,
    styles=styles,
    options=options,
)

st.markdown("""
    <style>
    /* Fondo blanco para toda la página */
    .main {
        background-color: white;
        color: black;
    }

    /* Ajustar el color de los encabezados y el texto */
    h1, h2, h3, h4, h5, h6 {
        color: black;
    }

    /* Estilo de los cuadros de texto del asistente y del usuario */
    div[role="alert"] {
        background-color: #d1f7c4;
        border-radius: 10px;
        padding: 10px;
        color: black;
    }

    /* Estilo personalizado para el área de texto de entrada */
    textarea {
        caret-color: black !important; /* Color del cursor */
        background-color: white !important;
        color: black !important;
        border: 2px solid #d1d1d1 !important;
        border-radius: 10px !important;
        }

    /* Estilo personalizado para el botón de envío */
    button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        cursor: pointer !important;
    }

    /* Hover para el botón de envío */
    button:hover {
        background-color: #45a049 !important;
    }

    /* Ocultar el menú de hamburguesa y la marca de agua de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Ocultar la barra superior (donde dice Deploy) */
    header {visibility: hidden;}
                        
    </style>
    """, unsafe_allow_html=True)

autores = {
    "(2017)Modern diagnosis and treatment": {
        "Autor": "Siegal", 
        "Link": "https://drive.google.com/file/d/14CDqXA3pv_fUUrWGgXzYAxQGI-nKCAtR/view"
    },
    "(2018)Biologic Keyhole Mesh": {
        "Autor": "Watkins", 
        "Link": "https://drive.google.com/file/d/1yl2hWbBnOdPS0S_AOw-EczxFTMr8LdhI/view"
    },
    "(2018)Large Paraesophageal Hiatus Hernia": {
        "Autor": "Dellaportas", 
        "Link": "https://drive.google.com/file/d/1EuA4Fo1XtgvE7lGKfP7CuERu1-F2ftCR/view"
    },
    "(2018)Mesh hiatal hernioplasty": {
        "Autor": "Sathasivam", 
        "Link": "https://drive.google.com/file/d/1aQiIDtDpYCDGq4NXkZJjb6mMeDiPXFuS/view"
    },
    "(2019)Mesh erosion after hiatal hernia": {
        "Autor": "Li", 
        "Link": "https://drive.google.com/file/d/1bV-pKDckJj3sCnhqhCLMD8Z00xvWzeQ9/view"
    },
    "(2021)When should we use mesh in laparoscopic": {
        "Autor": "Laxague", 
        "Link": "https://drive.google.com/file/d/1rKkxMbqhl1dNdunHE6UghAHiI2ns7TfF/view"
    },
    "(2022)Does bioabsorbable mesh reduce": {
        "Autor": "Clapp", 
        "Link": "https://drive.google.com/file/d/1df-saLfzlCEKzlgAoUX2a3Ol5U7K4Lor/view"
    },
    "(2022)Does the use of bioabsorbable mesh": {
        "Autor": "Clapp", 
        "Link": "https://drive.google.com/file/d/11pBttIcb8V-qxDQW7MHqmr4VyZN2W0g-/view"
    },
    "(2022)Tension-free hiatal hernia": {
        "Autor": "Cheng", 
        "Link": "https://drive.google.com/file/d/1Q3cbe-oxsPk1-HZ8Auz8TjSY1-NScl5q/view"
    },
    "(2023)Hiatal hernia repair with biosynthetic": {
        "Autor": "Lima", 
        "Link": "https://drive.google.com/file/d/1WtT3Dp39O9U51w7zMPFaCteCFtYmFnry/view"
    },
    "(2023)The mesh configurations in hiatal hernia": {
        "Autor": "Li", 
        "Link": "https://drive.google.com/drive/folders/1iBc_XBhrNK-zKl_eAOMo9hSpYgA4nBkr"
    },
    "(2023)What works best in hiatus hernia repair": {
        "Autor": "Temperley", 
        "Link": "https://drive.google.com/file/d/1rvUeDJW5OWQQBvnVKc89VLQqM-Tr8CiL/view"
    }
}

# Cargar la clave de API de OpenAI y el ID del asistente desde los secretos de Streamlit
api_key = st.secrets["api_keys"]["openai_key"]
assistant_id = st.secrets["assistant"]["id"]

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=api_key)

# Usar columnas para colocar la imagen en la parte superior izquierda
col1, col2 = st.columns([1, 4])

with col1:
    # Añadir la imagen del chatbot en la parte superior izquierda
    st.image("chatbot_image.png", width=220)

with col2:
    # Título de la aplicación
    st.markdown("<h1 style='font-size: 4em;'>Asistente Experto en Hernia Hiatal</h1>", unsafe_allow_html=True)

    # Descripción introductoria
    st.markdown("""
    ## ¡Bienvenido! Soy tu asistente especializado en hernia hiatal. 
    Estoy aquí para ayudarte a responder cualquier pregunta que tengas sobre este tema. 
    Simplemente escribe tu consulta a continuación.
    """)


# Verificar si ya existe un hilo en la sesión actual
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = None

def format_message(text):
    citation_pattern = r"【(\d+):(\d+)†source】"
    
    def replace_citation(match):
        articulo = client.files.list().data[int(match.group(1))-1].filename
        articulo = articulo[:len(articulo)-4]
        return f" ['<a href=\"{autores[articulo]['Link']}\">{articulo}</a>', {autores[articulo]['Autor']} et al. " #, p{int(match.group(2))+1}] 

    return re.sub(citation_pattern, replace_citation, text)

def show_conversation():
    if st.session_state['thread_id']:
        messages = list(client.beta.threads.messages.list(thread_id=st.session_state['thread_id']))
        messages.reverse()

        conversation = ""
        for msg in messages:
            if msg.role == 'user':
                conversation += f"<div style='display: flex; align-items: center; justify-content: flex-end; margin: 5px 0;'>" \
                                f"<div style='max-width: 55%; text-align: right; background-color: #0995D4; border-radius: 10px; padding: 10px; color: white; margin-right: 10px;'>" \
                                f"{msg.content[0].text.value}</div>" \
                                f"<img src='https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png' alt='Descripción de la imagen' style='width: 60px; height: 50px; border-radius: 5px;'>" \
                                f"</div>"
                
            elif msg.role == 'assistant':
                formatted_content = format_message(msg.content[0].text.value)
                conversation += f"<div style='display: flex; align-items: center; margin: 5px 0;'>" \
                                f"<img src='https://png.pngtree.com/png-vector/20220611/ourmid/pngtree-chatbot-icon-chat-bot-robot-png-image_4841963.png' alt='Descripción de la imagen' style='width: 50px; height: 50px; border-radius: 5px; margin-right: 10px;'>" \
                                f"<div style='max-width: 55%; text-align: left; background-color: #F2F2F2; border-radius: 10px; padding: 10px; color: black;'>" \
                                f"<strong>Asistente:</strong> {formatted_content}</div>" \
                                f"</div>"
                                
        return conversation
    return ""


# Mostrar todos los mensajes en el hilo
messages_placeholder = st.empty()
messages_placeholder.markdown(show_conversation(), unsafe_allow_html=True)

# Campo de entrada para la consulta
user_input = st.text_area("Ingrese su consulta aquí:", height=100)

if st.button("Enviar Consulta"):
    if user_input:
        try:
            # Crear un hilo de conversación si no existe
            if st.session_state['thread_id'] is None:
                thread = client.beta.threads.create(
                    messages=[{"role": "user", "content": user_input}]
                )
                st.session_state['thread_id'] = thread.id  # Guardar el ID del hilo en la sesión
            else:
                # Enviar el mensaje al hilo existente
                client.beta.threads.messages.create(
                    thread_id=st.session_state['thread_id'],
                    role="user",
                    content=user_input
                )

            # Ejecutar el hilo con el asistente configurado
            run = client.beta.threads.runs.create(
                thread_id=st.session_state['thread_id'],
                assistant_id=assistant_id
            )

            # Esperar un momento para asegurarse de que el asistente haya procesado la solicitud
            time.sleep(10)  # Espera de 10 segundos para dar tiempo al asistente de responder

            # Actualizar los mensajes después de enviar la consulta
            #formatted_conversation = format_citations(show_conversation())
            
            messages_placeholder.markdown(show_conversation(), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Ocurrió un error: {str(e)}")

# Aplicar estilo con HTML y CSS
st.markdown(
    """
    <style>
    .custom-info {
        background-color: #AEECFF   ;
        padding: 10px;
        border-radius: 5px;
        color: black;
        font-size: 16px;
    }
    </style>
    <div class="custom-info">
        Nota: Esta es una versión en desarrollo del asistente con integración real.
    </div>
    """, unsafe_allow_html=True
)
 

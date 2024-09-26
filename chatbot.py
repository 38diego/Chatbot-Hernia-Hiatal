import streamlit as st
from openai import OpenAI
import time
import re
import os
from streamlit_navigation_bar import st_navbar

st.set_page_config(layout="wide")

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
    .st-emotion-cache-qdbtli {
        background-color: white !important; /* Cambia el color de fondo a blanco */
    }
    </style>
""", unsafe_allow_html=True)

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

api_key = st.secrets["api_keys"]["openai_key"]
assistant_id = st.secrets["assistant"]["id"]
project_id = st.secrets["project_id"]["projid"]

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=api_key, project=project_id)

# Usar columnas para colocar la imagen en la parte superior izquierda
col1, col2 = st.columns([1, 4])

with col1:
    st.image("chatbot_image.png", width=220)

with col2:
    st.markdown("<h1 style='font-size: 4em;'>Asistente Experto en Hernia Hiatal</h1>", unsafe_allow_html=True)
    st.markdown("""
    ## ¡Bienvenido! Soy tu asistente especializado en hernia hiatal. 
    Estoy aquí para ayudarte a responder cualquier pregunta que tengas sobre este tema. 
    Simplemente escribe tu consulta a continuación.
    """)

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = None
    st.session_state["messages"] = []

def format_message(text):
    if not isinstance(text, str):  # Asegúrate de que text sea un string
        return str(text)  # Convierte a string si no lo es

    citation_pattern = r"【(\d+):(\d+)†source】"
    
    def replace_citation(match):
        articulo_index = int(match.group(1)) - 1
        if articulo_index < len(client.files.list().data):
            articulo = client.files.list().data[articulo_index].filename
            articulo = articulo[:len(articulo) - 4]
            return f" ['<a href=\"{autores[articulo]['Link']}\">{articulo}</a>', {autores[articulo]['Autor']} et al., p{int(match.group(2)) + 1}] "
        else:
            return match.group(0)  # Retornar el texto original si el índice está fuera de rango

    return re.sub(citation_pattern, replace_citation, text)

# Mostrar mensajes anteriores
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='display: flex; align-items: center; justify-content: flex-end; margin: 5px 0;'>"
            f"<div style='max-width: 55%; text-align: right; background-color: #0995D4; border-radius: 10px; padding: 10px; color: white; margin-right: 10px;'>"
            f"{msg['content']}</div>"
            f"<img src='https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png' alt='Descripción de la imagen' style='width: 60px; height: 50px; border-radius: 5px;'>"
            f"</div>",
            unsafe_allow_html=True
        )
    else:  # Mensaje del asistente
        try:
            formatted_content = format_message(msg["content"][0].text.value)
        except:
            formatted_content = format_message(msg["content"])
        st.markdown(
            f"<div style='display: flex; align-items: center; margin: 5px 0;'>"
            f"<img src='https://png.pngtree.com/png-vector/20220611/ourmid/pngtree-chatbot-icon-chat-bot-robot-png-image_4841963.png' alt='Descripción de la imagen' style='width: 50px; height: 50px; border-radius: 5px; margin-right: 10px;'>"
            f"<div style='max-width: 55%; text-align: left; background-color: #F2F2F2; border-radius: 10px; padding: 10px; color: black;'>"
            f"<strong>Asistente:</strong> {formatted_content}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

# Manejar la entrada del usuario
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar la entrada del usuario
    st.markdown(
        f"<div style='display: flex; align-items: center; justify-content: flex-end; margin: 5px 0;'>"
        f"<div style='max-width: 55%; text-align: right; background-color: #0995D4; border-radius: 10px; padding: 10px; color: white; margin-right: 10px;'>"
        f"{prompt}</div>"
        f"<img src='https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png' alt='Descripción de la imagen' style='width: 60px; height: 50px; border-radius: 5px;'>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    # Crear un hilo de conversación si no existe
    if st.session_state['thread_id'] is None:
        thread = client.beta.threads.create(
            messages=st.session_state.messages
        )
        st.session_state['thread_id'] = thread.id
    else:
        client.beta.threads.messages.create(
            thread_id=st.session_state['thread_id'],
            role="user",
            content=prompt
        )

    # Ejecutar el asistente
    run = client.beta.threads.runs.create(
        thread_id=st.session_state['thread_id'],
        assistant_id=assistant_id
    )

    time.sleep(10)

    # Obtener la respuesta del asistente
    messages = list(client.beta.threads.messages.list(thread_id=st.session_state['thread_id']))
    if messages:  # Asegúrate de que la lista no esté vacía
        msg = messages[0].content  # Obtener el último mensaje
        print(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        formatted_content = format_message(msg[0].text.value)

        # Mostrar la respuesta del asistente
        st.markdown(
            f"<div style='display: flex; align-items: center; margin: 5px 0;'>"
            f"<img src='https://png.pngtree.com/png-vector/20220611/ourmid/pngtree-chatbot-icon-chat-bot-robot-png-image_4841963.png' alt='Descripción de la imagen' style='width: 50px; height: 50px; border-radius: 5px; margin-right: 10px;'>"
            f"<div style='max-width: 55%; text-align: left; background-color: #F2F2F2; border-radius: 10px; padding: 10px; color: black;'>"
            f"<strong>Asistente:</strong> {formatted_content}</div>"  # Cambia msg por formatted_content
            f"</div>",
            unsafe_allow_html=True
        )

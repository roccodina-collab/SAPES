import streamlit as st
import os

# Importem el graf de LangGraph del teu main.py
from main import app

st.set_page_config(page_title="SAPES AI Agent", page_icon="🤖", layout="centered")

st.title("🤖 Agent d'IA de SAPES")
st.write("Fes preguntes sobre la documentació del projecte o sol·licita assistència de codi.")

# Inicialitzar l'historial de xat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar l'historial de missatges a la pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Camp d'entrada de text per a l'usuari
if prompt := st.chat_input("Escriu la teva pregunta..."):
    # Afegir i mostrar la pregunta de l'usuari
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Executar l'agent i mostrar la resposta
    with st.chat_message("assistant"):
        with st.spinner("L'agent està processant la resposta..."):
            try:
                # Invocació del graf de LangGraph
               # Executar l'agent i mostrar la resposta
    with st.chat_message("assistant"):
        with st.spinner("L'agent està processant la resposta..."):
            try:
                # Invocació del graf de LangGraph
                inputs = {"messages": [("user", prompt)]}
                result = app.invoke(inputs)
                
                # Extreure l'últim missatge de la llista
                last_message = result["messages"][-1]
                
                # Comprovar si el missatge és un objecte de LangChain o una tupla (role, content)
                if hasattr(last_message, "content"):
                    response_text = last_message.content
                elif isinstance(last_message, tuple):
                    response_text = last_message[1]
                else:
                    response_text = str(last_message)
                
                st.markdown(response_text)
                
                # Afegir la resposta a l'historial
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"S'ha produït un error: {e}")
                
               
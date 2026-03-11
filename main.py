# titulo
# input do chat
# a cada mensagem enviada, ela tem que aparecer em tela
# a pergunta vai ir para alguma IA responder
# exibir a respsota da IA

#=================================================================

# será usado o Streamlit, pq dá pra fazer back e front só com o python
# IA usada: gemini

# pip install google-generativeai 

# No terminal: streamlit run main.py - main.py é o nome do arquivo no vscode, esse comando abre o projeto no navegador

#===================================================================

import streamlit as st
from google import genai

# CONFIGURAÇÃO DA API
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

st.set_page_config(page_title="Gemini Chat", page_icon="🤖")
st.title("🤖 Chatinho")

# HISTÓRICO DA CONVERSA
if "history" not in st.session_state:
    st.session_state.history = []

# EXIBE HISTÓRICO
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# INPUT DO USUÁRIO
if prompt := st.chat_input("Como posso ajudar?"):

    # mostra mensagem do usuário
    st.chat_message("user").markdown(prompt)

    st.session_state.history.append({
        "role": "user",
        "content": prompt
    })

    # gera resposta
    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        try:
            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=[
                    m["content"] for m in st.session_state.history
                ]
            )

            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Erro na geração: {e}")

    st.session_state.history.append({
        "role": "assistant",
        "content": full_response
    })
import streamlit as st
from agente import AgentePatricia

# Configurações de layout da página do Streamlit
st.set_page_config(page_title="Patrícia — Assistente Move Brasil", page_icon="🚗", layout="centered")

st.title("🚗 Conversando com a Patrícia")
st.subheader("Esclareça suas dúvidas sobre o Programa Move Brasil 2026")
st.caption("Protótipo de Agente Financeiro Local alimentado por Ollama")

# Inicializa a instância do agente de IA no estado de sessão do Streamlit
if "agente" not in st.session_state:
    st.session_state.agente = AgentePatricia()
    # Simula a busca de dados do cliente logado (passando um CPF fictício)
    st.session_state.contexto_usuario = st.session_state.agente.obter_contexto_usuario("123.456.789-00")

# Inicializa a lista de histórico de mensagens visual
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem inicial padrão humanizada e acolhedora
    boas_vindas = "Olá, Carlos! Tudo bem? Sou a Patrícia. Estou aqui para te ajudar a entender tudo sobre o Move Brasil de um jeito simples, para você tomar a melhor decisão para o seu bolso e trocar seu veículo com segurança. Vamos começar?"
    st.session_state.messages.append({"role": "assistant", "content": boas_vindas})

# Renderiza as mensagens do histórico na tela a cada atualização
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input de texto para interação do motorista
if prompt := st.chat_input("Digite sua dúvida aqui (ex: Eu tenho direito ao crédito?)"):
    # Renderiza a mensagem do usuário imediatamente
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processa a resposta da Patrícia
    with st.chat_message("assistant"):
        with st.spinner("Consultando diretrizes do BNDES..."):
            resposta_agente = st.session_state.agente.responder(
                mensagem_usuario=prompt,
                historico_chat=st.session_state.messages[1:],  # Remove a saudação fixa do histórico interno da LLM
                contexto_usuario=st.session_state.contexto_usuario
            )
            st.markdown(resposta_agente)

    # Registra a interação atual no histórico do Streamlit
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": resposta_agente})

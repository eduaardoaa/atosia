import streamlit as st
import requests
import json

# Configuração da página
st.set_page_config(
    page_title="Assistente Atos Capital",
    page_icon="🤖",
    layout="wide"
)

# CSS customizado para o estilo WhatsApp
st.markdown("""
<style>
    .message-container {
        display: flex;
        margin-bottom: 12px;
    }
    .user-message {
        background-color: #DCF8C6;
        color: #000;
        border-radius: 15px 15px 0 15px;
        padding: 10px 15px;
        margin-left: auto;
        max-width: 70%;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }
    .assistant-message {
        background-color: #ECE5DD;
        color: #000;
        border-radius: 15px 15px 15px 0;
        padding: 10px 15px;
        margin-right: auto;
        max-width: 70%;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }
    .sender-name {
        font-size: 0.8em;
        font-weight: bold;
        margin-bottom: 3px;
    }
    .chat-input {
        position: fixed;
        bottom: 20px;
        width: 80%;
    }
</style>
""", unsafe_allow_html=True)

# Título da aplicação
st.title("🤖 Assistente Atos Capital")
st.header("💬 Conversa com Atos")

# Inicialização do histórico
if 'historico' not in st.session_state:
    st.session_state.historico = []

# Função para enviar ao webhook
def enviar_para_webhook(mensagem):
    try:
        response = requests.post(
            "https://n8n-n8n.zofbat.easypanel.host/webhook/pergunta-whatsapp",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"pergunta": mensagem}),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao conectar com o webhook: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.image("logoatos.png", width=200)
    st.markdown("---")
    st.button("← Voltar", disabled=True)
    st.markdown("---")

# Exibir histórico de mensagens
for mensagem in st.session_state.historico:
    if mensagem["autor"] == "Atos Capital IA":
        st.markdown(f"""
        <div class="message-container">
            <div class="assistant-message">
                <div class="sender-name">Atos Capital IA</div>
                {mensagem['conteudo']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-container">
            <div class="user-message">
                <div class="sender-name">Você</div>
                {mensagem['conteudo']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona mensagem do usuário (direita)
    st.session_state.historico.append({
        "autor": "Usuário",
        "conteudo": prompt
    })
    
    # Processamento com webhook
    with st.spinner("Processando..."):
        resposta_webhook = enviar_para_webhook(prompt)
        
        if resposta_webhook:
            # Verifica se a resposta tem o formato esperado
            resposta = resposta_webhook.get("resposta") or resposta_webhook.get("output") or resposta_webhook.get("message") or str(resposta_webhook)
            
            # Adiciona resposta da IA (esquerda)
            st.session_state.historico.append({
                "autor": "Atos Capital IA",
                "conteudo": resposta
            })
        else:
            st.session_state.historico.append({
                "autor": "Atos Capital IA",
                "conteudo": "Desculpe, não consegui processar sua solicitação no momento."
            })
    
    st.rerun()

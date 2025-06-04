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
</style>
""", unsafe_allow_html=True)

# Título da aplicação
st.title("🤖 Assistente Atos Capital")

# Inicialização do histórico de conversa
if 'historico' not in st.session_state:
    st.session_state.historico = []

# Função para enviar mensagem para o webhook
def enviar_para_webhook(mensagem):
    webhook_url = "https://n8n-n8n.zofbat.easypanel.host/webhook/pergunta-whatsapp"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "pergunta": mensagem
    }
    
    try:
        response = requests.post(
            webhook_url,
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao enviar para o webhook: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.image("logoatos.png", width=200)
    st.markdown("---")
    st.button("← Voltar", disabled=True)
    st.markdown("---")

# Área de conversa
st.header("💬 Conversa com Atos")

# Exibir histórico de conversa
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

# Entrada do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.historico.append({
        "autor": "Usuário",
        "conteudo": prompt
    })
    
    # Mostra spinner enquanto processa
    with st.spinner("Processando sua pergunta..."):
        # Envia para o webhook e obtém resposta
        resposta_webhook = enviar_para_webhook(prompt)
        
        # Só aceita a resposta se vier do webhook
        if resposta_webhook and "resposta" in resposta_webhook:
            resposta = resposta_webhook["resposta"]
        else:
            # Não adiciona resposta se não vier do webhook
            st.error("Não recebi uma resposta válida do serviço.")
            st.rerun()
    
    # Adiciona resposta ao histórico
    st.session_state.historico.append({
        "autor": "Atos Capital IA",
        "conteudo": resposta
    })
    
    # Força atualização para mostrar as novas mensagens
    st.rerun()

# Rodapé
st.markdown("---")
st.caption("Assistente Atos Capital v1.0")

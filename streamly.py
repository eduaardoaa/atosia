import streamlit as st
import requests
import json
import re

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
    .loading-dots {
        display: inline-block;
    }
    .loading-dots:after {
        content: ' .';
        animation: dots 1.5s steps(5, end) infinite;
    }
    a {
        color: #0066cc;
        text-decoration: underline;
    }
    @keyframes dots {
        0%, 20% {
            color: rgba(0,0,0,0);
            text-shadow: .25em 0 0 rgba(0,0,0,0), .5em 0 0 rgba(0,0,0,0);
        }
        40% {
            color: black;
            text-shadow: .25em 0 0 rgba(0,0,0,0), .5em 0 0 rgba(0,0,0,0);
        }
        60% {
            text-shadow: .25em 0 0 black, .5em 0 0 rgba(0,0,0,0);
        }
        80%, 100% {
            text-shadow: .25em 0 0 black, .5em 0 0 black;
        }
    }
</style>
""", unsafe_allow_html=True)

# Função para converter URLs em links clicáveis
def url_to_link(text):
    # Regex para encontrar URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    
    # Função para substituir cada URL por um link HTML
    def replace_with_link(match):
        url = match.group(0)
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return f'<a href="{url}" target="_blank">{url}</a>'
    
    # Aplicar a substituição no texto
    return url_pattern.sub(replace_with_link, text)

# Título da aplicação
st.title("🤖 Assistente Atos Capital")
st.header("💬 Conversa com Atos")

# Inicialização do histórico
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'aguardando_resposta' not in st.session_state:
    st.session_state.aguardando_resposta = False

# Função para enviar ao webhook
def enviar_para_webhook(mensagem):
    try:
        response = requests.post(
            "https://n8n-n8n.zofbat.easypanel.host/webhook/pergunta-whatsapp",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"pergunta": mensagem}),
            timeout=300
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
    conteudo = url_to_link(mensagem['conteudo']) if isinstance(mensagem['conteudo'], str) else str(mensagem['conteudo'])
    
    if mensagem["autor"] == "Atos Capital IA":
        st.markdown(f"""
        <div class="message-container">
            <div class="assistant-message">
                <div class="sender-name">Atos Capital IA</div>
                {conteudo}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-container">
            <div class="user-message">
                <div class="sender-name">Você</div>
                {conteudo}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem...", disabled=st.session_state.aguardando_resposta):
    # Adiciona mensagem do usuário imediatamente (direita)
    st.session_state.historico.append({
        "autor": "Usuário",
        "conteudo": prompt
    })
    
    # Adiciona placeholder de "digitando..." (esquerda)
    st.session_state.historico.append({
        "autor": "Atos Capital IA",
        "conteudo": "<div class='loading-dots'>Processando sua resposta, aguarde</div>",
        "loading": True  # Flag para identificar que é um placeholder
    })
    
    st.session_state.aguardando_resposta = True
    st.rerun()

# Se estiver aguardando resposta, processa o webhook
if st.session_state.aguardando_resposta:
    # Encontra a última mensagem do usuário
    ultima_mensagem_usuario = next(
        (msg for msg in reversed(st.session_state.historico) if msg["autor"] == "Usuário"),
        None
    )
    
    if ultima_mensagem_usuario:
        # Processamento com webhook
        resposta_webhook = enviar_para_webhook(ultima_mensagem_usuario["conteudo"])
        
        # Remove o placeholder de "digitando..."
        st.session_state.historico = [msg for msg in st.session_state.historico if not msg.get("loading")]
        
        if resposta_webhook:
            # Verifica se a resposta tem o formato esperado
            resposta = resposta_webhook.get("resposta") or resposta_webhook.get("output") or resposta_webhook.get("message") or str(resposta_webhook)
            
            # Adiciona resposta real da IA (esquerda)
            st.session_state.historico.append({
                "autor": "Atos Capital IA",
                "conteudo": resposta
            })
        else:
            st.session_state.historico.append({
                "autor": "Atos Capital IA",
                "conteudo": "Desculpe, não consegui processar sua solicitação no momento, envie a pergunta novamente."
            })
    
    st.session_state.aguardando_resposta = False
    st.rerun()

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Assistente Atos Capital",
    page_icon="🤖",
    layout="wide"
)

# CSS customizado para o estilo WhatsApp
st.markdown("""
<style>
    /* Container das mensagens */
    .message-container {
        display: flex;
        margin-bottom: 12px;
    }
    
    /* Mensagens do usuário (direita) */
    .user-message {
        background-color: #DCF8C6;
        color: #000;
        border-radius: 15px 15px 0 15px;
        padding: 10px 15px;
        margin-left: auto;
        max-width: 70%;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }
    
    /* Mensagens do assistente (esquerda) */
    .assistant-message {
        background-color: #ECE5DD;
        color: #000;
        border-radius: 15px 15px 15px 0;
        padding: 10px 15px;
        margin-right: auto;
        max-width: 70%;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }
    
    /* Nome do remetente */
    .sender-name {
        font-size: 0.8em;
        font-weight: bold;
        margin-bottom: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Título da aplicação
st.title("🤖 Assistente Atos Capita")

# Inicialização do histórico de conversa
if 'historico' not in st.session_state:
    st.session_state.historico = []

# Sidebar
with st.sidebar:
    st.image("logoatos.png", width=200)
    st.markdown("---")
    st.button("← Voltar", disabled=True)
    st.markdown("---")

# Área de conversa
st.header("💬 Conversa com Atos")

# Exibir histórico de conversa no estilo WhatsApp
for mensagem in st.session_state.historico:
    if mensagem["autor"] == "Usuário":
        # Mensagem do assistente (esquerda)
        st.markdown(f"""
        <div class="message-container">
            <div class="assistant-message">
                <div class="sender-name">Usuário</div>
                {mensagem['conteudo']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Mensagem do usuário (direita)
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
    
    # Resposta simulada do assistente
    resposta = "Esta é uma resposta simulada. A funcionalidade de IA foi desativada nesta versão."
    
    # Adiciona resposta ao histórico
    st.session_state.historico.append({
        "autor": "Atos Capital IA",
        "conteudo": resposta
    })
    
    # Força atualização para mostrar as novas mensagens
    st.rerun()

# Rodapé
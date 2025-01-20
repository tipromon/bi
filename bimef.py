import streamlit as st
import streamlit.components.v1 as components
import base64
import os
# Configuração da página
st.set_page_config(page_title="Assistente Promon - Acciona", layout="wide")

# CSS atualizado
st.markdown("""
    <style>
        /* Remover padding padrão do Streamlit */
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        .stApp {
            margin: 0;
            padding: 0;
            overflow: hidden !important;
        }
        
        /* Estilo para o header principal fixo */
        .header-fixed {
            position: fixed;
            top: 50px;  /* Padding superior para evitar sobreposição */
            left: 250px;
            right: 0;
            z-index: 1000;
            background-color: white;
            height: 60px;
            display: flex;
            justify-content: center;
            align-items: center;
            border-bottom: 1px solid #ddd;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Estilo para o título principal */
        .header-title {
            color: #003366;
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            margin: 0;
            padding: 0;
            width: 100%;
        }
        
        /* Container do chat */
        .chat-container {
            position: fixed;
            top: 110px;  /* Ajustado para começar após o header (50px + 60px) */
            left: 250px;
            right: 0;
            bottom: 0;
            overflow: hidden;
        }
        
        /* Ajuste do conteúdo principal */
        .main-content {
            height: 100%;
            padding: 0;
            margin: 0;
            overflow: hidden;
        }
        
        /* Ajustes para o iframe do chat */
        iframe {
            width: 100% !important;
            height: calc(100vh) !important;  /* Altura total menos header */
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remover outros espaços em branco do Streamlit */
        .css-18e3th9 {
            padding: 0 !important;
        }
        
        .css-1d391kg {
            padding: 1rem 1rem !important;
        }
        
        div[data-testid="stVerticalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
        }
        
        /* Ocultar "Powered by Flowise" */
        .chatbot-footer {
            display: none !important;
        }
        
        div[class*="powered-by"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Header principal fixo com título centralizado
st.markdown("""
    <div class="header-fixed">
        <h2 class="header-title">Assistente Virtual Promon</h2>
    </div>
""", unsafe_allow_html=True)

# Container do chat
st.markdown("""
    <div class="main-content">
        <div class="chat-container">
""", unsafe_allow_html=True)

# Dicionário expandido com configurações específicas para cada agente
agents = {
    "Assistente BI - Acciona": {
        "chatflowid": st.secrets["acciona_chatflow_id"],
        "welcome_message": "Bem-vindo ao Assistente Acciona! Estou aqui para ajudar com informações sobre a empresa Acciona."
    },
    "Mineração e Fertilizantes": {
        "chatflowid": st.secrets["mineracao_chatflow_id"],
        "welcome_message": "Bem-vindo ao Assistente de Mineração e Fertilizantes! Como posso ajudar?"
    },
    "SAF (Sustainable Aviation Fuel)": {
        "chatflowid": st.secrets["saf_chatflow_id"],
        "welcome_message": "Bem-vindo ao Assistente SAF! Estou aqui para ajudar com informações sobre Sustainable Aviation Fuel."
    },
    "Assistente BI - VALE": {
        "chatflowid": st.secrets["vale_chatflow_id"],
        "welcome_message": "Bem-vindo ao Assistente VALE! Estou aqui para ajudar com informações sobre a VALE."
    },
    "Assistente BI - Hydro": {
        "chatflowid": st.secrets["hydro_chatflow_id"],
        "welcome_message": "Bem-vindo ao Assistente Hydro! Estou aqui para ajudar com informações sobre a Hydro."
    }
}

# Sidebar com logo e seletor
with st.sidebar:
    # Corrigindo o parâmetro depreciado e usando URL direto do GitHub
    st.image(
        "https://raw.githubusercontent.com/tipromon/bi/main/LOGO-COLORIDO-%E2%80%93-FUNDO-BRANCO.png",
        width=150,
        use_container_width=True  # Substituindo use_column_width por use_container_width
    )
    
    # Título e seletor
    st.title("Selecione o Assistente")
    selected_agent = st.selectbox("Agente:", list(agents.keys()))
    
    # Adicionar descrição do assistente selecionado
    st.markdown(f"**Assistente atual:** {selected_agent}")

# Obter configurações do agente selecionado
agent_config = agents[selected_agent]

# Código para renderizar o Flowise chatbot
flowise_fullpage_code = f"""
<div style="width: 100%; height: calc(100vh); display: flex; flex-direction: column;">
    <flowise-fullchatbot style="width: 100%; flex-grow: 1;"></flowise-fullchatbot>
</div>
<script type="module">
    import Chatbot from "https://cdn.jsdelivr.net/npm/flowise-embed/dist/web.js"
    Chatbot.initFull({{
        chatflowid: "{agent_config['chatflowid']}",
        apiHost: "https://flowiseaiflowise-production-56bf.up.railway.app",
        theme: {{
            chatWindow: {{
                backgroundColor: "#ffffff",
                height: "100%",
                welcomeMessage: "{agent_config['welcome_message']}",
                containerStyle: {{
                    overflow: "auto"
                }}
            }},
            textInput: {{
                position: "fixed",
                bottom: 0,
                left: 0,
                right: 0,
                backgroundColor: '#ffffff',
                textColor: '#000000',
                sendButtonColor: '#FF6600',
                placeholder: 'Digite sua pergunta',
                borderTop: '1px solid #ddd',
                boxShadow: '0 -2px 4px rgba(0,0,0,0.1)',
                padding: '1rem'
            }}
        }},
        containerStyle: {{
            height: '100%',
            display: 'flex',
            flexDirection: 'column'
        }}
    }})
</script>
"""

# Renderizar o chatbot com altura ajustada
components.html(
    flowise_fullpage_code,
    height=250,
    scrolling=True
)

# Fechar as divs
st.markdown("""
        </div>
    </div>
""", unsafe_allow_html=True)

# Disclaimer no rodapé
st.sidebar.markdown("""
---
**Disclaimer**:
O "Assistente Promon" tem como objetivo fornecer informações que sirvam de orientação e apoio aos colaboradores da Promon. As respostas são baseadas em documentos internos e fontes confiáveis disponíveis no sistema.
""")

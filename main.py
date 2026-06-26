import streamlit as st
import pandas as pd
import urllib.parse
import os
from datetime import datetime, timedelta
from supabase import create_client, Client

# ==========================================
# 0. CONFIGURAÇÃO VISUAL DA PÁGINA (BRANDING)
# ==========================================
FAVICON = "logo_silvia_guia.png" if os.path.exists("logo_silvia_guia.png") else "🧵"

st.set_page_config(
    page_title="Silvia Castro Conserto de Roupas", 
    page_icon=FAVICON, 
    layout="wide"
)
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
# Caminho da imagem da logo
LOGO_PATH = "file.jpeg" if os.path.exists("file.jpeg") else ("logo_silvia.png" if os.path.exists("logo_silvia.png") else None)

# Injeção de CSS Avançado para corrigir o topo e criar o Header Fixo
st.markdown("""
<style>
    :root {
        --primary-color: #2b2b2b;
        --sidebar-bg: #fbe4e6;
        --main-bg: #f8f9fa;
        --header-bg: #ffffff;
    }
    
    /* Remove a barra superior padrão do Streamlit e os espaçamentos fantasmas */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        height: 0px !important;
        display: none !important;
    }

    /* Esconde o menu hamburguer e footer do Streamlit */
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .stApp > header { display: none !important; }

    .block-container {
        padding-top: 90px !important;
    }
    
    /* Fundo geral da aplicação */
    .stApp {
        background-color: #f8f6fb;
        background-image: radial-gradient(circle, rgba(180,140,200,0.06) 1px, transparent 1px);
        background-size: 18px 18px;
    }

    /* CABEÇALHO FIXO SUPERIOR */
    .custom-top-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 72px;
        background: linear-gradient(135deg, #d4607e 0%, #e8829c 60%, #f195b2 100%) !important;
        box-shadow: 0 3px 16px rgba(136, 14, 79, 0.35);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 40px;
        border-bottom: none;
    }

    .header-brand {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .header-title {
        font-family: 'Garamond', 'Times New Roman', Times, serif !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        letter-spacing: 0.8px;
        text-shadow: 0 1px 4px rgba(0,0,0,0.15);
    }

    .header-cnpj {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        font-size: 11px !important;
        font-weight: 400 !important;
        color: rgba(255,255,255,0.75) !important;
        margin-top: 3px !important;
        letter-spacing: 0.8px;
    }

    .header-status {
        background-color: rgba(255,255,255,0.18);
        color: #ffffff;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif !important;
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(4px);
    }

    /* Força uma estilização elegant nos containers nativos com borda */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid rgba(0,0,0,0.06) !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02) !important;
    }
    
    /* Customizando a Barra Lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff0f3 0%, #fce4ec 100%) !important;
        border-right: 1px solid #f8bbd0 !important;
        padding-top: 20px;
        z-index: 999 !important;
    }

    /* Título do menu lateral */
    [data-testid="stSidebar"] .stRadio > label {
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        color: #ad1457 !important;
        padding-left: 4px;
    }

    /* Container do grupo de opções — sem gap, sem padding lateral */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 0px !important;
        display: flex;
        flex-direction: column;
    }

    /* Cada item do menu */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        display: flex !important;
        align-items: center !important;
        padding: 11px 20px !important;
        border-radius: 0px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #6d2b45 !important;
        cursor: pointer !important;
        transition: background-color 0.15s ease !important;
        border: none !important;
        background-color: transparent !important;
        width: 100% !important;
        font-family: 'Segoe UI', sans-serif !important;
    }

    /* Hover */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background-color: #f8bbd0 !important;
        color: #880e4f !important;
    }

    /* Item selecionado — rosa suave, retângulo cheio */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
        background-color: #f195b2 !important;
        color: #4a0e2a !important;
        font-weight: 700 !important;
        border-left: 4px solid #d4607e !important;
    }

    /* Esconde o círculo do radio button */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span:first-child {
        display: none !important;
    }

    /* Esconde o svg/circle interno do radio */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] input[type="radio"] {
        display: none !important;
    }

    /* Divisor lateral */
    [data-testid="stSidebar"] hr {
        border-color: #f48fb1 !important;
        opacity: 0.4;
    }

    /* Centraliza o logo na sidebar */
    [data-testid="stSidebar"] [data-testid="stImage"],
    [data-testid="stSidebar"] [data-testid="stImage"] > div {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        text-align: center !important;
    }
    [data-testid="stSidebar"] [data-testid="stImage"] img {
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
    }
    
    /* Estilização dos Botões Primários */
    .stButton>button[type="primary"] {
        background-color: var(--primary-color) !important;
        border-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    .stButton>button[type="primary"]:hover {
        background-color: #404040 !important;
        border-color: #404040 !important;
    }
    
    /* Estilização dos Botões Secundários */
    .stButton>button {
        border-radius: 8px !important;
    }
    
    /* Cabeçalhos e Tipografia interna */
    h1 {
        color: #4a0e2a !important;
        font-family: 'Garamond', 'Georgia', 'Times New Roman', serif !important;
        font-weight: 700 !important;
        font-size: 28px !important;
        letter-spacing: 0.5px !important;
        margin-top: 0px !important;
        margin-bottom: 16px !important;
    }
    h2, h3 {
        color: #4a0e2a !important;
        font-family: 'Garamond', 'Georgia', 'Times New Roman', serif !important;
        font-weight: 700 !important;
        margin-top: 0px !important;
    }
    
    /* Inputs arredondados */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Renderização estruturada do topo fixo com CNPJ
st.markdown(f"""
<div class="custom-top-header">
    <div class="header-brand">
        <span class="header-title">Silvia Castro Conserto de Roupas</span>
        <span class="header-cnpj">CNPJ: 36.329.114/0001-27 | Telefone: 12 99683-1392</span>
    </div>
    <div class="header-status">
        🟢 Sistema Online
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 0.5 SISTEMA DE AUTENTICAÇÃO (LOGIN VISUAL)
# ==========================================
# Lê a senha de uma variável de ambiente. Se não existir, usa "1234" como padrão.
# Para definir, crie um arquivo .env ou execute: export SENHA_ERP="sua_senha_aqui"
SENHA_MASTER = os.environ.get("SENHA_ERP", "1234")

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

def tela_login():
    st.markdown("""
        <style>
        /* Remove o cabeçalho padrão e ajusta o fundo da tela de login */
        [data-testid="stHeader"] { display: none !important; }
        .custom-top-header { display: none !important; }
        
        /* Fundo geral da tela em BRANCO */
        .stApp {
            background-color: #ffffff !important; 
        }
        
        /* Quadrado centralizado com a cor ROSA SUAVE do logo */
        [data-testid="stVerticalBlockBorderWrapper"] {
            max-width: 450px !important;
            margin: 60px auto 0 auto !important;
            background-color: #fbe4e6 !important; 
            padding: 35px !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
            border: 1px solid rgba(0,0,0,0.02) !important;
        }
        
        /* Alinhamentos dos textos */
        .login-title {
            font-family: 'Times New Roman', Times, serif !important;
            color: #2b2b2b !important;
            font-weight: 700 !important;
            text-align: center !important;
            margin-top: 15px !important;
            margin-bottom: 2px !important;
            font-size: 26px !important;
        }
        
        .login-subtitle {
            font-family: 'Segoe UI', sans-serif !important;
            color: #5c5c5c !important; 
            text-align: center !important;
            font-size: 14px !important;
            margin-bottom: 25px !important;
            letter-spacing: 0.5px;
        }
        
        /* Força a centralização absoluta de qualquer container de imagem dentro do bloco */
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            margin-left: auto !important;
            margin-right: auto !important;
            width: 100% !important;
        }
        
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] img {
            border-radius: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container(border=True):
            # 1. Exibe a Logo centralizada com tamanho menor e controlado
            if os.path.exists("logo_silvia.png"):
                # Ajustamos aqui: aumentamos as laterais para a coluna do meio ficar menor
                sub_col1, sub_col2, sub_col3 = st.columns([1.5, 2, 1.5])
                with sub_col2:
                    st.image("logo_silvia.png", use_container_width=True)
            else:
                st.markdown("<h1 style='text-align: center; font-size: 50px; margin:0;'>🧵</h1>", unsafe_allow_html=True)
                
            # 2. Títulos
            st.markdown('<h2 class="login-title">Silvia Castro Conserto de Roupas</h2>', unsafe_allow_html=True)
            st.markdown('<p class="login-subtitle">Gestão da Empresa</p>', unsafe_allow_html=True)
            
            # 3. Campo de senha e botão
            senha_digitada_login = st.text_input("Senha de Acesso", type="password", key="campo_senha_login", placeholder="••••••••")
            st.write("")
            
            if st.button("Entrar no Sistema ✅", type="primary", use_container_width=True):
                if senha_digitada_login == SENHA_MASTER:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("❌ Senha incorreta. Tente novamente.")
                    
    st.stop()

if not st.session_state.autenticado:
    tela_login()


# DADOS DA EMPRESA (Para o Cupom)
NOME_LOJA = "Silvia Castro Conserto de Roupas"
CNPJ_LOJA = "36.329.114/0001-27"
ENDERECO_LOJA = "Rua Conego Almeida, 85 - Centro, Taubate - SP, 12.080-260"
TELEFONE_LOJA = "12 99683-1392"

# ==========================================
# 1. CONEXÃO COM O BANCO DE DADOS (SUPABASE)
# ==========================================
SUPABASE_URL = "https://tqagcuooqbtotwnaznue.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_secret_QqBIxIZ-h5BC7719HiemSw_QzgDCk77")

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

sb = get_supabase()

def sb_query(table, filters=None, select="*", order=None):
    try:
        q = sb.table(table).select(select)
        if filters:
            for col, val in filters.items():
                q = q.eq(col, val)
        if order:
            q = q.order(order)
        result = q.execute()
        return pd.DataFrame(result.data) if result.data else pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao consultar {table}: {e}")
        return pd.DataFrame()

def sb_insert(table, data):
    try:
        result = sb.table(table).insert(data).execute()
        if result.data:
            return result.data[0].get("id")
    except Exception as e:
        st.error(f"Erro ao inserir em {table}: {e}")
    return None

def sb_update(table, data, match_col, match_val):
    try:
        sb.table(table).update(data).eq(match_col, match_val).execute()
    except Exception as e:
        st.error(f"Erro ao atualizar {table}: {e}")

def sb_delete(table, match_col, match_val):
    try:
        sb.table(table).delete().eq(match_col, match_val).execute()
    except Exception as e:
        st.error(f"Erro ao deletar em {table}: {e}")

def sb_fetch_one(table, filters):
    df = sb_query(table, filters=filters)
    if not df.empty:
        return df.iloc[0].to_dict()
    return None

# Tabelas já criadas no Supabase via SQL Editor

if "versao_senha_os" not in st.session_state:
    st.session_state.versao_senha_os = 0
if "versao_senha_cli" not in st.session_state:
    st.session_state.versao_senha_cli = 0
if "versao_senha_serv" not in st.session_state:
    st.session_state.versao_senha_serv = 0
if "versao_senha_desp" not in st.session_state:
    st.session_state.versao_senha_desp = 0
if "cupom_pronto" not in st.session_state:
    st.session_state.cupom_pronto = None
if "versao_nova_os" not in st.session_state:
    st.session_state.versao_nova_os = 0

# ==========================================
# 2. MENU LATERAL DE NAVEGAÇÃO
# ==========================================
if LOGO_PATH:
    import base64
    with open(LOGO_PATH, "rb") as img_file:
        logo_b64 = base64.b64encode(img_file.read()).decode()
    ext = LOGO_PATH.split(".")[-1].replace("jpg", "jpeg")
    st.sidebar.markdown(f"""
        <div style="text-align: center; padding: 10px 0 5px 0;">
            <img src="data:image/{ext};base64,{logo_b64}" style="width: 160px; display: inline-block;">
        </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.title("🧵 Silvia Castro Conserto de Roupas")
    
st.sidebar.write("---")
menu = st.sidebar.radio("Ir para:", [
    "Nova OS",
    "Painel de Trabalho (Kanban)",
    "Consultar / Editar OS",
    "Clientes",
    "Registrar Despesa",
    "Gráficos & Financeiro",
    "Catálogo de Serviços",
    "Funcionários"
])

# ==========================================
# TELA 1: NOVA OS
# ==========================================
if menu == "Nova OS":
    st.title("➕ Abertura de Nova Ordem de Serviço")
    
    df_max = sb_query("ordens_servico", select="id")
    ultimo_id = int(df_max["id"].max()) if not df_max.empty and not df_max["id"].isna().all() else 0
    proxima_os = (ultimo_id + 1) if ultimo_id is not None else 1
    
    st.info(f"📋 **Você está preenchendo a Ordem de Serviço Nº: #{proxima_os}**")
    
    clientes_df = sb_query("clientes", order="nome")
    _sf = sb_query("servicos", order="nome")
    servicos_df = _sf[["nome","preco"]] if not _sf.empty else pd.DataFrame(columns=["nome","preco"])

    v = st.session_state.versao_nova_os

    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.subheader("📋 Dados do Atendimento")
            cliente_novo = st.checkbox("👤 Cliente Novo / Não Cadastrado?", key=f"cli_novo_chk_{v}")
            
            if cliente_novo:
                name_novo = st.text_input("Nome da Nova Cliente", value="", key=f"nome_novo_{v}")
                whatsapp_novo = st.text_input("WhatsApp (com DDD, ex: 12996831392)", value="", key=f"whats_novo_{v}")
                cliente_id = None
                nome_final_cupom = name_novo
                whats_final_whatsapp = whatsapp_novo
            else:
                if clientes_df.empty:
                    st.info("💡 Não há clientes cadastradas. Vá no menu '👥 Clientes' ou marque a caixinha acima para começar!")
                    cliente_id = None
                    nome_final_cupom = ""
                    whats_final_whatsapp = ""
                else:
                    opcoes_clientes = {"Selecione uma cliente...": None}
                    for index, row in clientes_df.iterrows():
                        opcoes_clientes[f"{row['nome']} ({row['whatsapp']})"] = (row['id'], row['nome'], row['whatsapp'])
                    
                    cliente_selecionada = st.selectbox("Selecione a Cliente Já Cadastrada", list(opcoes_clientes.keys()), key=f"sel_cli_{v}")
                    
                    if opcoes_clientes[cliente_selecionada] is not None:
                        cliente_id = opcoes_clientes[cliente_selecionada][0]
                        nome_final_cupom = opcoes_clientes[cliente_selecionada][1]
                        whats_final_whatsapp = opcoes_clientes[cliente_selecionada][2]
                    else:
                        cliente_id = None
                        nome_final_cupom = ""
                        whats_final_whatsapp = ""
            
            lista_de_servicos = servicos_df['nome'].tolist()
            servicos_selecionados = st.multiselect("Selecione os Serviços Realizados", lista_de_servicos, key=f"multi_serv_{v}")
            
            servicos_selecionados_dados = []
            preco_sugerido = 0.0
            total_pecas_os = 0
            
            if servicos_selecionados:
                st.markdown("🔧 **Defina as quantidades abaixo:**")
                for s_nome in servicos_selecionados:
                    s_preco = float(servicos_df[servicos_df['nome'] == s_nome]['preco'].values[0])
                    col_nome, col_input = st.columns([3, 1])
                    with col_nome:
                        st.markdown(f"<p style='padding-top:10px;'>{s_nome} (R$ {s_preco:.2f})</p>", unsafe_allow_html=True)
                    with col_input:
                        qtd = st.number_input(f"Qtd para {s_nome}", min_value=1, value=1, step=1, key=f"qtd_{s_nome}_{v}", label_visibility="collapsed")
                    
                    preco_sugerido += (s_preco * qtd)
                    total_pecas_os += qtd
                    servicos_selecionados_dados.append(f"{s_nome} (x{qtd})")
                    
            st.write("---")
            prioridade = st.selectbox("Prioridade para a Production", ["Normal", "Alta 🚨"], key=f"prio_{v}")
            detalhes = st.text_area("Detalhes / Observações do Ajuste", value="", key=f"detalhes_{v}")
            
            st.write("---")
            funcionarios_lista = sb_query("funcionarios", order="nome")["nome"].tolist() if not sb_query("funcionarios", order="nome").empty else []
            if funcionarios_lista:
                atendente_selecionado = st.selectbox("👤 Atendente (quem está abrindo a OS)", ["— Selecione —"] + funcionarios_lista, key=f"atend_{v}")
                atendente_nome = atendente_selecionado if atendente_selecionado != "— Selecione —" else ""
            else:
                st.info("💡 Nenhum funcionário cadastrado. Acesse '👤 Funcionários' no menu.")
                atendente_nome = ""

    with col2:
        with st.container(border=True):
            st.subheader("💰 Valores, Prazos e Pagamento")
            
            chave_dinamica_total = f"total_calc_{preco_sugerido}_{v}"
            valor_final = st.number_input("Valor Cobrado Total (R$)", min_value=0.0, value=preco_sugerido, format="%.2f", key=chave_dinamica_total)
            
            c_sinal1, c_sinal2 = st.columns(2)
            with c_sinal1:
                valor_sinal = st.number_input("Sinal / Entrada (R$)", min_value=0.0, value=0.0, format="%.2f", key=f"val_sin_{v}")
            with c_sinal2:
                forma_sinal = st.selectbox("Forma de Pag. (Sinal)", ["Não se aplica", "Pix", "Dinheiro", "Cartão de Crédito", "Cartão de Débito"], key=f"forma_sin_{v}")
                
            forma_restante = st.selectbox("Forma de Pag. do Saldo Restante", ["Pendente (Paga na retirada)", "Pix", "Dinheiro", "Cartão de Crédito", "Cartão de Débito"], key=f"forma_res_{v}")
            
            data_entrega = st.date_input("Data de Entrega", value=None, min_value=datetime.today(), format="DD/MM/YYYY", key=f"data_ent_{v}")
            hora_pedido = st.time_input("Horário do Pedido (Hora atual)", value=datetime.now().time(), key=f"hora_ped_{v}")
            
            prazo_formatated = data_entrega.strftime('%d/%m/%Y') if data_entrega else ""
            data_atual_br = datetime.today().strftime('%d/%m')
            horario_pedido_formatado = f"{data_atual_br} - {hora_pedido.strftime('%H:%M')}"

    st.write("")
    if st.button("💾 Salvar e Gerar Cupom Térmico (80mm)", type="primary", use_container_width=True):
        if cliente_novo and (not name_novo or not whatsapp_novo):
            st.error("❌ Por favor, preencha o Nome e o WhatsApp da nova cliente.")
        elif cliente_novo and len("".join(filter(str.isdigit, whatsapp_novo))) < 10:
            st.error("❌ WhatsApp inválido. Digite apenas números com DDD (mínimo 10 dígitos).")
        elif not cliente_novo and cliente_id is None:
            st.error("❌ Selecione uma cliente cadastrada ou marque a caixinha de Cliente Novo.")
        elif not servicos_selecionados:
            st.error("❌ Por favor, selecione pelo menos um serviço.")
        elif not data_entrega:
            st.error("❌ Por favor, selecione a Data de Entrega.")
        else:
            pode_salvar = True
            if cliente_novo:
                checar_df = sb_query("clientes", filters={"nome": name_novo.strip()})
                checar = checar_df.iloc[0]["id"] if not checar_df.empty else None
                if checar:
                    st.error(f"⚠️ A cliente já está cadastrada no sistema!")
                    pode_salvar = False
                else:
                    cliente_id = sb_insert("clientes", {"nome": name_novo.strip(), "whatsapp": whatsapp_novo.strip()})
                    nome_final_cupom = name_novo.strip()
                    whats_final_whatsapp = whatsapp_novo.strip()
            
            if pode_salvar:
                texto_servicos_db = ", ".join(servicos_selecionados_dados)
                
                resta_pagar_calc = valor_final - valor_sinal
                forma_restante_db = "Quitado" if resta_pagar_calc <= 0 else forma_restante

                os_id = sb_insert("ordens_servico", {
                    "cliente_id": cliente_id, "servico_nome": texto_servicos_db, "detalhes": detalhes,
                    "valor_total": valor_final, "valor_sinal": valor_sinal, "prazo_entrega": prazo_formatated,
                    "horario_pedido": horario_pedido_formatado, "qtd_pecas": total_pecas_os,
                    "prioridade": prioridade, "forma_sinal": forma_sinal, "forma_restante": forma_restante_db,
                    "atendente_nome": atendente_nome
                })
                
                resta_pagar = valor_final - valor_sinal
                status_pagamento_cupom = f"RESTA PAGAR: R$ {resta_pagar:,.2f} ({forma_restante_db})" if resta_pagar > 0 else "STATUS VALOR: ✅ TOTALMENTE QUITADO"
                
                lista_servicos_cupom = ""
                for s in servicos_selecionados_dados:
                    lista_servicos_cupom += f"- {s}\n"
                
                texto_cupom = f"""=========================================
       {NOME_LOJA.upper()}              
 CNPJ: {CNPJ_LOJA}
 END: {ENDERECO_LOJA}
 TEL: {TELEFONE_LOJA}
-----------------------------------------
         --- VIA DO CLIENTE ---          
=========================================
OS NÚMERO: #{os_id}
DATA DO PEDIDO: {horario_pedido_formatado}
-----------------------------------------
CLIENTE: {nome_final_cupom}
WHATSAPP: {whats_final_whatsapp}
TOTAL DE PEÇAS: {total_pecas_os}
SERVIÇOS REALIZADOS:
{lista_servicos_cupom}-----------------------------------------
DETALHES: {detalhes if detalhes else 'Nenhum'}
-----------------------------------------
DATA DE ENTREGA: {prazo_formatated}
-----------------------------------------
VALOR TOTAL: R$ {valor_final:,.2f}
SINAL PAGO:  R$ {valor_sinal:,.2f} ({forma_sinal})
{status_pagamento_cupom}
=========================================
     Obrigado pela preferência!
=========================================











=========================================
      {NOME_LOJA.upper()}              
        --- VIA DA PRODUÇÃO ---         
=========================================
OS NÚMERO: #{os_id} {"[!!! ALTA PRIORIDADE !!!]" if prioridade == "Alta 🚨" else ""}
DATA DO PEDIDO: {horario_pedido_formatado}
-----------------------------------------
CLIENTE: {nome_final_cupom}
WHATSAPP: {whats_final_whatsapp}
TOTAL DE PEÇAS: {total_pecas_os}
SERVIÇOS REALIZADOS:
{lista_servicos_cupom}-----------------------------------------
DETALHES: {detalhes if detalhes else 'Nenhum'}
-----------------------------------------
VALOR TOTAL: R$ {valor_final:,.2f}
SINAL PAGO:  R$ {valor_sinal:,.2f} ({forma_sinal})
{status_pagamento_cupom}
-----------------------------------------
➡️ DATA DE ENTREGA: {prazo_formatated}
⚠️ PRIORIDADE: {prioridade.upper()}
-----------------------------------------
👤 ATENDENTE: {atendente_nome if atendente_nome else 'Não informado'}
=========================================
              
  PRODUÇÃO                  
=========================================









"""
                st.session_state.cupom_pronto = texto_cupom
                st.success("🎉 OS salva no banco de dados!")
                st.rerun()

    if st.session_state.cupom_pronto:
        with st.container(border=True):
            st.subheader("🖨️ Cupom Pronto para Impressão (Duas Vias)")
            st.text_area("Visualização do Cupom:", value=st.session_state.cupom_pronto, height=450)
            
            # Escapa backticks e barras do cupom para evitar quebra do template literal JS
            cupom_js_safe = (
                st.session_state.cupom_pronto
                .replace("\\", "\\\\")
                .replace("`", "\\`")
                .replace("$", "\\$")
            )
            html_impressao = f"""
            <script>
            function imprimirCupom() {{
                var receita = `{cupom_js_safe}`;
                var janela = window.open('', '', 'width=300,height=800');
                janela.document.write('<pre style="font-family: monospace; font-size: 12px; margin: 0; padding: 10px; white-space: pre-wrap;">' + receita + '</pre>');
                janela.document.close();
                janela.focus();
                janela.print();
                janela.close();
            }}
            </script>
            <button onclick="imprimirCupom()" style="
                width: 100%; 
                background-color: #28a745; 
                color: white; 
                padding: 12px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                font-weight: bold; 
                font-size: 16px;
                margin-bottom: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">🖨️ Imprimir Duas Vias na Impressora Térmica</button>
            """
            st.components.v1.html(html_impressao, height=60)
            
            if st.button("Fechar / Nova Venda", use_container_width=True):
                st.session_state.cupom_pronto = None
                st.session_state.versao_nova_os += 1
                st.rerun()

# ==========================================
# TELA: CONSULTAR / EDITAR OS
# ==========================================
elif menu == "Consultar / Editar OS":
    st.title("🔍 Consulta Geral de Ordens de Serviço")
    
    busca_os = st.text_input("🔍 Buscar OS (Digite o Nº da OS ou o nome da Cliente)")
    aba_ativas, aba_entregues = st.tabs(["📌 OS Ativas", "📦 Histórico de OS Entregues"])
    
    clausula_busca = ""
    parametros_busca = []
    if busca_os:
        if busca_os.isdigit():
            clausula_busca = " AND (os.id = ?) "
            parametros_busca.append(int(busca_os))
        else:
            clausula_busca = " AND (c.nome LIKE ?) "
            parametros_busca.append(f"%{busca_os}%")

    os_clicada_id = None

    with aba_ativas:
        try:
            _df_os_a = sb_query("ordens_servico", order="id")
            _df_cli_a = sb_query("clientes")
            if not _df_os_a.empty and not _df_cli_a.empty:
                _df_os_a = _df_os_a.merge(_df_cli_a.rename(columns={"id":"cliente_id","nome":"Cliente","whatsapp":"whatsapp"}), on="cliente_id", how="left")
            _df_os_a = _df_os_a[_df_os_a["status"] != "Entregue"] if not _df_os_a.empty else _df_os_a
            if busca_os and not _df_os_a.empty:
                if busca_os.isdigit():
                    _df_os_a = _df_os_a[_df_os_a["id"] == int(busca_os)]
                else:
                    _df_os_a = _df_os_a[_df_os_a["Cliente"].str.contains(busca_os, case=False, na=False)]
            if not _df_os_a.empty:
                _df_os_a = _df_os_a.sort_values("id", ascending=False)
                _df_os_a["Falta Pagar (R$)"] = _df_os_a["valor_total"] - _df_os_a["valor_sinal"]
                df_ativas = _df_os_a.rename(columns={"id":"Nº OS","prioridade":"🚨 Prioridade","qtd_pecas":"Total Peças","servico_nome":"Serviços (Qtd)","valor_total":"Total (R$)","horario_pedido":"Abertura/Hora","prazo_entrega":"Data Entrega","status":"Status"})
            else:
                df_ativas = pd.DataFrame()
            if df_ativas.empty:
                st.info("Nenhuma Ordem de Serviço ativa encontrada.")
            else:
                df_ativas['Situação Financeira'] = df_ativas['Falta Pagar (R$)'].apply(lambda x: "✅ Quitado" if x <= 0 else f"⚠️ Falta R$ {x:.2f}")
                
                selecao_ativas = st.dataframe(
                    df_ativas[['Nº OS', 'Cliente', '🚨 Prioridade', 'Total Peças', 'Serviços (Qtd)', 'Total (R$)', 'Situação Financeira', 'Abertura/Hora', 'Data Entrega', 'Status']], 
                    use_container_width=True, 
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="single-row"
                )
                if selecao_ativas and "rows" in selecao_ativas["selection"] and selecao_ativas["selection"]["rows"]:
                    idx_linha = selecao_ativas["selection"]["rows"][0]
                    os_clicada_id = int(df_ativas.iloc[idx_linha]['Nº OS'])
        except Exception as e:
            st.error(f"Erro ao buscar OS Ativas: {e}")

    with aba_entregues:
        try:
            _df_os_e = sb_query("ordens_servico", order="id")
            _df_cli_e = sb_query("clientes")
            if not _df_os_e.empty and not _df_cli_e.empty:
                _df_os_e = _df_os_e.merge(_df_cli_e.rename(columns={"id":"cliente_id","nome":"Cliente","whatsapp":"whatsapp"}), on="cliente_id", how="left")
            _df_os_e = _df_os_e[_df_os_e["status"] == "Entregue"] if not _df_os_e.empty else _df_os_e
            if busca_os and not _df_os_e.empty:
                if busca_os.isdigit():
                    _df_os_e = _df_os_e[_df_os_e["id"] == int(busca_os)]
                else:
                    _df_os_e = _df_os_e[_df_os_e["Cliente"].str.contains(busca_os, case=False, na=False)]
            if not _df_os_e.empty:
                _df_os_e = _df_os_e.sort_values("id", ascending=False)
                _df_os_e["Falta Pagar (R$)"] = _df_os_e["valor_total"] - _df_os_e["valor_sinal"]
                df_entregues = _df_os_e.rename(columns={"id":"Nº OS","qtd_pecas":"Total Peças","servico_nome":"Serviços (Qtd)","valor_total":"Total (R$)","horario_pedido":"Abertura/Hora","prazo_entrega":"Data Entrega","status":"Status"})
            else:
                df_entregues = pd.DataFrame()
            if df_entregues.empty:
                st.info("Nenhuma Ordem de Serviço entregue encontrada.")
            else:
                df_entregues['Situação Financeira'] = df_entregues['Falta Pagar (R$)'].apply(lambda x: "✅ Quitado" if x <= 0 else f"⚠️ Falta R$ {x:.2f}")
                
                selecao_entregues = st.dataframe(
                    df_entregues[['Nº OS', 'Cliente', 'Total Peças', 'Serviços (Qtd)', 'Total (R$)', 'Situação Financeira', 'Abertura/Hora', 'Data Entrega', 'Status']], 
                    use_container_width=True, 
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="single-row"
                )
                if selecao_entregues and "rows" in selecao_entregues["selection"] and selecao_entregues["selection"]["rows"]:
                    idx_linha = selecao_entregues["selection"]["rows"][0]
                    os_clicada_id = int(df_entregues.iloc[idx_linha]['Nº OS'])
        except Exception as e:
            st.error(f"Erro ao buscar Histórico: {e}")
        
    st.divider()
    with st.container(border=True):
        st.subheader("📝 Modificar, Reabrir ou Cancelar uma OS")
        
        if os_clicada_id is None:
            st.info("💡 Clique em cima de qualquer Ordem de Serviço nas tabelas superiores para liberar a consulta e alteração dos dados.")
        else:
            try:
                _df_ed = sb_query("ordens_servico", order="id")
                _df_cli_ed = sb_query("clientes")
                if not _df_ed.empty and not _df_cli_ed.empty:
                    _df_ed = _df_ed.merge(_df_cli_ed.rename(columns={"id":"cliente_id","nome":"Cliente"}), on="cliente_id", how="left")
                    _df_ed = _df_ed.sort_values("id", ascending=False)
                    df_todas_edicao = _df_ed.rename(columns={"id":"Nº OS","servico_nome":"Serviços"})
                else:
                    df_todas_edicao = pd.DataFrame()
            except:
                df_todas_edicao = pd.DataFrame()
            
            if df_todas_edicao.empty:
                st.caption("Nenhuma Ordem de Serviço disponível para alteração.")
            else:
                opcoes_os = {f"OS #{row['Nº OS']} - {row['Cliente']} ({row['Serviços']})": row['Nº OS'] for _, row in df_todas_edicao.iterrows()}
                lista_opcoes = list(opcoes_os.keys())
                
                index_padrao = 0
                for idx, texto in enumerate(lista_opcoes):
                    if opcoes_os[texto] == os_clicada_id:
                        index_padrao = idx
                        break

                os_selecionada = st.selectbox(
                    "OS Selecionada", 
                    lista_opcoes, 
                    index=index_padrao,
                    disabled=True
                )
                id_os = opcoes_os[os_selecionada]
                
                _dos = sb_fetch_one("ordens_servico", {"id": id_os})
                dados_os = (_dos["detalhes"], _dos["valor_total"], _dos["valor_sinal"], _dos["prazo_entrega"], _dos["status"], _dos["horario_pedido"], _dos["forma_sinal"], _dos["forma_restante"]) if _dos else None
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    novo_detalhe = st.text_area("Alterar Detalhes/Observações", value=dados_os[0] if dados_os[0] else "")
                    lista_status = ["A Iniciar", "Em Andamento", "Finalizado", "Avisado", "Entregue"]
                    novo_status = st.selectbox("Alterar Status da OS", lista_status, index=lista_status.index(dados_os[4]) if dados_os[4] in lista_status else 0)
                with c2:
                    novo_total = st.number_input("Alterar Valor Total (R$)", min_value=0.0, value=float(dados_os[1]), format="%.2f")
                    novo_sinal = st.number_input("Alterar Sinal (R$)", min_value=0.0, value=float(dados_os[2]), format="%.2f")
                    lista_pagamentos = ["Não se aplica", "Pix", "Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pendente (Paga na retirada)", "Quitado"]
                    novo_forma_sinal = st.selectbox("Alterar Pag. Sinal", lista_pagamentos, index=lista_pagamentos.index(dados_os[6]) if dados_os[6] in lista_pagamentos else 0)
                    novo_forma_restante = st.selectbox("Alterar Pag. Restante", lista_pagamentos, index=lista_pagamentos.index(dados_os[7]) if dados_os[7] in lista_pagamentos else 0)
                with c3:
                    novo_prazo = st.text_input("Alterar Data de Entrega", value=dados_os[3])
                    novo_hora_ped = st.text_input("Alterar Horário/Data do Pedido", value=dados_os[5] if dados_os[5] else "")
                    chave_senha_os = f"senha_os_v_{st.session_state.versao_senha_os}"
                    senha_digitada = st.text_input("🔑 Digite a senha para autorizar mudanças", type="password", key=chave_senha_os)

                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("Salvar Alterações / Reabrir OS ✅", use_container_width=True, type="primary"):
                        if senha_digitada == SENHA_MASTER:
                            f_restante = "Quitado" if novo_sinal >= novo_total else novo_forma_restante
                            
                            sb_update("ordens_servico", {
                                "detalhes": novo_detalhe, "valor_total": novo_total, "valor_sinal": novo_sinal,
                                "prazo_entrega": novo_prazo, "status": novo_status, "horario_pedido": novo_hora_ped,
                                "forma_sinal": novo_forma_sinal, "forma_restante": f_restante
                            }, "id", id_os)
                            st.success(f"✅ OS #{id_os} atualizada com sucesso!")
                            st.session_state.versao_senha_os += 1
                            st.rerun()
                        else:
                            st.error("❌ Senha incorreta!")
                with col_b2:
                    if st.button("Excluir / Cancelar OS ❌", use_container_width=True):
                        if senha_digitada == SENHA_MASTER:
                            sb_delete("ordens_servico", "id", id_os)
                            st.warning(f"OS #{id_os} apagada!")
                            st.session_state.versao_senha_os += 1
                            st.rerun()
                        else:
                            st.error("❌ Senha incorreta!")

# ==========================================
# TELA: CLIENTES
# ==========================================
elif menu == "Clientes":
    st.title("👥 Gestão de Clientes")
    
    cliente_clicado_id = None
    col_cadastro, col_lista = st.columns([1, 1.5])
    
    with col_lista:
        with st.container(border=True):
            st.subheader("🔍 Lista Geral de Clientes")
            busca = st.text_input("Buscar cliente por nome...")
            if busca:
                dados_clientes = sb_query("clientes", order="nome").rename(columns={"id":"Código","nome":"Nome","whatsapp":"WhatsApp"}).loc[lambda df: df["Nome"].str.contains(busca, case=False, na=False)]
            else:
                dados_clientes = sb_query("clientes", order="nome").rename(columns={"id":"Código","nome":"Nome","whatsapp":"WhatsApp"})
            
            selecao_clientes = st.dataframe(
                dados_clientes, 
                use_container_width=True, 
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row"
            )
            if selecao_clientes and "rows" in selecao_clientes["selection"] and selecao_clientes["selection"]["rows"]:
                idx_linha = selecao_clientes["selection"]["rows"][0]
                cliente_clicado_id = int(dados_clientes.iloc[idx_linha]['Código'])

    with col_cadastro:
        with st.container(border=True):
            st.subheader("➕ Novo Cadastro")
            nome_cliente = st.text_input("Nome Completo", key="cad_nome")
            whatsapp_cliente = st.text_input("WhatsApp (Apenas números com DDD)", key="cad_whats")
            if st.button("Salvar Cliente", type="primary", use_container_width=True):
                if nome_cliente and whatsapp_cliente:
                    checar_df2 = sb_query("clientes", filters={"nome": nome_cliente.strip()})
                    checar = checar_df2.iloc[0]["id"] if not checar_df2.empty else None
                    if checar:
                        st.error("⚠️ Este nome de cliente já está cadastrado!")
                    else:
                        sb_insert("clientes", {"nome": nome_cliente.strip(), "whatsapp": whatsapp_cliente.strip()})
                        st.success("Cliente salva com sucesso!")
                        st.rerun()
                else:
                    st.error("Por favor, preencha todos os campos.")

        with st.container(border=True):
            st.subheader("📝 Gerenciar & Histórico")
            
            if cliente_clicado_id is None:
                st.info("💡 Selecione um cliente na tabela ao lado para gerenciar seu cadastro e ver o histórico de ordens.")
            else:
                clientes_lista = sb_query("clientes", order="nome")[["id","nome"]]
                if not clientes_lista.empty:
                    dict_clientes = {row['nome']: row['id'] for _, row in clientes_lista.iterrows()}
                    lista_nomes = list(dict_clientes.keys())
                    
                    index_cli_padrao = 0
                    for idx, nome in enumerate(lista_nomes):
                        if dict_clientes[nome] == cliente_clicado_id:
                            index_cli_padrao = idx
                            break
                            
                    cliente_gerenciar = st.selectbox(
                        "Cliente Selecionado", 
                        lista_nomes, 
                        index=index_cli_padrao,
                        disabled=True
                    )
                    id_gerenciar = dict_clientes[cliente_gerenciar]
                    _dc = sb_fetch_one("clientes", {"id": id_gerenciar})
                    dados_atuais = (_dc["nome"], _dc["whatsapp"]) if _dc else None
                    
                    st.markdown(f"📊 **Histórico de Serviços de {dados_atuais[0]}:**")
                    try:
                        _hcli = sb_query("ordens_servico", filters={"cliente_id": int(id_gerenciar)}, order="id")
                        if not _hcli.empty:
                            _hcli["Saldo Devedor"] = _hcli["valor_total"] - _hcli["valor_sinal"]
                            df_historico_cli = _hcli.sort_values("id", ascending=False).rename(columns={"id":"Nº OS","servico_nome":"Serviços","valor_total":"Total (R$)","prazo_entrega":"Entrega","status":"Status"})[["Nº OS","Serviços","Total (R$)","Saldo Devedor","Entrega","Status"]]
                        else:
                            df_historico_cli = pd.DataFrame()
                        
                        if df_historico_cli.empty:
                            st.caption("Nenhum serviço registrado para este cliente.")
                        else:
                            df_historico_cli['Pagamento'] = df_historico_cli['Saldo Devedor'].apply(lambda x: "✅ Quitado" if x <= 0 else f"❌ Falta R$ {x:.2f}")
                            st.dataframe(df_historico_cli[['Nº OS', 'Serviços', 'Total (R$)', 'Pagamento', 'Entrega', 'Status']], use_container_width=True, hide_index=True)
                    except Exception as e:
                        st.caption("Não foi possível carregar o histórico.")
                    
                    st.write("---")
                    st.markdown("✏️ **Editar dados do cliente:**")
                    novo_nome = st.text_input("Alterar Nome", value=dados_atuais[0])
                    novo_whats = st.text_input("Alterar WhatsApp", value=dados_atuais[1])
                    chave_senha_cli = f"senha_cli_v_{st.session_state.versao_senha_cli}"
                    senha_cliente = st.text_input("🔑 Senha para Modificar Cliente", type="password", key=chave_senha_cli)
                    
                    c_edit, c_del = st.columns(2)
                    with c_edit:
                        if st.button("Salvar Alteração ✅", use_container_width=True):
                            if senha_cliente == SENHA_MASTER:
                                sb_update("clientes", {"nome": novo_nome.strip(), "whatsapp": novo_whats.strip()}, "id", id_gerenciar)
                                st.success("✅ Cadastro atualizado com sucesso!")
                                st.session_state.versao_senha_cli += 1
                                st.rerun()
                            else:
                                st.error("❌ Senha incorreta!")
                    with c_del:
                        if st.button("Excluir Cliente ❌", type="secondary", use_container_width=True):
                            if senha_cliente == SENHA_MASTER:
                                sb_delete("clientes", "id", id_gerenciar)
                                sb_delete("ordens_servico", "cliente_id", id_gerenciar)
                                st.warning("Cliente e suas OS foram excluídos!")
                                st.session_state.versao_senha_cli += 1
                                st.rerun()
                            else:
                                st.error("❌ Senha incorreta!")
                else:
                    st.caption("Nenhum cliente cadastrado.")

# ==========================================
# TELA: KANBAN (COM NOVO FILTRO DE DATA)
# ==========================================
elif menu == "Painel de Trabalho (Kanban)":
    st.title("📋 Painel de Trabalho da Oficina")
    
    # Linha com os dois filtros do sistema no topo
    col_f1, col_f2 = st.columns([1.5, 1])
    
    with col_f1:
        busca_kanban = st.text_input("🔍 Filtrar Painel (Digite o Nº da OS ou o Nome da Cliente)", value="")
        
    with col_f2:
        opcao_data = st.selectbox(
            "📅 Filtrar por Prazo de Entrega:",
            ["Todos os Prazos", "Hoje", "Amanhã", "Atrasadas 🚨", "Escolher uma Data Específica"]
        )
        
    # Tratamento lógico das datas de filtro
    hoje_str = datetime.today().strftime('%d/%m/%Y')
    amanha_str = (datetime.today() + timedelta(days=1)).strftime('%d/%m/%Y')
    
    data_alvo = None
    filtrar_atrasadas = False
    
    if opcao_data == "Hoje":
        data_alvo = hoje_str
    elif opcao_data == "Amanhã":
        data_alvo = amanha_str
    elif opcao_data == "Atrasadas 🚨":
        filtrar_atrasadas = True
    elif opcao_data == "Escolher uma Data Específica":
        data_escolhida = st.date_input("Selecione a data limite para produção:", value=datetime.today(), format="DD/MM/YYYY")
        if data_escolhida:
            data_alvo = data_escolhida.strftime('%d/%m/%Y')

    try:
        query_base = """
            SELECT os.id, c.nome as cliente, c.whatsapp, os.servico_nome, os.prazo_entrega, os.status, os.qtd_pecas, os.prioridade, os.horario_pedido, os.valor_total, os.valor_sinal
            FROM ordens_servico os JOIN clientes c ON os.cliente_id = c.id 
            WHERE os.status != 'Entregue'
        """
        _df_k = sb_query("ordens_servico", order="id")
        _df_kc = sb_query("clientes")
        if not _df_k.empty and not _df_kc.empty:
            _df_k = _df_k.merge(_df_kc.rename(columns={"id":"cliente_id","nome":"cliente"}), on="cliente_id", how="left")
        df_os = _df_k if not _df_k.empty else pd.DataFrame()
    except:
        df_os = pd.DataFrame()
        
    # Aplicação do filtro de Texto/Número
    if not df_os.empty and busca_kanban:
        texto_busca = busca_kanban.strip().lower()
        if texto_busca.isdigit():
            df_os = df_os[df_os['id'] == int(texto_busca)]
        else:
            df_os = df_os[df_os['cliente'].str.lower().str.contains(texto_busca)]
            
    # Aplicação do novo filtro de Datas
    if not df_os.empty:
        if data_alvo:
            df_os = df_os[df_os['prazo_entrega'] == data_alvo]
        elif filtrar_atrasadas:
            # Converte temporariamente para data para fazer a validação com segurança
            def checar_se_atrasou(prazo):
                try:
                    return datetime.strptime(prazo, '%d/%m/%Y').date() < datetime.today().date()
                except:
                    return False
            df_os = df_os[df_os['prazo_entrega'].apply(checar_se_atrasou)]
        
    col_iniciar, col_andamento, col_pronto, col_avisado = st.columns(4)
    
    with col_iniciar:
        st.markdown("### 📥 A Iniciar")
        if not df_os.empty:
            for idx, os_data in df_os[df_os['status'] == 'A Iniciar'].iterrows():
                with st.container(border=True):
                    if os_data['prioridade'] == "Alta 🚨":
                        st.markdown("<span style='color:red; font-weight:bold;'>🚨 URGENTE</span>", unsafe_allow_html=True)
                        
                    st.markdown(f"**OS #{os_data['id']} - {os_data['cliente']}**")
                    st.markdown(f"🧵 {os_data['servico_nome']}")
                    st.markdown(f"<small>⏱️ Aberta: {os_data['horario_pedido']}<br>📅 Limite: {os_data['prazo_entrega']}</small>", unsafe_allow_html=True)
                    
                    if st.button("Começar 🧵", key=f"ini_{os_data['id']}", use_container_width=True):
                        sb_update('ordens_servico', {'status': 'Em Andamento'}, 'id', os_data['id'])
                        st.rerun()
                      
    with col_andamento:
        st.markdown("### 🧵 Em Andamento")
        if not df_os.empty:
            for idx, os_data in df_os[df_os['status'] == 'Em Andamento'].iterrows():
                with st.container(border=True):
                    if os_data['prioridade'] == "Alta 🚨":
                        st.markdown("<span style='color:red; font-weight:bold;'>🚨 URGENTE</span>", unsafe_allow_html=True)
                        
                    st.markdown(f"**OS #{os_data['id']} - {os_data['cliente']}**")
                    st.markdown(f"🧵 {os_data['servico_nome']}")
                    st.markdown(f"<small>⏱️ Aberta: {os_data['horario_pedido']}<br>📅 Limite: {os_data['prazo_entrega']}</small>", unsafe_allow_html=True)
                    
                    if st.button("Pronto ✅", key=f"and_{os_data['id']}", use_container_width=True):
                        sb_update('ordens_servico', {'status': 'Finalizado'}, 'id', os_data['id'])
                        st.rerun()
                       
    with col_pronto:
        st.markdown("### ✅ Pronto")
        if not df_os.empty:
            for idx, os_data in df_os[df_os['status'] == 'Finalizado'].iterrows():
                with st.container(border=True):
                    if os_data['prioridade'] == "Alta 🚨":
                        st.markdown("<span style='color:red; font-weight:bold;'>🚨 URGENTE</span>", unsafe_allow_html=True)
                        
                    st.markdown(f"**OS #{os_data['id']} - {os_data['cliente']}**")
                    st.markdown(f"🧵 {os_data['servico_nome']}")
                    st.markdown(f"<small>📅 Limite original: {os_data['prazo_entrega']}</small>", unsafe_allow_html=True)
                    
                    nome_completo_banco = os_data['cliente']
                    if nome_completo_banco:
                        nome_cliente = nome_completo_banco.split()[0].strip().capitalize()
                    else:
                        nome_cliente = "Cliente"
                   
                    hora_atual = datetime.now().hour
                    saudacao = "Bom dia" if hora_atual < 12 else "Boa tarde"
                    
                    total_pecas = os_data['qtd_pecas']
                    if total_pecas == 1:
                        texto_peca_completo = "a sua peça já está *pronta* para a retirada, está esperando por você!"
                    else:
                        texto_peca_completo = "as suas peças já estão *prontas* para a retirada, estão esperando por você!"
                    
                    msg = f"""{saudacao}, {nome_cliente}! ✨

Passando para avisar que {texto_peca_completo} 🧵✂️

⏰ Nosso horário: Segunda a Sexta, das 8h30 às 17h30 e Sábado, das 9h às 13h.
Obrigada pela preferência e confiança em nosso trabalho! 
*Silvia Castro Conserto de Roupas*"""
                    
                    numero_limpo = "".join(filter(str.isdigit, str(os_data['whatsapp'])))
                    msg_url = urllib.parse.quote(msg)
                    link_whats = f"https://api.whatsapp.com/send?phone=55{numero_limpo}&text={msg_url}"
                    
                    html_botao_whats = f"""
                    <div style="width: 100%; display: flex; justify-content: center; align-items: center; margin: 8px 0;">
                        <a href="{link_whats}" target="_blank" style="text-decoration: none; width: 100%;">
                            <button style="
                                width: 100%;
                                background-color: #25D366;
                                color: white;
                                border: none;
                                padding: 10px 14px;
                                border-radius: 8px;
                                font-weight: 600;
                                cursor: pointer;
                                font-size: 14px;
                                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                box-sizing: border-box;
                            ">💬 Enviar Aviso Pronto ({saudacao})</button>
                        </a>
                    </div>
                    """
                    st.components.v1.html(html_botao_whats, height=50)
                    
                    if st.button("Mover p/ Avisados 📱", key=f"avi_{os_data['id']}", use_container_width=True, type="primary"):
                        sb_update('ordens_servico', {'status': 'Avisado'}, 'id', os_data['id'])
                        st.rerun()
      
    with col_avisado:
        st.markdown("### 📱 Avisados")
        if not df_os.empty:
            for idx, os_data in df_os[df_os['status'] == 'Avisado'].iterrows():
                with st.container(border=True):
                    saldo = float(os_data['valor_total']) - float(os_data['valor_sinal'])
                    
                    if os_data['prioridade'] == "Alta 🚨":
                        st.markdown("<span style='color:red; font-weight:bold;'>🚨 URGENTE</span>", unsafe_allow_html=True)
                        
                    # Alerta visual de status financeiro superior
                    if saldo > 0:
                        st.markdown(f"<span style='background-color:#ffebee; color:#c62828; padding:2px 6px; border-radius:4px; font-size:11px; font-weight:bold;'>⚠️ FALTAM R$ {saldo:.2f}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='background-color:#e8f5e9; color:#2e7d32; padding:2px 6px; border-radius:4px; font-size:11px; font-weight:bold;'>✅ QUITADO</span>", unsafe_allow_html=True)
                        
                    st.markdown(f"**OS #{os_data['id']} - {os_data['cliente']}**")
                    st.markdown(f"🧵 {os_data['servico_nome']}")
                    st.markdown(f"<small>📅 Prazo original: {os_data['prazo_entrega']}</small>", unsafe_allow_html=True)
                    
                    # Seletor Central Único para definição do meio de pagamento restante
                    meio_quitacao = "Quitado"
                    if saldo > 0:
                        st.write("---")
                        col_q1, col_q2 = st.columns([1.2, 1])
                        with col_q1:
                            meio_quitacao = st.selectbox("Forma Restante", ["Pix", "Dinheiro", "Cartão"], key=f"q_avis_meio_{os_data['id']}", label_visibility="collapsed")
                        with col_q2:
                            if st.button("Quitar 💵", key=f"btn_q_avis_{os_data['id']}", use_container_width=True):
                                sb_update('ordens_servico', {'valor_sinal': os_data['valor_total'], 'forma_restante': meio_quitacao}, 'id', os_data['id'])
                                st.rerun()
                                
                    st.write("---")
                    
                    if st.button("Entregue 📦", key=f"fim_{os_data['id']}", use_container_width=True, type="primary"):
                        forma_final = meio_quitacao if saldo > 0 else "Quitado"
                        sinal_final = os_data['valor_total'] if saldo > 0 else os_data['valor_sinal']
                        
                        sb_update('ordens_servico', {'status': 'Entregue', 'valor_sinal': sinal_final, 'forma_restante': forma_final}, 'id', os_data['id'])
                        st.rerun()

# ==========================================
# TELA: CATÁLOGO DE SERVIÇOS
# ==========================================
elif menu == "Catálogo de Serviços":
    st.title("🏷️ Catálogo de Serviços & Preços")
    
    servico_clicado_id = None
    col_cad, col_tab = st.columns([1, 1.5])
    
    with col_tab:
        with st.container(border=True):
            st.subheader("Serviços Ativos")
            busca_serv = st.text_input("Buscar serviço por nome...")
            
            if busca_serv:
                _dfs = sb_query("servicos", order="nome")
                if busca_serv:
                    _dfs = _dfs[_dfs["nome"].str.contains(busca_serv, case=False, na=False)]
                df_servicos_lista = _dfs.rename(columns={"id":"Código","nome":"Serviço","preco":"Preço Base (R$)"}) if not _dfs.empty else pd.DataFrame()
            else:
                df_servicos_lista = sb_query("servicos", order="nome").rename(columns={"id":"Código","nome":"Serviço","preco":"Preço Base (R$)"})
            
            selecao_servicos = st.dataframe(
                df_servicos_lista, 
                use_container_width=True, 
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row"
            )
            if selecao_servicos and "rows" in selecao_servicos["selection"] and selecao_servicos["selection"]["rows"]:
                idx_linha = selecao_servicos["selection"]["rows"][0]
                servico_clicado_id = int(df_servicos_lista.iloc[idx_linha]['Código'])

    with col_cad:
        with st.container(border=True):
            st.subheader("➕ Novo Serviço")
            novo_servico = st.text_input("Nome do Serviço")
            novo_preco = st.number_input("Preço Sugerido (R$)", min_value=0.0, format="%.2f")
            if st.button("Adicionar", type="primary", use_container_width=True):
                if novo_servico:
                    sb_insert("servicos", {"nome": novo_servico, "preco": novo_preco})
                    st.success("Adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, preencha o nome do serviço.")

        with st.container(border=True):
            st.subheader("📝 Gerenciar Serviço")
            
            if servico_clicado_id is None:
                st.info("💡 Selecione um serviço na tabela ao lado para editar ou excluir seu cadastro.")
            else:
                _ds = sb_fetch_one("servicos", {"id": servico_clicado_id})
                dados_serv_atual = (_ds["nome"], _ds["preco"]) if _ds else None
                
                st.markdown(f"✏️ **Modificando:** {dados_serv_atual[0]}")
                alterar_nome_serv = st.text_input("Alterar Nome do Serviço", value=dados_serv_atual[0])
                alterar_preco_serv = st.number_input("Alterar Preço (R$)", min_value=0.0, value=float(dados_serv_atual[1]), format="%.2f")
                
                chave_senha_serv = f"senha_serv_v_{st.session_state.versao_senha_serv}"
                senha_servico = st.text_input("🔑 Senha para Autorizar", type="password", key=chave_senha_serv)
                
                c_edit_s, c_del_s = st.columns(2)
                with c_edit_s:
                    if st.button("Salvar Alteração ✅", key="btn_edit_serv", use_container_width=True):
                        if senha_servico == SENHA_MASTER:
                            if alterar_nome_serv:
                                sb_update("servicos", {"nome": alterar_nome_serv.strip(), "preco": alterar_preco_serv}, "id", servico_clicado_id)
                                st.success("Serviço atualizado!")
                                st.session_state.versao_senha_serv += 1
                                st.rerun()
                            else:
                                st.error("O nome do serviço não pode ficar vazio.")
                        else:
                            st.error("❌ Senha incorreta!")
                            
                with c_del_s:
                    if st.button("Excluir Serviço ❌", key="btn_del_serv", type="secondary", use_container_width=True):
                        if senha_servico == SENHA_MASTER:
                            sb_delete("servicos", "id", servico_clicado_id)
                            st.warning("Serviço excluído do catálogo!")
                            st.session_state.versao_senha_serv += 1
                            st.rerun()
                        else:
                            st.error("❌ Senha incorreta!")

# ==========================================
# TELA: DESPESAS (PRO FLUXO DE CAIXA)
# ==========================================
elif menu == "Registrar Despesa":
    st.title("💸 Fluxo de Caixa & Controle de Despesas")
    
    with st.container(border=True):
        st.subheader("🔍 Filtros de Consulta")
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        with f_col1:
            data_inicio = st.date_input("Data de Início", value=datetime.today() - timedelta(days=30), format="DD/MM/YYYY")
        with f_col2:
            data_fim = st.date_input("Data de Fim", value=datetime.today(), format="DD/MM/YYYY")
        with f_col3:
            filtro_tipo = st.selectbox("Tipo de Despesa", ["Todas", "Fixa", "Diária / Variável"])
        with f_col4:
            filtro_status = st.selectbox("Status", ["Todos", "Paga", "Pendente / Agendada"])

    query_desp = "SELECT id, data, descricao, valor, category, tipo, status FROM despesas WHERE data BETWEEN ? AND ?"
    params_desp = [data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')]
    
    if filtro_tipo != "Todas":
        query_desp += " AND tipo = ?"
        params_desp.append(filtro_tipo)
    if filtro_status != "Todos":
        query_desp += " AND status = ?"
        params_desp.append(filtro_status)
        
    query_desp += " ORDER BY data DESC, id DESC"
    _dfd = sb_query("despesas", order="data")
    if not _dfd.empty:
        if data_inicio and data_fim:
            _dfd = _dfd[(_dfd["data"] >= data_inicio.strftime('%Y-%m-%d')) & (_dfd["data"] <= data_fim.strftime('%Y-%m-%d'))]
        if filtro_status != "Todos":
            _dfd = _dfd[_dfd["status"] == filtro_status]
        _dfd = _dfd.sort_values("data", ascending=False)
    df_despesas_filtradas = _dfd

    total_pago = 0.0
    total_pendente = 0.0
    if not df_despesas_filtradas.empty:
        total_pago = float(df_despesas_filtradas[df_despesas_filtradas['status'] == 'Paga']['valor'].sum())
        total_pendente = float(df_despesas_filtradas[df_despesas_filtradas['status'] == 'Pendente / Agendada']['valor'].sum())
    total_geral = total_pago + total_pendente

    with st.container(border=True):
        m1, m2, m3 = st.columns(3)
        m1.metric("🟢 Total Pago", f"R$ {total_pago:,.2f}")
        m2.metric("🔴 Total Pendente (A Vencer)", f"R$ {total_pendente:,.2f}")
        m3.metric("📊 Total Geral do Período", f"R$ {total_geral:,.2f}")

    st.divider()

    despesa_clicada_id = None
    col_cad, col_hist = st.columns([1, 1.8])
    
    with col_cad:
        with st.container(border=True):
            st.subheader("➕ Lançar Despesa")
            desc = st.text_input("Descrição da Conta / Gasto")
            val = st.number_input("Valor do Gasto (R$)", min_value=0.0, format="%.2f")
            cat = st.selectbox("Categoria do Item", ["Insumos", "Infraestrutura", "Manutenção", "Aluguel", "Funcionários", "Outros"])
            
            c_lan1, c_lan2 = st.columns(2)
            with c_lan1:
                tipo_gasto = st.selectbox("Tipo de Custo", ["Diária / Variável", "Fixa"])
            with c_lan2:
                status_gasto = st.selectbox("Situação Atual", ["Paga", "Pendente / Agendada"])
                
            data_gasto = st.date_input("Data do Vencimento/Gasto", value=datetime.today(), format="DD/MM/YYYY")
            
            if st.button("Lançar no Caixa 💸", type="primary", use_container_width=True):
                if desc and val > 0:
                    sb_insert("despesas", {
                        "descricao": desc.strip(), "valor": val,
                        "data": data_gasto.strftime('%Y-%m-%d'), "category": cat,
                        "tipo": tipo_gasto, "status": status_gasto
                    })
                    st.success("Despesa registrada com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, preencha a descrição e defina um valor maior que R$ 0.00.")

    with col_hist:
        with st.container(border=True):
            st.subheader("📝 Extrato de Contas")
            if df_despesas_filtradas.empty:
                st.info("Nenhuma despesa localizada para este período com os filtros atuais.")
            else:
                df_exibicao = df_despesas_filtradas.copy()
                df_exibicao['data'] = pd.to_datetime(df_exibicao['data']).dt.strftime('%d/%m/%Y')
                df_exibicao.columns = ['ID', 'Data', 'Descrição', 'Valor (R$)', 'Categoria', 'Tipo', 'Status']
                
                selecao_desp = st.dataframe(
                    df_exibicao, 
                    use_container_width=True, 
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="single-row"
                )
                if selecao_desp and "rows" in selecao_desp["selection"] and selecao_desp["selection"]["rows"]:
                    idx_linha = selecao_desp["selection"]["rows"][0]
                    despesa_clicada_id = int(df_despesas_filtradas.iloc[idx_linha]['id'])

        if despesa_clicada_id is not None:
            with st.container(border=True):
                st.subheader("⚙️ Gerenciar Conta Selecionada")
                _dd = sb_fetch_one("despesas", {"id": despesa_clicada_id})
                dados_d_atual = (_dd["descricao"], _dd["valor"], _dd["status"]) if _dd else None
                
                st.markdown(f"**Item:** {dados_d_atual[0]} | **Valor:** R$ {dados_d_atual[1]:.2f} | **Status:** `{dados_d_atual[2]}`")
                
                chave_senha_desp = f"senha_desp_v_{st.session_state.versao_senha_desp}"
                senha_despesa = st.text_input("🔑 Senha para Autorizar Ações", type="password", key=chave_senha_desp)
                
                b_baixa, b_excluir = st.columns(2)
                with b_baixa:
                    pode_dar_baixa = dados_d_atual[2] == "Pendente / Agendada"
                    if st.button("Confirmar Pagamento (Dar Baixa) 💵", use_container_width=True, type="primary", disabled=not pode_dar_baixa):
                        if senha_despesa == SENHA_MASTER:
                            sb_update("despesas", {"status": "Paga", "data": datetime.today().strftime("%Y-%m-%d")}, "id", despesa_clicada_id)
                            st.success("Conta baixada com sucesso como PAGA!")
                            st.session_state.versao_senha_desp += 1
                            st.rerun()
                        else:
                            st.error("❌ Senha incorreta!")
                            
                with b_excluir:
                    if st.button("Excluir Lançamento ❌", use_container_width=True):
                        if senha_despesa == SENHA_MASTER:
                            sb_delete("despesas", "id", despesa_clicada_id)
                            st.warning("Lançamento de gasto removido do caixa!")
                            st.session_state.versao_senha_desp += 1
                            st.rerun()
                        else:
                            st.error("❌ Senha incorreta!")

# ==========================================
# TELA: FINANCEIRO
# ==========================================
elif menu == "Gráficos & Financeiro":
    st.title("📊 Painel Financeiro")

    # Apenas OS com status 'Entregue' representam receita realizada
    _df_ent = sb_query("ordens_servico", filters={"status": "Entregue"}, select="valor_total")
    total_entradas = float(_df_ent["valor_total"].sum()) if not _df_ent.empty else 0.0
    _df_sai = sb_query("despesas", filters={"status": "Paga"}, select="valor")
    total_saidas = float(_df_sai["valor"].sum()) if not _df_sai.empty else 0.0
    lucro = total_entradas - total_saidas

    # OS ativas que ainda não foram entregues (receita pendente / a receber)
    _df_pend = sb_query("ordens_servico", select="valor_total,status")
    total_pendente_os = float(_df_pend[_df_pend["status"] != "Entregue"]["valor_total"].sum()) if not _df_pend.empty else 0.0

    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💰 Faturamento Realizado", f"R$ {total_entradas:,.2f}", help="Soma das OS com status 'Entregue'")
        c2.metric("⏳ A Receber (OS Ativas)", f"R$ {total_pendente_os:,.2f}", help="OS abertas que ainda não foram entregues")
        c3.metric("💸 Despesas Pagas", f"R$ {total_saidas:,.2f}", delta=f"-R$ {total_saidas:,.2f}", delta_color="inverse")
        c4.metric("📈 Lucro Líquido Real", f"R$ {lucro:,.2f}")
    
    st.divider()
    
    with st.container(border=True):
        st.subheader("💳 Faturamento por Meio de Pagamento (Sinal)")
        _dfms = sb_query("ordens_servico", select="forma_sinal,valor_sinal")
        df_meios_sinal = _dfms.groupby("forma_sinal")["valor_sinal"].sum().reset_index().rename(columns={"forma_sinal":"Meio","valor_sinal":"Total"}) if not _dfms.empty else pd.DataFrame()
        st.dataframe(df_meios_sinal, use_container_width=True, hide_index=True)
    
    with st.container(border=True):
        st.bar_chart(pd.DataFrame({"Tipo": ["Realizadas", "Saídas"], "Valor (R$)": [total_entradas, total_saidas]}).set_index("Tipo"))

    st.divider()

    # ---- BACKUP DO BANCO DE DADOS ----
    with st.container(border=True):
        st.subheader("💾 Backup do Banco de Dados")
        st.caption("Baixe uma cópia de segurança do banco a qualquer momento.")
        if os.path.exists("database_v2.db"):
            with open("database_v2.db", "rb") as f_db:
                st.download_button(
                    label="⬇️ Baixar Backup (database_v2.db)",
                    data=f_db,
                    file_name=f"backup_erp_{datetime.today().strftime('%Y%m%d_%H%M')}.db",
                    mime="application/octet-stream",
                    use_container_width=True
                )

    st.divider()

    # ---- EXPORTAÇÃO PARA EXCEL ----
    with st.container(border=True):
        st.subheader("📊 Exportar Dados para Excel")
        st.caption("Gera um arquivo .xlsx com abas separadas para cada tipo de dado. Útil para análise, contabilidade ou histórico mensal.")

        # Filtro de período para a exportação
        ex_col1, ex_col2 = st.columns(2)
        with ex_col1:
            export_inicio = st.date_input("Período — De:", value=datetime.today().replace(day=1), format="DD/MM/YYYY", key="export_inicio")
        with ex_col2:
            export_fim = st.date_input("Período — Até:", value=datetime.today(), format="DD/MM/YYYY", key="export_fim")

        if st.button("📥 Gerar Excel Completo", type="primary", use_container_width=True):
            import io
            output = io.BytesIO()

            inicio_str = export_inicio.strftime('%Y-%m-%d')
            fim_str    = export_fim.strftime('%Y-%m-%d')
            inicio_br  = export_inicio.strftime('%d/%m/%Y')
            fim_br     = export_fim.strftime('%d/%m/%Y')

            # --- Ordens de Serviço ---
            _exp_os = sb_query("ordens_servico", order="id")
            _exp_cli = sb_query("clientes")
            if not _exp_os.empty and not _exp_cli.empty:
                _exp_os = _exp_os.merge(_exp_cli.rename(columns={"id":"cliente_id","nome":"Cliente","whatsapp":"WhatsApp"}), on="cliente_id", how="left")
                _exp_os["Saldo Restante (R$)"] = _exp_os["valor_total"] - _exp_os["valor_sinal"]
                _exp_os = _exp_os.sort_values("id", ascending=False)
                if inicio_str and fim_str:
                    _exp_os = _exp_os[(_exp_os["horario_pedido"].str[-10:] >= inicio_str) | (_exp_os["horario_pedido"] >= inicio_str)]
                df_os_exp = _exp_os.rename(columns={
                    "id":"Nº OS","servico_nome":"Serviços","detalhes":"Detalhes",
                    "qtd_pecas":"Qtd Peças","prioridade":"Prioridade","atendente_nome":"Atendente",
                    "horario_pedido":"Data/Hora Abertura","prazo_entrega":"Prazo Entrega",
                    "status":"Status","valor_total":"Valor Total (R$)","valor_sinal":"Sinal Pago (R$)",
                    "forma_sinal":"Forma Pagto Sinal","forma_restante":"Forma Pagto Restante"
                })
            else:
                df_os_exp = pd.DataFrame()

            # --- Faturamento por OS Entregue ---
            df_fat_exp = df_os_exp[df_os_exp["Status"] == "Entregue"].copy() if not df_os_exp.empty else pd.DataFrame()

            # --- Clientes ---
            _exp_cli2 = sb_query("clientes", order="nome")
            _exp_os2 = sb_query("ordens_servico", select="cliente_id,valor_total")
            if not _exp_cli2.empty:
                if not _exp_os2.empty:
                    _grp = _exp_os2.groupby("cliente_id").agg(total_os=("valor_total","count"), total_gasto=("valor_total","sum")).reset_index()
                    _exp_cli2 = _exp_cli2.merge(_grp.rename(columns={"cliente_id":"id"}), on="id", how="left")
                    _exp_cli2["total_os"] = _exp_cli2["total_os"].fillna(0).astype(int)
                    _exp_cli2["total_gasto"] = _exp_cli2["total_gasto"].fillna(0)
                df_cli_exp = _exp_cli2.rename(columns={"id":"Código","nome":"Nome","whatsapp":"WhatsApp","total_os":"Total de OS","total_gasto":"Total Gasto (R$)"})
            else:
                df_cli_exp = pd.DataFrame()

            # --- Despesas ---
            _exp_desp = sb_query("despesas", order="data")
            if not _exp_desp.empty:
                _exp_desp = _exp_desp[(_exp_desp["data"] >= inicio_str) & (_exp_desp["data"] <= fim_str)]
                _exp_desp = _exp_desp.sort_values("data", ascending=False)
                _exp_desp["data"] = pd.to_datetime(_exp_desp["data"]).dt.strftime('%d/%m/%Y')
                df_desp_exp = _exp_desp.rename(columns={"id":"ID","data":"Data","descricao":"Descrição","valor":"Valor (R$)","category":"Categoria","tipo":"Tipo","status":"Status"})
            else:
                df_desp_exp = pd.DataFrame()

            # --- Catálogo de Serviços ---
            df_serv_exp = sb_query("servicos", order="nome").rename(columns={"nome":"Serviço","preco":"Preço Base (R$)"})

            # --- Resumo Financeiro ---
            total_fat   = float(df_fat_exp["Valor Total (R$)"].sum()) if not df_fat_exp.empty else 0.0
            total_desp  = float(df_desp_exp[df_desp_exp["Status"] == "Paga"]["Valor (R$)"].sum()) if not df_desp_exp.empty else 0.0
            df_resumo = pd.DataFrame({
                "Item": [
                    "Faturamento Realizado (OS Entregues)",
                    "Despesas Pagas",
                    "Lucro Líquido",
                    "Período"
                ],
                "Valor": [
                    f"R$ {total_fat:,.2f}",
                    f"R$ {total_desp:,.2f}",
                    f"R$ {(total_fat - total_desp):,.2f}",
                    f"{inicio_br} a {fim_br}"
                ]
            })

            # --- Grava no Excel com múltiplas abas ---
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df_resumo.to_excel(writer,   sheet_name="Resumo Financeiro",  index=False)
                df_os_exp.to_excel(writer,   sheet_name="Ordens de Serviço",  index=False)
                df_fat_exp.to_excel(writer,  sheet_name="Faturamento",        index=False)
                df_cli_exp.to_excel(writer,  sheet_name="Clientes",           index=False)
                df_desp_exp.to_excel(writer, sheet_name="Despesas",           index=False)
                df_serv_exp.to_excel(writer, sheet_name="Catálogo Serviços",  index=False)

            output.seek(0)
            nome_arquivo = f"erp_silviacastro_{export_inicio.strftime('%d%m%Y')}_a_{export_fim.strftime('%d%m%Y')}.xlsx"

            st.download_button(
                label="⬇️ Baixar Excel Gerado",
                data=output,
                file_name=nome_arquivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.success(f"✅ Excel gerado com sucesso! Período: {inicio_br} a {fim_br}")

# ==========================================
# TELA 8: FUNCIONÁRIOS
# ==========================================
elif menu == "Funcionários":
    st.title("👤 Funcionários")
    st.caption("Cadastre aqui os nomes dos atendentes. Eles aparecerão na seleção ao abrir uma nova OS e na via da empresa do cupom.")

    # --- Cadastro ---
    with st.container(border=True):
        st.subheader("➕ Cadastrar Novo Funcionário")
        novo_func = st.text_input("Nome completo do funcionário", placeholder="Ex: Silvia Castro")
        if st.button("💾 Cadastrar", type="primary", use_container_width=True):
            if not novo_func.strip():
                st.error("❌ Digite o nome do funcionário.")
            else:
                _ef = sb_query("funcionarios", filters={"nome": novo_func.strip()})
                existente = _ef.iloc[0]["id"] if not _ef.empty else None
                if existente:
                    st.warning(f"⚠️ '{novo_func.strip()}' já está cadastrado.")
                else:
                    sb_insert("funcionarios", {"nome": novo_func.strip()})
                    st.success(f"✅ '{novo_func.strip()}' cadastrado com sucesso!")
                    st.rerun()

    # --- Lista ---
    _fdf = sb_query("funcionarios", order="nome")
    funcionarios_db = list(zip(_fdf["id"].tolist(), _fdf["nome"].tolist())) if not _fdf.empty else []

    if not funcionarios_db:
        st.info("Nenhum funcionário cadastrado ainda.")
    else:
        with st.container(border=True):
            st.subheader(f"📋 Funcionários Cadastrados ({len(funcionarios_db)})")
            for func_id, func_nome in funcionarios_db:
                col_nome, col_btn = st.columns([5, 1])
                with col_nome:
                    st.markdown(f"👤 **{func_nome}**")
                with col_btn:
                    if st.button("🗑️ Remover", key=f"del_func_{func_id}"):
                        sb_delete("funcionarios", "id", func_id)
                        st.success(f"'{func_nome}' removido.")
                        st.rerun()

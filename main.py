import streamlit as st
import pandas as pd
import sqlite3
import urllib.parse
import os
from datetime import datetime

# ==========================================
# 0. CONFIGURAÇÃO VISUAL DA PÁGINA (BRANDING)
# ==========================================
FAVICON = "logo_silvia.png" if os.path.exists("logo_silvia.png") else "🧵"

st.set_page_config(
    page_title="ERP Silvia Castro - Conserto de Roupas", 
    page_icon=FAVICON, 
    layout="wide"
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
    }
    
    .block-container {
        padding-top: 115px !important; 
    }
    
    /* Fundo geral da aplicação */
    .stApp {
        background-color: var(--main-bg);
    }
    /* CABEÇALHO FIXO SUPERIOR SUPER PREMIUM */
    .custom-top-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px; /* Aumentado ligeiramente para acomodar o CNPJ */
        background-color: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(8px); /* Efeito moderno de vidro fosco */
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 40px;
        border-bottom: 1px solid rgba(0,0,0,0.06);
    }
    
    .header-brand {
        display: flex;
        flex-direction: column; /* Coloca o CNPJ embaixo do título */
        justify-content: center;
    }
    
    .header-title {
        font-family: 'Garamond', 'Times New Roman', Times, serif !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #1A1A1A !important; /* Cor cinza escuro nobre */
        margin: 0 !important;
        line-height: 1.2 !important;
        letter-spacing: 0.5px;
    }

    .header-cnpj {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        color: #7A7A7A !important; /* Cor mais suave para o CNPJ */
        margin-top: 3px !important;
        letter-spacing: 1px;
    }
    
    .header-status {
        background-color: #e6f4ea;
        color: #137333;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif !important;
    }

    /* Força uma estilização elegante nos containers nativos com borda */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid rgba(0,0,0,0.06) !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02) !important;
    }
    
    /* Customizando a Barra Lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid rgba(0,0,0,0.05);
        padding-top: 20px;
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
    h1, h2, h3 {
        color: #2b2b2b !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: 700 !important;
    }
    
    /* Inputs arredondados */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Renderização estruturada do novo topo fixo da aplicação com CNPJ
st.markdown(f"""
<div class="custom-top-header">
    <div class="header-brand">
        <span class="header-title">ERP | Silvia Castro Conserto de Roupas</span>
        <span class="header-cnpj">CNPJ: 36.329.114/0001-27</span>
    </div>
    <div class="header-status">
        🟢 Sistema Online
    </div>
</div>
""", unsafe_allow_html=True)

# SENHA DO SISTEMA
SENHA_MASTER = "1234"

# DADOS DA EMPRESA (Para o Cupom)
NOME_LOJA = "Silvia Castro Conserto de Roupas"
CNPJ_LOJA = "36.329.114/0001-27"
ENDERECO_LOJA = "Rua Conego Almeida, 85 - Centro, Taubate - SP, 12.080-260"
TELEFONE_LOJA = "12 99683-1392"

# ==========================================
# 1. CONEXÃO COM O BANCO DE DADOS
# ==========================================
conn = sqlite3.connect("database_v2.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS servicos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, preco REAL NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, whatsapp TEXT NOT NULL)")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ordens_servico (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    cliente_id INTEGER NOT NULL, 
    servico_nome TEXT NOT NULL,
    detalhes TEXT, 
    valor_total REAL NOT NULL, 
    valor_sinal REAL NOT NULL, 
    prazo_entrega TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'A Iniciar', 
    horario_pedido TEXT, 
    qtd_pecas INTEGER DEFAULT 1, 
    prioridade TEXT DEFAULT 'Normal',
    forma_sinal TEXT DEFAULT 'Não se aplica',
    forma_restante TEXT DEFAULT 'Pendente',
    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
)
""")
cursor.execute("CREATE TABLE IF NOT EXISTS despesas (id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT NOT NULL, valor REAL NOT NULL, data TEXT NOT NULL, category TEXT NOT NULL)")
conn.commit()

try:
    cursor.execute("ALTER TABLE ordens_servico ADD COLUMN forma_sinal TEXT DEFAULT 'Não se aplica'")
    cursor.execute("ALTER TABLE ordens_servico ADD COLUMN forma_restante TEXT DEFAULT 'Pendente'")
    conn.commit()
except:
    pass

if "versao_senha_os" not in st.session_state:
    st.session_state.versao_senha_os = 0
if "versao_senha_cli" not in st.session_state:
    st.session_state.versao_senha_cli = 0
if "cupom_pronto" not in st.session_state:
    st.session_state.cupom_pronto = None
if "versao_nova_os" not in st.session_state:
    st.session_state.versao_nova_os = 0

# ==========================================
# 2. MENU LATERAL DE NAVEGAÇÃO
# ==========================================
if LOGO_PATH:
    st.sidebar.image(LOGO_PATH, width=200)
else:
    st.sidebar.title("🧵 Ateliê ERP")
    
st.sidebar.write("---")
menu = st.sidebar.radio("Ir para:", [
    "➕ Nova OS", 
    "🔍 Consultar / Editar OS", 
    "👥 Clientes", 
    "📋 Painel de Trabalho (Kanban)", 
    "🏷️ Catálogo de Serviços", 
    "💸 Registrar Despesa", 
    "📊 Gráficos & Financeiro"
])

# ==========================================
# TELA 1: NOVA OS
# ==========================================
if menu == "➕ Nova OS":
    st.title("➕ Abertura de Nova Ordem de Serviço")
    
    ultimo_id = cursor.execute("SELECT MAX(id) FROM ordens_servico").fetchone()[0]
    proxima_os = (ultimo_id + 1) if ultimo_id is not None else 1
    
    st.info(f"📋 **Você está preenchendo a Ordem de Serviço Nº: #{proxima_os}**")
    
    clientes_df = pd.read_sql_query("SELECT id, nome, whatsapp FROM clientes ORDER BY nome ASC", conn)
    servicos_df = pd.read_sql_query("SELECT nome, preco FROM servicos ORDER BY nome ASC", conn)

    v = st.session_state.versao_nova_os

    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.subheader("📋 Dados do Atendimento")
            cliente_novo = st.checkbox("👤 Cliente Novo / Não Cadastrado?", key=f"cli_novo_chk_{v}")
            
            if cliente_novo:
                nome_novo = st.text_input("Nome da Nova Cliente", value="", key=f"nome_novo_{v}")
                whatsapp_novo = st.text_input("WhatsApp (com DDD, ex: 12996831392)", value="", key=f"whats_novo_{v}")
                cliente_id = None
                nome_final_cupom = nome_novo
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
            prioridade = st.selectbox("Prioridade para a Produção", ["Normal", "Alta 🚨"], key=f"prio_{v}")
            detalhes = st.text_area("Detalhes / Observações do Ajuste", value="", key=f"detalhes_{v}")

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
        if cliente_novo and (not nome_novo or not whatsapp_novo):
            st.error("❌ Por favor, preencha o Nome e o WhatsApp da nova cliente.")
        elif not cliente_novo and cliente_id is None:
            st.error("❌ Selecione uma cliente cadastrada ou marque a caixinha de Cliente Novo.")
        elif not servicos_selecionados:
            st.error("❌ Por favor, selecione pelo menos um serviço.")
        elif not data_entrega:
            st.error("❌ Por favor, selecione a Data de Entrega.")
        else:
            pode_salvar = True
            if cliente_novo:
                checar = cursor.execute("SELECT id FROM clientes WHERE nome = ?", (nome_novo.strip(),)).fetchone()
                if checar:
                    st.error(f"⚠️ A cliente já está cadastrada no sistema!")
                    pode_salvar = False
                else:
                    cursor.execute("INSERT INTO clientes (nome, whatsapp) VALUES (?, ?)", (nome_novo.strip(), whatsapp_novo.strip()))
                    conn.commit()
                    cliente_id = cursor.lastrowid
                    nome_final_cupom = nome_novo.strip()
                    whats_final_whatsapp = whatsapp_novo.strip()
            
            if pode_salvar:
                texto_servicos_db = ", ".join(servicos_selecionados_dados)
                
                cursor.execute("""
                    INSERT INTO ordens_servico (cliente_id, servico_nome, detalhes, valor_total, valor_sinal, prazo_entrega, horario_pedido, qtd_pecas, prioridade, forma_sinal, forma_restante)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (cliente_id, texto_servicos_db, detalhes, valor_final, valor_sinal, prazo_formatated, horario_pedido_formatado, total_pecas_os, prioridade, forma_sinal, forma_restante))
                conn.commit()
                os_id = cursor.lastrowid
                
                resta_pagar = valor_final - valor_sinal
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
RESTA PAGAR: R$ {resta_pagar:,.2f} ({forma_restante})
=========================================
     Obrigado pela preferência!          
=========================================


- - - - - - - - CORTE AQUI - - - - - - - -


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
RESTA PAGAR: R$ {resta_pagar:,.2f} ({forma_restante})
-----------------------------------------
➡️ DATA DE ENTREGA: {prazo_formatated}
⚠️ PRIORIDADE: {prioridade.upper()}
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
            
            html_impressao = f"""
            <script>
            function imprimirCupom() {{
                var receita = `{st.session_state.cupom_pronto}`;
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
# TELA: CONSULTAR / EDITAR OS (COM REABERTURA)
# ==========================================
elif menu == "🔍 Consultar / Editar OS":
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

    with aba_ativas:
        try:
            query_ativas = f"""
                SELECT os.id as 'Nº OS', c.nome as 'Cliente', os.prioridade as '🚨 Prioridade', os.qtd_pecas as 'Total Peças', os.servico_nome as 'Serviços (Qtd)', 
                       os.valor_total as 'Total (R$)', os.horario_pedido as 'Abertura/Hora', os.prazo_entrega as 'Data Entrega', os.status as 'Status'
                FROM ordens_servico os JOIN clientes c ON os.cliente_id = c.id
                WHERE os.status != 'Entregue' {clausula_busca}
                ORDER BY os.id DESC
            """
            df_ativas = pd.read_sql_query(query_ativas, conn, params=parametros_busca)
            if df_ativas.empty:
                st.info("Nenhuma Ordem de Serviço ativa encontrada.")
            else:
                st.dataframe(df_ativas, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Erro ao buscar OS Ativas: {e}")

    with aba_entregues:
        try:
            query_entregues = f"""
                SELECT os.id as 'Nº OS', c.nome as 'Cliente', os.qtd_pecas as 'Total Peças', os.servico_nome as 'Serviços (Qtd)', 
                       os.valor_total as 'Total (R$)', os.horario_pedido as 'Abertura/Hora', os.prazo_entrega as 'Data Entrega', os.status as 'Status'
                FROM ordens_servico os JOIN clientes c ON os.cliente_id = c.id
                WHERE os.status = 'Entregue' {clausula_busca}
                ORDER BY os.id DESC
            """
            df_entregues = pd.read_sql_query(query_entregues, conn, params=parametros_busca)
            if df_entregues.empty:
                st.info("Nenhuma Ordem de Serviço entregue encontrada.")
            else:
                st.dataframe(df_entregues, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Erro ao buscar Histórico: {e}")
        
    st.divider()
    with st.container(border=True):
        st.subheader("📝 Modificar, Reabrir ou Cancelar uma OS")
        try:
            df_todas_edicao = pd.read_sql_query("""
                SELECT os.id as 'Nº OS', c.nome as 'Cliente', os.servico_nome as 'Serviços'
                FROM ordens_servico os JOIN clientes c ON os.cliente_id = c.id
                ORDER BY os.id DESC
            """, conn)
        except:
            df_todas_edicao = pd.DataFrame()
        
        if df_todas_edicao.empty:
            st.caption("Nenhuma Ordem de Serviço disponível para alteração.")
        else:
            opcoes_os = {f"OS #{row['Nº OS']} - {row['Cliente']} ({row['Serviços']})": row['Nº OS'] for _, row in df_todas_edicao.iterrows()}
            os_selecionada = st.selectbox("Selecione a OS que deseja alterar ou reabrir", list(opcoes_os.keys()))
            id_os = opcoes_os[os_selecionada]
            
            dados_os = cursor.execute("SELECT detalhes, valor_total, valor_sinal, prazo_entrega, status, horario_pedido, forma_sinal, forma_restante FROM ordens_servico WHERE id = ?", (id_os,)).fetchone()
            
            c1, c2, c3 = st.columns(3)
            with c1:
                novo_detalhe = st.text_area("Alterar Detalhes/Observações", value=dados_os[0] if dados_os[0] else "")
                lista_status = ["A Iniciar", "Em Andamento", "Finalizado", "Avisado", "Entregue"]
                novo_status = st.selectbox("Alterar Status da OS (Mude para 'A Iniciar' ou 'Em Andamento' para reabrir)", lista_status, index=lista_status.index(dados_os[4]) if dados_os[4] in lista_status else 0)
            with c2:
                novo_total = st.number_input("Alterar Valor Total (R$)", min_value=0.0, value=float(dados_os[1]), format="%.2f")
                novo_sinal = st.number_input("Alterar Sinal (R$)", min_value=0.0, value=float(dados_os[2]), format="%.2f")
                lista_pagamentos = ["Não se aplica", "Pix", "Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pendente (Paga na retirada)"]
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
                        cursor.execute("""
                            UPDATE ordens_servico 
                            SET detalhes = ?, valor_total = ?, valor_sinal = ?, prazo_entrega = ?, status = ?, horario_pedido = ?, forma_sinal = ?, forma_restante = ?
                            WHERE id = ?
                        """, (novo_detalhe, novo_total, novo_sinal, novo_prazo, novo_status, novo_hora_ped, novo_forma_sinal, novo_forma_restante, id_os))
                        conn.commit()
                        st.success(f"OS #{id_os} atualizada com sucesso no sistema!")
                        st.session_state.versao_senha_os += 1
                        st.rerun()
                    else:
                        st.error("❌ Senha incorreta!")
            with col_b2:
                if st.button("Excluir / Cancelar OS ❌", use_container_width=True):
                    if senha_digitada == SENHA_MASTER:
                        cursor.execute("DELETE FROM ordens_servico WHERE id = ?", (id_os,))
                        conn.commit()
                        st.warning(f"OS #{id_os} apagada!")
                        st.session_state.versao_senha_os += 1
                        st.rerun()
                    else:
                        st.error("❌ Senha incorreta!")

# ==========================================
# TELA: CLIENTES (COM HISTÓRICO DE SERVIÇOS)
# ==========================================
elif menu == "👥 Clientes":
    st.title("👥 Gestão de Clientes")
    col_cadastro, col_lista = st.columns([1, 1.5])
    with col_cadastro:
        with st.container(border=True):
            st.subheader("➕ Novo Cadastro")
            nome_cliente = st.text_input("Nome Completo", key="cad_nome")
            whatsapp_cliente = st.text_input("WhatsApp (Apenas números com DDD)", key="cad_whats")
            if st.button("Salvar Cliente", type="primary", use_container_width=True):
                if nome_cliente and whatsapp_cliente:
                    checar = cursor.execute("SELECT id FROM clientes WHERE nome = ?", (nome_cliente.strip(),)).fetchone()
                    if checar:
                        st.error("⚠️ Este nome de cliente já está cadastrado!")
                    else:
                        cursor.execute("INSERT INTO clientes (nome, whatsapp) VALUES (?, ?)", (nome_cliente.strip(), whatsapp_cliente.strip()))
                        conn.commit()
                        st.success("Cliente salva com sucesso!")
                        st.rerun()
                else:
                    st.error("Por favor, preencha todos os campos.")

        with st.container(border=True):
            st.subheader("📝 Gerenciar & Histórico")
            clientes_lista = pd.read_sql_query("SELECT id, nome FROM clientes ORDER BY nome ASC", conn)
            if not clientes_lista.empty:
                dict_clientes = {row['nome']: row['id'] for _, row in clientes_lista.iterrows()}
                cliente_gerenciar = st.selectbox("Selecione o Cliente para Ver Histórico/Editar", list(dict_clientes.keys()))
                id_gerenciar = dict_clientes[cliente_gerenciar]
                dados_atuais = cursor.execute("SELECT nome, whatsapp FROM clientes WHERE id = ?", (id_gerenciar,)).fetchone()
                
                # Exibição do Histórico do cliente selecionado antes dos inputs de edição
                st.markdown(f"📊 **Histórico de Serviços de {dados_atuais[0]}:**")
                try:
                    df_historico_cli = pd.read_sql_query("""
                        SELECT id as 'Nº OS', servico_nome as 'Serviços', valor_total as 'Valor (R$)', prazo_entrega as 'Entrega', status as 'Status'
                        FROM ordens_servico 
                        WHERE cliente_id = ? 
                        ORDER BY id DESC
                    """, conn, params=(id_gerenciar,))
                    
                    if df_historico_cli.empty:
                        st.caption("Nenhum serviço registrado para este cliente.")
                    else:
                        st.dataframe(df_historico_cli, use_container_width=True, hide_index=True)
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
                            cursor.execute("UPDATE clientes SET nome = ?, whatsapp = ? WHERE id = ?", (novo_nome.strip(), novo_whats.strip(), id_gerenciar))
                            conn.commit()
                            st.success("Cadastro atualizado!")
                            st.session_state.versao_senha_cli += 1
                            st.rerun()
                        else:
                            st.error("❌ Senha incorreta!")
                with c_del:
                    if st.button("Excluir Cliente ❌", type="secondary", use_container_width=True):
                        if senha_cliente == SENHA_MASTER:
                            cursor.execute("DELETE FROM clientes WHERE id = ?", (id_gerenciar,))
                            cursor.execute("DELETE FROM ordens_servico WHERE cliente_id = ?", (id_gerenciar,))
                            conn.commit()
                            st.warning("Cliente e suas OS foram excluídos!")
                            st.session_state.versao_senha_cli += 1
                            st.rerun()
                        else:
                            st.error("❌ Senha incorreta!")
            else:
                st.caption("Nenhum cliente cadastrado.")

    with col_lista:
        with st.container(border=True):
            st.subheader("🔍 Lista Geral de Clientes")
            busca = st.text_input("Buscar cliente por nome...")
            if busca:
                dados_clientes = pd.read_sql_query("SELECT id as 'Código', nome as 'Nome', whatsapp as 'WhatsApp' FROM clientes WHERE nome LIKE ? ORDER BY nome ASC", conn, params=(f"%{busca}%",))
            else:
                dados_clientes = pd.read_sql_query("SELECT id as 'Código', nome as 'Nome', whatsapp as 'WhatsApp' FROM clientes ORDER BY nome ASC", conn)
            st.dataframe(dados_clientes, use_container_width=True, hide_index=True)

# ==========================================
# TELA: KANBAN
# ==========================================
elif menu == "📋 Painel de Trabalho (Kanban)":
    st.title("📋 Painel de Trabalho da Oficina")
    try:
        df_os = pd.read_sql_query("""
            SELECT os.id, c.nome as cliente, c.whatsapp, os.servico_nome, os.prazo_entrega, os.status, os.qtd_pecas, os.prioridade, os.horario_pedido 
            FROM ordens_servico os JOIN clientes c ON os.cliente_id = c.id 
            WHERE os.status != 'Entregue'
        """, conn)
    except:
        df_os = pd.DataFrame()
        
    col_iniciar, col_andamento, col_pronto, col_avisado = st.columns(4)
    with col_iniciar:
        st.markdown("### 📥 A Iniciar")
        if not df_os.empty:
            for idx, os in df_os[df_os['status'] == 'A Iniciar'].iterrows():
                with st.container(border=True):
                    if os['prioridade'] == "Alta 🚨":
                        st.markdown("<span style='color:red; font-weight:bold;'>🚨 URGENTE</span>", unsafe_allow_html=True)
                    st.markdown(f"**OS #{os['id']} - {os['cliente']}**")
                    st.markdown(f"🧵 {os['servico_nome']}")
                    st.markdown(f"<small>⏱️ Aberta: {os['horario_pedido']}<br>📅 Limite: {os['prazo_entrega']}</small>", unsafe_allow_html=True)
                    if st.button("Começar 🪡", key=f"ini_{os['id']}", use_container_width=True):
                        cursor.execute("UPDATE ordens_servico SET status = 'Em Andamento' WHERE id = ?", (os['id'],))
                        conn.commit()
                        st.rerun()
                        
    with col_andamento:
        st.markdown("### 🪡 Em Andamento")
        if not df_os.empty:
            for idx, os in df_os[df_os['status'] == 'Em Andamento'].iterrows():
                with st.container(border=True):
                    if os['prioridade'] == "Alta 🚨":
                        st.markdown("<span style='color:red; font-weight:bold;'>🚨 URGENTE</span>", unsafe_allow_html=True)
                    st.markdown(f"**OS #{os['id']} - {os['cliente']}**")
                    st.markdown(f"🧵 {os['servico_nome']}")
                    st.markdown(f"<small>⏱️ Aberta: {os['horario_pedido']}<br>📅 Limite: {os['prazo_entrega']}</small>", unsafe_allow_html=True)
                    if st.button("Pronto ✅", key=f"and_{os['id']}", use_container_width=True):
                        cursor.execute("UPDATE ordens_servico SET status = 'Finalizado' WHERE id = ?", (os['id'],))
                        conn.commit()
                        st.rerun()
                         
    with col_pronto:
        st.markdown("### ✅ Pronto")
        if not df_os.empty:
            for idx, os in df_os[df_os['status'] == 'Finalizado'].iterrows():
                with st.container(border=True):
                    if os['prioridade'] == "Alta 🚨":
                        st.markdown("<span style='color:red; font-weight:bold;'>🚨 URGENTE</span>", unsafe_allow_html=True)
                    st.markdown(f"**OS #{os['id']} - {os['cliente']}**")
                    st.markdown(f"🧵 {os['servico_nome']}")
                    
                    msg = f"Olá {os['cliente']}! Passando para avisar que sua peça ({os['servico_nome']}) já está prontinha te esperando aqui no Ateliê Silvia Castro! 🧵✨"
                    msg_url = urllib.parse.quote(msg)
                    link_whats = f"https://wa.me/55{os['whatsapp']}?text={msg_url}"
                    
                    html_botao_whats = f"""
                    <a href="{link_whats}" target="_blank" style="text-decoration: none;">
                        <button style="
                            width: 100%;
                            background-color: #25D366;
                            color: white;
                            border: none;
                            padding: 10px;
                            border-radius: 8px;
                            font-weight: bold;
                            cursor: pointer;
                            font-size: 14px;
                            margin-bottom: 8px;
                            text-align: center;
                        ">Enviar Mensagem 💬</button>
                    </a>
                    """
                    st.components.v1.html(html_botao_whats, height=45)
                    if st.button("Mover p/ Avisados 📱", key=f"avi_{os['id']}", use_container_width=True, type="primary"):
                        cursor.execute("UPDATE ordens_servico SET status = 'Avisado' WHERE id = ?", (os['id'],))
                        conn.commit()
                        st.rerun()
                        
    with col_avisado:
        st.markdown("### 📱 Avisados")
        if not df_os.empty:
            for idx, os in df_os[df_os['status'] == 'Avisado'].iterrows():
                with st.container(border=True):
                    if os['prioridade'] == "Alta 🚨":
                        st.markdown("<span style='color:red; font-weight:bold;'>🚨 URGENTE</span>", unsafe_allow_html=True)
                    st.markdown(f"**OS #{os['id']} - {os['cliente']}**")
                    st.markdown(f"🧵 {os['servico_nome']}")
                    st.markdown(f"<small>⏱️ Aberta: {os['horario_pedido']}</small>", unsafe_allow_html=True)
                    if st.button("Entregue 📦", key=f"fim_{os['id']}", use_container_width=True, type="primary"):
                        cursor.execute("UPDATE ordens_servico SET status = 'Entregue' WHERE id = ?", (os['id'],))
                        conn.commit()
                        st.rerun()

# ==========================================
# TELA: CATÁLOGO DE SERVIÇOS
# ==========================================
elif menu == "🏷️ Catálogo de Serviços":
    st.title("🏷️ Catálogo de Serviços & Preços")
    col_cad, col_tab = st.columns([1, 2])
    with col_cad:
        with st.container(border=True):
            st.subheader("➕ Novo Serviço")
            novo_servico = st.text_input("Nome do Serviço")
            novo_preco = st.number_input("Preço Sugerido (R$)", min_value=0.0, format="%.2f")
            if st.button("Adicionar", type="primary", use_container_width=True):
                if novo_servico:
                    cursor.execute("INSERT INTO servicos (nome, preco) VALUES (?, ?)", (novo_servico, novo_preco))
                    conn.commit()
                    st.success("Adicionado!")
                    st.rerun()
    with col_tab:
        with st.container(border=True):
            st.subheader("Serviços Ativos")
            st.table(pd.read_sql_query("SELECT nome as 'Serviço', preco as 'Preço Base (R$)' FROM servicos", conn))

# ==========================================
# TELA: DESPESAS
# ==========================================
elif menu == "💸 Registrar Despesa":
    st.title("💸 Controle de Gastos")
    col_cad, col_hist = st.columns([1, 2])
    with col_cad:
        with st.container(border=True):
            st.subheader("➕ Lançar Despesa")
            desc = st.text_input("Descrição")
            val = st.number_input("Valor", min_value=0.0, format="%.2f")
            cat = st.selectbox("Categoria", ["Insumos", "Infraestrutura", "Manutenção", "Aluguel", "Outros"])
            if st.button("Salvar", type="primary", use_container_width=True):
                if desc and val > 0:
                    cursor.execute("INSERT INTO despesas (descricao, valor, data, category) VALUES (?, ?, ?, ?)", (desc, val, datetime.today().strftime('%Y-%m-%d'), cat))
                    conn.commit()
                    st.success("Registrado!")
                    st.rerun()
    with col_hist:
        with st.container(border=True):
            st.subheader("📝 Últimos Gastos")
            st.dataframe(pd.read_sql_query("SELECT data as 'Data', descricao as 'Descrição', valor as 'Valor' FROM despesas ORDER BY id DESC", conn), use_container_width=True, hide_index=True)

# ==========================================
# TELA: FINANCEIRO
# ==========================================
elif menu == "📊 Gráficos & Financeiro":
    st.title("📊 Painel Financeiro")
    total_entradas = float(pd.read_sql_query("SELECT SUM(valor_total) as total FROM ordens_servico", conn)['total'].fillna(0).values[0])
    total_saidas = float(pd.read_sql_query("SELECT SUM(valor) as total FROM despesas", conn)['total'].fillna(0).values[0])
    lucro = total_entradas - total_saidas
    
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento Bruto", f"R$ {total_entradas:,.2f}")
        c2.metric("Despesas Totais", f"R$ {total_saidas:,.2f}", delta=f"-R$ {total_saidas:,.2f}", delta_color="inverse")
        c3.metric("Lucro Líquido Real", f"R$ {lucro:,.2f}")
    
    st.divider()
    
    with st.container(border=True):
        st.subheader("💳 Faturamento por Meio de Pagamento")
        df_meios_sinal = pd.read_sql_query("SELECT forma_sinal as Meio, SUM(valor_sinal) as Total FROM ordens_servico GROUP BY forma_sinal", conn)
        st.dataframe(df_meios_sinal, use_container_width=True, hide_index=True)
    
    with st.container(border=True):
        st.bar_chart(pd.DataFrame({"Tipo": ["Entradas", "Saídas"], "Valor (R$)": [total_entradas, total_saidas]}).set_index("Tipo"))
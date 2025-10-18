# ==========================================================
# 💎 SmartFin AI Blockchain v2
# ==========================================================
# Autor: Claudio Yoshida
# Descrição: Sistema antifraude financeiro com IA + Blockchain (Proof of Work)
# ==========================================================

import streamlit as st
from ai_fraud import treinar_modelo, analisar_transacao
from blockchain import Blockchain
import os
import json
import requests
import threading
import pandas as pd
import altair as alt

# ==========================================================
# 🔄 PING AUTOMÁTICO PARA ACORDAR O BACKEND
# ==========================================================
def ping_backend():
    url = "https://smartfin-backend.onrender.com/"
    try:
        requests.get(url, timeout=5)
        print("🔄 Backend acordado com sucesso!")
    except Exception as e:
        print("⚠️ Erro ao pingar backend:", e)

# Executa o ping em segundo plano (não trava o app)
threading.Thread(target=ping_backend, daemon=True).start()

# ==========================================================
# ⚙️ CONFIGURAÇÕES INICIAIS
# ==========================================================
st.set_page_config(
    page_title="SmartFin AI Blockchain v2",
    layout="wide",
    page_icon="💰"
)

st.title("💰 SmartFin AI Blockchain v2 — IA + Blockchain Antifraude")
st.markdown("""
Este sistema demonstra como **IA e Blockchain** podem trabalhar juntas para criar um ambiente
**financeiro mais seguro, transparente e auditável**.
""")

# ==========================================================
# 🧩 VERIFICAÇÃO AUTOMÁTICA DE ARQUIVOS
# ==========================================================
os.makedirs("data", exist_ok=True)

# Cria arquivo JSON inicial se não existir
if not os.path.exists("data/chain.json"):
    with open("data/chain.json", "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

# Cria CSV inicial se não existir
if not os.path.exists("data/transactions.csv"):
    with open("data/transactions.csv", "w", encoding="utf-8") as f:
        f.write("valor,pais_origem,pais_destino,hora,historico,risco\n")
        f.write("1500,Brasil,EUA,14,bom,baixo\n")
        f.write("3200,EUA,Brasil,22,medio,medio\n")
        f.write("7000,China,Nigéria,3,ruim,alto\n")
        f.write("2500,Alemanha,Brasil,11,bom,baixo\n")
        f.write("10000,Brasil,China,18,ruim,alto\n")

# ==========================================================
# 🚀 INICIALIZAÇÃO
# ==========================================================
if "modelo" not in st.session_state:
    st.session_state.modelo, st.session_state.encoders = treinar_modelo()

if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain(dificuldade=4)

# ==========================================================
# 🧾 FORMULÁRIO DE TRANSAÇÃO
# ==========================================================
st.header("📤 Analisar nova transação")

col1, col2 = st.columns(2)

with col1:
    valor = st.number_input("💸 Valor da transação (R$)", min_value=10, max_value=10000, value=1500)
    hora = st.slider("🕓 Horário da transação", 0, 23, 14)
    historico = st.selectbox("📈 Histórico do cliente", ["bom", "medio", "ruim"])

with col2:
    pais_origem = st.selectbox("🌍 País de origem", ["Brasil", "EUA", "China", "Nigéria", "Alemanha"])
    pais_destino = st.selectbox("🌎 País de destino", ["Brasil", "EUA", "China", "Nigéria", "Alemanha"])

if st.button("🔍 Analisar risco com IA"):
    resultado = analisar_transacao(
        st.session_state.modelo,
        st.session_state.encoders,
        valor, pais_origem, pais_destino, hora, historico
    )
    st.session_state.resultado = resultado
    st.success(f"Resultado: {resultado}")

# ==========================================================
# ⛓️ REGISTRO NA BLOCKCHAIN
# ==========================================================
st.header("🔒 Registrar transação na Blockchain")

if "resultado" in st.session_state:
    if st.button("💾 Registrar na Blockchain"):
        transacao = f"{pais_origem} → {pais_destino} | R${valor} | {historico}"
        risco = st.session_state.resultado
        st.session_state.blockchain.adicionar_bloco(transacao, risco)
        st.session_state.blockchain.salvar_em_json("data/chain.json")
        st.success("✅ Transação registrada com sucesso na blockchain!")

# ==========================================================
# 📜 VISUALIZAR BLOCKCHAIN
# ==========================================================
st.header("📜 Cadeia de Blocos (Blockchain)")

if os.path.exists("data/chain.json"):
    with open("data/chain.json", "r", encoding="utf-8") as f:
        chain_data = json.load(f)
        for bloco in chain_data:
            cor = "🟢" if "segura" in bloco["risco"].lower() else ("🟡" if "médio" in bloco["risco"].lower() else "🔴")
            st.markdown(f"""
            **{cor} Bloco {bloco['index']}**
            - 🧩 **Hash:** `{bloco['hash'][:25]}...`
            - 🔗 **Anterior:** `{bloco['hash_anterior'][:25]}...`
            - 💸 **Transação:** {bloco['transacao']}
            - 🧠 **Risco:** {bloco['risco']}
            - ⏱️ **Timestamp:** {bloco['timestamp']}
            """)
else:
    st.info("Nenhum bloco registrado ainda. Faça uma análise e registre a primeira transação!")

# ==========================================================
# 🧮 VERIFICAR INTEGRIDADE
# ==========================================================
st.header("🧮 Verificação de integridade da Blockchain")

if st.button("🔍 Verificar integridade"):
    ok = st.session_state.blockchain.verificar_integridade()
    if ok:
        st.success("✅ Blockchain íntegra e sem alterações detectadas.")
    else:
        st.error("⚠️ Blockchain alterada ou corrompida!")

# ==========================================================
# 🔍 TESTE ÚNICO DO BACKEND (com tratamento robusto)
# ==========================================================
st.header("🧠 Teste de Conexão com Backend (FastAPI)")

if st.button("🔍 Testar API Backend", key="backend_teste"):
    url = "https://smartfin-backend.onrender.com/analisar"
    data = {
        "valor": 3500,
        "pais_origem": "Brasil",
        "pais_destino": "EUA",
        "hora": 14,
        "historico": "medio"
    }

    with st.spinner("🔄 Enviando dados para o backend... Aguarde um momento."):
        try:
            resp = requests.post(url, json=data, timeout=10)
            st.write(f"📡 Código de resposta: {resp.status_code}")

            if resp.status_code == 200:
                try:
                    resultado = resp.json()
                    st.success("✅ Backend respondeu com sucesso:")
                    st.json(resultado)
                except ValueError:
                    st.warning("⚠️ O backend respondeu, mas o conteúdo não é JSON válido.")
                    st.text(resp.text[:500])
            else:
                st.error(f"❌ Erro HTTP {resp.status_code}")
                st.text(resp.text[:500])

        except requests.exceptions.ConnectionError:
            st.error("🚫 Não foi possível conectar ao backend (servidor offline ou hibernando).")
            st.info("💤 O Render gratuito hiberna após 15 minutos sem acesso. Tente novamente em alguns segundos.")
        except requests.exceptions.Timeout:
            st.error("⏳ O backend demorou muito para responder (timeout).")
        except Exception as e:
            st.error(f"❌ Erro inesperado: {e}")

# ==========================================================
# 📊 DASHBOARD DE MONITORAMENTO
# ==========================================================
st.header("📊 Dashboard de Monitoramento — SmartFin AI Blockchain")

if os.path.exists("data/chain.json"):
    with open("data/chain.json", "r", encoding="utf-8") as f:
        chain_data = json.load(f)
    df = pd.DataFrame(chain_data)

    if not df.empty:
        total = len(df)
        seguras = len(df[df['risco'].str.contains('segura', case=False)])
        medias = len(df[df['risco'].str.contains('médio', case=False)])
        altas = len(df[df['risco'].str.contains('fraude|alto', case=False)])
        ult_hash = df.iloc[-1]['hash'][:20]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Transações Totais", total)
        col2.metric("Seguras", seguras)
        col3.metric("Suspeitas", medias + altas)
        col4.metric("Último Hash", ult_hash)

        st.markdown("---")

        st.subheader("📉 Distribuição de Risco nas Transações")
        risk_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("risco:N", title="Nível de Risco"),
            y=alt.Y("count():Q", title="Quantidade"),
            color=alt.Color("risco:N", legend=None)
        )
        st.altair_chart(risk_chart, use_container_width=True)

        st.subheader("⛓️ Evolução dos Blocos na Blockchain")
        time_chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X("index:Q", title="Índice do Bloco"),
            y=alt.Y("valor:Q", title="Valor (simulado R$)", scale=alt.Scale(domain=(0, 10000))),
            color=alt.Color("risco:N", legend=None)
        ).interactive()
        st.altair_chart(time_chart, use_container_width=True)

        st.subheader("🧾 Histórico Completo de Blocos")
        df_display = df[["index", "transacao", "risco", "hash", "timestamp"]]
        st.dataframe(df_display, use_container_width=True, height=300)
    else:
        st.info("Nenhum bloco encontrado na cadeia.")
else:
    st.info("A blockchain ainda não foi criada. Registre uma transação para iniciar.")

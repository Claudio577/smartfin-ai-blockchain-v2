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
# 🚀 INICIALIZAÇÃO
# ==========================================================
if "modelo" not in st.session_state:
    st.session_state.modelo, st.session_state.label = treinar_modelo()

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
    resultado = analisar_transacao(st.session_state.modelo, st.session_state.label,
                                   valor, pais_origem, pais_destino, hora, historico)
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


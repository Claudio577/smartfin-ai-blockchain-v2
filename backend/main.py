# ==========================================================
# 💎 SmartFin AI Blockchain Backend (FastAPI)
# ==========================================================
# Autor: Claudio Yoshida
# Descrição: API antifraude + blockchain integrada
# ==========================================================

from fastapi import FastAPI
from pydantic import BaseModel
from ai_fraud import treinar_modelo, analisar_transacao
from blockchain import Blockchain

app = FastAPI(
    title="SmartFin AI Blockchain API",
    description="API antifraude + blockchain integrada com IA",
    version="2.0"
)

# ==========================================================
# 🚀 Inicialização
# ==========================================================
modelo, label = treinar_modelo()
blockchain = Blockchain(dificuldade=4)

# ==========================================================
# 🧾 Modelo de entrada da transação
# ==========================================================
class Transacao(BaseModel):
    valor: float
    pais_origem: str
    pais_destino: str
    hora: int
    historico: str

# ==========================================================
# 🔍 Endpoint: Analisar risco de transação
# ==========================================================
@app.post("/analisar")
def analisar(transacao: Transacao):
    resultado = analisar_transacao(
        modelo, label,
        transacao.valor,
        transacao.pais_origem,
        transacao.pais_destino,
        transacao.hora,
        transacao.historico
    )
    return {"resultado": resultado}

# ==========================================================
# ⛓️ Endpoint: Registrar transação na Blockchain
# ==========================================================
@app.post("/registrar")
def registrar(transacao: Transacao):
    resultado = analisar_transacao(
        modelo, label,
        transacao.valor,
        transacao.pais_origem,
        transacao.pais_destino,
        transacao.hora,
        transacao.historico
    )

    blockchain.adicionar_bloco(
        f"{transacao.pais_origem} → {transacao.pais_destino} | R${transacao.valor}",
        resultado
    )
    blockchain.salvar_em_json("data/chain.json")

    return {
        "mensagem": "✅ Transação registrada com sucesso!",
        "risco": resultado
    }

# ==========================================================
# 🌐 Endpoint raiz
# ==========================================================
@app.get("/")
def raiz():
    return {"mensagem": "SmartFin AI Blockchain API v2 ativa ✅"}

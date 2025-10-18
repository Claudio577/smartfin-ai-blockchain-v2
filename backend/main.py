# ==========================================================
# 💎 SmartFin AI Blockchain Backend (FastAPI)
# ==========================================================
# Autor: Claudio Yoshida
# Descrição: API antifraude + blockchain integrada com IA
# Versão: 2.0 (compatível com Streamlit)
# ==========================================================

from fastapi import FastAPI
from pydantic import BaseModel
from ai_fraud import treinar_modelo, analisar_transacao
from blockchain import Blockchain
from fastapi.middleware.cors import CORSMiddleware

# ==========================================================
# ⚙️ Configuração básica
# ==========================================================
app = FastAPI(
    title="SmartFin AI Blockchain API",
    description="API antifraude + blockchain integrada com IA + suporte ao Streamlit",
    version="2.0"
)

# Permite chamadas do Streamlit (CORS liberado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# 🚀 Inicialização dos modelos
# ==========================================================
try:
    modelo, encoders = treinar_modelo()
    blockchain = Blockchain(dificuldade=4)
    print("✅ Modelo e Blockchain inicializados com sucesso!")
except Exception as e:
    print("⚠️ Erro ao inicializar modelo ou blockchain:", e)
    modelo, encoders, blockchain = None, None, None

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
    if not modelo or not encoders:
        return {"erro": "Modelo não inicializado. Reinicie o servidor."}

    try:
        resultado = analisar_transacao(
            modelo, encoders,
            transacao.valor,
            transacao.pais_origem,
            transacao.pais_destino,
            transacao.hora,
            transacao.historico
        )
        return {"resultado": resultado}
    except Exception as e:
        return {"erro": f"Falha ao analisar transação: {str(e)}"}

# ==========================================================
# ⛓️ Endpoint: Registrar transação na Blockchain
# ==========================================================
@app.post("/registrar")
def registrar(transacao: Transacao):
    if not blockchain:
        return {"erro": "Blockchain não inicializada. Reinicie o servidor."}

    try:
        resultado = analisar_transacao(
            modelo, encoders,
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
            "mensagem": "✅ Transação registrada com sucesso na Blockchain!",
            "risco": resultado
        }
    except Exception as e:
        return {"erro": f"Falha ao registrar transação: {str(e)}"}

# ==========================================================
# 🌐 Endpoint raiz
# ==========================================================
@app.get("/")
def raiz():
    return {
        "mensagem": "SmartFin AI Blockchain API v2 ativa ✅",
        "status": "ok",
        "documentação": "/docs"
    }

# ==========================================================
# 🚀 Instrução de execução local (Render usa Start Command)
# ==========================================================
# uvicorn main:app --host 0.0.0.0 --port 10000

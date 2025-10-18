# ==========================================================
# 💎 SmartFin AI Blockchain - Módulo de Blockchain
# ==========================================================
# Autor: Claudio Yoshida
# Descrição: Motor blockchain com Proof of Work, mineração e verificação antifraude.
# ==========================================================

import hashlib
import time
import json
from datetime import datetime

# ==========================================================
# 🧱 CLASSE BLOCO
# ==========================================================
class Bloco:
    def __init__(self, index, transacao, risco, hash_anterior, dificuldade=4):
        self.index = index
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transacao = transacao
        self.risco = risco
        self.hash_anterior = hash_anterior
        self.nonce = 0
        self.hash = self.minerar_bloco(dificuldade)

    # Gera o hash do bloco
    def gerar_hash(self):
        conteudo = (
            str(self.index)
            + str(self.timestamp)
            + str(self.transacao)
            + str(self.risco)
            + str(self.hash_anterior)
            + str(self.nonce)
        )
        return hashlib.sha256(conteudo.encode()).hexdigest()

    # Simula a mineração (Proof of Work)
    def minerar_bloco(self, dificuldade):
        print(f"⛏️ Minerando bloco {self.index}...")
        alvo = "0" * dificuldade
        inicio = time.time()
        while True:
            self.hash = self.gerar_hash()
            if self.hash.startswith(alvo):
                fim = time.time()
                print(
                    f"✅ Bloco {self.index} minerado! Hash: {self.hash[:20]}... ⏱️ Tempo: {fim - inicio:.2f}s\n"
                )
                return self.hash
            self.nonce += 1

    # Converte o bloco em dicionário (para salvar em JSON)
    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transacao": self.transacao,
            "risco": self.risco,
            "hash_anterior": self.hash_anterior,
            "hash": self.hash,
            "nonce": self.nonce,
        }


# ==========================================================
# 🔗 CLASSE BLOCKCHAIN
# ==========================================================
class Blockchain:
    def __init__(self, dificuldade=4):
        self.cadeia = []
        self.dificuldade = dificuldade
        self.criar_bloco_genesis()

    # Primeiro bloco da cadeia
    def criar_bloco_genesis(self):
        bloco_genesis = Bloco(0, "Transação inicial", "Seguro", "0", self.dificuldade)
        self.cadeia.append(bloco_genesis)

    # Adiciona novo bloco (transação analisada pela IA)
    def adicionar_bloco(self, transacao, risco):
        ultimo_bloco = self.cadeia[-1]
        novo_bloco = Bloco(
            len(self.cadeia), transacao, risco, ultimo_bloco.hash, self.dificuldade
        )
        self.cadeia.append(novo_bloco)

    # Verifica integridade da cadeia
    def verificar_integridade(self):
        print("\n🔍 Verificando integridade da blockchain...\n")
        for i in range(1, len(self.cadeia)):
            bloco_atual = self.cadeia[i]
            bloco_anterior = self.cadeia[i - 1]

            if bloco_atual.hash != bloco_atual.gerar_hash():
                print(f"⚠️ O bloco {i} foi alterado!")
                return False
            if bloco_atual.hash_anterior != bloco_anterior.hash:
                print(f"⚠️ O bloco {i} perdeu a ligação com o anterior!")
                return False

        print("✅ Blockchain íntegra — nenhuma alteração detectada.\n")
        return True

    # Exporta blockchain para arquivo JSON
    def salvar_em_json(self, caminho="data/chain.json"):
        dados = [bloco.to_dict() for bloco in self.cadeia]
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"💾 Blockchain salva em {caminho}")

    # Carrega blockchain salva
    def carregar_de_json(self, caminho="data/chain.json"):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.cadeia = []
                for bloco_data in dados:
                    bloco = Bloco(
                        bloco_data["index"],
                        bloco_data["transacao"],
                        bloco_data["risco"],
                        bloco_data["hash_anterior"],
                        self.dificuldade,
                    )
                    bloco.timestamp = bloco_data["timestamp"]
                    bloco.hash = bloco_data["hash"]
                    bloco.nonce = bloco_data["nonce"]
                    self.cadeia.append(bloco)
            print(f"📂 Blockchain carregada de {caminho}")
        except FileNotFoundError:
            print("⚠️ Arquivo de blockchain não encontrado. Criando nova cadeia...")
            self.criar_bloco_genesis()


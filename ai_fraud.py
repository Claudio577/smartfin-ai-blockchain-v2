# ==========================================================
# 🤖 SmartFin AI Blockchain - Módulo de IA Antifraude (v2)
# ==========================================================
# Autor: Claudio Yoshida
# Descrição: Modelo de Machine Learning com dados reais do PaySim
# ==========================================================

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ==========================================================
# 🔍 CARREGAR DADOS REAIS
# ==========================================================
def carregar_dados(caminho="data/transactions.csv"):
    print("📂 Carregando dados reais de transações...")
    df = pd.read_csv(caminho)

    # Validação rápida
    if df.empty:
        raise ValueError("❌ O arquivo transactions.csv está vazio ou inválido.")

    print(f"✅ Dataset carregado com {len(df)} linhas e {len(df.columns)} colunas.")
    return df

# ==========================================================
# 🧠 TREINAMENTO DO MODELO
# ==========================================================
def treinar_modelo():
    df = carregar_dados()

    # Codificar variáveis categóricas
    label = LabelEncoder()
    for col in ["pais_origem", "pais_destino", "historico"]:
        df[col] = label.fit_transform(df[col])

    X = df[["valor", "pais_origem", "pais_destino", "hora", "historico"]]
    y = df["risco"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    print("✅ Modelo antifraude treinado com sucesso usando dados reais.")
    return modelo, label

# ==========================================================
# 🧮 FUNÇÃO DE ANÁLISE DE RISCO
# ==========================================================
def analisar_transacao(modelo, label, valor, pais_origem, pais_destino, hora, historico):
    entrada = pd.DataFrame([{
        "valor": valor,
        "pais_origem": label.transform([pais_origem])[0],
        "pais_destino": label.transform([pais_destino])[0],
        "hora": hora,
        "historico": label.transform([historico])[0]
    }])

    risco_previsto = modelo.predict(entrada)[0]

    if risco_previsto == "baixo":
        emoji = "🟢"
        mensagem = "Transação segura"
    elif risco_previsto == "medio":
        emoji = "🟡"
        mensagem = "Risco médio"
    else:
        emoji = "🔴"
        mensagem = "Suspeita de fraude"

    resultado = f"{emoji} {mensagem}"
    print(f"🔍 Resultado da análise: {resultado}")
    return resultado

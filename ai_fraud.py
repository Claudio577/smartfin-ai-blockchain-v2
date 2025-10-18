# ==========================================================
# 🤖 SmartFin AI Blockchain - Módulo de IA Antifraude
# ==========================================================
# Autor: Claudio Yoshida
# Descrição: Modelo de Machine Learning para análise de risco financeiro.
# ==========================================================

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ==========================================================
# 🔍 GERADOR DE DADOS SINTÉTICOS
# ==========================================================
def gerar_dados_sinteticos(n=300):
    np.random.seed(42)
    dados = pd.DataFrame({
        "valor": np.random.randint(50, 5000, n),
        "pais_origem": np.random.choice(["Brasil", "EUA", "China", "Nigéria", "Alemanha"], n),
        "pais_destino": np.random.choice(["Brasil", "EUA", "China", "Nigéria", "Alemanha"], n),
        "hora": np.random.randint(0, 24, n),
        "historico_cliente": np.random.choice(["bom", "medio", "ruim"], n)
    })

    # Cria um rótulo de risco (simulação)
    risco = []
    for i in range(n):
        if dados.loc[i, "valor"] > 4000 or dados.loc[i, "historico_cliente"] == "ruim":
            risco.append("alto")
        elif dados.loc[i, "valor"] > 2000 or dados.loc[i, "historico_cliente"] == "medio":
            risco.append("medio")
        else:
            risco.append("baixo")

    dados["risco"] = risco
    return dados

# ==========================================================
# 🧠 TREINAMENTO DO MODELO
# ==========================================================
def treinar_modelo():
    df = gerar_dados_sinteticos(500)

    # Codificadores separados por coluna
    encoders = {
        "pais_origem": LabelEncoder(),
        "pais_destino": LabelEncoder(),
        "historico_cliente": LabelEncoder(),
    }

    for col, encoder in encoders.items():
        df[col] = encoder.fit_transform(df[col])

    X = df[["valor", "pais_origem", "pais_destino", "hora", "historico_cliente"]]
    y = df["risco"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    print("✅ Modelo antifraude treinado com sucesso.")
    return modelo, encoders

# ==========================================================
# 🧮 FUNÇÃO DE ANÁLISE DE RISCO
# ==========================================================
def analisar_transacao(modelo, encoders, valor, pais_origem, pais_destino, hora, historico_cliente):
    entrada = pd.DataFrame([{
        "valor": valor,
        "pais_origem": encoders["pais_origem"].transform([pais_origem])[0],
        "pais_destino": encoders["pais_destino"].transform([pais_destino])[0],
        "hora": hora,
        "historico_cliente": encoders["historico_cliente"].transform([historico_cliente])[0]
    }])

    risco_previsto = modelo.predict(entrada)[0]

    if risco_previsto == "baixo":
        emoji, mensagem = "🟢", "Transação segura"
    elif risco_previsto == "medio":
        emoji, mensagem = "🟡", "Risco médio"
    else:
        emoji, mensagem = "🔴", "Suspeita de fraude"

    resultado = f"{emoji} {mensagem}"
    print(f"🔍 Resultado da análise: {resultado}")
    return resultado


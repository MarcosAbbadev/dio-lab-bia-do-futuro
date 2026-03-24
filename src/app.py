import json
import pandas as pd
import requests
import streamlit as st
from pathlib import Path


# Configuracao
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b"

# Definir diretório base
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Carregar dados
perfil = json.load(open(DATA_DIR / 'perfil_investidor.json'))
transacoes = pd.read_csv(DATA_DIR / 'transacoes.csv')
historico = pd.read_csv(DATA_DIR / 'historico_atendimento.csv')
produtos = json.load(open(DATA_DIR / 'produtos_financeiros.json'))

# Montar o Contexto
contexto = f"""
CLENTE: {perfil["nome"]}, {perfil["idade"]} anos, perfil {perfil["perfil_investidor"]}
OBJETIVO: {perfil["objetivo_principal"]}
PATRIMONIO: R$ {perfil["patrimonio_total"]} | RESERVA: R$ {perfil["reserva_emergencia_atual"]}

TRANSACOES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONIVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# Prompt do Sistema
SYSTEM_PROMPT = """Você é o CashEd, mas prefere ser chamado de Ed, um educador financeiro amigável e didático.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos

REGRAS:
1. NUNCA recomende investimentos específicos - apenas explique como funciona;
2. Use os dados fornecidos para dar exemplos personalizados;
3. Linguagem simples, como se explicasse para uma criança;
4. Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
5. Sempre pergunte se o cliente entendeu;
6. Responda de forma direta, com um máximo de 2 paragrafos.
7. JAMAIS responda a perguntas fora do contexto de ensino de finanças pessoais. Quando ocorrer, responda lembrando o seu papel de educador financeiro e redirecione a conversa para o tema de finanças pessoais.
"""

# Chamar Ollama
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']


# Interface
st.title("CashEd, Seu Educador Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta)) 

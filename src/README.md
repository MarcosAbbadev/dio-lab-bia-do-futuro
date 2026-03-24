# Passo a passo de execução

## Setup do Ollama
```bash
# 1. Instalar o Ollama (ollama.com)
# 2. Baixar um modelo leve
ollama pull gpt-oss:20b

# 3. Testar de funciona
ollama run gpt-oss:20b "Olá!"
```

Esta pasta contém o código do seu agente financeiro.

## Código completo

Todo o código-fonte está disponível no arquivo [app.py](./app.py)

## Exemplo de requirements.txt

```
streamlit
openai
python-dotenv
```

## Como Rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
streamlit run .\src\app.py
```

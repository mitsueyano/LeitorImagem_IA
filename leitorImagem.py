import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import ollama
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota principal
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("templates/index.html", "r", encoding="utf-8") as arquivo_html:
        return arquivo_html.read()

# Rota POST
@app.post("/analisar")
async def analisar_imagem(file: UploadFile = File(...)):

    conteudo_imagem = await file.read()

    try:
        max_tentativas = 3
        texto_ia = ""

        for tentativa in range(max_tentativas):
            seed_usado = random.randint(00, 99999)

            resposta = ollama.chat(
                model="moondream",
                messages=[{
                    "role": "user",
                    "content": "Describe this image in few details.",
                    "images": [conteudo_imagem]
                }],
                options={
                    "temperature": 0.3,
                    "top_p": 0.85,
                    "min_p": 0.05,
                    "seed": seed_usado,
                    "num_predict": 150
                }
            )

            texto_ia = resposta['message']['content'].strip()

            if texto_ia:
                # -------------- Tradução pt-br --------------
                #resposta2 = ollama.chat(
                #   model="qwen3.5:2b",
                #   messages=[{
                #       "role": "user",
                #       "content": "Traduza o seguinte texto para pt-br, responda apenas com a tradução, sem comentário: " + resposta['message']['content'],
                #   }],
                #   think=False
                #)
                #texto_ia = resposta2['message']['content'].strip()
                #print(f"content (PT-BR traduzido): {texto_ia}")
                break

        if not texto_ia:
            texto_ia = "Não foi possível gerar uma descrição para esta imagem. Tente novamente."

    except Exception as e:
        print("ERRO COMPLETO:", repr(e))
        texto_ia = f"Erro ao processar imagem no Ollama: {str(e)}"
    return {"descricao": texto_ia}

# Comando para rodar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
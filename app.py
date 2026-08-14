import os
import sys
import webview
import yt_dlp
from flask import Flask, render_template, request

# Configuração de caminhos para o PyInstaller
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/download", methods=['POST'])
def download():
    voltar = '<br><a href="/"><b>Voltar</b></a>'
    try:
        url = request.form.get('url')
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
        return f"Download concluído!{voltar}"
    except Exception as e:
        return f"Erro ao tentar baixar vídeo: {str(e)}.{voltar}"

if __name__ == '__main__':
    # Cria a janela desktop customizada apontando para o servidor Flask
    # Você pode definir o título, largura (width) e altura (height)
    window = webview.create_window(
        title="Download de vídeos", 
        url=app, 
        width=1000, 
        height=700
    )
    
    # Inicia a janela (o pywebview inicia o Flask internamente de forma automática)
    webview.start()


# from flask import Flask, render_template, request
# import yt_dlp

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/download", methods=['POST'])
# def download():
#     voltar = '<br><a href="/"><b>Voltar</b></a>'
#     try:
#         url = request.form.get('url')
#         ydl_opts = {}
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download(url)
#         return f"Download concluído!{voltar}"
#     except Exception as e:
#         return f"Erro ao tentar baixar vídeo: {str(e)}.{voltar}"

# if __name__ == "__main__":
#     app.run(debug=True)
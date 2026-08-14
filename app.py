from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route("/")
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

if __name__ == "__main__":
    app.run(debug=True)
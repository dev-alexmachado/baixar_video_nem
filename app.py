import os
import shutil
import tempfile

from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=['POST'])
def download():
    voltar = '<br><a href="/"><b>Voltar</b></a>'
    url = request.form.get('url')

    if not url:
        return f"URL do vídeo não informada.{voltar}"

    tmpdir = tempfile.mkdtemp(prefix='video_download_')
    output_template = os.path.join(tmpdir, '%(title)s.%(ext)s')
    ydl_opts = {
        'outtmpl': output_template,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        file_path = yt_dlp.YoutubeDL(ydl_opts).prepare_filename(info)

        if not os.path.exists(file_path):
            raise FileNotFoundError('O arquivo do vídeo não foi encontrado após o download.')

        filename = os.path.basename(file_path)
        response = send_file(file_path, as_attachment=True, download_name=filename)

        def cleanup():
            if os.path.exists(file_path):
                os.remove(file_path)
            shutil.rmtree(tmpdir, ignore_errors=True)

        response.call_on_close(cleanup)
        return response
    except Exception as e:
        shutil.rmtree(tmpdir, ignore_errors=True)
        return f"Erro ao tentar baixar vídeo: {str(e)}.{voltar}"


if __name__ == "__main__":
    app.run(debug=True)
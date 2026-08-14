import glob
import os
import shutil
import tempfile

from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)


def get_downloaded_file(folder_path):
    arquivos = sorted(
        glob.glob(os.path.join(folder_path, '*')),
        key=os.path.getmtime,
        reverse=True,
    )
    for item in arquivos:
        if os.path.isfile(item) and not item.endswith('.part') and not item.endswith('.webm.part'):
            return item
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=['POST'])
def download():
    voltar = '<br><a href="/"><b>Voltar</b></a>'
    url = request.form.get('url', '').strip()

    if not url:
        return f"URL do vídeo não informada.{voltar}"

    tmpdir = tempfile.mkdtemp(prefix='video_download_')
    output_template = os.path.join(tmpdir, '%(title)s.%(ext)s')

    ydl_opts = {
        'outtmpl': output_template,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['web', 'android', 'tv_embedded'],
                'player_skip': ['webpage'],
            }
        },
        'format': 'best[ext=mp4]/best',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8'
        },
        'retries': 10,
        'fragment_retries': 10,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)

        file_path = get_downloaded_file(tmpdir)
        if not file_path:
            raise FileNotFoundError('Nenhum arquivo de vídeo foi gerado para download.')

        filename = os.path.basename(file_path)
        response = send_file(file_path, as_attachment=True, download_name=filename)
        response.headers['Content-Disposition'] = (
            f'attachment; filename="{filename}"; '
            f"filename*=UTF-8''{filename.replace(' ', '%20')}"
        )

        def cleanup():
            if os.path.exists(file_path):
                os.remove(file_path)
            shutil.rmtree(tmpdir, ignore_errors=True)

        response.call_on_close(cleanup)
        return response
    except Exception as e:
        shutil.rmtree(tmpdir, ignore_errors=True)
        return f"Erro ao tentar baixar vídeo público: {str(e)}.{voltar}"


if __name__ == "__main__":
    app.run(debug=True)
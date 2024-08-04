from flask import Flask, request, send_from_directory, render_template
import instaloader
import os
import requests

app = Flask(__name__)

# Cria o diretório para os vídeos se não existir
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    loader = instaloader.Instaloader()
    
    try:
        # Obtém o shortcode da URL
        shortcode = url.split('/')[-2]

        # Carrega o post usando o shortcode
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Define o caminho do arquivo
        filename = f"{shortcode}.mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        # Baixa o vídeo
        if post.is_video:
            video_url = post.video_url
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
            else:
                return "Erro ao baixar o vídeo. Status: " + str(response.status_code)
        else:
            return "O link fornecido não é um vídeo."

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)

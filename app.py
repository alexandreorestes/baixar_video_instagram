from flask import Flask, request, Response, render_template, jsonify
import instaloader
import requests
import logging
import io

app = Flask(__name__)

# Configuração do logging
logging.basicConfig(level=logging.DEBUG)

# Configurações do Instaloader
USERNAME = 'xandre.tk@gmail.com'  # Substitua com seu nome de usuário do Instagram
PASSWORD = 'salmos3729'    # Substitua com sua senha do Instagram

@app.route('/')
def index():
    # Renderiza o template HTML para a página principal
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    loader = instaloader.Instaloader()
    
    try:
        # Faz login no Instagram
        loader.login(USERNAME, PASSWORD)
        logging.debug("Autenticado com sucesso")

        # Obtém o shortcode da URL
        shortcode = url.split('/')[-2]
        logging.debug(f"Shortcode extraído: {shortcode}")

        # Carrega o post usando o shortcode
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        logging.debug(f"URL do post: {post.url}")

        # Verifica se o post é um vídeo
        if post.is_video:
            video_url = post.video_url
            logging.debug(f"URL do vídeo: {video_url}")

            # Faz o download do vídeo
            response = requests.get(video_url, stream=True)
            
            # Verifica se a resposta do servidor é bem-sucedida (código 200)
            if response.status_code == 200:
                # Cria um objeto de bytes para o vídeo
                video_stream = io.BytesIO(response.content)
                
                # Define o nome do arquivo para o download
                filename = f"{shortcode}.mp4"

                # Retorna o vídeo como uma resposta de download
                return Response(
                    video_stream,
                    mimetype='video/mp4',
                    headers={"Content-Disposition": f"attachment;filename={filename}"}
                )
            else:
                # Se o download falhar, retorna uma mensagem de erro
                error_msg = f"Erro ao baixar o vídeo. Status: {response.status_code}. URL: {video_url}"
                logging.error(error_msg)
                return jsonify({"success": False, "message": error_msg})
        else:
            # Se o post não for um vídeo, retorna uma mensagem de erro
            error_msg = "O link fornecido não é um vídeo."
            logging.error(error_msg)
            return jsonify({"success": False, "message": error_msg})

    except Exception as e:
        # Captura qualquer outra exceção e retorna uma mensagem de erro
        error_msg = f"Erro: {str(e)}. URL: {url}"
        logging.error(error_msg)
        return jsonify({"success": False, "message": error_msg})

if __name__ == '__main__':
    app.run(debug=True)

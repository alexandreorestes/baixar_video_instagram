document.getElementById('downloadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const url = document.getElementById('url').value;
    const progressDiv = document.getElementById('progress');
    const countdownElem = document.getElementById('countdown');
    const messageDiv = document.getElementById('message');

    // Exibe a área de progresso
    progressDiv.style.display = 'block';
    messageDiv.innerHTML = '';

    // Simula um contador de 10 segundos para mostrar a preparação do vídeo
    let countdown = 10;
    countdownElem.innerText = countdown;

    const interval = setInterval(() => {
        countdown--;
        countdownElem.innerText = countdown;
        if (countdown <= 0) {
            clearInterval(interval);
            countdownElem.innerText = '';
        }
    }, 1000);

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ url: url })
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('Erro ao baixar o vídeo');
        }
    })
    .then(blob => {
        progressDiv.style.display = 'none';  // Esconde a área de progresso

        const videoUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = videoUrl;
        a.download = 'video.mp4';  // Nome padrão do arquivo
        document.body.appendChild(a);
        a.click();
        a.remove();

        // Exibe mensagem de sucesso
        messageDiv.className = 'message success';
        messageDiv.innerHTML = 'Vídeo baixado com sucesso!';
    })
    .catch(error => {
        progressDiv.style.display = 'none';  // Esconde a área de progresso
        messageDiv.className = 'message error';
        messageDiv.innerHTML = `Erro: ${error.message}`;
    });
});

document.getElementById('downloadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const url = document.getElementById('url').value;

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
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'video.mp4';  // Nome padrão do arquivo
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => console.error('Erro:', error));
});

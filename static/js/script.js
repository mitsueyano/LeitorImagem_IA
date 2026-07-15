const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');
const respostaDiv = document.getElementById('resposta');

// Sempre que o usuário escolhe uma nova foto
fileInput.onchange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Mostra a imagem na tela na área de Preview
    const reader = new FileReader();
    reader.onload = (e) => {
        preview.src = e.target.result;
        preview.style.display = 'block';
    };
    reader.readAsDataURL(file);

    respostaDiv.innerHTML = '<span class="analyzing">Analisando imagem...</span>';

    // Prepara e envia a foto para o Python
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/analisar', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) throw new Error('Falha na comunicação com o backend.');

        const data = await response.json();
        
        // Exibie a resposta
        respostaDiv.innerText = data.descricao;

    } catch (error) {
        respostaDiv.innerHTML = `<span style="color: #ef4444;">Erro: ${error.message}</span>`;
    }
};
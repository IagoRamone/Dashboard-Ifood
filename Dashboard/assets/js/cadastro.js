$('form').on('submit', function(e) {
    e.preventDefault(); // Evita o redirecionamento padrão do formulário

    var nome = $('#nome').val();
    var email = $('#email').val();
    var telefone = $('#tel').val();
    var usuario = $('#user').val();
    var senha = $('#senha').val();

    // Envia os dados como JSON para o servidor
    $.ajax({
        url: 'https://deliveryturbo.adezcomunica.com/cadastrar',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            nome: nome,
            email: email,
            tel: telefone,
            user: usuario,
            senha: senha
        }),
        success: function(response) {
            alert(response.message); 
        },
        error: function(xhr) {
            alert('Erro: ' + xhr.responseText);
            console.log('Erro: ' + xhr.responseText);
        }
    });
});

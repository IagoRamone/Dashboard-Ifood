<?php
include 'auth.php'; // Importa a função de autenticação

function listMerchants() {
    $token = getIfoodToken();
    if (!$token) {
        die("Erro ao obter o token.");
    }

    $url = "https://merchant-api.ifood.com.br/merchant/v1.0/merchants";
    $headers = [
        "Authorization: Bearer $token",
        "Content-Type: application/json"
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $response = curl_exec($ch);
    curl_close($ch);

    return json_decode($response, true);
}

// Testando a listagem de merchants
$merchants = listMerchants();
echo "<pre>";
print_r($merchants);
echo "</pre>";
?>

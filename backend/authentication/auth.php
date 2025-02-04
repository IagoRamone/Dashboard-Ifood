<?php

include 'token_manager.php'; // Importa a lógica de gerenciamento de token
    
// OBS: Nesse formato de "token_manager" o token foi armazenado em um file '.json'.
//        Mas pode ser feito tambem com o LocalStorage ou no banco de dados.

function getIfoodToken() {

    $savedToken = getSavedToken();
    if ($savedToken) {
        return $savedToken; // Usa o token salvo se ainda for válido
    }

    // Se não há token salvo ou está expirado, solicita um novo
    $clientId = "SEU_CLIENT_ID";
    $clientSecret = "SEU_CLIENT_SECRET";

    $url = "https://merchant-api.ifood.com.br/authentication/v1.0/oauth/token";
    $data = [
        "grantType" => "client_credentials",
        "clientId" => $clientId,
        "clientSecret" => $clientSecret
    ];

    $headers = ["Content-Type: application/json"];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));

    $response = curl_exec($ch);
    curl_close($ch);

    $result = json_decode($response, true);
    return $result['accessToken'] ?? null;
}

// Testando a autenticação
$token = getIfoodToken();
echo $token ? "Token: $token" : "Falha na autenticação";
?>


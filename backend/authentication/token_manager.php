<?php
define("TOKEN_FILE", "token.json"); // Arquivo para armazenar o token

function getSavedToken() {
    if (!file_exists(TOKEN_FILE)) {
        return null;
    }

    $data = json_decode(file_get_contents(TOKEN_FILE), true);
    if (!$data || time() >= $data['expires_at']) {
        return null; // Token expirado ou inválido
    }

    return $data['access_token'];
}

function saveToken($token, $expires_in) {
    $data = [
        "access_token" => $token,
        "expires_at" => time() + $expires_in // Calcula o timestamp de expiração
    ];
    file_put_contents(TOKEN_FILE, json_encode($data));
}
?>

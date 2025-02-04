<?php
header("Content-Type: application/json"); // Define o tipo de resposta como JSON
include 'auth.php'; // Importa a autenticação

function getMerchantStatus($merchantId) {
    $token = getIfoodToken();
    if (!$token) {
        http_response_code(500);
        echo json_encode(["error" => "Erro ao obter o token"]);
        exit;
    }

    $url = "https://merchant-api.ifood.com.br/merchant/v1.0/merchants/$merchantId/status";
    $headers = [
        "Authorization: Bearer $token",
        "Content-Type: application/json"
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $response = curl_exec($ch);
    curl_close($ch);

    if (!$response) {
        http_response_code(500);
        echo json_encode(["error" => "Erro ao buscar status do merchant"]);
        exit;
    }

    echo $response; // Retorna o JSON original da API
}

$merchantId = $_GET['id'] ?? null;
if (!$merchantId) {
    http_response_code(400);
    echo json_encode(["error" => "ID do Merchant não informado"]);
    exit;
}

getMerchantStatus($merchantId);
?>

<?php
include 'auth.php'; // Importa a autenticação

function getMerchantDetails($merchantId) {
    $token = getIfoodToken();
    if (!$token) {
        die("Erro ao obter o token.");
    }

    $url = "https://merchant-api.ifood.com.br/merchant/v1.0/merchants/$merchantId";
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

// Teste com um merchantId específico
$merchantId = "SEU_MERCHANT_ID";
$merchantDetails = getMerchantDetails($merchantId);

echo "<pre>";
print_r($merchantDetails);
echo "</pre>";
?>

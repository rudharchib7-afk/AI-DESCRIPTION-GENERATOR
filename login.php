<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';
    
    // Simple backend mock
    if ($email === 'admin@example.com' && $password === 'password123') {
        $_SESSION['user'] = $email;
        echo json_encode(['success' => true, 'message' => 'Logged in successfully']);
    } else {
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'Invalid credentials']);
    }
    exit;
}
?>

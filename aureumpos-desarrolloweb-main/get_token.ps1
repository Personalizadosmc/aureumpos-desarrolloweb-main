# Script para obtener token JWT de AureumPOS API

param(
    [string]$Email = "admin@aureumpos.com",
    [string]$Password = "admin123"
)

Write-Host "Obteniendo token JWT..." -ForegroundColor Cyan

$body = @{
    email = $Email
    password = $Password
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "`nToken obtenido exitosamente!" -ForegroundColor Green
    Write-Host "`nInformación del usuario:" -ForegroundColor Yellow
    Write-Host "   Email: $($response.user.email)"
    Write-Host "   Nombre: $($response.user.first_name) $($response.user.last_name)"
    Write-Host "   Es Admin: $($response.user.is_admin)"
    
    Write-Host "`nToken JWT:" -ForegroundColor Yellow
    Write-Host $response.access_token -ForegroundColor White
    
    Write-Host "`nPara usar el token en peticiones:" -ForegroundColor Cyan
    Write-Host '   Headers: Authorization: Bearer ' -NoNewline
    Write-Host $response.access_token -ForegroundColor White
    
    # Guardar token en archivo
    $tokenFile = "token.txt"
    $response.access_token | Out-File -FilePath $tokenFile -Encoding utf8
    Write-Host "`nToken guardado en: $tokenFile" -ForegroundColor Green
    
} catch {
    Write-Host "`nError al obtener token:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host $_.ErrorDetails.Message -ForegroundColor Red
    }
}


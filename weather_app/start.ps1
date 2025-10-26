# お天気取得ツール - 起動スクリプト (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  お天気取得ツール - 起動スクリプト" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# スクリプトのディレクトリに移動
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "[1/3] 仮想環境の確認..." -ForegroundColor Yellow

$pythonPath = $null
if (Test-Path "..\.venv\Scripts\python.exe") {
    $pythonPath = Resolve-Path "..\.venv\Scripts\python.exe"
} elseif (Test-Path "..\venv\Scripts\python.exe") {
    $pythonPath = Resolve-Path "..\venv\Scripts\python.exe"
}

if (-not $pythonPath) {
    Write-Host ""
    Write-Host "エラー: 仮想環境が見つかりません。" -ForegroundColor Red
    Write-Host "環境構築を実行してください。" -ForegroundColor Red
    Write-Host ""
    Read-Host "Enterキーを押して終了してください"
    exit 1
}

Write-Host "[2/3] OpenWeatherMap APIキーの確認..." -ForegroundColor Yellow

$envContent = Get-Content .env -Raw
if ($envContent -match "OPENWEATHER_API_KEY=your_api_key_here") {
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host "⚠️  警告: APIキーが未設定です" -ForegroundColor Red
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host ""
    Write-Host ".envファイルを開いて、OpenWeatherMap APIキーを設定してください。" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "APIキーの取得方法:" -ForegroundColor Cyan
    Write-Host "1. https://home.openweathermap.org/users/sign_up"
    Write-Host "2. アカウント登録後、APIキーを取得"
    Write-Host "3. .envファイルのOPENWEATHER_API_KEYを更新"
    Write-Host ""
    Write-Host "設定後、このスクリプトを再度実行してください。" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Enterキーを押して終了してください"
    exit 1
}

Write-Host "[3/3] アプリケーションを起動中..." -ForegroundColor Yellow
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host "🌤️  お天気取得ツール 起動中..." -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""
Write-Host "ブラウザで以下のURLにアクセスしてください:" -ForegroundColor Cyan
Write-Host "  http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "停止するには Ctrl+C を押してください" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""

# アプリケーション起動
& $pythonPath app.py

Read-Host "Enterキーを押して終了してください"

@echo off
title お天気取得ツール - 開発サーバー
chcp 65001 > nul
echo ========================================
echo   お天気取得ツール - 起動スクリプト
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 仮想環境の確認...
if not exist "..\venv\Scripts\python.exe" (
    if not exist "..\.venv\Scripts\python.exe" (
        echo エラー: 仮想環境が見つかりません。
        echo 環境構築を実行してください。
        pause
        exit /b 1
    )
)

echo [2/3] OpenWeatherMap APIキーの確認...
findstr /C:"OPENWEATHER_API_KEY=your_api_key_here" .env > nul
if %errorlevel% equ 0 (
    echo.
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo ??  警告: APIキーが未設定です
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo.
    echo .envファイルを開いて、OpenWeatherMap APIキーを設定してください。
    echo.
    echo APIキーの取得方法:
    echo 1. https://home.openweathermap.org/users/sign_up
    echo 2. アカウント登録後、APIキーを取得
    echo 3. .envファイルのOPENWEATHER_API_KEYを更新
    echo.
    echo 設定後、このバッチファイルを再度実行してください。
    echo.
    pause
    exit /b 1
)

echo [3/3] アプリケーションを起動中...
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ??  お天気取得ツール 起動中...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo サーバー起動後に既定のブラウザを自動で開きます。
echo 停止するには Ctrl+C を押してください
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM 仮想環境のPythonパスを確認
if exist "..\.venv\Scripts\python.exe" (
    set PYTHON_PATH=..\.venv\Scripts\python.exe
) else (
    set PYTHON_PATH=..\venv\Scripts\python.exe
)

REM アプリケーション起動
"%PYTHON_PATH%" app.py

pause

@echo off
title ���V�C�擾�c�[�� - �J���T�[�o�[
chcp 65001 > nul
echo ========================================
echo   ���V�C�擾�c�[�� - �N���X�N���v�g
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] ���z���̊m�F...
if not exist "..\venv\Scripts\python.exe" (
    if not exist "..\.venv\Scripts\python.exe" (
        echo �G���[: ���z����������܂���B
        echo ���\�z�����s���Ă��������B
        pause
        exit /b 1
    )
)

echo [2/3] OpenWeatherMap API�L�[�̊m�F...
findstr /C:"OPENWEATHER_API_KEY=your_api_key_here" .env > nul
if %errorlevel% equ 0 (
    echo.
    echo ����������������������������������������������������������������������
    echo ??  �x��: API�L�[�����ݒ�ł�
    echo ����������������������������������������������������������������������
    echo.
    echo .env�t�@�C�����J���āAOpenWeatherMap API�L�[��ݒ肵�Ă��������B
    echo.
    echo API�L�[�̎擾���@:
    echo 1. https://home.openweathermap.org/users/sign_up
    echo 2. �A�J�E���g�o�^��AAPI�L�[���擾
    echo 3. .env�t�@�C����OPENWEATHER_API_KEY���X�V
    echo.
    echo �ݒ��A���̃o�b�`�t�@�C�����ēx���s���Ă��������B
    echo.
    pause
    exit /b 1
)

echo [3/3] �A�v���P�[�V�������N����...
echo.
echo ����������������������������������������������������������������������
echo ??  ���V�C�擾�c�[�� �N����...
echo ����������������������������������������������������������������������
echo.
echo �T�[�o�[�N����Ɋ���̃u���E�U�������ŊJ���܂��B
echo ��~����ɂ� Ctrl+C �������Ă�������
echo ����������������������������������������������������������������������
echo.

REM ���z����Python�p�X���m�F
if exist "..\.venv\Scripts\python.exe" (
    set PYTHON_PATH=..\.venv\Scripts\python.exe
) else (
    set PYTHON_PATH=..\venv\Scripts\python.exe
)

REM �A�v���P�[�V�����N��
"%PYTHON_PATH%" app.py

pause

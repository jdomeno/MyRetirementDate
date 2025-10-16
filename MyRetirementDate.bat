@echo off

REM ================================
REM Activar entorno virtual
REM ================================
call C:\Users\%username%\Python_Envs\venv_01\Scripts\activate.bat

REM ================================
REM Ir al directorio donde está dashboard
REM ================================
cd /d "c:\02-GIT\MyRetirementDate\"

REM ================================
REM Ejecutar Streamlit en modo headless
REM (no abre navegador automáticamente)
REM ================================
start "" /B streamlit run app.py --server.headless true

REM ================================
REM Esperar unos segundos para que Streamlit arranque
REM ================================
timeout /t 2 /nobreak >nul

REM ================================
REM Ruta al ejecutable de Chrome
REM ================================
set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"

REM ================================
REM Abrir Chrome en pantalla completa
REM (solo una pestaña, no se repite en cada recálculo)
REM ================================
start "" %CHROME_PATH% --start-fullscreen http://localhost:8501

exit
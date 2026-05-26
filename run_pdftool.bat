@echo off
setlocal
title amaru_fo PDF TOOL
cd /d "%~dp0"

set "INSTALL_DIR=%LOCALAPPDATA%\AmaruFoPdfTool"
set "INSTALL_RUN=%INSTALL_DIR%\abrir_amaru_fo_pdf_tool.bat"

if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" "%~dp0pdftool.py" menu
    goto :end
)

if exist "%INSTALL_RUN%" (
    call "%INSTALL_RUN%"
    goto :eof
)

if exist "%INSTALL_DIR%\.venv\Scripts\python.exe" (
    "%INSTALL_DIR%\.venv\Scripts\python.exe" "%INSTALL_DIR%\pdftool.py" menu
    goto :end
)

echo.
echo =====================================================
echo   amaru_fo PDF TOOL no esta instalado todavia
echo =====================================================
echo.
echo Se abrira el instalador. Cuando termine, se intentara abrir la herramienta.
echo.
pause
call "%~dp0install_windows.bat"

if exist "%INSTALL_RUN%" (
    call "%INSTALL_RUN%"
    goto :eof
)

:end
echo.
echo Puedes cerrar esta ventana.
pause >nul

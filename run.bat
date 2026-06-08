@echo off
where py >nul 2>nul
if %errorlevel%==0 (
    py src\main.py %*
    exit /b %errorlevel%
)

where python >nul 2>nul
if %errorlevel%==0 (
    python src\main.py %*
    exit /b %errorlevel%
)

echo ERRO: Python nao encontrado. Instale o Python ou adicione ao PATH.
exit /b 1

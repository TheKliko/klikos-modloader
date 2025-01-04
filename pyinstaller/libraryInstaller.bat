@echo off
echo running %~nx0...

set "dependencies=requests pypresence pyperclip customtkinter pillow psutil fonttools"
set "libraries=%~dp0..\libraries"


if not exist "%libraries%" (
    mkdir "%libraries%"
)


@REM check if PIP is installed before attempting to use it
where pip >nul 2>&1
if errorlevel 1 (
    goto pipNotInstalled
) else (
    goto pipInstalled
)


:pipNotInstalled
echo ERROR: pip not found!
echo Please make sure Python and pip are installed before trying again
pause
exit /b 1


:pipInstalled
pip install --upgrade --target="%libraries%" %dependencies%
goto end


:end
pause
exit
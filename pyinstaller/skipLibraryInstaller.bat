@echo off
echo running %~nx0...

set "project_name=Kliko's modloader"
set "dependencies=requests pypresence pyperclip customtkinter pillow psutil fonttools"

set "temp=%~dp0temp"
set "bin=%~dp0bin"

set "icon=..\favicon.ico"
set "splash=..\splash.png"

set "root=%~dp0.."
set "libraries=%root%\libraries"
set "modules=%root%\modules"
set "config=%root%\config"
set "resources=%root%\resources"


@REM check if pyinstaller is installed before attempting to use it
where pip >nul 2>&1
if errorlevel 1 (
    goto pyinstallerNotInstalled
) else (
    goto pyinstallerInstalled
)


:pyinstallerNotInstalled
echo ERROR: pyinstaller not found!
echo Please make sure pyinstaller is installed before trying again
pause
exit /b 1


:pyinstallerInstalled
if exist "%temp%" (
    rmdir /s /q "%temp%"
)
mkdir "%temp%"

if exist "%bin%" (
    rmdir /s /q "%bin%"
)
mkdir "%bin%"

echo Running pyinstaller...
pyinstaller ..\main.py ^
--distpath="%bin%" ^
--workpath="%temp%" ^
--specpath="%temp%" ^
--name="executable" ^
--icon="%icon%" ^
--splash="%splash%" ^
--clean --onefile --noconsole ^
--paths="%libraries%" ^
--add-data="%resources%;resources" ^
--add-data="%config%;config"


if exist "%bin%\executable.exe" (
    ren "%bin%\executable.exe" "%project_name%.exe"
)
if exist "%work_path%" (
    rmdir /s /q "%work_path%"
)

goto end


:end
pause
exit
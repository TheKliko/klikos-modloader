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





@REM ChatGPT
REM Find the correct Python installation directory
for /f "delims=" %%i in ('python -c "import sys; print(sys.base_prefix)"') do set "python_path=%%i"

REM Handle missing Python installation
if "%python_path%"=="" (
    echo ERROR: Python is not installed or not in PATH!
    pause
    exit /b 1
)

REM Locate Tcl/Tk dynamically
set "tcl_path=%python_path%\tcl\tcl8.6"
set "tk_path=%python_path%\tcl\tk8.6"

REM Check if Tcl/Tk directories exist
if not exist "%tcl_path%" (
    echo ERROR: Tcl directory not found at "%tcl_path%".
    echo Make sure Tcl is installed with Python.
    pause
    exit /b 1
)

if not exist "%tk_path%" (
    echo ERROR: Tk directory not found at "%tk_path%".
    echo Make sure Tk is installed with Python.
    pause
    exit /b 1
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
if exist "%libraries%" (
    rmdir /s /q "%libraries%"
)
mkdir "%libraries%"
echo Installing libraries...
pip install --upgrade --target="%libraries%" %dependencies%


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
--add-data="%config%;config" ^
--hidden-import=tkinter ^
--add-data="%tcl_path%;lib/tcl8.6" ^
--add-data="%tk_path%;lib/tk8.6"


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
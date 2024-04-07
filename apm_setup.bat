@echo off
net session >nul 2>&1
if %errorlevel% == 0 (
	
    echo Running with administrative privileges.
	"%~dp0Extractor\wget.exe" "https://github.com/VidyutPrabakaran1/apm-repov1/releases/download/v1.0/AI-Password-Manager.zip"
	"%~dp0Extractor\7z.exe" x AI-Password-Manager.zip -o"C:\Program Files"
	"%~dp0Extractor\streams.exe" -d "C:\Program Files\AI-Password-Manager1\AI-Password-Manager.exe" /accepteula
	"%~dp0Extractor\create-shortcut.exe" --work-dir "C:\Program Files\AI-Password-Manager1" --arguments "--myarg=myval" "C:\Program Files\AI-Password-Manager1\AI-Password-Manager.exe" "%USERPROFILE%\Desktop\AI-Password-Manager.lnk"
	echo ""
	echo Installation Complete !
	echo Exiting in 15 seconds. To exit immediately, press Ctrl + C .
	timeout /t 15 /nobreak
	echo ""
	echo Exiting ...
	exit
) else (
    echo Not running with administrative privileges.
    echo Please run the setup as an administrator.
	echo ""
	echo Exiting in 15 seconds. To exit immediately, press Ctrl + C .
	timeout /t 15 /nobreak
	echo ""
	echo Exiting ...
	exit
)
@echo off

setlocal
if exist "%~dp0\python.exe" (
    "%~dp0\python" "%~dp0sensed" %*
) else (
    "%~dp0..\python" "%~dp0sensed" %*
)
endlocal

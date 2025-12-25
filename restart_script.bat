@echo off
setlocal

:retry
python3 scrapetwitterfollowers.py
set exit_code=%errorlevel%

rem Check the exit code
if %exit_code% equ 1 (
    echo All followers scraped.
    goto :end
) else if %exit_code% equ 0 (
    echo Script completed successfully.
    goto :end
) else (
    echo An error occurred. Exit code: %exit_code%
    timeout /t 10 >nul 2>&1
    goto :retry
)

:end
endlocal

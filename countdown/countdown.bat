@echo off
title 2026 DSE Countdown
mode con: cols=5 lines=1

set "target=2026-04-08 08:30:00"

for /f "delims=" %%a in ('powershell -Command "$t=[datetime]'2026-04-08 08:30:00'; $c=Get-Date; $d=$t-$c; [math]::Floor($d.TotalSeconds)"') do (
    set "s_rem=%%a"
)

if not defined s_rem (
    cls
    echo Error: Could not calculate initial time.
    pause
    goto :eof
)


:loop
setlocal
set /a "s_copy=s_rem"

set /a "d=s_copy / 86400"
set /a "s_copy=s_copy %% 86400"
set /a "h=s_copy / 3600"
set /a "s_copy=s_copy %% 3600"
set /a "m=s_copy / 60"
set /a "s=s_copy %% 60"

cls
echo %d%days %h%h %m%m %s%s

endlocal
set /a "s_rem=s_rem - 1"

timeout /t 1 /nobreak >nul
goto loop

:eof
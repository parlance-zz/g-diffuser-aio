@echo off
copy bin\install_or_update.exe .
install_or_update.exe
del install_or_update.exe
pause
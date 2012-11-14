@echo off

echo Si no esta seguro de iniciar la instalacion de 'forestweb' presione Ctrl+c
pause

REM #=========================================================
REM # Instalacion de python
REM #==========================================================

python-2.7.3.msi

REM #=======================================================
REM # Instalacion del codigo de la Aplicacion
REM #=======================================================

mkdir C:\forestal

mkdir C:\forestal\src

xcopy /E ..\..\src C:\forestal\src

mkdir C:\forestal\datainstall

xcopy /E ..\data C:\forestal\datainstall

mkdir C:\forestal\mongodb

mkdir C:\forestal\mongodb\win32

xcopy /E ..\..\mongodb\win32 C:\forestal\mongodb\win32

mkdir C:\forestal\doc

xcopy /E ..\..\doc C:\forestal\doc

copy forestweb.URL "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs

copy forestweb.URL "%USERPROFILE%\Desktop"

echo ::: COPIADA LA APLICACION 'forestal' en C: OK !
pause

REM #=========================================================
REM # Instalacion de la Aplicacion Web como proceso
REM #==========================================================

copy "forestalsrv.bat"  C:\forestal\

copy "forestalini.lnk" "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

echo ::: INSTALADA LA APLICACION WEB COMO SERVIDOR. OK.!

pause

REM #=========================================================
REM # Instalacion de las Bases de Datos
REM #==========================================================

cd C:\forestal\mongodb\win32\

mongorestore --dbpath=data ..\..\datainstall\mongodump

echo ::: GENERADAS LAS BASES DE DATOS. OK  :::
echo ""
echo :::  REINICE SU COMPUTADOR PARA COMPLETAR LA INSTALACION !!! :::
pause
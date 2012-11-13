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

copy forestweb.URL "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs
copy forestweb.URL "%USERPROFILE%\Desktop"

echo ::: COPIADA LA APLICACION 'forestal' en C:
pause

REM #=========================================================
REM # Instalacion de la Aplicacion Web como proceso
REM #==========================================================

copy "forestal.bat" "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

REM C:\Users\windows7\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
echo ::: COPIADO SCRIPT DE EJECUCION DE APLICACION WEB AL MENU INICIO. OK.

pause

REM #=========================================================
REM # Instalacion de las Bases de Datos
REM #==========================================================

cd C:\forestal\mongodb\win32\

mongorestore --dbpath=data ..\..\datainstall\mongodump

REM #mongod --install --auth --dbpath=data  --logpath=log/mongod.log --bind_ip=127.0.0.1 --port=27019 --serviceName=MongoDB

REM #net start MongoDBs

echo ::: GENERADAS LAS BASES DE DATOS. OK
pause

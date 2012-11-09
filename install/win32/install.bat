@echo off

echo Si no esta seguro de iniciar la instalacion de 'forestweb' presione Ctrl+c

pause

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

echo ::: COPIADA LA APLICACION 'forestal' en C:
pause

REM #=========================================================
REM # Instalacion de la Aplicacion Web como proceso
REM #==========================================================

copy "forestal.bat" "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

REM C:\Users\windows7\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
echo ::: COPIADO EL SCRIPT DE EJECUCION DE LA APLICACION WEB AL MENU INICIO. OK.

echo ::: Ejecute el programa 'forestweb' del Menu 'Todos los programas' :::

echo ::: y luego habra el navegador para y dirijase a la direccion: 	:::

echo ::: http://localhost:8080 y empezar a usar la aplicacion.:::
pause

REM #=========================================================
REM # Instalacion de las Bases de Datos
REM #==========================================================

cd C:\forestal\mongodb\win32\

REM mongorestore --dbpath data C:\forestal\datainstall\mongodump
mongorestore --dbpath data ..\..\datainstall\mongodump

echo ::: Generada las Bases de datos. OK
pause
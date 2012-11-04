@echo off

echo Si no esta seguro de iniciar la instalacion de 'forestweb' presione Ctrl+c

pause

REM #=======================================================

REM # Instalacion.

REM #=======================================================

mkdir C:\forestweb

xcopy /E ..\..\src\forestweb\ C:\forestweb

echo ::: COPIADA LA APLICACION 'forestweb' en C:

copy "forestal.bat" "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\"

REM #=========================================================
Instalacion de la Base de Datos
REM #==========================================================
cd C:\forestweb

mongorestore --dbpath mongodb/linux32/data data/mongobackup


echo ::: COPIADO EL SCRIPT DE EJECUCION DE LA APLICACION WEB AL MENU INICIO. OK.

echo ::: Ejecute el programa 'forestweb' del Menu 'Todos los programas' :::

echo ::: y luego habra el navegador para y dirijase a la direccion: 	:::

echo ::: http://localhost:8080 y empezar a usar la aplicacion.			:::

pause
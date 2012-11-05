@echo off

echo Si no esta seguro de iniciar la instalacion de 'forestweb' presione Ctrl+c

pause

REM #=======================================================
REM # Instalacion del codigo de la Aplicacion
REM #=======================================================

mkdir C:\forestweb

xcopy /E ..\..\src\forestweb\ C:\forestweb

echo ::: COPIADA LA APLICACION 'forestweb' en C:

REM #=========================================================
REM # Instalacion de la Base de Datos
REM #==========================================================

cd C:\forestweb\mongodb\win32\

mongorestore --dbpath data C:\forestweb\data\mongobackup

echo ::: Generada la Base de datos. OK

# Pendiente iniciar servidor de BD
mongo localhost:27019/admin --quiet --eval "db.addUser('mongoadmin','humongous')"

echo ::: Agregado el usuario administrador de BD. OK

REM #=========================================================
REM # Instalacion de la Aplicacion Web como proceso
REM #==========================================================

copy "forestal.bat" "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\"

echo ::: COPIADO EL SCRIPT DE EJECUCION DE LA APLICACION WEB AL MENU INICIO. OK.

echo ::: Ejecute el programa 'forestweb' del Menu 'Todos los programas' :::

echo ::: y luego habra el navegador para y dirijase a la direccion: 	:::

echo ::: http://localhost:8080 y empezar a usar la aplicacion.			:::

pause
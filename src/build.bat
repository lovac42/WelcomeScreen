@echo off
set ZIP=C:\PROGRA~1\7-Zip\7z.exe a -tzip -y -r
set REPO=monthly_physical
set NAME=Monthly_Physical
set PACKID=monthly_physical
set VERSION=0.0.2


quick_manifest.exe "%NAME%" "%PACKID%" >%REPO%\manifest.json
echo %VERSION% >%REPO%\VERSION

fsum -r -jm -md5 -d%REPO% * > checksum.md5
move checksum.md5 %REPO%\checksum.md5

%ZIP% %NAME%_v%VERSION%_Anki20.zip *.py %REPO%\*
cd %REPO%
%ZIP% ../%NAME%_v%VERSION%_Anki21.ankiaddon *
%ZIP% ../%NAME%_v%VERSION%_CCBC.adze *

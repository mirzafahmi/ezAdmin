@echo off
setlocal enabledelayedexpansion

echo BACKUP SEQUENCE FOR EZADMIN is running...

REM Set the relative paths from the batch script location
set DB_SOURCE=.\ezAdmin\db.sqlite3
set MEDIA_SOURCE=.\ezAdmin\media
set BACKUP_DIR=.\..\ezAdmin_backup

REM Get the current date and time in the desired format (YYYY-MM-DD_HH:MM:SS)
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set datetime=%%a
set "datetime=!datetime:~0,4!-!datetime:~4,2!-!datetime:~6,2!_!datetime:~8,2!-!datetime:~10,2!-!datetime:~12,2!"

set BACKUP_FOLDER=%BACKUP_DIR%\backup_%datetime%
mkdir %BACKUP_FOLDER%

REM Copy the database file
copy "%DB_SOURCE%" "%BACKUP_FOLDER%"

REM Copy the media folder (recursively)
xcopy "%MEDIA_SOURCE%" "%BACKUP_FOLDER%\media\" /E /I

REM Compress the backup folder using PowerShell
powershell Compress-Archive -Path "%BACKUP_FOLDER%" -DestinationPath "%BACKUP_FOLDER%.zip"

REM Remove the original backup folder
rmdir /s /q "%BACKUP_FOLDER%"

echo BACKUP SEQUENCE FOR EZADMIN completed successfully...
pause

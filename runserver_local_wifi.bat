@echo off
FOR /F "delims=: tokens=2" %%a in ('ipconfig ^| find "IPv4"') do set _IPAddress=%%a

call myenv\Scripts\activate
cd medivenadmin

echo Starting the medivenAdmin server...
start /B python manage.py runserver %_IPAddress%:80
cmd /k
ECHO OFF
ECHO Hello World

cd %userprofile%\downloads

curl "https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe" -o pythonInstall.exe
curl "https://deploy.totallyacdn.com/desktop-apps/2.6.14/Windscribe_2.6.14.exe" -o windscribeInstall.exe

pip install mysql-connector-python

start pythonInstall.exe
start windscribeInstall.exe


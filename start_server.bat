rem start server

call C:\Users\steve\miniconda3\Scripts\activate.bat C:\Users\steve\miniconda3
call conda activate prai310

set FLASK_APP=app.py
set FLASK_ENV=development

flask run -p 1964 -h 192.168.4.43

rem start /b C:\S\bin\ngrok http 1964

rem if %1 == cantor (
rem     echo cantor port %2
rem     REM cantor is 192.168.4.42 uses 1730
rem     flask run -p %2 -h 192.168.4.42
rem ) ELSE (
rem     echo kolmogorov  %2
rem     REM kolmogorov is 4.43 uses 1731
rem )




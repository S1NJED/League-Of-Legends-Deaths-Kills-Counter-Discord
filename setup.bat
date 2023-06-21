@echo off

echo Creation of virutal environment ...
python -m venv .env

echo Activation of the venv ...
call .env\Scripts\activate

echo Installation of required packages ...
pip install -r requirements.txt

echo Starting config.py, follow the instructions ...
python config.py

pause
exit
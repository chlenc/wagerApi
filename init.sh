python3 -m venv venv  
. venv/bin/activate.fish 
which pip
pip install -r ./requirements.txt
export FLASK_ENV=development
export FLASK_APP=main.py
echo use "flask run" to run app

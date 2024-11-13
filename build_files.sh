echo " BUILD START"
Python3.12.2 -m pip install -r requirements.txt
Python3.12.2 manage.py collectstatic --noinput --clear
echo " BUILD END"
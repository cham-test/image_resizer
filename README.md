Для запуска проекта. <br>
python3 -m venv venv <br>
source venv/bin/activate <br>
<br>
Файл requirements.txt был собран с помощью pip freeze, потому если не нужен ipython, conda... etc лучше ввести: <br>
pip install -r requirements_only_needs.txt <br>
или все же: <br>
pip install -r requirements.txt <br>

python manage.py makemigrations && python manage.py migrate <br>
python manage.py runserver
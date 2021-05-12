## Spotify и Youtube проект

### Описание
Основной задачей проекта является загрузка и отображение моих плейлистов,  
а затем последовательный поиск и отображение найденных видео для треков в моих плейлистах.

### Реализация
* В качестве решения основным инструментом является библиотека **[Spotipy](https://spotipy.readthedocs.io/en/latest/#)** и **OAuth авторизация** (для Spotify) и обычные API запросы к Youtube.  
* Помимо указанных в списке requirements.txt библиотек используется Docker и Docker-compose для сборки образа и его запуск в Яндекс.Облаке.  
*ВМ в облаке прерываемая и обычно выключена.*

### Особенности
Проект не завершен, а потому код не приведен к конечному виду.
* Не релизована авторизация (хотя в dev ветке номинально присутствует)
* Не найден метод клиентской авторизации Spotify, чтобы загружать не только свои плейлисты, но и любого пользователя. Только сервер-сервер через OAuth, [увы](https://stackoverflow.com/questions/54436348/spotipy-client-credential-manager-no-token-provided).


## Запуск проекта
```python 
git clone https://github.com/neverd1m/spotify_lists 
git cd spotify_lists

# Опциональное создание отдельного окружения
virtualenv spotify_env
source spotify_env/bin/activate

pip3 install -r requirements.txt
./manage.py makemigrations && migrate
./manage.py runserver # или docker-compose up, если настроен .yml файл.

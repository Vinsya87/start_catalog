# start_catalog

В проекте реализована большая часть функционала каталогов,

это рубрики - записи,

сам каталог с товарами,

портфолио которое можно связать либо с продуктом либо с категорией продуктов,

отзывы как общиие так и к товарам

настройки сайта и сео - своеобразные произвольные поля

корзина, избранное, и сам заказ

отправка почты при заказе есть, но не влючена

отправка простого сообщения с сайта есть

регистрация юзера и тд, в том числе при регистрации перенос избранного и корзины

Юкасса со старого проекта взял, но не включил никак


Инструкция по развертыванию Django-проекта
1. Установка и настройка виртуального окружения

Для Windows:

    Откройте командную строку (cmd) или PowerShell.
    Перейдите в корневую папку вашего проекта.
    Выполните команды:

    python -m venv venv
    venv\Scripts\activate

Для Linux/macOS:

    Откройте терминал.
    Перейдите в корневую папку вашего проекта.
    Выполните команды:

    python3 -m venv venv
    source venv/bin/activate

2. Обновление pip и установка зависимостей

    Обновите pip:

python -m pip install --upgrade pip

Установите зависимости из файла requirements.txt:

    pip install -r requirements.txt

3. Создание файла .env и добавление данных

    В корневой директории вашего проекта создайте файл .env.

    Вставьте в файл следующие данные (замените значения на свои):

<pre class="notranslate">
    <code>
        # Django superuser credentials
    SUPERUSER_NAME='AdminUser'
    SUPERUSER_PASSWORD='SecurePassword123'
    SUPERUSER_EMAIL='admin@example.com'
    
    # Django settings
    SECRET_KEY='django-insecure-examplekey-1234567890abcdefghijklmnopqrstuvwxyz'
    DEBUG=True
    
    # Email settings
    EMAIL_HOST='smtp.example.com'
    EMAIL_PORT=587
    EMAIL_HOST_USER='noreply@example.com'
    EMAIL_HOST_PASSWORD='examplepassword'
    DEFAULT_FROM_EMAIL='noreply@example.com'
    
    </code>
</pre>

4. Создание суперпользователя и начальных данных(если не добавили SUPERUSER_NAME и тд)

    Создайте суперпользователя (вы можете пропустить, если нет необходимости):

python manage.py createsuperuser

Если вы хотите создать суперпользователя автоматически через .env файл, можете использовать специальную команду или скрипт, если таковой предусмотрен.

5. Запуск сервера

    Выполните миграции и запустите сервер:

    
<pre class="notranslate">
    <code>
        cd vinsteam
        python manage.py makemigrations
        python manage.py migrate
        Создайте начальные тестовые данные

        python manage.py create_base
        python manage.py runserver
    
    </code>
</pre>

Теперь ваш проект должен быть развернут и доступен по адресу http://127.0.0.1:8000/. Убедитесь, что все команды выполнены успешно и что приложение работает должным образом. ВОЗМОЖНО НАДО ЗАЙТИ ПОД СУПЕРОМ, И НА ГЛАВНОЙ СТРАНИЦЕ САЙТА В САМОМ ВЕРХУ НАЖАТЬ СБРОСИТЬ ВЕСЬ КЕШ.
либо 

python manage.py clear_cache


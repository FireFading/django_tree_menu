## реализация древовидного меню
### usage
- `{% draw_menu 'main_menu' %}`
### setup
- создайте файл .env по образцу .env.example
### run
- `docker compose up --build -d`
### superuser
- создание аккаунта админа: `docker exec -it django bash -c "python manage.py createsuperuser"`
### linting
- `nox` в корневой директории

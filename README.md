![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

# Сервис FlowerShop

Онлайн сервис и телеграм бота цветочного бизнеса в Красноярске. 

## Установка.
- Python3 должен быть уже установлен.
- Рекомендуется использовать среду окружения [venv](https://docs.python.org/3/library/venv.html) 
для изоляции проекта.
 - Используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей
```console
$ pip install -r requirements.txt
```

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

- `DEBUG=True` — дебаг-режим. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.

- `SECRET_KEY=My Secret Key` — секретный ключ проекта

- `ALLOWED_HOSTS=localhost,127.0.0.1` - Список строк, представляющих имена хоста / домена, которые может обслуживать этот сайт

- `TG_TOKEN=HERE_TOKEN_TELEGRAM_BOT` - Токен ключ телеграм бота

## Запуск

```console
$ python3 manage.py runserver
```

## Цели проекта

Код написан в учебных целях — это командный проект на курсе по Python [Devman](https://dvmn.org).


<img src="https://dvmn.org/assets/img/logo.8d8f24edbb5f.svg" alt= “” width="102" height="25">
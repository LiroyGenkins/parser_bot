# parser_bot

## Описание

На codeforces есть [большая подборка задач](https://codeforces.com/problemset?order=BY_SOLVED_DESC).
Данный парсер написан на scrapy извлекает задачи и их свойства:
+ Темы
+ Количество решений задач
+ Название и номер
+ Сложность задачи

Так же он обеспечивает сохранение в БД PostgreSQL и дополнение, в случае если какой-то задачи нет или изменились её свойства. 
Автоматический парсинг настроен с периодичностью 1 час при помощи apscheduler.
Сам интерфейс взаимодействия реализован через Telegram-бота на pyTelegramBotAPI.

## Основной функционал

1. Получение подборки из 10 задач определенной сложности и тематики, которые распределяются по контестам (наборам задач). Распределение происходит так, чтобы не было пересечений, то есть выбрали тему сортировки и сложность - выдается 10 задач, при этом они принадлежат только этому контесту.
3. Поиск по номеру или названию задачи и выдача всех её свойств.

## Требования

Для запуска бота понабодится:
* Python3.9+
* PostgreSQL 10+ на 5432 порту

## Использование

Данный код предназначен для подключения к существующему телеграмм боту. Поэтому, если такового не имеется, сначала необходимо завести его через `@BotFather` в телеграмме.

## Установка

Установить и запустить код можно выполнив следующие команды:
```
git clone https://github.com/LiroyGenkins/parser_bot.git
cd parser_bot
setup.bat 
python bot.py [ТОКЕН ВАШЕГО БОТА] [ИМЯ ПОЛЬЗОВАТЕЛЯ В БД] [ПАРОЛЬ ПОЛЬЗОВАТЕЛЯ В БД] [ИМЯ БД]
```
Далее следует подождать пару минут пока произойдёт первый парсинг и запись в БД, затем можно пользоваться ботом, повторный парсинг будет происходить в фоновом режиме.

(в скором времени планируется обернуть всё в docker-compose)


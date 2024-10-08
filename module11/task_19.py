"""
Задача - Книжный магазин
Напишите небольшое приложение которые имитирует работу книжного магазина, оперируем
всего двумя объектами - книгой и автором.

Объект книги:
id (int)
title (str)
author (id)
count (int) - остаток книг на складе

Объект автор:
id (int)
first_name (str)
last_name (str)

Приложение должно реализовывать следующее апи:
GET /api/books - возвращает список книг
POST /api/books - создает новую книгу
PUT /api/books/{id} - редактирует книгу
POST /api/books/{id}/buy - апи для покупки книги, уменьшает счетчик count если он положительный или возвращает ошибку

GET /api/authors - возвращает список авторов, для каждого автора отдаем список его книг (только названия)
POST /api/authors - создает нового автора
PUT /api/authors/{id} - редактирует автора
"""

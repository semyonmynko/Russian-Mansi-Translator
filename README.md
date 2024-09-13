# Русско-Мансийский Переводчик

Данный репозиторий содержит **source code** для русско-мансийского переводчика.

## Как запустить
Переводчик работает по ссылке http://89.169.133.146 (Лучше открывать в браузере Chrome в режиме инкогнито)

Чтобы запустить проект локально, воспользуйтесь гайдом в файле [howto.txt](howto.txt).

## Функционал
Переводчик имеет следующий функционал:
- Перевод с русского на мансийский и с мансийского на русский с помощью дообученной модели facebook/m2m100_418M.
- Поиск предложений, содержащих искомое слово/фразу.
- Словарь.
- Раздел "полезные материалы", содержащий литературу, связанную с мансийским языком (словари, учебники), а так же видео-курс мансийского языка.
- Тематический корпус, содержащий 20 разделов: разделы были получены путем кластеризации эмбеддингов предложений методом k-средних. Эмбеддинги были получены с помощью модели text2vec. Поиск по тематическому корпусу выдает 10 случайных предложений по заданной тематике.

## Документация

- [translation_approaches.pdf](research/translation_approaches.pdf) — информация об изученных статьях, моделях и подходах, выбранных для создания нашей модели.
- EDA.pdf — анализ данных, предоставленных кейсодателем, а также собранных нами.

## Исследования

В папке **research** можно найти:
- Пайплайны обучения моделей
- Генерацию синтетических данных
- Topic modelling для создания тематического корпуса из имеющихся предложений

## Метод для перевода с использованием API

Используйте следующий cURL-запрос для перевода:

```bash
curl -X 'POST' \
  'http://89.169.133.146/translate' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your_actual_api_token' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Собака",
  "source_lang": "russian",
  "target_lang": "mansi"
}'
```
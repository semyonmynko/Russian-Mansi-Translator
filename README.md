# Русско-Мансийский Переводчик

Данный репозиторий содержит **source code** для русско-мансийского переводчика.

## Как запустить

Чтобы запустить проект, воспользуйтесь гайдом в файле [howto.txt](howto.txt).

## Документация

- translation_approaches.pdf — информация об изученных статьях, моделях и подходах, выбранных для создания нашей модели.
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
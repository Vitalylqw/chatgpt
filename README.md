# chatgpt REST API Example

Пример сервиса на базе FastAPI, который принимает PDF или изображение,
отправляет содержимое в API OpenAI и возвращает JSON с данными документа.

## Запуск

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Укажите ключ API в переменной окружения `OPENAI_API_KEY`.
3. Запустите сервер:
   ```bash
   python main.py
   ```

POST запрос на `/parse` с файлом вернёт JSON‑ответ модели.

# MLOps Factory

## Локальный запуск и отладка

1.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Настройте переменные окружения:**
    ```bash
    cp .env.example .env
    # Заполните .env файл необходимыми значениями
    ```

4.  **Настройте креды для DVC S3:**
    ```bash
    dvc remote modify --local s3-origin access_key_id $S3_ACCESS_KEY_ID
    dvc remote modify --local s3-origin secret_access_key $S3_SECRET_ACCESS_KEY
    dvc pull
    ```

5.  **Обучите модель:**
    ```bash
    dvc repro
    ```

6.  **Запустите API-сервер:**
    ```bash
    uvicorn app:app --reload --port 8000
    ```

7.  **Отправьте тестовый запрос:**
    Откройте второй терминал и выполните следующий `curl` запрос для проверки эндпоинта `/predict`.

    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/predict' \
      -H 'Content-Type: application/json' \
      -d '{ 
        "MedInc": 8.3, 
        "HouseAge": 41, 
        "AveRooms": 6.9, 
        "AveBedrms": 1, 
        "Population": 322, 
        "AveOccup": 2.5, 
        "Latitude": 37.8, 
        "Longitude": -122.2 
      }'
    ```

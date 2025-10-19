# MLOps Factory

Проект для изучения жизненного цикла ML-моделей.

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

3.  **Обучите модель (если `model.pkl` отсутствует):**
    ```bash
    python train.py
    ```

4.  **Запустите API-сервер:**
    ```bash
    uvicorn app:app --reload --port 8000
    ```

5.  **Отправьте тестовый запрос:**
    Откройте второй терминал и выполните следующий `curl` запрос для проверки эндпоинта `/predict`.

    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/predict' \
      -H 'Content-Type: application/json' \
      -d 
'{ 
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
